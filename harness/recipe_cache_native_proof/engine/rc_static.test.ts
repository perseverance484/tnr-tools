/**
 * Gate S — pure checks of the synthetic one-of-two choice record and Weighted Cache items against
 * the pinned engine's own validators and pure libraries (no DB).
 */
import { describe, it } from "bun:test";
import { verifyQuestContentForSave, verifyQuestObjectiveFlow } from "@/libs/quest";
import { buildRewardChoiceCards, getRewardPickCount, isRewardChoiceQuest, verifyRewardChoiceForSave } from "@/libs/rewardChoice";
import { resolveWeightedCache } from "@/libs/weightedCache";
import { QuestValidator } from "@/validators/objectives";
import { QuestReward } from "@/validators/rewardPackages";
import { weightedCacheSchema } from "@/validators/weightedCache";
import { Evidence, requireClean } from "./lib/report";
import { compileObjectives, GRAPH_PATH } from "./lib/graph";
import { ARSENAL, BUNDLES, cacheEffect, choiceRecord, RESEARCH } from "./lib/cachefix";

const ev = new Evidence("s_static");
const rec = choiceRecord();

describe("S: choice record", () => {
  it("QuestValidator and save checks accept the 99-objective choose record", () => {
    const parsed = QuestValidator.safeParse(rec);
    ev.check("QuestValidator accepts battlepyramid + rewardMode choose + pick 1", parsed.success, parsed.success ? undefined : parsed.error.issues.slice(0, 5));
    const objectives = compileObjectives();
    ev.check("objective graph unchanged: 99 objectives, flow + save checks pass", objectives.length === 99 && verifyQuestObjectiveFlow(objectives).check && verifyQuestContentForSave(objectives, true).check);
    ev.check("graph source is alt99_f4gate", GRAPH_PATH.endsWith("alt99_f4gate.json"), GRAPH_PATH);
    const win = objectives.find((o) => o.id === "w.complete") as Record<string, unknown>;
    const winItems = ((win.reward_items as unknown[]) ?? []).length;
    ev.check("w.complete carries no reward_items", winItems === 0, winItems);
    const anyObjectiveItems = objectives.filter((o) => (((o as Record<string, unknown>).reward_items as unknown[]) ?? []).length > 0).map((o) => o.id);
    ev.check("no objective carries reward_items", anyObjectiveItems.length === 0, anyObjectiveItems);
    const v = verifyRewardChoiceForSave(rec.content);
    ev.check("verifyRewardChoiceForSave accepts 2 cards for 1 pick", v.check, v.message);
    ev.check("isRewardChoiceQuest + pick count 1", isRewardChoiceQuest(rec.content) && getRewardPickCount(rec.content) === 1);
    const cards = buildRewardChoiceCards(QuestReward.parse(rec.content.reward));
    ev.put("cards", cards);
    ev.check("exactly two item cards, one per cache, quantity 1", cards.length === 2 &&
      cards.map((c) => c.contentId).sort().join() === [ARSENAL, RESEARCH].sort().join() && cards.every((c) => c.field === "reward_items" && c.amount === 1), cards);
    const one = { ...rec.content, reward: QuestReward.parse({ reward_items: [{ ids: [ARSENAL], number: 100, quantity: 1 }] }) };
    ev.check("negative: a single cache card for one pick is rejected at save", !verifyRewardChoiceForSave(one).check, verifyRewardChoiceForSave(one).message);
  });
});

describe("S: cache items and weighted config", () => {
  it("invalid weighted configs fail the schema", () => {
    const base = () => structuredClone(cacheEffect(ARSENAL).weightedCache!);
    const cases: [string, (c: ReturnType<typeof base>) => void][] = [
      ["roll probabilities 9,999", (c) => { c.rolls[0]!.probability = 9_999; }],
      ["tier probabilities 10,001", (c) => { c.tiers[0]!.probability += 1; }],
      ["positive tier with zero entries", (c) => { c.tiers[1]!.entries = []; }],
      ["entry with no items", (c) => { c.tiers[0]!.entries[0]!.items = []; }],
      ["11 items in one bundle", (c) => { c.tiers[0]!.entries[0]!.items = Array.from({ length: 11 }, (_, i) => ({ itemId: `x${i}`, quantity: 1 })); }],
      ["quantity 101", (c) => { c.tiers[0]!.entries[0]!.items[0]!.quantity = 101; }],
      ["worst case > 2,000 items", (c) => { c.rolls = [{ count: 20, probability: 10_000 }]; c.tiers[0]!.entries[0]!.items = Array.from({ length: 10 }, (_, i) => ({ itemId: `y${i}`, quantity: 100 })); }],
      ["empty displayName", (c) => { c.displayName = ""; }],
    ];
    ev.check("valid synthetic config passes", weightedCacheSchema.safeParse(base()).success);
    for (const [name, mutate] of cases) {
      const c = base(); mutate(c);
      ev.check(`rejected: ${name}`, !weightedCacheSchema.safeParse(c).success);
    }
  });
  it("resolveWeightedCache: every roll grants exactly one whole bundle; tier frequencies track weights", () => {
    let seed = 20261016;
    const rnd = () => ((seed = (seed * 1103515245 + 12345) % 2 ** 31) / 2 ** 31);
    for (const id of [ARSENAL, RESEARCH] as const) {
      const cache = cacheEffect(id).weightedCache!;
      const bundles = [...BUNDLES[id].Epic, ...BUNDLES[id].Legendary].map((b) => JSON.stringify([...b].sort((a, z) => a.itemId.localeCompare(z.itemId))));
      const N = 20_000; let epic = 0; let bad = 0; const entries: Record<string, number> = {};
      for (let i = 0; i < N; i++) {
        const r = resolveWeightedCache(cache, rnd);
        const sel = r.selections;
        if (sel.length !== 1) { bad++; continue; }
        const got = JSON.stringify([...r.items].sort((a, z) => a.itemId.localeCompare(z.itemId)));
        if (!bundles.includes(got)) bad++;
        if (sel[0]!.tierName === "Epic") epic++;
        const k = `${sel[0]!.tierName}#${sel[0]!.entryIndex}`; entries[k] = (entries[k] ?? 0) + 1;
      }
      ev.put(`${id}.draws`, { N, epicShare: Math.round((epic / N) * 1000) / 1000, entries: Object.keys(entries).sort() });
      ev.check(`${id}: ${N} seeded draws, each exactly one coherent bundle (no mixing)`, bad === 0, bad);
      ev.check(`${id}: Epic share within ±2% of 75%`, Math.abs(epic / N - 0.75) < 0.02, epic / N);
      ev.check(`${id}: every configured entry selected`, Object.keys(entries).length === BUNDLES[id].Epic.length + BUNDLES[id].Legendary.length);
    }
    const multi = cacheEffect(RESEARCH, { rolls: [{ count: 2, probability: 10_000 }] }).weightedCache!;
    const r = resolveWeightedCache(multi, rnd);
    ev.check("two-roll config: two selections, each a whole bundle, quantities summed", r.selections.length === 2 && r.items.reduce((s, x) => s + x.quantity, 0) === r.selections.reduce((s, x) => s + x.items.reduce((t, y) => t + y.quantity, 0), 0));
  });
});

requireClean(ev);
