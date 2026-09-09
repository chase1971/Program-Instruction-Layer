/**
 * FILE: scripts/doc-index-html.js
 * PURPOSE: Render the front-door index page for build-doc-index.js.
 *
 * Dwell-friendly by construction: every target is at least 48px, the pin button
 * is always visible (no hover-only affordances), and the whole card is the link.
 * Pins and open/closed section state live in localStorage, so they survive a
 * rebuild of this file.
 */
'use strict';

const esc = (s) => String(s == null ? '' : s)
  .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

function cardHtml(page, accent) {
  const desc = page.desc || page.title;
  return `<div class="row" data-href="${esc(page.href)}">
    <a class="card ${esc(accent || '')}" href="${esc(page.href)}">
      <div class="t">${esc(page.title)}</div>
      <div class="d">${esc(desc)}</div>
      <div class="m">${esc(page.href)}${page.mtime ? ` · ${esc(page.mtime)}` : ''}</div>
    </a>
    <button class="pin" type="button" data-href="${esc(page.href)}"
      aria-label="Pin ${esc(page.title)} to the top" title="Pin to top">
      <span class="star">☆</span>
    </button>
  </div>`;
}

function groupHtml(g) {
  const count = g.items.length + g.collapsed.length;
  const collapsedBlock = g.collapsed.length
    ? `<details class="subgroup">
        <summary><span class="sumtitle">Generated run archive</span>
          <span class="count">${g.collapsed.length}</span></summary>
        <div class="sublist">${g.collapsed
    .slice()
    .sort((a, b) => b.href.localeCompare(a.href))
    .map((p) => `<a class="mini" href="${esc(p.href)}">${esc(p.title)}</a>`).join('')}</div>
      </details>`
    : '';

  return `<details class="group" data-group="${esc(g.id)}"${g.open ? ' open' : ''}>
    <summary>
      <span class="sumtitle">${esc(g.title)}</span>
      <span class="count">${count}</span>
    </summary>
    <div class="groupbody">
      ${g.blurb ? `<p class="blurb">${esc(g.blurb)}</p>` : ''}
      ${g.items.map((p) => cardHtml(p, g.accent)).join('')}
      ${collapsedBlock}
    </div>
  </details>`;
}

function renderIndexHtml(groups, totalPages) {
  return `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Programs — pages</title>
<style>
  :root{--bg:#0f1419;--panel:#1a2332;--panel-alt:#243044;--text:#e8edf4;--muted:#94a3b8;
        --accent:#38bdf8;--green:#34d399;--amber:#fbbf24;--purple:#a78bfa;--red:#f87171;
        --border:#334155;--radius:14px;--font:"Segoe UI",system-ui,sans-serif}
  *{box-sizing:border-box;margin:0;padding:0}
  body{font-family:var(--font);background:var(--bg);color:var(--text);line-height:1.5;font-size:18px}
  .page{max-width:960px;margin:0 auto;padding:2.2rem 1.25rem 4rem}

  header{margin-bottom:1.4rem;padding-bottom:1.2rem;border-bottom:2px solid var(--border)}
  header h1{font-size:clamp(1.7rem,5vw,2.3rem);font-weight:700;letter-spacing:-.02em}
  header p{color:var(--muted);margin-top:.55rem;font-size:1rem}

  /* ---- pinned ---- */
  #pinned-section{margin-bottom:1.6rem}
  #pinned-section h2{color:var(--amber)}
  .pinned-empty{background:var(--panel);border:1px dashed var(--border);border-radius:var(--radius);
    padding:1rem 1.15rem;color:var(--muted);font-size:.92rem}
  .pinned-empty b{color:var(--text)}

  h2{font-size:.85rem;letter-spacing:.15em;text-transform:uppercase;font-weight:700;
     margin:0 0 .6rem;color:var(--accent)}

  /* ---- groups ---- */
  details.group{background:var(--panel);border:1px solid var(--border);border-radius:var(--radius);
    margin-bottom:.7rem;overflow:hidden}
  details.group>summary{cursor:pointer;list-style:none;min-height:60px;padding:1rem 1.15rem;
    display:flex;align-items:center;gap:.7rem;background:var(--panel-alt);font-weight:700;font-size:1.05rem}
  details.group>summary::-webkit-details-marker{display:none}
  details.group>summary::before{content:"▸";color:var(--accent);font-size:1.1rem;flex:0 0 auto;
    transition:transform .12s}
  details.group[open]>summary::before{transform:rotate(90deg)}
  details.group>summary:hover,details.group>summary:focus{background:#2b3a52;outline:none}
  .sumtitle{flex:1 1 auto}
  .count{flex:0 0 auto;background:var(--bg);color:var(--muted);border-radius:999px;
    padding:.15rem .6rem;font-size:.8rem;font-weight:700;font-family:Consolas,monospace}
  .groupbody{padding:.9rem 1.15rem 1.1rem}
  .blurb{color:var(--muted);font-size:.9rem;margin-bottom:.9rem}

  /* ---- cards ---- */
  .row{display:flex;gap:.55rem;align-items:stretch;margin-bottom:.7rem}
  a.card{flex:1 1 auto;display:block;text-decoration:none;background:var(--bg);
    border:1px solid var(--border);border-left:5px solid var(--accent);
    border-radius:var(--radius);padding:.95rem 1.1rem;min-height:76px;color:inherit}
  a.card:hover,a.card:focus{background:var(--panel-alt);border-color:var(--accent);outline:none}
  a.card.green{border-left-color:var(--green)}
  a.card.amber{border-left-color:var(--amber)}
  a.card.grey{border-left-color:var(--border)}
  a.card.purple{border-left-color:var(--purple)}
  a.card .t{font-size:1.06rem;font-weight:700;color:var(--text);line-height:1.35}
  a.card .d{font-size:.9rem;color:var(--muted);margin-top:.28rem}
  a.card .m{font-size:.74rem;color:#64748b;margin-top:.4rem;font-family:Consolas,monospace;
    word-break:break-all}

  /* pin button — always visible, dwell-sized */
  button.pin{flex:0 0 auto;width:60px;min-height:76px;background:var(--bg);
    border:1px solid var(--border);border-radius:var(--radius);color:var(--muted);
    font-size:1.6rem;cursor:pointer;display:grid;place-items:center;padding:0;font-family:inherit}
  button.pin:hover,button.pin:focus{background:var(--panel-alt);border-color:var(--amber);
    color:var(--amber);outline:none}
  button.pin[data-pinned="1"]{color:var(--amber);border-color:var(--amber);background:#2a2313}

  /* ---- collapsed sub-list ---- */
  details.subgroup{background:var(--bg);border:1px solid var(--border);border-radius:var(--radius);
    margin-top:.4rem;overflow:hidden}
  details.subgroup>summary{cursor:pointer;list-style:none;min-height:52px;padding:.85rem 1rem;
    display:flex;align-items:center;gap:.6rem;font-size:.95rem;color:var(--muted)}
  details.subgroup>summary::-webkit-details-marker{display:none}
  details.subgroup>summary::before{content:"▸";color:var(--accent);transition:transform .12s}
  details.subgroup[open]>summary::before{transform:rotate(90deg)}
  .sublist{display:flex;flex-wrap:wrap;gap:.4rem;padding:0 1rem 1rem}
  a.mini{display:block;background:var(--panel-alt);border:1px solid var(--border);
    border-radius:10px;padding:.55rem .8rem;min-height:44px;font-size:.85rem;
    color:var(--accent);text-decoration:none;font-family:Consolas,monospace}
  a.mini:hover,a.mini:focus{background:#2b3a52;outline:none}

  footer{margin-top:2.5rem;padding-top:1.2rem;border-top:1px solid var(--border);
    color:var(--muted);font-size:.85rem;text-align:center}
  code{background:var(--panel-alt);color:var(--accent);padding:.08rem .32rem;border-radius:4px;
    font-size:.85em;font-family:Consolas,monospace}
</style>
</head>
<body>
<div class="page">

<header>
  <h1>Programs — pages</h1>
  <p>${totalPages} pages served on <code>127.0.0.1:8765</code>.
     Tap ☆ on any card to pin it to the top — pins and open sections are remembered on this machine.</p>
</header>

<section id="pinned-section">
  <h2>Pinned</h2>
  <div id="pinned-list"></div>
</section>

<div id="groups">
${groups.map(groupHtml).join('\n')}
</div>

<footer>
  Regenerate with <code>node scripts/build-doc-index.js</code> ·
  grouping lives in <code>agent docs/page-manifest.json</code>
</footer>

</div>
<script>
(function(){
  var PIN_KEY = 'programs-index-pins';
  var OPEN_KEY = 'programs-index-open';

  function load(key, fallback){
    try { var v = JSON.parse(localStorage.getItem(key)); return v || fallback; }
    catch(e){ return fallback; }
  }
  function save(key, val){
    try { localStorage.setItem(key, JSON.stringify(val)); } catch(e){}
  }

  var pins = load(PIN_KEY, []);
  var pinnedList = document.getElementById('pinned-list');

  function cardFor(href){
    var row = document.querySelector('#groups .row[data-href="' + CSS.escape(href) + '"]');
    return row ? row : null;
  }

  function renderPinned(){
    pinnedList.innerHTML = '';
    var live = pins.filter(function(h){ return cardFor(h); });
    if (live.length !== pins.length){ pins = live; save(PIN_KEY, pins); }

    if (!pins.length){
      pinnedList.innerHTML = '<div class="pinned-empty">Nothing pinned yet. '
        + 'Tap <b>☆</b> on any card to keep it up here.</div>';
      return;
    }
    pins.forEach(function(href){
      var clone = cardFor(href).cloneNode(true);
      clone.setAttribute('data-pinned-clone','1');
      pinnedList.appendChild(clone);
    });
    syncStars();
  }

  function syncStars(){
    document.querySelectorAll('button.pin').forEach(function(btn){
      var on = pins.indexOf(btn.getAttribute('data-href')) !== -1;
      btn.setAttribute('data-pinned', on ? '1' : '0');
      btn.querySelector('.star').textContent = on ? '★' : '☆';
      btn.setAttribute('title', on ? 'Unpin' : 'Pin to top');
    });
  }

  document.addEventListener('click', function(ev){
    var btn = ev.target.closest ? ev.target.closest('button.pin') : null;
    if (!btn) return;
    ev.preventDefault();
    var href = btn.getAttribute('data-href');
    var i = pins.indexOf(href);
    if (i === -1) pins.push(href); else pins.splice(i, 1);
    save(PIN_KEY, pins);
    renderPinned();
  });

  // Remember which sections are open.
  var openState = load(OPEN_KEY, null);
  document.querySelectorAll('details.group').forEach(function(d){
    var id = d.getAttribute('data-group');
    if (openState && Object.prototype.hasOwnProperty.call(openState, id)) d.open = !!openState[id];
    d.addEventListener('toggle', function(){
      var st = load(OPEN_KEY, {});
      st[id] = d.open;
      save(OPEN_KEY, st);
    });
  });

  renderPinned();
})();
</script>
</body>
</html>`;
}

module.exports = { renderIndexHtml };
