/**
 * Export the hunts build spec: harness/skyglass_wreck_sim/hunts_spec.json.
 *
 *   TNR_SCRIPT=hunts_build.ts run.sh [--params overrides/hunts.params.json] [--spec-out hunts_spec.json]
 *
 * Per enemy (live AI records upgraded in place, plus the Foundry Warden): solo-tuned stats as replayed through the
 * server's scaleEditedAi, the jutsu list with each entry's provenance, and the ordered rules, each marked as a
 * reference to the shared endgame kit (engine/kits.ts dg-* copy, rule index) or as a hunt addition. Per hunt-boss
 * jutsu: the full record, validated against the live JutsuValidator (combat.ts; coordinateTargeting.ts through it),
 * marked NEW (library / hunt) or LIVE (live id). Rules are validated by AiRule (ai.ts) when built (kitlib), and each
 * AI row by insertAiSchema.
 */
import { existsSync, readdirSync, readFileSync, writeFileSync } from "node:fs";
import { join, resolve } from "node:path";
import { AiRule } from "@/validators/ai";
import { insertAiSchema } from "@/validators/aiInput";
import { JutsuValidator } from "@/validators/combat";
import { ALARM, buildHunts, buildPaths, CREW_TO_LIB, crownTemplates, DEFAULT_HUNT_PARAMS, LIVE, LIVE_JUTSU_FIXES, NAME, petFor, TERM } from "./hunts";
import { buildEndgame, DEFAULT_PARAMS, IDS } from "./kits";
import { LIB } from "./library";
import { buildTemplates, loadJson } from "./model";

const args = process.argv.slice(2);
const opt = (k: string) => {
  const i = args.indexOf(`--${k}`);
  return i >= 0 ? args[i + 1] : undefined;
};
const H = process.env.TNR_HARNESS!;
const baseline = loadJson(join(H, "data/baseline.json"));
const pp = opt("params");
const p = pp ? loadJson(resolve(pp)) : {};
const HP = { ...DEFAULT_HUNT_PARAMS, ...p, stats: { ...DEFAULT_HUNT_PARAMS.stats, ...(p.stats ?? {}) } };
const kpf = loadJson(join(H, "overrides/kits_endgame.params.json"));
const kitParams = { ...DEFAULT_PARAMS, ...kpf, pow: { ...DEFAULT_PARAMS.pow, ...(kpf.pow ?? {}) } };
const built = buildHunts(HP, kitParams);
const coreRupture = loadJson(join(H, "overrides/director_6wave_tuned.json")).jutsu["nCQETf-HNnbRec1OSY2-R"];
built.override.jutsu["nCQETf-HNnbRec1OSY2-R"] = coreRupture;
const T = buildTemplates(baseline, built.override as never);
Object.assign(T.enemies, crownTemplates(T.enemies[LIVE.warden]!.row, T.jutsu, HP));
const shared = (buildEndgame(kitParams, "endgame").override as any).newEnemies;
const SHARED_FROM: Record<string, string> = {
  [LIVE.warden]: IDS.warden, [LIVE.charge]: IDS.charge, [LIVE.sentinel]: IDS.sentinel, [LIVE.blade]: IDS.blade,
  [LIVE.wayfinder]: IDS.wayfinder, [LIVE.horror]: IDS.horror, [LIVE.captain]: IDS.captain, [LIVE.sealwright]: IDS.sealwright,
};
const libIds = new Set<string>([...Object.values(LIB.mark), ...Object.values(LIB.blast), ...Object.values(LIB.sig), LIB.loweredGuard, ...Object.values(LIB.crew)]);
const provenance = (id: string) => {
  if (libIds.has(id)) return { status: "NEW", source: "shared set-piece library (engine/library.ts, library_spec.json; lib-* id is a placeholder)" };
  if (id.startsWith("hunt-")) return { status: "NEW", source: "hunt-only (this spec; hunt-* id is a placeholder)" };
  if (id.startsWith("dg-")) return { status: "SHARED KIT", source: "endgame dungeon kit (build_spec.json endgame; dg-* id is a placeholder)" };
  return { status: "LIVE", source: `live record ${id}`, liveId: id };
};
const RECORD_FIELDS = [
  "name", "description", "battleDescription", "jutsuType", "jutsuRank", "requiredRank", "requiredLevel", "jutsuWeapon",
  "target", "method", "range", "coordinateTargeting", "methodSize", "cooldown", "actionCostPerc", "healthCost", "chakraCost",
  "staminaCost", "healthCostReducePerLvl", "chakraCostReducePerLvl", "staminaCostReducePerLvl", "battleUsageType",
  "elementClassification", "statClassification", "hidden", "extraBaseCost", "image", "effects",
];
const ANIM = /^(tg|dt|ch|cp|cc|fw|lg)_[a-z_]+$|^(mark-sigil|chain-hook-hit|skyglass-pane)$/;
const anims = (rec: any) => [...new Set(rec.effects.flatMap((e: any) => ["appearAnimation", "staticAnimation", "disappearAnimation"].map((k) => e[k]).filter((v: any) => typeof v === "string" && ANIM.test(v))))];
const RELATIONS = new Set(["jutsus", "items", "aiProfile", "titles", "raidBuffs", "cookingJobs", "village", "bloodline", "sageMode", "anbuSquad", "clan", "loadout", "userSkills", "userQuests", "completedQuests", "bounties", "bountySignups", "queue"]);
const key = (r: any) => JSON.stringify({ c: r.conditions, a: r.action });

const enemyIds = [LIVE.warden, LIVE.canister, LIVE.keeper, LIVE.charge, LIVE.foundry, LIVE.horror, LIVE.sentinel, LIVE.archivist, LIVE.sealwright, LIVE.stonebound, LIVE.wayfinder, LIVE.blade, LIVE.captain];
const usedJutsu = new Set<string>();
const ais = enemyIds.map((id) => {
  const e = T.enemies[id]!;
  const row = e.row;
  const rules = e.profile.rules as any[];
  const sh = SHARED_FROM[id] ? (shared[SHARED_FROM[id]!].rules as any[]).map((r: any) => (r.action.jutsuId && CREW_TO_LIB[r.action.jutsuId] ? { ...r, action: { ...r.action, jutsuId: CREW_TO_LIB[r.action.jutsuId] } } : r)) : [];
  const shKeys = sh.map(key);
  const aiInput = { ...Object.fromEntries(Object.entries(row).filter(([k]) => !RELATIONS.has(k))), jutsus: row.jutsus.map((uj: any) => uj.jutsuId) };
  const check = insertAiSchema.safeParse(aiInput);
  for (const uj of row.jutsus) usedJutsu.add(uj.jutsuId);
  const s = HP.stats[id];
  return {
    liveId: id, username: row.username,
    record: id === LIVE.foundry ? "live record created by push/262 (Foundry Warden), upgraded in place"
      : id === LIVE.stonebound ? "Crownhold live record (push/272 D3.REG4), used as stored: only summoned by Called to the Archive (HP and power % set by the summon)"
      : id === LIVE.archivist ? "Crownhold live record (push/272 D3.REG1, live readback stats), upgraded in place as the Archive alarm guard (RUL-2026-10-28-013); NOTE: the same record is a Crownhold D3 regular, so these stats also apply there"
      : `live record ${id}, upgraded in place`,
    soloTuning: s, level: row.level, rank: row.rank, statsMultiplier: row.statsMultiplier, poolsMultiplier: row.poolsMultiplier,
    pools: { maxHealth: row.maxHealth, maxChakra: row.maxChakra, maxStamina: row.maxStamina },
    stats: { offence: row.offence, defence: row.defence, strength: row.strength, intelligence: row.intelligence, willpower: row.willpower, speed: row.speed },
    effects: row.effects,
    kit: SHARED_FROM[id]
      ? `shared endgame kit of ${SHARED_FROM[id]} (build_spec.json endgame; engine/kits.ts) with the six crew additions remapped to the identical library records${(built.rules as any)[id].rules.length > sh.length ? ", plus the hunt-boss additions marked below" : ""}`
      : id === LIVE.keeper || id === LIVE.archivist || id === LIVE.stonebound ? "live kit and live rules (no shared endgame kit exists)" : (built.rules as any)[id]?.note,
    note: (built.notes as any)[id],
    jutsu: row.jutsus.map((uj: any) => ({ id: uj.jutsuId, name: T.jutsu[uj.jutsuId]?.name ?? uj.jutsuId, ...provenance(uj.jutsuId) })),
    includeDefaultRules: e.profile.includeDefaultRules,
    rules: rules.map((r, i) => {
      const k = shKeys.indexOf(key(r));
      const ok = AiRule.safeParse(r).success;
      const from = k >= 0 ? `shared ${SHARED_FROM[id]} rule ${k}`
        : id === LIVE.keeper || id === LIVE.archivist || id === LIVE.stonebound ? "live rule"
        : r.action.description.startsWith("hold while veiled") ? `SHARED KIT FIX for ${SHARED_FROM[id]}: append as its last rule (stealth give-up death)`
        : "hunt";
      return { index: i, from, note: r.action.description, conditions: r.conditions, action: r.action, aiRule: ok ? "ok" : "INVALID" };
    }),
    signatureRules: (built.override.signatures as any)[id] ?? null,
    scaleEditedAiNotes: e.notes,
    insertAiSchemaCheck: check.success ? "ok" : check.error.issues.map((i) => `${i.path.join(".")}: ${i.message}`).slice(0, 6),
  };
});

// Hunt-boss jutsu: every jutsu in a hunt boss's rules that is not part of the shared crew kit.
const BOSSES = [LIVE.foundry, LIVE.sealwright, LIVE.sentinel, LIVE.wayfinder, LIVE.blade, LIVE.captain];
const bossJutsu = new Map<string, string[]>();
for (const b of BOSSES) for (const r of (built.rules as any)[b].rules) if (r.action.jutsuId) bossJutsu.set(r.action.jutsuId, [...new Set([...(bossJutsu.get(r.action.jutsuId) ?? []), NAME[b]!])]);
const jutsuSpec = [...usedJutsu].sort().map((id) => {
  const rec = T.jutsu[id];
  const parsed = JutsuValidator.safeParse(rec);
  const pv = provenance(id);
  return {
    id, ...pv, usedBy: enemyIds.filter((e) => T.enemies[e]!.row.jutsus.some((uj: any) => uj.jutsuId === id)).map((e) => NAME[e]),
    huntBossSetPiece: bossJutsu.has(id) && pv.status !== "SHARED KIT",
    record: pv.status === "LIVE" && !bossJutsu.has(id) ? undefined : Object.fromEntries(RECORD_FIELDS.map((k) => [k, rec[k]])),
    animationPlaceholders: anims(rec),
    validator: parsed.success ? "JutsuValidator: ok" : `JutsuValidator: ${parsed.error.issues.map((i) => i.message).join("; ")}`,
  };
});
const newBeyondLibrary = jutsuSpec.filter((j) => j.status === "NEW" && j.id.startsWith("hunt-"));
const libraryUsed = jutsuSpec.filter((j) => j.status === "NEW" && libIds.has(j.id));

/** AIs holding a jutsu in the committed captures (rosters; a live check is still needed before the edit). */
function holdersOf(jid: string) {
  const out = new Map<string, string>();
  const repo = process.env.TNR_REPO!;
  const walk = (x: any) => {
    if (Array.isArray(x)) x.forEach(walk);
    else if (x && typeof x === "object") {
      const js = x.jutsus;
      if (Array.isArray(js) && x.isAi !== false && js.some((j: any) => (typeof j === "string" ? j : j?.jutsuId) === jid)) out.set(x.userId ?? x.id, x.username ?? x.name);
      for (const v of Object.values(x)) walk(v);
    }
  };
  for (const f of readdirSync(join(repo, "harvests/inbox")).filter((f) => f.endsWith(".json"))) {
    const t = readFileSync(join(repo, "harvests/inbox", f), "utf8");
    if (t.includes(jid)) walk(JSON.parse(t));
  }
  return { count: out.size, ids: [...out.entries()].map(([id, name]) => `${id} (${name})`) };
}
/** Counters check: per hunt boss path, the win rate with each answer disabled against all answers on. */
function countersView(rows: any[]) {
  const by: Record<string, any> = {};
  for (const r of rows) {
    const b = (by[r.path] ??= { hunt: r.hunt, boss: r.fights[r.fights.length - 1].label, cases: {} });
    b.cases[r.case] = { win: `${r.wins}/${r.runs}`, bossWonOfReached: `${r.fights[r.fights.length - 1].won}/${r.fights[r.fights.length - 1].reached}`, endHpMedian: r.endHpPctMedian };
  }
  return by;
}
const paths = buildPaths(HP.compose ?? {});
const spec = {
  _about: "Skyglass treasure hunts, solo build spec (harness output; not pushed). Live crew records upgraded in place with solo-tuned stats; kits and rules reference the shared endgame kit (build_spec.json endgame) and the shared set-piece library (library_spec.json). lib-*, hunt-* and dg-* ids are placeholders: the builder mints real ids, and rule jutsuId references must be remapped. Generated by harness/skyglass_wreck_sim/engine/hunts_build.ts.",
  schemas: "validated against the live validators at engine pin c86f43f4: JutsuValidator (validators/combat.ts; coordinateTargeting.ts through it), AiRule (validators/ai.ts), insertAiSchema (validators/aiInput.ts)",
  params: { file: pp ?? "(defaults in engine/hunts.ts)", ...HP },
  jutsuCount: {
    newBeyondLibrary: newBeyondLibrary.map((j) => `${j.id} (${j.record?.name})`),
    libraryRecordsUsedByHunts: libraryUsed.map((j) => `${j.id} (${j.record?.name})`),
    liveRecordsUsedByHuntBosses: jutsuSpec.filter((j) => j.status === "LIVE" && j.huntBossSetPiece).map((j) => `${j.id} (${j.record?.name})`),
  },
  sharedKitFixes: [
    { record: "dg-first-blade (shared First Blade kit)", fix: "append rule: end turn, no conditions ('hold while veiled (no valid action)')", why: "while Glassveil Step's stealth lasts no rule matches and the engine's give-up path sets his HP to 0 (ai_v2.ts)" },
    { record: `${LIB.crew.ward} (Ward of Command, library crew addition)`, fix: "decreasedamagetaken row: target SELF -> INHERIT", why: "the SELF target (inherited from the Folding Screen Guard shape donor) makes the ward land on the caster, never on the ally the rule picks; the hunts use the fixed row" },
    ...Object.entries(LIVE_JUTSU_FIXES).map(([id, f]) => ({
      record: `${id} (${T.jutsu[id]?.name}), LIVE jutsu`, fix: f.note,
      procedure: "law 18: unequip it from every holder, edit the record, re-equip",
      holders: holdersOf(id),
    })),
  ],
  counters: existsSync(join(H, "results/hunts_counters.json")) ? countersView(JSON.parse(readFileSync(join(H, "results/hunts_counters.json"), "utf8"))) : "not run",
  playerPet: { model: "one modelled mid-rank companion per player, in every hunt fight (engine/hunts.ts petFor)", example: (({ species, ...p }) => ({ ...p, species: { rarity: species.rarity, role: species.role } }))(petFor({ userId: "player", username: "Player" })) },
  questDebuffs: { ALARM, TERM, source: "push/skyglass_hunts.gen.py (unchanged)" },
  hunts: Object.fromEntries(Object.entries(paths).map(([k, v]) => [k, { hunt: v.hunt, fights: v.fights.map((f) => ({ label: f.label, opponents: f.ids.map((i) => NAME[i]), debuffs: f.debuffs ? f.debuffs.map((d: any) => d.type) : [], boss: !!f.boss })) }])),
  ais, jutsu: jutsuSpec,
};
const out = resolve(opt("spec-out") ?? join(H, "hunts_spec.json"));
writeFileSync(out, `${JSON.stringify(spec, null, 1)}\n`);
console.log(`wrote ${out}: ${ais.length} AIs, ${jutsuSpec.length} jutsu entries; new beyond library: ${newBeyondLibrary.length}; library records used: ${libraryUsed.length}`);
for (const a of ais) console.log(`  ${a.username.padEnd(18)} HP ${a.pools.maxHealth} rows ${a.effects.length} rules ${a.rules.length} jutsu ${a.jutsu.length} insertAi ${JSON.stringify(a.insertAiSchemaCheck).slice(0, 60)} badRules ${a.rules.filter((r) => r.aiRule !== "ok").length}`);
for (const j of jutsuSpec) if (!j.validator.endsWith("ok")) console.log(`  ! ${j.id}: ${j.validator}`);
void existsSync;
void readFileSync;
