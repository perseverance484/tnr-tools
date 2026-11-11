/**
 * Replay-based PvP turn simulator (offline, in-process, sockets denied by offline_exec.py).
 *
 * Instead of rebuilding live tags from log text, this replays the battle: every logged action of both sides,
 * in order, through the engine's own availableUserActions → performBattleAction path with the real records.
 * The engine then holds every effect itself (seals, time compression/dilation, barriers, ground effects,
 * prevents, stuns, potency changes, heal-over-time, cooldowns, shared locks). After the replay the actual HP
 * and positions are restored from the live battle.
 *
 * Input (argv[2], JSON):
 *   round, hisTurn: "same" | "next", mode: "list" | "eval"
 *   me / him: { id, hp, x, y, profile?, kit: [{ record, level, kind }], passives?: [{type, power}] }
 *   log: [{ round, actor: "me" | "him", actionId }]       — chronological, "wait"/"move" allowed (skipped)
 *   candidates?: [[{ actionId, x, y }]]                   — eval mode
 *   replyCap?: number                                      — max enemy reply bundles to try (default 60)
 * Output: { ap, available: [{id, name, cost}], replayIssues: [...], results?: [...] }
 *   results[i] = { legal, failedAt?, reason?, afterMe: {me, him}, best: {me, him, actions}, typical: {...} }
 */
import { readFileSync } from "node:fs";
import * as F from "./lib/fixtures";
import * as S from "./lib/sim";
import * as I from "./lib/itembattle";
import { makeEffect } from "./lib/helpers";
import { availableUserActions, getActionPointCost } from "@/libs/combat/actions";
import { calcApReduction } from "@/libs/combat/turn";
import { getActionAffectedTiles, getBattleGrid } from "@/libs/combat/util";
import { getPossibleActionTiles } from "@/libs/hexgrid";
import type { CompleteBattle } from "@/libs/combat/types";

const req = JSON.parse(readFileSync(process.argv[2], "utf8"));
const caps = S.joninCaps();
const issues: any[] = [];
const BASIC_SKIP = new Set(["wait", "move", "flee", "endTurn"]);

// older captures lack some columns the engine reads; fill schema defaults (only where absent)
const JUTSU_DEFAULTS = { jutsuWeapon: "NONE", battleUsageType: "BOTH", jutsuType: "NORMAL", requiredRank: "STUDENT",
  requiredLevel: 1, jutsuRank: "D", elementClassification: "None", statClassification: "Ninjutsu", method: "SINGLE",
  methodSize: null, villageId: "", bloodlineId: "", hidden: false, injectableInBattle: false, healthCost: 0,
  chakraCost: 0, staminaCost: 0, healthCostReducePerLvl: 0, chakraCostReducePerLvl: 0, staminaCostReducePerLvl: 0,
  requiredPetSpeciesId: null, requiredSkillId: null, requiredBloodlineItemId: null, reskinParentJutsuId: null };
const stripSummons = (rec: any) => ({ ...JUTSU_DEFAULTS, ...rec,
  effects: (rec.effects ?? []).filter((e: any) => e.type !== "summon") });

const buildUser = (side: any, village: string) => {
  const pol = { id: `policy::${side.id}`, userId: side.id, includeDefaultRules: false, rules: [] };
  const u: any = F.playerQueryUser(side.id, side.band ?? "jonin-cap", "striker", pol, caps);
  u.villageId = village;
  for (const k of ["offence", "defence", "strength", "speed", "intelligence", "willpower", "ninjutsuMastery",
    "genjutsuMastery", "taijutsuMastery", "bukijutsuMastery", "bloodlineMastery", "sageMastery",
    "preferredGeneral1", "preferredGeneral2", "level", "rank", "bloodlineId"]) {
    if (side.profile?.[k] !== undefined) u[k] = side.profile[k];
  }
  const jutsus = side.kit.filter((k: any) => k.kind === "jutsu");
  const items = side.kit.filter((k: any) => k.kind === "item");
  u.jutsus = jutsus.map((k: any, i: number) => ({
    id: `uj-${side.id}-${i}`, userId: side.id, jutsuId: k.record.id, level: k.level ?? 25, experience: 0,
    equipped: true, finishTraining: null, reskinId: null, jutsu: stripSummons(k.record),
  }));
  let hand = 0, slot = 0;
  u.items = items.map((k: any, i: number) => ({
    id: `ui-${side.id}-${i}`, userId: side.id, itemId: k.record.id, quantity: 20, level: k.level ?? 25,
    experience: 0, equipped: k.record.itemType === "WEAPON" ? `HAND_${++hand}` : `ITEM_${++slot}`,
    durability: 100, dropChancePerc: 0, imbuements: [], lastUsedRound: -99, item: stripSummons(k.record),
  }));
  // worn gear (armor / accessory / keystone): processUsersForBattle folds its percentages into the pre-battle gear
  // stage (damagePipeline.ts consolidatePreBattleDamageModifiers: gear sums additively) and applies finished
  // imbuements on imbuable pieces (mastery.ts wornGearTags)
  let gearN = 0;
  for (const g of side.gear ?? []) {
    const n = ++gearN;
    u.items.push({
      id: `ug-${side.id}-${n}`, userId: side.id, itemId: g.record.id, quantity: 1, level: 25, experience: 0,
      equipped: g.slot, durability: g.record.maxDurability ?? 100, dropChancePerc: 0, lastUsedRound: -99,
      item: g.record,
      imbuements: g.imbue ? [{ id: `im-${side.id}-${n}`, userItemId: `ug-${side.id}-${n}`, itemId: g.imbue.id,
        craftingFinishedAt: new Date(0), item: g.imbue }] : [],
    });
  }
  // bloodline row: its effects become passive "bloodline" effects (sealable; damage mods use bloodline stacking)
  if (side.bloodline) { u.bloodline = side.bloodline; u.bloodlineId = side.bloodline.id; }
  const bl = jutsus.find((k: any) => k.record.bloodlineId)?.record.bloodlineId;
  if (bl && !u.bloodlineId) u.bloodlineId = bl;
  // element access (engine elementalMastery.ts providedElements/getUserElements): two innate slots plus one unlocked
  // trained BASIC element. A real kit can span three elements (Targaryen: Storm bloodline + Water + Lightning), so fill
  // the innate slots non-basic first and give the trained slot to a leftover basic element. side.elements (used-first
  // order from the bridge) wins when given. Access only: the trained element's +15% passive is not added here (the
  // fitted damage passive covers live passives; see README).
  const BASIC_EL = new Set(["Fire", "Water", "Wind", "Earth", "Lightning"]);
  const els: string[] = [...new Set([...(side.elements ?? []),
    ...jutsus.flatMap((k: any) => k.record.effects.flatMap((e: any) => e.elements ?? []))])]
    .filter((x: any) => x && x !== "None") as string[];
  const slots = [...els.filter((e) => !BASIC_EL.has(e)), ...els.filter((e) => BASIC_EL.has(e))].slice(0, 2);
  const trained = els.find((e) => BASIC_EL.has(e) && !slots.includes(e));
  u.primaryElement = slots[0] ?? null;
  u.secondaryElement = slots[1] ?? null;
  if (trained) {
    u.activeTrainedElement = trained;
    u.elementalMastery = { ...(u.elementalMastery ?? {}), [trained]: 300_000 };
  }
  u.curHealth = 5050;
  return u;
};

let effN = 0;
const addPassives = (b: CompleteBattle, side: any, u: any) => {
  for (const p of side.passives ?? []) {
    b.usersEffects.push(makeEffect(p.type, { power: p.power, powerPerLevel: 0, rounds: 100, calculation: "percentage" } as never, {
      id: `passive-${++effN}`, creatorId: u.userId, targetId: u.userId, level: 1, isNew: false, castThisRound: false,
      createdRound: 0, longitude: u.longitude, latitude: u.latitude, actionId: "passive", fromType: "jutsu",
    } as never));
  }
};

const userOf = (b: CompleteBattle, cid: string) => b.usersState.find((u) => u.controllerId === cid)!;
// records by id from the request kits (battle user state does not carry the jutsu/item rows after assembly)
const KIT = new Map<string, any>();
for (const side of [req.me, req.him]) for (const k of side.kit ?? []) KIT.set(k.record.id, k.record);
const recordOf = (_b: CompleteBattle, _cid: string, id: string) => KIT.get(id);
const SELF_BASICS = new Set(["defensiveStance", "offensiveStance", "basicHeal", "meditate", "cleanse"]);

/** Target tile for an action: self for self-targeted, the opponent's tile otherwise. */
const targetFor = (b: CompleteBattle, cid: string, actionId: string) => {
  const me = userOf(b, cid);
  const other = b.usersState.find((u) => u.controllerId !== cid && u.curHealth > 0)!;
  const rec = recordOf(b, cid, actionId);
  if (SELF_BASICS.has(actionId) || rec?.target === "SELF") return { x: me.longitude, y: me.latitude };
  if (actionId === "replacementTechnique" || (rec && (rec.effects ?? []).some((e: any) => e.type === "move"))) {
    // reposition onto a free neighbour (positions are restored after the replay)
    for (const [dx, dy] of [[-1, 0], [1, 0], [0, -1], [0, 1], [-1, 1], [1, -1]]) {
      const x = me.longitude + dx, y = me.latitude + dy;
      if (x >= 0 && y >= 0 && x < b.width && y < b.height && !(x === other.longitude && y === other.latitude)) return { x, y };
    }
  }
  return { x: other.longitude, y: other.latitude };
};

const tryAct = (b: CompleteBattle, cid: string, actionId: string, at?: { x: number; y: number }) => {
  try {
    const r = I.act(b, cid, actionId, at ?? targetFor(b, cid, actionId));
    return r.ok ? { ok: true, battle: r.battle, effects: (r as any).effects ?? [] }
      : { ok: false, reason: r.reason, battle: b };
  } catch (err) {
    return { ok: false, reason: String((err as Error).message).slice(0, 140), battle: b };
  }
};

const setActive = (b: CompleteBattle, cid: string, ap?: number) => {
  const u = userOf(b, cid);
  for (const x of b.usersState) x.actionPoints = 0;
  b.activeUserId = u.userId;
  // the engine keeps actionPoints at 100 and subtracts the stun when it checks an action
  // (actions.ts actionPointsAfterAction); pre-subtracting it here counted a stun twice
  u.actionPoints = ap ?? 100;
};

const trace: any[] = [];
const prepare = async (): Promise<CompleteBattle> => {
  const me = buildUser(req.me, "village-me");
  const him = buildUser(req.him, "village-him");
  let b = await S.assembleBattle({
    users: [me, him], battleType: "COMBAT",
    placements: [{ userId: req.me.id, x: req.me.x, y: req.me.y }, { userId: req.him.id, x: req.him.x, y: req.him.y }],
    leftSideUserIds: [req.me.id],
  });
  addPassives(b, req.me, userOf(b, req.me.id));
  addPassives(b, req.him, userOf(b, req.him.id));
  b.round = 1;
  let cur = 1;
  let lastActor = "";
  for (const step of req.log ?? []) {
    if (step.round > req.round) break;
    while (cur < step.round) {
      I.nextRound(b);
      cur = b.round;
      lastActor = "";
      // keep both alive through the replay; actual HP is restored at the end
      for (const u of b.usersState) u.curHealth = Math.max(u.curHealth, 3000);
    }
    if (BASIC_SKIP.has(step.actionId)) continue;
    const cid = step.actor === "me" ? req.me.id : req.him.id;
    // AP is not what we replay for (effects are): give the actor a full 100 before each logged action
    setActive(b, cid, 100);
    lastActor = step.actor;
    const meU = userOf(b, req.me.id), himU = userOf(b, req.him.id);
    const hp0 = { me: meU.curHealth, him: himU.curHealth };
    const r = tryAct(b, cid, step.actionId);
    if (r.ok) {
      const m1 = userOf(r.battle, req.me.id), h1 = userOf(r.battle, req.him.id);
      trace.push({ round: step.round, actor: step.actor, actionId: step.actionId,
        me: Math.round(hp0.me - m1.curHealth), him: Math.round(hp0.him - h1.curHealth),
        // the engine's own log lines: direct hits ("<user> takes N damage") compare like for like with the live log
        hits: (() => { const out: any = { me: 0, him: 0 }; const names: any = { [m1.username]: "me", [h1.username]: "him" };
          for (const e of ((r as any).effects ?? []) as any[]) { const m = /^(\S+) takes ([\d.]+) damage$/.exec(String(e.txt ?? "").trim());
            if (m && names[m[1]]) out[names[m[1]]] += Number(m[2]); } return { me: Math.round(out.me), him: Math.round(out.him) }; })(),
        ...(req.trace === "effects" ? { fx: (b.usersEffects as any[]).map((e) => `${e.targetId === m1.userId ? "me" : "him"}:${e.type}:${Math.round(e.power ?? 0)}+L${e.level}x${e.powerPerLevel}:r${e.createdRound}+${e.rounds}`) } : {}) });
    }
    if (!r.ok) {
      const u = userOf(b, cid);
      const a: any = availableUserActions(b as never, u.userId, true, true).find((x: any) => x.id === step.actionId);
      issues.push({ round: step.round, actor: step.actor, actionId: step.actionId, reason: r.reason,
        ap: u.actionPoints, stun: calcApReduction(b as never, u.userId), cost: a ? getActionPointCost(u.userId, b as never, a) : null,
        listed: !!a, pos: [u.longitude, u.latitude], active: b.activeUserId === u.userId, round: b.round,
        tiles: (() => {
          if (!a) return null;
          const grid = getBattleGrid(1, b as never);
          const at = targetFor(b, cid, step.actionId);
          const uh = grid.getHex({ col: u.longitude, row: u.latitude });
          const th = grid.getHex({ col: at.x, row: at.y });
          const hl = getPossibleActionTiles(a, uh as never, grid as never);
          const alive = b.usersState.filter((x) => x.curHealth > 0);
          alive.forEach((x: any) => { x.hex = grid.getHex({ col: x.longitude, row: x.latitude }); });
          const r2: any = getActionAffectedTiles({ a: uh as never, b: th as never, action: a, grid: grid as never,
            restrictGrid: hl as never, users: alive as never, ground: b.groundEffects as never, userId: u.userId });
          return { target: at, highlights: hl ? (hl as any).size : null, green: r2?.green?.size, ground: b.groundEffects.length,
                   groundAtMe: b.groundEffects.filter((g: any) => g.longitude === u.longitude && g.latitude === u.latitude).map((g: any) => g.type) };
        })() });
    }
    b = r.battle;
    // restore positions after any reposition so ranges match the live board
    const m2 = userOf(b, req.me.id), h2 = userOf(b, req.him.id);
    m2.longitude = req.me.x; m2.latitude = req.me.y; h2.longitude = req.him.x; h2.latitude = req.him.y;
    for (const u of b.usersState) u.curHealth = Math.max(u.curHealth, 3000);
    void meU; void himU;
  }
  while (b.round < req.round) I.nextRound(b);
  const meU = userOf(b, req.me.id), himU = userOf(b, req.him.id);
  meU.curHealth = req.me.hp; himU.curHealth = req.him.hp;
  // pools: the replay drains chakra/stamina (poison, drain, pool-cost debuffs) without the live regen and potions, so
  // restore them from the live battle when given, else full (live pools are rarely the binding constraint)
  for (const [side, u] of [[req.me, meU], [req.him, himU]] as const) {
    const uu: any = u;
    uu.curChakra = side.cp ?? uu.maxChakra ?? uu.curChakra;
    uu.curStamina = side.sp ?? uu.maxStamina ?? uu.curStamina;
  }
  meU.longitude = req.me.x; meU.latitude = req.me.y; himU.longitude = req.him.x; himU.latitude = req.him.y;
  // whose turn: if he already acted this round (hisTurn === "next"), I act now and he replies next round
  setActive(b, req.me.id);
  return b;
};

const hp = (b: CompleteBattle, cid: string) => Math.round(userOf(b, cid).curHealth);

const available = (b: CompleteBattle, cid: string) => {
  const u = userOf(b, cid);
  return availableUserActions(b as never, u.userId, true, true)
    .filter((a: any) => !BASIC_SKIP.has(a.id))
    .map((a: any) => ({ id: a.id, name: a.name, cost: getActionPointCost(u.userId, b as never, a) }));
};

/** His reply bundles: subsets (size <= 3) of his available actions that fit his AP, most damaging first. */
const replyBundles = (b: CompleteBattle) => {
  const u = userOf(b, req.him.id);
  const ap = Math.max(0, 100 - calcApReduction(b as never, u.userId));
  // real attacking/support actions first; stances, heals and pure moves only as AP fillers
  const FILLER = new Set(["replacementTechnique", "meditate", "defensiveStance", "offensiveStance", "basicHeal"]);
  const all = available(b, req.him.id);
  const meU = userOf(b, req.me.id);
  const adjacent = Math.max(Math.abs(meU.longitude - u.longitude), Math.abs(meU.latitude - u.latitude)) <= 1;
  const acts = all.filter((a) => !FILLER.has(a.id) && (a.id !== "basicAttack" || adjacent))
    .concat(all.filter((a) => a.id === "offensiveStance").slice(0, 1));
  const out: string[][] = [];
  const n = acts.length;
  for (let i = 0; i < n; i++) {
    if (acts[i].cost <= ap) out.push([acts[i].id]);
    for (let j = i + 1; j < n; j++) {
      const c2 = acts[i].cost + acts[j].cost;
      if (c2 <= ap) out.push([acts[i].id, acts[j].id]);
      for (let k = j + 1; k < n; k++) {
        if (c2 + acts[k].cost <= ap) out.push([acts[i].id, acts[j].id, acts[k].id]);
      }
    }
  }
  // most damaging first (record damage/pierce/elemental power), then fuller AP use
  const power = (id: string) => (KIT.get(id)?.effects ?? [])
    .filter((e: any) => ["damage", "pierce", "elementaldamage"].includes(e.type))
    .reduce((s: number, e: any) => s + (e.power ?? 0) + 25 * (e.powerPerLevel ?? 0), 0) + (id === "basicAttack" ? 10 : 0);
  const cost = (bb: string[]) => bb.reduce((s, id) => s + (acts.find((a) => a.id === id)?.cost ?? 0), 0);
  const val = (bb: string[]) => bb.reduce((s, id) => s + power(id), 0) * 10 + cost(bb) / 10
    + (bb.some((id) => (KIT.get(id)?.effects ?? []).some((e: any) => ["increasedamagegiven", "increasedamagetaken", "stun"].includes(e.type))) ? 5 : 0);
  out.sort((x, y) => val(y) - val(x));
  return { ap, bundles: out.slice(0, req.replyCap ?? 60) };
};

const main = async () => {
  const base = await S.withSeed(7, prepare);
  const res: any = { round: base.round,
    ap: Math.max(0, userOf(base, req.me.id).actionPoints - calcApReduction(base as never, userOf(base, req.me.id).userId)), available: available(base, req.me.id),
    replayIssues: issues, ...(req.trace ? { trace } : {}) };
  if (req.mode === "eval") {
    res.results = [];
    for (const cand of req.candidates ?? []) {
      const out: any = { bundle: cand.map((a: any) => a.actionId) };
      await S.withSeed(11, async () => {
        let b = structuredClone(base);
        for (let i = 0; i < cand.length; i++) {
          const a = cand[i];
          const r = tryAct(b, req.me.id, a.actionId, a.x === undefined ? undefined : { x: a.x, y: a.y });
          if (!r.ok) {
            const u: any = userOf(b, req.me.id);
            out.legal = false; out.failedAt = i; out.reason = r.reason;
            out.state = { ap: u.actionPoints, stun: calcApReduction(b as never, u.userId), cp: Math.round(u.curChakra), sp: Math.round(u.curStamina), hp: Math.round(u.curHealth) };
            return;
          }
          b = r.battle;
          if (hp(b, req.me.id) <= 0 || hp(b, req.him.id) <= 0) break;
        }
        out.legal = true;
        out.afterMe = { me: hp(b, req.me.id), him: hp(b, req.him.id) };
        if (out.afterMe.me <= 0 || out.afterMe.him <= 0) return;
        const b1 = structuredClone(b);
        if (req.hisTurn === "next") I.nextRound(b1);
        setActive(b1, req.him.id);
        const { bundles } = replyBundles(b1);
        const tried: any[] = [];
        for (const rb of bundles) {
          let b2 = structuredClone(b1);
          const done: string[] = [];
          for (const id of rb) {
            const r = tryAct(b2, req.him.id, id);
            if (!r.ok) { if ((out.replyFail ??= []).length < 4) out.replyFail.push([id, r.reason]); continue; }
            b2 = r.battle;
            done.push(id);
            if (hp(b2, req.me.id) <= 0) break;
          }
          if (done.length) tried.push({ actions: done, me: hp(b2, req.me.id), him: hp(b2, req.him.id) });
        }
        tried.sort((x, y) => x.me - y.me);
        out.replyCount = tried.length;
        out.best = tried[0] ?? null;                                   // worst case for me
        out.typical = tried[Math.floor(tried.length / 2)] ?? null;    // median damage reply
      });
      res.results.push(out);
    }
  }
  process.stdout.write(JSON.stringify(res));
};

main().catch((e) => { console.error(String(e?.message ?? e).slice(0, 800), String(e?.stack ?? "").slice(0, 1200)); process.exit(1); });
