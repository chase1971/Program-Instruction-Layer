const fs = require('fs');
const path = require('path');

const dir = __dirname;
const order = [
  { key: 'square', label: 'Square' },
  { key: 'drain', label: 'Draining tank' },
  { key: 'ladder', label: 'Ladder' },
  { key: 'cone', label: 'Cone' },
  { key: 'rocket', label: 'Rocket' },
  { key: 'lighthouse', label: 'Lighthouse' },
];

const slides = order.map(({ key, label }) => {
  const html = fs.readFileSync(path.join(dir, `related-rates-${key}.html`), 'utf8');
  const title = (html.match(/<title>([^<]+)<\/title>/) || [])[1] || label;
  const heading = (html.match(/<h1>([^<]+)<\/h1>/) || [])[1] || title;
  const src = (html.match(/src="(data:video[^"]+)"/) || [])[1];
  const desc = (html.match(/<\/div><p>([\s\S]*?)<\/p><p><small>/) || [])[1] || '';
  const source = (html.match(/<small>([\s\S]*?)<\/small>/) || [])[1] || '';
  if (!src) throw new Error(`Missing video in related-rates-${key}.html`);
  return { key, label, title, heading, src, desc, source };
});

const slideJson = JSON.stringify(slides);

const viewer = `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Related rates animations — all six</title>
<style>
  body { margin: 0; background: #101c30; color: #f2f5fa; font: 20px Segoe UI, sans-serif; text-align: center; }
  main { max-width: 1150px; margin: 20px auto; padding: 16px; }
  h1 { margin: 0 0 8px; font-size: 1.35rem; }
  .counter { color: #b2c0d4; margin-bottom: 16px; font-size: 1.05rem; }
  video { width: 100%; border-radius: 12px; display: block; }
  .controls { display: flex; flex-wrap: wrap; justify-content: center; gap: 12px; margin: 18px 0; }
  button {
    font: inherit; padding: 18px 30px; border: 0; border-radius: 10px;
    background: #ffc66d; color: #101c30; cursor: pointer; min-width: 145px;
  }
  button.secondary { background: #86c8ff; }
  button:disabled { opacity: 0.45; cursor: default; }
  p { line-height: 1.6; max-width: 900px; margin: 0 auto 12px; }
  small { color: #b2c0d4; display: block; margin-top: 8px; }
  a { color: #86c8ff; display: inline-block; margin-top: 20px; }
  .jump-row { display: flex; flex-wrap: wrap; justify-content: center; gap: 8px; margin: 12px 0 4px; }
  .jump-row button { min-width: 110px; padding: 14px 18px; font-size: 0.95rem; }
  .jump-row button.active { outline: 3px solid #f2f5fa; }
</style>
</head>
<body>
<main>
  <h1 id="heading"></h1>
  <div class="counter" id="counter"></div>
  <video id="movie" playsinline preload="metadata" controls></video>
  <div class="controls">
    <button type="button" id="prev" class="secondary">Previous</button>
    <button type="button" id="play">Play / Pause</button>
    <button type="button" id="replay">Replay</button>
    <button type="button" id="next">Next</button>
  </div>
  <div class="jump-row" id="jump-row"></div>
  <p id="desc"></p>
  <small id="source"></small>
  <a href="/pages.html">&larr; All pages</a>
</main>
<script>
const slides = ${slideJson};
let index = 0;
const movie = document.getElementById('movie');
const heading = document.getElementById('heading');
const counter = document.getElementById('counter');
const desc = document.getElementById('desc');
const source = document.getElementById('source');
const prevBtn = document.getElementById('prev');
const nextBtn = document.getElementById('next');
const jumpRow = document.getElementById('jump-row');

slides.forEach((slide, i) => {
  const btn = document.createElement('button');
  btn.type = 'button';
  btn.textContent = slide.label;
  btn.onclick = () => show(i, true);
  btn.dataset.index = String(i);
  jumpRow.appendChild(btn);
});

function show(i, autoplay) {
  index = i;
  const slide = slides[i];
  heading.innerHTML = slide.heading;
  counter.textContent = 'Animation ' + (i + 1) + ' of ' + slides.length;
  movie.src = slide.src;
  desc.innerHTML = slide.desc;
  source.innerHTML = slide.source;
  prevBtn.disabled = i === 0;
  nextBtn.disabled = i === slides.length - 1;
  jumpRow.querySelectorAll('button').forEach((btn, j) => {
    btn.classList.toggle('active', j === i);
  });
  if (autoplay) {
    movie.onloadeddata = () => { movie.play(); movie.onloadeddata = null; };
    movie.load();
  } else {
    movie.load();
  }
}

document.getElementById('play').onclick = () => {
  if (movie.paused) movie.play();
  else movie.pause();
};
document.getElementById('replay').onclick = () => {
  movie.currentTime = 0;
  movie.play();
};
prevBtn.onclick = () => { if (index > 0) show(index - 1, true); };
nextBtn.onclick = () => { if (index < slides.length - 1) show(index + 1, true); };

show(0, false);
</script>
</html>
`;

const outPath = path.join(dir, 'related-rates-viewer.html');
fs.writeFileSync(outPath, viewer);
const mb = (fs.statSync(outPath).size / (1024 * 1024)).toFixed(1);
console.log('Wrote ' + outPath + ' (' + mb + ' MB, ' + slides.length + ' slides)');
