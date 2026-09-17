/**
 * Serve Programs/docs/, agent docs/, and School documents on a fixed localhost port
 * so chat http:// links open in a browser.
 * Usage: node scripts/serve-programs-docs.js
 * Then open: http://127.0.0.1:8765/context-engineering-infographic.html
 *
 * Also accepts ONE kind of write: POST /__comments/<page path> saves reader comments
 * to <page>.comments.json beside the page, so a page can collect Chase's notes and an
 * agent can read them straight off disk. Nothing else is writable. Detail:
 * agent docs/rules/html-delivery.md § Reader comments.
 */
'use strict';

const http = require('http');
const fs = require('fs');
const path = require('path');

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
const MAX_COMMENT_BODY = 512 * 1024;

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

const server = http.createServer((req, res) => {
  let rel = decodeURIComponent((req.url || '/').split('?')[0]);

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
  fs.readFile(file, (err, data) => {
    if (err) {
      res.writeHead(404);
      res.end('Not found');
      return;
    }
    res.writeHead(200, { 'Content-Type': MIME[path.extname(file).toLowerCase()] || 'application/octet-stream' });
    res.end(data);
  });
});

server.listen(PORT, '127.0.0.1', () => {
  console.log(`Programs pages: http://127.0.0.1:${PORT}/`);
  console.log(`Session tracking: http://127.0.0.1:${PORT}/session-tracking-log.html`);
  console.log(`Session metrics: http://127.0.0.1:${PORT}/session-metrics-log.html`);
});
