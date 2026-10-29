/**
 * The Haul (docs/design/SKYGLASS_THE_HAUL.md; RUL-2026-10-29-037, variety RUL-2026-10-29-038): the S-rank profession
 * push-your-luck charts, 3 layout pages per profession, steeping modifiers, locker bonus chances.
 *
 * - Up to 5 steps. At each step: Crate (base tier, crew fight), Locker (+1 tier, elite + crew, one hazard for the first
 *   rounds; + a bonus chest of the same tier at bonusChance %), Cut through (-1 tier, min Common, no fight now, a
 *   lingering hazard on the next fight), or Leave.
 * - Alertness = lockers opened (never falls): 0 as built; 1-2 one more crew guard + 1 starting hazard; 3+ the Arsenal
 *   Keeper / Sealwright echo joins the elite (locker) fights + 2 starting hazards.
 * - Health and chakra carry between fights; any lost fight fails the run; the haul pays only at a win ending.
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
  /** Base tier index by step (0 C .. 3 L); lockers +lockerUp (per step if an array), cuts -cutDown. */
  tiers: { base: number[]; lockerUp: number | number[]; cutDown: number | number[] };
  /** Steps offering a locker. */
  lockerSteps: number[];
  /**
   * Steps offering a cut-through (proposed: only where it costs a tier; at steps 1-2 "one tier lower, minimum Common"
   * is a Common chest for no fight). Absent: every step (step 5 excluded under must-fight-next).
   */
  cutSteps?: number[];
  /** Hazard strength multipliers: every hazard / the cut-through hazard only. Rounds: added to the defaults. */
  hazardMult: number; cutMult: number; roundsAdd?: { locker?: number; alert?: number; cut?: number };
  bonusChance?: number;
};
export type ModP = {
  name: string; effect: string;
  /** Rot-Sealed Page cache weight (relative). */
  weight: number;
  hazardMult?: number; tierShift?: number; floodRounds?: number; lockerNoHazard?: boolean; startAlert?: number;
  legendaryLockerFrom?: number;
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
  /** Drop chance (%) of every haul chest at the ending (design: 100). */
  chestChance: number;
  /** Locker bonus chest of the same tier, drop chance (%), unless the layout sets its own. */
  bonusChance: number;
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
    "h-veteran": { src: LIVE.blade, name: "First Blade (veteran)", stats: 3, pools: 1.4, rows: 3, taken: 100, role: "hunter crew, steps 4-5 (the crew scaled to the step)", rules: "shared" },
    "h-lookout": { src: LIVE.warden, name: "Deck Warden (lookout)", stats: 3, pools: 1, rows: 0, taken: 100, givenDown: 30, role: "hunter alertness crew", rules: "shared" },
    "trophy-warden": { src: "0PZU_FvlbM3ErYGlD5r56", name: "Trophy Warden", stats: 4, pools: 1.5, rows: 2, role: "hunter elite (Oathkeeper copy)", setPiece: "ring" },
    "h-keeper": { src: LIVE.keeper, name: "Arsenal Keeper", stats: 5, pools: 1, rows: 0, role: "hunter alertness 3+ (joins locker fights)" },
    // Gatherers: stores crew with Seal Charges / Core Canisters, the Stores Ward (Crown Archivist copy), the Sealwright echo.
    "g-warden": { src: LIVE.warden, name: "Deck Warden", stats: 3, pools: 1, rows: 2, taken: 100, givenDown: 40, role: "gatherer crew", rules: "shared" },
    "g-sentinel": { src: LIVE.sentinel, name: "Skyglass Sentinel", stats: 3, pools: 1, rows: 2, taken: 100, givenDown: 40, role: "gatherer crew", rules: "shared" },
    "g-veteran": { src: LIVE.sentinel, name: "Skyglass Sentinel (veteran)", stats: 3, pools: 1.4, rows: 3, taken: 100, role: "gatherer crew, steps 4-5 (the crew scaled to the step)", rules: "shared" },
    "g-lookout": { src: LIVE.warden, name: "Deck Warden (lookout)", stats: 3, pools: 1, rows: 0, taken: 100, givenDown: 30, role: "gatherer alertness crew", rules: "shared" },
    "g-charge": { src: LIVE.charge, name: "Seal Charge", stats: 1, pools: 1, rows: 0, taken: 100, fuse: { adjacent: 0, round: 4 }, role: "gatherer hazard AI" },
    "g-canister": { src: LIVE.canister, name: "Core Canister", stats: 1, pools: 1, rows: 0, taken: 100, fuse: { adjacent: 0, round: 5 }, role: "gatherer hazard AI" },
    "stores-ward": { src: LIVE.archivist, name: "Stores Ward", stats: 4, pools: 1.5, rows: 3, role: "gatherer elite (Crown Archivist copy)", setPiece: "sealLines" },
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
  bonusChance: 20,
  layouts: {
    // ---------------- hunters ----------------
    trophy: {
      quest: "hunter", page: "The Trophy Hold", chart: "Ledger Page: The Trophy Hold", character: "the classic balance",
      crate: [["h-blade", "h-wayfinder"], ["h-blade", "h-wayfinder"], ["h-blade", "h-wayfinder", "h-warden"], ["h-veteran", "h-wayfinder"], ["h-veteran", "h-wayfinder"]],
      locker: [["trophy-warden"], ["trophy-warden"], ["trophy-warden", "h-wayfinder"], ["trophy-warden", "h-veteran"], ["trophy-warden", "h-veteran"]],
      alertCrew: "h-lookout", alertBoss: "h-keeper",
      hazards: ["wound", "poison", "moveprevent", "decreasemaxpools"], alertHazards: ["wound", "poison", "decreasemaxpools"],
      lockerHazards: ["wound", "poison", "decreasemaxpools", "wound", "poison"],
      cutHazards: ["wound", "wound"],
      tiers: { base: [0, 0, 1, 2, 2], lockerUp: 1, cutDown: [1, 1, 1, 2, 1] }, lockerSteps: [1, 2, 3, 4, 5], cutSteps: [3, 4], hazardMult: 1, cutMult: 2.5,
    },
    bone: {
      // Lockers only at steps 1-3, two tiers up at steps 1-2 (Epic); the opening crates and lockers carry an extra guard.
      quest: "hunter", page: "The Bone Store", chart: "Ledger Page: The Bone Store", character: "lockers early, a cheap but dangerous start",
      crate: [["h-blade", "h-wayfinder"], ["h-blade", "h-wayfinder"], ["h-blade", "h-wayfinder", "h-warden"], ["h-veteran", "h-wayfinder"], ["h-veteran", "h-wayfinder"]],
      locker: [["trophy-warden"], ["trophy-warden"], ["trophy-warden", "h-veteran"], ["trophy-warden", "h-veteran"], ["trophy-warden", "h-veteran"]],
      alertCrew: "h-lookout", alertBoss: "h-keeper",
      hazards: ["wound", "poison", "moveprevent", "decreasemaxpools"], alertHazards: ["wound", "poison", "decreasemaxpools"],
      lockerHazards: ["poison", "wound", "decreasemaxpools", "wound", "poison"],
      cutHazards: ["wound", "wound"],
      tiers: { base: [0, 0, 1, 2, 2], lockerUp: [2, 2, 1, 1, 1], cutDown: [1, 1, 1, 2, 1] }, lockerSteps: [1, 2, 3], cutSteps: [3, 4], hazardMult: 1, cutMult: 1.5,
    },
    snare: {
      // Every fight from step 2 carries a snare, hazards x1.25; cut-throughs from step 2 with a 2-round bleed, but they drop two tiers at steps 3-4.
      quest: "hunter", page: "The Snare Room", chart: "Ledger Page: The Snare Room", character: "heavy hazards, safe cut-throughs",
      crate: [["h-blade", "h-wayfinder"], ["h-blade", "h-wayfinder"], ["h-blade", "h-wayfinder", "h-warden"], ["h-veteran", "h-wayfinder"], ["h-veteran", "h-wayfinder"]],
      locker: [["trophy-warden"], ["trophy-warden"], ["trophy-warden", "h-wayfinder"], ["trophy-warden", "h-veteran"], ["trophy-warden", "h-veteran"]],
      alertCrew: "h-lookout", alertBoss: "h-keeper",
      hazards: ["wound", "poison", "moveprevent", "decreasemaxpools"], alertHazards: ["wound", "poison", "decreasemaxpools"],
      lockerHazards: ["wound", "decreasemaxpools", "wound", "wound", "poison"],
      crateHazards: [null, "moveprevent", "wound", "poison", "decreasemaxpools"],
      cutHazards: ["wound", "wound"],
      tiers: { base: [0, 0, 1, 2, 2], lockerUp: 1, cutDown: [1, 1, 2, 2, 1] }, lockerSteps: [1, 2, 3, 4, 5], cutSteps: [2, 3, 4], hazardMult: 1.25, cutMult: 1.5,
      roundsAdd: { cut: -2 },
    },
    // ---------------- gatherers ----------------
    overgrown: {
      quest: "gatherer", page: "The Overgrown Stores", chart: "Stores Manifest: The Overgrown Stores", character: "the classic balance",
      crate: [["g-warden", "g-sentinel", "g-charge"], ["g-warden", "g-sentinel", "g-charge"], ["g-sentinel", "g-warden", "g-charge"], ["g-veteran", "g-warden", "g-charge"], ["g-veteran", "g-warden", "g-charge"]],
      locker: [["stores-ward", "g-canister"], ["stores-ward", "g-canister"], ["stores-ward", "g-warden", "g-canister"], ["stores-ward", "g-veteran", "g-canister"], ["stores-ward", "g-veteran", "g-canister"]],
      alertCrew: "g-lookout", alertBoss: "g-sealwright",
      hazards: ["elementalseal", "increasepoolcost", "decreasemaxpools", "afterburn"],
      lockerHazards: ["elementalseal", "increasepoolcost", "decreasemaxpools", "afterburn", "elementalseal"],
      cutHazards: ["elementalseal", "afterburn"],
      tiers: { base: [0, 0, 1, 2, 2], lockerUp: 1, cutDown: [1, 1, 1, 2, 1] }, lockerSteps: [1, 2, 3, 4, 5], cutSteps: [3, 4], hazardMult: 1, cutMult: 1.5,
    },
    vault: {
      // Every locker fields an extra guard; a step-3 locker pays Legendary; locker bonus chance 40%.
      quest: "gatherer", page: "The Ore Vault", chart: "Stores Manifest: The Ore Vault", character: "dense guards, rich lockers",
      crate: [["g-warden", "g-sentinel", "g-charge"], ["g-warden", "g-sentinel", "g-charge"], ["g-sentinel", "g-warden", "g-charge"], ["g-veteran", "g-warden", "g-charge"], ["g-veteran", "g-warden", "g-charge"]],
      locker: [["stores-ward", "g-warden", "g-canister"], ["stores-ward", "g-warden", "g-canister"], ["stores-ward", "g-veteran", "g-canister"], ["stores-ward", "g-veteran", "g-warden", "g-canister"], ["stores-ward", "g-veteran", "g-warden", "g-canister"]],
      alertCrew: "g-lookout", alertBoss: "g-sealwright",
      hazards: ["elementalseal", "increasepoolcost", "decreasemaxpools", "afterburn"],
      lockerHazards: ["increasepoolcost", "elementalseal", "afterburn", "decreasemaxpools", "increasepoolcost"],
      cutHazards: ["elementalseal", "afterburn"],
      tiers: { base: [0, 0, 1, 2, 2], lockerUp: [1, 1, 2, 1, 1], cutDown: [1, 1, 1, 2, 1] }, lockerSteps: [1, 2, 3, 4, 5], cutSteps: [3, 4], hazardMult: 1, cutMult: 1.5, bonusChance: 40,
    },
    bloom: {
      // Dust on every crate, no multiplier; Common, Common, Rare, Rare, then a Legendary crate at step 5.
      quest: "gatherer", page: "The Bloom Cellar", chart: "Stores Manifest: The Bloom Cellar", character: "heavy dust hazards, a steep tier curve",
      crate: [["g-warden", "g-sentinel", "g-charge"], ["g-warden", "g-sentinel", "g-charge"], ["g-sentinel", "g-warden", "g-charge"], ["g-veteran", "g-warden", "g-charge"], ["g-veteran", "g-warden", "g-charge"]],
      locker: [["stores-ward", "g-canister"], ["stores-ward", "g-canister"], ["stores-ward", "g-warden", "g-canister"], ["stores-ward", "g-veteran", "g-canister"], ["stores-ward", "g-veteran", "g-canister"]],
      alertCrew: "g-lookout", alertBoss: "g-sealwright",
      hazards: ["decreasemaxpools", "afterburn", "elementalseal", "increasepoolcost"],
      lockerHazards: ["decreasemaxpools", "afterburn", "elementalseal", "decreasemaxpools", "afterburn"],
      crateHazards: ["afterburn", "decreasemaxpools", "afterburn", "decreasemaxpools", "afterburn"],
      cutHazards: ["elementalseal", "afterburn"],
      tiers: { base: [0, 0, 1, 1, 3], lockerUp: 1, cutDown: [1, 1, 1, 2, 1] }, lockerSteps: [1, 2, 3, 4, 5], cutSteps: [3, 4], hazardMult: 1, cutMult: 1.5,
    },
  },
  modifiers: {
    // Proposed steeping premium (all but Picked clean): every chest one tier higher and a 40% bonus chest of its tier.
    // Rot-soaked's own effect is the doubled hazards; Picked clean is the bad roll (easier, one tier lower, chests at 60%).
    // Weights are the Rot-Sealed Page cache weights.
    rot: { name: "Rot-soaked", effect: "every hazard doubled; every chest one tier higher (+40% bonus chest)", weight: 30, hazardMult: 2, tierShift: 1, bonusAll: 40 },
    flood: { name: "Flooded hold", effect: "moveprevent on the opening round of every fight; lockers carry no hazard; chests one tier higher (+40% bonus chest)", weight: 25, floodRounds: 1, lockerNoHazard: true, tierShift: 1, bonusAll: 40 },
    alarmed: { name: "Alarmed", effect: "start at alertness 2; a Legendary locker from step 4; chests one tier higher (+40% bonus chest)", weight: 25, startAlert: 2, legendaryLockerFrom: 4, tierShift: 1, bonusAll: 40 },
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
export const tierOf = (P: HaulParams, v: Variant, step: number, c: Choice): Tier => {
  const L = lay(P, v);
  const m = modOf(P, v);
  const b = L.tiers.base[step - 1]!;
  const up = Array.isArray(L.tiers.lockerUp) ? L.tiers.lockerUp[step - 1]! : L.tiers.lockerUp;
  const down = Array.isArray(L.tiers.cutDown) ? L.tiers.cutDown[step - 1]! : L.tiers.cutDown;
  let t = c === "L" ? b + up : c === "X" ? b - down : b;
  t = Math.max(0, Math.min(3, t));
  if (c === "L" && m?.legendaryLockerFrom !== undefined && step >= m.legendaryLockerFrom) t = 3;
  return TIERS[Math.max(0, Math.min(3, t + (m?.tierShift ?? 0)))]!;
};
export const bonusOf = (P: HaulParams, v: Variant) => lay(P, v).bonusChance ?? P.bonusChance;

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
  if (m?.floodRounds) add("moveprevent", m.floodRounds, 1, "flooded hold");
  if (kind === "L" && !m?.lockerNoHazard) add(L.lockerHazards[step - 1]!, P.rounds.locker + (ra.locker ?? 0), hmult, "locker");
  const ch = L.crateHazards?.[step - 1];
  if (kind === "C" && ch && !m?.easier) add(ch, P.rounds.crate, hmult, "crate (layout)");
  if (pendingFrom !== null) add(L.cutHazards[(pendingFrom - 1) % 2]!, P.rounds.cut + (ra.cut ?? 0), hmult * L.cutMult, "cut-through");
  // Alertness: +1 / +2 starting hazards, distinct from the ones already on this fight, in the layout's order from the step.
  const AH = L.alertHazards ?? L.hazards;
  if (!m?.easier)
    for (let k = 0, n = 0; n < band && k < AH.length; k++) {
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
export const pathTiers = (P: HaulParams, v: Variant, path: string) => [...path].map((c, i) => tierOf(P, v, i + 1, c as Choice));
/** Expected haul value of a cleared path (M): chests x chestChance + lockers' bonus chests x bonusChance. */
export const chanceOf = (P: HaulParams, v: Variant) => modOf(P, v)?.haulChance ?? P.chestChance;
export const pathValue = (P: HaulParams, v: Variant, path: string) => {
  const q = questOf(P, v);
  const all = (modOf(P, v)?.bonusAll ?? 0) / 100;
  let s = 0;
  [...path].forEach((c, i) => {
    const t = tierOf(P, v, i + 1, c as Choice);
    s += VALUE[q][t] * (chanceOf(P, v) / 100) * (1 + (c === "L" ? bonusOf(P, v) / 100 : 0) + all);
  });
  return s;
};
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
type Haul = Record<string, number>; // "C" / "R" / "E" / "L" chests, "bR" etc. locker bonus entries
const haulKey = (h: Haul) => [...TIERS, ...TIERS.map((t) => `b${t}`), ...TIERS.map((t) => `a${t}`)].map((t) => (h[t] ? `${t}${h[t]}` : "")).join("") || "empty";

/**
 * The generated quest as a state graph. Node state = (step, alertness 0..3 [3 = 3+], pending cut hazard, haul). A haul
 * is the exact multiset of chests plus locker bonus entries (bounded: no value folding is needed). `fold` > 0 instead
 * keys nodes by a value band of that width (millions), paying the band's first-reached haul (a lossy alternative).
 */
export const buildGraph = (P: HaulParams, v: Variant, copyMeta: Record<string, { id: string; name: string }>, fold = 0) => {
  const q = questOf(P, v);
  const L = lay(P, v);
  const m = modOf(P, v);
  const bonus = bonusOf(P, v);
  const chance = chanceOf(P, v);
  const all = m?.bonusAll ?? 0;
  type Node = { id: string; task: "dialog"; step: number; alertness: number; pending: number | null; haul: Haul; haulExpectedM: number; options: any[] };
  const choices = new Map<string, Node>();
  const battles = new Map<string, any>();
  const endings = new Map<string, any>();
  const canonical = new Map<string, Haul>();
  const val = (h: Haul) => Math.round(TIERS.reduce((s, t) => s + (((h[t] ?? 0) + ((h[`b${t}`] ?? 0) * bonus + (h[`a${t}`] ?? 0) * all) / 100) * chance) / 100 * VALUE[q][t], 0) * 100) / 100;
  const keyOf = (h: Haul) => {
    if (!fold) return haulKey(h);
    const b = `v${Math.floor(val(h) / fold)}`;
    if (!canonical.has(b)) canonical.set(b, { ...h });
    return b;
  };
  const resolveHaul = (h: Haul) => (fold ? canonical.get(keyOf(h))! : h);
  const ending = (h0: Haul) => {
    const h = resolveHaul(h0);
    const id = `win_${haulKey(h)}`;
    if (!endings.has(id))
      endings.set(id, {
        id, task: "win_quest", haul: { ...h }, haulExpectedM: val(h),
        reward_items: TIERS.flatMap((t) => [
          ...Array.from({ length: h[t] ?? 0 }, () => ({ ids: [CHEST[q][t].id], name: CHEST[q][t].name, number: chance, quantity: 1 })),
          ...Array.from({ length: h[`b${t}`] ?? 0 }, () => ({ ids: [CHEST[q][t].id], name: `${CHEST[q][t].name} (locker bonus)`, number: Math.round(bonus * chance) / 100, quantity: 1 })),
          ...Array.from({ length: h[`a${t}`] ?? 0 }, () => ({ ids: [CHEST[q][t].id], name: `${CHEST[q][t].name} (sealed-page bonus)`, number: Math.round(all * chance) / 100, quantity: 1 })),
        ]),
      });
    return id;
  };
  endings.set("fail", { id: "fail", task: "fail_quest", note: "any lost (or drawn / fled) fight: the run fails, the chart stays spent, no haul" });
  const visit = (s: number, a: number, p: number | null, h: Haul): string => {
    if (s > 5) return ending(h);
    const id = `c${s}_a${a}_p${p ?? 0}_${keyOf(h)}`;
    if (choices.has(id)) return id;
    const node: Node = { id, task: "dialog", step: s, alertness: a, pending: p, haul: { ...resolveHaul(h) }, haulExpectedM: val(resolveHaul(h)), options: [] };
    choices.set(id, node);
    for (const o of optionsAt(P, v, s, p !== null)) {
      if (o === "leave") {
        node.options.push({ choice: "leave", text: "Take what you have and go", next: ending(h) });
        continue;
      }
      const tier = tierOf(P, v, s, o);
      const h2: Haul = { ...h, [tier]: (h[tier] ?? 0) + 1 };
      if (o === "L" && bonus > 0) h2[`b${tier}`] = (h2[`b${tier}`] ?? 0) + 1;
      if (all > 0) h2[`a${tier}`] = (h2[`a${tier}`] ?? 0) + 1;
      if (o === "X") {
        node.options.push({ choice: "cut", tier, chest: CHEST[q][tier].name, fight: false, hazardNextFight: L.cutHazards[(s - 1) % 2], next: visit(s + 1, a, s, h2) });
        continue;
      }
      const f = fightFor(P, v, o, s, a, p);
      const onWin = visit(s + 1, o === "L" ? Math.min(3, a + 1) : a, null, h2);
      const bid = `b${s}${o}_a${a}_p${p ?? 0}_${keyOf(h)}`;
      const opp = new Map<string, number>();
      for (const k of f.ids) opp.set(k, (opp.get(k) ?? 0) + 1);
      battles.set(bid, {
        id: bid, task: "start_battle", step: s, kind: o === "C" ? "crate" : "locker", alertness: a, alertBand: alertBand(a), pendingCutFrom: p,
        opponent_ai: [...opp.entries()].map(([k, n]) => ({ ids: [copyMeta[k]!.id], name: copyMeta[k]!.name, number: n })),
        opponent_scaled_to_user: true, applyDebuffs: f.debuffs, hazards: f.hazards.map((x) => ({ hazard: x.key, type: x.type, rounds: x.rounds, mult: x.mult, why: x.why })),
        nextObjectiveId: onWin, failObjectiveId: "fail",
      });
      node.options.push({ choice: o === "C" ? "crate" : "locker", tier, chest: CHEST[q][tier].name, bonusChance: o === "L" ? bonus : 0, fight: true, battle: bid });
    }
    return id;
  };
  const start = visit(1, Math.min(3, startAlert(P, v)), null, {});
  const shapes = new Set([...battles.values()].map((b) => JSON.stringify([b.opponent_ai, b.hazards])));
  return {
    variant: variantKey(v), quest: q, page: L.page, chart: m ? `Rot-Sealed ${L.chart} (${m.name})` : L.chart, modifier: m ? { key: v.mod, name: m.name, effect: m.effect } : null,
    gate: q === "hunter" ? "huntingRank S RANK" : "gatheringRank S RANK", start, fold,
    counts: { choiceNodes: choices.size, battles: battles.size, endings: endings.size, objectives: choices.size + battles.size + endings.size, distinctFightShapes: shapes.size, legalPaths: allPaths(P, v).length },
    nodes: [...choices.values()], battles: [...battles.values()], endings: [...endings.values()],
  };
};
