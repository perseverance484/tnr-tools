/**
 * Gate C — the compiled candidate quest (state/silent_bastion_authoring/compiled/quest.candidate.json)
 * and all 20 compiled AI profiles against the pinned engine: schemas, flow, structure vs the locked
 * alt99_f4gate graph, puzzle wiring, protocol targets, the real editor save, the real AI-profile
 * save (server rule cap) and Countermand's stored-row validation. Refs are symbolic in the
 * candidate; here they become local fixture ids.
 */
import { beforeEach, describe, expect, it, vi } from "bun:test";
import { readFileSync } from "node:fs";
import { join } from "node:path";
import { eq } from "drizzle-orm";
import { aiProfile, item, quest, userData, userItem } from "@/drizzle/schema";
import { verifyQuestContentForSave, verifyQuestObjectiveFlow } from "@/libs/quest";
import { findPredecessor } from "@/libs/objectives";
import { Pusher } from "@/libs/pusher";
import { verifyRewardChoiceForSave } from "@/libs/rewardChoice";
import { aiRouter } from "@/server/api/routers/ai";
import { fetchItemWithCraftingRequirements, itemRouter } from "@/server/api/routers/item";
import { questsRouter } from "@/server/api/routers/quests";
import { ItemValidator, NonCombatConsumeRewardTag, questBuffTypes, questDebuffTypes } from "@/validators/combat";
import { AiRule } from "@/validators/ai";
import { QuestValidator } from "@/validators/objectives";
import { insertItems, insertUserItems, insertUsers } from "../setup/factories";
import { callerFor, callerForDatabase, describeWithDatabase, getTestDatabase, resetTables } from "../setup/testDatabase";
import { Evidence, requireClean } from "./lib/report";
import { exclusiveId, itemRecord, REPO } from "./lib/units";

const ev = new Evidence("c_content");
const c = (n: string, p: boolean, d?: unknown) => ev.check(n, p, d);
const A = "state/silent_bastion_authoring";
const read = (p: string) => JSON.parse(readFileSync(join(REPO, p), "utf8"));
const lock = read("state/silent_bastion_approved_authoring_lock.json");
const graph = read(lock.selectedGraph.path) as { nodes: { id: string; kind: string; next?: string; choices?: { label: string; to: string }[]; onWin?: string; onLoss?: string; resetTarget?: string; encounterSlot?: string; startPoolsPercent?: number; startEffect?: string }[] };
const compiled = read(`${A}/compiled/quest.candidate.json`);
const profiles = read(`${A}/compiled/ai_profiles.candidate.json`).profiles as { slot: string; key: string; name: string; aiProfile: { rules: Record<string, unknown>[] } }[];
const script = read(`${A}/design/script.json`);
const protocols = read(`${A}/design/protocols.json`);
const entry = read(`${A}/design/entry_and_rewards.json`);
type Bundle = { itemId: string; quantity: number }[];
type CacheOut = { ref: string; srcId: string; entries: Record<string, string[]>; record: Record<string, unknown> & { effects: { weightedCache: { rolls: { probability: number }[]; tiers: { name: string; probability: number; entries: { items: Bundle }[] }[] } }[] } };
const cacheOut = read(`${A}/compiled/cache_items.candidate.json`).caches as CacheOut[];
const pools = read(entry.caches.weightedCache.poolsSource).pools as Record<string, { chosen: { status: string; output: { name: string; rarity: string }; ingredients: { id: string; quantityFull: number; quantityPyramid: number }[] }[] }>;
const bundleKey = (b: Bundle) => JSON.stringify(b.map((x) => [x.itemId, x.quantity]).sort());

/** Symbolic refs → local fixture ids (never live ids). */
const fixtureId = (ref: string) => ref.startsWith("@ai:") ? `sb-ai-${ref.slice(4).toLowerCase().replace(".", "-")}`
  : ref.startsWith("@item:") || ref.startsWith("@jutsu:") ? `sb-${ref.split(":")[1]!.replace(/_/g, "-")}` : ref;
const subst = <T,>(x: T): T => JSON.parse(JSON.stringify(x), (_k, v) => (typeof v === "string" && /^@(ai|item|jutsu|asset):/.test(v) ? (v.startsWith("@asset:") ? "" : fixtureId(v)) : v));
const record = () => subst(structuredClone(compiled.record));
type O = Record<string, unknown> & { id: string; task: string };
const objectives = () => record().content.objectives as O[];
const outs = (o: O) => [...(Array.isArray(o.nextObjectiveId) ? (o.nextObjectiveId as { nextObjectiveId: string }[]).map((x) => x.nextObjectiveId) : typeof o.nextObjectiveId === "string" ? [o.nextObjectiveId] : []),
  ...(typeof o.failObjectiveId === "string" ? [o.failObjectiveId] : [])];

describe("C1 compiled quest: schemas, flow, counts, provenance", () => {
  it("validators", () => {
    const rec = record();
    const parsed = QuestValidator.safeParse(rec);
    c("QuestValidator accepts the compiled candidate (battlepyramid, choose, pick 1, Beacon entry)", parsed.success, parsed.success ? undefined : parsed.error.issues.slice(0, 5));
    const objs = objectives();
    c("verifyQuestObjectiveFlow", verifyQuestObjectiveFlow(objs as never).check, verifyQuestObjectiveFlow(objs as never).message);
    c("verifyQuestContentForSave(consecutive)", verifyQuestContentForSave(objs as never, true).check);
    c("verifyRewardChoiceForSave: 2 cache cards for 1 pick", verifyRewardChoiceForSave(rec.content).check, verifyRewardChoiceForSave(rec.content).message);
    const roots = objs.filter((o) => !findPredecessor(objs as never, o.id)).map((o) => o.id);
    c("single root d2.n.f1", roots.join() === "d2.n.f1", roots);
    const t: Record<string, number> = {};
    for (const o of objs) t[o.task] = (t[o.task] ?? 0) + 1;
    ev.put("taskCounts", t);
    c("99 = 45 dialog + 40 start_battle + 12 reset + 1 win + 1 fail (lock counts)", objs.length === lock.selectedGraph.counts.objectives && t.dialog === 45 && t.start_battle === 40 && t.reset_quest === 12 && t.win_quest === 1 && t.fail_quest === 1, t);
    c("compiled provenance = locked graph sha256", compiled.provenance.graphSha256 === lock.selectedGraph.rawSha256);
  });
  it("structure equals the locked alt99_f4gate graph", () => {
    const by = new Map(objectives().map((o) => [o.id, o]));
    const bad: string[] = [];
    for (const n of graph.nodes) {
      const o = by.get(n.id);
      if (!o) { bad.push(`missing ${n.id}`); continue; }
      const want = [n.next, ...(n.choices ?? []).map((x) => x.to), n.onWin, n.onLoss].filter(Boolean).sort().join();
      if (outs(o).sort().join() !== want) bad.push(`${n.id} edges`);
      if (n.kind === "reset" && o.resetObjectiveId !== n.resetTarget) bad.push(`${n.id} reset`);
      if (n.kind === "battle") {
        const ids = (o.opponentAIs as { ids: string[] }[])[0]!.ids;
        if (ids.join() !== fixtureId(`@ai:${n.encounterSlot}`)) bad.push(`${n.id} opponent`);
        if ((n.startPoolsPercent ?? null) !== ((o.givePools as number | undefined) ?? null)) bad.push(`${n.id} givePools`);
      }
    }
    c("every node, edge, reset target, opponent slot and givePools matches the locked graph", bad.length === 0, bad);
    c("no separate fourth-fight intro: terminal gates bN.n.f4 directly", [2, 3, 4, 5].every((d) => !by.has(`d${d}.n.f4`) && outs(by.get(`d${d}.n.terminal`)!).includes(`b${d}.n.f4`)));
    c("recovery confirmation dialogs dN.recovered present (C1 fix)", [2, 3, 4, 5].every((d) => by.get(`d${d}.recovered`)?.task === "dialog" && (by.get(`b${d}.recovery_later`)!.nextObjectiveId === `d${d}.recovered`)));
    const recovery = graph.nodes.filter((n) => n.kind === "battle" && /\.recovery_(first|later)$/.test(n.id)).map((n) => n.id).sort();
    const parsedObjs = (QuestValidator.parse(record()).content.objectives as unknown as O[]);
    const zero = parsedObjs.filter((o) => o.task === "start_battle" && o.scaleGains === 0).map((o) => o.id).sort();
    const rawSet = objectives().filter((o) => "scaleGains" in o).map((o) => o.id).sort();
    c("scaleGains 0 on exactly the 8 recovery battles after QuestValidator parsing, unset on every other battle (RUL-2026-10-16-005)",
      recovery.length === 8 && zero.join() === recovery.join() && rawSet.join() === recovery.join(), { recovery, zero, rawSet });
    const preds = new Map<string, string[]>();
    for (const o of objectives()) for (const t of outs(o)) preds.set(t, [...(preds.get(t) ?? []), o.id]);
    const ungated = objectives().filter((o) => o.task === "start_battle").filter((o) => (preds.get(o.id) ?? []).some((p) => by.get(p)!.task !== "dialog") || !(preds.get(o.id) ?? []).length).map((o) => o.id);
    c("all 40 battles are dialog-gated", ungated.length === 0, ungated);
  });
  it("text, puzzles, protocols, rewards", () => {
    const objs = objectives(); const by = new Map(objs.map((o) => [o.id, o]));
    const emptyDialog = objs.filter((o) => o.task === "dialog" && (!String(o.description).trim() || (o.nextObjectiveId as { text: string }[]).some((x) => !x.text.trim()))).map((o) => o.id);
    c("45 dialogs: non-empty scene text and option labels", emptyDialog.length === 0, emptyDialog);
    c("40 battles: non-empty objective text", objs.filter((o) => o.task === "start_battle" && !String(o.description).trim()).length === 0);
    const oddQuotes = objs.filter((o) => [String(o.description ?? ""), ...(Array.isArray(o.nextObjectiveId) ? (o.nextObjectiveId as { text: string }[]).map((x) => x.text) : [])]
      .some((t) => (t.match(/"/g) ?? []).length % 2 === 1)).map((o) => o.id);
    c("no objective text or option label has an unbalanced double quote (review F4)", oddQuotes.length === 0, oddQuotes);
    c("12 resets are silent", objs.filter((o) => o.task === "reset_quest" && String(o.description ?? "").trim()).length === 0);
    const puzzle: Record<number, unknown> = {};
    const bad: string[] = [];
    for (const d of [2, 3, 4, 5]) {
      const pz = by.get(`d${d}.n.puzzle`)!.nextObjectiveId as { text: string; nextObjectiveId: string }[];
      const clean = pz.filter((x) => x.nextObjectiveId === `d${d}.n.boss.clean`).length;
      const alert = pz.filter((x) => x.nextObjectiveId === `d${d}.n.boss.alert`).length;
      if (pz.length !== 3 || clean !== 1 || alert !== 2) bad.push(`D${d} wiring`);
      const s = script.objectives[`d${d}.n.puzzle`];
      if (pz.find((x) => x.nextObjectiveId === `d${d}.n.boss.clean`)!.text !== s.options.correct) bad.push(`D${d} correct text not on clean edge`);
      const earlier = [1, 2, 3].map((i) => String(by.get(`d${d}.n.f${i}`)!.description)).join(" ");
      const missing = (s.clues as string[]).filter((x) => !earlier.includes(x));
      if (missing.length) bad.push(`D${d} clues missing from f1–f3: ${missing}`);
      puzzle[d] = { order: pz.map((x) => (x.nextObjectiveId.endsWith("clean") ? "correct" : "wrong")), correctPosition: pz.findIndex((x) => x.nextObjectiveId.endsWith("clean")) + 1 };
    }
    ev.put("puzzles", puzzle);
    c("4 puzzles: 3 options, 1 correct→clean, 2 wrong→alert; correct text on the clean edge; every clue planted in that division's f1–f3", bad.length === 0, bad);
    c("puzzle answers are not always first", new Set(Object.values(puzzle).map((p) => (p as { correctPosition: number }).correctPosition)).size > 1);
    const fx: string[] = [];
    for (const o of objs.filter((x) => x.task === "start_battle")) {
      for (const [f, allowed] of [["applyBuffs", questBuffTypes], ["applyDebuffs", questDebuffTypes]] as const)
        for (const e of (o[f] as { type: string; target?: string }[]) ?? []) {
          if (!(allowed as readonly string[]).includes(e.type)) fx.push(`${o.id} ${e.type} not in allowlist`);
          fx.push(`${o.id}:${f}:${e.type}`);
        }
    }
    ev.put("startingEffects", fx);
    const want = [2, 3, 4, 5].flatMap((d) => [`b${d}.n.boss.alert:applyDebuffs:${protocols.securityAlert.effect.tag.type}`, `b${d}.n.boss.combat:applyBuffs:${protocols.combat[`D${d}`].effect.tag.type}`]).sort();
    c("starting effects: Security Alert debuff on 4 alert commanders, Combat buff on 4 combat commanders, nothing else, all allowlisted", fx.slice().sort().join() === want.join(), fx);
    const d5 = by.get("b5.n.boss.combat")!.applyBuffs as { type: string; power: number; rounds: number; target?: string }[];
    c("D5 Combat Protocol is the approved Debuff Prevent 100 / 3r on the player (RUL-2026-10-16-008)",
      String(protocols.combat.D5.status).startsWith("APPROVED — RUL-2026-10-16-008") && d5.length === 1 && d5[0]!.type === "debuffprevent" && d5[0]!.power === 100 && d5[0]!.rounds === 3, d5);
    c("no objective carries reward_items; quest-level choose of two caches", objs.every((o) => !((o.reward_items as unknown[]) ?? []).length) &&
      record().content.rewardMode === "choose" && record().content.rewardPickCount === 1 && record().content.reward.reward_items.length === 2);
    c("entry item is the Beacon ref", record().content.entryItems[0].ids[0] === fixtureId("@item:skyglass_signal_beacon"));
    // 625 successful routes, 16–20 fights, 4 commanders.
    let paths = 0; const lens = new Set<number>(); const err: string[] = [];
    const walk = (id: string, nb: number, boss: number) => {
      const o = by.get(id)!;
      const b = nb + (o.task === "start_battle" ? 1 : 0), bs = boss + (o.task === "start_battle" && id.includes(".boss.") ? 1 : 0);
      if (o.task === "win_quest") { paths++; lens.add(b); if (bs !== 4) err.push(id); return; }
      if (o.task !== "dialog" && o.task !== "start_battle") { err.push(id); return; }
      const nx = Array.isArray(o.nextObjectiveId) ? (o.nextObjectiveId as { nextObjectiveId: string }[]).map((x) => x.nextObjectiveId) : [o.nextObjectiveId as string];
      for (const n of nx) walk(n, b, bs);
    };
    walk("d2.n.f1", 0, 0);
    c("625 successful routes, 16–20 fights each, four commanders, one ending", paths === 625 && [...lens].sort().join() === "16,17,18,19,20" && !err.length, { paths, lens: [...lens] });
  });
  it("encounter ledger: 20 identities, all used", () => {
    const ledger = read(`${A}/compiled/encounter_ledger.json`).slots as { slot: string; battleObjectives: string[] }[];
    c("20 encounter slots (16 regular + 4 commanders), each used by ≥1 battle", ledger.length === 20 && ledger.every((s) => s.battleObjectives.length > 0) &&
      ledger.filter((s) => s.slot.endsWith("BOSS")).length === 4, ledger.map((s) => s.slot));
    c("20 compiled AI profiles, ≤20 rules each, unconditional end_turn last", profiles.length === 20 && profiles.every((p) => p.aiProfile.rules.length <= 20 &&
      (p.aiProfile.rules.at(-1) as { conditions: unknown[]; action: { type: string } }).action.type === "end_turn"));
  });
});

describe("C1b completion caches (RUL-2026-10-16-010)", () => {
  it("cache records: engine schemas, approved weights, Strong Pyramid recipe bundles", () => {
    c("two caches, matching the quest-level reward refs", cacheOut.length === 2 &&
      cacheOut.map((x) => x.ref).sort().join() === compiled.record.content.reward.reward_items.map((r: { ids: string[] }) => r.ids[0]).sort().join());
    for (const ch of cacheOut) {
      const fam = ch.srcId.includes("arsenal") ? "arsenal" : "research";
      const eff = ch.record.effects[0]!;
      const tag = NonCombatConsumeRewardTag.safeParse(eff);
      c(`${fam}: NonCombatConsumeRewardTag accepts the active weightedCache effect`, tag.success, tag.success ? undefined : tag.error.issues.slice(0, 5));
      const wc = eff.weightedCache;
      c(`${fam}: one roll at 10000; tiers Epic 5000 / Legendary 5000`, wc.rolls.length === 1 && wc.rolls[0]!.probability === 10_000 &&
        wc.tiers.map((t) => `${t.name}:${t.probability}`).join() === "Epic:5000,Legendary:5000", wc.tiers.map((t) => [t.name, t.probability]));
      const want = (rarity: string, legendary: boolean) => pools[fam]!.chosen.filter((r) => r.status === "PROPOSED_PILOT" && r.output.rarity === rarity)
        .map((r) => bundleKey(r.ingredients.map((i) => ({ itemId: i.id, quantity: legendary ? (i.quantityFull * 2) / 5 : i.quantityFull }))));
      const got = (n: string) => wc.tiers.find((t) => t.name === n)!.entries.map((e) => bundleKey(e.items));
      c(`${fam}: every Epic entry is one whole recipe (100%), exact ratios`, got("Epic").sort().join("|") === want("EPIC", false).sort().join("|"), ch.entries);
      c(`${fam}: every Legendary entry is exactly 40% of one recipe`, got("Legendary").sort().join("|") === want("LEGENDARY", true).sort().join("|"), ch.entries);
      c(`${fam}: untradeable, consumable, destroyed on use, no battle use, target SELF`, ch.record.canBeTraded === false && ch.record.itemType === "CONSUMABLE" &&
        ch.record.destroyOnUse === true && ch.record.preventBattleUsage === true && ch.record.target === "SELF");
    }
  });
});

describeWithDatabase("C2 real saves", () => {
  beforeEach(() => { vi.spyOn(Pusher.prototype, "trigger").mockResolvedValue(undefined); });
  it("editor save of the compiled 99-objective quest (hidden)", async () => {
    const db = await getTestDatabase();
    await resetTables(aiProfile, quest, item);
    await insertUsers([{ userId: "sb-editor", username: "sb-editor", role: "CONTENT" }]);
    await insertItems([{ id: fixtureId("@item:skyglass_signal_beacon"), name: "Beacon [fixture]", itemType: "CONSUMABLE" },
      { id: fixtureId("@item:bastion_arsenal_cache"), name: "Arsenal [fixture]", itemType: "CONSUMABLE" },
      { id: fixtureId("@item:bastion_research_cache"), name: "Research [fixture]", itemType: "CONSUMABLE" }] as never);
    const rec = record();
    await db.insert(quest).values({ id: "sb-bastion", ...rec, content: rec.content } as never);
    const res = await (await callerFor(questsRouter, "sb-editor")).update({ id: "sb-bastion", data: QuestValidator.parse(rec) });
    c("quests.update saves the compiled candidate", res.success, res.message);
    const saved = await db.query.quest.findFirst({ where: eq(quest.id, "sb-bastion") });
    c("saved: 99 objectives in order, hidden, choose/pick 1", !!saved && saved.hidden && saved.content.objectives.length === 99 &&
      saved.content.objectives.map((o) => o.id).join() === rec.content.objectives.map((o: O) => o.id).join() && saved.content.rewardMode === "choose");
    ev.put("savedContentBytes", JSON.stringify(saved?.content).length);
    expect(res.success).toBe(true);
  }, 120_000);
  it("all 20 AI profiles save through ai.updateAiProfile; 21 rules are refused", async () => {
    const db = await getTestDatabase();
    await resetTables(aiProfile);
    const failures: unknown[] = [];
    for (const p of profiles) {
      const aiId = fixtureId(`@ai:${p.slot}`);
      await insertUsers([{ userId: aiId, username: aiId, isAi: true }]);
      await db.insert(aiProfile).values({ id: `prof-${aiId}`, userId: aiId, rules: [], includeDefaultRules: true });
      const rules = subst(p.aiProfile.rules).map(({ source: _s, ...r }) => AiRule.parse(r));
      const res = await (await callerFor(aiRouter, "sb-editor")).updateAiProfile({ id: `prof-${aiId}`, rules, includeDefaultRules: false });
      const row = await db.query.aiProfile.findFirst({ where: eq(aiProfile.id, `prof-${aiId}`) });
      if (!res.success || row?.rules.length !== rules.length || row.includeDefaultRules) failures.push({ key: p.key, msg: res.message });
    }
    c("20/20 compiled profiles saved with includeDefaultRules:false and every rule kept", failures.length === 0, failures);
    const p0 = profiles.find((p) => p.key === "arakane")!;
    const rules21 = [...subst(p0.aiProfile.rules), p0.aiProfile.rules.at(-1)].map(({ source: _s, ...r }) => AiRule.parse(subst(r)));
    const over = await (await callerFor(aiRouter, "sb-editor")).updateAiProfile({ id: `prof-${fixtureId("@ai:D5.BOSS")}`, rules: rules21, includeDefaultRules: false });
    c("negative control: 21 rules refused by the server cap", !over.success && /Maximum of 20/.test(over.message), over.message);
  }, 300_000);
  it("Countermand stored row passes ItemValidator", async () => {
    const db = await getTestDatabase();
    await resetTables(item);
    const cm = itemRecord("X:COUNTERMAND");
    await insertItems([{ ...cm, id: exclusiveId("X:COUNTERMAND") }] as never);
    const row = await fetchItemWithCraftingRequirements(db, exclusiveId("X:COUNTERMAND"));
    const parsed = ItemValidator.safeParse({ ...row, cost: 1 });
    c("Countermand (OTHER, reusable Clear 100, 40AP r5 CD6, PVE) validates as a stored item", parsed.success, parsed.success ? undefined : parsed.error.issues.slice(0, 5));
  }, 120_000);
  it("both caches validate as stored items and every opening grants exactly one whole compiled bundle", async () => {
    const db = await getTestDatabase();
    await resetTables(userItem, item, userData);
    const hero = "sb-cache-opener";
    await insertUsers([{ userId: hero, username: hero, status: "AWAKE", rank: "JONIN", level: 100, money: 0, sector: 0 }]);
    const ings = [...new Set(cacheOut.flatMap((ch) => ch.record.effects[0]!.weightedCache.tiers.flatMap((t) => t.entries.flatMap((e) => e.items.map((x) => x.itemId)))))];
    await insertItems([
      ...cacheOut.map((ch) => ({ ...ch.record, id: fixtureId(ch.ref) })),
      ...ings.map((id) => ({ id, name: `Ingredient ${id} [fixture]`, itemType: "MATERIAL", canStack: true, stackSize: 1000 })),
    ] as never);
    const OPENS = 12;
    for (const ch of cacheOut) {
      const fam = ch.srcId.includes("arsenal") ? "arsenal" : "research";
      const id = fixtureId(ch.ref);
      const row = await fetchItemWithCraftingRequirements(db, id);
      const parsed = ItemValidator.safeParse({ ...row, cost: 1 });
      c(`${fam}: stored cache row passes ItemValidator`, parsed.success, parsed.success ? undefined : parsed.error.issues.slice(0, 5));
      await insertUserItems([{ id: `stack-${fam}`, userId: hero, itemId: id, quantity: OPENS }]);
      const allowed = new Set(ch.record.effects[0]!.weightedCache.tiers.flatMap((t) => t.entries.map((e) => bundleKey(e.items))));
      const held = async () => Object.fromEntries((await db.query.userItem.findMany({ where: eq(userItem.userId, hero) }))
        .filter((r) => ings.includes(r.itemId)).reduce((m, r) => m.set(r.itemId, (m.get(r.itemId) ?? 0) + r.quantity), new Map<string, number>()));
      const bad: unknown[] = []; const seen: Record<string, number> = {};
      for (let i = 0; i < OPENS; i++) {
        const before = await held();
        const res = await callerForDatabase(itemRouter, hero, db).consume({ userItemId: `stack-${fam}`, requestId: `open-${fam}-${String(i).padStart(4, "0")}` });
        const after = await held();
        const g = Object.keys(after).filter((k) => after[k]! !== (before[k] ?? 0)).map((k) => ({ itemId: k, quantity: after[k]! - (before[k] ?? 0) }));
        const key = bundleKey(g);
        if (!res.success || !allowed.has(key)) bad.push({ i, msg: res.message, g });
        seen[key] = (seen[key] ?? 0) + 1;
      }
      const left = (await db.query.userItem.findMany({ where: eq(userItem.userId, hero) })).filter((r) => r.itemId === id).reduce((s, r) => s + r.quantity, 0);
      c(`${fam}: ${OPENS}/${OPENS} openings succeed, each grants exactly one whole compiled bundle, and every cache is destroyed`, bad.length === 0 && left === 0, { bad, left });
      ev.timing(`${fam}.bundlesSeen`, seen);
    }
  }, 300_000);
  requireClean(ev);
});
