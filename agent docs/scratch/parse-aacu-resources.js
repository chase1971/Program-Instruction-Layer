const fs = require("fs");
const path = String.raw`C:\Users\chase\.cursor\projects\c-Users-chase-Documents-Programs\agent-tools\24572f10-79ee-4e0a-bae6-62ca34b51f0a.txt`;
const t = fs.readFileSync(path, "utf8");
const start = t.indexOf("{");
const end = t.indexOf("\n### Ran Playwright");
const j = JSON.parse(t.slice(start, end).trim());
const lines = [];
lines.push(`Checked ${j.total} presentations. ${j.withResourcesCount} have Resources.`);
lines.push("");
j.withResources.forEach((s, i) => {
  lines.push(`${i + 1}. ${s.name}`);
  for (const f of s.files) lines.push(`   - ${f.name}`);
  lines.push("");
});
const out = String.raw`C:\Users\chase\Documents\Programs\agent docs\scratch\aacu-sessions-with-resources.txt`;
fs.writeFileSync(out, lines.join("\n"), "utf8");
console.log(lines.join("\n"));
