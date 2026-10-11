// Profiles Macro App main (inspector 9339) and main renderer (DevTools 9224) in CHUNK-second slices
// for up to DURATION seconds. Every slice is saved (chunk-N-<proc>.cpuprofile + summary.txt appended)
// so closing the app early still leaves data. Usage: node profile-macro-app.mjs <outDir> [duration] [chunk]
import fs from 'node:fs';
import path from 'node:path';

const OUT = process.argv[2];
const DURATION = Number(process.argv[3] || 300);
const CHUNK = Number(process.argv[4] || 10);
fs.mkdirSync(OUT, { recursive: true });
const log = (m) => { fs.appendFileSync(path.join(OUT, 'progress.log'), `${new Date().toISOString()} ${m}\n`); };
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

async function json(url, tries = 900) {
  for (let i = 0; i < tries; i += 1) {
    try { const r = await fetch(url, { signal: AbortSignal.timeout(3000) }); return await r.json(); } catch { await sleep(1000); }
  }
  throw new Error(`no answer from ${url}`);
}

function session(wsUrl, name) {
  const ws = new WebSocket(wsUrl);
  let id = 0; const pending = new Map();
  let closed = false;
  ws.onmessage = (ev) => { const m = JSON.parse(ev.data); if (m.id && pending.has(m.id)) { pending.get(m.id)(m); pending.delete(m.id); } };
  ws.onclose = () => { closed = true; for (const res of pending.values()) res(null); pending.clear(); };
  const opened = new Promise((res, rej) => { ws.onopen = res; ws.onerror = rej; });
  const send = (method, params = {}, timeoutMs = 60000) => new Promise((res) => {
    if (closed) { res(null); return; }
    id += 1; const myId = id; pending.set(myId, res);
    try { ws.send(JSON.stringify({ id: myId, method, params })); } catch { pending.delete(myId); res(null); return; }
    setTimeout(() => { if (pending.has(myId)) { pending.delete(myId); res(null); } }, timeoutMs);
  });
  return { opened, send, name, isClosed: () => closed };
}

function summarize(profile, label) {
  const self = new Map(); const byId = new Map(profile.nodes.map((n) => [n.id, n]));
  const dt = profile.timeDeltas; const counts = new Map();
  profile.samples.forEach((s, i) => counts.set(s, (counts.get(s) || 0) + (dt[i] || 0)));
  for (const [nid, us] of counts) {
    const cf = byId.get(nid).callFrame;
    const key = `${cf.functionName || '(anon)'} ${cf.url.split('/').slice(-2).join('/')}:${cf.lineNumber + 1}`;
    self.set(key, (self.get(key) || 0) + us);
  }
  const top = [...self.entries()].sort((a, b) => b[1] - a[1]).slice(0, 30);
  const parent = new Map(); profile.nodes.forEach((n) => (n.children || []).forEach((c) => parent.set(c, n.id)));
  const hotNodes = [...counts.entries()].sort((a, b) => b[1] - a[1]).slice(0, 10).map(([nid, us]) => {
    const chain = []; let cur = nid;
    while (cur && chain.length < 40) { const cf = byId.get(cur).callFrame; chain.push(`${cf.functionName || '(anon)'}@${cf.url.split('/').pop()}:${cf.lineNumber + 1}`); cur = parent.get(cur); }
    return `${(us / 1e6).toFixed(2)}s  ${chain.join(' <- ')}`;
  });
  return `== ${label} top self time ==\n${top.map(([k, us]) => `${(us / 1e6).toFixed(2)}s  ${k}`).join('\n')}\n== ${label} hottest stacks ==\n${hotNodes.join('\n')}\n`;
}

const mainList = await json('http://127.0.0.1:9339/json/list');
log('main inspector up');
const main = session(mainList[0].webSocketDebuggerUrl, 'main');
await main.opened;
await main.send('Profiler.enable'); await main.send('Profiler.setSamplingInterval', { interval: 1000 });

let renderer = null;
async function attachRenderer() {
  try {
    const list = await json('http://127.0.0.1:9224/json/list', 1);
    const page = list.find((t) => t.type === 'page' && /localhost:53\d\d/.test(t.url));
    if (!page) return;
    const s = session(page.webSocketDebuggerUrl, 'renderer'); await s.opened;
    await s.send('Profiler.enable'); await s.send('Profiler.setSamplingInterval', { interval: 1000 });
    renderer = s; log('renderer attached');
  } catch { /* retry next chunk */ }
}

const startedAt = Date.now();
let chunk = 0;
while (Date.now() - startedAt < DURATION * 1000 && !main.isClosed()) {
  chunk += 1;
  if (!renderer || renderer.isClosed()) { renderer = null; await attachRenderer(); }
  const active = [main, renderer].filter(Boolean);
  for (const s of active) await s.send('Profiler.start', {}, 15000);
  log(`chunk ${chunk} started (${active.map((s) => s.name).join('+')})`);
  await sleep(CHUNK * 1000);
  for (const s of active) {
    const res = await s.send('Profiler.stop', {}, 60000);
    if (!res?.result?.profile) { log(`chunk ${chunk} ${s.name}: no profile`); continue; }
    fs.writeFileSync(path.join(OUT, `chunk-${chunk}-${s.name}.cpuprofile`), JSON.stringify(res.result.profile));
    let text = summarize(res.result.profile, `chunk ${chunk} ${s.name}`);
    const heap = await s.send('Runtime.getHeapUsage', {}, 15000);
    if (heap?.result) text += `${s.name} heap used ${(heap.result.usedSize / 1e6).toFixed(0)} MB / total ${(heap.result.totalSize / 1e6).toFixed(0)} MB\n`;
    fs.appendFileSync(path.join(OUT, 'summary.txt'), `\n### ${new Date().toISOString()}\n${text}`);
    log(`chunk ${chunk} ${s.name} saved`);
  }
}
log('done');
process.exit(0);
