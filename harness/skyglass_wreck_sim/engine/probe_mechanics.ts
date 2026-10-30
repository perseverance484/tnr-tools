/**
 * Mechanics probes (offline, engine-executed): can an AI enemy use movement, summon, ground-AOE,
 * barrier and clone jutsu, and what happens? Each scenario is one plain QUEST battle: one
 * "average" player vs one probe enemy (Deck Warden row; kit = the probe jutsu only; rule 0 casts it
 * at the given target; includeDefaultRules true so the engine's fallbacks still apply).
 *
 *   TNR_SCRIPT=probe_mechanics.ts run.sh [--seeds 3] [--rounds 6] [--only A1,B1] [--out results/probe_mechanics.json]
 *
 * All probe jutsu are real captured records (path printed); the summon probes copy the captured
 * "Summoning: Hell Hound" record and point its aiId at a captured hazard AI (Seal Charge /
 * Core Canister), as the director asked.
 */
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { buildTemplates, enemyQueryUser, loadDmgConfig, loadJson, PLAYER_VARIANTS, playerQueryUser } from "./model";
import { assembleFloor, mulberry32, runFloor } from "./sim";

const args = process.argv.slice(2);
const opt = (k: string, d?: string) => {
  const i = args.indexOf(`--${k}`);
  return i >= 0 ? args[i + 1] : d;
};
const H = process.env.TNR_HARNESS!;
const REPO = process.env.TNR_REPO!;
const seeds = Number(opt("seeds", "3"));
const rounds = Number(opt("rounds", "6"));
const only = opt("only")?.split(",");

/** Newest captured copy of a jutsu record from the given harvest files. */
const findJutsu = (id: string, files: string[]) => {
  let best: any = null;
  let src = "";
  const walk = (x: any, f: string) => {
    if (Array.isArray(x)) x.forEach((v) => walk(v, f));
    else if (x && typeof x === "object") {
      if (x.id === id && "jutsuType" in x && "effects" in x && (!best || (x.updatedAt ?? "") > (best.updatedAt ?? ""))) {
        best = x;
        src = f;
      }
      Object.values(x).forEach((v) => walk(v, f));
    }
  };
  for (const f of files) walk(JSON.parse(readFileSync(join(REPO, f), "utf8")), f);
  if (!best) throw new Error(`jutsu ${id} not found in ${files.join(", ")}`);
  return { record: best, source: src };
};
const F1 = "harvests/inbox/tnr_results_1792732003454.json";
const F2 = "harvests/inbox/tnr_results_1792780147534.json";
const J = {
  replacement: findJutsu("clh4d6pok0002tb0hx1bxro6l", [F2]),
  bodyFlicker: findJutsu("y39RtS7NN7TdqOgyT52gr", [F1]),
  hellHound: findJutsu("kP_KMs7H9wQJwRHeaTGCZ", [F1]),
  drowningMire: findJutsu("VmZzkyfPswbJLXvuB-mcV", [F1]),
  fortress: findJutsu("i4lGrYY5HNN2Q2GPToKUS", [F1]),
  clone: findJutsu("clh4d6phm0000tb0h7wo71p2z", [F1]),
};
const SEAL_CHARGE = "wTgO-Q32caSSd0is1QIS7";
const CORE_CANISTER = "frc9LTxqQlM7mncG4VZGK";
const summonCopy = (aiId: string, name: string) => {
  const r = structuredClone(J.hellHound.record);
  r.id = `probe-summon-${name}`;
  r.name = `Hell Hound summon -> ${name}`;
  r.effects = r.effects.map((e: any) => (e.type === "summon" ? { ...e, aiId } : e));
  return r;
};

type Scenario = {
  key: string; question: string; jutsu: any; target: string;
  /** Player behaviour: "kit" (normal rotation), "stay" (always ends turn), "walk" (stays through round 2, then walks toward tile 1,8). */
  player: "kit" | "stay" | "walk";
  coordinateOnPlayer?: boolean;
  /** Optional cast gate (distance to the player) so the enemy first walks into range. */
  within?: number;
};
const S: Scenario[] = [
  { key: "A1", question: "movement jutsu (Replacement Technique) at EMPTY_GROUND_CLOSEST_TO_OPPONENT", jutsu: J.replacement.record, target: "EMPTY_GROUND_CLOSEST_TO_OPPONENT", player: "stay" },
  { key: "A2", question: "movement jutsu (Replacement Technique) at CLOSEST_OPPONENT", jutsu: J.replacement.record, target: "CLOSEST_OPPONENT", player: "stay" },
  { key: "A3", question: "movement+damage jutsu (Body Flicker) at EMPTY_GROUND_CLOSEST_TO_OPPONENT", jutsu: J.bodyFlicker.record, target: "EMPTY_GROUND_CLOSEST_TO_OPPONENT", player: "stay" },
  { key: "A4", question: "movement+damage jutsu (Body Flicker) at CLOSEST_OPPONENT", jutsu: J.bodyFlicker.record, target: "CLOSEST_OPPONENT", player: "stay" },
  { key: "B1", question: "summon (Hell Hound record, aiId -> Seal Charge) at EMPTY_GROUND_CLOSEST_TO_OPPONENT", jutsu: summonCopy(SEAL_CHARGE, "SealCharge"), target: "EMPTY_GROUND_CLOSEST_TO_OPPONENT", player: "stay" },
  { key: "B2", question: "summon (Hell Hound record, aiId -> Core Canister) at EMPTY_GROUND_CLOSEST_TO_OPPONENT", jutsu: summonCopy(CORE_CANISTER, "CoreCanister"), target: "EMPTY_GROUND_CLOSEST_TO_OPPONENT", player: "stay" },
  { key: "C1", within: 4, question: "ground AOE poison/damage (Drowning Mire: damage 15 + IDT 15, 2 rounds) at EMPTY_GROUND_CLOSEST_TO_OPPONENT, player stays", jutsu: J.drowningMire.record, target: "EMPTY_GROUND_CLOSEST_TO_OPPONENT", player: "stay" },
  { key: "C2", within: 4, question: "ground AOE (Drowning Mire: damage 15 + IDT 15, 2 rounds) at COORDINATE = the player's tile, player stays", jutsu: J.drowningMire.record, target: "COORDINATE", player: "stay", coordinateOnPlayer: true },
  { key: "C3", within: 4, question: "ground AOE (Drowning Mire: damage 15 + IDT 15, 2 rounds) at COORDINATE = the player's tile, player walks off", jutsu: J.drowningMire.record, target: "COORDINATE", player: "walk", coordinateOnPlayer: true },
  { key: "D1", within: 2, question: "barrier wall (Adamantine Fortress) at EMPTY_GROUND_CLOSEST_TO_OPPONENT, player uses its normal kit/profile", jutsu: J.fortress.record, target: "EMPTY_GROUND_CLOSEST_TO_OPPONENT", player: "kit" },
  { key: "E1", question: "clone (Clone Technique) at EMPTY_GROUND_CLOSEST_TO_OPPONENT", jutsu: J.clone.record, target: "EMPTY_GROUND_CLOSEST_TO_OPPONENT", player: "stay" },
];

const baseline = loadJson(join(H, "data/baseline.json"));
const dmg = loadDmgConfig(H, "live");
const out: any[] = [];
for (const sc of S) {
  if (only && !only.includes(sc.key)) continue;
  const rule = { conditions: sc.within ? [{ type: "distance_lower_than", value: sc.within, target: "CLOSEST_OPPONENT", description: "" }] : [], action: { type: "use_specific_jutsu", jutsuId: sc.jutsu.id, target: sc.target, description: "", ...(sc.target === "COORDINATE" ? { coordinates: { longitude: 0, latitude: 0 } } : {}) } };
  const ov = {
    jutsu: { [sc.jutsu.id]: sc.jutsu },
    newEnemies: { probe: { base: "Deck Warden", username: `Probe ${sc.key}`, jutsuIds: [sc.jutsu.id], rules: [rule], includeDefaultRules: true } },
  };
  const t = buildTemplates(baseline, ov as never);
  const rows = Object.fromEntries(Object.entries(t.enemies).map(([id, e]) => [id, enemyQueryUser(e)]));
  const playerRulesFor = {
    kit: undefined,
    stay: [{ conditions: [], action: { type: "end_turn", description: "" } }],
    // Stays through round 2 (the cast round in these seeds), then walks off toward a far tile.
    walk: [
      { conditions: [{ type: "round_greater_than", value: 2, description: "" }], action: { type: "move_towards_opponent", target: "COORDINATE", coordinates: { longitude: 1, latitude: 8 }, description: "" } },
      { conditions: [], action: { type: "end_turn", description: "" } },
    ],
  }[sc.player];
  const v = { ...PLAYER_VARIANTS.average!, ...(playerRulesFor ? { rules: playerRulesFor } : {}) };
  const donor = t.enemies["texZaFi42S3EvJZBwQ8cd"]!.row;
  const runs: any[] = [];
  for (let seed = 1; seed <= seeds; seed++) {
    const rand = mulberry32(seed);
    const orig = Math.random;
    Math.random = rand;
    try {
      const player = playerQueryUser(0, v as never, donor, t.jutsu);
      const b = await assembleFloor({
        players: [player], enemyRows: rows, floor: { kind: "floor", waves: [{ aiIds: ["probe"], delayRounds: 0 }] },
        rand, initialBarriers: false, dmgConfig: dmg.config, mode: "quest",
      });
      const pu = b.usersState.find((u) => u.userId === player.userId)!;
      if (sc.coordinateOnPlayer) {
        const prof = Object.values<any>(b.extraState.aiProfiles ?? {}).find((p) => p.rules?.[0]?.action?.jutsuId === sc.jutsu.id);
        prof.rules[0].action.coordinates = { longitude: pu.longitude, latitude: pu.latitude };
      }
      const res = runFloor(b, { playerIds: [player.userId], maxRounds: rounds, detail: true });
      const names = new Map<string, string>([[player.userId, "player"]]);
      for (const w of res.waves) for (const e of w.enemies) names.set(e.uid, "probe");
      const log = res.steps.map((s) => {
        for (const n of s.newUnits ?? []) if (!names.has(n.uid)) names.set(n.uid, `${n.isSummon ? "summon" : "unit"}:${n.name}`);
        return {
          round: s.round, actor: names.get(s.actorUid) ?? s.actor,
          action: s.actionId === sc.jutsu.id ? sc.jutsu.name : s.actionId, rule: s.ruleIndex, authored: s.authoredRules,
          from: s.actorFrom, to: s.actorTo,
          hp: Object.fromEntries(Object.entries(s.hp).map(([k, d]) => [names.get(k) ?? k, Math.round(d)])),
          newUnits: s.newUnits?.map((n) => ({ ...n, uid: undefined, label: names.get(n.uid) })),
          newEffects: s.effects.map((e) => `${e.type}->${names.get(e.target) ?? e.target}`),
          ground: s.groundAfter,
        };
      });
      runs.push({ seed, outcome: res.outcome, rounds: res.rounds, playerStart: [pu.longitude, pu.latitude], log });
    } finally {
      Math.random = orig;
    }
  }
  const casts = runs.map((r) => r.log.filter((l: any) => l.actor === "probe" && l.action === sc.jutsu.name).length);
  out.push({ key: sc.key, question: sc.question, jutsu: { id: sc.jutsu.id, name: sc.jutsu.name, target: sc.jutsu.target, method: sc.jutsu.method, range: sc.jutsu.range, cooldown: sc.jutsu.cooldown, effects: sc.jutsu.effects.map((e: any) => ({ type: e.type, power: e.power, rounds: e.rounds, aiId: e.aiId })) }, ruleTarget: sc.target, player: sc.player, castsPerSeed: casts, runs });
  console.log(`\n### ${sc.key}: ${sc.question}\ncasts per seed: ${casts.join(", ")}`);
  for (const l of runs[0].log) {
    if (l.actor === "player" && l.action === "wait" && !Object.keys(l.hp).length) continue;
    console.log(`  r${l.round} ${String(l.actor).padEnd(26)} ${String(l.action).padEnd(32)} rule ${l.rule ?? "-"}/${l.authored} ${JSON.stringify(l.from)}->${JSON.stringify(l.to)} hp ${JSON.stringify(l.hp)}${l.newUnits?.length ? ` NEW ${JSON.stringify(l.newUnits)}` : ""}${l.newEffects.length ? ` fx ${l.newEffects.join(",")}` : ""}${l.ground?.length ? ` ground ${JSON.stringify(l.ground)}` : ""}`);
  }
}
const outPath = opt("out");
if (outPath) {
  mkdirSync(dirname(resolve(outPath)), { recursive: true });
  writeFileSync(resolve(outPath), `${JSON.stringify({ generatedBy: "engine/probe_mechanics.ts", sources: Object.fromEntries(Object.entries(J).map(([k, v]) => [k, `${v.record.name} (${v.record.id}) from ${v.source}`])), dmgConfig: dmg.name, probes: out }, null, 1)}\n`);
  console.log(`wrote ${outPath}`);
}
