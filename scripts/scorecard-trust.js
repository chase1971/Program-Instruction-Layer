/**
 * Shared counts-trust flags for session scorecard running tally + finalize.
 * Used by scorecard-hook-tally.js and append-session-scorecard.js.
 */
'use strict';

/**
 * @param {object} r running or finalized entry fields
 * @returns {object} same object, mutated
 */
function refreshCountsTrust(r) {
  if (!r || typeof r !== 'object') {
    return r;
  }

  const bumped = !!(r.agentBumped || r.bumped === true);
  const taskChunks = Array.isArray(r.taskLog)
    ? r.taskLog.length
    : Number(r.taskBumpCount) || 0;
  const hook = !!r.hookTally;
  const summarized = !!r.summarized;

  if (hook && !r.hookFirstTallyAt) {
    r.hookFirstTallyAt = new Date().toISOString();
    r.preHookWorkUntracked = true;
  }

  r.missingEarlyWork = !!(
    r.preHookWorkUntracked
    || summarized
    || (hook && !bumped)
    || (hook && bumped && taskChunks < 1)
  );

  if (summarized && !bumped && !hook) {
    r.countsTrust = 'low';
  } else if (summarized && taskChunks < 1) {
    r.countsTrust = 'low';
  } else if (r.missingEarlyWork && !bumped) {
    r.countsTrust = 'low';
  } else if (summarized || r.preHookWorkUntracked || (hook && taskChunks < 1)) {
    r.countsTrust = 'medium';
  } else if (bumped && taskChunks >= 1) {
    r.countsTrust = summarized ? 'medium' : 'high';
  } else {
    r.countsTrust = 'low';
  }

  return r;
}

function emptyTrustFields() {
  return {
    hookFirstTallyAt: null,
    preHookWorkUntracked: false,
    missingEarlyWork: false,
    countsTrust: 'low',
    summarized: false,
  };
}

module.exports = { refreshCountsTrust, emptyTrustFields };
