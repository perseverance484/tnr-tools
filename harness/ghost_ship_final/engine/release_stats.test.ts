/**
 * STATS: release combat stats through the pinned server and battle code (RUL-2026-10-12-012).
 *
 * For every AI push/90 writes, the push/90 payload is merged exactly as Forge does
 * (forge/src/runner/recipes.mjs mergeAi over the live push/86 row), then saved exactly as the
 * server does at 585534d7 (profile.updateAi):
 *   insertAiSchema.parse -> setEmptyStringsToNulls -> drop jutsus/items -> {...stored, ...data}
 *   -> scaleEditedAi(stored, edited)
 * The stored read-back is that edited row. Then the battle paths at combat.ts:2469-2487 run: an
 * unscaled fight (capUserStats at rank) and a quest fight scaled to a level-100 opponent
 * (user.level = 100; scaleUserStats(user, "ai"); capUserStats). Every engine function is imported
 * from the pinned source; nothing is reimplemented.
 *
 * Covered:
 *   - the 9 included existing AIs: every save push/90 performs (law-60 unequip, then the final edit),
 *     then a repeated identical save (operator re-run or an editor save with no change);
 *   - Sealwright: profile.create's placeholder row (userData defaults, level 100) then one full-create
 *     update from push/90, then a repeated save;
 *   - the two hazards: their saves change no stat or multiplier;
 *   - boss effects: insertAiSchema's effects parse of every asserted effects array is its own fixed
 *     point (canonical; nothing stripped, added or transformed).
 */
import { afterAll, describe, expect, it } from "bun:test";
import { readFileSync } from "node:fs";
import { join } from "node:path";
import { insertAiSchema, userData } from "@/drizzle/schema";
import { scaleEditedAi } from "@/server/api/routers/profile";
import { capUserStats, scaleUserStats } from "@/libs/profile";
import { CombatStatNames, MasteryNames, getUserCaps } from "@/drizzle/constants";
import { setEmptyStringsToNulls } from "@/server/utils/emptyStrings";
import { Evidence, requireClean } from "./lib/report";

const REPO = process.env.TNR_REPO ?? "";
if (!REPO) throw new Error("TNR_REPO must point at the tnr-tools checkout");
const rd = (rel: string) => JSON.parse(readFileSync(join(REPO, rel), "utf8"));
const E = new Evidence("STATS");
afterAll(() => E.flush({ scope: "pinned-server save path and battle scaling/clamping for every AI push/90 writes; FakeGame-free, DB-free" }));

const MANIFEST = rd("push/90_ghost_ship_skyglass_release.json");
const P86 = rd("harvests/inbox/tnr_results_1791727613862.json").captures.filter((c: any) => c.proc === "profile.getAi").map((c: any) => c.data);
const LIVE = new Map<string, any>(P86.map((d: any) => [d.userId, d]));
const CAPPED = ["texZaFi42S3EvJZBwQ8cd", "AQi-bHJ-5tHXtxrnc0P9E", "0PZU_FvlbM3ErYGlD5r56", "v7T9_XdGMfP46em0dPuBc", "2OXJEXoktxJcjqMkE851g",
  "3V_gdHYaclMB1gTyOPAbV", "d6g0mOM7RBSsYI1hrUVT9", "QY69h271Nx9uHrBeR6jwW", "fDU9jCPZtH7YHbdQPO9RF"];
const HAZARDS: Record<string, number> = { "wTgO-Q32caSSd0is1QIS7": 10, "frc9LTxqQlM7mncG4VZGK": 20 };
const CAPS = getUserCaps("JONIN");
const REQUIRED = { offence: 1_300_000, defence: 1_300_000, strength: 400_000, intelligence: 400_000, willpower: 400_000, speed: 400_000 };

const DATE_COLS = new Set(Object.entries((userData as any)).filter(([, c]: any) => c?.columnType === "MySqlTimestamp" || c?.dataType === "date").map(([k]) => k));
/** JSON capture -> the shape superjson hands the server (Date objects for timestamp columns). */
const revive = (row: any) => { const o = structuredClone(row); for (const k of Object.keys(o)) if (DATE_COLS.has(k) && typeof o[k] === "string") o[k] = new Date(o[k]); return o; };

let mergeAi: (live: any, data: any) => any;
const forge = import(join(REPO, "forge/src/runner/recipes.mjs")).then((m) => { mergeAi = m.mergeAi; });

/** profile.updateAi at 585534d7, minus DB I/O: returns the stored row after the save. */
function serverSave(stored: any, manifestData: any) {
  const payload = mergeAi(structuredClone(stored), structuredClone(manifestData)); // what Forge sends
  const parsed: any = insertAiSchema.parse(revive(payload));
  setEmptyStringsToNulls(parsed, userData);
  parsed.customTitle = parsed.customTitle ?? "";
  delete parsed.jutsus; delete parsed.items;
  const edited: any = { ...stored, ...parsed };
  scaleEditedAi(stored, edited);
  return edited;
}
const pick = (u: any, keys: readonly string[]) => Object.fromEntries(keys.map((k) => [k, u[k]]));
function battle(stored: any, scaleToLevel: number | null) {
  const u: any = structuredClone(stored);
  if (scaleToLevel !== null) { u.level = scaleToLevel; scaleUserStats(u, "ai"); } // combat.ts:2469-2472
  capUserStats(u, u.rank); // combat.ts:2487
  return pick(u, CombatStatNames);
}
const atCaps = (s: any) => Object.entries(REQUIRED).every(([k, v]) => s[k] === v);
const itemsFor = (target: string) => MANIFEST.items.filter((it: any) => it.entity === "ai" && it.targetId === target)
  .sort((a: any, b: any) => (a.phase ?? 5) - (b.phase ?? 5));

describe("STATS — pinned-server save path, repeated saves, battle scaling and clamping", () => {
  it("required caps are the pinned JONIN caps", async () => {
    await forge;
    E.check("JONIN stats_cap 1,300,000 and gens_cap 400,000 at 585534d7", CAPS.stats_cap === 1_300_000 && CAPS.gens_cap === 400_000, CAPS);
  });

  it("nine included existing AIs reach the caps in every fight, across all push/90 saves and a repeated save", async () => {
    await forge;
    const rows: Record<string, unknown> = {};
    for (const uid of CAPPED) {
      const before = LIVE.get(uid);
      const saves = itemsFor(uid);
      let stored = revive(before);
      for (const it of saves) stored = serverSave(stored, it.data);
      const afterRelease = structuredClone(stored);
      const resaved = serverSave(stored, saves[saves.length - 1].data); // identical re-save
      const unscaled = battle(afterRelease, null), quest100 = battle(afterRelease, 100), resavedQuest = battle(resaved, 100);
      const name = saves[saves.length - 1].data.username;
      rows[name] = {
        saves: saves.length, multiplier: [before.statsMultiplier, afterRelease.statsMultiplier],
        storedBefore: pick(before, CombatStatNames), storedAfter: pick(afterRelease, CombatStatNames),
        unscaledFight: unscaled, questFightLevel100: quest100,
      };
      E.check(`${name}: statsMultiplier ${before.statsMultiplier} -> 5 stored`, afterRelease.statsMultiplier === 5, afterRelease.statsMultiplier);
      E.check(`${name}: stored combat stats reach or exceed the caps`, CombatStatNames.every((k) => afterRelease[k] >= (k === "offence" || k === "defence" ? CAPS.stats_cap : CAPS.gens_cap)), pick(afterRelease, CombatStatNames));
      E.check(`${name}: unscaled fight enters at exactly the caps`, atCaps(unscaled), unscaled);
      E.check(`${name}: quest fight scaled to a level-100 opponent enters at exactly the caps`, atCaps(quest100), quest100);
      E.check(`${name}: a repeated save is a fixed point (stats, masteries, pools, experience)`,
        JSON.stringify(pick(resaved, [...CombatStatNames, ...MasteryNames, "maxHealth", "maxChakra", "maxStamina", "experience", "statsMultiplier"]))
          === JSON.stringify(pick(afterRelease, [...CombatStatNames, ...MasteryNames, "maxHealth", "maxChakra", "maxStamina", "experience", "statsMultiplier"])) && atCaps(resavedQuest),
        { afterRelease: pick(afterRelease, CombatStatNames), resaved: pick(resaved, CombatStatNames) });
      E.check(`${name}: level, rank, pools, regeneration and masteries preserved`,
        JSON.stringify(pick(afterRelease, ["level", "rank", "poolsMultiplier", "maxHealth", "maxChakra", "maxStamina", "regeneration", ...MasteryNames]))
          === JSON.stringify(pick(before, ["level", "rank", "poolsMultiplier", "maxHealth", "maxChakra", "maxStamina", "regeneration", ...MasteryNames])),
        { before: pick(before, [...MasteryNames, "maxHealth"]), after: pick(afterRelease, [...MasteryNames, "maxHealth"]) });
    }
    E.put("includedExisting", rows);
  });

  it("Sealwright: one full create reaches the caps; a repeated save is stable", async () => {
    await forge;
    const create = MANIFEST.items.find((it: any) => it.entity === "ai" && it.slot === "create" && it.srcId === "sealwright");
    // profile.create (profile.ts:1390): userData defaults with username/gender/avatar/level 100/isAi.
    const placeholder: any = { ...structuredClone(LIVE.get("QY69h271Nx9uHrBeR6jwW")), userId: "sealwright", username: "New AI - sealwright",
      experience: 0, statsMultiplier: 1, poolsMultiplier: 1, regeneration: 60, rank: "STUDENT", level: 100, effects: [], jutsus: [], items: [],
      curHealth: 100, maxHealth: 100, curChakra: 100, maxChakra: 100, curStamina: 100, maxStamina: 100,
      ...Object.fromEntries([...CombatStatNames, ...MasteryNames].map((k) => [k, 10])) };
    const stored = serverSave(revive(placeholder), create.data);
    const resaved = serverSave(stored, create.data);
    const unscaled = battle(stored, null), quest100 = battle(stored, 100);
    const captain = LIVE.get("QY69h271Nx9uHrBeR6jwW");
    E.put("sealwright", { sent: pick(create.data, [...CombatStatNames, "statsMultiplier"]), stored: pick(stored, [...CombatStatNames, ...MasteryNames, "experience", "maxHealth"]), unscaledFight: unscaled, questFightLevel100: quest100 });
    E.check("Sealwright: create sends all six combat fields together at 1,391,300 with statsMultiplier 5 and no preferredStat",
      CombatStatNames.every((k) => create.data[k] === 1_391_300) && create.data.statsMultiplier === 5 && !("preferredStat" in create.data), pick(create.data, [...CombatStatNames, "statsMultiplier"]));
    E.check("Sealwright: stored read-back equals the sent 1,391,300 in every combat stat", CombatStatNames.every((k) => stored[k] === 1_391_300), pick(stored, CombatStatNames));
    E.check("Sealwright: unscaled and level-100 quest fights enter at exactly the caps", atCaps(unscaled) && atCaps(quest100), { unscaled, quest100 });
    E.check("Sealwright: masteries, pools and regeneration equal the regular Captain's",
      JSON.stringify(pick(stored, [...MasteryNames, "maxHealth", "maxChakra", "maxStamina", "regeneration", "level", "rank", "poolsMultiplier"]))
        === JSON.stringify(pick(captain, [...MasteryNames, "maxHealth", "maxChakra", "maxStamina", "regeneration", "level", "rank", "poolsMultiplier"])),
      { stored: pick(stored, [...MasteryNames, "maxHealth"]), captain: pick(captain, [...MasteryNames, "maxHealth"]) });
    E.check("Sealwright: a repeated save is a fixed point", JSON.stringify(pick(resaved, [...CombatStatNames, ...MasteryNames, "experience"])) === JSON.stringify(pick(stored, [...CombatStatNames, ...MasteryNames, "experience"])), pick(resaved, CombatStatNames));
    // The superseded two-stage path, as a control: create without the combat fields, then edit them.
    const partial = Object.fromEntries(Object.entries(create.data).filter(([k]) => !CombatStatNames.includes(k as any)));
    const stage1 = serverSave(revive(placeholder), { ...partial, strength: 834780, intelligence: 834780, willpower: 834780, speed: 834780, statsMultiplier: 3 });
    E.put("twoStageControl", { afterIncompleteCreate: pick(stage1, CombatStatNames) });
    E.check("control: an incomplete-stat create leaves offence/defence far below the caps (why the full create is required)", stage1.offence < CAPS.stats_cap && stage1.defence < CAPS.stats_cap, pick(stage1, CombatStatNames));
  });

  it("hazards: no stat or multiplier change from any push/90 save", async () => {
    await forge;
    for (const [uid, mult] of Object.entries(HAZARDS)) {
      const before = LIVE.get(uid);
      let stored = revive(before);
      const saves = itemsFor(uid);
      for (const it of saves) stored = serverSave(stored, it.data);
      const name = saves[saves.length - 1].data.username;
      E.put(`hazard ${name}`, { saves: saves.length, multiplier: stored.statsMultiplier, stored: pick(stored, CombatStatNames) });
      E.check(`${name}: no save asserts statsMultiplier or a combat stat`, saves.every((it: any) => !("statsMultiplier" in it.data) && CombatStatNames.every((k) => !(k in it.data))));
      E.check(`${name}: statsMultiplier stays ${mult} and stored combat stats are unchanged`, stored.statsMultiplier === mult
        && JSON.stringify(pick(stored, [...CombatStatNames, ...MasteryNames])) === JSON.stringify(pick(before, [...CombatStatNames, ...MasteryNames])), pick(stored, CombatStatNames));
    }
  });

  it("boss and Sealwright effects are canonical: the server's effects parse is a fixed point", async () => {
    await forge;
    const out: Record<string, unknown> = {};
    for (const it of MANIFEST.items.filter((x: any) => x.entity === "ai" && Array.isArray(x.data.effects))) {
      const parsed = (insertAiSchema as any).shape.effects.parse(structuredClone(it.data.effects));
      const same = JSON.stringify(parsed.map((e: any) => Object.fromEntries(Object.keys(e).sort().map((k) => [k, e[k]]))))
        === JSON.stringify(it.data.effects.map((e: any) => Object.fromEntries(Object.keys(e).sort().map((k) => [k, e[k]]))));
      out[it.data.username] = it.data.effects.map((e: any) => [e.type, e.power, e.rounds]);
      E.check(`${it.data.username}: asserted effects survive insertAiSchema.effects unchanged`, same, { sent: it.data.effects, parsed });
    }
    E.put("effects", out);
  });
});

requireClean(E);
