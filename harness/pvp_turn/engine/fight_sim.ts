/**
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

const main = async () => {
  const out: any = { rounds: [] };
  await S.withSeed(req.seed ?? 7, async () => {
    const me = buildUser(req.me, "village-me");
    const him = buildUser(req.him, "village-him");
    let b = await S.assembleBattle({
      users: [me, him], battleType: "COMBAT",
      placements: [{ userId: req.me.id, x: req.me.x, y: req.me.y }, { userId: req.him.id, x: req.him.x, y: req.him.y }],
      leftSideUserIds: [req.me.id],
    });
    for (const r of req.inject ?? []) (b.extraState as any).jutsus[r.id] ??= norm(r);
    // measured gear totals (fit_gear.py) on the pre-battle gear stage
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
    b.round = 1;
    out.start = { me: { hp: userOf(b, req.me.id).curHealth, fx: fx(b, req.me.id) }, him: { hp: userOf(b, req.him.id).curHealth, fx: fx(b, req.him.id) } };
    for (const [ri, rnd] of (req.script as any[]).entries()) {
      const R: any = { round: b.round, steps: [] };
      for (const actor of rnd.order ?? ["me", "him"]) {
        const cid = actor === "me" ? req.me.id : req.him.id;
        for (const x of b.usersState) x.actionPoints = 0;
        const u0 = userOf(b, cid);
        b.activeUserId = u0.userId;
        u0.actionPoints = 100;
        for (const st of rnd[actor] ?? []) {
          const u = userOf(b, cid);
          const stun = calcApReduction(b as never, u.userId);
          const action: any = availableUserActions(b as never, u.userId, true, true).find((a: any) => a.id === st.a);
          const cost = action ? getActionPointCost(u.userId, b as never, action) : null;
          const ap = u.actionPoints - stun;
          const hp0 = { me: userOf(b, req.me.id).curHealth, him: userOf(b, req.him.id).curHealth };
          const at = targetFor(b, cid, st.a, st.at);
          let r: any;
          try { r = I.act(b, cid, st.a, at); } catch (e) { r = { ok: false, reason: String((e as Error).message).slice(0, 160) }; }
          const step: any = { actor, a: st.a, name: NAMES.get(st.a) ?? st.a, at: [at.x, at.y], ok: !!r.ok && r.battle !== b || !!r.ok, ap, cost, stun };
          if (!r.ok) { step.ok = false; step.reason = r.reason; R.steps.push(step); continue; }
          b = r.battle;
          const lines = ((r.effects ?? []) as any[]).map((e) => String(e.txt ?? "").trim()).filter(Boolean);
          const after = { me: userOf(b, req.me.id).curHealth, him: userOf(b, req.him.id).curHealth };
          step.apLeft = userOf(b, cid).actionPoints - calcApReduction(b as never, userOf(b, cid).userId);
          step.dmg = { me: Math.round(hp0.me - after.me), him: Math.round(hp0.him - after.him) };
          step.hp = { me: Math.round(after.me), him: Math.round(after.him) };
          step.pos = { me: [userOf(b, req.me.id).longitude, userOf(b, req.me.id).latitude], him: [userOf(b, req.him.id).longitude, userOf(b, req.him.id).latitude] };
          step.lines = lines;
          step.fxMe = fx(b, req.me.id); step.fxHim = fx(b, req.him.id);
          if (st.available) step.available = availableUserActions(b as never, userOf(b, cid).userId, true, true).map((a: any) => `${a.name}:${getActionPointCost(userOf(b, cid).userId, b as never, a)}`);
          R.steps.push(step);
          if (req.keepAlive) for (const x of b.usersState) x.curHealth = x.maxHealth;
          if (after.me <= 0 || after.him <= 0) { if (!req.keepAlive) break; }
        }
      }
      out.rounds.push(R);
      if (req.keepAlive) for (const x of b.usersState) x.curHealth = x.maxHealth;
      if (!req.keepAlive && (userOf(b, req.me.id).curHealth <= 0 || userOf(b, req.him.id).curHealth <= 0)) break;
      if (ri < req.script.length - 1) I.nextRound(b);
      R.endFx = { me: fx(b, req.me.id), him: fx(b, req.him.id) };
    }
  });
  process.stdout.write(JSON.stringify(out, null, 1));
};

main().catch((e) => { console.error(String(e?.message ?? e).slice(0, 800), String(e?.stack ?? "").slice(0, 1500)); process.exit(1); });
