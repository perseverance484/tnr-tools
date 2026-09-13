import { readFile, writeFile, mkdir } from "node:fs/promises";
import { createHash } from "node:crypto";
import { stableStringify } from "../src/hash.mjs";
import { normalizeEffect } from "../src/effects.mjs";
import { templateDefinitions } from "../templates/series.mjs";
import { assertTemplate } from "../src/template.mjs";
const sha = (s) => createHash("sha256").update(s).digest("hex");
const read = async (p) =>
  JSON.parse(await readFile(new URL(p, import.meta.url), "utf8"));
const sourceFiles = [
  "tnr_results_1789188714166.json",
  "tnr_results_1789271613950.json",
  "tnr_results_1789273598969.json",
  "public-refresh-2026-09-13.json",
  "bloodline-refresh-2026-09-13.json",
];
const raw = new Map(),
  bloodlines = new Map(),
  summons = new Map(),
  sources = [];
for (const file of sourceFiles) {
  const bytes = await readFile(new URL("../fixtures/" + file, import.meta.url));
  sources.push({ file: "fixtures/" + file, sha256: sha(bytes) });
  const doc = JSON.parse(bytes);
  const add = (record, capture, level) => {
    raw.set(record.id, {
      record,
      provenance: {
        file: "fixtures/" + file,
        proc: capture.proc,
        capturedAt: capture.at,
      },
      level,
    });
  };
  for (const c of doc.captures) {
    if (c.proc === "jutsu.get") add(c.data, c);
    if (c.proc === "jutsu.getAll")
      c.data.data.forEach((x) => add(x, c, x.jutsuType === "AI" ? 1 : 25));
    if (c.proc === "bloodline.get")
      bloodlines.set(c.data.id, {
        ...c.data,
        provenance: { file: "fixtures/" + file, capturedAt: c.at },
      });
    if (c.proc === "profile.getAi") {
      summons.set(c.data.userId, c.data);
      for (const j of c.data.jutsus) add(j.jutsu, c, j.level);
    }
  }
}
const assetMeta = await read("../fixtures/official-assets.json");
const imageData = {};
for (const a of Object.keys(assetMeta)
  .sort()
  .map((k) => assetMeta[k])) {
  const bytes = await readFile(new URL("../public" + a.url, import.meta.url));
  if (sha(bytes) !== a.sha256) throw Error("Asset hash mismatch " + a.url);
  imageData[a.url] = "data:image/webp;base64," + bytes.toString("base64");
}
const jutsu = [...raw.values()]
  .map(({ record: r, provenance, level }) => ({
    id: r.id,
    name:
      r.name === "OHKO" && r.jutsuType === "AI" ? "Summon Departure" : r.name,
    sourceName: r.name,
    description: /^(New jutsu description|placeholder)$/i.test(
      r.description.trim(),
    )
      ? ""
      : r.description.trim(),
    image: assetMeta[r.id],
    bloodlineId: r.bloodlineId || null,
    type: r.jutsuType,
    rank: r.jutsuRank,
    requiredRank: r.requiredRank,
    action: r.actionCostPerc,
    range: r.range,
    cooldown: r.cooldown,
    target: r.target,
    method: r.method,
    hidden: r.hidden,
    costs: {
      stamina: r.staminaCost,
      chakra: r.chakraCost,
      health: r.healthCost,
    },
    level: level ?? (r.jutsuType === "AI" ? 1 : 25),
    effects: r.effects
      .map((e) =>
        normalizeEffect(e, r, level ?? (r.jutsuType === "AI" ? 1 : 25)),
      )
      .filter(Boolean),
    provenance,
  }))
  .sort((a, b) => (a.id < b.id ? -1 : a.id > b.id ? 1 : 0));
const bloodlineRecords = [...bloodlines.values()].map((b) => ({
  id: b.id,
  name: b.name,
  rank: b.rank,
  description: b.description,
  image: assetMeta[b.id],
  classification: b.statClassification,
  regen: b.regenIncrease,
  traits: b.traits,
  level: 100,
  effects: b.effects
    .map((e) => normalizeEffect(e, { ...b, target: "SELF" }, 100))
    .filter(Boolean),
  provenance: b.provenance,
}));
const templates = templateDefinitions.map((t) => ({
  ...t,
  name: bloodlines.get(t.bloodlineId).name,
  hero: assetMeta[t.bloodlineId],
}));
const registry = {
  schema: "tnr-catalog/v1",
  sourceSha: "36c5873b7b6ee5fd3af717008d7c51b0f185b756",
  normalizerVersion: 1,
  templates,
  jutsu,
  bloodlines: bloodlineRecords,
  summons: [...summons.values()].map((s) => ({
    id: s.userId,
    name: s.username,
    image: assetMeta[s.userId],
    jutsuIds: s.jutsus.map((j) => j.jutsuId),
  })),
  sources,
  imageData,
};
registry.version = "catalog-" + sha(stableStringify(registry)).slice(0, 20);
for (const t of templates) assertTemplate(t, registry);
// Delivery projection only: the version still pins the complete canonical catalog.
// Official bytes stay in /assets and the server catalog, never the initial JS.
const { imageData: embeddedImages, ...browserRegistry } = registry;
browserRegistry.assetHashes = Object.fromEntries(
  Object.values(assetMeta).map((a) => [a.url, a.sha256]),
);
const outputs = {
  "../catalog/browser.v1.json":
    JSON.stringify(JSON.parse(stableStringify(browserRegistry)), null, 2) +
    "\n",
  "../catalog/catalog.v1.json":
    JSON.stringify(JSON.parse(stableStringify(registry)), null, 2) + "\n",
  "../catalog/catalog-meta.json":
    JSON.stringify(
      {
        version: registry.version,
        sourceSha: registry.sourceSha,
        sources,
        templateVersions: templates.map((t) => ({
          slug: t.slug,
          version: t.version,
        })),
        jutsuLevel: 25,
        bloodlineLevel: 100,
        summonLevel: "captured equipped level",
        scope:
          "Two complete bloodline kits, linked summon abilities, and the reference guides’ support-jutsu catalog",
      },
      null,
      2,
    ) + "\n",
};
for (const [path, text] of Object.entries(outputs)) {
  if (process.argv.includes("--check")) {
    if ((await readFile(new URL(path, import.meta.url), "utf8")) !== text)
      throw Error("Stale generated " + path);
  } else await writeFile(new URL(path, import.meta.url), text);
}
console.log(
  `${registry.version}: ${templates.length} complete templates; ${jutsu.length} jutsu; ${registry.summons.length} summons. ${process.argv.includes("--check") ? "Reproducible." : "Generated."}`,
);
