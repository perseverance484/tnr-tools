/**
 * Silent Bastion Phase 1 — symbolic graph → schema-correct offline quest fixture.
 *
 * The committed design graph (state/silent_bastion_phase1_graph.json) is symbolic and
 * explicitly non-executable. This module compiles it 1:1 into the pinned engine's own
 * objective schemas (DialogObjective, InstantStartBattleObjective, ResetQuestObjective,
 * InstantWinLoseObjective), then the suites run the engine's validators and runtime on it.
 *
 * Nothing here is a production manifest: AI ids are local fixture users, the reward is a
 * single sentinel item used only to count payouts, and every starting effect is a
 * HARNESS PLACEHOLDER (see PLACEHOLDER_EFFECTS) because the design leaves magnitudes open.
 */
import { readFileSync } from "node:fs";
import { join } from "node:path";
import {
  type AllObjectivesType,
  DialogObjective,
  InstantStartBattleObjective,
  InstantWinLoseObjective,
  ResetQuestObjective,
} from "@/validators/objectives";
import { ObjectiveReward } from "@/validators/rewards";

export const REPO = process.env.TNR_REPO ?? join(import.meta.dir, "../../../../../../..");
/** TNR_GRAPH (repo-relative) selects another symbolic graph, e.g. the condensed 99-node candidate. */
export const GRAPH_PATH = join(REPO, process.env.TNR_GRAPH ?? "state/silent_bastion_phase1_graph.json");

export type SymNode = {
  id: string;
  kind: "dialog" | "battle" | "reset" | "win" | "fail";
  next?: string;
  choices?: { label: string; to: string }[];
  encounterSlot?: string;
  onWin?: string;
  onLoss?: string;
  startPoolsPercent?: number;
  startEffect?: string;
  resetTo?: string;
  /** Condensed-99 spelling of resetTo. */
  resetTarget?: string;
  division?: number;
  lane?: "n" | "r";
  route?: string;
  regular?: number;
};
export type SymGraph = { entry?: string; root?: string; revision?: string; nodes: SymNode[]; [k: string]: unknown };

export const loadGraph = (): SymGraph => JSON.parse(readFileSync(GRAPH_PATH, "utf8"));

/** Fixture AI user id for an encounter slot, e.g. D3.REG2 → sb-ai-d3-reg2. */
export const aiIdForSlot = (slot: string) => `sb-ai-${slot.toLowerCase().replace(".", "-")}`;
export const ENTRY_ITEM_ID = "sb-skyglass-signal-beacon";
export const QUEST_ID = "sb-phase1-pyramid";
/**
 * Sentinel completion reward item: used only to count quest payouts (battle settlement ryo/XP
 * is ordinary combat income and cannot distinguish quest rewards). Not a reward proposal.
 */
export const SENTINEL_ITEM_ID = "sb-sentinel-completion-reward";

/**
 * HARNESS PLACEHOLDERS — not proposals, not balance. The design leaves Security Alert and every
 * Combat Protocol magnitude open (release plan §4.1–4.2). Divisions I–IV use the latest Discord
 * list's tag types only so the route mechanics can be exercised; Division V's advertised
 * `clearprevent` is NOT authorable as a quest starting buff at the pin (proved separately in
 * p1_static), so its route carries a stand-in until the director chooses.
 */
export const PLACEHOLDER_EFFECTS: Record<string, { kind: "buff" | "debuff"; tag: Record<string, unknown> }> = {
  SECURITY_ALERT_TBD: { kind: "debuff", tag: { type: "increasedamagetaken", rounds: 2, power: 10, calculation: "percentage" } },
  COMBAT_PROTOCOL_D1_TBD: { kind: "buff", tag: { type: "decreasedamagetaken", rounds: 3, power: 20, calculation: "percentage" } },
  COMBAT_PROTOCOL_D2_TBD: { kind: "buff", tag: { type: "stunprevent", rounds: 2, power: 100, calculation: "percentage" } },
  COMBAT_PROTOCOL_D3_TBD: { kind: "buff", tag: { type: "increasedamagegiven", rounds: 3, power: 25, calculation: "percentage" } },
  COMBAT_PROTOCOL_D4_TBD: { kind: "buff", tag: { type: "sealprevent", rounds: 2, power: 100 } },
  // STAND-IN for the unsupported advertised Clear Prevent; director decision open.
  COMBAT_PROTOCOL_D5_TBD: { kind: "buff", tag: { type: "debuffprevent", rounds: 3, power: 100 } },
};

export const DIALOG_CONTINUE = "Continue";

/** Compile one symbolic node into the pinned engine's objective schema. */
export const compileNode = (n: SymNode): AllObjectivesType => {
  switch (n.kind) {
    case "dialog":
      return DialogObjective.parse({
        id: n.id,
        task: "dialog",
        description: `[fixture] ${n.id}`,
        nextObjectiveId: n.next
          ? [{ text: DIALOG_CONTINUE, nextObjectiveId: n.next }]
          : (n.choices ?? []).map((c) => ({ text: c.label, nextObjectiveId: c.to })),
      });
    case "battle": {
      const effect = n.startEffect ? PLACEHOLDER_EFFECTS[n.startEffect] : undefined;
      if (n.startEffect && !effect) throw new Error(`No placeholder for ${n.startEffect}`);
      return InstantStartBattleObjective.parse({
        id: n.id,
        task: "start_battle",
        description: `[fixture] ${n.id}`,
        opponentAIs: [{ ids: [aiIdForSlot(n.encounterSlot!)], number: 1 }],
        nextObjectiveId: n.onWin,
        failObjectiveId: n.onLoss,
        ...(n.startPoolsPercent !== undefined ? { givePools: n.startPoolsPercent } : {}),
        ...(effect?.kind === "buff" ? { applyBuffs: [effect.tag] } : {}),
        ...(effect?.kind === "debuff" ? { applyDebuffs: [effect.tag] } : {}),
      });
    }
    case "reset":
      return ResetQuestObjective.parse({ id: n.id, task: "reset_quest", resetObjectiveId: n.resetTo ?? n.resetTarget });
    case "win":
      return InstantWinLoseObjective.parse({ id: n.id, task: "win_quest", description: "[fixture] win" });
    case "fail":
      return InstantWinLoseObjective.parse({ id: n.id, task: "fail_quest", description: "[fixture] Arakane defeat" });
  }
};

/**
 * TNR_COMPILED_QUEST (repo-relative) swaps the generated fixture objectives for an authored compiled
 * quest (e.g. state/silent_bastion_authoring/compiled/quest.candidate.json): its symbolic `@ai:<slot>`
 * opponents become the fixture AI ids, then every objective is parsed by the engine's own schemas.
 */
const compiledObjectives = (path: string) => {
  const rec = JSON.parse(readFileSync(join(REPO, path), "utf8")).record;
  return (rec.content.objectives as Record<string, unknown>[]).map((o) => {
    const x = structuredClone(o) as Record<string, unknown> & { opponentAIs?: { ids: string[]; number: number }[] };
    if (x.opponentAIs) x.opponentAIs = x.opponentAIs.map((a) => ({ ...a, ids: a.ids.map((id) => (id.startsWith("@ai:") ? aiIdForSlot(id.slice(4)) : id)) }));
    switch (x.task) {
      case "dialog": return DialogObjective.parse(x);
      case "start_battle": return InstantStartBattleObjective.parse(x);
      case "reset_quest": return ResetQuestObjective.parse(x);
      default: return InstantWinLoseObjective.parse(x);
    }
  });
};
export const compileObjectives = (g: SymGraph = loadGraph()) =>
  process.env.TNR_COMPILED_QUEST ? compiledObjectives(process.env.TNR_COMPILED_QUEST) : g.nodes.map(compileNode);

/** Raw quest record accepted by QuestValidator and insertable into the local test DB. */
export const questRecord = (objectives = compileObjectives()) => ({
  name: "Ghost Ship: The Last Directive [offline fixture]",
  description: "Offline Phase 1 progression fixture. Not a manifest.",
  successDescription: "Offline fixture complete.",
  questType: "battlepyramid" as const,
  hidden: false,
  consecutiveObjectives: true,
  maxAttempts: 100,
  maxCompletes: 100,
  tierLevel: null,
  endsAt: null,
  startsAt: null,
  content: {
    isolated: true,
    entryItems: [{ ids: [ENTRY_ITEM_ID], number: 1 }],
    objectives,
    reward: ObjectiveReward.parse({ reward_items: [{ ids: [SENTINEL_ITEM_ID], number: 100, quantity: 1 }] }),
    sceneBackground: "",
    sceneCharacters: [],
  },
});

export const encounterSlots = (g: SymGraph = loadGraph()) =>
  [...new Set(g.nodes.filter((n) => n.kind === "battle").map((n) => n.encounterSlot!))].sort();
