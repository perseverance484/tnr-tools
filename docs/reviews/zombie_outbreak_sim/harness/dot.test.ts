import { it } from "bun:test";
import { assembleBattle, runFight, withSeed } from "./sim";
import { IDS, aiCopy, playerPolicy, playerUser, zombieProfile } from "./fixtures";
import { performAIaction } from "@/libs/combat/ai_v2";
import { alignBattle, getBattleGrid } from "@/libs/combat/util";
it("claws DoT persistence", async () => {
  const p = playerUser(40, 1, "basic", playerPolicy("basic"));
  const e = aiCopy(IDS.villager, 1, zombieProfile());
  await withSeed(3, async () => {
    let b = await assembleBattle({ users: [p, e], placements: [], autoCombatUserIds: ["player"], scaleTarget: true });
    for (const u of b.usersState) { u.latitude = 4; u.longitude = u.controllerId === "player" ? 1 : 3; }
    const grid = getBattleGrid(1, b); const ar: number[] = [];
    for (let i = 0; i < 40; i++) {
      const pre = alignBattle(b, ar, "player"); if (!ar.includes(pre.actionRound)) ar.push(pre.actionRound);
      const pl = b.usersState.find((u) => u.controllerId === "player")!;
      const dots = b.usersEffects.filter((x) => x.targetId === pl.userId && x.type === "damage");
      if (pre.actor.controllerId === "player") console.log("round", b.round, "player hp", Math.round(pl.curHealth), "damage effects on player:", dots.length, "rounds fields:", dots.map((d) => d.rounds));
      if (pl.curHealth <= 0) break;
      b = performAIaction(b, grid, pre.actor.userId).nextBattle; alignBattle(b, ar, "player");
    }
  });
}, 600000);
