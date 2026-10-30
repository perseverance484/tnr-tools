/**
 * Rule audit for one enemy: at every decision the AI makes, why each authored rule did or did not fire.
 *   TNR_SCRIPT=audit_rules.ts run.sh --override overrides/kits_endgame.json --floor 4 --enemy "The Captain"
 *       [--runs 20] [--variant average] [--pets] [--phase-hp 50] [--together "Steady the Helm|Raise the Gunwale|Omen:"]
 *       [--out results/audit_captain.json]
 *
 * Read-only: the hook (runFloor onAiDecision) inspects a clone of the battle just before performAIaction, so outcomes
 * are those of the ordinary run. Per decision and rule:
 *   fired      the rule that produced the action (engine rule probe);
 *   preempted  below the fired rule, and its jutsu was usable (off cooldown, affordable) with conditions met;
 *   condition  its conditions were false (distance by hex distance: an approximation of the engine's path length);
 *   cooldown   its jutsu was on its own cooldown;   locked: held by a shared-cooldown (GCD) lock from another jutsu;
 *   ap         not enough action points left this turn;
 *   engine     above the fired rule, conditions met and usable here, but the engine rejected it (no target / range /
 *              validation), or the distance approximation disagreed.
 * Each wave appearance counts once per rule (any decision that fired it).
 */
import { mkdirSync, writeFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { actionPointsAfterAction, availableUserActions, stillInBattle } from "@/libs/combat/actions";
import { areBattleAllies } from "@/libs/combat/participants";
import { buildTemplates, enemyQueryUser, loadDmgConfig, loadJson, petFor, PLAYER_VARIANTS, playerQueryUser } from "./model";
import { assembleFloor, mulberry32, runFloor, seedEntropy } from "./sim";

const args = process.argv.slice(2);
const opt = (k: string) => (args.includes(`--${k}`) ? args[args.indexOf(`--${k}`) + 1] : undefined);
const H = process.env.TNR_HARNESS!;
const ov = loadJson(resolve(opt("override")!));
const floorIdx = Number(opt("floor") ?? 4);
const enemyName = opt("enemy") ?? "The Captain";
const runs = Number(opt("runs") ?? 20);
const variant = opt("variant") ?? "average";
const pets = args.includes("--pets");
const t = buildTemplates(loadJson(join(H, "data/baseline.json")), ov);
const v = { ...PLAYER_VARIANTS[variant]!, ...(ov.players?.[variant] ?? {}) };
const donor = t.enemies["texZaFi42S3EvJZBwQ8cd"]!.row;
const rows = Object.fromEntries(Object.entries(t.enemies).map(([id, e]) => [id, enemyQueryUser(e)]));
const dmg = loadDmgConfig(H, "live");

type Tally = Record<string, number>;
const reasons = ["fired", "preempted", "condition", "cooldown", "locked", "ap", "engine"] as const;
let rules: any[] = [];
const perRule: Tally[] = [];
const appearancesFired: number[] = [];
let decisions = 0;
let appearances = 0;
const roundsInWave: number[] = [];
// Phases: --phase-hp N splits each appearance at the first decision below N% health (phase 1 above, phase 2 below).
const phaseHp = Number(opt("phase-hp") ?? 50);
const phase1Rounds: number[] = [];
const phase2Rounds: number[] = [];
let reachedPhase2 = 0;
let killed = 0;
const phase2RoundsKilled: number[] = [];
// Per appearance: seed, phase lengths, his health % at his first decision below the split, killed or not.
const perAppearance: { seed: number; phase1: number; phase2: number | null; hpAtFirstPhase2Decision: number | null; killed: boolean }[] = [];
const firedByPhase: { p1: number; p2: number }[] = [];
// Every action the enemy took, by name, split by phase (e.g. to show that no set piece is cast in phase 1).
const actionsByPhase: { p1: Record<string, number>; p2: Record<string, number> } = { p1: {}, p2: {} };
// --together "a|b|c": rule-note substrings that should fire in one turn (e.g. a phase transition). Per appearance, the
// round each group first fires (a group = every rule whose note contains the substring); reported as how often all
// groups fired, and how often they did so in the same round.
const together = (opt("together") ?? "").split("|").filter(Boolean);
const togetherStats = { appearances: 0, allFired: 0, sameRound: 0, rounds: [] as (number | null)[][] };

const hpPct = (u: any) => (u.curHealth / u.maxHealth) * 100;
for (let s = 1; s <= runs; s++) {
  const rand = mulberry32(s);
  seedEntropy(s);
  Math.random = rand;
  const players = [0, 1, 2].map((i) => playerQueryUser(i, v, donor, t.jutsu));
  const ps = pets ? players.map((p) => petFor(p)) : undefined;
  if (ps) players.forEach((p, i) => (p.activePetId = ps[i]!.id));
  const b0 = await assembleFloor({ players, enemyRows: rows, floor: t.floors[floorIdx]!, rand, initialBarriers: true, dmgConfig: dmg.config, pets: ps });
  const pending: { uid: string; per: string[]; phase: 1 | 2 }[] = [];
  const crossed = new Map<string, number>();
  const crossHp = new Map<string, number>();
  const firedThisRun = new Map<string, Set<number>>();
  const firstRound = new Map<string, Map<number, number>>();
  const r = runFloor(b0, {
    playerIds: players.map((p) => p.userId), maxRounds: 150, dodge: true,
    onAiDecision: (b, uid, grid) => {
      const u: any = b.usersState.find((x) => x.userId === uid);
      if (!u || u.username !== enemyName) return;
      const prof: any = (b.extraState.aiProfiles as any)[u.aiProfileId];
      if (!prof) return;
      if (!rules.length) rules = prof.rules;
      const c = structuredClone(b);
      const me: any = c.usersState.find((x) => x.userId === uid);
      const avail = new Set(availableUserActions(c as never, uid, true, true).map((a: any) => a.id));
      const hexes = grid.toArray();
      const at = (x: any) => hexes.find((h: any) => h.col === x.longitude && h.row === x.latitude);
      const here = at(me);
      const live = c.usersState.filter((x: any) => stillInBattle(x, c.usersEffects));
      const foes = live.filter((x: any) => !areBattleAllies(x, me));
      const players = foes.filter((x: any) => !x.isAi && !x.isSummon);
      const dist = (x: any) => (here && at(x) ? grid.distance(here, at(x)) : 99);
      const pick = (target: string): any[] => {
        if (target === "SELF") return [me];
        if (target === "CLOSEST_OPPONENT") return foes.length ? [foes.reduce((a: any, b2: any) => (dist(b2) < dist(a) ? b2 : a))] : [];
        if (target === "HIGHEST_ENMITY_OPPONENT") return foes.length ? [foes.reduce((a: any, b2: any) => ((b2.enmity ?? 0) > (a.enmity ?? 0) ? b2 : a))] : [];
        if (target === "RANDOM_OPPONENT") return foes; // any of them (no random draw in a read-only hook)
        return foes;
      };
      const effOn = (x: any, type: string) => c.usersEffects.filter((e: any) => e.targetId === x.userId && e.type === type).reduce((n: number, e: any) => n + (e.power ?? 0), 0);
      const condOk = (cd: any) => {
        switch (cd.type) {
          case "health_below": return hpPct(me) < cd.value;
          case "distance_higher_than": return pick(cd.target).some((x) => dist(x) >= cd.value);
          case "distance_lower_than": return pick(cd.target).some((x) => dist(x) <= cd.value);
          case "player_within_range": return players.some((x: any) => dist(x) >= cd.minRange && dist(x) <= cd.maxRange);
          case "round_greater_than": return c.round > cd.value;
          case "round_lower_than": return c.round < cd.value;
          case "has_effect": return effOn(me, cd.effectType) >= cd.threshold;
          case "target_has_effect": return cd.threshold === 0 || pick(cd.target).some((x) => effOn(x, cd.effectType) >= cd.threshold);
          default: return true;
        }
      };
      const per = prof.rules.map((rule: any) => {
        if (!rule.conditions.every(condOk)) return "condition";
        const id = rule.action.jutsuId;
        if (!id) return "ok";
        if (!avail.has(id)) {
          const uj = me.jutsus.find((j: any) => j.jutsuId === id);
          const base = (c as any).jutsus?.find?.((j: any) => j.id === id)?.cooldown ?? uj?.jutsu?.cooldown;
          return uj && uj.originalCooldown === 3 && base !== 3 ? "locked" : "cooldown";
        }
        const action: any = availableUserActions(c as never, uid, true, true).find((a: any) => a.id === id);
        if (action && !actionPointsAfterAction(me, c as never, action).canAct) return "ap";
        return "ok";
      });
      const phase = hpPct(me) < phaseHp ? 2 : 1;
      if (phase === 2 && !crossed.has(uid)) {
        crossed.set(uid, c.round);
        crossHp.set(uid, Math.round(hpPct(me)));
      }
      pending.push({ uid, per, phase });
    },
  });
  // Pair each decision with the step it produced (same order: one performAIaction per AI decision).
  const capSteps = r.steps.filter((st: any) => pending.some((p) => p.uid === st.actorUid));
  for (let i = 0; i < pending.length && i < capSteps.length; i++) {
    const fired = capSteps[i]!.ruleIndex ?? -1;
    decisions++;
    {
      const name = t.jutsu[capSteps[i]!.actionId]?.name ?? String(capSteps[i]!.actionId);
      const tally = actionsByPhase[pending[i]!.phase === 1 ? "p1" : "p2"];
      tally[name] = (tally[name] ?? 0) + 1;
    }
    pending[i]!.per.forEach((st: string, k: number) => {
      perRule[k] ??= Object.fromEntries(reasons.map((x) => [x, 0]));
      const reason = k === fired ? "fired" : st === "ok" ? (fired >= 0 && k > fired ? "preempted" : "engine") : st;
      perRule[k]![reason]!++;
      if (k === fired) {
        firedByPhase[k] ??= { p1: 0, p2: 0 };
        firedByPhase[k]![pending[i]!.phase === 1 ? "p1" : "p2"]++;
        const set = firedThisRun.get(pending[i]!.uid) ?? new Set<number>();
        set.add(k);
        firedThisRun.set(pending[i]!.uid, set);
        const fr = firstRound.get(pending[i]!.uid) ?? new Map<number, number>();
        if (!fr.has(k)) fr.set(k, capSteps[i]!.round);
        firstRound.set(pending[i]!.uid, fr);
      }
    });
  }
  for (const w of r.waves) for (const e of w.enemies) if (e.name === enemyName) {
    appearances++;
    // His fight ends when he dies, or when the battle ends (a wipe leaves the wave open: endRound null).
    const end = e.diedRound ?? w.endRound ?? r.rounds;
    roundsInWave.push(end - w.startRound + 1);
    if (e.diedRound !== null) killed++;
    const x = crossed.get(e.uid);
    if (x !== undefined) {
      reachedPhase2++;
      phase1Rounds.push(x - w.startRound);
      phase2Rounds.push(end - x + 1);
      if (e.diedRound !== null) phase2RoundsKilled.push(end - x + 1);
      perAppearance.push({ seed: s, phase1: x - w.startRound, phase2: end - x + 1, hpAtFirstPhase2Decision: crossHp.get(e.uid) ?? null, killed: e.diedRound !== null });
    } else {
      phase1Rounds.push(end - w.startRound + 1);
      perAppearance.push({ seed: s, phase1: end - w.startRound + 1, phase2: null, hpAtFirstPhase2Decision: null, killed: e.diedRound !== null });
    }
    for (const k of firedThisRun.get(e.uid) ?? []) appearancesFired[k] = (appearancesFired[k] ?? 0) + 1;
    if (together.length) {
      const fr = firstRound.get(e.uid) ?? new Map<number, number>();
      const groupRound = together.map((sub) => {
        const rs = rules.flatMap((rule: any, k: number) => (rule.action.description.includes(sub) && fr.has(k) ? [fr.get(k)!] : []));
        return rs.length ? Math.min(...rs) : null;
      });
      togetherStats.appearances++;
      togetherStats.rounds.push(groupRound);
      if (groupRound.every((x) => x !== null)) {
        togetherStats.allFired++;
        if (new Set(groupRound).size === 1) togetherStats.sameRound++;
      }
    }
  }
}
const table = rules.map((rule, k) => {
  const tally = perRule[k] ?? {};
  const main = reasons.filter((x) => x !== "fired").sort((a, b) => (tally[b] ?? 0) - (tally[a] ?? 0))[0];
  return { index: k, note: rule.action.description, jutsuId: rule.action.jutsuId ?? null, conditions: rule.conditions.map((c: any) => `${c.type} ${c.value ?? c.threshold ?? `${c.minRange}-${c.maxRange}`}${c.effectType ? ` ${c.effectType}` : ""}${c.target ? ` ${c.target}` : ""}`), firedInAppearancesPct: Math.round((100 * (appearancesFired[k] ?? 0)) / Math.max(1, appearances)), firedByPhase: firedByPhase[k] ?? { p1: 0, p2: 0 }, decisions: tally, mainReasonNotFired: main };
});
const med = (xs: number[]) => {
  const q = [...xs].sort((a, b) => a - b);
  return q.length ? q[Math.floor(q.length / 2)]! : null;
};
const p90 = (xs: number[]) => {
  const q = [...xs].sort((a, b) => a - b);
  return q.length ? q[Math.min(q.length - 1, Math.ceil(0.9 * q.length) - 1)]! : null;
};
const sorted = [...roundsInWave].sort((a, b) => a - b);
const phases = { phaseHp, reachedPhase2Pct: Math.round((100 * reachedPhase2) / Math.max(1, appearances)), phase1RoundsMedian: med(phase1Rounds), phase2RoundsMedian: med(phase2Rounds), phase2RoundsMedianKilled: med(phase2RoundsKilled), phase1RoundsP90: p90(phase1Rounds), phase2RoundsP90: p90(phase2Rounds), hpAtFirstPhase2DecisionMedian: med(perAppearance.flatMap((a) => (a.hpAtFirstPhase2Decision === null ? [] : [a.hpAtFirstPhase2Decision]))), killedPct: Math.round((100 * killed) / Math.max(1, appearances)), phase1Range: [Math.min(...phase1Rounds), Math.max(...phase1Rounds)], phase2Range: phase2Rounds.length ? [Math.min(...phase2Rounds), Math.max(...phase2Rounds)] : null };
const togetherOut = together.length
  ? { groups: together, allFiredPct: Math.round((100 * togetherStats.allFired) / Math.max(1, togetherStats.appearances)), sameRoundOfAllFiredPct: Math.round((100 * togetherStats.sameRound) / Math.max(1, togetherStats.allFired)), firstRoundsPerAppearance: togetherStats.rounds }
  : undefined;
const out = { generatedBy: "engine/audit_rules.ts", override: opt("override"), floor: floorIdx, enemy: enemyName, runs, variant, pets, appearances, decisions, roundsInWaveMedian: sorted[Math.floor(sorted.length / 2)] ?? null, phases, together: togetherOut, actionsByPhase, perAppearance, rules: table };
console.log(`${enemyName}: ${appearances} appearances, ${decisions} decisions, wave rounds median ${out.roundsInWaveMedian}; phases ${JSON.stringify(phases)}`);
console.log(`actions by phase ${JSON.stringify(actionsByPhase)}`);
if (togetherOut) console.log(`together ${JSON.stringify(together)}: all fired in ${togetherOut.allFiredPct}% of appearances; same round in ${togetherOut.sameRoundOfAllFiredPct}% of those`);
for (const x of table) console.log(`${String(x.index).padStart(2)} ${x.note.slice(0, 58).padEnd(58)} fired ${String(x.firedInAppearancesPct).padStart(3)}% (p1 ${x.firedByPhase.p1}, p2 ${x.firedByPhase.p2})  ${reasons.map((rr) => `${rr}:${x.decisions[rr] ?? 0}`).join(" ")}`);
const outPath = opt("out");
if (outPath) {
  mkdirSync(dirname(resolve(outPath)), { recursive: true });
  writeFileSync(resolve(outPath), `${JSON.stringify(out, null, 1)}\n`);
}
