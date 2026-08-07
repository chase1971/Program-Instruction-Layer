/**
 * FILE: scripts/scorecard-enforce.js
 * PURPOSE: Force scorecard bumps to actually happen, instead of relying on the agent
 *          remembering an always-on prose instruction (which was the failure Chase hit —
 *          a whole session with real edits and zero bumps).
 *
 * Two modes, one script so the "is there unbumped work" check has one home:
 *   --stop        Stop hook. Blocks the agent from ending its turn when there's clear
 *                 evidence of unbumped work. Capped at MAX_BLOCKS consecutive blocks,
 *                 then force-allows — this can never trap the session.
 *   --precompact  PreCompact hook. Non-blocking (Stop is the only hook here allowed to
 *                 block). Injects a reminder before compaction, since the running-tally
 *                 counts already survive compaction (written to disk on every tool call)
 *                 but the agent's memory that it needs to bump does not.
 *
 * Fails open on every path: missing file, unparsable JSON, write error, unknown mode.
 * A bug in this script must never be the reason Chase can't get a response.
 *
 * Manual smoke test:
 *   echo '{}' | node scripts/scorecard-enforce.js --stop
 *   echo '{}' | node scripts/scorecard-enforce.js --precompact
 */
'use strict';

const fs = require('fs');
const path = require('path');

const ROOT = path.join(__dirname, '..');
const RUNNING = path.join(ROOT, 'agent docs', '.session-scorecard-running.json');

const MIN_TURNS = 3;
const MIN_EDITED_FILES = 2;
const MAX_BLOCKS = 3;

function readRunning() {
  if (!fs.existsSync(RUNNING)) {
    return null;
  }
  try {
    return JSON.parse(fs.readFileSync(RUNNING, 'utf8'));
  } catch {
    return null;
  }
}

function writeRunning(data) {
  try {
    fs.writeFileSync(RUNNING, JSON.stringify(data, null, 2), 'utf8');
  } catch {
    // Fail open — a write failure must never be why a turn gets blocked.
  }
}

function unbumpedState(running) {
  const edited = Array.isArray(running.filesEditedList) ? running.filesEditedList.length : 0;
  const bumps = Array.isArray(running.taskLog) ? running.taskLog.length : 0;
  const turns = Number(running.turns) || 0;
  return { edited, bumps, turns, looksUnbumped: edited >= MIN_EDITED_FILES && bumps === 0 };
}

function printAndExit(obj) {
  process.stdout.write(JSON.stringify(obj || {}));
  process.exit(0);
}

function runStop() {
  const running = readRunning();
  if (!running) {
    return printAndExit();
  }

  const { edited, bumps, turns, looksUnbumped } = unbumpedState(running);
  const blocks = Number(running.stopBlockCount) || 0;
  const shouldBlock = looksUnbumped && turns >= MIN_TURNS && blocks < MAX_BLOCKS;

  if (!shouldBlock) {
    if (blocks > 0) {
      running.stopBlockCount = 0;
      writeRunning(running);
    }
    return printAndExit();
  }

  running.stopBlockCount = blocks + 1;
  writeRunning(running);

  const message =
    `Session scorecard: ${edited} file(s) edited this session, ${bumps} bumps logged. `
    + 'Before finishing, run node scripts/append-session-scorecard.js --bump-file <path> '
    + '(see agent docs/SESSION_SCORECARD.md) with a chunkNote for the work just done, '
    + 'then finish your reply normally. '
    + `(This auto-allows after ${MAX_BLOCKS} reminders regardless, so it can't loop forever.)`;

  printAndExit({
    decision: 'block',
    reason: message,
    followup_message: message,
  });
}

function runPrecompact() {
  const running = readRunning();
  if (!running) {
    return printAndExit();
  }

  const { edited, bumps } = unbumpedState(running);
  if (edited === 0 || bumps > 0) {
    return printAndExit();
  }

  printAndExit({
    hookSpecificOutput: {
      hookEventName: 'PreCompact',
      additionalContext:
        `Compaction is about to summarize this conversation. ${edited} file(s) have been `
        + 'edited so far with 0 scorecard bumps logged. Run node scripts/append-session-scorecard.js '
        + '--bump-file <path> now, before detail about the work gets summarized away.',
    },
  });
}

function main() {
  try {
    if (process.argv.includes('--stop')) {
      return runStop();
    }
    if (process.argv.includes('--precompact')) {
      return runPrecompact();
    }
    printAndExit();
  } catch {
    // Fail open — never block, never crash the hook chain.
    try {
      printAndExit();
    } catch {
      process.exit(0);
    }
  }
}

main();
