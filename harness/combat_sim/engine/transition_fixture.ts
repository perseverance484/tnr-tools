/**
 * Transition fixture (review item 9): text the engine emits at a round transition (alignBattle's expired effects)
 * must land in the step's history texts, in router order, and its HP change in the step's HP delta.
 *
 * The fixture gives the player a Curse with 1 round left and 50 HP stored, on a player missing 100 HP. When the
 * round advances, alignBattle pays the Curse ("<name>'s Curse expires and restores N HP", N >= 50).
 *
 *   run.sh transition_fixture.ts      (exits 1 on failure)
 */
import { join } from "node:path";
import { enemyRow, loadLibrary, playerRow } from "./model";
import { assemble, runFight, seedRun } from "./sim";

const lib = loadLibrary([join(process.env.TNR_HARNESS!, "data/live/2026-11-18")]);
const S = "pz4azy5M6ZYJiwURtKZjp"; // Rogue Shinobi
const rows = Object.fromEntries(Object.keys(lib.ai).map((id) => [id, enemyRow(lib, id)]));
seedRun(3);
const p = playerRow(lib, { name: "Genin", level: 15, rank: "GENIN", jutsu: [{ id: "EOMOSOVn3za-UddIC2hY9", level: 8 }] }, 0, lib.ai[S]);
const b: any = await assemble({ players: [p], enemyRows: rows, waves: [{ aiIds: [S], delayRounds: 0 }], mode: "dungeon", runtime: lib.runtime });
const me = b.usersState.find((u: any) => u.username === "Genin");
me.curHealth -= 100;
b.usersEffects.push({
  id: "fixture-curse", type: "curse", creatorId: me.userId, targetId: me.userId, villageId: me.villageId, level: 1,
  rounds: 1, createdRound: 0, castThisRound: false, isNew: false, power: 20, powerPerLevel: 0, calculation: "percentage",
  damageBonusPercent: 0, direction: "offence", fromType: "jutsu", description: "fixture", target: "SELF",
  curseState: { storedHealing: 50, activatedRound: 0, ready: true, settled: false },
});
const run = runFight(b, { maxRounds: 3, policy: { dodge: false } });
const re = /^Genin's Curse expires and restores ([\d.]+) HP$/;
const hits = run.steps.filter((s) => s.texts.some((t) => re.test(t)));
const step = hits[0];
const line = step?.texts.find((t) => re.test(t));
const healed = line ? Number(line.match(re)![1]) : NaN;
// The action's own lines sit as one block inside the entry; the transition line sits outside that block.
const block = step ? step.texts.findIndex((_, i) => step.actionTexts.every((t, k) => step.texts[i + k] === t)) : -1;
const ok = {
  curseLineRecorded: hits.length === 1,
  inARecordedEntry: !!step && step.description !== null,
  notPartOfTheAction: !!step && !!line && !step.actionTexts.includes(line),
  actionLinesContiguous: !!step && (step.actionTexts.length === 0 || block >= 0),
  storedHealingPaid: healed >= 50, // 50 stored, plus what the curse stored from the first round's damage
  healInHpDelta: !!step && Math.abs((step.hp["Genin"] ?? 0) - healed) < 0.01,
};
console.log(JSON.stringify({ step: step ? { round: step.round, actor: step.actor, texts: step.texts, actionTexts: step.actionTexts, hp: step.hp } : null, ...ok }, null, 1));
if (!Object.values(ok).every(Boolean)) process.exit(1);
