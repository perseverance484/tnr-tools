/**
 * Vanquish the Horde: simulated pyramid runs through the real engine (assembly + ai_v2 + alignBattle),
 * both sides on the engine's auto-combat selector. Output: TNR_OUT/pyramid_runs.json.
 */
import { describe, it, expect } from "bun:test";
import { writeFileSync, mkdirSync } from "node:fs";
import { assembleBattle, runFight, withSeed } from "./sim";
import {
  IDS, PLAYER_KITS, aiCopy, liveQuest, patientZeroProfile, playerPolicy, playerUser, zombieProfile,
  type KitName,
} from "./fixtures";

const OUT = process.env.TNR_OUT ?? "/tmp/claude-0/zombie_sim";
const LEVELS = (process.env.SIM_LEVELS ?? "25,30,40,60,100").split(",").map(Number);
const BANDS = (process.env.SIM_BANDS ?? "1,0.6").split(",").map(Number);
const KITS = (process.env.SIM_KITS ?? "basic,strong").split(",") as KitName[];
const MODES = (process.env.SIM_MODES ?? "live,after403,after403+claws").split(",");
const SEEDS = Number(process.env.SIM_SEEDS ?? 6);
const MAX_ROUNDS = Number(process.env.SIM_MAX_ROUNDS ?? 30);

/** Stage list: fight objective, its retry budget on the live quest, label. */
const STAGES = [
  { id: "FgBZU", tries: 3, label: "Wave 1" },
  { id: "xrTWj", tries: 3, label: "Wave 2" },
  { id: "QcCtW", tries: 2, label: "Wave 3" },
  { id: "UlQqE", tries: 2, label: "Boss" },
];

const ONLY = process.env.SIM_STAGES?.split(",");
const quest = liveQuest();
const objective = (id: string) => quest.content.objectives.find((o: any) => o.id === id);
const zProf = zombieProfile();
const pzProf = patientZeroProfile();

const enemiesFor = (stageId: string, claws: boolean) => {
  const ids: string[] = objective(stageId).opponentAIs.flatMap((o: any) => Array(o.number).fill(o.ids).flat());
  const count: Record<string, number> = {};
  return ids.map((tid) => {
    count[tid] = (count[tid] ?? 0) + 1;
    return aiCopy(tid, count[tid], tid === IDS.patientZero ? pzProf : zProf, claws);
  });
};

const placements = (users: any[], width: number, height: number) => {
  const out = [{ userId: users[0].userId, x: 1, y: Math.floor(height / 2) }];
  users.slice(1).forEach((u, i) => {
    const col = width - 2 - Math.floor(i / height);
    const row = (Math.floor(height / 2) + (i % 2 ? -1 : 1) * Math.ceil((i % height) / 2) + height) % height;
    out.push({ userId: u.userId, x: col, y: row });
  });
  return out;
};

type Pools = { hp: number; cp: number; sp: number } | null;

const fightOnce = async (level: number, band: number, kit: KitName, stage: (typeof STAGES)[number], scale: boolean, claws: boolean, pools: Pools, seed: number) => {
  const pol = playerPolicy(kit);
  const player = playerUser(level, band, kit, pol);
  if (pools) Object.assign(player, { curHealth: pools.hp, curChakra: pools.cp, curStamina: pools.sp });
  const enemies = enemiesFor(stage.id, claws);
  const users = [player, ...enemies];
  return withSeed(seed, async () => {
    const battle = await assembleBattle({
      users, placements: [], autoCombatUserIds: ["player"], scaleTarget: scale,
    });
    const pl = placements(battle.usersState, battle.width, battle.height);
    for (const u of battle.usersState) {
      const p = pl.find((x) => x.userId === u.controllerId);
      if (p) { u.longitude = p.x; u.latitude = p.y; }
    }
    const enemyIds = battle.usersState.filter((u) => u.controllerId !== "player").map((u) => u.controllerId);
    const res = runFight(battle, { playerIds: ["player"], bossIds: enemyIds, maxRounds: MAX_ROUNDS, seed });
    const me = res.final.player!;
    const enemyStats = battle.usersState.filter((u) => u.controllerId !== "player").map((u) => ({
      name: u.username, level: u.level, rank: u.rank, hp: u.maxHealth, offence: Math.round(u.offence), defence: Math.round(u.defence),
    }));
    const pz = res.log.filter((r) => r.actor.startsWith(IDS.patientZero));
    return {
      winner: res.winner, rounds: res.measuredRounds, end: { hp: me.curHealth, maxHp: me.maxHealth, cp: me.curChakra, sp: me.curStamina },
      playerStart: { hp: battle.usersState.find((u) => u.controllerId === "player")!.curHealth, offence: Math.round(player.offence), defence: Math.round(player.defence) },
      enemies: enemyStats,
      patientZeroActions: pz.reduce((m: Record<string, number>, r) => { const k = r.actionName ?? "(none)"; m[k] = (m[k] ?? 0) + 1; return m; }, {}),
      idle: res.idleTimeouts,
    };
  });
};

describe("Vanquish the Horde simulated runs", () => {
  it("runs every configuration", async () => {
    mkdirSync(OUT, { recursive: true });
    const runs: any[] = [];
    for (const mode of MODES)
      for (const kit of KITS)
        for (const band of BANDS)
          for (const level of LEVELS)
            for (let s = 0; s < SEEDS; s++) {
              const seed = 1000 + s;
              let pools: Pools = null;
              const stages: any[] = [];
              let cleared = true;
              for (const [si, st] of STAGES.entries()) {
                if (ONLY && !ONLY.includes(st.label)) continue;
                const scale = mode.startsWith("after403") ? true : !!objective(st.id).opponent_scaled_to_user;
                const claws = mode.endsWith("+claws");
                const attempts: any[] = [];
                let won = false;
                for (let t = 0; t < st.tries && !won; t++) {
                  // A loss sends the player to hospital; the retry starts healed (full pools).
                  const r = await fightOnce(level, band, kit, st, scale, claws, t === 0 ? pools : null, seed * 10 + si * 3 + t);
                  attempts.push(r);
                  won = r.winner === "player";
                  if (won) pools = { hp: r.end.hp, cp: r.end.cp, sp: r.end.sp };
                }
                stages.push({ stage: st.label, scaled: scale, claws, attempts });
                if (!won) { cleared = false; break; }
              }
              runs.push({ mode, kit, band, level, seed, cleared, stages });
            }
    writeFileSync(`${OUT}/pyramid_runs.json`, JSON.stringify({ quest: IDS.voth, maxRounds: MAX_ROUNDS, runs }, null, 1));
    expect(runs.length).toBeGreaterThan(0);
  }, 3_600_000);
});
