/**
 * Gate S — the compiled fixture against the pinned engine's own schemas and flow validators.
 * Pure (no DB). Every claim below is evaluated by engine code (QuestValidator,
 * verifyQuestContentForSave, verifyQuestObjectiveFlow, findPredecessor, buildObjectiveEdges)
 * except the topology comparisons, which compare engine-parsed objectives to the design JSON.
 */
import { describe, expect, it } from "bun:test";
import { verifyQuestContentForSave, verifyQuestObjectiveFlow } from "@/libs/quest";
import { buildObjectiveEdges, findPredecessor } from "@/libs/objectives";
import { InstantStartBattleObjective, QuestValidator } from "@/validators/objectives";
import { questBuffTypes } from "@/validators/combat";
import { Evidence, requireClean } from "./lib/report";
import {
  aiIdForSlot, compileObjectives, encounterSlots, GRAPH_PATH, loadGraph,
  PLACEHOLDER_EFFECTS, questRecord, type SymNode,
} from "./lib/graph";

const ev = new Evidence("s_static");
const g = loadGraph();
const objectives = compileObjectives(g);
const byId = new Map(objectives.map((o) => [o.id, o]));
const sym = new Map(g.nodes.map((n) => [n.id, n]));
type O = (typeof objectives)[number] & Record<string, unknown>;

/** Every outgoing edge of a parsed objective (success, dialog option, fail; reset kept apart). */
const outEdges = (o: O) => {
  const e: string[] = [];
  if (Array.isArray(o.nextObjectiveId)) for (const b of o.nextObjectiveId as { nextObjectiveId?: string }[]) b.nextObjectiveId && e.push(b.nextObjectiveId);
  else if (typeof o.nextObjectiveId === "string") e.push(o.nextObjectiveId);
  if (typeof o.failObjectiveId === "string") e.push(o.failObjectiveId);
  return e;
};
const symEdges = (n: SymNode) => [n.next, ...(n.choices ?? []).map((c) => c.to), n.onWin, n.onLoss].filter(Boolean) as string[];

describe("S: schema and flow validators", () => {
  it("QuestValidator accepts the complete battlepyramid record", () => {
    const t0 = performance.now();
    const parsed = QuestValidator.safeParse(questRecord(objectives));
    ev.timing("questValidatorMs", performance.now() - t0);
    ev.check("QuestValidator.safeParse success", parsed.success, parsed.success ? undefined : parsed.error.issues.slice(0, 5));
    expect(parsed.success).toBe(true);
  });
  it("engine flow validators accept the 208-objective consecutive graph", () => {
    const t0 = performance.now();
    const flow = verifyQuestObjectiveFlow(objectives);
    ev.timing("verifyQuestObjectiveFlowMs", performance.now() - t0);
    const save = verifyQuestContentForSave(objectives, true);
    ev.check("verifyQuestObjectiveFlow check", flow.check, flow.message);
    ev.check("verifyQuestContentForSave(consecutive) check", save.check, save.message);
    expect(flow.check && save.check).toBe(true);
  });
  it("counts match the design and every node compiled 1:1", () => {
    const tasks: Record<string, number> = {};
    for (const o of objectives) tasks[o.task] = (tasks[o.task] ?? 0) + 1;
    ev.put("objectiveTaskCounts", tasks);
    ev.put("graphSource", GRAPH_PATH.split("/").slice(-2).join("/"));
    ev.check("208 objectives", objectives.length === 208, objectives.length);
    ev.check("111 dialog / 90 start_battle / 5 reset_quest / 1 win / 1 fail",
      tasks.dialog === 111 && tasks.start_battle === 90 && tasks.reset_quest === 5 && tasks.win_quest === 1 && tasks.fail_quest === 1, tasks);
    ev.check("unique ids", byId.size === objectives.length);
    let topologyMismatch: string[] = [];
    for (const n of g.nodes) {
      const a = outEdges(byId.get(n.id) as O).sort().join(","), b = symEdges(n).sort().join(",");
      if (a !== b) topologyMismatch.push(n.id);
      if (n.kind === "reset" && (byId.get(n.id) as O).resetObjectiveId !== n.resetTo) topologyMismatch.push(`${n.id}:reset`);
    }
    ev.check("compiled edges equal symbolic edges for all 208 nodes", topologyMismatch.length === 0, topologyMismatch);
  });
});

describe("S: progression structure via engine helpers", () => {
  it("single root, found by the runtime's own predecessor search", () => {
    const roots = objectives.filter((o) => !findPredecessor(objectives, o.id)).map((o) => o.id);
    ev.check("exactly one objective without predecessor", roots.length === 1, roots);
    ev.check("runtime root is design entry d1.n.f1", roots[0] === g.entry && g.entry === "d1.n.f1", roots);
    const edges = buildObjectiveEdges(objectives, true);
    ev.put("logbookGraphEdges", { total: edges.length, fail: edges.filter((e) => e.classes === "fail-edge").length, reset: edges.filter((e) => e.classes === "reset-edge").length });
  });
  it("every battle is gated by exactly one dialog and nothing else", () => {
    const inEdges = new Map<string, string[]>();
    for (const o of objectives) for (const t of outEdges(o as O)) inEdges.set(t, [...(inEdges.get(t) ?? []), o.id]);
    const bad: unknown[] = [];
    const battles = objectives.filter((o) => o.task === "start_battle");
    for (const b of battles) {
      const preds = inEdges.get(b.id) ?? [];
      if (preds.length !== 1 || byId.get(preds[0]!)?.task !== "dialog") bad.push({ battle: b.id, preds });
      const pred = byId.get(preds[0]!) as O;
      if (pred && (pred.nextObjectiveId as unknown[]).length !== 1) bad.push({ battle: b.id, gate: pred.id, note: "gate dialog has >1 option" });
    }
    ev.check("90/90 battles: single predecessor, a single-option dialog", bad.length === 0 && battles.length === 90, bad);
    const battleToBattle = battles.flatMap((b) => outEdges(b as O).filter((t) => byId.get(t)?.task === "start_battle").map((t) => `${b.id}->${t}`));
    ev.check("no battle routes directly into another battle (win or loss)", battleToBattle.length === 0, battleToBattle);
    const reset = objectives.filter((o) => o.task === "reset_quest");
    const resetInto = reset.flatMap((r) => (inEdges.get(r.id) ?? []).filter((p) => !p.includes(".r.")));
    ev.check("reset_quest reachable only from retry-lane battles", resetInto.length === 0, resetInto);
  });
  it("three terminal routes per division (+2 wrong-answer puzzle options) on both lanes", () => {
    const bad: string[] = [];
    for (let d = 1; d <= 5; d++) for (const lane of ["n", "r"]) {
      const term = byId.get(`d${d}.${lane}.terminal`) as O;
      const opts = (term?.nextObjectiveId as { text: string; nextObjectiveId: string }[]) ?? [];
      const want = [`d${d}.${lane}.puzzle`, `d${d}.${lane}.f4.medical`, `d${d}.${lane}.f4.combat`];
      if (opts.map((o) => o.nextObjectiveId).join() !== want.join()) bad.push(`${term?.id}`);
      const puzzle = byId.get(`d${d}.${lane}.puzzle`) as O;
      const p = (puzzle?.nextObjectiveId as { nextObjectiveId: string }[]).map((o) => o.nextObjectiveId);
      if (p.length !== 3 || p[0] !== `d${d}.${lane}.boss.clean` || p[1] !== `d${d}.${lane}.boss.alert` || p[2] !== `d${d}.${lane}.boss.alert`) bad.push(`${puzzle?.id}`);
      // terminal is entered only after regular fight 3
      const preds = objectives.filter((o) => outEdges(o as O).includes(term.id)).map((o) => o.id);
      if (preds.join() !== `b${d}.${lane}.f3`) bad.push(`${term.id}<-${preds}`);
    }
    ev.check("10 terminals × (Maintenance, Medical, Combat); puzzles 1 correct + 2 wrong; terminal after fight 3", bad.length === 0, bad);
  });
  it("battle-start pools: 50 only on retry first fights, 75 only on Medical commanders, absent elsewhere", () => {
    const withPools = objectives.filter((o) => o.task === "start_battle" && (o as O).givePools !== undefined)
      .map((o) => `${o.id}=${(o as O).givePools}`).sort();
    const want = [1, 2, 3, 4, 5].flatMap((d) => [`b${d}.r.f1=50`, `b${d}.n.boss.medical=75`, `b${d}.r.boss.medical=75`]).sort();
    ev.put("givePoolsObjectives", withPools);
    ev.check("exactly 15 givePools objectives (5×50 retry entry, 10×75 Medical)", withPools.join() === want.join(), withPools);
  });
  it("starting effects only on Security Alert and Combat Protocol commander battles", () => {
    const fx = objectives.filter((o) => o.task === "start_battle" && (((o as O).applyBuffs as unknown[]).length || ((o as O).applyDebuffs as unknown[]).length));
    const bad = fx.filter((o) => !/^b\d\.[nr]\.boss\.(alert|combat)$/.test(o.id)).map((o) => o.id);
    ev.check("20 effect battles, all alert/combat commanders", fx.length === 20 && bad.length === 0, { count: fx.length, bad });
    const alertDebuffOnly = fx.filter((o) => o.id.endsWith(".alert")).every((o) => ((o as O).applyBuffs as unknown[]).length === 0 && ((o as O).applyDebuffs as unknown[]).length === 1);
    const combatBuffOnly = fx.filter((o) => o.id.endsWith(".combat")).every((o) => ((o as O).applyDebuffs as unknown[]).length === 0 && ((o as O).applyBuffs as unknown[]).length === 1);
    ev.check("alert = one player debuff; combat = one player buff", alertDebuffOnly && combatBuffOnly);
    ev.put("placeholderEffects", PLACEHOLDER_EFFECTS);
  });
  it("25 encounter identities; each slot is the same single AI on every lane/route", () => {
    const slots = encounterSlots(g);
    const bad = objectives.filter((o) => o.task === "start_battle").filter((o) => {
      const ids = ((o as O).opponentAIs as { ids: string[]; number: number }[]);
      return ids.length !== 1 || ids[0]!.ids.length !== 1 || ids[0]!.number !== 1 || ids[0]!.ids[0] !== aiIdForSlot(sym.get(o.id)!.encounterSlot!);
    }).map((o) => o.id);
    ev.check("25 encounter slots", slots.length === 25, slots);
    ev.check("90 battles each fight exactly one copy of their slot AI", bad.length === 0, bad);
  });
});

describe("S: path enumeration over the engine-parsed objectives", () => {
  it("all successful selections: 3,125 paths, 20–25 battles, 5 commanders, single ending", () => {
    // Follow success edges (dialog options, battle nextObjectiveId) from the root; losses excluded.
    const succ = (o: O): string[] => Array.isArray(o.nextObjectiveId)
      ? (o.nextObjectiveId as { nextObjectiveId: string }[]).map((b) => b.nextObjectiveId)
      : typeof o.nextObjectiveId === "string" ? [o.nextObjectiveId] : [];
    let paths = 0; const lengths = new Set<number>(); const bad: string[] = [];
    const walk = (id: string, battles: number, bosses: number, trail: string[]) => {
      const o = byId.get(id) as O;
      const nb = battles + (o.task === "start_battle" ? 1 : 0);
      const nboss = bosses + (o.task === "start_battle" && id.includes(".boss.") ? 1 : 0);
      if (o.task === "fail_quest" || o.task === "reset_quest") { bad.push(`success path reached ${id}`); return; }
      if (o.task === "win_quest") {
        paths++; lengths.add(nb);
        if (nboss !== 5) bad.push(`${trail.join(">")} bosses=${nboss}`);
        if (trail.some((t) => t.includes(".r."))) bad.push(`success path entered retry lane: ${id}`);
        return;
      }
      for (const n of succ(o)) walk(n, nb, nboss, trail.length < 400 ? [...trail, id] : trail);
    };
    walk(g.entry, 0, 0, []);
    ev.put("successPaths", { count: paths, battleCounts: [...lengths].sort() });
    ev.check("3,125 successful selection paths, each ending at w.complete via d.aftermath", paths === 3125 && bad.length === 0, bad.slice(0, 5));
    ev.check("successful path length 20–25 battles", [...lengths].sort().join() === "20,21,22,23,24,25", [...lengths]);
  });
  it("loss edges: same-division retry entry, retry reset, Arakane hard fail; commander wins join next n lane", () => {
    const bad: string[] = [];
    for (const o of objectives.filter((x) => x.task === "start_battle") as O[]) {
      const [b, lane] = o.id.split(".");
      const d = Number(b!.slice(1));
      const arakane = d === 5 && o.id.includes(".boss.");
      const wantFail = arakane ? "f.arakane" : lane === "n" ? `d${d}.r.f1` : `r${d}.retry`;
      if (o.failObjectiveId !== wantFail) bad.push(`${o.id} fail→${o.failObjectiveId}`);
      if (o.id.includes(".boss.")) {
        const wantWin = d === 5 ? "d.aftermath" : `d${d + 1}.n.f1`;
        if (o.nextObjectiveId !== wantWin) bad.push(`${o.id} win→${o.nextObjectiveId}`);
      }
    }
    for (const o of objectives.filter((x) => x.task === "reset_quest") as O[])
      if (o.resetObjectiveId !== `d${o.id[1]}.r.f1`) bad.push(`${o.id} reset→${o.resetObjectiveId}`);
    ev.check("all 90 fail edges, 25 commander win edges and 5 reset targets as designed", bad.length === 0, bad);
  });
});

describe("S: source contract findings the design depends on", () => {
  it("Arakane Combat Protocol as advertised (clearprevent) is rejected by the starting-buff allowlist", () => {
    const r = InstantStartBattleObjective.safeParse({ id: "x", task: "start_battle", opponentAIs: [{ ids: ["a"], number: 1 }],
      applyBuffs: [{ type: "clearprevent", rounds: 3, power: 100, calculation: "percentage" }] });
    ev.check("clearprevent not in questBuffTypes", !(questBuffTypes as readonly string[]).includes("clearprevent"));
    ev.check("start_battle with applyBuffs clearprevent fails schema", !r.success, r.success ? null : r.error.issues.map((i) => i.message));
    const n = { ...g.nodes.find((x) => x.id === "b5.n.boss.combat")! };
    const recs = compileObjectives(g).map((o) => o.id === n.id ? { ...o, applyBuffs: [{ type: "clearprevent", rounds: 3, power: 100, calculation: "percentage" }] } : o);
    ev.check("whole quest with advertised Arakane protocol fails QuestValidator", !QuestValidator.safeParse(questRecord(recs as never)).success);
  });
  it("placeholder effect types are inside the engine allowlists", () => {
    for (const [k, v] of Object.entries(PLACEHOLDER_EFFECTS)) {
      const r = InstantStartBattleObjective.safeParse({ id: k, task: "start_battle", opponentAIs: [{ ids: ["a"], number: 1 }],
        [v.kind === "buff" ? "applyBuffs" : "applyDebuffs"]: [v.tag] });
      ev.check(`placeholder ${k} (${v.tag.type}) authorable`, r.success);
    }
  });
  it("validator rejects a second root and a non-reset cycle (negative controls)", () => {
    const orphan = [...objectives, { ...objectives.find((o) => o.id === "d1.n.f2")!, id: "orphan" }];
    ev.check("extra root rejected", !verifyQuestObjectiveFlow(orphan as never).check, verifyQuestObjectiveFlow(orphan as never).message.slice(0, 80));
    const cyc = objectives.map((o) => o.id === "b1.r.f1" ? { ...o, failObjectiveId: "d1.r.f1" } : o);
    ev.check("loss edge back into the retry lane (no reset) rejected as a cycle", verifyQuestObjectiveFlow(cyc as never).message === "Cycle detected in objective chain");
  });
});

requireClean(ev);
