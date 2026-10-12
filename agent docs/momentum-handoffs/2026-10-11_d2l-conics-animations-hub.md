# Momentum handoff — D2L Conics animations hub (sandbox)

**Written:** 2026-10-11

## Read first
- This conversation arc (D2L Manage Files + Content iframe); no dedicated recipe yet.
- `School Scrips/School documents/conics-d2l/index.html` — canonical hub source.
- `School Scrips/Macro App/scripts/probe_manage_files_paths.py` (`--mp4-links` scrapes `viewFile.d2lfile` hrefs when Manage Files → **animations** is open).
- `School Scrips/Macro App/scripts/diagnose_conics_hub_video.py` — tests index/MP4 URL shapes via CDP (`127.0.0.1:9224`).
- Optional prior art (different layout): `My Drive/M2412/Unit 3 (10.2 - 10.7)/Conics/index.html` + `player.html` (links to `player.html?clip=` and `videos/*.mp4` — **do not** upload that pair to D2L animations unless paths are fixed).

## Objective and phase
Chase wants **Conics Manim clips inside Brightspace** without the student portal: MP4s in course files, a **single hub UI** students reach by opening a **Content module** (not a separate browser tab). Phase: **sandbox proof on M1314 test course** (`ou=1726642`). Module description **iframe** works when pointed at `index.html`; **clip playback** was still broken at handoff — root causes identified, **link-based `index.html` written but not yet confirmed** after re-upload to D2L.

## Chase's desired feel
- Stay **inside D2L** (Brightspace chrome); module opens to the hub — **no extra click** on a “Web Page” topic if possible (iframe in **module description**, not a linked topic).
- Same general idea as portal Conics gallery / Drive `Conics` index: **Parabolas / Ellipses / Hyperbolas**, big dwell-friendly targets.
- **No Math Portal** for this experiment unless he changes mind later.
- Duplicates like `parabola-opens-up(1).mp4` are fine as long as **plain** `parabola-opens-up.mp4` exists.

## Accepted decisions
- **Manage Files folder:** `/content/enforced/1726642-SA_1588_1785419431/animations/` (all MP4s + `index.html` siblings, flat names).
- **Student entry:** Content module → **Description** → Source Code → iframe:
  ```html
  <iframe
    src="/content/enforced/1726642-SA_1588_1785419431/animations/index.html"
    title="Conics animations"
    style="width:100%; min-height:900px; border:0;"
  ></iframe>
  ```
- **No separate “index” Content topic required** once description iframe works (Chase deleted that topic; description must keep the iframe).
- **Google Drive copy** for sync: `My Drive/M2412/Unit 3 (10.2 - 10.7)/Conics/animations/` (8 gallery MP4s + `index.html`; optional extra `conics-intro.mp4` not in hub list).
- **Portal clip list** (8 files): `parabola-opens-up`, `parabola-directrix`, `parabola-opens-left`, `ellipse-horizontal`, `ellipse-vertical`, `ellipse-definition`, `hyperbola-horizontal`, `hyperbola-vertical` — see `student-portal/.../conicsGuide.ts`.

## Rejected / don't rediscover
- **External link** to Netlify portal for this test.
- **Assuming** `/content/enforced/.../file.mp4` works in `<video src>` — on Lone Star it returned **`text/html`** (not MP4 bytes) in CDP checks; embedded `<video>` + absolute enforced URLs **will not play**.
- **Old white `index.html`** on D2L (title “Conics”, links to `player.html?clip=...`) — that file was live at `…/animations/index.html` and explains “links do nothing” (`player.html` not in folder).
- **Fully automated Manage Files upload** via CDP — file chooser worked; commit Upload flaky; **Chase uploaded MP4s manually**.
- **Duplicate MP4 names** as the cause of failure — originals with correct names are present.

## Implementation state
- **On D2L (Chase):** MP4s uploaded to **animations**; module iframe showed hub at least once; clip links failed with old index + video-tag approach.
- **Repo / Drive (source of truth for next upload):**
  - `School Scrips/School documents/conics-d2l/index.html` — **link-based hub** (dark theme, `<a href="*.mp4">` per clip, no JS, no `<video>`). Copied to Drive `…/Conics/animations/index.html`.
- **Macro App helpers (uncommitted utilities):**
  - `scripts/upload_manage_files_animations.py` — folder create + upload (incomplete).
  - `scripts/probe_manage_files_paths.py` — paths + `--mp4-links`.
  - `scripts/diagnose_conics_hub_video.py` — index/MP4 probes.
- **Not done:** Chase has **not** confirmed the **new link-based** `index.html` after overwrite on D2L. No git commit requested this session.

## Verified via CDP (Macro App, logged-in)
- `https://d2l.lonestar.edu/content/enforced/1726642-SA_1588_1785419431/animations/index.html` served **old** hub (no `#player`, links to `player.html`).
- `GET …/animations/parabola-opens-up.mp4` → **200** but **`Content-Type: text/html`**, body starts with `<!DOCTYPE html>`.
- Manage Files table links use **`/d2l/common/viewFile.d2lfile/...`** (working path for file open); scrape when **inside animations** folder.

## Open questions
- Do **same-tab `.mp4` links** from the new `index.html` inside the module iframe open D2L’s native video viewer? **Test first** after re-upload.
- If links still fail: rebuild hub with **hardcoded or scraped `viewFile.d2lfile` URLs** per file (run `--mp4-links` with Manage Files on animations).
- Chase may want **one-page player** (portal-style) later — needs viewFile URLs or different hosting, not enforced-path `<video>`.
- Production course path will differ from `1726642-SA_1588_1785419431` — update iframe + any baked URLs when moving off sandbox.

## Exact next step (do this first)
1. Ask Chase to confirm he **re-uploaded** `index.html` from `…/Conics/animations/` and replaced the old file on D2L (page title should be **“Conics Animations”**, dark background, eight `.mp4` links — **not** “Conics” white page with `player.html`).
2. **View as Student** → open the module → click **Opens up** → report: video plays, blank, or download only.
3. If fail: Macro App open → Manage Files → **animations** → run `python scripts/probe_manage_files_paths.py --mp4-links`, wire those hrefs into `index.html` (or a small generator script), re-upload, retest.
4. Do **not** launch GUI or Netlify deploy without asking.
