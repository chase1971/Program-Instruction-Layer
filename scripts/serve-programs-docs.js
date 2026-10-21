/**
 * Serve Programs/docs/, agent docs/, and School documents on a fixed localhost port
 * so chat http:// links open in a browser.
 * Usage: node scripts/serve-programs-docs.js
 * Then open: http://127.0.0.1:8765/context-engineering-infographic.html
 *
 * Writable POST endpoints (agents read the files on disk):
 * - POST /__comments/<page path> → <page>.comments.json beside the page
 * - POST /__registry/sync-pull-registry → agent docs/sync-pull-registry.json
 * - POST /__layout/factoring-guided-portal → agent docs/scratch/factoring-guided-layout-latest.json
 * - POST /__layout/factoring-guided-portal/journal → agent docs/scratch/factoring-guided-layout-journal.json
 * - GET/POST /__layout/build/<appId> → that app's source buildLayout.json (allowlisted)
 * Detail: agent docs/rules/html-delivery.md
 */
'use strict';

const http = require('http');
const fs = require('fs');
const path = require('path');
const {
  resolveBuildLayoutAppId,
  resolveBuildLayoutPath,
  isBuildLayout,
  layoutForWrite,
} = require('./build-layout-docs-route');

const PORT = 8765;
const DOCS = path.join(__dirname, '..', 'docs');
const AGENT_DOCS = path.join(__dirname, '..', 'agent docs');
const SCHOOL_DOCS_CANDIDATES = [
  path.join(__dirname, '..', 'School Scrips', 'School documents'),
  path.join(__dirname, '..', 'School Scripts', 'School documents'),
];
const SCHOOL_DOCS = SCHOOL_DOCS_CANDIDATES.find((dir) => fs.existsSync(dir)) || SCHOOL_DOCS_CANDIDATES[0];
// School documents first so teaching HTML (exam maps) wins over agent-docs stubs
const SERVE_ROOTS = [SCHOOL_DOCS, DOCS, AGENT_DOCS];

const MIME = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.png': 'image/png',
  '.svg': 'image/svg+xml',
  '.pdf': 'application/pdf',
  '.mp4': 'video/mp4',
};

function resolveFile(rel) {
  const clean = rel.replace(/^\//, '');
  for (const root of SERVE_ROOTS) {
    const file = path.normalize(path.join(root, clean));
    if (!file.startsWith(root)) {
      continue;
    }
    if (fs.existsSync(file) && fs.statSync(file).isFile()) {
      return file;
    }
  }
  return null;
}

const COMMENTS_PREFIX = '/__comments/';
const COMMENTS_SUFFIX = '.comments.json';
const REGISTRY_SAVE_PATH = '/__registry/sync-pull-registry';
const REGISTRY_FILE = path.join(AGENT_DOCS, 'sync-pull-registry.json');
const FACTORING_LAYOUT_SAVE_PATH = '/__layout/factoring-guided-portal';
const FACTORING_LAYOUT_JOURNAL_SAVE_PATH = '/__layout/factoring-guided-portal/journal';
const FACTORING_LAYOUT_FILE = path.join(
  AGENT_DOCS,
  'scratch',
  'factoring-guided-layout-latest.json',
);
const FACTORING_LAYOUT_JOURNAL_FILE = path.join(
  AGENT_DOCS,
  'scratch',
  'factoring-guided-layout-journal.json',
);
const MAX_COMMENT_BODY = 512 * 1024;
const MAX_REGISTRY_BODY = 256 * 1024;
const MAX_LAYOUT_BODY = 512 * 1024;

function jsonCorsHeaders() {
  return {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
  };
}

/**
 * Where a page's comments file lives: beside the page, in whichever served root
 * holds it. Returns null for anything that is not an existing .html page.
 */
function resolveCommentsFile(rel) {
  const clean = rel.replace(/^\//, '');
  if (!clean.toLowerCase().endsWith('.html') || clean.includes('\0')) {
    return null;
  }
  const page = resolveFile(`/${clean}`);
  if (!page) {
    return null;
  }
  return page.replace(/\.html$/i, '') + COMMENTS_SUFFIX;
}

function handleSaveComments(req, res, rel) {
  const target = resolveCommentsFile(rel);
  if (!target) {
    res.writeHead(404, { 'Content-Type': 'application/json' });
    res.end('{"ok":false,"error":"no such page"}');
    return;
  }

  let body = '';
  let tooBig = false;
  req.on('data', (chunk) => {
    body += chunk;
    if (body.length > MAX_COMMENT_BODY) {
      tooBig = true;
      req.destroy();
    }
  });
  req.on('end', () => {
    if (tooBig) {
      res.writeHead(413, { 'Content-Type': 'application/json' });
      res.end('{"ok":false,"error":"too large"}');
      return;
    }
    let parsed;
    try {
      parsed = JSON.parse(body || '{}');
    } catch {
      res.writeHead(400, { 'Content-Type': 'application/json' });
      res.end('{"ok":false,"error":"bad json"}');
      return;
    }
    try {
      fs.writeFileSync(target, JSON.stringify(parsed, null, 2) + '\n', 'utf8');
      console.log(`comments saved: ${path.basename(target)}`);
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ ok: true, file: path.basename(target) }));
    } catch (err) {
      res.writeHead(500, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ ok: false, error: String(err.message || err) }));
    }
  });
}

function handleSavePullRegistry(req, res) {
  let body = '';
  let tooBig = false;
  req.on('data', (chunk) => {
    body += chunk;
    if (body.length > MAX_REGISTRY_BODY) {
      tooBig = true;
      req.destroy();
    }
  });
  req.on('end', () => {
    if (tooBig) {
      res.writeHead(413, { 'Content-Type': 'application/json' });
      res.end('{"ok":false,"error":"too large"}');
      return;
    }
    let parsed;
    try {
      parsed = JSON.parse(body || '{}');
    } catch {
      res.writeHead(400, { 'Content-Type': 'application/json' });
      res.end('{"ok":false,"error":"bad json"}');
      return;
    }
    if (!parsed || parsed.version !== 1 || !Array.isArray(parsed.repos)) {
      res.writeHead(400, { 'Content-Type': 'application/json' });
      res.end('{"ok":false,"error":"invalid registry shape"}');
      return;
    }
    for (const r of parsed.repos) {
      if (!r || typeof r.path !== 'string' || typeof r.pull !== 'boolean') {
        res.writeHead(400, { 'Content-Type': 'application/json' });
        res.end('{"ok":false,"error":"each repo needs path and pull boolean"}');
        return;
      }
    }
    parsed.updated = new Date().toISOString();
    try {
      fs.writeFileSync(REGISTRY_FILE, JSON.stringify(parsed, null, 2) + '\n', 'utf8');
      console.log('sync-pull-registry saved');
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ ok: true }));
    } catch (err) {
      res.writeHead(500, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ ok: false, error: String(err.message || err) }));
    }
  });
}

function handleSaveFactoringLayoutJournal(req, res) {
  let body = '';
  let tooBig = false;
  req.on('data', (chunk) => {
    body += chunk;
    if (body.length > MAX_LAYOUT_BODY) {
      tooBig = true;
      req.destroy();
    }
  });
  req.on('end', () => {
    if (tooBig) {
      res.writeHead(413, jsonCorsHeaders());
      res.end('{"ok":false,"error":"too large"}');
      return;
    }
    let parsed;
    try {
      parsed = JSON.parse(body || '{}');
    } catch {
      res.writeHead(400, jsonCorsHeaders());
      res.end('{"ok":false,"error":"bad json"}');
      return;
    }
    if (!parsed || parsed.version !== 1 || !Array.isArray(parsed.entries)) {
      res.writeHead(400, jsonCorsHeaders());
      res.end('{"ok":false,"error":"need version 1 and entries[]"}');
      return;
    }
    try {
      fs.mkdirSync(path.dirname(FACTORING_LAYOUT_JOURNAL_FILE), { recursive: true });
      parsed.updatedAt = parsed.updatedAt || new Date().toISOString();
      fs.writeFileSync(
        FACTORING_LAYOUT_JOURNAL_FILE,
        JSON.stringify(parsed, null, 2) + '\n',
        'utf8',
      );
      console.log('factoring guided layout journal synced');
      res.writeHead(200, jsonCorsHeaders());
      res.end(JSON.stringify({ ok: true, entries: parsed.entries.length }));
    } catch (err) {
      res.writeHead(500, jsonCorsHeaders());
      res.end(JSON.stringify({ ok: false, error: String(err.message || err) }));
    }
  });
}

function readJsonBody(req, maxBytes) {
  return new Promise((resolve, reject) => {
    let body = '';
    let tooBig = false;
    req.on('data', (chunk) => {
      body += chunk;
      if (body.length > maxBytes) {
        tooBig = true;
        req.destroy();
      }
    });
    req.on('end', () => {
      if (tooBig) {
        reject(Object.assign(new Error('too large'), { statusCode: 413 }));
        return;
      }
      try {
        resolve(JSON.parse(body || '{}'));
      } catch {
        reject(Object.assign(new Error('bad json'), { statusCode: 400 }));
      }
    });
    req.on('error', (err) => {
      reject(err);
    });
  });
}

function sendJson(res, statusCode, payload) {
  res.writeHead(statusCode, jsonCorsHeaders());
  res.end(JSON.stringify(payload));
}

function handleBuildLayout(req, res, appId) {
  const target = resolveBuildLayoutPath(appId);
  if (!target) {
    sendJson(res, 404, { ok: false, error: `unknown Build app: ${appId}` });
    return;
  }

  if (req.method === 'GET') {
    let raw;
    try {
      raw = fs.readFileSync(target, 'utf8');
    } catch (err) {
      sendJson(res, 500, { ok: false, error: String(err.message || err) });
      return;
    }
    let parsed;
    try {
      parsed = JSON.parse(raw);
    } catch {
      sendJson(res, 500, { ok: false, error: 'layout file is not valid json' });
      return;
    }
    if (!isBuildLayout(parsed)) {
      sendJson(res, 500, { ok: false, error: 'layout file has an invalid shape' });
      return;
    }
    sendJson(res, 200, { ok: true, layout: parsed });
    return;
  }

  readJsonBody(req, MAX_LAYOUT_BODY)
    .then((incoming) => {
      let current = null;
      try {
        current = JSON.parse(fs.readFileSync(target, 'utf8'));
      } catch (err) {
        sendJson(res, 500, { ok: false, error: String(err.message || err) });
        return;
      }
      const next = layoutForWrite(current, incoming, appId);
      if (!next.ok) {
        sendJson(res, 400, { ok: false, error: next.error });
        return;
      }
      fs.writeFileSync(target, JSON.stringify(next.layout, null, 2) + '\n', 'utf8');
      console.log(`build layout saved: ${appId} revision ${next.layout.revision}`);
      sendJson(res, 200, { ok: true, layout: next.layout });
    })
    .catch((err) => {
      const status = err.statusCode || 500;
      sendJson(res, status, { ok: false, error: String(err.message || err) });
    });
}

function handleSaveFactoringLayout(req, res) {
  let body = '';
  let tooBig = false;
  req.on('data', (chunk) => {
    body += chunk;
    if (body.length > MAX_LAYOUT_BODY) {
      tooBig = true;
      req.destroy();
    }
  });
  req.on('end', () => {
    if (tooBig) {
      res.writeHead(413, jsonCorsHeaders());
      res.end('{"ok":false,"error":"too large"}');
      return;
    }
    let parsed;
    try {
      parsed = JSON.parse(body || '{}');
    } catch {
      res.writeHead(400, jsonCorsHeaders());
      res.end('{"ok":false,"error":"bad json"}');
      return;
    }
    if (!parsed || typeof parsed.updatedAt !== 'string' || !parsed.layout) {
      res.writeHead(400, jsonCorsHeaders());
      res.end('{"ok":false,"error":"need updatedAt and layout"}');
      return;
    }
    try {
      fs.mkdirSync(path.dirname(FACTORING_LAYOUT_FILE), { recursive: true });
      fs.writeFileSync(
        FACTORING_LAYOUT_FILE,
        JSON.stringify(parsed, null, 2) + '\n',
        'utf8',
      );
      console.log('factoring guided layout synced (Move box)');
      res.writeHead(200, jsonCorsHeaders());
      res.end(JSON.stringify({ ok: true }));
    } catch (err) {
      res.writeHead(500, jsonCorsHeaders());
      res.end(JSON.stringify({ ok: false, error: String(err.message || err) }));
    }
  });
}

const server = http.createServer((req, res) => {
  let rel = decodeURIComponent((req.url || '/').split('?')[0]);

  const buildAppId = resolveBuildLayoutAppId(rel);
  if (buildAppId) {
    if (req.method === 'OPTIONS') {
      res.writeHead(204, jsonCorsHeaders());
      res.end();
      return;
    }
    if (req.method !== 'GET' && req.method !== 'POST') {
      sendJson(res, 405, { ok: false, error: 'GET or POST only' });
      return;
    }
    handleBuildLayout(req, res, buildAppId);
    return;
  }

  if (rel === FACTORING_LAYOUT_JOURNAL_SAVE_PATH) {
    if (req.method === 'OPTIONS') {
      res.writeHead(204, jsonCorsHeaders());
      res.end();
      return;
    }
    if (req.method !== 'POST') {
      res.writeHead(405, jsonCorsHeaders());
      res.end('{"ok":false,"error":"POST only"}');
      return;
    }
    handleSaveFactoringLayoutJournal(req, res);
    return;
  }

  if (rel === FACTORING_LAYOUT_SAVE_PATH) {
    if (req.method === 'OPTIONS') {
      res.writeHead(204, jsonCorsHeaders());
      res.end();
      return;
    }
    if (req.method !== 'POST') {
      res.writeHead(405, jsonCorsHeaders());
      res.end('{"ok":false,"error":"POST only"}');
      return;
    }
    handleSaveFactoringLayout(req, res);
    return;
  }

  if (rel === REGISTRY_SAVE_PATH) {
    if (req.method !== 'POST') {
      res.writeHead(405, { 'Content-Type': 'application/json' });
      res.end('{"ok":false,"error":"POST only"}');
      return;
    }
    handleSavePullRegistry(req, res);
    return;
  }

  if (rel.startsWith(COMMENTS_PREFIX)) {
    if (req.method !== 'POST') {
      res.writeHead(405, { 'Content-Type': 'application/json' });
      res.end('{"ok":false,"error":"POST only"}');
      return;
    }
    handleSaveComments(req, res, rel.slice(COMMENTS_PREFIX.length - 1));
    return;
  }

  if (rel === '/') rel = '/index.html';
  const file = resolveFile(rel);
  if (!file) {
    res.writeHead(404);
    res.end('Not found');
    return;
  }
  const contentType = MIME[path.extname(file).toLowerCase()] || 'application/octet-stream';
  const rangeMatch = /^bytes=(\d*)-(\d*)$/.exec(req.headers.range || '');
  if (rangeMatch) {
    // Video seeking needs HTTP Range; browsers reset currentTime to 0 without it.
    fs.stat(file, (statErr, stat) => {
      if (statErr || !stat.isFile()) {
        res.writeHead(404);
        res.end('Not found');
        return;
      }
      const size = stat.size;
      let start = rangeMatch[1] === '' ? size - Number(rangeMatch[2]) : Number(rangeMatch[1]);
      let end = rangeMatch[1] === '' || rangeMatch[2] === '' ? size - 1 : Number(rangeMatch[2]);
      start = Math.max(0, start);
      end = Math.min(size - 1, end);
      if (Number.isNaN(start) || Number.isNaN(end) || start > end) {
        res.writeHead(416, { 'Content-Range': `bytes */${size}` });
        res.end();
        return;
      }
      res.writeHead(206, {
        'Content-Type': contentType,
        'Accept-Ranges': 'bytes',
        'Content-Range': `bytes ${start}-${end}/${size}`,
        'Content-Length': end - start + 1,
      });
      fs.createReadStream(file, { start, end }).pipe(res);
    });
    return;
  }
  fs.readFile(file, (err, data) => {
    if (err) {
      res.writeHead(404);
      res.end('Not found');
      return;
    }
    res.writeHead(200, { 'Content-Type': contentType, 'Accept-Ranges': 'bytes' });
    res.end(data);
  });
});

server.listen(PORT, '127.0.0.1', () => {
  console.log(`Programs pages: http://127.0.0.1:${PORT}/`);
  console.log(`Session tracking: http://127.0.0.1:${PORT}/session-tracking-log.html`);
  console.log(`Session metrics: http://127.0.0.1:${PORT}/session-metrics-log.html`);
});
