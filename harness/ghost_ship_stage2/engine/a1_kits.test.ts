/**
 * Gate A1: actual AI/action tests for all eleven accepted Ghost Ship kits.
 *
 * Variants per AI (kit change and rule change kept separate):
 *   captured   captured kit + captured profile          (October 1 baseline)
 *   kitOnly    accepted kit + captured profile, unchanged (isolates the kit change)
 *   candidate  accepted kit + captured profile with jutsu IDs remapped through the
 *              accepted mapping (a RULE-CHANGE PROPOSAL, ledgered separately)
 * Every AI keeps its captured numeric profile, innate effects and item rows
 * (asserted after real battle assembly). Each variant runs:
 *   - cadence vs a passive dummy (auto-combat, no rules → waits) at hex distance 3
 *     and 7 for 20 rounds: actions, AP use, cooldown gaps, idles, exhaustion;
 *   - representative fights vs three player fixtures × 3 seeds.
 * Hazards (Seal Charge >2, Core Canister >6) and Crowned Captain dormant support
 * are asserted explicitly. A Crowned support rotation is run only as a labelled,
 * unapproved proposal.
 */
import { afterAll, describe, expect, it } from "bun:test";
import { availableUserActions } from "@/libs/combat/actions";
import { calcPoolCost } from "@/libs/combat/util";
import { getUserCaps, MAX_MASTERY_CAP } from "@/drizzle/constants";
import * as F from "./lib/fixtures";
import * as S from "./lib/sim";
import { Evidence, requireClean } from "./lib/report";

const A1 = new Evidence("A1");
afterAll(() => A1.flush({ dmgConfig: "engine source defaults (battle.extraState.dmgConfig unset; live game settings not read)", migration: F.MIGRATION_0056, battleStart: "initiateBattle preprocessing: capUserStats at own rank (QUEST, scaleTarget false), applyPoolAdjustmentsToBase, refreshMasteries" }));

type Variant = "captured" | "kitOnly" | "candidate";
const VARIANTS: Variant[] = ["captured", "kitOnly", "candidate"];
const ROUNDS = 20;
const DUMMY = "dummy_cadence"; // no "user_" prefix → engine adds no backup rules; auto-combat → waits

const profileFor = (e: any, v: Variant) => (v === "candidate" ? F.remappedRules(e).profile : F.capturedRules(e));
const bossFor = (e: any, v: Variant) => F.aiQueryUser(e, v === "captured" ? "captured" : "accepted", profileFor(e, v));

const dummy = (hp = 10_000_000) => {
  const pol = { id: "policy::dummy", userId: DUMMY, includeDefaultRules: false, rules: [] };
  const u = F.playerQueryUser(DUMMY, "upstream-helper", "striker", pol, S.joninCaps());
  u.jutsus = [];
  u.curHealth = hp;
  u.maxHealth = hp;
  return u;
};

const summariseCadence = (r: S.FightResult, bossCid: string, kitById: Record<string, any>) => {
  const mine = r.log.filter((l) => l.actor === bossCid);
  const uses: Record<string, number[]> = {};
  const perRound: Record<number, { ap: number; actions: string[] }> = {};
  for (const l of mine) {
    const name = l.actionName ?? "(none)";
    (uses[name] ??= []).push(l.round);
    const pr = (perRound[l.round] ??= { ap: 0, actions: [] });
    pr.ap += Math.max(0, l.apBefore - l.apAfter);
    pr.actions.push(name);
  }
  const gaps: Record<string, { cooldown: number | null; minGap: number | null; uses: number }> = {};
  for (const [name, rounds] of Object.entries(uses)) {
    const rec = Object.values(kitById).find((j: any) => j.name === name);
    const g = rounds.slice(1).map((x, i) => x - rounds[i]!).filter((x) => x > 0);
    gaps[name] = { cooldown: rec ? rec.cooldown : null, minGap: g.length ? Math.min(...g) : null, uses: rounds.length };
  }
  const cooldownViolations = Object.entries(gaps).filter(([, g]) => g.cooldown && g.minGap !== null && g.minGap < g.cooldown);
  const dmgToDummy = r.log.filter((l) => l.actor === bossCid).reduce((s, l) => s - Math.min(0, l.hpDelta[DUMMY] ?? 0), 0);
  const roundsActive = Object.values(perRound);
  return {
    actionsByName: Object.fromEntries(Object.entries(uses).map(([k, v]) => [k, v.length])),
    cooldownGaps: gaps,
    cooldownViolations: cooldownViolations.map(([k]) => k),
    waits: (uses.wait ?? []).length,
    moves: (uses.move ?? []).length,
    basicAttacks: (uses.basicAttack ?? []).length,
    idleTimeouts: r.idleTimeouts[bossCid] ?? 0,
    exhausted: r.bossExhausted,
    meanApPerRound: roundsActive.length ? roundsActive.reduce((s, x) => s + x.ap, 0) / roundsActive.length : 0,
    measuredRounds: r.measuredRounds,
    dummySurvived: (r.final[DUMMY]?.curHealth ?? 0) > 0,
    damageToDummyPerRound: dmgToDummy / Math.max(1, r.measuredRounds),
    firstRounds: Object.entries(perRound).slice(0, 6).map(([k, v]) => `${k}: ${v.actions.join(" + ")}`),
    bossFinal: r.final[bossCid],
  };
};

const kitRecords = (e: any, v: Variant) => {
  const u = bossFor(e, v);
  return Object.fromEntries(u.jutsus.map((uj: any) => [uj.jutsuId, uj.jutsu]));
};

describe("A1 — assembly, profile preservation and availability", () => {
  for (const e of F.entities()) {
    it(`${e.name}: accepted kit assembles with captured numeric profile, innate effects and items`, async () => {
      const cap = await S.assembleBattle({ users: [dummy(), bossFor(e, "captured")], placements: [{ userId: DUMMY, x: 3, y: 4 }, { userId: e.aiId, x: 6, y: 4 }], autoCombatUserIds: [DUMMY] });
      const acc = await S.assembleBattle({ users: [dummy(), bossFor(e, "candidate")], placements: [{ userId: DUMMY, x: 3, y: 4 }, { userId: e.aiId, x: 6, y: 4 }], autoCombatUserIds: [DUMMY] });
      const bu = (b: any) => b.usersState.find((u: any) => u.controllerId === e.aiId);
      const c = bu(cap);
      const a = bu(acc);
      // Battle-start caps (initiateBattle → capUserStats at the AI's own rank).
      const raw = bossFor(e, "captured");
      const { stats_cap, gens_cap } = getUserCaps(raw.rank);
      const capOf = (f: string) => (["offence", "defence"].includes(f) ? stats_cap : f.endsWith("Mastery") ? MAX_MASTERY_CAP : gens_cap);
      const capFields = ["offence", "defence", "strength", "intelligence", "willpower", "speed", "ninjutsuMastery", "genjutsuMastery", "taijutsuMastery", "bukijutsuMastery"];
      const capped = Object.fromEntries(capFields.map((f) => [f, { stored: raw[f], cap: capOf(f), battle: c[f], expected: Math.min(raw[f], capOf(f)) }]));
      const capMismatch = capFields.filter((f) => c[f] !== Math.min(raw[f], capOf(f)) || a[f] !== c[f]);
      const fields = ["level", "rank", "statsMultiplier", "poolsMultiplier", "regeneration", "maxHealth", "maxChakra", "maxStamina", "offence", "defence", "strength", "intelligence", "willpower", "speed", "highestGenerals", "primaryElement", "secondaryElement"];
      const diffs = fields.filter((f) => JSON.stringify(c[f]) !== JSON.stringify(a[f]));
      const innate = (b: any) => b.usersEffects.filter((x: any) => x.targetId === bu(b).userId && x.fromType === "bloodline").map((x: any) => `${x.type}:${x.power}/${x.rounds}`);
      const kitIds = e.proposedKit.map((m: string) => F.resolveMember(m).record.id);
      const assembled = a.jutsus.map((j: any) => j.jutsuId);
      const items = a.items.map((i: any) => `${i.itemId}:${i.equipped}:${i.dropChancePerc}`);
      const actions = availableUserActions(acc as any, a.userId, true, true).filter((x) => x.type === "jutsu");
      const affordable = actions.map((x) => ({ id: x.id, name: x.name, ap: x.actionCostPerc, cooldown: x.cooldown, range: x.range, cost: calcPoolCost(x, acc.usersEffects, a) }));
      A1.put(`assembly:${e.name}`, {
        acceptedKit: e.proposedKit, assembledJutsuIds: assembled, numericDiffsCapturedVsAccepted: diffs,
        innateCaptured: innate(cap), innateAccepted: innate(acc), items, round1JutsuActions: affordable,
        migratedStats: { offence: a.offence, defence: a.defence },
        rank: raw.rank, battleStartCaps: capped, exceedsCaps: capFields.filter((f) => raw[f] > capOf(f)),
      });
      expect(capMismatch).toEqual([]);
      A1.check(`${e.name}: battle-start stats = min(stored 0056-converted value, ${raw.rank} cap) for offence/defence/generals/masteries`, capMismatch.length === 0, capped);
      expect(assembled).toEqual(kitIds);
      expect(diffs).toEqual([]);
      expect(innate(acc)).toEqual(innate(cap));
      A1.check(`${e.name}: assembled membership = accepted kit (${kitIds.length})`, JSON.stringify(assembled) === JSON.stringify(kitIds));
      A1.check(`${e.name}: no numeric profile change between captured and accepted assembly`, diffs.length === 0, diffs);
      A1.check(`${e.name}: innate effects preserved (incl. duplicates)`, JSON.stringify(innate(acc)) === JSON.stringify(innate(cap)), innate(acc));
      A1.check(`${e.name}: every kit jutsu is an available action at round 1`, kitIds.every((id: string) => actions.some((x) => x.id === id)), { missing: kitIds.filter((id: string) => !actions.some((x) => x.id === id)) });
    });
  }
});

describe("A1 — cadence vs passive dummy (20 rounds, distance 3 and 7)", () => {
  for (const e of F.entities()) {
    if (e.name === "Seal Charge" || e.name === "Core Canister") continue;
    it(`${e.name}: captured vs kitOnly vs candidate`, async () => {
      const out: Record<string, any> = {};
      for (const v of VARIANTS) {
        for (const dist of [3, 7]) {
          const r = await S.withSeed(11, async () => {
            const b = await S.assembleBattle({ users: [dummy(), bossFor(e, v)], placements: [{ userId: DUMMY, x: 2, y: 4 }, { userId: e.aiId, x: 2 + dist, y: 4 }], autoCombatUserIds: [DUMMY] });
            return S.runFight(b, { playerIds: [DUMMY], bossIds: [e.aiId], maxRounds: ROUNDS, seed: 11 });
          });
          out[`${v}@d${dist}`] = summariseCadence(r, e.aiId, kitRecords(e, v));
        }
      }
      A1.put(`cadence:${e.name}`, out);
      for (const v of ["kitOnly", "candidate"] as const) {
        for (const d of [3, 7]) {
          const s = out[`${v}@d${d}`];
          A1.check(`${e.name} ${v}@d${d}: no AI-exhaustion give-up`, !s.exhausted, s.firstRounds);
          A1.check(`${e.name} ${v}@d${d}: no cooldown violation`, s.cooldownViolations.length === 0, s.cooldownGaps);
          A1.check(`${e.name} ${v}@d${d}: full ${ROUNDS}-round measurement interval (dummy survived)`, s.measuredRounds === ROUNDS && s.dummySurvived, { measuredRounds: s.measuredRounds, dummySurvived: s.dummySurvived });
        }
      }
      expect(out["candidate@d3"].exhausted).toBe(false);
    });
  }
});

describe("A1 — representative fights (player fixtures × seeds)", () => {
  const PLAYERS: [F.PlayerStatBand, keyof typeof F.PLAYER_KITS][] = [["jonin-cap", "buffer"], ["jonin-cap", "striker"], ["jonin-half", "moderate"]];
  const SEEDS = [1, 2, 3];
  for (const e of F.entities()) {
    it(`${e.name}: fights`, async () => {
      const out: Record<string, any> = {};
      for (const v of VARIANTS) {
        for (const [band, kitName] of PLAYERS) {
          const rows = [];
          for (const seed of SEEDS) {
            const r = await S.withSeed(seed, async () => {
              const pid = "user_p";
              const pol = F.playerPolicy(pid, kitName);
              const pl = F.playerQueryUser(pid, band, kitName, pol, S.joninCaps());
              const b = await S.assembleBattle({ users: [pl, bossFor(e, v)], placements: [{ userId: pid, x: 2, y: 4 }, { userId: e.aiId, x: 8, y: 4 }], autoCombatUserIds: [pid] });
              return S.runFight(b, { playerIds: [pid], bossIds: [e.aiId], maxRounds: 40, seed });
            });
            rows.push({ seed, winner: r.winner, rounds: r.rounds, exhausted: r.bossExhausted, bossHpLeftPct: r.final[e.aiId] ? r.final[e.aiId]!.curHealth / r.final[e.aiId]!.maxHealth : null, playerHpLeftPct: r.final.user_p ? r.final.user_p.curHealth / r.final.user_p.maxHealth : null });
          }
          out[`${v}|${band}/${kitName}`] = rows;
        }
      }
      A1.put(`fights:${e.name}`, out);
      const exhausted = Object.entries(out).filter(([k, rows]: any) => !k.startsWith("captured") && rows.some((x: any) => x.exhausted));
      A1.check(`${e.name}: no exhaustion give-up in accepted-kit fights`, exhausted.length === 0, exhausted.map(([k]) => k));
      expect(exhausted).toEqual([]);
    });
  }
});

describe("A1 — hazards keep ID, 100 AP self-destruct and delayed triggers", () => {
  for (const [name, trigger] of [["Seal Charge", 2], ["Core Canister", 6]] as const) {
    it(`${name}: waits until round > ${trigger}, then Core Rupture (ID nCQETf-HNnbRec1OSY2-R)`, async () => {
      const e = F.entityByName(name);
      const rec = F.legacyJutsu("nCQETf-HNnbRec1OSY2-R").record;
      const res: Record<string, any> = { record: { id: rec.id, actionCostPerc: rec.actionCostPerc, cooldown: rec.cooldown, range: rec.range, effects: rec.effects.map((x: any) => [x.type, x.power, x.rounds, x.target]) } };
      for (const v of VARIANTS) {
        for (const dist of [3, 8]) {
          const r = await S.withSeed(5, async () => {
            const b = await S.assembleBattle({ users: [dummy(), bossFor(e, v)], placements: [{ userId: DUMMY, x: 2, y: 4 }, { userId: e.aiId, x: 2 + dist, y: 4 }], autoCombatUserIds: [DUMMY] });
            return S.runFight(b, { playerIds: [DUMMY], bossIds: [e.aiId], maxRounds: 12, seed: 5 });
          });
          const mine = r.log.filter((l) => l.actor === e.aiId);
          const explosion = mine.find((l) => l.actionId === rec.id);
          res[`${v}@d${dist}`] = {
            actions: mine.map((l) => `${l.round}:${l.actionName ?? "(none)"}:${l.apBefore}->${l.apAfter}`),
            explosionRound: explosion?.round ?? null,
            apSpent: explosion ? explosion.apBefore - explosion.apAfter : null,
            selfAfter: r.final[e.aiId]?.curHealth ?? null,
            dummyDamage: explosion ? -(explosion.hpDelta[DUMMY] ?? 0) : 0,
            exhausted: r.bossExhausted,
            idleTimeouts: r.idleTimeouts[e.aiId] ?? 0,
          };
        }
      }
      A1.put(`hazard:${name}`, res);
      for (const v of VARIANTS) {
        const near = res[`${v}@d3`];
        const far = res[`${v}@d8`];
        A1.check(`${name} ${v}: Core Rupture first used in round ${trigger + 1} at range`, near.explosionRound === trigger + 1, near.actions);
        A1.check(`${name} ${v}: 100 AP spent and self-destructs (curHealth 0)`, near.apSpent === 100 && near.selfAfter === 0, near);
        A1.check(`${name} ${v}: waits safely before trigger (no exhaustion)`, !near.exhausted && near.actions.filter((a: string) => Number(a.split(":")[0]) <= trigger).every((a: string) => a.includes(":wait:")), near.actions);
        // Core Rupture is method ALL: the blast is not limited by its nominal range 5
        // (hexgrid ALL expands to the grid), so distance does not delay or prevent it.
        A1.check(`${name} ${v}: ALL-method blast also fires on trigger at d8 and reaches the opponent (no exhaustion)`, far.explosionRound === trigger + 1 && far.dummyDamage > 0 && !far.exhausted, { explosionRound: far.explosionRound, dummyDamage: far.dummyDamage });
        A1.check(`${name} ${v}: blast damages and stuns the opponent at d3`, near.dummyDamage > 0, near.dummyDamage);
      }
      expect(res["candidate@d3"].explosionRound).toBe(trigger + 1);
    });
  }
});

describe("A1 — Crowned Captain dormant support (Second Wind, Stolen Form, Rebounding Form)", () => {
  it("captured and candidate rules never select the equipped support moves; proposal reported separately", async () => {
    const e = F.entityByName("Crowned Captain");
    const support = { S35: F.poolJutsuByCode("S35").record, B07: F.poolJutsuByCode("B07").record, Rebounding: F.legacyJutsu("T3glZGcSd-jS8G-NB43GR").record };
    const supportIds = Object.values(support).map((r: any) => r.id);
    const proposal = (() => {
      const base = F.remappedRules(e).profile;
      const rules = [
        { conditions: [{ type: "health_below", value: 50, description: "" }], action: { type: "use_specific_jutsu", jutsuId: support.S35.id, target: "SELF", description: "" } },
        { conditions: [{ type: "target_has_effect", effectType: "increasedamagegiven", target: "CLOSEST_OPPONENT", threshold: 30, description: "" }, { type: "distance_lower_than", value: 5, target: "CLOSEST_OPPONENT", description: "" }], action: { type: "use_specific_jutsu", jutsuId: support.B07.id, target: "CLOSEST_OPPONENT", description: "" } },
        { conditions: [{ type: "distance_lower_than", value: 3, target: "CLOSEST_OPPONENT", description: "" }], action: { type: "use_specific_jutsu", jutsuId: support.Rebounding.id, target: "SELF", description: "" } },
        ...base.rules,
      ];
      return { ...base, id: `${base.id}::supportProposal`, rules };
    })();
    const profiles: Record<string, any> = { captured: F.capturedRules(e), candidate: F.remappedRules(e).profile, supportProposal_NOT_APPROVED: proposal };
    const out: Record<string, any> = {};
    for (const [label, prof] of Object.entries(profiles)) {
      const counts: Record<string, number> = {};
      const results: any[] = [];
      for (const [band, kitName] of [["jonin-cap", "buffer"], ["jonin-cap", "striker"]] as const) {
        for (const seed of [1, 2, 3, 4, 5]) {
          const r = await S.withSeed(seed, async () => {
            const pid = "user_p";
            const pl = F.playerQueryUser(pid, band, kitName, F.playerPolicy(pid, kitName), S.joninCaps());
            const boss = F.aiQueryUser(e, label === "captured" ? "captured" : "accepted", prof);
            const b = await S.assembleBattle({ users: [pl, boss], placements: [{ userId: pid, x: 2, y: 4 }, { userId: e.aiId, x: 8, y: 4 }], autoCombatUserIds: [pid] });
            return S.runFight(b, { playerIds: [pid], bossIds: [e.aiId], maxRounds: 40, seed });
          });
          for (const l of r.log.filter((x) => x.actor === e.aiId && x.actionId && supportIds.includes(x.actionId))) counts[l.actionName!] = (counts[l.actionName!] ?? 0) + 1;
          results.push({ kit: kitName, seed, winner: r.winner, rounds: r.rounds, bossHpLeftPct: r.final[e.aiId]!.curHealth / r.final[e.aiId]!.maxHealth });
        }
      }
      out[label] = { supportUses: counts, results };
    }
    A1.put("crownedSupport", { note: "supportProposal is NOT approved behaviour; evidence only for the director's activation decision", proposalRules: proposal.rules.slice(0, 3), ...out });
    A1.check("captured rules: equipped support never selected (dormant)", Object.keys(out.captured.supportUses).length === 0, out.captured.supportUses);
    A1.check("candidate remapped rules: equipped support stays dormant", Object.keys(out.candidate.supportUses).length === 0, out.candidate.supportUses);
    expect(Object.keys(out.candidate.supportUses)).toHaveLength(0);
  });
});

describe("A1 — rule-change ledger (candidate remap)", () => {
  it("lists every remapped reference per AI", () => {
    const ledger = Object.fromEntries(F.entities().map((e) => [e.name, F.remappedRules(e).changes]));
    A1.put("ruleChangeLedger", ledger);
    expect(ledger["The Captain"]).toEqual([]);
    A1.check("regular Captain needs no remap (all captured rule IDs retained)", ledger["The Captain"].length === 0);
  });
});

requireClean(A1);
