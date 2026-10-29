/**
 * The Haul (docs/design/SKYGLASS_THE_HAUL.md; RUL-2026-10-29-037, variety -038, simulator rulings -044): the S-rank
 * profession push-your-luck charts, 3 layout pages per profession, steeping modifiers.
 *
 * - Up to 5 steps. At each step: Crate (crew fight), Locker (elite + crew, one hazard for the first 2 rounds, more
 *   points), Cut through (fewer points, no fight now, a lingering hazard on the next fight, which must be fought), or Leave.
 * - Alertness = lockers opened (never falls): 0 as built; 1-2 one more crew guard (while a fight has < maxGuards) + 1
 *   starting hazard; 3+ the Arsenal Keeper / Sealwright echo joins locker fights; alert3 sets its extra hazards.
 * - Health and chakra carry between fights; any lost fight fails the run; the haul pays only at a win ending.
 * - Payout (-044): each choice adds haul points; the run pays the profession ladder's highest rung its points reach
 *   (guaranteed chests). Points are order-free, which keeps every quest under ~90 objectives.
 *
 * Pure data (no engine run): params, hazard tags (questDebuffTypes only), the fight for each graph state, and the
 * quest state-graph generator (`buildGraph`) whose JSON feeds the quest generator later.
 *
 * Guards are stat copies (placeholder ids `haul-*`) of records the harness already fights with: same kit and rules,
 * their own statsMultiplier / poolsMultiplier / innate rows. All Haul fights are opponent_scaled_to_user.
 */
import { tag } from "./kitlib";
import { LIVE } from "./hunts";

export type Quest = "hunter" | "gatherer";
export type Tier = "C" | "R" | "E" | "L";
export const TIERS: Tier[] = ["C", "R", "E", "L"];
export type Choice = "C" | "L" | "X"; // crate, locker, cut through ("leave" ends the path)

/** Chest EV per opening, material-cost basis (final tables, RUL-2026-10-29-036; state/skyglass_design/chests.json), millions of ryo. */
export const VALUE: Record<Quest, Record<Tier, number>> = {
  hunter: { C: 4.2, R: 6.1, E: 6.7, L: 11.5 },
  gatherer: { C: 3.2, R: 4.9, E: 5.4, L: 10.5 },
};
/** The 8 profession chests (live ids, answers/names_item.json). */
export const CHEST: Record<Quest, Record<Tier, { id: string; name: string }>> = {
  hunter: {
    C: { id: "KwgjMOya2XT6uYsgXbsh6", name: "Common Hunter's Chest" }, R: { id: "M-0CPw9yBmmreLvJU6gav", name: "Rare Hunter's Chest" },
    E: { id: "32k2rXF6W-7gn_Fubp4kU", name: "Epic Hunter's Chest" }, L: { id: "nAAfu3ya-dkVaZeH7LycZ", name: "Legendary Hunter's Chest" },
  },
  gatherer: {
    C: { id: "gb6vxdzWTYZR--7s-4kTX", name: "Common Gatherer's Chest" }, R: { id: "SWQpaXB8csJWL3zZMTz4r", name: "Rare Gatherer's Chest" },
    E: { id: "hikAzfsQPCvNUaFw_P8vs", name: "Epic Gatherer's Chest" }, L: { id: "Fh3xch8ox_JMaHj0-ntTF", name: "Legendary Gatherer's Chest" },
  },
};

/* ------------------------------------------------------------------ */
/* Params                                                               */
/* ------------------------------------------------------------------ */
/**
 * A guard copy. rules "shared": the endgame dungeon crew rules (the regular crew's minor marks: Splash / Short Line)
 * instead of the source's hunt-boss set pieces; setPiece: one shared library mark + blast pair added on top (no new jutsu).
 */
export type CopyP = { src: string; name: string; stats: number; pools: number; rows: number; taken?: number; givenDown?: number; role: string; rules?: "shared"; setPiece?: string; fuse?: { adjacent: number; round: number } };
/** A hazard (design name -> engine questDebuffType). `by`: how a multiplier applies (power, capped at `max`; or rounds). */
export type HazardP = { type: string; power: number; calc: "static" | "percentage"; pools?: string[]; by: "power" | "rounds"; max?: number; desc: string };
export type LayoutP = {
  quest: Quest; page: string; chart: string; character: string;
  /** Per step 1..5: copy keys at a crate / a locker (alertness extras are added on top). */
  crate: string[][]; locker: string[][];
  alertCrew: string; alertBoss: string;
  /** The quest's four hazards (design order, keys of `hazard`). */
  hazards: string[];
  /** Locker hazard at step s: lockerHazards[s-1]. Crate hazard at step s (layout trait): crateHazards?.[s-1]. */
  lockerHazards: string[]; crateHazards?: (string | null)[];
  /** Hazards alertness may add (default: `hazards`). moveprevent is kept out of elite fights: rooted under a set piece is a guaranteed hit. */
  alertHazards?: string[];
  /** Cut-through hazard by the step it was cut at: [odd step, even step]. */
  cutHazards: string[];
  /**
   * Haul points (millions of chest value) a step adds: a crate adds step[s-1], a locker step[s-1] + locker, a cut
   * step[s-1] - cut[s-1]. The run pays the quest's ladder bundle for its total (RUL-2026-10-29-044: guaranteed chests,
   * the quest stays small; points are order-free, so the graph state is (step, alertness, pending cut, points)).
   */
  points: { step: number[]; locker: number; cut: number[] };
  /** Steps offering a locker. */
  lockerSteps: number[];
  /**
   * Steps offering a cut-through (proposed: only where it costs a tier; at steps 1-2 "one tier lower, minimum Common"
   * is a Common chest for no fight). Absent: every step (step 5 excluded under must-fight-next).
   */
  cutSteps?: number[];
  /** Hazard strength multipliers: every hazard / the cut-through hazard only. Rounds: added to the defaults. */
  hazardMult: number; cutMult: number; roundsAdd?: { locker?: number; alert?: number; cut?: number };
};
/** One rung of a quest's payout ladder: guaranteed chests, plus optional bonus chests at a chance (%). */
export type Rung = { chests: Tier[]; bonus?: { tier: Tier; chance: number }[] };
export type ModP = {
  name: string; effect: string;
  /** Rot-Sealed Page cache weight (relative). */
  weight: number;
  hazardMult?: number; tierShift?: number; floodRounds?: number; floodRoundsGatherer?: number; lockerNoHazard?: boolean; startAlert?: number;
  /** Alarmed: lockers are offered from this step on every page; every locker adds `lockerPts` more points (order-free, so the graph stays small). */
  legendaryLockerFrom?: number; lockerPts?: number;
  /** Picked clean: guard compositions taken from `easier` steps earlier (min step 1); no crate / alertness hazards. */
  easier?: number;
  /** Proposed steeping premium: every chest of the haul also carries a bonus chest of its tier at this chance (%). */
  bonusAll?: number;
  /** Drop chance (%) of the haul's chests on this page instead of chestChance (Picked clean: the smaller haul). */
  haulChance?: number;
};
export type HaulParams = {
  copies: Record<string, CopyP>;
  hazard: Record<string, HazardP>;
  /** Rounds (incl. the opening round): the locker hazard, the alertness hazards, the cut-through hazard, a crate hazard. */
  rounds: { locker: number; alert: number; cut: number; crate: number };
  /**
   * "as-written": cut-through at every step, leaving right after it (a cut followed by leave, or a cut at step 5, is a
   * chest for nothing). "must-fight-next" (proposed): the node after a cut offers only Crate / Locker, step 5 no cut.
   */
  cutRule: "as-written" | "must-fight-next";
  /** Alertness adds its crew guard only while a fight has fewer guards than this (hazard AIs not counted). */
  maxGuards: number;
  /** Drop chance (%) of every haul chest at the ending (RUL-2026-10-29-044: 100, guaranteed). */
  chestChance: number;
  /** Payout ladder per profession, ascending; a run pays the highest rung whose value is <= its points (else the lowest). */
  ladder: Record<Quest, Rung[]>;
  /** Alertness 3+ (RUL-2026-10-29-044 item 2, softened): extra hazards on crates / on lockers (the Keeper still joins lockers). */
  alert3: { crateHazards: number; lockerHazards: number };
  layouts: Record<string, LayoutP>;
  modifiers: Record<string, ModP>;
};
/** One generated quest: a layout page, optionally with a steeping modifier. */
export type Variant = { layout: string; mod: string | null };
export const variantKey = (v: Variant) => `${v.layout}${v.mod ? `+${v.mod}` : ""}`;

const H = (type: string, power: number, calc: "static" | "percentage", by: "power" | "rounds", desc: string, o: Partial<HazardP> = {}): HazardP => ({ type, power, calc, by, desc, ...o });
const rep = <T>(x: T, n = 5) => Array.from({ length: n }, () => structuredClone(x));

export const DEFAULT_HAUL: HaulParams = {
  copies: {
    // Hunters: the ship's old hunting party (crew echoes), the Trophy Warden (Oathkeeper copy), the Arsenal Keeper.
    "h-wayfinder": { src: LIVE.wayfinder, name: "Wayfinder", stats: 3, pools: 1, rows: 2, taken: 100, givenDown: 40, role: "hunter crew", rules: "shared" },
    "h-blade": { src: LIVE.blade, name: "First Blade", stats: 3, pools: 1, rows: 2, taken: 100, givenDown: 40, role: "hunter crew", rules: "shared" },
    "h-warden": { src: LIVE.warden, name: "Deck Warden", stats: 3, pools: 1, rows: 2, taken: 100, givenDown: 40, role: "hunter crew", rules: "shared" },
    "h-veteran": { src: LIVE.blade, name: "First Blade (veteran)", stats: 3, pools: 1.2, rows: 3, taken: 100, role: "hunter crew, steps 4-5 (the crew scaled to the step)", rules: "shared" },
    "h-lookout": { src: LIVE.warden, name: "Deck Warden (lookout)", stats: 3, pools: 1, rows: 0, taken: 100, givenDown: 30, role: "hunter alertness crew", rules: "shared" },
    "trophy-warden": { src: "0PZU_FvlbM3ErYGlD5r56", name: "Trophy Warden", stats: 4, pools: 1.2, rows: 2, role: "hunter elite (Oathkeeper copy)", setPiece: "ring" },
    "h-keeper": { src: LIVE.keeper, name: "Arsenal Keeper", stats: 5, pools: 1, rows: 0, role: "hunter alertness 3+ (joins locker fights)" },
    // Gatherers: stores crew with Seal Charges / Core Canisters, the Stores Ward (Crown Archivist copy), the Sealwright echo.
    "g-warden": { src: LIVE.warden, name: "Deck Warden", stats: 3, pools: 1, rows: 2, taken: 100, givenDown: 40, role: "gatherer crew", rules: "shared" },
    "g-sentinel": { src: LIVE.sentinel, name: "Skyglass Sentinel", stats: 3, pools: 1, rows: 2, taken: 100, givenDown: 40, role: "gatherer crew", rules: "shared" },
    "g-veteran": { src: LIVE.sentinel, name: "Skyglass Sentinel (veteran)", stats: 3, pools: 1.2, rows: 3, taken: 100, role: "gatherer crew, steps 4-5 (the crew scaled to the step)", rules: "shared" },
    "g-lookout": { src: LIVE.warden, name: "Deck Warden (lookout)", stats: 3, pools: 1, rows: 0, taken: 100, givenDown: 30, role: "gatherer alertness crew", rules: "shared" },
    "g-charge": { src: LIVE.charge, name: "Seal Charge", stats: 1, pools: 1, rows: 0, taken: 100, fuse: { adjacent: 0, round: 4 }, role: "gatherer hazard AI" },
    "g-canister": { src: LIVE.canister, name: "Core Canister", stats: 1, pools: 1, rows: 0, taken: 100, fuse: { adjacent: 0, round: 5 }, role: "gatherer hazard AI" },
    "stores-ward": { src: LIVE.archivist, name: "Stores Ward", stats: 4, pools: 1.2, rows: 3, role: "gatherer elite (Crown Archivist copy)", setPiece: "sealLines" },
    "g-sealwright": { src: LIVE.sealwright, name: "Sealwright's Echo", stats: 5, pools: 1, rows: 0, role: "gatherer alertness 3+ (joins locker fights)" },
  },
  hazard: {
    // `wound` as a quest starting debuff never deals damage (tags.ts wound scales the creator's damage this action; a quest
    // effect has none): measured identical to no hazard. Closest questDebuffType with the same meaning: drain (bleed per action).
    wound: H("drain", 6, "percentage", "power", "Torn on a snare: you bleed with every action", { pools: ["Health"], max: 15 }),
    poison: H("poison", 250, "percentage", "power", "An old bait vial bursts: chakra and stamina you spend burn as poison", { max: 400 }),
    moveprevent: H("moveprevent", 100, "static", "rounds", "A line around the ankle: you cannot move"),
    decreasemaxpools: H("decreasemaxpools", 30, "percentage", "power", "Cold eyes / crystal in the lungs: your maximum health is lowered", { pools: ["Health"], max: 50 }),
    elementalseal: H("elementalseal", 100, "static", "rounds", "Dust in the seal channels: your elemental jutsu are sealed"),
    increasepoolcost: H("increasepoolcost", 300, "percentage", "power", "The growth drinks chakra: your jutsu cost more", { pools: ["Chakra", "Stamina"], max: 300 }),
    afterburn: H("afterburn", 60, "percentage", "power", "A cut channel flares: damage you take burns again", { max: 60 }),
  },
  rounds: { locker: 2, alert: 2, cut: 4, crate: 2 },
  cutRule: "must-fight-next",
  maxGuards: 2,
  chestChance: 100,
  ladder: {
    hunter: [{ chests: ["C"] }, { chests: ["R"] }, { chests: ["C", "C"] }, { chests: ["C", "R"] }, { chests: ["R", "R"] }, { chests: ["C", "L"] }, { chests: ["R", "L"] }, { chests: ["C", "R", "L"] }, { chests: ["L", "L"] }, { chests: ["C", "L", "L"] }],
    gatherer: [{ chests: ["C"] }, { chests: ["R"] }, { chests: ["C", "R"] }, { chests: ["R", "R"] }, { chests: ["L"] }, { chests: ["C", "L"] }, { chests: ["R", "L"] }, { chests: ["C", "R", "L"] }, { chests: ["L", "L"] }, { chests: ["C", "L", "L"] }],
  },
  alert3: { crateHazards: 1, lockerHazards: 1 },
  layouts: {
    // ---------------- hunters ----------------
    trophy: {
      quest: "hunter", page: "The Trophy Hold", chart: "Ledger Page: The Trophy Hold", character: "the classic balance",
      crate: [["h-blade", "h-wayfinder"], ["h-blade", "h-wayfinder"], ["h-blade", "h-wayfinder", "h-warden"], ["h-veteran", "h-wayfinder"], ["h-veteran", "h-wayfinder"]],
      locker: [["trophy-warden"], ["trophy-warden"], ["trophy-warden", "h-wayfinder"], ["trophy-warden", "h-veteran"], ["trophy-warden", "h-veteran"]],
      alertCrew: "h-lookout", alertBoss: "h-keeper",
      hazards: ["wound", "poison", "moveprevent", "decreasemaxpools"], alertHazards: ["poison", "decreasemaxpools"],
      lockerHazards: ["wound", "poison", "decreasemaxpools", "wound", "poison"],
      cutHazards: ["wound", "wound"],
      points: { step: [4.2, 0.9, 1.3, 3, 5.4], locker: 2.4, cut: [0, 0, 0, 2, 0] }, lockerSteps: [1, 2, 3, 4, 5], cutSteps: [3, 4], hazardMult: 1, cutMult: 2.5,
    },
    bone: {
      // Lockers only at steps 1-3, two tiers up at steps 1-2 (Epic); the opening crates and lockers carry an extra guard.
      quest: "hunter", page: "The Bone Store", chart: "Ledger Page: The Bone Store", character: "lockers early, a cheap but dangerous start",
      crate: [["h-blade", "h-wayfinder"], ["h-blade", "h-wayfinder"], ["h-blade", "h-wayfinder", "h-warden"], ["h-veteran", "h-wayfinder"], ["h-veteran", "h-wayfinder"]],
      locker: [["trophy-warden"], ["trophy-warden"], ["trophy-warden", "h-veteran"], ["trophy-warden", "h-veteran"], ["trophy-warden", "h-veteran"]],
      alertCrew: "h-lookout", alertBoss: "h-keeper",
      hazards: ["wound", "poison", "moveprevent", "decreasemaxpools"], alertHazards: ["poison", "decreasemaxpools"],
      lockerHazards: ["poison", "wound", "decreasemaxpools", "wound", "poison"],
      cutHazards: ["wound", "wound"],
      points: { step: [4.2, 0.9, 1.3, 1.2, 7.3], locker: 2.5, cut: [0, 0, 0, 2, 0] }, lockerSteps: [1, 2, 3], cutSteps: [3, 4], hazardMult: 1, cutMult: 1.5,
    },
    snare: {
      // Crates at steps 2-4 carry a snare on top of the usual hazards; cut-throughs from step 2 with a 2-round bleed (only a step-4 cut drops to Common).
      quest: "hunter", page: "The Snare Room", chart: "Ledger Page: The Snare Room", character: "heavy hazards, safe cut-throughs",
      crate: [["h-blade", "h-wayfinder"], ["h-blade", "h-wayfinder"], ["h-blade", "h-wayfinder", "h-warden"], ["h-veteran", "h-wayfinder"], ["h-veteran", "h-wayfinder"]],
      locker: [["trophy-warden"], ["trophy-warden", "h-wayfinder"], ["trophy-warden", "h-wayfinder"], ["trophy-warden", "h-veteran"], ["trophy-warden", "h-veteran"]],
      alertCrew: "h-lookout", alertBoss: "h-keeper",
      hazards: ["wound", "poison", "moveprevent", "decreasemaxpools"], alertHazards: ["poison", "decreasemaxpools"],
      lockerHazards: ["wound", "decreasemaxpools", "wound", "wound", "poison"],
      crateHazards: [null, "moveprevent", "wound", "poison", null],
      cutHazards: ["wound", "wound"],
      points: { step: [5.2, 0.9, 1.5, 1.2, 3.5], locker: 3.3, cut: [0, 0, 0, 2, 0] }, lockerSteps: [1, 2, 3, 4, 5], cutSteps: [2, 3, 4], hazardMult: 1, cutMult: 1.5,
      roundsAdd: { cut: -2 },
    },
    // ---------------- gatherers ----------------
    overgrown: {
      quest: "gatherer", page: "The Overgrown Stores", chart: "Stores Manifest: The Overgrown Stores", character: "the classic balance",
      crate: [["g-warden", "g-sentinel", "g-charge"], ["g-warden", "g-sentinel", "g-charge"], ["g-sentinel", "g-warden", "g-charge"], ["g-veteran", "g-warden", "g-charge"], ["g-veteran", "g-warden", "g-charge"]],
      locker: [["stores-ward", "g-canister"], ["stores-ward", "g-canister"], ["stores-ward", "g-warden", "g-canister"], ["stores-ward", "g-veteran", "g-canister"], ["stores-ward", "g-veteran", "g-canister"]],
      alertCrew: "g-lookout", alertBoss: "g-sealwright",
      hazards: ["elementalseal", "increasepoolcost", "decreasemaxpools", "afterburn"], alertHazards: ["increasepoolcost", "decreasemaxpools", "afterburn"],
      lockerHazards: ["elementalseal", "increasepoolcost", "decreasemaxpools", "afterburn", "elementalseal"],
      cutHazards: ["elementalseal", "elementalseal"],
      points: { step: [3.7, 1.4, 1.9, 2.5, 8.6], locker: 1.1, cut: [0, 0, 0, 2, 0] }, lockerSteps: [1, 2, 3, 4, 5], cutSteps: [3, 4], hazardMult: 1, cutMult: 1.5,
    },
    vault: {
      // Every locker fields an extra guard; a step-3 locker pays Legendary; locker bonus chance 40%.
      quest: "gatherer", page: "The Ore Vault", chart: "Stores Manifest: The Ore Vault", character: "dense guards, rich lockers",
      crate: [["g-warden", "g-sentinel", "g-charge"], ["g-warden", "g-sentinel", "g-charge"], ["g-sentinel", "g-warden", "g-charge"], ["g-veteran", "g-charge"], ["g-veteran", "g-charge"]],
      locker: [["stores-ward", "g-warden", "g-canister"], ["stores-ward", "g-warden", "g-canister"], ["stores-ward", "g-veteran", "g-canister"], ["stores-ward", "g-canister"], ["stores-ward", "g-canister"]],
      alertCrew: "g-lookout", alertBoss: "g-sealwright",
      hazards: ["elementalseal", "increasepoolcost", "decreasemaxpools", "afterburn"], alertHazards: ["increasepoolcost", "decreasemaxpools", "afterburn"],
      lockerHazards: ["increasepoolcost", "elementalseal", "afterburn", "decreasemaxpools", "increasepoolcost"],
      cutHazards: ["elementalseal", "elementalseal"],
      points: { step: [4.5, 1.9, 2.2, 0.6, 0.6], locker: 1.9, cut: [0, 0, 0, 2, 0] }, lockerSteps: [1, 2, 3, 4, 5], cutSteps: [3, 4], hazardMult: 1, cutMult: 1.5,
    },
    bloom: {
      // Dust on every crate, no multiplier; Common, Common, Rare, Rare, then a Legendary crate at step 5.
      quest: "gatherer", page: "The Bloom Cellar", chart: "Stores Manifest: The Bloom Cellar", character: "heavy dust hazards, a steep tier curve",
      crate: [["g-warden", "g-sentinel", "g-charge"], ["g-warden", "g-sentinel", "g-charge"], ["g-sentinel", "g-warden", "g-charge"], ["g-veteran", "g-warden", "g-charge"], ["g-veteran", "g-warden", "g-charge"]],
      locker: [["stores-ward", "g-canister"], ["stores-ward", "g-canister"], ["stores-ward", "g-warden", "g-canister"], ["stores-ward", "g-veteran", "g-canister"], ["stores-ward", "g-veteran", "g-canister"]],
      alertCrew: "g-lookout", alertBoss: "g-sealwright",
      hazards: ["decreasemaxpools", "afterburn", "elementalseal", "increasepoolcost"], alertHazards: ["decreasemaxpools", "afterburn", "increasepoolcost"],
      lockerHazards: ["decreasemaxpools", "afterburn", "elementalseal", "decreasemaxpools", "afterburn"],
      crateHazards: ["afterburn", "decreasemaxpools", "afterburn", "decreasemaxpools", "afterburn"],
      cutHazards: ["elementalseal", "elementalseal"],
      points: { step: [4.1, 0.9, 1.9, 4.2, 5.7], locker: 1.4, cut: [0, 0, 0, 2, 0] }, lockerSteps: [1, 2, 3, 4, 5], cutSteps: [3, 4], hazardMult: 1, cutMult: 1.5,
    },
  },
  modifiers: {
    // Proposed steeping premium (all but Picked clean): every chest one tier higher and a 40% bonus chest of its tier.
    // Rot-soaked's own effect is the doubled hazards; Picked clean is the bad roll (easier, one tier lower, chests at 60%).
    // Weights are the Rot-Sealed Page cache weights.
    rot: { name: "Rot-soaked", effect: "every hazard doubled; every chest one tier higher (+40% bonus chest each)", weight: 30, hazardMult: 2, tierShift: 1, bonusAll: 40 },
    flood: { name: "Flooded hold", effect: "rooted (moveprevent) for the first 3 rounds of every fight (2 on gatherer pages, RUL-2026-10-29-045); lockers carry no hazard; chests one tier higher (+40% bonus chest)", weight: 25, floodRounds: 3, floodRoundsGatherer: 2, lockerNoHazard: true, tierShift: 1, bonusAll: 40 },
    alarmed: { name: "Alarmed", effect: "start at alertness 2; lockers offered at every step from 4 and worth more; chests one tier higher (+40% bonus chest each)", weight: 25, startAlert: 2, legendaryLockerFrom: 4, lockerPts: 1.5, tierShift: 1, bonusAll: 40 },
    picked: { name: "Picked clean", effect: "easier fights (the previous step's guards, no crate or alertness hazards); chests one tier lower, each at 60%", weight: 20, easier: 1, tierShift: -1, haulChance: 60 },
  },
};
void rep;

export const copyId = (key: string) => `haul-${key}`;

/* ------------------------------------------------------------------ */
/* Hazards, tiers, fights                                               */
/* ------------------------------------------------------------------ */
const lay = (P: HaulParams, v: Variant) => {
  const L = P.layouts[v.layout];
  if (!L) throw new Error(`layout ${v.layout}?`);
  return L;
};
const modOf = (P: HaulParams, v: Variant): ModP | null => (v.mod ? P.modifiers[v.mod] ?? (() => { throw new Error(`modifier ${v.mod}?`); })() : null);
export const questOf = (P: HaulParams, v: Variant) => lay(P, v).quest;

/** One authored starting debuff (questDebuffTypes), shaped through the live AllTags schema; mult per HazardP.by. */
export const hazardTag = (P: HaulParams, key: string, rounds: number, mult = 1) => {
  const h = P.hazard[key];
  if (!h) throw new Error(`hazard ${key} has no params`);
  const power = h.by === "power" ? Math.min(h.max ?? Infinity, Math.round(h.power * mult)) : h.power;
  const r = h.by === "rounds" ? Math.max(1, Math.round(rounds * mult)) : rounds;
  return tag(h.type, { power, rounds: r, calculation: h.calc, target: "INHERIT", description: h.desc, ...(h.pools ? { poolsAffected: h.pools } : {}) });
};

export const alertBand = (a: number) => (a <= 0 ? 0 : a <= 2 ? 1 : 2);
export const startAlert = (P: HaulParams, v: Variant) => modOf(P, v)?.startAlert ?? 0;
export const lockerOffered = (P: HaulParams, v: Variant, step: number) => {
  const m = modOf(P, v);
  return lay(P, v).lockerSteps.includes(step) || (m?.legendaryLockerFrom !== undefined && step >= m.legendaryLockerFrom);
};
/** Points a choice adds at `step`. */
export const choicePoints = (P: HaulParams, v: Variant, step: number, c: Choice) => {
  const Lp = lay(P, v).points;
  const m = modOf(P, v);
  const base = Lp.step[step - 1]!;
  if (c === "X") return base - Lp.cut[step - 1]!;
  if (c === "L") return base + Lp.locker + (m?.lockerPts ?? 0);
  return base;
};
export const chanceOf = (P: HaulParams, v: Variant) => modOf(P, v)?.haulChance ?? P.chestChance;
/** A ladder rung as paid on this page: steeping tier shift, sealed-page bonus chests, chest chance. */
export const rungEntries = (P: HaulParams, v: Variant, r: Rung) => {
  const m = modOf(P, v);
  const sh = (t: Tier) => TIERS[Math.max(0, Math.min(3, TIERS.indexOf(t) + (m?.tierShift ?? 0)))]!;
  const chance = chanceOf(P, v);
  const out: { tier: Tier; chance: number; why: string }[] = r.chests.map((t) => ({ tier: sh(t), chance, why: "haul" }));
  for (const b of r.bonus ?? []) out.push({ tier: sh(b.tier), chance: Math.round(b.chance * chance) / 100, why: "bonus" });
  if (m?.bonusAll) for (const t of r.chests) out.push({ tier: sh(t), chance: Math.round(m.bonusAll * chance) / 100, why: "sealed-page bonus" });
  return out;
};
export const rungValue = (P: HaulParams, v: Variant, r: Rung) => rungEntries(P, v, r).reduce((s, e) => s + (VALUE[questOf(P, v)][e.tier] * e.chance) / 100, 0);
/** The rung a points total pays: the highest whose base value (unmodified) is <= the points, else the lowest. */
export const rungFor = (P: HaulParams, v: Variant, pts: number) => {
  const q = questOf(P, v);
  const lad = P.ladder[q];
  const base = (r: Rung) => r.chests.reduce((s, t) => s + VALUE[q][t], 0) + (r.bonus ?? []).reduce((s, b) => s + (VALUE[q][b.tier] * b.chance) / 100, 0);
  let k = 0;
  lad.forEach((r, i) => { if (base(r) <= pts + 1e-9) k = i; });
  return k;
};
export const rungName = (r: Rung) => [...r.chests, ...(r.bonus ?? []).map((b) => `${b.tier}@${b.chance}%`)].join("+");

export type FightDef = { key: string; label: string; ids: string[]; debuffs: any[]; hazards: { key: string; type: string; rounds: number; mult: number; why: string }[] };

/**
 * The fight for a crate or locker at `step` with `alert` lockers already opened (incl. a modifier's start alertness) and
 * an optional pending cut hazard (`pendingFrom` = the step the cut was made at). Ids are copy keys.
 */
export const fightFor = (P: HaulParams, v: Variant, kind: "C" | "L", step: number, alert: number, pendingFrom: number | null): FightDef => {
  const L = lay(P, v);
  const m = modOf(P, v);
  const band = alertBand(alert);
  const compStep = Math.max(1, step - (m?.easier ?? 0));
  const ids = [...(kind === "C" ? L.crate : L.locker)[compStep - 1]!];
  // Alertness 1+: one more crew guard, up to `maxGuards` guards (hazard AIs not counted), so the step-4/5 fights, which
  // already field three, take only the hazard.
  const guards = ids.filter((k) => !P.copies[k]?.fuse).length;
  if (band >= 1 && guards < P.maxGuards) ids.push(L.alertCrew);
  if (band >= 2 && kind === "L") ids.push(L.alertBoss);
  const hmult = L.hazardMult * (m?.hazardMult ?? 1);
  const ra = L.roundsAdd ?? {};
  const hz: FightDef["hazards"] = [];
  const add = (key: string, rounds: number, mult: number, why: string) => {
    const ex = hz.find((h) => h.key === key);
    if (ex) {
      ex.rounds = Math.max(ex.rounds, rounds);
      ex.mult = Math.max(ex.mult, mult);
    } else hz.push({ key, type: P.hazard[key]!.type, rounds: Math.max(1, rounds), mult, why });
  };
  if (m?.floodRounds) add("moveprevent", (L.quest === "gatherer" ? m.floodRoundsGatherer : undefined) ?? m.floodRounds, 1, "flooded hold");
  if (kind === "L" && !m?.lockerNoHazard) add(L.lockerHazards[step - 1]!, P.rounds.locker + (ra.locker ?? 0), hmult, "locker");
  const ch = L.crateHazards?.[step - 1];
  if (kind === "C" && ch && !m?.easier) add(ch, P.rounds.crate, hmult, "crate (layout)");
  if (pendingFrom !== null) add(L.cutHazards[(pendingFrom - 1) % 2]!, P.rounds.cut + (ra.cut ?? 0), hmult * L.cutMult, "cut-through");
  // Alertness: +1 / +2 starting hazards, distinct from the ones already on this fight, in the layout's order from the step.
  const AH = L.alertHazards ?? L.hazards;
  if (!m?.easier)
    for (let k = 0, n = 0, want = band < 2 ? band : kind === "C" ? P.alert3.crateHazards : P.alert3.lockerHazards; n < want && k < AH.length; k++) {
      const key = AH[(step - 1 + k) % AH.length]!;
      if (hz.some((h) => h.key === key)) continue;
      add(key, P.rounds.alert + (ra.alert ?? 0), hmult, "alertness");
      n++;
    }
  const debuffs = hz.map((h) => hazardTag(P, h.key, h.rounds, h.mult));
  const key = `${variantKey(v)}:${kind}${step}:a${Math.min(alert, 3)}:p${pendingFrom ?? "-"}`;
  const label = `${variantKey(v)} step ${step} ${kind === "C" ? "crate" : "locker"} alert ${alert}${pendingFrom !== null ? " cut-hazard" : ""} [${ids.join("+")}] hz ${hz.map((h) => `${h.key}x${h.mult}/${h.rounds}`).join(",") || "-"}`;
  return { key, label, ids, debuffs, hazards: hz };
};

/** Options offered at a choice node (before step `step` is taken). */
export const optionsAt = (P: HaulParams, v: Variant, step: number, pending: boolean): (Choice | "leave")[] => {
  if (step > 5) return ["leave"];
  const o: (Choice | "leave")[] = ["C"];
  if (lockerOffered(P, v, step)) o.push("L");
  if (pending && P.cutRule === "must-fight-next") return o;
  const cs = lay(P, v).cutSteps;
  if (!(P.cutRule === "must-fight-next" && step === 5) && (!cs || cs.includes(step))) o.push("X");
  if (step > 1) o.push("leave");
  return o;
};

/** Every legal complete path (a string over C/L/X; it ends by leaving, or after step 5). */
export const allPaths = (P: HaulParams, v: Variant) => {
  const out: string[] = [];
  const rec = (p: string, pending: boolean) => {
    const step = p.length + 1;
    if (step > 5) return void out.push(p);
    for (const o of optionsAt(P, v, step, pending)) {
      if (o === "leave") out.push(p);
      else rec(p + o, o === "X");
    }
  };
  rec("", false);
  return out;
};
export const pathPoints = (P: HaulParams, v: Variant, path: string) => [...path].reduce((t, c, i) => t + choicePoints(P, v, i + 1, c as Choice), 0);
/** The rung a cleared path pays (index into the ladder) and its name, for tables. */
export const pathTiers = (P: HaulParams, v: Variant, path: string) => {
  const k = rungFor(P, v, pathPoints(P, v, path));
  return [`r${k}:${rungName(P.ladder[questOf(P, v)][k]!)}`];
};
/** Expected value (M) of a cleared path: its rung's chests (and bonus entries) at their chances. */
export const pathValue = (P: HaulParams, v: Variant, path: string) => (path.length ? rungValue(P, v, P.ladder[questOf(P, v)][rungFor(P, v, pathPoints(P, v, path))]!) : 0);
/** Path -> its fight states: [{step, kind, alert, pendingFrom}] (cuts skipped). */
export const pathFights = (P: HaulParams, v: Variant, path: string) => {
  const out: { step: number; kind: "C" | "L"; alert: number; pendingFrom: number | null }[] = [];
  let alert = startAlert(P, v);
  let pending: number | null = null;
  [...path].forEach((c, i) => {
    const s = i + 1;
    if (c === "X") return void (pending = s);
    out.push({ step: s, kind: c as "C" | "L", alert, pendingFrom: pending });
    if (c === "L") alert++;
    pending = null;
  });
  return out;
};

/* ------------------------------------------------------------------ */
/* Quest state graph (spec for the quest generator)                     */
/* ------------------------------------------------------------------ */
/**
 * The generated quest as a state graph (RUL-2026-10-29-044: under ~90 objectives a quest).
 * - Choice node (dialog) per state (step, alertness 0..3 [3 = 3+, exact below: lockers drive the fights], pending cut,
 *   haul points). Points are order-free (step + locker + cut values), so paths with the same state share the node.
 * - Battle per (state, crate|locker): nextObjectiveId -> the next state's node (or the paid ending after step 5).
 * - Ending per payout rung (the ladder bundle the points buy), shared by every path that earns it; one fail ending.
 */
export const buildGraph = (P: HaulParams, v: Variant, copyMeta: Record<string, { id: string; name: string }>) => {
  const q = questOf(P, v);
  const L = lay(P, v);
  const m = modOf(P, v);
  type Node = { id: string; task: "dialog"; step: number; alertness: number; pending: number | null; points: number; rungIfLeaving: number; options: any[] };
  const choices = new Map<string, Node>();
  const battles = new Map<string, any>();
  const endings = new Map<string, any>();
  const r2 = (x: number) => Math.round(x * 100) / 100;
  const ending = (pts: number) => {
    const k = rungFor(P, v, pts);
    const id = `win_r${k}`;
    if (!endings.has(id)) {
      const r = P.ladder[q][k]!;
      endings.set(id, {
        id, task: "win_quest", rung: k, bundle: rungName(r), expectedValueM: r2(rungValue(P, v, r)),
        reward_items: rungEntries(P, v, r).map((e) => ({ ids: [CHEST[q][e.tier].id], name: `${CHEST[q][e.tier].name}${e.why === "haul" ? "" : ` (${e.why})`}`, number: e.chance, quantity: 1 })),
      });
    }
    return id;
  };
  endings.set("fail", { id: "fail", task: "fail_quest", note: "any lost (or drawn / fled) fight: the run fails, the chart stays spent, no haul" });
  const visit = (s: number, a: number, p: number | null, pts: number): string => {
    if (s > 5) return ending(pts);
    const id = `c${s}_a${a}_p${p ?? 0}_v${r2(pts)}`;
    if (choices.has(id)) return id;
    const node: Node = { id, task: "dialog", step: s, alertness: a, pending: p, points: r2(pts), rungIfLeaving: s > 1 ? rungFor(P, v, pts) : -1, options: [] };
    choices.set(id, node);
    for (const o of optionsAt(P, v, s, p !== null)) {
      if (o === "leave") {
        node.options.push({ choice: "leave", text: "Take what you have and go", next: ending(pts) });
        continue;
      }
      const add = choicePoints(P, v, s, o);
      if (o === "X") {
        node.options.push({ choice: "cut", points: r2(add), fight: false, hazardNextFight: L.cutHazards[(s - 1) % 2], next: visit(s + 1, a, s, pts + add) });
        continue;
      }
      const f = fightFor(P, v, o, s, a, p);
      const onWin = visit(s + 1, o === "L" ? Math.min(3, a + 1) : a, null, pts + add);
      const bid = `b${s}${o}_a${a}_p${p ?? 0}_v${r2(pts)}`;
      const opp = new Map<string, number>();
      for (const k of f.ids) opp.set(k, (opp.get(k) ?? 0) + 1);
      battles.set(bid, {
        id: bid, task: "start_battle", step: s, kind: o === "C" ? "crate" : "locker", alertness: a, alertBand: alertBand(a), pendingCutFrom: p,
        opponent_ai: [...opp.entries()].map(([k, n]) => ({ ids: [copyMeta[k]!.id], name: copyMeta[k]!.name, number: n })),
        opponent_scaled_to_user: true, applyDebuffs: f.debuffs, hazards: f.hazards.map((x) => ({ hazard: x.key, type: x.type, rounds: x.rounds, mult: x.mult, why: x.why })),
        nextObjectiveId: onWin, failObjectiveId: "fail",
      });
      node.options.push({ choice: o === "C" ? "crate" : "locker", points: r2(add), fight: true, battle: bid });
    }
    return id;
  };
  const start = visit(1, Math.min(3, startAlert(P, v)), null, 0);
  const shapes = new Set([...battles.values()].map((b) => JSON.stringify([b.opponent_ai, b.hazards])));
  return {
    variant: variantKey(v), quest: q, page: L.page, chart: m ? `Rot-Sealed ${L.chart} (${m.name})` : L.chart, modifier: m ? { key: v.mod, name: m.name, effect: m.effect } : null,
    gate: q === "hunter" ? "huntingRank S RANK" : "gatheringRank S RANK", start,
    counts: { choiceNodes: choices.size, battles: battles.size, endings: endings.size, objectives: choices.size + battles.size + endings.size, distinctFightShapes: shapes.size, legalPaths: allPaths(P, v).length },
    nodes: [...choices.values()], battles: [...battles.values()], endings: [...endings.values()],
  };
};
