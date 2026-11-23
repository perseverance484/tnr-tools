/**
 * duel_sim: like fight_sim, but the opponent ("him") CHOOSES each round instead of following a script.
 * Each of his turns: every legal bundle of up to two actions that fits his AP (both orders, Cleanse/Clear included,
 * plain basic actions left out) is played on a copy of the fight, then scored by a two-round lookahead: the rest of
 * this round, my next scripted round, then his greedy best-damage reply. Score = HP he takes off me minus HP I take
 * off him over that window, with a large bonus for a kill. "forced" pins some of his actions on a round (the
 * condition being tested); he fills the rest of that round's AP by the same search. When my script runs out I
 * choose by the same search. Extra input: forced?: { [roundIndex]: [{a, at?}] }, maxRounds?: number.
 *
 * (original fight_sim header follows)
 * Scripted multi-round PvP fight on the pinned TNR engine (offline, in-process, sockets denied by offline_exec.py).
 * For checking a build's claims: both sides play a fixed script, round by round, with real AP (stun, time
 * dilation), real positions (moves move), real cooldowns, and every effect held by the engine itself.
 *
 * Input (argv[2], JSON):
 *   me / him: { id, x, y, level?, kit: [{ record, level, kind }], bloodline?, gearMods?, passives? }
 *   inject: [record]                         — injectable records (extraState.jutsus) for injectjutsus grants
 *   script: [{ order: ["me","him"], me: [{ a, at? }], him: [{ a, at? }] }]   — one entry per round
 *   seed?: number, keepAlive?: boolean   — refill both HP after every step (damage still logged per step)
 * Output: { rounds: [{ round, steps: [{ actor, a, name, ok, reason?, ap, cost, apLeft, stun, dmg, hp, lines,
 *           fxMe, fxHim }] }] }
 */
import { readFileSync } from "node:fs";
import * as F from "./lib/fixtures";
import * as S from "./lib/sim";
import * as I from "./lib/itembattle";
import { makeEffect } from "./lib/helpers";
import { availableUserActions, getActionPointCost } from "@/libs/combat/actions";
import { calcApReduction } from "@/libs/combat/turn";
import { isEffectActive } from "@/libs/combat/util";
import { getEffectPower } from "@/libs/combat/power";
import type { CompleteBattle } from "@/libs/combat/types";

const req = JSON.parse(readFileSync(process.argv[2], "utf8"));
const caps = S.joninCaps();

const JUTSU_DEFAULTS = { jutsuWeapon: "NONE", battleUsageType: "BOTH", jutsuType: "NORMAL", requiredRank: "STUDENT",
  requiredLevel: 1, jutsuRank: "D", elementClassification: "None", statClassification: "Ninjutsu", method: "SINGLE",
  methodSize: null, villageId: "", bloodlineId: "", hidden: false, injectableInBattle: false, healthCost: 0,
  chakraCost: 0, staminaCost: 0, healthCostReducePerLvl: 0, chakraCostReducePerLvl: 0, staminaCostReducePerLvl: 0,
  requiredPetSpeciesId: null, requiredSkillId: null, requiredBloodlineItemId: null, reskinParentJutsuId: null };
const norm = (rec: any) => ({ ...JUTSU_DEFAULTS, ...rec, effects: (rec.effects ?? []).filter((e: any) => e.type !== "summon") });

const NAMES = new Map<string, string>();
const RECS = new Map<string, any>();
for (const side of [req.me, req.him]) for (const k of side.kit) { NAMES.set(k.record.id, k.record.name); RECS.set(k.record.id, k.record); }
for (const r of req.inject ?? []) { NAMES.set(r.id, r.name); RECS.set(r.id, r); }

const buildUser = (side: any, village: string) => {
  const pol = { id: `policy::${side.id}`, userId: side.id, includeDefaultRules: false, rules: [] };
  const u: any = F.playerQueryUser(side.id, "jonin-cap", "striker", pol, caps);
  u.villageId = village;
  u.level = side.level ?? 100;
  u.rank = "JONIN";
  const jutsus = side.kit.filter((k: any) => k.kind !== "item");
  const items = side.kit.filter((k: any) => k.kind === "item");
  u.jutsus = jutsus.map((k: any, i: number) => ({
    id: `uj-${side.id}-${i}`, userId: side.id, jutsuId: k.record.id, level: k.level ?? 25, experience: 0,
    equipped: true, finishTraining: null, reskinId: null, jutsu: norm(k.record),
  }));
  let slot = 0;
  u.items = items.map((k: any, i: number) => ({
    id: `ui-${side.id}-${i}`, userId: side.id, itemId: k.record.id, quantity: 20, level: k.level ?? 25,
    experience: 0, equipped: `ITEM_${++slot}`, durability: 100, dropChancePerc: 0, imbuements: [], lastUsedRound: -99,
    item: norm(k.record),
  }));
  if (side.bloodline) { u.bloodline = side.bloodline; u.bloodlineId = side.bloodline.id; }
  const bl = jutsus.find((k: any) => k.record.bloodlineId)?.record.bloodlineId;
  if (bl && !u.bloodlineId) u.bloodlineId = bl;
  const BASIC_EL = new Set(["Fire", "Water", "Wind", "Earth", "Lightning"]);
  const els: string[] = [...new Set([...(side.elements ?? []),
    ...jutsus.flatMap((k: any) => k.record.effects.flatMap((e: any) => e.elements ?? []))])]
    .filter((x: any) => x && x !== "None") as string[];
  const slots = [...els.filter((e) => !BASIC_EL.has(e)), ...els.filter((e) => BASIC_EL.has(e))].slice(0, 2);
  const trained = side.trainedElement === null ? undefined : (side.trainedElement ?? els.find((e) => BASIC_EL.has(e) && !slots.includes(e)));
  u.primaryElement = slots[0] ?? null;
  u.secondaryElement = slots[1] ?? null;
  if (trained) { u.activeTrainedElement = trained; u.elementalMastery = { ...(u.elementalMastery ?? {}), [trained]: 300_000 }; }
  return u;
};

const userOf = (b: CompleteBattle, cid: string) => b.usersState.find((u) => u.controllerId === cid)!;
const otherOf = (b: CompleteBattle, cid: string) => b.usersState.find((u) => u.controllerId !== cid)!;
const occupied = (b: CompleteBattle, x: number, y: number) => b.usersState.some((u) => u.curHealth > 0 && u.longitude === x && u.latitude === y);
const dist = (ax: number, ay: number, bx: number, by: number) => {
  // offset hex (odd-r like) approximate: use engine grid distance via cube conversion (columns = longitude)
  const toCube = (c: number, r: number) => { const x = c - (r - (r & 1)) / 2; const z = r; return [x, -x - z, z]; };
  const [a1, a2, a3] = toCube(ax, ay); const [b1, b2, b3] = toCube(bx, by);
  return Math.max(Math.abs(a1 - b1), Math.abs(a2 - b2), Math.abs(a3 - b3));
};

const targetFor = (b: CompleteBattle, cid: string, a: string, at?: [number, number]) => {
  if (at) return { x: at[0], y: at[1] };
  const me = userOf(b, cid); const other = otherOf(b, cid);
  const rec = RECS.get(a);
  if (["defensiveStance", "offensiveStance", "basicHeal", "meditate", "cleanse"].includes(a) || rec?.target === "SELF")
    return { x: me.longitude, y: me.latitude };
  if (rec?.target === "EMPTY_GROUND") {
    // a free tile next to the opponent (moves close the gap; ground casts land beside me when range is short)
    const range = rec.range ?? 1;
    let best: any = null;
    for (let x = 0; x < b.width; x++) for (let y = 0; y < b.height; y++) {
      if (occupied(b, x, y) || dist(me.longitude, me.latitude, x, y) > range) continue;
      const d = dist(x, y, other.longitude, other.latitude);
      if (d >= 1 && (!best || d < best.d)) best = { x, y, d };
    }
    if (best) return { x: best.x, y: best.y };
  }
  return { x: other.longitude, y: other.latitude };
};

const fx = (b: CompleteBattle, cid: string) => {
  const u = userOf(b, cid);
  return (b.usersEffects as any[]).filter((e) => e.targetId === u.userId && isEffectActive(e) && !["visual"].includes(e.type))
    .map((e) => `${e.type}${e.elements?.length ? "[" + e.elements.map((x: string) => x[0]).join("") + "]" : ""}:${Math.round(getEffectPower(e) * 10) / 10}${e.calculation === "percentage" ? "%" : ""}`
      + `:${e.fromType === "bloodline" ? "BL" : (NAMES.get(e.actionId) ?? e.actionId)}:r${e.rounds ?? "-"}${e.castThisRound ? ":new" : ""}`);
};


const BASIC_KEEP = new Set(["cleanse", "clear"]);
const ME = req.me.id, HIM = req.him.id;
const clone = <T>(x: T): T => structuredClone(x);
const isBasicSkip = (a: any) => !RECS.has(a.id) && !BASIC_KEEP.has(a.id);
const apOf = (b: CompleteBattle, cid: string) => { const u = userOf(b, cid); return u.actionPoints - calcApReduction(b as never, u.userId); };
const hpOf = (b: CompleteBattle, cid: string) => userOf(b, cid).curHealth;
const startTurn = (b: CompleteBattle, cid: string) => {
  for (const x of b.usersState) x.actionPoints = 0;
  const u = userOf(b, cid); b.activeUserId = u.userId; u.actionPoints = 100;
};
const legal = (b: CompleteBattle, cid: string) => {
  const u = userOf(b, cid); const ap = apOf(b, cid);
  return (availableUserActions(b as never, u.userId, true, true) as any[]).filter((a) => !isBasicSkip(a))
    .map((a) => ({ id: a.id as string, cost: getActionPointCost(u.userId, b as never, a) as number }))
    .filter((a) => a.cost <= ap);
};
const tryAct = (b: CompleteBattle, cid: string, id: string, at?: [number, number]): CompleteBattle | null => {
  const u = userOf(b, cid);
  const action: any = (availableUserActions(b as never, u.userId, true, true) as any[]).find((a) => a.id === id);
  if (!action) return null;
  if (getActionPointCost(u.userId, b as never, action) > apOf(b, cid)) return null;
  const t = targetFor(b, cid, id, at);
  try { const r = I.act(b, cid, id, t); return r.ok ? r.battle : null; } catch { return null; }
};
const dead = (b: CompleteBattle) => hpOf(b, ME) <= 0 || hpOf(b, HIM) <= 0;
const other = (cid: string) => (cid === ME ? HIM : ME);
let SIMS = 0;
// greedy: best immediate damage, action by action (used inside the lookahead only)
const greedy = (b: CompleteBattle, cid: string) => {
  for (let k = 0; k < 3 && !dead(b); k++) {
    let best: CompleteBattle | null = null; let bestD = 0;
    for (const a of legal(b, cid)) {
      const h0 = hpOf(b, other(cid)); const b1 = tryAct(clone(b), cid, a.id); SIMS++;
      if (!b1) continue; const d = h0 - hpOf(b1, other(cid));
      if (d > bestD) { bestD = d; best = b1; }
    }
    if (!best) break; b = best;
  }
  return b;
};
// all bundles of up to two actions after an optional pinned prefix
const bundles = (b0: CompleteBattle, cid: string, prefix: any[]) => {
  let b = b0; const ids: string[] = [];
  for (const p of prefix) { const b1 = tryAct(b, cid, p.a, p.at); if (b1) { b = b1; ids.push(p.a); } }
  const out: { ids: string[]; b: CompleteBattle }[] = [];
  const free = 2 - ids.length;
  const rec = (bb: CompleteBattle, chosen: string[], depth: number) => {
    const opts = depth > 0 && !dead(bb) ? legal(bb, cid) : [];
    let any = false;
    for (const a of opts) {
      const b1 = tryAct(clone(bb), cid, a.id); SIMS++;
      if (!b1) continue; any = true;
      rec(b1, [...chosen, a.id], depth - 1);
    }
    if (!any) out.push({ ids: chosen, b: bb });
  };
  rec(b, ids, free);
  return out;
};
const scoreFor = (cid: string, base: CompleteBattle, after: CompleteBattle, myNext: any[] | null) => {
  // cid = the chooser. Lookahead: next round, the other side plays its script or greedy, then cid greedy.
  let b = clone(after);
  const opp = other(cid);
  const lost = (bb: CompleteBattle) => ({ c: hpOf(base, cid) - hpOf(bb, cid), o: hpOf(base, opp) - hpOf(bb, opp) });
  if (!dead(b)) {
    I.nextRound(b);
    for (const first of ORDER) {
      if (dead(b)) break;
      startTurn(b, first);
      if (first === cid) b = greedy(b, cid);
      else if (first === ME && myNext) { for (const st of myNext) { const b1 = tryAct(b, ME, st.a, st.at); SIMS++; if (b1) b = b1; if (dead(b)) break; } }
      else b = greedy(b, first);
    }
  }
  const L = lost(b);
  let s = L.o - L.c;
  if (hpOf(b, opp) <= 0) s += 100000 - 1000 * (dead(after) ? 0 : 1);
  if (hpOf(b, cid) <= 0) s -= 100000;
  return s;
};
let ORDER: string[] = [ME, HIM];
const choose = (b: CompleteBattle, cid: string, prefix: any[], myNext: any[] | null) => {
  const cands = bundles(b, cid, prefix);
  const scored = cands.map((c) => ({ ids: c.ids, s: scoreFor(cid, b, c.b, myNext) }));
  scored.sort((x, y) => y.s - x.s);
  return scored;
};

const main = async () => {
  const out: any = { rounds: [] };
  const forced: any = req.forced ?? {};
  const maxRounds = req.maxRounds ?? 10;
  await S.withSeed(req.seed ?? 7, async () => {
    const me = buildUser(req.me, "village-me");
    const him = buildUser(req.him, "village-him");
    let b = await S.assembleBattle({
      users: [me, him], battleType: "COMBAT",
      placements: [{ userId: req.me.id, x: req.me.x, y: req.me.y }, { userId: req.him.id, x: req.him.x, y: req.him.y }],
      leftSideUserIds: [req.me.id],
    });
    for (const r of req.inject ?? []) (b.extraState as any).jutsus[r.id] ??= norm(r);
    const mods: any = (b as any).preBattleGearModifiers ?? (b as any).extraState?.preBattleGearModifiers;
    for (const side of [req.me, req.him]) if (mods && side.gearMods) {
      const uid = userOf(b, side.id).userId; mods[uid] = { ...(mods[uid] ?? {}), ...side.gearMods };
    }
    let n = 0;
    for (const side of [req.me, req.him]) for (const p of side.passives ?? []) {
      const u = userOf(b, side.id);
      b.usersEffects.push(makeEffect(p.type, { power: p.power, powerPerLevel: 0, rounds: 100, calculation: "percentage", ...(p.fields ?? {}) } as never, {
        id: `passive-${++n}`, creatorId: u.userId, targetId: u.userId, level: 1, isNew: false, castThisRound: false,
        createdRound: 0, longitude: u.longitude, latitude: u.latitude, actionId: "passive", fromType: "jutsu" } as never));
    }
    for (const side of [req.me, req.him]) if (side.hp) { const u = userOf(b, side.id); u.maxHealth = side.hp; u.curHealth = side.hp; }
    b.round = 1;
    ORDER = (req.order ?? ["me", "him"]).map((x: string) => (x === "me" ? ME : HIM));
    out.start = { me: { hp: hpOf(b, ME) }, him: { hp: hpOf(b, HIM) } };
    const script: any[] = req.script ?? [];
    for (let ri = 0; ri < maxRounds; ri++) {
      const R: any = { round: b.round, steps: [], choice: {} };
      for (const cid of ORDER) {
        if (dead(b)) break;
        startTurn(b, cid);
        let plan: any[];
        const scripted = cid === ME && ri < script.length && !req.meAdaptive;
        if (scripted) plan = script[ri].me ?? [];
        else {
          const prefix = cid === HIM ? (forced[ri] ?? []) : [];
          const myNext = cid === HIM && ri + 1 < script.length ? script[ri + 1].me : null;
          const sc = choose(clone(b), cid, prefix, myNext);
          R.choice[cid === ME ? "me" : "him"] = sc.slice(0, 3).map((x) => ({ s: Math.round(x.s), names: x.ids.map((i) => NAMES.get(i) ?? i) }));
          plan = (sc[0]?.ids ?? []).map((a) => ({ a }));
          // keep pinned targets of forced actions
          for (const p of prefix) { const q = plan.find((x) => x.a === p.a); if (q && p.at) q.at = p.at; }
        }
        for (const st of plan) {
          const actor = cid === ME ? "me" : "him";
          const hp0 = { me: hpOf(b, ME), him: hpOf(b, HIM) };
          const b1 = tryAct(b, cid, st.a, st.at);
          const step: any = { actor, a: st.a, name: NAMES.get(st.a) ?? st.a, ok: !!b1, ap: apOf(b, cid) };
          if (b1) {
            b = b1;
            step.dmg = { me: Math.round(hp0.me - hpOf(b, ME)), him: Math.round(hp0.him - hpOf(b, HIM)) };
            step.hp = { me: Math.round(hpOf(b, ME)), him: Math.round(hpOf(b, HIM)) };
          }
          R.steps.push(step);
          if (dead(b)) break;
        }
        // a scripted step that failed (stun AP, cooldown, range): fill the AP left by the same search
        if (scripted && !dead(b) && R.steps.some((x: any) => x.actor === "me" && !x.ok) && legal(b, ME).length) {
          const sc = choose(clone(b), ME, [], null);
          R.choice.meFill = sc.slice(0, 2).map((x) => ({ s: Math.round(x.s), names: x.ids.map((i) => NAMES.get(i) ?? i) }));
          for (const id of sc[0]?.ids ?? []) {
            const hp0 = { me: hpOf(b, ME), him: hpOf(b, HIM) };
            const b1 = tryAct(b, ME, id);
            const step: any = { actor: "me", a: id, name: (NAMES.get(id) ?? id) + " (fill)", ok: !!b1 };
            if (b1) { b = b1; step.dmg = { me: Math.round(hp0.me - hpOf(b, ME)), him: Math.round(hp0.him - hpOf(b, HIM)) }; }
            R.steps.push(step);
            if (dead(b)) break;
          }
        }
      }
      R.end = { me: Math.round(hpOf(b, ME)), him: Math.round(hpOf(b, HIM)) };
      R.fxMe = fx(b, ME); R.fxHim = fx(b, HIM);
      out.rounds.push(R);
      if (dead(b)) break;
      I.nextRound(b);
    }
    out.result = hpOf(b, HIM) <= 0 ? "win" : hpOf(b, ME) <= 0 ? "loss" : "open";
    out.final = { me: Math.round(hpOf(b, ME)), him: Math.round(hpOf(b, HIM)), round: out.rounds.length };
    out.sims = SIMS;
  });
  process.stdout.write(JSON.stringify(out, null, 1));
};

main().catch((e) => { console.error(String(e?.message ?? e).slice(0, 800), String(e?.stack ?? "").slice(0, 1500)); process.exit(1); });
