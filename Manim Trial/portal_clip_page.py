"""A review page for one portrait portal clip, with the portal player's controls.

Same behavior as the student portal's Auto/Slow player (useVideoExamplePlayer.ts), driven by
the clip's `*_steps.json` (one time per caption, the last is the final hold):
    Auto   plays on its own; Back / Next jump one caption step and keep playing.
    Slow   no autoplay between steps; Next plays to the next step and stops; Back seeks to the
           previous step and stops; Next while playing skips ahead to the following step.
    Pause / Play, Restart. Switching Auto/Slow never restarts the clip.
The video is sized to the window height so the whole player fits one screen.
Used by build_page.py for the slugs in PORTRAIT.
"""

import base64
import json
import pathlib

STYLE = (
    'body{margin:0;background:#101c30;color:#f2f5fa;font:18px Segoe UI,sans-serif;text-align:center}'
    'main{max-width:900px;margin:0 auto;padding:6px}h1{font-size:20px;margin:6px 0}'
    'video{width:auto;max-width:100%;height:calc(100vh - 235px);border-radius:12px;'
    'background:#fff;cursor:pointer}'
    '.row{display:flex;justify-content:center;gap:10px;margin:8px 0}'
    'button{font:inherit;flex:0 1 190px;min-height:50px;border:0;border-radius:10px;'
    'background:#ffc66d;color:#101c30;cursor:pointer}'
    'button.mode{background:#3a4a66;color:#f2f5fa}button.mode.on{background:#86c8ff;color:#101c30}'
    'a{color:#86c8ff}'
)

SCRIPT = r'''
const S = STEPS, v = document.getElementById("movie"), END = S[S.length - 1];
let mode = "auto", goal = END;
const $ = id => document.getElementById(id);
const nextHold = t => S.find(s => s > t + 0.1) ?? END;
const setGoal = () => { goal = nextHold(v.currentTime); };
function show() {
  $("auto").classList.toggle("on", mode === "auto");
  $("slow").classList.toggle("on", mode === "slow");
  $("pause").textContent = v.paused ? "Play" : "Pause";
}
function go(t, play) {
  v.currentTime = Math.max(0, t); setGoal();
  if (play) v.play(); else v.pause();
}
function toggle() {
  if (!v.paused) { v.pause(); return; }
  if (v.currentTime >= END - 0.1) v.currentTime = 0;
  setGoal(); v.play();
}
function next() {
  const t = v.currentTime;
  if (mode === "slow" && v.paused) { if (t >= END - 0.1) return; setGoal(); v.play(); return; }
  if (t >= END - 0.1) return;
  go(mode === "slow" ? goal + 0.05 : nextHold(t), true);
  if (mode === "slow") setGoal();
}
function back() {
  const t = v.currentTime, done = S.filter(s => s <= t + 0.1);
  let i = done.length - 1;
  if (i >= 0 && Math.abs(done[i] - t) <= 0.12) i -= 1;
  go(i >= 0 ? S[i] : 0, mode === "auto");
}
$("auto").onclick = () => { mode = "auto"; setGoal(); show(); };
$("slow").onclick = () => { mode = "slow"; setGoal(); show(); };
$("restart").onclick = () => go(0, mode === "auto");
$("pause").onclick = toggle; $("next").onclick = next; $("back").onclick = back;
v.onclick = toggle;
document.onkeydown = e => { if (e.code === "Space") { e.preventDefault(); toggle(); } };
["play", "pause", "seeked"].forEach(n => v.addEventListener(n, show));
(function tick() {
  if (!v.paused && (v.currentTime >= END - 0.02 || (mode === "slow" && v.currentTime >= goal - 0.02))) {
    const stop = v.currentTime >= END - 0.02 ? END : goal;
    v.pause(); v.currentTime = stop;
  }
  requestAnimationFrame(tick);
})();
setGoal(); show();
v.play().catch(show);
'''


def build_clip_page(out, heading, tab, video, steps_file):
    steps = json.loads(pathlib.Path(steps_file).read_text(encoding='utf-8'))
    data = base64.b64encode(pathlib.Path(video).read_bytes()).decode('ascii')
    html = (
        '<!doctype html><html lang="en"><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        f'<title>{tab}</title><style>{STYLE}</style><main><h1>{heading}</h1>'
        '<video id="movie" playsinline muted preload="auto">'
        f'<source src="data:video/mp4;base64,{data}" type="video/mp4"></video>'
        '<div class="row"><button class="mode on" id="auto">Auto</button>'
        '<button class="mode" id="slow">Slow</button><button id="restart">Restart</button></div>'
        '<div class="row"><button id="pause">Pause</button><button id="back">Back</button>'
        '<button id="next">Next</button></div>'
        '<a href="/pages.html">&larr; All pages</a></main>'
        f'<script>const STEPS={json.dumps(steps)};{SCRIPT}</script></html>'
    )
    pathlib.Path(out).write_text(html, encoding='utf-8')
    return f'{pathlib.Path(out).stat().st_size:,} bytes'
