const EPISODE_IDS = ["ep1", "ep2", "ep3", "ep4", "ep5", "ep6", "trader"];

const SECTION_LABELS_BY_EP = {
  ep1: {
    overview: "Overview",
    vision: "Country vision",
    decisions: "Decisions",
    prep: "Checklist",
    next: "Near-term plan",
  },
  ep2: {
    overview: "Overview",
    vision: "Direction",
    decisions: "Decisions",
    prep: "Actions",
    next: "Where it leaves off",
  },
  ep3: {
    overview: "Overview",
    vision: "Direction",
    decisions: "Decisions",
    prep: "Actions",
    next: "Where it leaves off",
  },
  ep4: {
    overview: "Overview",
    vision: "Direction",
    decisions: "Decisions",
    prep: "Actions",
    next: "Where it leaves off",
  },
  ep5: {
    overview: "Overview",
    vision: "Direction",
    decisions: "Decisions",
    prep: "Actions",
    next: "Where it leaves off",
  },
  ep6: {
    overview: "Overview",
    vision: "Direction",
    decisions: "Decisions",
    prep: "Actions",
    next: "Where it leaves off",
  },
  trader: {
    overview: "Overview",
    opening: "Opening economy",
    morocco: "Morocco wars",
    growth: "Growth and Africa",
    india: "India route",
    colonies: "Colonization machine",
    takeaways: "Strategy cards",
  },
};

const episodeTabs = [...document.querySelectorAll("#episode-tabs button")];
const sectionTabs = document.getElementById("section-tabs");
const pageSub = document.getElementById("page-sub");
const episodeRoot = document.getElementById("episode-root");
const loaded = new Set();
let currentEpisode = "ep1";
let currentSection = "overview";
let loadQueue = Promise.resolve();

function labelsFor(ep) {
  return SECTION_LABELS_BY_EP[ep] || SECTION_LABELS_BY_EP.ep1;
}

function rebuildSectionTabs() {
  const labels = labelsFor(currentEpisode);
  sectionTabs.innerHTML = "";
  Object.keys(labels).forEach((id) => {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.dataset.sec = id;
    btn.textContent = labels[id];
    if (id === currentSection) btn.classList.add("on");
    btn.addEventListener("click", () => showSection(id));
    sectionTabs.appendChild(btn);
  });
}

async function ensureEpisode(epId) {
  if (loaded.has(epId)) return;
  const res = await fetch(`/scratch/eu5-portugal/${epId}.html`);
  if (!res.ok) throw new Error(`Failed to load ${epId}: ${res.status}`);
  const html = await res.text();
  episodeRoot.insertAdjacentHTML("beforeend", html);
  loaded.add(epId);
}

function showSection(secId) {
  currentSection = secId;
  const ep = document.getElementById(currentEpisode);
  if (!ep) return;
  ep.querySelectorAll("section").forEach((s) => {
    s.classList.toggle("on", s.dataset.sec === secId);
  });
  sectionTabs.querySelectorAll("button").forEach((b) => {
    b.classList.toggle("on", b.dataset.sec === secId);
  });
  window.scrollTo(0, 0);
}

function showEpisode(epId, sectionId) {
  loadQueue = loadQueue.then(async () => {
    await ensureEpisode(epId);
    currentEpisode = epId;
    episodeTabs.forEach((b) => b.classList.toggle("on", b.dataset.episode === epId));
    episodeRoot.querySelectorAll(".episode").forEach((ep) => {
      ep.classList.toggle("on", ep.id === epId);
    });
    const ep = document.getElementById(epId);
    if (ep && ep.dataset.label) pageSub.textContent = ep.dataset.label;
    showSection(sectionId || "overview");
    rebuildSectionTabs();
    window.scrollTo(0, 0);
  }).catch((err) => {
    console.error(err);
    pageSub.textContent = "Could not load that episode. Refresh and try again.";
  });
  return loadQueue;
}

episodeTabs.forEach((b) => {
  b.addEventListener("click", () => showEpisode(b.dataset.episode, "overview"));
});

episodeRoot.addEventListener("click", (e) => {
  const gotoBtn = e.target.closest("[data-goto]");
  if (gotoBtn) {
    showSection(gotoBtn.dataset.goto);
    return;
  }
  const switchBtn = e.target.closest("[data-switch]");
  if (switchBtn) showEpisode(switchBtn.dataset.switch, "overview");
});

// Prefetch all episodes so tab switches stay snappy after the first load.
EPISODE_IDS.reduce(
  (chain, id) => chain.then(() => ensureEpisode(id).catch((err) => console.error(err))),
  Promise.resolve(),
).then(() => showEpisode("ep1", "overview"));
