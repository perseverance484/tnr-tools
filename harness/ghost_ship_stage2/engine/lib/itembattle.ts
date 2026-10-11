/**
 * Item-gate battle helpers: a human wielder (not auto-combat) acting through the
 * same path the combat router uses for a player action — availableUserActions →
 * performBattleAction — on a battle assembled by processUsersForBattle.
 */
import { availableUserActions, performBattleAction } from "@/libs/combat/actions";
import { alignBattle, getBattleGrid, isEffectActive } from "@/libs/combat/util";
import type { CompleteBattle, UserEffect } from "@/libs/combat/types";
import * as F from "./fixtures";
import * as S from "./sim";

export const caps = () => S.joninCaps();

/** A player-side user with no jutsu and a given item list (rows from items.userItemRow). */
export const wielder = (id: string, items: any[], jutsuIds: string[] = [], band: F.PlayerStatBand = "jonin-cap") => {
  const pol = { id: `policy::${id}`, userId: id, includeDefaultRules: false, rules: [] };
  const u = F.playerQueryUser(id, band, "striker", pol, caps());
  u.jutsus = jutsuIds.map((jid, i) => ({
    id: `uj-${id}-${i}`, userId: id, jutsuId: jid, level: 1, experience: 0, equipped: true,
    finishTraining: null, reskinId: null, jutsu: F.poolJutsuById(jid).record,
  }));
  u.items = items;
  return u;
};

/** Enemy target: upstream-helper band player in another village (no kit unless given). */
export const target = (id: string, jutsus: { record: any; level?: number }[] = []) => {
  const pol = { id: `policy::${id}`, userId: id, includeDefaultRules: false, rules: [] };
  const u = F.playerQueryUser(id, "upstream-helper", "striker", pol, caps());
  u.villageId = "village-enemy";
  u.jutsus = jutsus.map((j, i) => ({
    id: `uj-${id}-${i}`, userId: id, jutsuId: j.record.id, level: j.level ?? 1, experience: 0,
    equipped: true, finishTraining: null, reskinId: null, jutsu: j.record,
  }));
  return u;
};

export const build = (users: any[], placements: S.Placement[]) =>
  S.assembleBattle({ users, placements });

export const uid = (b: CompleteBattle, controllerId: string) =>
  b.usersState.find((u) => u.controllerId === controllerId)!.userId;

export const act = (b: CompleteBattle, actorCid: string, actionId: string, at: { x: number; y: number }) => {
  const actorId = uid(b, actorCid);
  const action = availableUserActions(b, actorId, true, true).find((a) => a.id === actionId);
  if (!action) return { ok: false as const, reason: "action not available", battle: b };
  const grid = getBattleGrid(1, b);
  const res = performBattleAction({ battle: b, action, grid, contextUserId: actorId, actorId, longitude: at.x, latitude: at.y });
  return { ok: true as const, battle: res.newBattle, effects: res.actionEffects, action };
};

export const actionList = (b: CompleteBattle, cid: string) =>
  availableUserActions(b, uid(b, cid), true, true).map((a) => ({ id: a.id, name: a.name, cooldown: a.cooldown, lastUsedRound: a.lastUsedRound }));

export const hp = (b: CompleteBattle, cid: string) => b.usersState.find((u) => u.controllerId === cid)!.curHealth;

export const shieldsOn = (b: CompleteBattle, cid: string): UserEffect[] =>
  b.usersEffects.filter((e) => e.type === "shield" && e.targetId === uid(b, cid) && (e.rounds === undefined || e.rounds > 0));

export const effectsOn = (b: CompleteBattle, cid: string, type: string) =>
  b.usersEffects.filter((e) => e.type === type && e.targetId === uid(b, cid));

/**
 * Advance to the next round the way the router does: exhaust every actor's AP
 * so alignBattle walks the turn ring and progresses the round counter (effect
 * rounds decrement, isNew/castThisRound reset).
 */
export const nextRound = (b: CompleteBattle) => {
  const start = b.round;
  for (let i = 0; i < 20 && b.round === start; i++) {
    b.usersState.forEach((u) => {
      u.actionPoints = 0;
    });
    alignBattle(b, [b.round], b.usersState[0]!.userId);
  }
  return b.round;
};

export const active = (e: UserEffect) => isEffectActive(e) && (e.rounds === undefined || e.rounds > 0);
