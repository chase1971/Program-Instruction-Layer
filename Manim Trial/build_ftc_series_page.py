"""Build the self-contained served HTML player for the four FTC portal clips."""

import base64
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
PORTAL_ASSETS = ROOT.parent / 'School Scrips' / 'student-portal' / 'src' / 'assets' / 'video-examples' / 'fundamental-theorem-calculus'
OUTPUT = ROOT.parent / 'agent docs' / 'scratch' / 'fundamental-theorem-calculus.html'

CLIPS = [
    ('1 · Area and position agree', 'triangle-square.mp4', 'triangle-square-steps.json', 26.25),
    ('2 · Riemann sums to integral', 'added-area.mp4', 'added-area-steps.json', 40.71),
    ('3 · The theorem', 'theorem-statement.mp4', 'theorem-statement-steps.json', 152.39),
    ('4 · The squeeze proof', 'squeeze-proof.mp4', 'squeeze-proof-steps.json', 44.24),
]


def video_data(path: Path) -> str:
    encoded = base64.b64encode(path.read_bytes()).decode('ascii')
    return f'data:video/mp4;base64,{encoded}'


def clip_data():
    return [
        {
            'label': label,
            'src': video_data(PORTAL_ASSETS / video_name),
            'steps': json.loads((PORTAL_ASSETS / steps_name).read_text(encoding='utf-8')),
            'end': end,
        }
        for label, video_name, steps_name, end in CLIPS
    ]


def build() -> Path:
    clips_json = json.dumps(clip_data(), separators=(',', ':'))
    html = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Fundamental Theorem of Calculus — Step-by-step animations</title>
<style>
  :root {{ color-scheme: dark; font-family: "Segoe UI", system-ui, sans-serif; background:#07152b; color:#fff; }}
  * {{ box-sizing:border-box; }}
  body {{ margin:0; min-height:100vh; background:radial-gradient(circle at top,#183861 0,#0b2140 42%,#07152b 100%); }}
  main {{ width:min(100%,960px); margin:0 auto; padding:18px 16px 30px; }}
  .top {{ display:flex; justify-content:space-between; align-items:center; gap:16px; margin-bottom:12px; }}
  .back {{ color:#dbeafe; font-weight:700; text-decoration:none; min-height:44px; display:inline-flex; align-items:center; }}
  .stamp {{ color:#a8c5ea; font-size:.82rem; text-align:right; }}
  h1 {{ font-size:clamp(1.25rem,4vw,2rem); text-align:center; margin:4px 0 14px; }}
  .card {{ background:#102b50; border:1px solid rgba(255,255,255,.2); border-radius:18px; padding:12px; box-shadow:0 18px 50px rgba(0,0,0,.3); }}
  .parts,.modes,.steps {{ display:flex; flex-wrap:wrap; justify-content:center; gap:8px; }}
  button {{ min-height:48px; padding:10px 16px; border-radius:12px; border:2px solid rgba(255,255,255,.42); background:#193b68; color:#fff; font:700 1rem/1.15 "Segoe UI",sans-serif; cursor:pointer; touch-action:manipulation; }}
  button.active {{ background:#fff; color:#102b50; border-color:#fff; }}
  button:disabled {{ opacity:.42; cursor:default; }}
  .parts button {{ flex:1 1 200px; }}
  .clip-title {{ text-align:center; font-size:1.08rem; font-weight:750; margin:12px 0 8px; min-height:1.4em; }}
  .video-wrap {{ width:min(100%,540px); margin:0 auto; background:#fff; border-radius:14px; overflow:hidden; border:2px solid rgba(255,255,255,.5); }}
  video {{ display:block; width:100%; aspect-ratio:1080/1350; object-fit:contain; background:#fff; }}
  .controls {{ display:grid; gap:10px; margin-top:12px; }}
  .modes button {{ min-width:120px; }}
  .steps button {{ min-width:130px; }}
  @keyframes next-pulse {{ 0%,100% {{ box-shadow:0 0 0 2px rgba(250,204,21,.5); }} 50% {{ box-shadow:0 0 0 7px rgba(250,204,21,.98); }} }}
  @keyframes watch-pulse {{ 0%,100% {{ transform:scale(.82); opacity:.65; }} 50% {{ transform:scale(1.18); opacity:1; }} }}
  button.pulse {{ animation:next-pulse 1s ease-in-out infinite; border-color:#facc15; }}
  .motion {{ width:min(100%,540px); margin:10px auto 0; min-height:50px; display:flex; align-items:center; justify-content:center; gap:10px; border-radius:12px; background:rgba(255,255,255,.1); color:#dbeafe; font-weight:750; text-align:center; padding:9px 14px; }}
  .motion-dot {{ width:14px; height:14px; border-radius:50%; background:#93c5fd; box-shadow:0 0 0 4px rgba(147,197,253,.18); flex:0 0 auto; }}
  .motion.playing {{ background:rgba(250,204,21,.13); color:#fff4b5; }}
  .motion.playing .motion-dot {{ background:#facc15; box-shadow:0 0 0 5px rgba(250,204,21,.2); animation:watch-pulse .8s ease-in-out infinite; }}
  .motion.complete .motion-dot {{ background:#86efac; box-shadow:0 0 0 4px rgba(134,239,172,.18); }}
  .hint {{ text-align:center; color:#bfd4ef; margin:9px 0 0; font-size:.9rem; }}
  @media (prefers-reduced-motion:reduce) {{ button.pulse {{ animation:none; box-shadow:0 0 0 5px rgba(250,204,21,.95); }} .motion.playing .motion-dot {{ animation:none; }} }}
  @media (max-width:560px) {{ main {{ padding:10px 8px 20px; }} .card {{ padding:8px; border-radius:12px; }} button {{ min-height:50px; }} .parts button {{ flex-basis:46%; font-size:.88rem; padding:8px; }} }}
</style>
</head>
<body>
<main>
  <div class="top"><a class="back" href="/pages.html">← All pages</a><span class="stamp">Prepared October 13, 2026 · one-off lesson page</span></div>
  <h1>Fundamental Theorem of Calculus</h1>
  <section class="card" aria-label="Animation player">
    <div class="parts" id="parts" role="tablist" aria-label="Lesson parts"></div>
    <div class="clip-title" id="title"></div>
    <div class="video-wrap"><video id="video" playsinline preload="auto" aria-label="Fundamental Theorem animation"></video></div>
    <div class="motion" id="motion" role="status" aria-live="polite"><span class="motion-dot"></span><span id="motionText"></span></div>
    <div class="controls">
      <div class="modes" aria-label="Playback mode">
        <button id="auto" type="button">Auto</button>
        <button id="slow" class="active" type="button">Slow</button>
        <button id="restart" type="button">Restart</button>
      </div>
      <div class="steps" aria-label="Step navigation">
        <button id="back" type="button">Back</button>
        <button id="next" type="button">Next</button>
      </div>
    </div>
    <p class="hint">Slow mode: each press of Next plays one explanation step. Tap the animation to pause or continue.</p>
  </section>
</main>
<script>
const clips={clips_json};
const video=document.getElementById('video');
const parts=document.getElementById('parts');
const title=document.getElementById('title');
const motion=document.getElementById('motion');
const motionText=document.getElementById('motionText');
const autoButton=document.getElementById('auto');
const slowButton=document.getElementById('slow');
const restartButton=document.getElementById('restart');
const backButton=document.getElementById('back');
const nextButton=document.getElementById('next');
let clipIndex=0;
let mode='slow';
let target=null;
let targetIndex=null;
let stepIndex=0;
let frameWatch=0;

clips.forEach((clip,index)=>{{
  const button=document.createElement('button');
  button.type='button';
  button.role='tab';
  button.textContent=clip.label;
  button.addEventListener('click',()=>selectClip(index));
  parts.appendChild(button);
}});

function currentClip(){{ return clips[clipIndex]; }}
function stepTimes(){{ return [0,...currentClip().steps]; }}
function setActiveButtons(){{
  [...parts.children].forEach((button,index)=>{{
    button.classList.toggle('active',index===clipIndex);
    button.setAttribute('aria-selected',String(index===clipIndex));
  }});
  autoButton.classList.toggle('active',mode==='auto');
  slowButton.classList.toggle('active',mode==='slow');
}}
function selectClip(index){{
  clipIndex=index;
  target=null;
  targetIndex=null;
  stepIndex=0;
  const clip=currentClip();
  title.textContent=clip.label;
  video.src=clip.src;
  video.load();
  setActiveButtons();
  video.addEventListener('loadedmetadata',()=>{{
    video.currentTime=0;
    if(mode==='auto') video.play().catch(()=>{{}});
    updateButtons();
  }},{{once:true}});
}}
function nextStep(){{
  const times=stepTimes();
  const last=times.length-1;
  if(mode==='auto'){{
    const atIndex=times.reduce((found,time,index)=>video.currentTime>=time-.12?index:found,0);
    if(atIndex>=last) return;
    const nextIndex=atIndex+1;
    video.currentTime=times[nextIndex];
    stepIndex=nextIndex;
    target=null; targetIndex=null;
    if(nextIndex>=last) video.pause(); else video.play().catch(()=>{{}});
    updateButtons();
    return;
  }}
  if(targetIndex!==null){{
    const completedTarget=targetIndex;
    video.currentTime=times[completedTarget];
    stepIndex=completedTarget;
    if(completedTarget>=last){{ video.pause(); target=null; targetIndex=null; updateButtons(); return; }}
    targetIndex=completedTarget+1;
    target=times[targetIndex];
    video.play().catch(()=>{{}});
    updateButtons();
    return;
  }}
  if(stepIndex>=last) return;
  targetIndex=stepIndex+1;
  target=times[targetIndex];
  video.play().catch(()=>{{}});
  updateButtons();
}}
function backStep(){{
  const times=stepTimes();
  const destination=targetIndex!==null?Math.max(0,targetIndex-1):Math.max(0,stepIndex-1);
  video.pause(); target=null; targetIndex=null; stepIndex=destination;
  video.currentTime=times[destination];
  updateButtons();
}}
function updateButtons(){{
  const last=stepTimes().length-1;
  const playing=!video.paused;
  const finished=stepIndex>=last&&targetIndex===null;
  backButton.disabled=stepIndex===0&&targetIndex===null;
  nextButton.disabled=finished;
  nextButton.textContent='Next';
  nextButton.classList.toggle('pulse',mode==='slow'&&!playing&&!finished);
  motion.classList.toggle('playing',playing);
  motion.classList.toggle('complete',!playing);
  if(playing) motionText.textContent=`Animation playing — watch the board · step ${{Math.min(targetIndex??(stepIndex+1),last)}} of ${{last}}`;
  else if(finished) motionText.textContent='Part complete — choose another part or press Restart.';
  else if(stepIndex===0) motionText.textContent='Ready — press Next to play the first animation.';
  else motionText.textContent=`Step ${{stepIndex}} of ${{last}} complete — Next is ready.`;
}}
function setMode(nextMode){{
  mode=nextMode; target=null; targetIndex=null; setActiveButtons();
  if(mode==='slow') video.pause(); else video.play().catch(()=>{{}});
  updateButtons();
}}
function watchTarget(){{
  const clip=currentClip();
  if(mode==='slow'&&target!==null&&video.currentTime>=target-.035){{
    const reached=targetIndex??stepIndex+1;
    video.pause(); video.currentTime=target; stepIndex=reached; target=null; targetIndex=null;
  }}
  if(video.currentTime>=clip.end-.035){{
    video.pause(); video.currentTime=clip.end; stepIndex=stepTimes().length-1; target=null; targetIndex=null;
  }}
  updateButtons();
  frameWatch=requestAnimationFrame(watchTarget);
}}
video.addEventListener('timeupdate',updateButtons);
video.addEventListener('click',()=>{{
  if(!video.paused){{ video.pause(); target=null; targetIndex=null; }}
  else if(mode==='slow') nextStep();
  else video.play().catch(()=>{{}});
  updateButtons();
}});
autoButton.addEventListener('click',()=>setMode('auto'));
slowButton.addEventListener('click',()=>setMode('slow'));
restartButton.addEventListener('click',()=>{{ video.currentTime=0; stepIndex=0; target=null; targetIndex=null; if(mode==='auto') video.play().catch(()=>{{}}); else video.pause(); updateButtons(); }});
backButton.addEventListener('click',backStep);
nextButton.addEventListener('click',nextStep);
selectClip(0);
cancelAnimationFrame(frameWatch);
frameWatch=requestAnimationFrame(watchTarget);
</script>
</body>
</html>'''
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(html, encoding='utf-8')
    return OUTPUT


if __name__ == '__main__':
    path = build()
    print(f'Wrote {path} ({path.stat().st_size:,} bytes)')
