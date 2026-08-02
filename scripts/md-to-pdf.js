#!/usr/bin/env node
/**
 * Render a markdown file to a print-formatted PDF.
 *
 *   node scripts/md-to-pdf.js "agent docs/AGENT_SETUP_FOR_PEER_REVIEW.md"
 *
 * Uses headless Edge (present on every Windows install) so nothing appears on screen.
 * Supports the markdown subset used by docs in this tree: headings, blockquotes, tables,
 * bullet and numbered lists, horizontal rules, bold/italic/code/links.
 */

const fs = require('fs');
const path = require('path');
const os = require('os');
const { execFileSync } = require('child_process');

const EDGE_CANDIDATES = [
  'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe',
  'C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe',
];

function escapeHtml(s) {
  return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

function inline(s) {
  return escapeHtml(s)
    .replace(/`([^`]+)`/g, (_, c) => `<code>${c}</code>`)
    .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
    .replace(/(^|[^*])\*([^*\n]+)\*/g, '$1<em>$2</em>')
    .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2">$1</a>');
}

function isTableRow(line) {
  return /^\s*\|.*\|\s*$/.test(line);
}

function splitRow(line) {
  return line.trim().replace(/^\||\|$/g, '').split('|').map((c) => c.trim());
}

/** Join wrapped continuation lines so a paragraph or list item renders as one block. */
function renderMarkdown(md) {
  const lines = md.split(/\r?\n/);
  const out = [];
  let i = 0;

  const flushParagraph = (buf) => {
    if (buf.length) out.push(`<p>${inline(buf.join(' '))}</p>`);
    return [];
  };

  let para = [];

  while (i < lines.length) {
    const line = lines[i];

    if (!line.trim()) {
      para = flushParagraph(para);
      i += 1;
      continue;
    }

    const heading = line.match(/^(#{1,4})\s+(.*)$/);
    if (heading) {
      para = flushParagraph(para);
      const level = heading[1].length;
      out.push(`<h${level}>${inline(heading[2])}</h${level}>`);
      i += 1;
      continue;
    }

    if (/^---+\s*$/.test(line)) {
      para = flushParagraph(para);
      out.push('<hr />');
      i += 1;
      continue;
    }

    if (line.startsWith('>')) {
      para = flushParagraph(para);
      const buf = [];
      while (i < lines.length && lines[i].startsWith('>')) {
        buf.push(lines[i].replace(/^>\s?/, ''));
        i += 1;
      }
      out.push(`<blockquote>${renderMarkdown(buf.join('\n'))}</blockquote>`);
      continue;
    }

    if (isTableRow(line) && isTableRow(lines[i + 1] || '') && /^[\s|:-]+$/.test(lines[i + 1])) {
      para = flushParagraph(para);
      const head = splitRow(line);
      i += 2;
      const body = [];
      while (i < lines.length && isTableRow(lines[i])) {
        body.push(splitRow(lines[i]));
        i += 1;
      }
      const th = head.map((c) => `<th>${inline(c)}</th>`).join('');
      const rows = body
        .map((r) => `<tr>${r.map((c) => `<td>${inline(c)}</td>`).join('')}</tr>`)
        .join('');
      out.push(`<table><thead><tr>${th}</tr></thead><tbody>${rows}</tbody></table>`);
      continue;
    }

    const bullet = line.match(/^([-*])\s+(.*)$/);
    const numbered = line.match(/^(\d+)\.\s+(.*)$/);
    if (bullet || numbered) {
      para = flushParagraph(para);
      const tag = bullet ? 'ul' : 'ol';
      const items = [];
      while (i < lines.length) {
        const m = lines[i].match(bullet ? /^[-*]\s+(.*)$/ : /^\d+\.\s+(.*)$/);
        if (!m) break;
        const buf = [m[1]];
        i += 1;
        while (i < lines.length && /^\s{2,}\S/.test(lines[i])) {
          buf.push(lines[i].trim());
          i += 1;
        }
        items.push(`<li>${inline(buf.join(' '))}</li>`);
      }
      out.push(`<${tag}>${items.join('')}</${tag}>`);
      continue;
    }

    para.push(line.trim());
    i += 1;
  }

  flushParagraph(para);
  return out.join('\n');
}

const CSS = `
  @page { size: letter; margin: 0.85in 0.9in; }
  body { font-family: "Segoe UI", Calibri, system-ui, sans-serif; font-size: 10.5pt;
         line-height: 1.55; color: #1a1a1a; margin: 0; }
  h1 { font-size: 20pt; line-height: 1.25; margin: 0 0 0.5em; border-bottom: 2px solid #2b2b2b;
       padding-bottom: 0.3em; }
  h2 { font-size: 14pt; margin: 1.6em 0 0.5em; color: #12406b; page-break-after: avoid; }
  h3 { font-size: 11.5pt; margin: 1.3em 0 0.4em; color: #333; page-break-after: avoid; }
  p { margin: 0 0 0.75em; }
  ul, ol { margin: 0 0 0.85em; padding-left: 1.4em; }
  li { margin-bottom: 0.35em; }
  code { font-family: Consolas, "Cascadia Mono", monospace; font-size: 0.88em;
         background: #f1f3f5; padding: 0.1em 0.32em; border-radius: 3px; }
  a { color: #12406b; text-decoration: none; }
  hr { border: 0; border-top: 1px solid #d8dde2; margin: 1.7em 0; }
  blockquote { margin: 0 0 1.2em; padding: 0.7em 1em; background: #f6f8fa;
               border-left: 3px solid #12406b; }
  blockquote p { margin: 0 0 0.5em; }
  blockquote p:last-child { margin-bottom: 0; }
  table { border-collapse: collapse; width: 100%; margin: 0 0 1.1em; font-size: 9.5pt;
          page-break-inside: avoid; }
  th, td { border: 1px solid #ccd3da; padding: 0.42em 0.6em; text-align: left;
           vertical-align: top; }
  th { background: #eef2f6; font-weight: 600; }
  tbody tr:nth-child(even) { background: #fafbfc; }
  strong { font-weight: 600; }
`;

function main() {
  const rel = process.argv[2];
  if (!rel) {
    console.error('Usage: node scripts/md-to-pdf.js <path-to-markdown>');
    process.exit(1);
  }

  const src = path.resolve(rel);
  const md = fs.readFileSync(src, 'utf8');
  const title = path.basename(src, '.md');
  const html = `<!doctype html><html><head><meta charset="utf-8">
<title>${escapeHtml(title)}</title><style>${CSS}</style></head>
<body>${renderMarkdown(md)}</body></html>`;

  const tmpHtml = path.join(os.tmpdir(), `${title}-${Date.now()}.html`);
  fs.writeFileSync(tmpHtml, html, 'utf8');

  const edge = EDGE_CANDIDATES.find((p) => fs.existsSync(p));
  if (!edge) {
    console.error('Microsoft Edge not found; cannot render PDF.');
    process.exit(1);
  }

  const outPdf = path.join(path.dirname(src), `${title}.pdf`);
  execFileSync(edge, [
    '--headless',
    '--disable-gpu',
    '--no-pdf-header-footer',
    `--print-to-pdf=${outPdf}`,
    `file:///${tmpHtml.replace(/\\/g, '/')}`,
  ], { stdio: 'ignore' });

  fs.unlinkSync(tmpHtml);

  if (!fs.existsSync(outPdf)) {
    console.error('Edge ran but produced no PDF.');
    process.exit(1);
  }
  console.log(`${outPdf}  (${(fs.statSync(outPdf).size / 1024).toFixed(0)} KB)`);
}

main();
