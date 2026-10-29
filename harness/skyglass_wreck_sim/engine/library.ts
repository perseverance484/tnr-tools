/**
 * The Skyglass set-piece library (docs/design/SKYGLASS_BOSS_FIGHTS.md section 5a): shared marks, shared blasts,
 * the bespoke signatures, the shared lowered guard and the crew additions. One record per jutsu, built on captured
 * shape donors and validated by the live JutsuValidator (kitlib). Every boss in the Wreck, the hunts and Crownhold
 * references these records by id; build_library.ts writes them to library_spec.json.
 *
 * Recipe (section 6, harness-confirmed): a mark is a 40 AP GROUND jutsu that lays a 1-round visual on the pattern and
 * puts its own primed-marker type on the caster; the matching blast (100 AP) fires on the caster's next turn when its
 * rule sees that marker (`has_effect <type> >= 1`). 40 AP leaves 60 for a plain attack or a 60 AP follow-up (the
 * two-marker chain) in the mark's turn, and never enough for a blast. Each mark has its own marker type, outside
 * SHARED_COOLDOWN_TAGS and with no gameplay effect on an AI boss, so any two marks coexist on one boss. Blasts that
 * stun, seal or push target CHARACTER (GROUND lands only damage); the scatter blasts stay GROUND so they leave a pool.
 */
import { getDefaultBattleSizes } from "@/libs/combat/util";
import { anim, copyJutsu, jutsu, T, tag } from "./kitlib";

const size = getDefaultBattleSizes("QUEST" as never, 100)!; // 12 x 10 at level >= 50
const W = size.width;
const H = size.height;
type XY = { longitude: number; latitude: number };
const cells = (pred: (c: number, r: number) => boolean) => {
  const out: XY[] = [];
  for (let c = 0; c < W; c++) for (let r = 0; r < H; r++) if (pred(c, r)) out.push({ longitude: c, latitude: r });
  return out;
};
const field = (selection: "ALL" | "EXCLUDE", coordinates: XY[], origin = "BATTLEFIELD") => ({ origin, selection, coordinates, randomCount: 1 });

/**
 * Engine grid (getBattleGrid: honeycomb-grid, Orientation.FLAT, checked with the engine's own grid.distance): FLAT-topped
 * hexes, odd columns shifted down. N/S neighbours are (0,-1)/(0,+1) in every column; the diagonal neighbours depend on
 * COLUMN parity:
 *   even column: NW (-1,-1) NE (+1,-1) SW (-1,0) SE (+1,0);  odd column: NW (-1,0) NE (+1,0) SW (-1,+1) SE (+1,+1).
 * There is no straight west direction; the hexes of one row, (-1,0), (-2,0), ..., form a zigzag line in which every hex
 * touches the next (W below). COORDINATES offsets are column/row, so a diagonal ray from a caster in an even column
 * differs from one in an odd column. `rayFrom` gives the exact ray for one starting column parity; the library records
 * use the union of both parities, so a boss in any column is covered (the diagonals are then two hexes wide on alternate
 * steps). The exact per-parity sets are exported too, for a boss that stands in a known column (a throne).
 * (Report 3 and library 5f6c3edb wrongly assumed pointy-topped rows; Lines and Seal Lines then ran near-vertical.)
 */
type Dir = "W" | "E" | "N" | "S" | "NW" | "NE" | "SW" | "SE";
const STEP: Record<Dir, [[number, number], [number, number]]> = {
  // [even-column step, odd-column step]
  W: [[-1, 0], [-1, 0]], E: [[1, 0], [1, 0]],
  N: [[0, -1], [0, -1]], S: [[0, 1], [0, 1]],
  NW: [[-1, -1], [-1, 0]], NE: [[1, -1], [1, 0]],
  SW: [[-1, 0], [-1, 1]], SE: [[1, 0], [1, 1]],
};
const rayFrom = (dir: Dir, len: number, startColParity: 0 | 1) => {
  const out: XY[] = [];
  let dc = 0;
  let dr = 0;
  for (let k = 1; k <= len; k++) {
    const colParity = (((startColParity + dc) % 2) + 2) % 2;
    const [sc, sr] = STEP[dir][colParity]!;
    dc += sc;
    dr += sr;
    out.push({ longitude: dc, latitude: dr });
  }
  return out;
};
const rays = (dirs: Dir[], len: number, parity: 0 | 1) => dirs.flatMap((d) => rayFrom(d, len, parity));
/** Offsets of every hex within `radius` of a caster in a column of the given parity (odd columns shifted down). */
const discFrom = (radius: number, parity: 0 | 1) => {
  const cube = (c: number, r: number) => {
    const z = r - (c - (c & 1)) / 2;
    return [c, z, -c - z];
  };
  const [ox, oy, oz] = cube(parity, 0);
  const out: XY[] = [];
  for (let dc = -radius; dc <= radius; dc++)
    for (let dr = -radius - 1; dr <= radius + 1; dr++) {
      const [x, y, z] = cube(parity + dc, dr);
      if (Math.max(Math.abs(x - ox), Math.abs(y - oy), Math.abs(z - oz)) <= radius) out.push({ longitude: dc, latitude: dr });
    }
  return out;
};
const NEIGHBOURS: Dir[] = ["N", "S", "NW", "NE", "SW", "SE"];
const ORIGIN: XY = { longitude: 0, latitude: 0 };
const notOrigin = (xs: XY[]) => xs.filter((x) => x.longitude !== 0 || x.latitude !== 0);
const uniq = (xs: XY[]) => [...new Map(xs.map((x) => [`${x.longitude},${x.latitude}`, x])).values()];

/** Patterns (all parity-safe). */
const STARS: XY[] = [{ longitude: 6, latitude: 2 }, { longitude: 5, latitude: 5 }, { longitude: 6, latitude: 8 }];
const isStar = (c: number, r: number) => STARS.some((x) => x.longitude === c && x.latitude === r);
const FAN: Dir[] = ["W", "NW", "SW"];
const CROSS: Dir[] = ["NW", "NE", "SW", "SE"];
export const PATTERNS = {
  rowsA: cells((_c, r) => r === 2 || r === 5),
  rowsB: cells((_c, r) => r === 3 || r === 6),
  /** Complementary halves: A and B together cover every hex except the three safe stars; every hex has a neighbour in the other half. */
  scatterA: cells((c, r) => ((c >> 1) + r) % 2 === 0 && !isStar(c, r)),
  scatterB: cells((c, r) => ((c >> 1) + r) % 2 === 1 && !isStar(c, r)),
  /** Fan of three rays west from the caster (W row zigzag, NW, SW; length 5), union of both column parities. */
  lines: uniq([...rays(FAN, 5, 0), ...rays(FAN, 5, 1)]),
  /** Diagonal cross (NW, NE, SW, SE; length 5), union of both column parities. */
  sealLines: uniq([...rays(CROSS, 5, 0), ...rays(CROSS, 5, 1)]),
  /** Minor marks (caster-anchored, so the marked hexes stay put until the blast): Splash = the hex two west of the
   * caster and its six neighbours (union of both column parities: a 3 x 3 block); Short line = the W row, 3 hexes. */
  splash: uniq([{ longitude: -2, latitude: 0 }, ...([0, 1] as const).flatMap((par) => NEIGHBOURS.map((d) => {
    const [dc, dr] = STEP[d][par]!;
    return { longitude: -2 + dc, latitude: dr };
  }))]),
  shortLine: rayFrom("W", 3, 0),
  /** Binding Ring / Ship's Bell: every hex within 2 of the caster in either column parity (caster excluded). The Bell's
   * blast adds the caster's own hex so the cast is valid even when everyone stepped off (it stays a CHARACTER jutsu for
   * its push and lock rows; its rows are enemies only, so the caster is untouched). */
  bindingRing: notOrigin(uniq([...discFrom(2, 0), ...discFrom(2, 1)])),
  /** Exact single-parity offset sets, for a boss on a known row. */
  linesByColumnParity: { even: rays(FAN, 5, 0), odd: rays(FAN, 5, 1) },
  sealLinesByColumnParity: { even: rays(CROSS, 5, 0), odd: rays(CROSS, 5, 1) },
  /** The three safe tiles of the arena-wide marks (columns <= 6, never under an east-side spawn). */
  stars: STARS,
};

/**
 * Primed-marker type per mark. All are outside SHARED_COOLDOWN_TAGS and change nothing for an AI boss: the cooldown and
 * range types list no actions; fleeprevent and robprevent guard things a boss never does; onehitkillprevent and
 * sealprevent only refuse an instant kill or a seal on the boss for that one round; disarm hides WEAPON items (bosses
 * carry none); elementalseal blocks elemental 60 AP jutsu (every library and boss jutsu is non-elemental); summonprevent
 * blocks a summon for that round (the Last Light users, the Core Horror and the Foundry Warden, summon nothing).
 * A visual on SELF was tried and rejected: it stayed on the caster a round too long and the blast fired twice.
 */
export const MARKER_TYPES = {
  ring: "increasecooldown",
  bindingRing: "decreasecooldown",
  rowsA: "increaserange",
  rowsB: "fleeprevent",
  scatterA: "robprevent",
  scatterB: "onehitkillprevent",
  lines: "disarm",
  sealLines: "elementalseal",
  lastLight: "summonprevent",
  lastLightBinding: "sealprevent",
  /** Minor marks for regular crew (RUL-2026-10-28-024). +1% heal given / 1% lifesteal on the caster for one round: no
   * library or Wreck crew record carries either type, and neither is a shared-cooldown or prevent type. */
  splash: "increaseheal",
  shortLine: "lifesteal",
} as const;
export type MarkKey = keyof typeof MARKER_TYPES;

// Prevent-style tags apply with probability power/100, so those markers carry power 100.
const markerTag = (type: string) =>
  ["increaseheal", "lifesteal"].includes(type)
    ? tag(type, { power: 1, rounds: 1, target: "SELF", calculation: "percentage" })
    : tag(type, {
        power: ["increasecooldown", "decreasecooldown", "increaserange"].includes(type) ? 1 : 100, rounds: 1, target: "SELF",
        ...(["increasecooldown", "decreasecooldown", "increaserange"].includes(type) ? { actionsAffected: [], calculation: "static" } : {}),
      });

/** Library ids (placeholders until the builder mints real ids). */
export const LIB = {
  mark: {
    ring: "lib-omen-ring", bindingRing: "lib-omen-binding-ring", rowsA: "lib-omen-rows-a", rowsB: "lib-omen-rows-b",
    scatterA: "lib-omen-scatter-a", scatterB: "lib-omen-scatter-b", lines: "lib-omen-lines", sealLines: "lib-omen-seal-lines",
    lastLight: "lib-omen-last-light", lastLightBinding: "lib-omen-last-light-binding",
    splash: "lib-omen-splash", shortLine: "lib-omen-short-line",
  } as Record<MarkKey, string>,
  blast: {
    ring: "lib-blast-ring", rowsA: "lib-blast-rows-a", rowsB: "lib-blast-rows-b", scatterA: "lib-blast-scatter-a",
    scatterB: "lib-blast-scatter-b", lines: "lib-blast-lines", sealLines: "lib-blast-seal-lines",
    splash: "lib-blast-splash", shortLine: "lib-blast-short-line",
  },
  sig: {
    maw: "lib-maw-of-the-deep", quench: "lib-quench", commandAbsolute: "lib-command-absolute", crownfall: "lib-crownfall",
    broadside: "lib-broadside", shipsBell: "lib-ships-bell",
  },
  loweredGuard: "lib-lowered-guard",
  crew: {
    chainHook: "lib-chain-hook", oath: "lib-oath-of-stillness", chartMark: "lib-chart-mark", aegis: "lib-skyglass-aegis",
    mending: "lib-mending-seal", ward: "lib-ward-of-command",
  },
  /** Phase transitions (RUL-2026-10-28-032). Steady the Helm: name approved in RUL-2026-10-29-045. */
  transition: {
    captain: "lib-steady-the-helm",
  },
  /** Skyglass-only copies of live jutsu (RUL-2026-10-28-026): used by the hunts / Crownhold instead of editing the
   * shared live record. */
  liveCopy: {
    stoneboundEruptingGround: "hunt-stonebound-erupting-ground",
  },
};
/** Which mark each blast or signature answers. */
/** Source and change of each Skyglass-only live copy. */
export const LIVE_COPY_SOURCE: Record<string, { liveId: string; liveName: string; change: string }> = {
  [LIB.liveCopy.stoneboundEruptingGround]: { liveId: "jBRyl7F4UjTyxG5nnzLqj", liveName: "Erupting Ground (Crown Stonebound)", change: "damage rows friendlyFire ENEMIES (live: unset, hits everyone)" },
};
export const ANSWERS: Record<string, MarkKey> = {
  [LIB.blast.ring]: "ring", [LIB.blast.rowsA]: "rowsA", [LIB.blast.rowsB]: "rowsB", [LIB.blast.scatterA]: "scatterA",
  [LIB.blast.scatterB]: "scatterB", [LIB.blast.lines]: "lines", [LIB.blast.sealLines]: "sealLines",
  [LIB.blast.splash]: "splash", [LIB.blast.shortLine]: "shortLine",
  [LIB.sig.maw]: "lastLight", [LIB.sig.quench]: "lastLight", [LIB.sig.commandAbsolute]: "lastLightBinding",
  [LIB.sig.crownfall]: "lines", [LIB.sig.broadside]: "rowsA", [LIB.sig.shipsBell]: "bindingRing",
};

export const LIB_POWERS = {
  blastRing: 160, blastRows: 140, blastScatter: 140, scatterPool: 30, blastLines: 150, sealLinesDamage: 60,
  maw: 200, quench: 220, commandAbsolute: 80, crownfall: 180, broadside: 140, shipsBell: 50,
  // RUL-2026-10-28-025: original powers; a modelled pet standing in a minor blast is accepted collateral.
  splash: 80, shortLine: 90,
  chainHook: 45, oath: 35, aegisShield: 1500, mending: 20, wardDR: 80,
};

const ALL_STATS = ["None", "Ninjutsu", "Genjutsu", "Taijutsu", "Bukijutsu"];
const ALL_GENERALS = ["Highest", "Strength", "Intelligence", "Willpower", "Speed"];
const weakness = (animation: string) =>
  tag("weakness", { target: "SELF", rounds: 1, dmgModifier: 3, statTypes: ALL_STATS, generalTypes: ALL_GENERALS, power: 100, staticAnimation: animation });

/**
 * The control payload for the violet blasts (Ship's Bell, Command Absolute, Seal Lines). It uses only types outside
 * SHARED_COOLDOWN_TAGS, so a boss's own stun, seal or root moves (Final Command, Ruin Refrain, Sovereign Fetters,
 * Keelbind) never lock the blast it marked for. Stun and seal are in the shared list: a blast carrying them could not
 * fire within 3 rounds of the boss's other stun or seal move, and its mark would go off with nothing after it.
 * Enemies only, so a boss's allies on the pattern are spared.
 */
const LOCK = (rounds: number) => [
  tag("elementalseal", { power: 100, rounds, friendlyFire: "ENEMIES" }),
  tag("timecompression", { power: 100, rounds, friendlyFire: "ENEMIES" }),
  tag("increasecooldown", { power: 2, rounds, friendlyFire: "ENEMIES", actionsAffected: ["move", "replacementTechnique"] }),
];

export const buildLibrary = () => {
  const J: Record<string, any> = {};
  const add = (j: any) => {
    J[j.id] = j;
    return j.id as string;
  };
  const p = LIB_POWERS;
  /* ---- marks ---- */
  const mark = (key: MarkKey, name: string, method: string, range: number, visuals: any[], ct: any, cooldown: number, line: string) =>
    add(jutsu(LIB.mark[key], {
      name, description: `A shared warning mark (${name}). Its blast follows on the caster's next turn.`, battleDescription: line,
      target: "GROUND", method, range, cooldown, actionCostPerc: 40, coordinateTargeting: ct, effects: [...visuals, markerTag(MARKER_TYPES[key])],
    }));
  const red = () => T.visual(anim("tg_heavy"), 1);
  const violet = () => T.visual(anim("tg_control"), 1);
  const safe = () => T.visual(anim("tg_safe"), 1, { target: "COORDINATES", coordinateTargeting: field("ALL", PATTERNS.stars) });
  mark("ring", "Omen: Ring", "AOE_SPIRAL_SHOOT", 2, [red()], undefined, 4, "The ground around %user cracks and glows.");
  mark("bindingRing", "Omen: Binding Ring", "COORDINATES", 0, [violet()], field("ALL", PATTERNS.bindingRing, "CASTER"), 4, "Chains of ink coil around %user.");
  mark("rowsA", "Omen: Rows", "COORDINATES", 0, [red()], field("ALL", PATTERNS.rowsA), 4, "Two lines across the field begin to glow.");
  mark("rowsB", "Omen: Rows", "COORDINATES", 0, [red()], field("ALL", PATTERNS.rowsB), 4, "Two lines across the field begin to glow.");
  mark("scatterA", "Omen: Scatter", "COORDINATES", 0, [red()], field("ALL", PATTERNS.scatterA), 4, "The ground swells in patches.");
  mark("scatterB", "Omen: Scatter", "COORDINATES", 0, [red()], field("ALL", PATTERNS.scatterB), 4, "The ground swells in patches.");
  mark("lines", "Omen: Lines", "COORDINATES", 0, [red()], field("ALL", PATTERNS.lines, "CASTER"), 4, "Thin lines of light fan out from %user.");
  mark("sealLines", "Omen: Seal Lines", "COORDINATES", 0, [violet()], field("ALL", PATTERNS.sealLines, "CASTER"), 4, "Seal script runs out from %user in four lines.");
  mark("lastLight", "Omen: Last Light", "COORDINATES", 0, [red(), safe()], field("EXCLUDE", PATTERNS.stars), 6, "The whole field darkens. Three points of skyglass light remain.");
  mark("lastLightBinding", "Omen: Last Light, Binding", "COORDINATES", 0, [violet(), safe()], field("EXCLUDE", PATTERNS.stars), 6, "Violet script covers the field. Three points of skyglass light remain.");
  /* ---- minor marks (regular crew; RUL-2026-10-28-024) ----
   * Caster-anchored COORDINATES patterns, cast with rule target SELF. A target-anchored blast (origin TARGET,
   * AOE_CIRCLE_SPAWN or AOE_LINE_SHOOT) is re-aimed at the target's current hex on the next turn, so stepping off the
   * marked hexes did not avoid it (probe_library); a caster-anchored pattern stays where it was marked. No floor
   * coverage, no safe tiles. */
  const minorMark = (key: "splash" | "shortLine", name: string, line: string) =>
    add(jutsu(LIB.mark[key], {
      name, description: `A minor warning mark (${name}). Its blast follows on the caster's next turn.`, battleDescription: line,
      target: "GROUND", method: "COORDINATES", range: 0, cooldown: 3, actionCostPerc: 40, coordinateTargeting: field("ALL", PATTERNS[key], "CASTER"), effects: [red(), markerTag(MARKER_TYPES[key])],
    }));
  minorMark("splash", "Omen: Splash", "%user marks a patch of deck in front of them.");
  minorMark("shortLine", "Omen: Short Line", "%user sights down a short line.");
  /* ---- shared blasts ---- */
  const blast = (id: string, name: string, target: string, method: string, range: number, ct: any, effects: any[], line = "The marked ground erupts.") =>
    add(jutsu(id, { name, description: `Shared blast: fires on the hexes its Omen marked.`, battleDescription: line, target, method, range, cooldown: 2, actionCostPerc: 100, coordinateTargeting: ct, effects }));
  const heavy = (power: number) => T.damage(power, { appearAnimation: anim("dt_heavy") });
  // Once marked, every blast goes off. Pure-damage blasts are GROUND: ground damage resolves as an instant hit on
  // occupants (enemies only), so they erupt on the marked tiles whether or not anyone is still there. (A CHARACTER
  // blast is not a valid cast with no character on its pattern; GROUND damage also strikes barriers on empty tiles.)
  // Blasts that stun, lock or push stay CHARACTER (GROUND lands only damage) and include a tile a character always
  // holds: the caster's own hex, or the whole field but the stars.
  blast(LIB.blast.ring, "Eruption: Ring", "GROUND", "AOE_SPIRAL_SHOOT", 2, undefined, [heavy(p.blastRing)]);
  blast(LIB.blast.rowsA, "Eruption: Rows", "GROUND", "COORDINATES", 0, field("ALL", PATTERNS.rowsA), [heavy(p.blastRows)]);
  blast(LIB.blast.rowsB, "Eruption: Rows", "GROUND", "COORDINATES", 0, field("ALL", PATTERNS.rowsB), [heavy(p.blastRows)]);
  for (const [id, pat] of [[LIB.blast.scatterA, PATTERNS.scatterA], [LIB.blast.scatterB, PATTERNS.scatterB]] as const)
    blast(id, "Eruption: Scatter", "GROUND", "COORDINATES", 0, field("ALL", pat), [T.damage(p.blastScatter, { appearAnimation: anim("dt_linger") }), T.pool(p.scatterPool, 2), T.visual(anim("tg_linger"), 2)]);
  blast(LIB.blast.lines, "Eruption: Lines", "GROUND", "COORDINATES", 0, field("ALL", PATTERNS.lines, "CASTER"), [heavy(p.blastLines)]);
  blast(LIB.blast.sealLines, "Binding: Seal Lines", "CHARACTER", "COORDINATES", 0, field("ALL", [ORIGIN, ...PATTERNS.sealLines], "CASTER"),
    [T.damage(p.sealLinesDamage, { appearAnimation: anim("dt_control") }), ...LOCK(2)], "The marked lines close.");
  // GROUND target: ground damage resolves as an instant hit on occupants, so the blast erupts on the marked tiles
  // whether or not anyone is still there (a CHARACTER blast is not a valid cast with nobody on its pattern).
  blast(LIB.blast.splash, "Eruption: Splash", "GROUND", "COORDINATES", 0, field("ALL", PATTERNS.splash, "CASTER"), [T.damage(p.splash, { appearAnimation: anim("dt_heavy"), friendlyFire: "ENEMIES" })], "The marked planks burst.");
  blast(LIB.blast.shortLine, "Eruption: Short Line", "GROUND", "COORDINATES", 0, field("ALL", PATTERNS.shortLine, "CASTER"), [T.damage(p.shortLine, { appearAnimation: anim("dt_heavy"), friendlyFire: "ENEMIES" })], "A short line of force cuts across the deck.");
  /* ---- bespoke signatures ---- */
  const sig = (id: string, f: { name: string; description: string; line: string; target: string; method: string; range: number; ct?: any; effects: any[] }) =>
    add(jutsu(id, { name: f.name, description: f.description, battleDescription: f.line, target: f.target, method: f.method, range: f.range, cooldown: 2, actionCostPerc: 100, coordinateTargeting: f.ct, effects: f.effects }));
  sig(LIB.sig.maw, { name: "Maw of the Deep", description: "Core Horror signature (Omen: Last Light): black water and teeth everywhere but the stars; Exposed Seam, x3 damage taken for 1 round.", line: "Black water and teeth rise from every plank. The mass splits open along a glowing seam.", target: "CHARACTER", method: "COORDINATES", range: 0, ct: field("EXCLUDE", PATTERNS.stars), effects: [T.damage(p.maw, { appearAnimation: anim("ch_maw") }), T.stun(1, { friendlyFire: "ENEMIES" }), weakness(anim("ch_exposed"))] });
  sig(LIB.sig.quench, { name: "Quench", description: "Foundry Warden signature (Omen: Last Light): steam everywhere but the cooled tiles; Cooling Shell, x3 damage taken for 1 round.", line: "%user tips seawater onto the melt. The room explodes in steam.", target: "CHARACTER", method: "COORDINATES", range: 0, ct: field("EXCLUDE", PATTERNS.stars), effects: [T.damage(p.quench, { appearAnimation: anim("fw_quench") }), weakness(anim("fw_cracked"))] });
  sig(LIB.sig.commandAbsolute, { name: "Command Absolute", description: "Crowned Captain signature (Omen: Last Light, Binding): everywhere but the stars, a 2-round lock: elemental jutsu sealed, +10 AP per action, Move and Replacement Technique +2 cooldown.", line: "\"Kneel.\"", target: "CHARACTER", method: "COORDINATES", range: 0, ct: field("EXCLUDE", PATTERNS.stars), effects: [T.damage(p.commandAbsolute, { appearAnimation: anim("cc_command_absolute") }), ...LOCK(2)] });
  sig(LIB.sig.crownfall, { name: "Crownfall", description: "Crowned Captain signature (Omen: Lines): crown shards fall along the fan.", line: "Shards of the crown fall like blades.", target: "GROUND", method: "COORDINATES", range: 0, ct: field("ALL", PATTERNS.lines, "CASTER"), effects: [T.damage(p.crownfall, { appearAnimation: anim("cc_crownfall") })] });
  sig(LIB.sig.broadside, { name: "Broadside", description: "The Captain's signature (Omen: Rows, set A): the ship's guns fire down the marked rows.", line: "\"Fire.\"", target: "GROUND", method: "COORDINATES", range: 0, ct: field("ALL", PATTERNS.rowsA), effects: [T.damage(p.broadside, { appearAnimation: anim("cp_broadside") })] });
  sig(LIB.sig.shipsBell, { name: "Ship's Bell", description: "The Captain's signature (Omen: Binding Ring): the bell tolls; push 3 and a 1-round lock inside the ring.", line: "\"All hands.\" The great bell answers.", target: "CHARACTER", method: "COORDINATES", range: 0, ct: field("ALL", [ORIGIN, ...PATTERNS.bindingRing], "CASTER"), effects: [T.damage(p.shipsBell, { appearAnimation: anim("cp_bell_toll") }), T.push(3, { friendlyFire: "ENEMIES" }), ...LOCK(1)] });
  /* ---- lowered guard ---- */
  add(jutsu(LIB.loweredGuard, { name: "Lowered Guard", description: "Shared window: the caster takes x3 damage for 1 round.", battleDescription: "%user lowers their guard for one breath.", target: "SELF", method: "SINGLE", range: 0, cooldown: 99, actionCostPerc: 40, effects: [weakness(anim("lg_lowered"))] }));
  /* ---- crew additions ---- */
  add(jutsu(LIB.crew.chainHook, { name: "Chain Hook", description: "A weighted chain hooks a target, drags them in and pins them.", battleDescription: "%user hurls a weighted chain and drags %target across the deck.", target: "OTHER_USER", method: "SINGLE", range: 5, cooldown: 3, actionCostPerc: 60, effects: [T.damage(p.chainHook, { appearAnimation: anim("chain-hook-hit") }), T.pull(3), T.root(1)] }));
  add(jutsu(LIB.crew.oath, { name: "Oath of Stillness", description: "A binding oath: +2 cooldown on Move and Replacement Technique for 2 rounds.", battleDescription: "%user speaks the oath; %target's footing turns to stone.", target: "OTHER_USER", method: "SINGLE", range: 5, cooldown: 4, actionCostPerc: 60, effects: [T.damage(p.oath), tag("increasecooldown", { power: 2, rounds: 2, actionsAffected: ["move", "replacementTechnique"] })] }));
  add(jutsu(LIB.crew.chartMark, { name: "Chart Mark", description: "Marks a target on the chart; the crew converge on it.", battleDescription: "%user marks %target on the chart. \"There.\"", target: "OTHER_USER", method: "SINGLE", range: 5, cooldown: 4, actionCostPerc: 40, effects: [T.pct("increasedamagetaken", 40, 2, { staticAnimation: anim("mark-sigil") }), tag("increasepoolcost", { power: 5, rounds: 2, calculation: "percentage", poolsAffected: [] })] }));
  add(jutsu(LIB.crew.aegis, { name: "Skyglass Aegis", description: "A pane of skyglass forms around an ally.", battleDescription: "%user raises a pane of skyglass around %target.", target: "ALLY", method: "SINGLE", range: 4, cooldown: 4, actionCostPerc: 40, donor: "xs-8r_KRJS8QQMpBDyhUv", effects: [tag("shield", { power: 100, health: p.aegisShield, rounds: 2, friendlyFire: "FRIENDLY", staticAnimation: anim("skyglass-pane") }), tag("absorb", { power: 20, rounds: 2, friendlyFire: "FRIENDLY", calculation: "percentage" })] }));
  add(jutsu(LIB.crew.mending, { name: "Mending Seal", description: "A seal that knits wounds and lifts afflictions from an ally.", battleDescription: "%user presses a mending seal to %target.", target: "ALLY", method: "SINGLE", range: 5, cooldown: 4, actionCostPerc: 40, donor: "xs-8r_KRJS8QQMpBDyhUv", effects: [T.heal(p.mending, { friendlyFire: "FRIENDLY" }), T.cleanse({ friendlyFire: "FRIENDLY" })] }));
  add(jutsu(LIB.crew.ward, { name: "Ward of Command", description: "The Sealwright's ward on the Captain: heavily reduced damage while she stands.", battleDescription: "%user binds the command ward to %target.", target: "ALLY", method: "SINGLE", range: 5, cooldown: 2, actionCostPerc: 40, donor: "xs-8r_KRJS8QQMpBDyhUv", effects: [
    T.pct("decreasedamagetaken", p.wardDR, 2, { target: "INHERIT", friendlyFire: "FRIENDLY", staticAnimation: anim("cp_command") }),
    // Clear-proof (RUL-2026-10-28-025; the hunts harness cleared it): clearprevent on the warded ally for the ward's
    // 2 rounds. clearprevent is a shared-cooldown type, but the Sealwright carries no other clearprevent jutsu.
    tag("clearprevent", { power: 100, rounds: 2, target: "INHERIT", friendlyFire: "FRIENDLY" }),
  ] }));
  /* ---- phase transitions ---- */
  // The Captain at 50% (RUL-2026-10-28-032): a 20 AP self move; with Raise the Gunwale (20 AP) and the first deck mark
  // (40 AP) the whole transition fits one turn, even under a player stun (apReduction 20, which cleanse cannot lift).
  // (JutsuValidator: actionCostPerc 10-100.)
  // Cooldown 99: once per fight. Its cleanse and clearprevent are shared-cooldown types, but no other jutsu in his kit
  // carries either (Unraveling Strike's "clear" is a separate group), so the 3-round lock blocks nothing.
  add(jutsu(LIB.transition.captain, {
    name: "Steady the Helm", description: "The Captain's turn to command: sheds afflictions, takes the wheel and braces for 2 rounds (40% less damage, 40% absorb, cannot be cleared).",
    // Placeholder text; the quote is the design's under-50% line (SKYGLASS_BOSS_FIGHTS.md section 1).
    battleDescription: "%user shakes off every hold on him and takes the wheel. \"I have held this deck through worse than you.\"",
    target: "SELF", method: "SINGLE", range: 0, cooldown: 99, actionCostPerc: 20, donor: "xs-8r_KRJS8QQMpBDyhUv",
    effects: [
      T.cleanse({ target: "SELF", friendlyFire: "FRIENDLY" }),
      T.pct("decreasedamagetaken", 40, 2, { target: "SELF", staticAnimation: anim("cp_steady") }),
      tag("absorb", { power: 40, rounds: 2, target: "SELF", calculation: "percentage" }),
      tag("clearprevent", { power: 100, rounds: 2, target: "SELF" }),
    ],
  }));
  /* ---- Skyglass-only copies of live jutsu ---- */
  // Crown Stonebound's Erupting Ground (live jBRyl7F4UjTyxG5nnzLqj), unchanged except that its damage hits enemies only.
  {
    const src = copyJutsu("jBRyl7F4UjTyxG5nnzLqj", LIB.liveCopy.stoneboundEruptingGround, {});
    add(copyJutsu("jBRyl7F4UjTyxG5nnzLqj", LIB.liveCopy.stoneboundEruptingGround, {
      description: `${src.description ?? ""} (Skyglass copy: damage hits enemies only.)`.trim(),
      effects: src.effects.map((e: any) => (e.type === "damage" ? { ...e, friendlyFire: "ENEMIES" } : e)),
    }));
  }
  return J;
};
