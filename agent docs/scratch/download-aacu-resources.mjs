import fs from "fs";
import path from "path";
import { chromium } from "playwright-core";

const outRoot = String.raw`C:\Users\chase\My Drive\AACU\documents`;
fs.mkdirSync(outRoot, { recursive: true });

const wanted = [
  "Coordinating AI Strategy Across the URI Campus: A Multi-Domain Approach",
  "Beyond Compliance: Reading AI Governance as a Signal of Institutional Digital Maturity",
  "Three Pathways, One Foundation: Faculty Champions Supporting AI Integration",
  "Utilizing a Networked Approach for Institutional AI Transformation",
  "14 Day AI Challenge: Fast, Fun, Low-Stakes Way to Boost Faculty Confidence",
  "From AI Experimentation to Institutional Coherence: A People-First Framework for Responsible Adoption",
  "TAKE AI.M: Preserving Engineering Judgement in AI-Assisted Learning Environments",
  "From AI Misuse to AI Literacy: Redesigning Business Courses for an AI-Infused Learning Environment",
  "From Players to Designers: Students Building AI-Assisted Sustainability Games",
  "Optimizing and Modernizing Student Success through AI",
  "Reclaim Your Time, Reclaim Your Agency: AI as Productivity Infrastructure for the Professoriate",
];

const norm = (s) =>
  String(s || "")
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, " ")
    .trim();

const sanitize = (s) =>
  String(s || "file")
    .replace(/[<>:"/\\|?*\u0000-\u001f]/g, "_")
    .replace(/\.+$/g, "")
    .replace(/\s+/g, " ")
    .trim()
    .slice(0, 120) || "file";

const eventId = "XAJTRV2VQTml9Tq-jMAhTQ";

const browser = await chromium.connectOverCDP("http://127.0.0.1:9227");
const context = browser.contexts()[0];
const page = context.pages().find((p) => p.url().includes("events.zoom.us"));
if (!page) {
  console.error("Zoom page not found");
  process.exit(1);
}

// Pull materials via in-page fetch (has auth), then download with CDP cookies.
const catalog = await page.evaluate(async (eventId) => {
  const listResp = await fetch(
    `https://events.zoom.us/api/v1/e/v/events/sessions?eventId=${eventId}&isLobby=true`,
    { credentials: "include" }
  );
  const sessions = await listResp.json();
  if (!Array.isArray(sessions)) return { error: sessions };

  const details = [];
  for (const s of sessions) {
    const sid = s.sessionId || s.id;
    const name = s.sessionName || s.title || "";
    const r = await fetch(
      `https://events.zoom.us/api/v2/e/v/lobby/events/${eventId}/sessions/${sid}/detail`,
      { credentials: "include" }
    );
    const j = await r.json();
    const d = j?.data || j;
    const materials = d?.resources?.materialUrls || [];
    details.push({
      sessionId: sid,
      name,
      materials: materials.map((m) => ({
        name: m.name || m.fileName || "download.bin",
        url: m.url || m.downloadUrl || m.link || null,
      })),
    });
  }
  return { details };
}, eventId);

if (catalog.error) {
  console.error("Catalog failed", catalog.error);
  process.exit(1);
}

const unmatched = [...wanted];
const matched = [];
for (const s of catalog.details) {
  const n = norm(s.name);
  const idx = unmatched.findIndex((w) => {
    const wn = norm(w);
    return n === wn || n.includes(wn) || wn.includes(n);
  });
  if (idx >= 0) {
    matched.push({ ...s, wanted: unmatched[idx] });
    unmatched.splice(idx, 1);
  }
}
if (unmatched.length) {
  for (const s of catalog.details) {
    const n = norm(s.name);
    for (const u of [...unmatched]) {
      const key = norm(u).split(" ").slice(0, 6).join(" ");
      if (n.includes(key)) {
        matched.push({ ...s, wanted: u });
        unmatched.splice(unmatched.indexOf(u), 1);
      }
    }
  }
}

console.log(`Matched ${matched.length}/${wanted.length}`);
if (unmatched.length) console.log("Unmatched:", unmatched);

const cdp = await context.newCDPSession(page);
const { cookies } = await cdp.send("Network.getAllCookies");
const cookieHeader = cookies
  .filter((c) => /zoom\.us$/i.test(c.domain.replace(/^\./, "")) || c.domain.includes("zoom.us"))
  .map((c) => `${c.name}=${c.value}`)
  .join("; ");

const summary = [];
let ok = 0;
let fail = 0;

for (const m of matched) {
  const folder = path.join(outRoot, sanitize(m.name));
  fs.mkdirSync(folder, { recursive: true });
  const filesOut = [];

  for (const item of m.materials) {
    const fileName = sanitize(item.name);
    let url = item.url;
    if (!url) {
      filesOut.push({ fileName, ok: false, error: "no url" });
      fail++;
      continue;
    }
    if (url.startsWith("/")) url = "https://events.zoom.us" + url;

    try {
      const resp = await fetch(url, {
        headers: {
          Cookie: cookieHeader,
          Referer: page.url(),
          "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36",
        },
        redirect: "follow",
      });
      const buf = Buffer.from(await resp.arrayBuffer());
      const head = buf.slice(0, 200).toString("utf8").toLowerCase();
      const looksHtml = head.includes("<html") || head.includes("<!doctype");
      if (!resp.ok || looksHtml || buf.length < 100) {
        filesOut.push({
          fileName,
          ok: false,
          status: resp.status,
          size: buf.length,
          looksHtml,
        });
        fail++;
        console.log(`FAIL ${m.name} -> ${fileName} status=${resp.status} size=${buf.length}`);
        continue;
      }
      const dest = path.join(folder, fileName);
      fs.writeFileSync(dest, buf);
      filesOut.push({ fileName, ok: true, status: resp.status, size: buf.length, dest });
      ok++;
      console.log(`OK  ${fileName} (${buf.length} bytes)`);
    } catch (e) {
      filesOut.push({ fileName, ok: false, error: String(e) });
      fail++;
      console.log(`FAIL ${fileName}: ${e}`);
    }
  }
  summary.push({ presentation: m.name, folder, filesOut });
}

console.log(JSON.stringify({ matched: matched.length, unmatched, ok, fail }, null, 2));
fs.writeFileSync(
  path.join(outRoot, "_download-summary.json"),
  JSON.stringify({ matched: matched.length, unmatched, ok, fail, summary }, null, 2)
);

browser.disconnect();
