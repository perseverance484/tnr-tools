/** Calibration: scale the sim player's damage (gear stand-in damageGivenPct) until it kills Isonade v3 like dauntless did live (12 rounds). Offline. */
import { readFileSync } from "node:fs";
import { ISO_DEFAULTS, runFight } from "./isonade";
import { PLAYER_VARIANTS } from "./model";
import { opt } from "./cclib";
const P = { ...ISO_DEFAULTS, ...JSON.parse(readFileSync(opt("params")!, "utf8")), playerPoolPolicy: "good" };
const seeds = Number(opt("seeds", "4"));
for (const dg of opt("dg", "0,80,120")!.split(",").map(Number)) {
  (PLAYER_VARIANTS.average as any).damageGivenPct = dg;
  const fs = [];
  for (let s = 1; s <= seeds; s++) fs.push(await runFight(P as any, s, 1, {}));
  const w = fs.filter((f) => f.outcome === "won");
  console.log(JSON.stringify({ dg, wins: w.length, of: fs.length, rounds: fs.map((f) => f.rounds), hp: fs.map((f) => f.playerHpPct), boss: fs.map((f) => f.bossHpPct) }));
}
