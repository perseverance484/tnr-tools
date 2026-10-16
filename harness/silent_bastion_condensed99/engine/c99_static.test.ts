/**
 * Gate S — the compiled condensed graph against the pinned engine's own schemas, flow validators
 * and graph helpers. Pure (no DB). Expected counts come from the graph's own `counts` block; the
 * structural rules come from docs/handoffs/SILENT_BASTION_CONDENSED99_NATIVE_PROOF_BRIEF.md.
 */
import { describe, expect, it } from "bun:test";
import { verifyQuestContentForSave, verifyQuestObjectiveFlow } from "@/libs/quest";
import { buildObjectiveEdges, findPredecessor } from "@/libs/objectives";
import { InstantStartBattleObjective, QuestValidator } from "@/validators/objectives";
import { questBuffTypes } from "@/validators/combat";
import { Evidence, requireClean } from "./lib/report";
import { aiIdForSlot, compileObjectives, encounterSlots, GRAPH_PATH, loadGraph, PLACEHOLDER_EFFECTS, questRecord, type SymNode } from "./lib/graph";
import { DIVS, ROOT } from "./lib/run99";

const ev = new Evidence("s_static");
const g = loadGraph();
const counts = g.counts as Record<string, number>;
const objectives = compileObjectives(g);
const byId = new Map(objectives.map((o) => [o.id, o]));
const sym = new Map(g.nodes.map((n) => [n.id, n]));
type O = (typeof objectives)[number] & Record<string, unknown>;

const outEdges = (o: O) => {
  const e: string[] = [];
  if (Array.isArray(o.nextObjectiveId)) for (const b of o.nextObjectiveId as { nextObjectiveId?: string }[]) b.nextObjectiveId && e.push(b.nextObjectiveId);
  else if (typeof o.nextObjectiveId === "string") e.push(o.nextObjectiveId);
  if (typeof o.failObjectiveId === "string") e.push(o.failObjectiveId);
  return e;
};
const symEdges = (n: SymNode) => [n.next, ...(n.choices ?? []).map((c) => c.to), n.onWin, n.onLoss].filter(Boolean) as string[];
const inEdges = new Map<string, string[]>();
for (const o of objectives) for (const t of outEdges(o as O)) inEdges.set(t, [...(inEdges.get(t) ?? []), o.id]);
const task = (id: string) => byId.get(id)?.task;
/** Follow single-next dialogs from `id` to the first non-gate objective. */
const through = (id: string) => {
  let cur = id;
  while (task(cur) === "dialog" && (byId.get(cur) as O).nextObjectiveId && ((byId.get(cur) as O).nextObjectiveId as unknown[]).length === 1 && /\.(f4|boss\.(clean|alert))$/.test(cur))
    cur = ((byId.get(cur) as O).nextObjectiveId as { nextObjectiveId: string }[])[0]!.nextObjectiveId;
  return cur;
};

describe("S: schema and flow validators", () => {
  it("QuestValidator accepts the complete battlepyramid record", () => {
    const t0 = performance.now();
    const parsed = QuestValidator.safeParse(questRecord(objectives));
    ev.timing("questValidatorMs", performance.now() - t0);
    ev.check("QuestValidator.safeParse success", parsed.success, parsed.success ? undefined : parsed.error.issues.slice(0, 5));
    expect(parsed.success).toBe(true);
  });
  it("engine flow validators accept the consecutive graph", () => {
    const flow = verifyQuestObjectiveFlow(objectives);
    const save = verifyQuestContentForSave(objectives, true);
    ev.check("verifyQuestObjectiveFlow check (single root, no cycles, resolved references)", flow.check, flow.message);
    ev.check("verifyQuestContentForSave(consecutive) check", save.check, save.message);
    expect(flow.check && save.check).toBe(true);
  });
  it("counts match the graph's declared counts and every node compiled 1:1", () => {
    const tasks: Record<string, number> = {};
    for (const o of objectives) tasks[o.task] = (tasks[o.task] ?? 0) + 1;
    ev.put("graph", { path: GRAPH_PATH.split("/").slice(-3).join("/"), variant: g.variant ?? "candidate", declaredCounts: counts });
    ev.put("objectiveTaskCounts", tasks);
    ev.check(`${counts.total} objectives (<= 100 budget)`, objectives.length === counts.total && objectives.length <= 100, objectives.length);
    ev.check("task counts equal declared dialog/battle/reset/win/fail counts",
      tasks.dialog === counts.dialogs && tasks.start_battle === counts.battles && tasks.reset_quest === counts.resets && tasks.win_quest === 1 && tasks.fail_quest === 1, tasks);
    ev.check("unique ids", byId.size === objectives.length);
    const mismatch: string[] = [];
    for (const n of g.nodes) {
      if (outEdges(byId.get(n.id) as O).sort().join() !== symEdges(n).sort().join()) mismatch.push(n.id);
      if (n.kind === "reset" && (byId.get(n.id) as O).resetObjectiveId !== (n.resetTarget ?? n.resetTo)) mismatch.push(`${n.id}:reset`);
    }
    ev.check("compiled edges and reset targets equal the symbolic graph", mismatch.length === 0, mismatch);
  });
});

describe("S: structure via engine helpers", () => {
  it("single root found by the runtime's own predecessor search", () => {
    const roots = objectives.filter((o) => !findPredecessor(objectives, o.id)).map((o) => o.id);
    ev.check(`exactly one root, the declared ${ROOT}`, roots.length === 1 && roots[0] === ROOT && ROOT === "d2.n.f1", roots);
    const edges = buildObjectiveEdges(objectives, true);
    ev.put("logbookGraphEdges", { total: edges.length, fail: edges.filter((e) => e.classes === "fail-edge").length, reset: edges.filter((e) => e.classes === "reset-edge").length });
  });
  it("every battle is gated by a dialog; no battle routes into a battle", () => {
    const battles = objectives.filter((o) => o.task === "start_battle");
    const bad = battles.map((b) => ({ battle: b.id, preds: inEdges.get(b.id) ?? [] })).filter((x) => x.preds.length === 0 || x.preds.some((p) => task(p) !== "dialog"));
    ev.check(`${battles.length}/${counts.battles} battles have only dialog predecessors`, bad.length === 0 && battles.length === counts.battles, bad);
    const b2b = battles.flatMap((b) => outEdges(b as O).filter((t) => task(t) === "start_battle").map((t) => `${b.id}->${t}`));
    ev.check("no battle win/loss edge targets a battle", b2b.length === 0, b2b);
  });
  it("hazard lint: reset_quest on a battle WIN edge (pre-selected while the fight is pending)", () => {
    const hazard = objectives.filter((o) => o.task === "start_battle" && task((o as O).nextObjectiveId as string) === "reset_quest").map((o) => `${o.id}->${(o as O).nextObjectiveId}`);
    ev.put("battleWinEdgesIntoReset", hazard);
    ev.finding("C1-static", "start_battle nextObjectiveId (WIN edge) targets a reset_quest; the engine pre-selects that edge while the fight is pending (quest.ts selectedNextObjectiveId preset), so the reset becomes available at battle start — runtime effect proven in gate D",
      hazard.length > 0, hazard);
  });
  it("recovery templates: 50% REG1 copy, dialog-gated, resets on the designed targets", () => {
    const bad: string[] = [];
    for (const d of DIVS) {
      const rf = byId.get(`b${d}.recovery_first`) as O, rl = byId.get(`b${d}.recovery_later`) as O;
      if (!rf || !rl) { bad.push(`D${d} missing recovery battle`); continue; }
      for (const r of [rf, rl]) {
        if (r.givePools !== 50) bad.push(`${r.id} givePools ${r.givePools}`);
        if (sym.get(r.id)!.encounterSlot !== `D${d}.REG1`) bad.push(`${r.id} slot`);
      }
      if ((inEdges.get(rf.id) ?? []).join() !== `d${d}.lost_first`) bad.push(`${rf.id} preds`);
      if ((inEdges.get(rl.id) ?? []).join() !== `d${d}.lost_later`) bad.push(`${rl.id} preds`);
      if (rf.nextObjectiveId !== `d${d}.n.f2` || rf.failObjectiveId !== `r${d}.reset_first`) bad.push(`${rf.id} edges`);
      const winTo = rl.nextObjectiveId as string;
      const resetWin = task(winTo) === "dialog" ? ((byId.get(winTo) as O).nextObjectiveId as { nextObjectiveId: string }[])[0]!.nextObjectiveId : winTo;
      if (resetWin !== `r${d}.reset_later_win` || rl.failObjectiveId !== `r${d}.reset_later_loss`) bad.push(`${rl.id} edges`);
      const want: Record<string, string> = { [`r${d}.reset_first`]: `d${d}.lost_first`, [`r${d}.reset_later_win`]: `d${d}.n.f2`, [`r${d}.reset_later_loss`]: `d${d}.lost_later` };
      for (const [r, t] of Object.entries(want)) if ((byId.get(r) as O)?.resetObjectiveId !== t) bad.push(`${r} -> ${(byId.get(r) as O)?.resetObjectiveId}`);
    }
    ev.check("4 divisions × (recovery_first, recovery_later): 50% REG1, gated by lost_first/lost_later, resets to lost_first / d.n.f2 / lost_later", bad.length === 0, bad);
    // Each reset target is a forward ancestor of its reset node (a rewind, never a jump ahead).
    const reach = (from: string, to: string) => { const seen = new Set<string>(); const st = [from]; while (st.length) { const x = st.pop()!; if (x === to) return true; if (seen.has(x)) continue; seen.add(x); st.push(...outEdges(byId.get(x) as O)); } return false; };
    const notRewind = objectives.filter((o) => o.task === "reset_quest").filter((r) => !reach((r as O).resetObjectiveId as string, r.id)).map((r) => r.id);
    ev.check("every reset target can reach its reset node (rewind only)", notRewind.length === 0, notRewind);
    const resetPreds = objectives.filter((o) => o.task === "reset_quest").flatMap((r) => (inEdges.get(r.id) ?? []).filter((p) => !/recovery_(first|later)$|\.recovered$/.test(p)).map((p) => `${p}->${r.id}`));
    ev.check("reset_quest entered only from recovery battles (or their confirmation dialog)", resetPreds.length === 0, resetPreds);
  });
  it("normal-lane loss and win edges", () => {
    const bad: string[] = [];
    for (const o of objectives.filter((x) => x.task === "start_battle" && /^b\d\.n\./.test(x.id)) as O[]) {
      const d = Number(o.id[1]);
      const boss = o.id.includes(".boss.");
      const want = d === 5 && boss ? "f.arakane" : o.id.endsWith(".f1") ? `d${d}.lost_first` : `d${d}.lost_later`;
      if (o.failObjectiveId !== want) bad.push(`${o.id} loss->${o.failObjectiveId}`);
      if (boss && o.nextObjectiveId !== (d === 5 ? "d.aftermath" : `d${d + 1}.n.f1`)) bad.push(`${o.id} win->${o.nextObjectiveId}`);
    }
    ev.check("REG1 loss -> lost_first; REG2-4 and D2-D4 commander loss -> lost_later; Arakane loss -> f.arakane; commander wins -> next division / aftermath", bad.length === 0, bad);
  });
  it("terminal, puzzle and protocol per division", () => {
    const bad: string[] = [];
    for (const d of DIVS) {
      const term = byId.get(`d${d}.n.terminal`) as O;
      const opts = (term.nextObjectiveId as { nextObjectiveId: string }[]).map((x) => x.nextObjectiveId);
      if (opts.length !== 2 || opts[0] !== `d${d}.n.puzzle` || through(opts[1]!) !== `b${d}.n.f4`) bad.push(`${term.id} ${opts}`);
      if ((inEdges.get(term.id) ?? []).join() !== `b${d}.n.f3`) bad.push(`${term.id} preds`);
      const pz = (byId.get(`d${d}.n.puzzle`) as O).nextObjectiveId as { text: string; nextObjectiveId: string }[];
      const pt = pz.map((x) => through(x.nextObjectiveId));
      if (pz.length !== 3 || pt[0] !== `b${d}.n.boss.clean` || pt[1] !== `b${d}.n.boss.alert` || pt[2] !== `b${d}.n.boss.alert`) bad.push(`d${d}.n.puzzle ${pt}`);
      const prot = ((byId.get(`d${d}.n.protocol`) as O).nextObjectiveId as { nextObjectiveId: string }[]).map((x) => x.nextObjectiveId);
      if (prot.join() !== `b${d}.n.boss.medical,b${d}.n.boss.combat`) bad.push(`d${d}.n.protocol ${prot}`);
      if ((inEdges.get(`d${d}.n.protocol`) ?? []).join() !== `b${d}.n.f4` || (byId.get(`b${d}.n.f4`) as O).nextObjectiveId !== `d${d}.n.protocol`) bad.push(`D${d} protocol only after the fourth fight`);
      const order = objectives.map((o) => o.id);
      if (order.indexOf(`b${d}.n.f4`) > order.indexOf(`b${d}.n.boss.medical`)) bad.push(`b${d}.n.f4 listed after its commander`);
    }
    ev.check("4 terminals (after REG3): Maintenance puzzle or the fourth fight; puzzle 1 correct -> clean + 2 wrong -> alert; post-fourth-fight protocol -> Medical/Combat", bad.length === 0, bad);
  });
  it("battle-start pools and starting effects", () => {
    const withPools = objectives.filter((o) => o.task === "start_battle" && (o as O).givePools !== undefined).map((o) => `${o.id}=${(o as O).givePools}`).sort();
    const want = DIVS.flatMap((d) => [`b${d}.recovery_first=50`, `b${d}.recovery_later=50`, `b${d}.n.boss.medical=100`]).sort();
    ev.put("givePoolsObjectives", withPools);
    ev.check("12 givePools objectives: 8×50 recovery REG1, 4×100 Medical", withPools.join() === want.join(), withPools);
    const fx = objectives.filter((o) => o.task === "start_battle" && (((o as O).applyBuffs as unknown[]).length || ((o as O).applyDebuffs as unknown[]).length));
    const badFx = fx.filter((o) => !/^b\d\.n\.boss\.(alert|combat)$/.test(o.id)).map((o) => o.id);
    const shape = fx.every((o) => o.id.endsWith(".alert") ? ((o as O).applyBuffs as unknown[]).length === 0 && ((o as O).applyDebuffs as unknown[]).length === 1 : ((o as O).applyDebuffs as unknown[]).length === 0 && ((o as O).applyBuffs as unknown[]).length === 1);
    ev.check("8 effect battles (4 alert debuff, 4 combat buff), none elsewhere", fx.length === 8 && badFx.length === 0 && shape, { count: fx.length, badFx });
    ev.put("placeholderEffects", PLACEHOLDER_EFFECTS);
  });
  it("20 encounter identities, one AI copy per battle", () => {
    const slots = encounterSlots(g);
    const bad = objectives.filter((o) => o.task === "start_battle").filter((o) => {
      const ids = (o as O).opponentAIs as { ids: string[]; number: number }[];
      return ids.length !== 1 || ids[0]!.ids.length !== 1 || ids[0]!.number !== 1 || ids[0]!.ids[0] !== aiIdForSlot(sym.get(o.id)!.encounterSlot!);
    }).map((o) => o.id);
    ev.check("20 encounter slots (16 regular + 4 commanders), no Gatewarden/D1", slots.length === 20 && !slots.some((s) => s.startsWith("D1.")), slots);
    ev.check("every battle fights exactly one copy of its slot AI", bad.length === 0, bad);
  });
});

describe("S: path enumeration over engine-parsed objectives", () => {
  it("all successful selections: 625 paths, 16-20 battles, four commanders, one ending", () => {
    const succ = (o: O): string[] => Array.isArray(o.nextObjectiveId) ? (o.nextObjectiveId as { nextObjectiveId: string }[]).map((b) => b.nextObjectiveId) : typeof o.nextObjectiveId === "string" ? [o.nextObjectiveId] : [];
    let paths = 0; const lengths = new Set<number>(); const bad: string[] = [];
    const walk = (id: string, battles: number, bosses: number, depth: number) => {
      const o = byId.get(id) as O;
      const nb = battles + (o.task === "start_battle" ? 1 : 0);
      const nboss = bosses + (o.task === "start_battle" && id.includes(".boss.") ? 1 : 0);
      if (o.task === "fail_quest" || o.task === "reset_quest" || id.includes("recover") || id.includes("lost_")) { bad.push(`success path reached ${id}`); return; }
      if (o.task === "win_quest") { paths++; lengths.add(nb); if (nboss !== 4) bad.push(`bosses=${nboss}`); return; }
      if (depth > 200) { bad.push("depth"); return; }
      for (const n of succ(o)) walk(n, nb, nboss, depth + 1);
    };
    walk(ROOT, 0, 0, 0);
    ev.put("successPaths", { count: paths, battleCounts: [...lengths].sort() });
    ev.check("625 successful selection paths (5 per division: clean, alert×2 wrong answers, medical, combat), each with 4 commanders, ending at w.complete", paths === 625 && bad.length === 0, bad.slice(0, 5));
    ev.check("successful path length 16-20 battles", [...lengths].sort().join() === "16,17,18,19,20", [...lengths]);
  });
});

describe("S: source contract checks", () => {
  it("negative controls: second root and a reset-free rewind are rejected", () => {
    const orphan = [...objectives, { ...objectives.find((o) => o.id === "d2.n.f2")!, id: "orphan" }];
    ev.check("extra root rejected", !verifyQuestObjectiveFlow(orphan as never).check);
    // Drop the reset (and an option's confirmation dialog) so the only change is the direct back edge.
    const cyc = objectives.filter((o) => o.id !== "r2.reset_later_win" && o.id !== "d2.recovered")
      .map((o) => (o.id === "b2.recovery_later" ? { ...o, nextObjectiveId: "d2.n.f2" } : o));
    ev.check("recovery WIN edge straight back to d2.n.f2 (no reset_quest) rejected as a cycle", verifyQuestObjectiveFlow(cyc as never).message === "Cycle detected in objective chain", verifyQuestObjectiveFlow(cyc as never).message);
  });
  it("advertised Arakane clearprevent Combat Protocol still not authorable", () => {
    const r = InstantStartBattleObjective.safeParse({ id: "x", task: "start_battle", opponentAIs: [{ ids: ["a"], number: 1 }], applyBuffs: [{ type: "clearprevent", rounds: 3, power: 100, calculation: "percentage" }] });
    ev.check("clearprevent not in questBuffTypes at the pin", !(questBuffTypes as readonly string[]).includes("clearprevent"));
    ev.check("start_battle with applyBuffs clearprevent fails schema", !r.success);
  });
  it("placeholder effect types are inside the engine allowlists", () => {
    for (const [k, v] of Object.entries(PLACEHOLDER_EFFECTS)) {
      if (k === "COMBAT_PROTOCOL_D1_TBD") continue;
      const r = InstantStartBattleObjective.safeParse({ id: k, task: "start_battle", opponentAIs: [{ ids: ["a"], number: 1 }], [v.kind === "buff" ? "applyBuffs" : "applyDebuffs"]: [v.tag] });
      ev.check(`placeholder ${k} (${v.tag.type}) authorable`, r.success);
    }
  });
});

requireClean(ev);
