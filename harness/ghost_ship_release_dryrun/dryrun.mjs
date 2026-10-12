// Headless Forge dry run of push/90 (offline; no socket, no game, no upload). Requires Forge 0.5.2+.
//
//   (cd forge && npm ci --ignore-scripts)            # once; lockfile-pinned test dependencies
//   node harness/ghost_ship_release_dryrun/dryrun.mjs [--out <dir>]
//
// Drives the SHIPPED ForgeCore and compose() wiring (forge/test/compose.mjs is the one way Forge's
// own tests build the app) through select -> image-pack fetch/verify -> Start -> run -> read-back
// -> export, against Forge's in-memory FakeGame. Only the environment is substituted:
//
//   game      FakeGame seeded from committed captures:
//               AIs + profiles   push/86 (tnr_results_1791727613862.json)
//               quests           push/89 (tnr_results_1791768613624.json)
//               jutsu            the push/86 embedded kit rows
//               items            October 1 item.get rows (Serum, Fragment)
//             SYNTHETIC (no capture exists): The Skyglass Crown item row and the nine existing
//             scene-asset rows, minimal shells carrying only id/name/type/image; and the post-0056
//             columns (offence, defence, six masteries) added to FakeGame's AI create placeholder,
//             because the live userData row has them and FakeGame's placeholder predates 0056.
//   github    raw(path, ref) = `git show <ref>:<path>` from this checkout (the imagePack commit)
//   uploader  records each File (name, size, sha256) and returns a fake CDN URL; nothing leaves
//
// FakeGame merges updates without server logic (no zod, no scaleEditedAi, no updateUserContent),
// so this proves FORGE: parse, plan, phase order, ref resolution, pre-send validation against live
// rows, merges, kit re-send, rules step, image-pack verification and binding, read-back and the
// results bundle. It does not prove server-side effects.

import { readFileSync, writeFileSync, mkdirSync } from "node:fs";
import { execFileSync } from "node:child_process";
import { createHash } from "node:crypto";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { composeForTest } from "../../forge/test/compose.mjs";
import { FakeGame } from "../../forge/test/fakegame.mjs";
import { MemoryStorage, fakeClock } from "../../forge/test/shim.mjs";
import { ForgeCore } from "../../forge/src/core/core.mjs";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..", "..");
const MANIFEST = "push/90_ghost_ship_skyglass_release.json";
const rd = (rel) => JSON.parse(readFileSync(join(ROOT, rel), "utf8"));
const caps = (rel, proc) => rd(rel).captures.filter((c) => c.proc === proc && c.data).map((c) => c.data);
const sha = (buf) => createHash("sha256").update(Buffer.from(buf)).digest("hex");
const outIdx = process.argv.indexOf("--out");
const OUT = outIdx > 0 ? process.argv[outIdx + 1] : null;

const POST0056 = { offence: 10, defence: 10, ninjutsuMastery: 10, genjutsuMastery: 10, taijutsuMastery: 10,
  bukijutsuMastery: 10, bloodlineMastery: 10, sageMastery: 10 };

class SeededGame extends FakeGame {
  handle(path, input) {
    const r = super.handle(path, input);
    if (path === "profile.create" && r.ok && r.data && r.data.success) Object.assign(this.tables.ai.get(r.data.message), POST0056);
    return r;
  }
}

function seed(game) {
  const synthetic = [];
  for (const a of caps("harvests/inbox/tnr_results_1791727613862.json", "profile.getAi")) {
    const row = structuredClone(a);
    for (const uj of row.jutsus) if (!game.tables.jutsu.has(uj.jutsuId)) game.seed("jutsu", structuredClone(uj.jutsu));
    game.seed("ai", row);
  }
  for (const p of caps("harvests/inbox/tnr_results_1791727613862.json", "ai.getAiProfile")) game.seed("aiProfile", structuredClone(p));
  for (const q of caps("harvests/inbox/tnr_results_1791768613624.json", "quests.get")) game.seed("quest", structuredClone(q));
  for (const i of caps("harvests/inbox/tnr_results_1790826836406.json", "item.get")) {
    if (["XhilCv1Hq4eNt-Wddok-m", "ayiRmSjWs05lMPyL3G-1d"].includes(i.id)) game.seed("item", structuredClone(i));
  }
  game.seed("item", { id: "yTS9TSpr_QLnh_3zmEpGg", name: "The White Crown", itemType: "ACCESSORY", image: "https://example.invalid/old-crown.webp", hidden: false, effects: [] });
  synthetic.push("item yTS9TSpr_QLnh_3zmEpGg (The White Crown) shell");
  const scenes = rd("state/ghost_ship_retheme_patch.json").sceneAssetRenames;
  const chars = new Set(["6iwMYC8WTCGJTf2QIYfBz", "xm3F2YXkNPeLWHRAUnbmF", "4Cu4EBaWRsGm5J_Ld1hTt"]);
  for (const id of Object.keys(scenes)) {
    game.seed("asset", { id, name: `old ${id}`, type: chars.has(id) ? "SCENE_CHARACTER" : "SCENE_BACKGROUND", image: `https://example.invalid/old-${id}.webp`,
      folder: "GhostShip", frames: 1, speed: 1, licenseDetails: "TNR", onInitialBattleField: false, hidden: false });
    synthetic.push(`asset ${id} shell`);
  }
  return synthetic;
}

const text = readFileSync(join(ROOT, MANIFEST), "utf8");
const manifest = JSON.parse(text);
const game = new SeededGame();
const synthetic = seed(game);
const github = {
  list: async () => [], text: async () => text, put: async () => ({ sha: "dryrun" }),
  raw: async (path, ref) => {
    const buf = execFileSync("git", ["-C", ROOT, "show", `${ref}:${path}`], { maxBuffer: 64 << 20 });
    return buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength);
  },
};
const uploads = [];
const uploader = {
  async upload(file) {
    const digest = sha(await file.arrayBuffer());
    uploads.push({ name: file.name, size: file.size, type: file.type, sha256: digest });
    return { ufsUrl: `https://utfs.io/f/dryrun-${digest.slice(0, 16)}`, key: digest.slice(0, 8), fileHash: digest };
  },
};

const storage = new MemoryStorage();
const clock = fakeClock();
const d = composeForTest({ game, storage, clock });
d.github = github;
const notes = [];
const core = new ForgeCore({ version: "dryrun", storage, now: clock, ...d });
core.runner.uploader = uploader;
core.subscribe((n) => notes.push(n));

const checks = [];
const check = (name, ok, detail) => { checks.push({ name, pass: !!ok, detail: ok ? undefined : detail }); };

await core.selectManifest({ name: "90_ghost_ship_skyglass_release.json", path: MANIFEST, number: 90, text });
const sel = core.state.selected;
check("selection: no parse/plan/pre-send problems", sel && sel.problems.length === 0, sel?.problems);
check("selection: no protected-procedure block", sel && sel.blocked.length === 0, sel?.blocked);
const packEntries = sel?.packResult?.entries ?? [];
check("image pack: every bound file fetched at the ref and verified (sha256 + bytes)",
  packEntries.length === Object.keys(manifest.imagePack.files).length && packEntries.every((e) => e.state === "ready"),
  packEntries.filter((e) => e.state !== "ready"));

await core.startJob();
const jobId = core.state.jobId;
const job = jobId ? core.journal.get(jobId) : null;
check("job opened and finished DONE", job && job.state === "DONE", job && { state: job.state, pause: job.pause });
const notVerified = job ? job.items.filter((i) => i.state !== "VERIFIED").map((i) => ({ idx: i.idx, name: i.name, state: i.state, phase: i.phase, error: i.error, verify: i.verify })) : ["no job"];
check(`all ${manifest.items.length} items VERIFIED by read-back`, job && notVerified.length === 0, notVerified);
const exported = notes.find((n) => n.type === "export");
const bundle = exported ? JSON.parse(exported.text) : null;
check("results bundle exported with outcome success", bundle && bundle.outcome === "success", bundle && { outcome: bundle.outcome, postflight: bundle.postflight });
check("postflight: every entry matches, none unresolved", bundle && bundle.postflight && bundle.postflight.unresolved === 0 && bundle.postflight.diff === 0,
  bundle && bundle.postflight);

// ---- final fake-game state
const leftRefs = [];
for (const [t, m] of Object.entries(game.tables)) for (const row of m.values()) {
  const s = JSON.stringify(row);
  for (const r of s.match(/"@(jutsu|ai|scene|item|quest|bloodline|img):[^"]+"/g) ?? []) leftRefs.push(`${t}: ${r}`);
}
check("no unresolved @ref left in any table", leftRefs.length === 0, leftRefs.slice(0, 10));
check("uploads: one per bound file, bytes equal the pack", uploads.length === Object.keys(manifest.imagePack.files).length
  && uploads.every((u) => manifest.imagePack.files[u.name]?.sha256 === u.sha256), uploads.map((u) => u.name));

const ais = [...game.tables.ai.values()];
const sealwright = ais.find((a) => a.username === "Sealwright");
const captain = game.tables.ai.get("QY69h271Nx9uHrBeR6jwW");
const keys = Object.keys(POST0056);

// ---- RUL-2026-10-12-012 stats as Forge writes them (server-side scaling is proven by the STATS gate)
const COMBAT = ["offence", "defence", "strength", "intelligence", "willpower", "speed"];
check("Sealwright: one create carried all six combat fields at 1,391,300 and statsMultiplier 5 (no follow-up edit)",
  sealwright && COMBAT.every((k) => sealwright[k] === 1391300) && sealwright.statsMultiplier === 5 && !("preferredStat" in sealwright),
  sealwright && Object.fromEntries([...COMBAT, "statsMultiplier"].map((k) => [k, sealwright[k]])));
check("Sealwright masteries equal the regular Captain's", sealwright && keys.filter((k) => /Mastery$/.test(k)).every((k) => sealwright[k] === captain[k]));
const capped = ["texZaFi42S3EvJZBwQ8cd", "AQi-bHJ-5tHXtxrnc0P9E", "0PZU_FvlbM3ErYGlD5r56", "v7T9_XdGMfP46em0dPuBc", "2OXJEXoktxJcjqMkE851g",
  "3V_gdHYaclMB1gTyOPAbV", "d6g0mOM7RBSsYI1hrUVT9", "QY69h271Nx9uHrBeR6jwW", "fDU9jCPZtH7YHbdQPO9RF"];
check("9 included existing AIs written with statsMultiplier 5", capped.every((u) => game.tables.ai.get(u).statsMultiplier === 5), capped.map((u) => game.tables.ai.get(u).statsMultiplier));
check("hazards keep statsMultiplier 10 / 20", game.tables.ai.get("wTgO-Q32caSSd0is1QIS7").statsMultiplier === 10 && game.tables.ai.get("frc9LTxqQlM7mncG4VZGK").statsMultiplier === 20);
const aiSaves = game.calls.filter((c) => c.path === "profile.updateAi");
check("no AI save sent the 0056-dropped preferredStat", aiSaves.length > 0 && aiSaves.every((c) => !("preferredStat" in (c.input?.data ?? {}))), aiSaves.filter((c) => "preferredStat" in (c.input?.data ?? {})).map((c) => c.input.id));
check("new items carry no 0056-removed requirement column", [...game.tables.item.values()].filter((i) => /^Skyglass (Katana|Crystal|Filament|Reliquary)$/.test(i.name)).every((i) => !Object.keys(i).some((k) => /^required(Ninjutsu|Genjutsu|Taijutsu|Bukijutsu)(Offence|Defence)$/.test(k))));
const swProfile = sealwright && game.tables.aiProfile.get(sealwright.aiProfileId);
check("Sealwright rules written: 10 rules, includeDefaultRules false", swProfile && swProfile.rules.length === 10 && swProfile.includeDefaultRules === false, swProfile);
check("Sealwright kit 7, avatar uploaded", sealwright && sealwright.jutsus.length === 7 && /dryrun-/.test(sealwright.avatar), sealwright && { kit: sealwright.jutsus.length, avatar: sealwright.avatar });
const renames = rd("state/ghost_ship_retheme_patch.json").aiRenames;
const badAi = Object.entries(renames).filter(([u, n]) => { const a = game.tables.ai.get(u); return !a || a.username !== n || !/dryrun-/.test(a.avatar); });
check("11 AIs renamed with new avatars", badAi.length === 0, badAi);
const crowned = game.tables.ai.get("fDU9jCPZtH7YHbdQPO9RF");
const katana = [...game.tables.item.values()].find((i) => i.name === "Skyglass Katana");
check("Crowned loot: Fragment 20, Katana 3 (ref resolved to the created Katana)",
  crowned && katana && crowned.items.some((i) => i.itemId === "ayiRmSjWs05lMPyL3G-1d" && i.dropChancePerc === 20)
  && crowned.items.some((i) => i.itemId === katana.id && i.dropChancePerc === 3), crowned && crowned.items);
const crystal = [...game.tables.item.values()].find((i) => i.name === "Skyglass Crystal");
const filament = [...game.tables.item.values()].find((i) => i.name === "Skyglass Filament");
const reliquary = [...game.tables.item.values()].find((i) => i.name === "Skyglass Reliquary");
check("Crystal recipe resolves to the created Filament x12", crystal && filament && JSON.stringify(crystal.craftingRequirements) === JSON.stringify([{ ids: [filament.id], number: 12 }]), crystal && crystal.craftingRequirements);
check("Reliquary loot table resolves Filament and Crystal ids", reliquary && JSON.stringify(reliquary.effects[0].reward_items.map((r) => r.ids[0])) === JSON.stringify([filament.id, "05hx4hI0I4L2vAME8CcZu", filament.id, "XhilCv1Hq4eNt-Wddok-m", "ONMLl57L7o0MivjhySHMA", crystal.id]), reliquary && reliquary.effects[0].reward_items);
check("all new items created hidden", [katana, crystal, filament, reliquary].every((i) => i && i.hidden === true));
for (const qid of ["6Ri-W5TtUrEMWpyYlnf_F", "HckXVOf-qk6ESU9t5rxLh"]) {
  const q = game.tables.quest.get(qid);
  const obj = q.content.objectives;
  const bs = obj.find((o) => o.id === "b_sealwright");
  const ws = obj.find((o) => o.id === "w_secret");
  check(`quest ${qid}: 83 objectives, hidden, new icon, Sealwright battle and Reliquary reward resolved`,
    obj.length === 83 && q.hidden === true && /dryrun-/.test(q.image) && bs.opponentAIs[0].ids[0] === sealwright?.userId && ws.reward_items[0].ids[0] === reliquary?.id,
    { n: obj.length, hidden: q.hidden, image: q.image, opp: bs?.opponentAIs, reward: ws?.reward_items });
}
const scenes = rd("state/ghost_ship_retheme_patch.json").sceneAssetRenames;
const badScene = Object.entries(scenes).filter(([id, n]) => { const a = game.tables.asset.get(id); return a.name !== n || !/dryrun-/.test(a.image); });
check("9 existing scene assets renamed with new art", badScene.length === 0, badScene);
const edited = rd("state/ghost_ship_legacy_jutsu_conversion.json").conversions;
const excluded = rd("state/ghost_ship_legacy_jutsu_edit_scope.json").excluded;
const badJ = edited.filter((c) => { const j = game.tables.jutsu.get(c.targetId); return excluded[c.targetId] ? j.name !== excluded[c.targetId].liveName : j.name !== c.after.name; });
check("9 legacy jutsu renamed; Counter Stance / Battle Trance untouched", badJ.length === 0, badJ.map((c) => c.targetId));
// law 60 order: every unequip landed before the first jutsu edit, every re-equip after the last
const calls = game.calls.map((c, i) => ({ i, path: c.path, id: c.input?.id }));
const jutsuWrites = calls.filter((c) => c.path === "jutsu.update").map((c) => c.i);
const legacyIds = new Set(edited.filter((c) => !excluded[c.targetId]).map((c) => c.targetId));
const aiWrites = calls.filter((c) => c.path === "profile.updateAi").map((c) => ({ i: c.i, kit: game.calls[c.i].input.data.jutsus ?? [] }));
const unequipBefore = aiWrites.filter((w) => w.i < Math.min(...jutsuWrites));
const holdsLegacyDuringEdit = aiWrites.filter((w) => w.i > Math.min(...jutsuWrites) && w.i < Math.max(...jutsuWrites) && w.kit.some((j) => legacyIds.has(j)));
check("law 60 order: 6 unequips before the first jutsu edit; no AI re-equips an edited jutsu mid-edit",
  unequipBefore.length === 6 && unequipBefore.every((w) => !w.kit.some((j) => legacyIds.has(j))) && holdsLegacyDuringEdit.length === 0,
  { unequipBefore: unequipBefore.length, holdsLegacyDuringEdit });
const captures = bundle ? bundle.captures : [];
check("before/after captures all ok and persisted", captures.length === manifest.capture.before.length * 2 && captures.every((c) => c.ok && c.persistOk),
  captures.filter((c) => !c.ok || !c.persistOk).map((c) => [c.proc, c.input, c.error]));
check("no live-game socket: every call went to the in-memory FakeGame", game.calls.length > 0);

const failed = checks.filter((c) => !c.pass);
const report = {
  schema: "tnr.ghost_ship_release_dryrun", manifest: MANIFEST, manifestSha256: sha(Buffer.from(text)),
  imageRef: manifest.imagePack.ref, forgeVersionUnderTest: JSON.parse(readFileSync(join(ROOT, "forge/package.json"), "utf8")).version,
  job: job && { state: job.state, items: job.items.length }, gameCalls: game.calls.length,
  callsByPath: game.calls.reduce((m, c) => ((m[c.path] = (m[c.path] ?? 0) + 1), m), {}),
  uploads: uploads.length, synthetic, checks: checks.length, failed: failed.length, results: checks,
};
for (const c of checks) console.log(`${c.pass ? "PASS" : "FAIL"} ${c.name}${c.pass ? "" : "\n     " + JSON.stringify(c.detail).slice(0, 900)}`);
console.log(`\ndry run: ${checks.length - failed.length}/${checks.length} checks pass; ${game.calls.length} fake-game calls; ${uploads.length} uploads recorded`);
if (OUT) {
  mkdirSync(OUT, { recursive: true });
  writeFileSync(join(OUT, "dryrun_report.json"), JSON.stringify(report, null, 1) + "\n");
  if (bundle) writeFileSync(join(OUT, "dryrun_results_bundle.json"), JSON.stringify(bundle, null, 1) + "\n");
}
process.exit(failed.length ? 1 : 0);
