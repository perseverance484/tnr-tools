/**
 * Player-strength calibration: one level-100 player vs The Captain, solo, as a plain QUEST battle
 * (initiateBattle without coop/waves: processUsersForBattle for both, no stat scaling of the
 * target, the player acts first). Live anchor (director, 2026-10-28): good players beat the
 * captured Captain solo in 8-10 rounds, some fewer, and it is a tough fight.
 *
 *   TNR_SCRIPT=calibrate.ts run.sh [--ladder ladder.json] [--seeds 60] [--seed 1]
 *        [--dmg-config live|default|file] [--out results/calibration.json]
 *
 * A ladder file is {"<name>": {<PlayerVariant fields>}, ...}; each entry starts from the built-in tier of the same name, else from the "cap"
 * tier (JONIN caps, standard kit at level 25) so only the gear stand-in knobs need be given:
 * poolsMultiplier, damageTakenReductionPct, damageGivenPct. Without --ladder, the built-in
 * calibrated tiers (weak/average/good) and the earlier ladder are measured.
 */
import { mkdirSync, writeFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { buildTemplates, enemyQueryUser, loadDmgConfig, loadJson, PLAYER_VARIANTS, type PlayerVariant, playerQueryUser } from "./model";
import { assembleFloor, mulberry32, runFloor } from "./sim";

const args = process.argv.slice(2);
const opt = (k: string, d?: string) => {
  const i = args.indexOf(`--${k}`);
  return i >= 0 ? args[i + 1] : d;
};
const H = process.env.TNR_HARNESS!;
const t = buildTemplates(loadJson(join(H, "data/baseline.json")), {});
const dmg = loadDmgConfig(H, opt("dmg-config", "live"));
const seeds = Number(opt("seeds", "60"));
const seed0 = Number(opt("seed", "1"));
const captainId = Object.keys(t.enemies).find((id) => t.enemies[id]!.row.username === "The Captain")!;
const rows = Object.fromEntries(Object.entries(t.enemies).map(([id, e]) => [id, enemyQueryUser(e)]));
const donor = t.enemies["texZaFi42S3EvJZBwQ8cd"]!.row;
const ladderPath = opt("ladder");
const ladder: Record<string, Partial<PlayerVariant>> = ladderPath
  ? loadJson(resolve(ladderPath))
  : Object.fromEntries(["average", "noarmor", "cap", "geared", "strong", "elite"].filter((n) => PLAYER_VARIANTS[n]).map((n) => [n, PLAYER_VARIANTS[n]!]));

const median = (xs: number[]) => {
  if (!xs.length) return null;
  const s = [...xs].sort((a, b) => a - b);
  const m = Math.floor(s.length / 2);
  return s.length % 2 ? s[m]! : (s[m - 1]! + s[m]!) / 2;
};
const pct = (xs: number[], p: number) => {
  if (!xs.length) return null;
  const s = [...xs].sort((a, b) => a - b);
  return s[Math.min(s.length - 1, Math.floor(p * (s.length - 1) + 0.5))]!;
};
const r1 = (x: number | null) => (x === null ? null : Math.round(x * 10) / 10);

const out: any[] = [];
for (const [name, partial] of Object.entries(ladder)) {
  const v = { ...(PLAYER_VARIANTS[name] ?? PLAYER_VARIANTS.cap!), ...partial, name } as PlayerVariant;
  let inBattle: any = null;
  const fights: { seed: number; won: boolean; rounds: number; playerHpPct: number; captainHpPct: number }[] = [];
  for (let i = 0; i < seeds; i++) {
    const seed = seed0 + i;
    const rand = mulberry32(seed);
    const orig = Math.random;
    Math.random = rand;
    try {
      const player = playerQueryUser(0, v, donor, t.jutsu);
      const battle = await assembleFloor({
        players: [player], enemyRows: rows, floor: { kind: "floor", waves: [{ aiIds: [captainId], delayRounds: 0 }] },
        rand, initialBarriers: true, dmgConfig: dmg.config, mode: "quest",
      });
      if (i === 0) {
        const pu = battle.usersState.find((u) => u.userId === player.userId)!;
        inBattle = {
          jutsuLoaded: pu.jutsus.map((j: any) => `${t.jutsu[j.jutsuId]?.name ?? j.jutsuId}@${j.level}`),
          jutsuDropped: player.jutsus.filter((j: any) => !pu.jutsus.some((x: any) => x.jutsuId === j.jutsuId)).map((j: any) => j.jutsu.name),
          maxHealth: pu.maxHealth, offence: pu.offence, defence: pu.defence,
          preBattleGearModifiers: (battle.extraState as any).preBattleGearModifiers?.[player.userId],
          itemEffects: battle.usersEffects.filter((e) => e.targetId === player.userId).map((e: any) => `${e.fromType}:${e.type} ${e.power}${e.calculation === "percentage" ? "%" : ""} r${e.rounds}`),
        };
      }
      const res = runFloor(battle, { playerIds: [player.userId], maxRounds: 60 });
      if (args.includes("--trace") && i === 0) {
        console.log(`--- trace ${name} seed ${seed}: ${res.outcome} in ${res.rounds} rounds`);
        for (const st of res.steps)
          console.log(`  r${st.round} ${st.human ? "player " : "captain"} ${(t.jutsu[st.actionId ?? ""]?.name ?? st.actionId ?? "-").padEnd(24)} rule ${st.ruleIndex ?? "-"} ${Object.values(st.hp).map((h) => Math.round(h)).join(" ")} ${st.effects.map((e) => e.type).join(",")}`);
      }
      const p = res.final[player.userId]!;
      const cap = Object.entries(res.final).find(([uid]) => uid !== player.userId)![1];
      fights.push({
        seed, won: res.outcome === "won", rounds: res.rounds,
        playerHpPct: (100 * Math.max(0, p.hp)) / p.maxHp, captainHpPct: (100 * Math.max(0, cap.hp)) / cap.maxHp,
      });
    } finally {
      Math.random = orig;
    }
  }
  const wins = fights.filter((f) => f.won);
  const losses = fights.filter((f) => !f.won);
  const row = {
    tier: name,
    knobs: { poolsMultiplier: v.poolsMultiplier, damageTakenReductionPct: v.damageTakenReductionPct, damageGivenPct: v.damageGivenPct, hp: Math.round(5050 * v.poolsMultiplier) },
    inBattle, seeds, winPct: r1((100 * wins.length) / seeds),
    winRoundsMedian: median(wins.map((f) => f.rounds)), winRoundsP10: pct(wins.map((f) => f.rounds), 0.1), winRoundsP90: pct(wins.map((f) => f.rounds), 0.9),
    winEndHpPctMedian: r1(median(wins.map((f) => f.playerHpPct))), winEndHpPctP10: r1(pct(wins.map((f) => f.playerHpPct), 0.1)), winEndHpPctP90: r1(pct(wins.map((f) => f.playerHpPct), 0.9)),
    lossRoundsMedian: median(losses.map((f) => f.rounds)), lossCaptainHpLeftPctMedian: r1(median(losses.map((f) => f.captainHpPct))),
    fights,
  };
  out.push(row);
  const { fights: _f, ...show } = row;
  console.log(JSON.stringify(show));
}
const outPath = opt("out");
if (outPath) {
  mkdirSync(dirname(resolve(outPath)), { recursive: true });
  writeFileSync(resolve(outPath), `${JSON.stringify({ generatedBy: "engine/calibrate.ts", scenario: "solo level-100 player vs The Captain (captured live record, push/249), plain QUEST battle", anchor: "director 2026-10-28: good players win in 8-10 rounds, some fewer; tough fight, end HP depends on build", dmgConfig: dmg.name, dmgConfigValues: dmg.config ?? null, seeds, seed0, tiers: out }, null, 1)}\n`);
  console.log(`wrote ${outPath}`);
}
