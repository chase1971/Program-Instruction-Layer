/**
 * Serve Programs/docs/ on a fixed localhost port so chat http:// links open in a browser.
 * Usage: node scripts/serve-programs-docs.js
 * Then open: http://127.0.0.1:8765/context-engineering-infographic.html
 */
'use strict';

const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = 8765;
const DOCS = path.join(__dirname, '..', 'docs');

const MIME = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.png': 'image/png',
  '.svg': 'image/svg+xml',
};

const server = http.createServer((req, res) => {
  let rel = decodeURIComponent((req.url || '/').split('?')[0]);
  if (rel === '/') rel = '/context-engineering-infographic.html';
  const file = path.normalize(path.join(DOCS, rel.replace(/^\//, '')));
  if (!file.startsWith(DOCS)) {
    res.writeHead(403);
    res.end('Forbidden');
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
  console.log(`Programs docs: http://127.0.0.1:${PORT}/context-engineering-infographic.html`);
});
