import { it } from "bun:test";
import { writeFileSync, mkdirSync } from "node:fs";
import { assembleBattle, runFight, withSeed } from "./sim";
import { IDS, aiCopy, playerPolicy, playerUser, zombieProfile, type KitName } from "./fixtures";
const OUT = process.env.TNR_OUT ?? "/tmp/claude-0/zombie_sim";
it("Zombie O sample fight (m_sW9: one Zombie Villager, scaled to the player)", async () => {
  const out: any[] = [];
  for (const kit of ["basic", "strong"] as KitName[])
    for (const band of [1, 0.6])
      for (const level of [10, 15, 25, 40, 60, 100])
        for (let s = 0; s < 4; s++) {
          const pol = playerPolicy(kit);
          const p = playerUser(level, band, kit, pol);
          const e = aiCopy(IDS.villager, 1, zombieProfile());
          const r = await withSeed(500 + s, async () => {
            const b = await assembleBattle({ users: [p, e], placements: [], autoCombatUserIds: ["player"], scaleTarget: true });
            for (const u of b.usersState) { u.latitude = 4; u.longitude = u.controllerId === "player" ? 1 : b.width - 2; }
            return runFight(b, { playerIds: ["player"], bossIds: [e.userId], maxRounds: 150, seed: 500 + s });
          });
          const claws = r.log.filter((x) => x.actionName === "Zombie Claws").length;
          out.push({ kit, band, level, seed: s, winner: r.winner, rounds: r.measuredRounds, clawHits: claws,
            playerEnd: Math.round(r.final.player!.curHealth), playerMax: r.final.player!.maxHealth });
        }
  mkdirSync(OUT, { recursive: true });
  writeFileSync(`${OUT}/zombieo_sample.json`, JSON.stringify(out, null, 1));
}, 1_700_000);
