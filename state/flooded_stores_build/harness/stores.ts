/**
 * The Flooded Stores (Stolen Stores weekend, design approved Nov 18): the storeroom crew records, their ration jutsu,
 * the three crew fights of the run and the two beach raider fights. Isonade (fight 4) is engine/isonade.ts.
 *
 * Built on charts.ts: the crew are copies of live Skyglass crew records (stats, avatars), scaled to the player
 * (opponent_scaled_to_user) like the common charts. New records and jutsu carry placeholder ids `fs-*` (law 17:
 * created ids replace them). Nothing here is pushed.
 *
 * The ration (finalstand, power 100, 1 round + a small heal) is the run's one trick: a fed looter can't fall this round.
 * - Hand Out a Ration targets one ally (method SINGLE on OTHER_USER): with nobody beside him the cast fails and the rule
 *   falls through, so "alone" needs no condition. Alone, the Mate counts out a ration (marker, round 2/5/8...) and eats
 *   it next turn.
 * - Open the Stores (the Quartermaster, round 1): every looter in reach is fed.
 * - Stack the Crates (the Sentinel, from round 2): a crate barrier in front of the player.
 */
import { anim, cast, cond, endTurn, jutsu, rule, tag, T } from "./kitlib";
import { buildCharts, COPY, type ChartParams, type Run } from "./charts";
import { LIVE, NAME } from "./hunts";
import { DONOR_SUMMON } from "./cclib";

export const FS = {
  deckhand: "fs-looting-deckhand", mate: "fs-quartermasters-mate", sentinel: "fs-looting-sentinel", blade: "fs-looting-blade",
  qm: "fs-quartermaster", deckhandSummon: "fs-looting-deckhand-hold",
  // beach copies: same kit, not scaled in the overworld? (overworld AI fights scale to the attacker: see note in report)
  j: {
    swing: "fs-crate-swing", slash: "fs-cutlass-slash", pocket: "fs-pocket-a-ration", ration: "fs-hand-out-a-ration", count: "fs-count-out-a-ration",
    eat: "fs-eat-a-ration", stores: "fs-count-the-stores", crates: "fs-stack-the-crates", open: "fs-open-the-stores",
    hold: "fs-up-from-the-hold",
  },
} as const;
Object.assign(NAME, {
  [FS.deckhand]: "Looting Deckhand", [FS.mate]: "Quartermaster's Mate", [FS.sentinel]: "Looting Sentinel",
  [FS.blade]: "Looting Blade", [FS.qm]: "The Quartermaster", [FS.deckhandSummon]: "Looting Deckhand",
});

export type StoresParams = {
  swing: number; slash: number; swingAp: number; countPower: number; countGrow: number; rationHeal: number; rationAp: number;
  crateHp: number; crateRounds: number; holdRound: number;
  rec: Record<string, { pools: number; stats: number; rows?: number; taken?: number; givenDown?: number }>;
};
export const DEFAULT_STORES: StoresParams = {
  swing: 160, slash: 220, swingAp: 40, countPower: 180, countGrow: 20, rationHeal: 5, rationAp: 30, crateHp: 3000, crateRounds: 3, holdRound: 3,
  rec: {
    // stats 1 + 100% damage taken: the common-chart convention (overrides/charts.params.json commons), so a level 30-80
    // player without gear can clear the crew while level 100 kits still feel the hits.
    [FS.deckhand]: { pools: 1.3, stats: 1, taken: 100 }, [FS.mate]: { pools: 1.6, stats: 1, taken: 100 }, [FS.sentinel]: { pools: 1, stats: 1, taken: 100 },
    [FS.blade]: { pools: 1.5, stats: 1, taken: 100, givenDown: 50 }, [FS.qm]: { pools: 2, stats: 1, taken: 50 }, [FS.deckhandSummon]: { pools: 1.3, stats: 1, taken: 100 },
  },
};

const FED = "Fed: can't fall this round";
const ration = (heal: number) => [
  tag("finalstand", { power: 100, rounds: 1, description: FED }),
  T.heal(heal, { friendlyFire: "FRIENDLY" }),
];
const pct = (type: string, power: number, rounds: number, description: string) => tag(type, { power, rounds, calculation: "percentage", description });

export const buildStores = (P: ChartParams & { stores?: Partial<StoresParams> }, kitParams: any) => {
  const S: StoresParams = { ...DEFAULT_STORES, ...(P.stores ?? {}), rec: { ...DEFAULT_STORES.rec, ...(P.stores?.rec ?? {}) } };
  const built = buildCharts(P, kitParams);
  const ov = built.override as any;
  const J = FS.j;
  const add = (r: any) => { ov.jutsu[r.id] = r; built.newRecords[r.id] = { kind: "jutsu", note: r.description }; };

  add(jutsu(J.swing, {
    name: "Crate Swing", description: "Swings a looted crate. The same steady hit every time.",
    battleDescription: "%user swings a looted crate at %target.", target: "OTHER_USER", method: "SINGLE", range: 1, cooldown: 1,
    actionCostPerc: S.swingAp, effects: [T.damage(S.swing, { calculation: "static" })],
  }));
  add(jutsu(J.slash, {
    name: "Cutlass Slash", description: "A looter's cutlass. The same hard cut every time.",
    battleDescription: "%user slashes at %target with a notched cutlass.", target: "OTHER_USER", method: "SINGLE", range: 1, cooldown: 1,
    actionCostPerc: S.swingAp, effects: [T.damage(S.slash, { calculation: "static" })],
  }));
  add(jutsu(J.pocket, {
    name: "Pocket a Ration", description: "Once a fight, at half health, he eats a pocketed ration and can't fall this round.",
    battleDescription: "%user stuffs a pocketed ration in his mouth. He won't fall this round.", target: "SELF", method: "SINGLE", range: 0,
    cooldown: 99, actionCostPerc: S.rationAp, effects: ration(S.rationHeal).map((e) => ({ ...e, target: "SELF" })),
  }));
  add(jutsu(J.ration, {
    name: "Hand Out a Ration", description: "Feeds one looter beside him: it can't fall this round and heals a little.",
    battleDescription: "%user hands %target a ration. %target won't fall this round.", target: "OTHER_USER", method: "SINGLE", range: 3,
    cooldown: 2, actionCostPerc: S.rationAp, effects: ration(S.rationHeal),
  }));
  add(jutsu(J.count, {
    name: "Count Out a Ration", description: "Alone, he counts out a ration for himself. He eats it next turn.",
    battleDescription: "%user counts out a ration for himself. He'll eat it next turn.", target: "SELF", method: "SINGLE", range: 0,
    cooldown: 2, actionCostPerc: 75, effects: [T.marker(1)],
  }));
  add(jutsu(J.eat, {
    name: "Eat a Ration", description: "Eats the ration he counted out: he can't fall this round and heals a little.",
    battleDescription: "%user eats his ration. He won't fall this round.", target: "SELF", method: "SINGLE", range: 0,
    cooldown: 2, actionCostPerc: S.rationAp, effects: ration(S.rationHeal).map((e) => ({ ...e, target: "SELF" })),
  }));
  add(jutsu(J.stores, {
    name: "Count the Stores", description: "A slow, heavy hit. Each count makes the next few hit harder.",
    battleDescription: "%user counts the stores out loud and brings the ledger down on %target.", target: "OTHER_USER", method: "SINGLE", range: 1,
    cooldown: 1, actionCostPerc: 50,
    effects: [T.damage(S.countPower, { calculation: "static" }), { ...pct("increasedamagegiven", S.countGrow, 3, "Counting: hits harder"), target: "SELF" }],
  }));
  add(jutsu(J.crates, {
    name: "Stack the Crates", description: "Stacks looted crates into a wall in front of the crew.",
    battleDescription: "%user stacks crates into a wall.", target: "EMPTY_GROUND", method: "SINGLE", range: 3, cooldown: 3, actionCostPerc: 40,
    effects: [tag("barrier", { power: 100, rounds: S.crateRounds, curHealth: S.crateHp, maxHealth: S.crateHp, absorbPercentage: 100, staticAnimation: anim("tg_crates") })],
  }));
  add(jutsu(J.open, {
    name: "Open the Stores", description: "Opens the stores: every looter around him is fed this round.",
    battleDescription: "%user opens the stores. Every looter in the room is fed and won't fall this round.", target: "GROUND", method: "AOE_CIRCLE_SPAWN", range: 5,
    cooldown: 99, actionCostPerc: 40, effects: ration(S.rationHeal),
  }));
  {
    const base = jutsu(J.hold, { name: "Up from the Hold", description: "Calls a deckhand up from the hold.",
      battleDescription: "%user bangs on the hatch. A deckhand climbs up from the hold.", target: "EMPTY_GROUND", method: "SINGLE", range: 3,
      cooldown: 99, actionCostPerc: 30, effects: [T.damage(1)] });
    add({ ...base, effects: DONOR_SUMMON.effects.filter((e: any) => e.type === "summon").map((e: any) => ({ ...e, aiId: FS.deckhandSummon, aiHp: 1000, power: 100, powerPerLevel: 0, rounds: 99, appearSfx: "" })) });
  }

  const fed = cond.marker(1, "increasecooldown");
  const rules: Record<string, any[]> = {
    [FS.deckhand]: [
      cast("Pocket a Ration (half health, once)", J.pocket, "SELF", [cond.hp(50)]),
      cast("Crate Swing", J.swing, "CLOSEST_OPPONENT", [cond.near(2)]),
      rule("close in", [], { type: "move_towards_opponent", target: "CLOSEST_OPPONENT" }),
    ],
    [FS.mate]: [
      cast("Hand Out a Ration (weakest looter)", J.ration, "LOWEST_MAX_HEALTH_ALLY"),
      cast("Eat a Ration (counted out last turn)", J.eat, "SELF", [fed]),
      cast("Count Out a Ration (alone)", J.count, "SELF"),
      cast("Count the Stores", J.stores, "CLOSEST_OPPONENT", [cond.near(2)]),
      rule("close in", [], { type: "move_towards_opponent", target: "CLOSEST_OPPONENT" }),
    ],
    [FS.qm]: [
      cast("Open the Stores (round 1)", J.open, "SELF", [{ type: "specific_round", value: 1, description: "" }]),
      cast("Up from the Hold (round 3 on)", J.hold, "EMPTY_GROUND_CLOSEST_TO_SELF", [cond.roundGt(S.holdRound - 1), cond.noSummon()]),
      cast("Hand Out a Ration (weakest looter)", J.ration, "LOWEST_MAX_HEALTH_ALLY"),
      cast("Crate Swing (only when cornered)", J.swing, "CLOSEST_OPPONENT", [cond.near(2)]),
      endTurn("stands behind his crew"),
    ],
  };
  rules[FS.deckhandSummon] = rules[FS.deckhand]!.filter((r) => r.action.jutsuId !== J.pocket);
  const kit = (rs: any[]) => [...new Set(rs.map((r) => r.action.jutsuId).filter((j: string) => j && j !== "basicAttack"))] as string[];
  const rowsFx = (n = 0) => Array.from({ length: n }, () => pct("increasedamagegiven", 100, 99, "Increased damage given"));
  const mk = (id: string, base: string, username: string, rs: any[], note: string) => {
    const s = S.rec[id]!;
    ov.newEnemies[id] = { base, username, aiEdit: { poolsMultiplier: s.pools, statsMultiplier: s.stats }, effects: [...rowsFx(s.rows), ...(s.taken ? [pct("increasedamagetaken", s.taken, 99, "Increased damage taken")] : []), ...(s.givenDown ? [pct("decreasedamagegiven", s.givenDown, 99, "Decreased damage given")] : [])], jutsuIds: kit(rs), rules: rs, includeDefaultRules: false };
    ov.signatures[id] = rs.map((r: any, i: number) => (r.action.jutsuId ? i : -1)).filter((i: number) => i >= 0);
    built.newRecords[id] = { kind: "AI", note: `${note}; pools ${s.pools}, statsMultiplier ${s.stats}, +${s.taken ?? 0}% damage taken; opponent_scaled_to_user`, rules: rs };
  };
  mk(FS.deckhand, "Deck Warden", "Looting Deckhand", rules[FS.deckhand]!, "beach raider + fight 1/3 looter (Deck Warden statline)");
  mk(FS.deckhandSummon, "Deck Warden", "Looting Deckhand", rules[FS.deckhandSummon]!, "the Quartermaster's summon (no pocketed ration)");
  mk(FS.mate, "Deck Warden", "Quartermaster's Mate", rules[FS.mate]!, "beach raider + fight 1/2 ration carrier");
  mk(FS.qm, "The Captain", "The Quartermaster", rules[FS.qm]!, "fight 3 boss: feeds his crew, calls deckhands from the hold");
  // Sentinel: the Skyglass Sentinel statline with a short kit (crates + Crate Swing): fight 2 is about the wall, not the
  // Sentinel's own Tide Line set pieces. Blade: the First Blade statline with a plain cutlass (its live Ring set pieces are a Wreck kit).
  const sentRules = [
    cast("Stack the Crates (round 2 on)", J.crates, "EMPTY_GROUND_CLOSEST_TO_OPPONENT", [cond.roundGt(1)]),
    cast("Crate Swing", J.swing, "CLOSEST_OPPONENT", [cond.near(2)]),
    rule("close in", [], { type: "move_towards_opponent", target: "CLOSEST_OPPONENT" }),
  ];
  mk(FS.sentinel, NAME[LIVE.sentinel]!, "Looting Sentinel", sentRules, "fight 2 wall builder (Skyglass Sentinel statline)");
  const bladeRules = [
    cast("Pocket a Ration (half health, once)", J.pocket, "SELF", [cond.hp(50)]),
    cast("Cutlass Slash", J.slash, "CLOSEST_OPPONENT", [cond.near(2)]),
    rule("close in", [], { type: "move_towards_opponent", target: "CLOSEST_OPPONENT" }),
  ];
  mk(FS.blade, NAME[LIVE.blade]!, "Looting Blade", bladeRules, "fight 3 guard (First Blade statline): Cutlass Slash + Pocket a Ration");
  return { ...built, S };
};

export const buildStoreRuns = (): Record<string, Run> => {
  const f = (label: string, ids: string[], o: any = {}) => ({ label, ids, scaled: true, ...o });
  return {
    flooded: {
      chart: "The Flooded Stores (fights 1 to 3; Isonade is isonade.ts)",
      fights: [
        f("The Ration Line: Mate + 2 Deckhands", [FS.mate, FS.deckhand, FS.deckhand]),
        f("The Crate Wall: Sentinel + Mate", [FS.sentinel, FS.mate]),
        f("The Quartermaster + 2 Blades", [FS.qm, FS.blade, FS.blade], { boss: true }),
      ],
    },
    beachDeckhand: { chart: "Beach: one Looting Deckhand", fights: [f("Deckhand", [FS.deckhand])] },
    beachMate: { chart: "Beach: one Quartermaster's Mate", fights: [f("Mate", [FS.mate])] },
  };
};
