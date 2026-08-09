/**
 * Serve Programs/docs/, agent docs/, and School documents on a fixed localhost port
 * so chat http:// links open in a browser.
 * Usage: node scripts/serve-programs-docs.js
 * Then open: http://127.0.0.1:8765/context-engineering-infographic.html
 */
'use strict';

const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = 8765;
const DOCS = path.join(__dirname, '..', 'docs');
const AGENT_DOCS = path.join(__dirname, '..', 'agent docs');
const SCHOOL_DOCS = path.join(__dirname, '..', 'School Scrips', 'School documents');
// School documents first so teaching HTML (exam maps) wins over agent-docs stubs
const SERVE_ROOTS = [SCHOOL_DOCS, DOCS, AGENT_DOCS];

const MIME = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.png': 'image/png',
  '.svg': 'image/svg+xml',
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

const server = http.createServer((req, res) => {
  let rel = decodeURIComponent((req.url || '/').split('?')[0]);
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
