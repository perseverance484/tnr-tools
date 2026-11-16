/**
 * PvP turn simulator on the pinned TNR engine (offline, in-process, sockets denied by offline_exec.py).
 *
 * Input (argv[2], JSON):
 *   round, hisTurn: "same" | "next"           — does his reply come later this round, or next round
 *   me / him: { id, hp, x, y, ap?, profile?, kit: [{ record, level, kind: "jutsu" | "item" }],
 *               used: [{ actionId, round }], band?: "jonin-cap" | "upstream-helper" }
 *   effects: [{ type, on: "me" | "him", by: "me" | "him", power, rounds, calculation?, fields? }]
 *   candidates: [[{ actionId, x, y }]]          — my bundles, fired in order
 *   replies: [{ name, actions: [{ actionId, x?, y? }] }]   — his reply options (x,y default: my tile / his tile)
 * Output (stdout, JSON): per candidate { legal, failedAt?, afterMe: {me, him}, replies: [{ name, me, him, legal }] }
 *
 * Every number comes from the engine's own availableUserActions → performBattleAction path on a battle
 * assembled by processUsersForBattle (via the frozen ghost_ship_final lib, copied at run time).
 * Approximations (declared): live tags are injected as engine effects rebuilt from the battle log text;
 * gear/armor modifiers are not modelled (both sides bare); the opponent uses the declared stat band.
 */
import { readFileSync } from "node:fs";
import * as F from "./lib/fixtures";
import * as S from "./lib/sim";
import * as I from "./lib/itembattle";
import { makeEffect } from "./lib/helpers";
import type { CompleteBattle } from "@/libs/combat/types";

const req = JSON.parse(readFileSync(process.argv[2], "utf8"));
const caps = S.joninCaps();

const buildUser = (side: any, village: string) => {
  const pol = { id: `policy::${side.id}`, userId: side.id, includeDefaultRules: false, rules: [] };
  const u: any = F.playerQueryUser(side.id, side.band ?? "jonin-cap", "striker", pol, caps);
  u.villageId = village;
  if (side.profile) {
    for (const k of ["offence", "defence", "strength", "speed", "intelligence", "willpower", "ninjutsuMastery",
      "genjutsuMastery", "taijutsuMastery", "bukijutsuMastery", "bloodlineMastery", "sageMastery",
      "preferredGeneral1", "preferredGeneral2", "level", "rank", "bloodlineId"] as const) {
      if (side.profile[k] !== undefined) u[k] = side.profile[k];
    }
  }
  const jutsus = side.kit.filter((k: any) => k.kind === "jutsu");
  const items = side.kit.filter((k: any) => k.kind === "item");
  u.jutsus = jutsus.map((k: any, i: number) => ({
    id: `uj-${side.id}-${i}`, userId: side.id, jutsuId: k.record.id, level: k.level ?? 25, experience: 0,
    equipped: true, finishTraining: null, reskinId: null, jutsu: k.record,
  }));
  let hand = 0, slot = 0;
  u.items = items.map((k: any, i: number) => ({
    id: `ui-${side.id}-${i}`, userId: side.id, itemId: k.record.id, quantity: 20, level: k.level ?? 25,
    experience: 0,
    equipped: k.record.itemType === "WEAPON" ? `HAND_${++hand}` : `ITEM_${++slot}`,
    durability: 100, dropChancePerc: 0, imbuements: [], lastUsedRound: -99,
    item: k.record,
  }));
  // bloodline jutsu need the matching bloodline on the user
  const bl = jutsus.find((k: any) => k.record.bloodlineId)?.record.bloodlineId;
  if (bl && !u.bloodlineId) u.bloodlineId = bl;
  // element gate: live, the bloodline supplies the elements; the harness user has no bloodline row, so
  // use primary/secondary elements taken from the kit (engine falls back to these, elementalMastery.ts)
  const els = [...new Set(jutsus.flatMap((k: any) => k.record.effects.flatMap((e: any) => e.elements ?? [])))]
    .filter((x: any) => x && x !== "None");
  u.primaryElement = side.elements?.[0] ?? els[0] ?? null;
  u.secondaryElement = side.elements?.[1] ?? els[1] ?? null;
  u.curHealth = side.hp;
  return u;
};

const skipped: any[] = [];
const effectId = (() => { let n = 0; return () => `inj-${++n}`; })();

const prepare = async (): Promise<CompleteBattle> => {
  const me = buildUser(req.me, "village-me");
  const him = buildUser(req.him, "village-him");
  const b = await S.assembleBattle({
    users: [me, him], battleType: "COMBAT",
    placements: [{ userId: req.me.id, x: req.me.x, y: req.me.y }, { userId: req.him.id, x: req.him.x, y: req.him.y }],
    leftSideUserIds: [req.me.id],
  });
  b.round = req.round;
  const uidOf = (cid: string) => I.uid(b, cid);
  const meU = b.usersState.find((u) => u.controllerId === req.me.id)!;
  const himU = b.usersState.find((u) => u.controllerId === req.him.id)!;
  meU.curHealth = req.me.hp;
  himU.curHealth = req.him.hp;
  // cooldowns: lastUsedRound on the battle copies of the user's jutsu/items
  for (const [side, u] of [[req.me, meU], [req.him, himU]] as const) {
    for (const used of side.used ?? []) {
      for (const coll of [(u as any).jutsus ?? [], (u as any).items ?? [], (u as any).basicActions ?? []]) {
        for (const x of coll) {
          const id = x.jutsuId ?? x.itemId ?? x.id;
          if (id === used.actionId) x.lastUsedRound = Math.max(x.lastUsedRound ?? -99, used.round);
        }
      }
    }
  }
  // live tags rebuilt from the log
  for (const e of req.effects ?? []) {
    const target = e.on === "me" ? meU : himU;
    const creator = e.by === "me" ? meU : himU;
    try {
    b.usersEffects.push(makeEffect(e.type, {
      power: e.power, powerPerLevel: 0, rounds: e.rounds, calculation: e.calculation ?? "percentage", ...(e.fields ?? {}),
    } as never, {
      id: effectId(), creatorId: creator.userId, targetId: target.userId, level: 1,
      // fresh = cast earlier this round (live from next round, engine castThisRound semantics)
      isNew: !!e.fresh, castThisRound: !!e.fresh, createdRound: e.fresh ? req.round : req.round - 1,
      longitude: target.longitude, latitude: target.latitude, actionId: `inj-${e.type}`, fromType: "jutsu",
    } as never));
    } catch (err) {
      skipped.push({ type: e.type, on: e.on, error: String((err as any)?.issues?.[0]?.message ?? (err as Error).message).slice(0, 160) });
    }
  }
  // calibrated permanent passives (gear / keystone / elemental mastery the harness user lacks; fitted to logs)
  for (const [side, u] of [[req.me, meU], [req.him, himU]] as const) {
    for (const p of side.passives ?? []) {
      b.usersEffects.push(makeEffect(p.type, { power: p.power, powerPerLevel: 0, rounds: 99, calculation: "percentage" } as never, {
        id: effectId(), creatorId: u.userId, targetId: u.userId, level: 1, isNew: false, castThisRound: false,
        createdRound: req.round - 1, longitude: u.longitude, latitude: u.latitude, actionId: "passive", fromType: "jutsu",
      } as never));
    }
  }
  b.activeUserId = meU.userId;
  meU.actionPoints = req.me.ap ?? 100;
  himU.actionPoints = 0;
  void uidOf;
  return b;
};

const hpOf = (b: CompleteBattle, cid: string) => Math.round(I.hp(b, cid));

const fire = (b: CompleteBattle, cid: string, acts: any[], defaultTarget: { x: number; y: number }) => {
  let cur = b;
  for (let i = 0; i < acts.length; i++) {
    const a = acts[i];
    let at = a.x === undefined ? defaultTarget : { x: a.x, y: a.y };
    if (a.x === undefined) {
      // self-targeted actions aim at the actor's own tile
      const actor = cur.usersState.find((u) => u.controllerId === cid)!;
      const act0 = I.actionList(cur, cid).find((x: any) => x.id === a.actionId);
      const rec = [...((actor as any).jutsus ?? []).map((j: any) => j.jutsu), ...((actor as any).items ?? []).map((j: any) => j.item)]
        .find((r: any) => r?.id === a.actionId);
      if ((rec && rec.target === "SELF") || ["defensiveStance", "offensiveStance", "basicHeal", "meditate", "cleanse"].includes(a.actionId))
        at = { x: actor.longitude, y: actor.latitude };
      void act0;
    }
    let r: any;
    try {
      r = I.act(cur, cid, a.actionId, at);
    } catch (err) {
      return { ok: false, failedAt: i, reason: String((err as Error).message).slice(0, 160), battle: cur };
    }
    if (!r.ok) return { ok: false, failedAt: i, reason: r.reason, battle: cur };
    cur = r.battle;
    if (hpOf(cur, req.me.id) <= 0 || hpOf(cur, req.him.id) <= 0) break;
  }
  return { ok: true, battle: cur };
};

const main = async () => {
  const base = await S.withSeed(7, prepare);
  if (process.env.TNR_LIST_ACTIONS) {
    for (const cid of [req.me.id, req.him.id]) {
      const b = structuredClone(base);
      b.activeUserId = I.uid(b, cid);
      console.error(cid, JSON.stringify(I.actionList(b, cid).map((a: any) => a.name)));
    }
  }
  const out: any[] = [];
  for (const cand of req.candidates) {
    const res: any = { bundle: cand.map((a: any) => a.actionId) };
    await S.withSeed(11, async () => {
      const b0 = structuredClone(base);
      const mine = fire(b0, req.me.id, cand, { x: req.him.x, y: req.him.y });
      res.legal = mine.ok;
      if (!mine.ok) { res.failedAt = mine.failedAt; res.reason = mine.reason; return; }
      const b1 = mine.battle;
      res.afterMe = { me: hpOf(b1, req.me.id), him: hpOf(b1, req.him.id) };
      res.replies = [];
      if (res.afterMe.him <= 0 || res.afterMe.me <= 0) return;
      for (const rep of req.replies) {
        const b2 = structuredClone(b1);
        if (req.hisTurn === "next") I.nextRound(b2);
        const himU = b2.usersState.find((u) => u.controllerId === req.him.id)!;
        const meU = b2.usersState.find((u) => u.controllerId === req.me.id)!;
        b2.activeUserId = himU.userId;
        himU.actionPoints = 100;
        meU.actionPoints = 0;
        const meNow = { x: meU.longitude, y: meU.latitude };
        const his = fire(b2, req.him.id, rep.actions, meNow);
        res.replies.push({ name: rep.name, legal: his.ok, failedAt: (his as any).failedAt, me: hpOf(his.battle, req.me.id), him: hpOf(his.battle, req.him.id) });
      }
    });
    out.push(res);
  }
  if (skipped.length) console.error("skipped effects:", JSON.stringify(skipped));
  process.stdout.write(JSON.stringify(out));
};

main().catch((e) => { console.error(String(e?.message ?? e).slice(0, 800), String(e?.stack ?? "").slice(0, 1200)); process.exit(1); });
