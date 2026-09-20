// The negative fixtures the plan names (§8) and every bypass the independent review reproduced,
// each one a mutation of the real Godstorm evidence.
//
// A green golden fixture only proves the tooling agrees with correct evidence; it is these that
// prove it disagrees with the wrong kind - and that it disagrees for the RIGHT reason, which is why
// each case asserts the finding code and the text, not just that something failed.
//
// Cases marked F1..F7 are the reviewer's witnesses against the previous frozen head, kept in the
// reviewer's own shape so a re-review can check them one for one.

import { test } from "node:test";
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";
import { join } from "node:path";
import {
  scenario, fatalsOf, fatalText, warnText, editQuest, dropAiCapture, aiCapture,
  AI, MARROW, STORMCOURT, REPO,
} from "./presentation.scenario.mjs";
import { parseSpec } from "../presentation/spec.mjs";
import { parseEvidence } from "../presentation/evidence.mjs";
import { PresentationError } from "../presentation/errors.mjs";
import { STATUS } from "../presentation/assets.mjs";

const MARROW_BUNDLE = "harvests/inbox/tnr_results_1789829183863.json";
const STORM_BUNDLE = "harvests/inbox/tnr_results_1789842714086.json";
const AI_0914_BUNDLE = "harvests/inbox/tnr_results_1789402842027.json";

const refuses = (fn, re, msg) => {
  let err = null;
  try { fn(); } catch (e) { err = e; }
  assert.ok(err instanceof PresentationError, msg ?? `expected a PresentationError, got ${err}`);
  assert.match(err.message, re);
  return err;
};

// ---------------------------------------------------------------------------------------------
// 1. Old floor cash-out / chest data trying to override current rewards
// ---------------------------------------------------------------------------------------------

test("a spec may not carry a rewards table at all", () => {
  const err = refuses(() => parseSpec({
    schema: "tnr.presentation.spec.v2", evidence: "evidence.json", template: "event-poster", title: "Godstorm",
    rewards: { floor1: { money: 20000, chest: "Marrow Cache" } },
  }), /"rewards" is a dossier fact, not a presentation choice/);
  assert.match(err.message, /dossier\.rewards/);
  assert.match(err.message, /second content database/);

  for (const key of ["cashOuts", "chests", "battles", "keepers", "cadence", "rosterNames", "counts"]) {
    refuses(() => parseSpec({
      schema: "tnr.presentation.spec.v2", evidence: "e.json", template: "event-poster", title: "T", [key]: {},
    }), /is a dossier fact/, `spec.${key} must be refused`);
  }
});

test("the old per-floor cash-outs cannot come back through an unreachable node", () => {
  const r = scenario({
    files: {
      [MARROW_BUNDLE]: editQuest(MARROW, (q) => {
        // A detached remnant of the removed floor structure: the node and its old forward edge are
        // still in the record, and nothing on the route points at it any more.
        q.content.objectives.push({
          id: "old_floor1_cashout", task: "dialog", description: "Floor 1 cleared.",
          reward_money: 20000, reward_tokens: 5, reward_prestige: 2, reward_items: ["chest_marrow_cache"],
          nextObjectiveId: [{ text: "Continue", nextObjectiveId: "old_floor1_tail" }], attackers: [], opponentAIs: [],
        });
        q.content.objectives.push({
          id: "old_floor1_tail", task: "dialog", description: "The old stair.",
          nextObjectiveId: [], attackers: [], opponentAIs: [],
        });
        return q;
      }),
    },
  });
  assert.ok(r.ok, r.ok ? "" : String(r.error));
  const rewards = r.built.dossier.rewards[MARROW];
  assert.deepEqual(rewards.fullClear.reward, { money: 125000, tokens: 25, prestige: 10 });
  assert.deepEqual(rewards.intermediateCashOuts, []);
  assert.deepEqual(rewards.rewardItems, []);
  assert.deepEqual(rewards.unreachableRewardNodes, ["old_floor1_cashout"]);
  assert.match(warnText(r.built), /old_floor1_cashout still carries a reward but nothing reaches it; it is historical/);
  assert.match(warnText(r.built), /detached remnants, not part of this quest/);
  assert.deepEqual(r.built.lint.fatal, [], fatalText(r.built));
});

test("a cash-out that IS on the route to the clear is reported, never folded in", () => {
  const r = scenario({
    files: {
      [MARROW_BUNDLE]: editQuest(MARROW, (q) => {
        const d = q.content.objectives.find((o) => o.id === "d3_1");
        d.reward_money = 20000;
        d.reward_items = ["chest_marrow_cache"];
        return q;
      }),
    },
  });
  assert.ok(r.ok, r.ok ? "" : String(r.error));
  const rewards = r.built.dossier.rewards[MARROW];
  assert.deepEqual(rewards.fullClear.reward, { money: 125000, tokens: 25, prestige: 10 }, "a full-clear reward must not absorb an intermediate one");
  assert.equal(rewards.intermediateCashOuts.length, 1);
  assert.equal(rewards.intermediateCashOuts[0].objectiveId, "d3_1");
  assert.deepEqual(rewards.rewardItems, ["chest_marrow_cache"]);
  assert.match(warnText(r.built), /must not fold it in/);
});

// F5 --------------------------------------------------------------------------------------------

test("F5: an optional exit reward cannot become the full clear", () => {
  // The reviewer's witness. The complete current route is retained; an opening dialogue choice
  // offers an exit paying 20,000 ryo into `fall`, placed BEFORE "Advance". The first version called
  // that the full clear, demoted the real 125,000 victory to a cash-out, and totalled 145,000
  // across two mutually exclusive routes.
  const r = scenario({
    files: {
      [MARROW_BUNDLE]: editQuest(MARROW, (q) => {
        const o = structuredClone(q.content.objectives.find((x) => x.id === "d5_victory"));
        o.id = "optional_exit_reward";
        o.description = "Leave with a partial reward.";
        o.reward_money = 20000; o.reward_tokens = 0; o.reward_prestige = 0;
        o.nextObjectiveId = [{ text: "Leave", nextObjectiveId: "fall" }];
        q.content.objectives.push(o);
        q.content.objectives[0].nextObjectiveId.unshift({ text: "Leave early", nextObjectiveId: o.id });
        return q;
      }),
    },
  });
  assert.ok(r.ok, r.ok ? "" : String(r.error));
  const rewards = r.built.dossier.rewards[MARROW];
  assert.equal(rewards.fullClear.objectiveId, "d5_victory", "the clear reward must still be the one on the route to a win");
  assert.deepEqual(rewards.fullClear.reward, { money: 125000, tokens: 25, prestige: 10 });
  assert.deepEqual(rewards.intermediateCashOuts, [], "an exit that cannot reach a win is not a cash-out on the clear route");
  assert.deepEqual(rewards.optionalRewardNodes.map((n) => n.objectiveId), ["optional_exit_reward"]);
  assert.equal(rewards.total.money, 125000, "two exclusive routes must never be summed");
  assert.equal(rewards.totalBasis, "the single success path from the entry to win_quest");
  assert.match(warnText(r.built), /optional_exit_reward pays a reward but cannot reach a win/);
});

test("F5: a reward for losing is classified as one", () => {
  const r = scenario({
    files: {
      [MARROW_BUNDLE]: editQuest(MARROW, (q) => {
        q.content.objectives.find((o) => o.id === "fall").reward_money = 500;
        return q;
      }),
    },
  });
  assert.ok(r.ok, r.ok ? "" : String(r.error));
  const rewards = r.built.dossier.rewards[MARROW];
  assert.deepEqual(rewards.failurePathRewardNodes.map((n) => n.objectiveId), ["fall"]);
  assert.equal(rewards.total.money, 125000);
  assert.match(warnText(r.built), /fall pays a reward on the failure path/);
});

test("F5: a branching route to completion refuses to state one full clear", () => {
  const r = scenario({
    files: {
      [MARROW_BUNDLE]: editQuest(MARROW, (q) => {
        // a second victory dialogue paying differently, both reaching `win`
        const alt = structuredClone(q.content.objectives.find((x) => x.id === "d5_victory"));
        alt.id = "d5_victory_alt";
        alt.reward_money = 90000;
        q.content.objectives.push(alt);
        // d5_victory keeps its predecessor; the route now forks at d5_1 and both forks reach `win`
        q.content.objectives.find((x) => x.id === "d5_1").nextObjectiveId = [
          { text: "Advance", nextObjectiveId: "b5_1" },
          { text: "Shortcut", nextObjectiveId: "d5_victory_alt" },
        ];
        return q;
      }),
    },
  });
  assert.ok(r.ok, r.ok ? "" : String(r.error));
  assert.equal(r.built.dossier.rewards[MARROW].fullClear, null);
  assert.equal(r.built.dossier.rewards[MARROW].fullClearAmbiguous, true);
  assert.equal(fatalsOf(r.built, "ambiguous-full-clear").length, 1, fatalText(r.built));
  assert.equal(r.built.dossier.rewards[MARROW].totalBasis, "none: the success path branches");
});

// ---------------------------------------------------------------------------------------------
// 2. A missing keeper under coverage:"all"
// ---------------------------------------------------------------------------------------------

test('coverage "all" catches a keeper no admissible capture can name', () => {
  const r = scenario({ files: { [AI_0914_BUNDLE]: dropAiCapture(AI.wardenHalfEclipse) } });
  assert.ok(r.ok, r.ok ? "" : String(r.error));
  assert.equal(r.built.dossier.roster.length, 18);
  const missing = r.built.dossier.roster.find((e) => e.aiId === AI.wardenHalfEclipse);
  assert.equal(missing.resolved, false);
  assert.equal(missing.name, null);
  assert.equal(fatalsOf(r.built, "roster-incomplete").length, 1, fatalText(r.built));
  assert.match(fatalsOf(r.built, "roster-incomplete")[0].message, /ai 3XMsIV6Yv4jy-uaJAe52f cannot be named/);
  assert.equal(fatalsOf(r.built, "asset-missing").length, 1);
});

test('coverage "all" catches a spec entry list that omits one keeper', () => {
  const r = scenario({
    spec: (s) => {
      s.roster = { coverage: "all", entries: Object.keys(s.roles).filter((id) => id !== AI.keeperHushedHours) };
      return s;
    },
  });
  assert.ok(r.ok, r.ok ? "" : String(r.error));
  assert.equal(fatalsOf(r.built, "roster-omission").length, 1, fatalText(r.built));
  assert.match(fatalsOf(r.built, "roster-omission")[0].message, /omits ai s6LjnqhSW85pIxYRM76Fw \(Keeper of Hushed Hours\)/);
});

test("a roster that lists a stranger is refused too", () => {
  const r = scenario({ spec: (s) => { s.roster = { coverage: "all", entries: [...Object.keys(s.roles), "someOtherAiId"] }; return s; } });
  assert.ok(r.ok, r.ok ? "" : String(r.error));
  assert.equal(fatalsOf(r.built, "roster-stranger").length, 1, fatalText(r.built));
});

test("an AI that fights but carries no role annotation is refused", () => {
  const r = scenario({ spec: (s) => { delete s.roles[AI.mothTyrant]; return s; } });
  assert.ok(r.ok, r.ok ? "" : String(r.error));
  assert.match(fatalsOf(r.built, "unannotated-role")[0].message, /The Moth Tyrant\) fights in 1 battle\(s\) but the spec gives it no role/);
});

test("a role annotation cannot invent an enemy that fights nowhere", () => {
  const r = scenario({ spec: (s) => { s.roles.notARealAiId = "keeper"; return s; } });
  assert.ok(r.ok, r.ok ? "" : String(r.error));
  assert.ok(fatalsOf(r.built, "extraction").some((f) => /names ai notARealAiId, which fights in no reachable battle/.test(f.message)), fatalText(r.built));
});

// F2 --------------------------------------------------------------------------------------------

test("F2: a failed, misidentified capture cannot resolve a keeper", () => {
  // The reviewer's witness: ok:false, persist:"none", persistOk:false, and an input naming another
  // entity. The first version deep-searched the document and resolved the keeper anyway.
  const r = scenario({
    files: {
      [AI_0914_BUNDLE]: (b) => {
        const c = aiCapture(b, AI.wardenHalfEclipse);
        c.ok = false; c.persist = "none"; c.persistOk = false; c.input.userId = "different-entity";
        return b;
      },
    },
  });
  assert.ok(r.ok, r.ok ? "" : String(r.error));
  assert.equal(r.built.dossier.roster.find((e) => e.aiId === AI.wardenHalfEclipse).resolved, false);
  assert.equal(fatalsOf(r.built, "roster-incomplete").length, 1, fatalText(r.built));
});

test("F2: each inadmissible clause is refused on its own", () => {
  for (const [what, damage, expect] of [
    ["ok:false", (c) => { c.ok = false; }, /roster-incomplete/],
    ["persist none", (c) => { c.persist = "none"; }, /roster-incomplete/],
    ["persistOk false", (c) => { c.persistOk = false; }, /roster-incomplete/],
    ["an error", (c) => { c.error = "boom"; }, /roster-incomplete/],
    ["a mismatched identity", (c) => { c.data.userId = "somebody-else"; }, /roster-incomplete/],
    ["no timestamp", (c) => { delete c.at; }, /roster-incomplete/],
  ]) {
    const r = scenario({ files: { [AI_0914_BUNDLE]: (b) => { damage(aiCapture(b, AI.wardenHalfEclipse)); return b; } } });
    assert.ok(r.ok, r.ok ? "" : String(r.error));
    assert.match(fatalText(r.built), expect, `${what} must make the keeper unresolvable`);
  }
});

test("F2: a record outside captures[] is not evidence", () => {
  // The reviewer's witness: drop the real capture and leave the old body in a top-level
  // `debugSnapshot`. A deep search found it; an admission boundary does not.
  const r = scenario({
    files: {
      [AI_0914_BUNDLE]: (b) => {
        const record = structuredClone(aiCapture(b, AI.wardenHalfEclipse).data);
        b = dropAiCapture(AI.wardenHalfEclipse)(b);
        b.debugSnapshot = record;
        return b;
      },
    },
  });
  assert.ok(r.ok, r.ok ? "" : String(r.error));
  assert.equal(r.built.dossier.roster.find((e) => e.aiId === AI.wardenHalfEclipse).resolved, false);
  assert.equal(fatalsOf(r.built, "roster-incomplete").length, 1, fatalText(r.built));
});

test("F2: an unpersisted quest capture is not current structure", () => {
  const r = scenario({
    files: {
      [STORM_BUNDLE]: (b) => {
        for (const c of b.captures) if (c.proc === "quests.get" && c.input.id === STORMCOURT) { c.persist = "none"; c.persistOk = false; }
        return b;
      },
    },
  });
  assert.equal(r.ok, false);
  assert.match(r.error.message, /no admissible quests\.get capture for OSADdXqostbyVliCxWk6k/);
  assert.match(r.error.message, /persisted as "none"/);
});

test("F2: a quest capture with no boolean hidden is incomplete evidence, not hidden:false", () => {
  const r = scenario({
    files: { [MARROW_BUNDLE]: editQuest(MARROW, (q) => { delete q.hidden; return q; }) },
  });
  assert.equal(r.ok, false);
  assert.match(r.error.message, /carries no boolean "hidden"; publication state would have to be guessed/);
});

// F3 --------------------------------------------------------------------------------------------

test("F3: a prepended stale before-capture cannot win by array order", () => {
  // The reviewer's witness: an earlier successful `before` read of Marrow with a 1-ryo victory,
  // prepended while the valid `after` read stays. The first version took the first match.
  const r = scenario({
    files: {
      [MARROW_BUNDLE]: (b) => {
        const c = structuredClone(b.captures.find((x) => x.proc === "quests.get" && x.input.id === MARROW));
        c.phase = "before";
        c.at = "2026-09-19T14:40:00.000Z";
        c.snapshotKey = "52-mu8i2pd8::before::2";
        c.data.content.objectives.find((o) => o.id === "d5_victory").reward_money = 1;
        b.captures.unshift(c);
        return b;
      },
    },
  });
  assert.ok(r.ok, r.ok ? "" : String(r.error));
  assert.deepEqual(r.built.dossier.rewards[MARROW].fullClear.reward, { money: 125000, tokens: 25, prestige: 10 },
    "the pinned capture must win, not the one that happens to be first");
});

test("F3: a quest record that does not pin its capture is refused", () => {
  const r = scenario({
    evidence: (e) => { delete e.records.find((x) => x.id === "marrow-quest").capture.at; delete e.records.find((x) => x.id === "marrow-quest").capture.snapshotKey; return e; },
  });
  assert.equal(r.ok, false);
  assert.match(r.error.message, /must pin the capture it selects by "at" or "snapshotKey"/);
});

test("F3: two admissible captures matching one selector are an ambiguity, not a choice", () => {
  const r = scenario({
    files: {
      [MARROW_BUNDLE]: (b) => {
        const c = structuredClone(b.captures.find((x) => x.proc === "quests.get" && x.input.id === MARROW));
        b.captures.unshift(c); // same at, same snapshotKey
        return b;
      },
    },
  });
  assert.equal(r.ok, false);
  assert.match(r.error.message, /matches 2 admissible captures/);
});

test("F3: an older before-read of an AI in the same bundle does not beat the newer one", () => {
  const r = scenario({
    files: {
      [AI_0914_BUNDLE]: (b) => {
        const c = structuredClone(aiCapture(b, AI.wardenHalfEclipse));
        c.phase = "after";
        c.at = "2026-09-14T15:00:00.000Z";
        c.data.username = "Stale Keeper";
        c.data.avatar = "https://example.invalid/stale.webp";
        b.captures.unshift(c);
        return b;
      },
    },
  });
  assert.ok(r.ok, r.ok ? "" : String(r.error));
  const e = r.built.dossier.roster.find((x) => x.aiId === AI.wardenHalfEclipse);
  assert.equal(e.name, "Warden of the Half Eclipse", "capture time decides, not array order");
  assert.equal(e.capturedAt, "2026-09-14T16:20:36.505Z", "the reported time must be the capture's own, not the bundle export time");
});

test("F3: two observations at the same instant that disagree are refused", () => {
  const r = scenario({
    files: {
      [AI_0914_BUNDLE]: (b) => {
        const real = aiCapture(b, AI.wardenHalfEclipse);
        const c = structuredClone(real);
        c.data.avatar = "https://example.invalid/other.webp";
        b.captures.unshift(c);
        return b;
      },
    },
  });
  assert.equal(r.ok, false);
  assert.match(r.error.message, /at the same instant .* disagree about its avatar/);
});

test("F3: editing only the working copy is caught by the source lock", () => {
  // The reviewer's witness: change Marrow's reward to 7 in the working tree. The first version
  // hashed whatever it read and produced a passing dossier with a fresh hash.
  const r = scenario({
    uncommitted: {
      [MARROW_BUNDLE]: editQuest(MARROW, (q) => {
        q.content.objectives.find((o) => o.id === "d5_victory").reward_money = 7;
        return q;
      }),
    },
  });
  assert.equal(r.ok, false);
  assert.match(r.error.message, /hashes [0-9a-f]{64} but the package declares/);
});

test("F3: a declared digest that matches an uncommitted file is still refused", () => {
  // Digest and file agree; the commit does not. Only the blob comparison catches this.
  const r = scenario({
    files: {
      [MARROW_BUNDLE]: editQuest(MARROW, (q) => {
        q.content.objectives.find((o) => o.id === "d5_victory").reward_money = 7;
        return q;
      }),
    },
    blobAtRef: (ref, path, fallback) => (path === MARROW_BUNDLE ? readFileSync(join(REPO, MARROW_BUNDLE)) : fallback(ref, path)),
  });
  assert.equal(r.ok, false);
  assert.match(r.error.message, /the dossier would be built from uncommitted bytes/);
});

test("F3: an evidence package with no source lock is refused at parse time", () => {
  refuses(() => parseEvidence({
    schema: "tnr.presentation.evidence.v2",
    subject: { title: "T" },
    records: [{ id: "a", kind: "uploads", path: "x.json", sha256: "0".repeat(64) }],
  }), /must name repoCommit as a 40-hex commit sha/);
});

test("F3: a draft package builds, and says so fatally", () => {
  const r = scenario({
    evidence: (e) => {
      delete e.repoCommit;
      e.draft = true;
      for (const rec of e.records) delete rec.sha256;
      return e;
    },
  });
  assert.ok(r.ok, r.ok ? "" : String(r.error));
  assert.equal(r.built.dossier.sources.draft, true);
  assert.equal(r.built.dossier.sources.repoCommit, null);
  assert.equal(fatalsOf(r.built, "draft-evidence").length, 1, fatalText(r.built));
  assert.match(warnText(r.built), /DRAFT - .* with no commit behind it/);
});

test("F3: a source file whose commit cannot be read is unverified, not verified", () => {
  const r = scenario({
    blobAtRef: (ref, path, fallback) => (path === MARROW_BUNDLE ? null : fallback(ref, path)),
  });
  assert.equal(r.ok, false);
  assert.match(r.error.message, /could not be read at eefefd1afd67, so its source lock cannot be verified/);
});

// F4 --------------------------------------------------------------------------------------------

test("F4: reordering storage without changing an edge changes nothing derived", () => {
  // The reviewer's witness: swap b1_1 and b1_boss in the array. The first version reported the
  // keeper as the first encounter and the cadence as "1 keeper then 8 recurring".
  const plain = scenario({});
  assert.ok(plain.ok, plain.ok ? "" : String(plain.error));
  const before = plain.built.dossier.encounters.find((e) => e.questId === MARROW);

  const r = scenario({
    files: {
      [MARROW_BUNDLE]: editQuest(MARROW, (q) => {
        const a = q.content.objectives;
        const x = a.findIndex((o) => o.id === "b1_1");
        const y = a.findIndex((o) => o.id === "b1_boss");
        [a[x], a[y]] = [a[y], a[x]];
        return q;
      }),
    },
  });
  assert.ok(r.ok, r.ok ? "" : String(r.error));
  const after = r.built.dossier.encounters.find((e) => e.questId === MARROW);
  assert.equal(after.cadenceText, "4 recurring fights then 1 keeper fight, repeated 5 times");
  assert.deepEqual(after.sequence.map((s) => s.objectiveId), before.sequence.map((s) => s.objectiveId));
  assert.deepEqual(r.built.lint.fatal, [], fatalText(r.built));
});

test("F4: moving the opening dialogue to the end of the array keeps it reachable", () => {
  const r = scenario({
    files: {
      [MARROW_BUNDLE]: editQuest(MARROW, (q) => {
        const a = q.content.objectives;
        a.push(a.splice(a.findIndex((o) => o.id === "d1_1"), 1)[0]);
        return q;
      }),
    },
  });
  assert.ok(r.ok, r.ok ? "" : String(r.error));
  assert.equal(r.built.dossier.structure[MARROW].entryObjectiveId, "d1_1");
  assert.ok(r.built.dossier.structure[MARROW].reachableIds.includes("d1_1"));
  assert.deepEqual(r.built.lint.fatal, [], fatalText(r.built));
});

test("F4: a detached remnant is reported, and real ambiguity is refused", () => {
  // Tolerated: a remnant that reaches nothing. The entry is still the one node that reaches a win.
  const remnant = scenario({
    files: {
      [MARROW_BUNDLE]: editQuest(MARROW, (q) => {
        q.content.objectives.push({ id: "orphan", task: "dialog", description: "x", nextObjectiveId: [] });
        return q;
      }),
    },
  });
  assert.ok(remnant.ok, remnant.ok ? "" : String(remnant.error));
  assert.equal(remnant.built.dossier.structure[MARROW].entryObjectiveId, "d1_1");
  assert.deepEqual(remnant.built.dossier.structure[MARROW].orphanStarts, ["orphan"]);
  assert.match(warnText(remnant.built), /detached remnants, not part of this quest/);

  // Refused: two unreferenced nodes that BOTH reach a win. Nothing in the record says which the
  // player starts from, and a presentation must not pick.
  const ambiguous = scenario({
    files: {
      [MARROW_BUNDLE]: editQuest(MARROW, (q) => {
        q.content.objectives.push({ id: "second_start", task: "dialog", description: "x", nextObjectiveId: [{ text: "Go", nextObjectiveId: "d5_victory" }] });
        return q;
      }),
    },
  });
  assert.equal(ambiguous.ok, false);
  assert.match(ambiguous.error.message, /expected exactly one entry objective that reaches a win \(one that nothing points at\), found 2/);

  // Refused: a cycle, so nothing is unreferenced at all.
  const cycle = scenario({
    files: {
      [MARROW_BUNDLE]: editQuest(MARROW, (q) => {
        q.content.objectives.find((o) => o.id === "d5_victory").nextObjectiveId = [{ text: "Loop", nextObjectiveId: "d1_1" }];
        return q;
      }),
    },
  });
  assert.equal(cycle.ok, false);
  assert.match(cycle.error.message, /expected exactly one entry objective that reaches a win \(one that nothing points at\), found 0/);
});

// ---------------------------------------------------------------------------------------------
// 3, 4 and F1. Swapped art, wrong art of the right size, and art nothing verified
// ---------------------------------------------------------------------------------------------

test("a swapped AI image is refused: the bound bytes are not what this character serves", () => {
  const r = scenario({
    spec: (s) => { s.assets[`ai:${AI.umbralReaver}`] = "art/godstorm/ai_godstorm_marrow_starless_monk.webp"; return s; },
  });
  assert.ok(r.ok, r.ok ? "" : String(r.error));
  const fatal = fatalsOf(r.built, "asset-mismatch");
  assert.equal(fatal.length, 1, fatalText(r.built));
  assert.match(fatal[0].message, /Umbral Reaver currently serves/);
  assert.match(fatal[0].message, /this is not this entity's art/);
});

test("wrong art of EXACTLY the right size is refused, and not because of its size", () => {
  const real = readFileSync(join(REPO, "art/godstorm/ai_godstorm_marrow_umbral_reaver.webp"));
  const other = readFileSync(join(REPO, "art/godstorm/ai_godstorm_marrow_starless_monk.webp"));
  const sameSize = Buffer.concat([other.subarray(0, real.length)], real.length);
  assert.equal(sameSize.length, real.length, "the fixture must be byte-for-byte the same LENGTH");
  const swappedSha = createHash("sha256").update(sameSize).digest("hex");
  assert.notEqual(swappedSha, createHash("sha256").update(real).digest("hex"));

  const r = scenario({
    extraFiles: { "art/godstorm/ai_godstorm_marrow_umbral_reaver.webp": sameSize },
    files: {
      "archive/spent-manifests/push-2026-09-19/53_godstorm_failed_items_repair.json": (m) => {
        m.imagePack.files["ai_godstorm_marrow_umbral_reaver.webp"].sha256 = swappedSha;
        return m;
      },
    },
  });
  assert.ok(r.ok, r.ok ? "" : String(r.error));
  const entry = r.built.dossier.assets.entries.find((e) => e.name === "Umbral Reaver");
  assert.equal(entry.bytes.length, real.length, "the fixture's point is that the size still matches");
  assert.equal(entry.bytes.declaredLength, real.length);
  assert.equal(entry.bytes.verified, false);
  assert.equal(entry.status, STATUS.MISMATCH);
  assert.equal(entry.renderable, false);
  const fatal = fatalsOf(r.built, "asset-mismatch");
  assert.equal(fatal.length, 1, fatalText(r.built));
  assert.match(fatal[0].message, /blob at the commit the pack names/);
});

test("F1: the same wrong image passes nothing when the pack's commit is unavailable", () => {
  // The reviewer's stronger witness: the same same-size replacement, but the pack names a commit
  // nobody can read, so the git reader returns null on its own. The first version recorded a note
  // and still called it exact-current-bytes.
  const real = readFileSync(join(REPO, "art/godstorm/ai_godstorm_marrow_umbral_reaver.webp"));
  const other = readFileSync(join(REPO, "art/godstorm/ai_godstorm_marrow_starless_monk.webp"));
  const sameSize = Buffer.concat([other.subarray(0, real.length)], real.length);
  const swappedSha = createHash("sha256").update(sameSize).digest("hex");

  const r = scenario({
    extraFiles: { "art/godstorm/ai_godstorm_marrow_umbral_reaver.webp": sameSize },
    files: {
      "archive/spent-manifests/push-2026-09-19/53_godstorm_failed_items_repair.json": (m) => {
        m.imagePack.ref = "0".repeat(40);
        m.imagePack.files["ai_godstorm_marrow_umbral_reaver.webp"].sha256 = swappedSha;
        return m;
      },
    },
  });
  assert.ok(r.ok, r.ok ? "" : String(r.error));
  const entry = r.built.dossier.assets.entries.find((e) => e.name === "Umbral Reaver");
  assert.equal(entry.bytes.verified, false);
  assert.equal(entry.renderable, false);
  // the pack's ref is what moved, so every binding it covers becomes unverified - and none of them
  // may pass, least of all the one holding the wrong pixels
  const fatal = fatalsOf(r.built, "asset-unverified");
  assert.equal(fatal.length, 5, fatalText(r.built));
  const mine = fatal.find((f) => /Umbral Reaver/.test(f.message));
  assert.ok(mine, fatalText(r.built));
  assert.match(mine.message, /Unverified bytes are not exact art/);
  assert.match(mine.message, /an unreadable commit is not a verified one/);
  assert.equal(r.built.dossier.assets.coverage.renderable, 0);
});

test("F1: an unreadable blob makes no binding renderable, even with the right bytes", () => {
  // scenario({blobAtRef: () => null}) would break the source lock first, so only the pack's own
  // commit is made unreadable here - the case a shallow clone actually produces.
  const r = scenario({
    blobAtRef: (ref, path, fallback) => (ref === "10fb25704dff1bab8105cd83631e0d524193ef0d" ? null : fallback(ref, path)),
  });
  assert.ok(r.ok, r.ok ? "" : String(r.error));
  const bound = r.built.dossier.assets.entries.filter((e) => e.bytes.bound);
  assert.equal(bound.length, 5);
  for (const e of bound) {
    assert.equal(e.bytes.verified, false, `${e.name}: an absent verifier must not imply verification`);
    assert.equal(e.renderable, false);
  }
  assert.equal(r.built.dossier.assets.coverage.renderable, 0);
  assert.equal(r.built.dossier.assets.coverage.unverifiedBindings, 5);
  assert.equal(fatalsOf(r.built, "asset-unverified").length, 5, fatalText(r.built));
});

test("art bound to a file no selected pack names is refused", () => {
  const r = scenario({ spec: (s) => { s.assets[`ai:${AI.umbralReaver}`] = "art/style_refs/whatever.webp"; return s; } });
  assert.ok(r.ok, r.ok ? "" : String(r.error));
  assert.match(fatalsOf(r.built, "asset-mismatch")[0].message, /not bound by any selected image pack/);
});

test("a bound path that tries to escape the repository is refused", () => {
  const r = scenario({ spec: (s) => { s.assets[`ai:${AI.umbralReaver}`] = "../../etc/passwd"; return s; } });
  assert.ok(r.ok, r.ok ? "" : String(r.error));
  assert.equal(fatalsOf(r.built, "asset-mismatch").length, 1, fatalText(r.built));
});

// F7 --------------------------------------------------------------------------------------------

test("F7: a quest or scene binding is checked, not silently ignored", () => {
  // The reviewer's witness: bind a quest listing image and a scene background to a file that does
  // not exist. Parsing and lint used to pass and the registry stayed at 18 entries.
  const r = scenario({
    spec: (s) => {
      s.assets[`quest:${MARROW}`] = "art/does-not-exist.webp";
      s.assets["asset:7EmVo6GH5GL4YtQTDrbDR"] = "art/does-not-exist.webp";
      return s;
    },
  });
  assert.ok(r.ok, r.ok ? "" : String(r.error));
  const quest = r.built.dossier.assets.entries.find((e) => e.entity === `quest:${MARROW}`);
  const scene = r.built.dossier.assets.entries.find((e) => e.entity === "asset:7EmVo6GH5GL4YtQTDrbDR");
  assert.ok(quest && scene, "both bindings must appear in the registry");
  assert.equal(quest.bytes.bound, true);
  assert.equal(scene.bytes.bound, true);
  assert.equal(fatalsOf(r.built, "asset-mismatch").length, 2, fatalText(r.built));
  for (const f of fatalsOf(r.built, "asset-mismatch")) assert.match(f.message, /not bound by any selected image pack/);
});

test("F7: a binding to an entity this subject does not have is reported", () => {
  const r = scenario({ spec: (s) => { s.assets["ai:not-in-this-event"] = "art/godstorm/ai_godstorm_marrow_umbral_reaver.webp"; return s; } });
  assert.ok(r.ok, r.ok ? "" : String(r.error));
  const stray = r.built.dossier.assets.entries.find((e) => e.entity === "ai:not-in-this-event");
  assert.ok(stray, "the binding must reach the registry");
  assert.equal(fatalsOf(r.built, "asset-missing").length, 1, fatalText(r.built));
  assert.match(fatalsOf(r.built, "asset-missing")[0].message, /not an entity of this subject/);
});

test("F7: sceneDetail requires exact art for every scene the subject shows", () => {
  // Stormcourt's three backgrounds have no gameAsset capture in the selected evidence, so they
  // cannot be captioned with exact art - and saying so is the point.
  const r = scenario({ spec: (s) => { s.sceneDetail = true; return s; } });
  assert.ok(r.ok, r.ok ? "" : String(r.error));
  const fatal = fatalsOf(r.built, "scene-art-unresolved");
  assert.ok(fatal.length >= 3, fatalText(r.built));
  assert.match(fatal[0].message, /has no selected record describing its current image/);
});

// ---------------------------------------------------------------------------------------------
// 5. A scene background declared a top-level location
// ---------------------------------------------------------------------------------------------

test("a scene background cannot be named as a top-level location", () => {
  for (const [assetId, label] of [
    ["7xVJ55rsqarfRmPqLdv98", "Upper Court"],
    ["L_ziMXaLeT9FSdyQ9hkDi", "Binding Dais Active"],
    ["_vK9jDEE0zyop_t23Ijgy", "Binding Dais Released"],
  ]) {
    const r = scenario({ spec: (s) => { s.locations = ["Marrow Vaults", "Stormcourt", `asset:${assetId}`]; return s; } });
    assert.ok(r.ok, r.ok ? "" : String(r.error));
    const fatal = fatalsOf(r.built, "scene-as-location");
    assert.equal(fatal.length, 1, `${label}: ` + fatalText(r.built));
    assert.match(fatal[0].message, /which is a scene-background used by \d+ objective\(s\)/);
    assert.match(fatal[0].message, /A background is artwork, not a place/);
  }
});

test("a location that is neither a component nor a scene asset is refused", () => {
  const r = scenario({ spec: (s) => { s.locations = ["Marrow Vaults", "Stormcourt", "The Dawnless Tower"]; return s; } });
  assert.ok(r.ok, r.ok ? "" : String(r.error));
  assert.equal(fatalsOf(r.built, "unknown-location").length, 1, fatalText(r.built));
});

// ---------------------------------------------------------------------------------------------
// 6 and F6. Stale dialogue anchors, stale wording, and changed text under an unchanged id
// ---------------------------------------------------------------------------------------------

test("a narrative anchored to an objective id that does not exist is refused", () => {
  const r = scenario({ spec: (s) => { s.story.marrow.sourceObjectives = ["d1_1", "d4_99", "d5_victory"]; return s; } });
  assert.ok(r.ok, r.ok ? "" : String(r.error));
  assert.ok(fatalsOf(r.built, "extraction").some((f) => /objective id "d4_99" does not exist, or is not reachable/.test(f.message)), fatalText(r.built));
});

test("old Tower/Dawnless wording cannot be supplied as a current narrative source", () => {
  const r = scenario({
    spec: (s) => {
      s.story.marrow.text = "The player descends the Dawnless Tower beneath Stormcourt, where the Unbroken Thread kept the elder sister, and climbs toward the Ashen Gate.";
      return s;
    },
  });
  assert.ok(r.ok, r.ok ? "" : String(r.error));
  const text = fatalsOf(r.built, "extraction").map((f) => f.message).join("\n");
  for (const stale of ["Dawnless", "Tower", "Ashen", "Gate"]) {
    assert.match(text, new RegExp(`names "${stale}"`), `"${stale}" must be reported:\n${text}`);
  }
});

test("F6: stale names at the START of a sentence are caught too", () => {
  // The reviewer's witness. The first version exempted every sentence-initial capitalised word.
  const r = scenario({
    spec: (s) => { s.story.marrow.text = "Dawnless awaits below. Tower rises above."; return s; },
  });
  assert.ok(r.ok, r.ok ? "" : String(r.error));
  const text = fatalsOf(r.built, "extraction").map((f) => f.message).join("\n");
  assert.match(text, /names "Dawnless"/);
  assert.match(text, /names "Tower"/);
});

test("F6: changed dialogue under an unchanged id invalidates the summary", () => {
  // The reviewer's witness: rewrite d5_victory so the stair stays CLOSED. The ids still resolve and
  // the Warden's name is still allowed, so only the source fingerprint can catch it.
  const r = scenario({
    files: {
      [MARROW_BUNDLE]: editQuest(MARROW, (q) => {
        q.content.objectives.find((o) => o.id === "d5_victory").description = "The stair remains closed. You leave by the entrance.";
        return q;
      }),
    },
  });
  assert.ok(r.ok, r.ok ? "" : String(r.error));
  const fatal = fatalsOf(r.built, "extraction").filter((f) => /story\.marrow/.test(f.message));
  assert.ok(fatal.length, fatalText(r.built));
  assert.match(fatal[0].message, /the dialogue behind its anchors has changed since this summary was reviewed/);
  assert.match(fatal[0].message, /Re-read the current text and update the summary and its sourceDigest together/);
});

test("F6: a summary with no sourceDigest is refused, and told what the current one is", () => {
  const r = scenario({ spec: (s) => { delete s.story.marrow.sourceDigest; return s; } });
  assert.ok(r.ok, r.ok ? "" : String(r.error));
  const fatal = fatalsOf(r.built, "extraction").filter((f) => /story\.marrow: no sourceDigest/.test(f.message));
  assert.equal(fatal.length, 1, fatalText(r.built));
  assert.match(fatal[0].message, /Current digest: [0-9a-f]{64}/);
});

test("F6: reordering the anchors changes the fingerprint", () => {
  const r = scenario({ spec: (s) => { s.story.marrow.sourceObjectives = ["d5_victory", "d4_1", "d1_1"]; return s; } });
  assert.ok(r.ok, r.ok ? "" : String(r.error));
  assert.ok(fatalsOf(r.built, "extraction").some((f) => /story\.marrow: the dialogue behind its anchors has changed/.test(f.message)), fatalText(r.built));
});

test("the wording check does not fire on prose the current evidence does carry", () => {
  const r = scenario({});
  assert.ok(r.ok, r.ok ? "" : String(r.error));
  assert.deepEqual(r.built.lint.fatal, [], fatalText(r.built));
});

test("a narrative with no source anchor at all is refused by the parser", () => {
  refuses(() => parseSpec({
    schema: "tnr.presentation.spec.v2", evidence: "e.json", template: "event-poster", title: "T",
    story: { marrow: { text: "Something happened." } },
  }), /must cite at least one source objective id/);
});

// ---------------------------------------------------------------------------------------------
// 7. Missing or unverified evidence
// ---------------------------------------------------------------------------------------------

test("an evidence record whose file is not there refuses the build", () => {
  const r = scenario({
    evidence: (e) => { e.records.find((x) => x.id === "marrow-quest").path = "harvests/inbox/tnr_results_0000000000000.json"; return e; },
  });
  assert.equal(r.ok, false);
  assert.match(r.error.message, /could not be read/);
});

test("a capture that did not read back ok is not evidence", () => {
  const r = scenario({
    files: {
      [STORM_BUNDLE]: (b) => {
        for (const c of b.captures) if (c.proc === "quests.get" && c.input.id === STORMCOURT) c.ok = false;
        return b;
      },
    },
  });
  assert.equal(r.ok, false);
  assert.match(r.error.message, /did not read back ok/);
});

test("a capture that holds a different quest than the record claims is refused", () => {
  const r = scenario({
    files: {
      [STORM_BUNDLE]: (b) => {
        for (const c of b.captures) if (c.proc === "quests.get" && c.input.id === STORMCOURT) c.data.id = "someOtherQuestId";
        return b;
      },
    },
  });
  assert.equal(r.ok, false);
  assert.match(r.error.message, /asked for id "OSADdXqostbyVliCxWk6k" but the body is "someOtherQuestId"/);
});

test("an evidence path that tries to leave the repository is refused before anything is read", () => {
  for (const bad of ["../secrets.json", "/etc/passwd", "harvests/../../x.json", "harvests\\inbox\\x.json"]) {
    const r = scenario({ evidence: (e) => { e.records.find((x) => x.id === "marrow-quest").path = bad; return e; } });
    assert.equal(r.ok, false, `${bad} must be refused`);
    assert.match(r.error.message, /path /);
  }
});

test("an evidence package that states a fact is refused", () => {
  const r = scenario({ evidence: (e) => { e.records[0].battles = 25; return e; } });
  assert.equal(r.ok, false);
  assert.match(r.error.message, /unknown key "battles"/);
});

test("an evidence record may not point its selector at another procedure", () => {
  const r = scenario({ evidence: (e) => { e.records.find((x) => x.id === "marrow-quest").capture.proc = "profile.getAi"; return e; } });
  assert.equal(r.ok, false);
  assert.match(r.error.message, /a quest record reads quests\.get/);
});

test("an evidence package with no quest record has nothing to present", () => {
  const r = scenario({ evidence: (e) => { e.records = e.records.filter((x) => x.kind !== "quest"); return e; } });
  assert.equal(r.ok, false);
  assert.match(r.error.message, /selects no quest record/);
});

test("the failed run that supplies Marrow Vaults is reported, not hidden and not used blindly", () => {
  const r = scenario({});
  assert.ok(r.ok, r.ok ? "" : String(r.error));
  assert.match(warnText(r.built), /tnr_results_1789829183863\.json is from a run whose outcome was "failed"/);
  assert.match(warnText(r.built), /each capture it supplies is admitted on its own merits/);
  assert.deepEqual(r.built.lint.fatal, [], "a capture that read back ok and persisted is still evidence");
});

// ---------------------------------------------------------------------------------------------
// 8. Historical-only art where exact-current is required
// ---------------------------------------------------------------------------------------------

test("art this character used to serve is refused as historical, not mistaken for a swap", () => {
  const older = JSON.parse(readFileSync(join(REPO, AI_0914_BUNDLE), "utf8"));
  const oldAvatar = aiCapture(older, AI.umbralReaver).data.avatar;
  assert.ok(oldAvatar, "the 09-14 bundle must carry Umbral Reaver's earlier avatar");

  const r = scenario({
    files: { [STORM_BUNDLE]: (b) => { b.idmap["ai_godstorm_marrow_umbral_reaver.webp"] = oldAvatar; return b; } },
  });
  assert.ok(r.ok, r.ok ? "" : String(r.error));
  const entry = r.built.dossier.assets.entries.find((e) => e.name === "Umbral Reaver");
  assert.equal(entry.status, STATUS.HISTORICAL);
  assert.match(entry.notes.join(" "), /is the art Umbral Reaver served at 2026-09-14/);
  assert.equal(fatalsOf(r.built, "asset-historical").length, 1, fatalText(r.built));
  assert.equal(fatalsOf(r.built, "asset-mismatch").length, 0, "historical art must not be reported as a swap");
});

test("a deterministic render refuses art that is current but not materialised", () => {
  const warnOnly = scenario({});
  assert.ok(warnOnly.ok);
  assert.deepEqual(warnOnly.built.lint.fatal, []);
  assert.equal(warnOnly.built.lint.warnings.filter((f) => f.code === "asset-remote").length, 18);

  const strict = scenario({ requireExactBytes: true });
  assert.ok(strict.ok);
  const fatal = fatalsOf(strict.built, "asset-not-materialised");
  assert.equal(fatal.length, 18, fatalText(strict.built));
  assert.match(fatal[0].message, /materialised into the content-addressed cache and hashed first/);
});

// ---------------------------------------------------------------------------------------------
// Spec hygiene
// ---------------------------------------------------------------------------------------------

test("the spec parser is closed: an unknown key is refused rather than ignored", () => {
  refuses(() => parseSpec({
    schema: "tnr.presentation.spec.v2", evidence: "e.json", template: "event-poster", title: "T", tittle: "typo",
  }), /unknown key "tittle"/);
});

test("a spec or evidence package of the wrong schema version is refused", () => {
  refuses(() => parseSpec({ schema: "tnr.presentation.spec.v1", evidence: "e.json", template: "event-poster", title: "T" }),
    /schema must be "tnr\.presentation\.spec\.v2"/);
  refuses(() => parseEvidence({ schema: "tnr.presentation.evidence.v1", subject: { title: "T" }, records: [] }),
    /schema must be "tnr\.presentation\.evidence\.v2"/);
});

test("a spec may not invent a template, a role or a malformed digest", () => {
  refuses(() => parseSpec({ schema: "tnr.presentation.spec.v2", evidence: "e.json", template: "poster", title: "T" }), /template must be one of/);
  refuses(() => parseSpec({ schema: "tnr.presentation.spec.v2", evidence: "e.json", template: "event-poster", title: "T", roles: { x: "miniboss" } }), /role must be one of/);
  refuses(() => parseSpec({
    schema: "tnr.presentation.spec.v2", evidence: "e.json", template: "event-poster", title: "T",
    story: { a: { text: "t", sourceObjectives: ["x"], sourceDigest: "nope" } },
  }), /sourceDigest must be 64 lowercase hex/);
});

// ---------------------------------------------------------------------------------------------
// R1-R3, the residuals the re-review reproduced against ac792ef
// ---------------------------------------------------------------------------------------------

test("R1: one quest cannot be selected twice, however the duplicate is spelled", () => {
  // No capture bytes, source refs or digests are touched in either case: both records are
  // individually admissible. The first correction counted the quest twice - 3 components, 75
  // battles, 15 keepers - while `structure` kept only the last and rewards read the first.
  const dup = scenario({
    evidence: (e) => {
      const r = structuredClone(e.records.find((x) => x.id === "marrow-quest"));
      r.id = "marrow-duplicate";
      e.records.push(r);
      return e;
    },
  });
  assert.equal(dup.ok, false);
  assert.match(dup.error.message, /selects quest 2yvE9PUQqlD8lbYNfgX-b twice/);
  assert.match(dup.error.message, /"marrow-quest"/);
  assert.match(dup.error.message, /"marrow-duplicate"/);
  assert.match(dup.error.message, /a quest is one component with one current record/i);

  // The sharper case: a genuinely older capture of Stormcourt, placed last, with the story block
  // removed so no narrative digest can mask the selection behaviour.
  const older = scenario({
    evidence: (e) => {
      const r = structuredClone(e.records.find((x) => x.id === "marrow-quest"));
      r.id = "stormcourt-earlier";
      r.questId = STORMCOURT;
      r.capture = { phase: "after", at: "2026-09-19T14:46:23.796Z", snapshotKey: "52-mu8i2pd8::after::3" };
      e.records.push(r);
      return e;
    },
    spec: (s) => { delete s.story.stormcourt; return s; },
  });
  assert.equal(older.ok, false);
  assert.match(older.error.message, /selects quest OSADdXqostbyVliCxWk6k twice/);
  assert.match(older.error.message, /tnr_results_1789829183863\.json/, "the error must point at both captures");
});

test("R1: record order cannot decide which facts win", () => {
  // The same overlap, reversed. A refusal that depended on position would pass one of these.
  for (const last of [true, false]) {
    const r = scenario({
      evidence: (e) => {
        const dupe = structuredClone(e.records.find((x) => x.id === "marrow-quest"));
        dupe.id = "marrow-duplicate";
        e.records = last ? [...e.records, dupe] : [dupe, ...e.records];
        return e;
      },
    });
    assert.equal(r.ok, false, `duplicate placed ${last ? "last" : "first"} must be refused`);
    assert.match(r.error.message, /selects quest 2yvE9PUQqlD8lbYNfgX-b twice/);
  }
});

test("R1: the dossier refuses a duplicated quest even when handed one directly", () => {
  // parseEvidence is the gate, but the invariant belongs where the damage happened too: a caller
  // assembling a package by hand must not be able to inflate the totals.
  const r = scenario({
    evidence: (e) => {
      const dupe = structuredClone(e.records.find((x) => x.id === "marrow-quest"));
      dupe.id = "marrow-duplicate";
      e.records.push(dupe);
      return e;
    },
  });
  assert.equal(r.ok, false);
  // and the golden totals are what a single selection yields
  const good = scenario({});
  assert.deepEqual(good.built.dossier.totals, { components: 2, battles: 50, keepers: 10, distinctAi: 18 });
  assert.equal(good.built.dossier.locations.length, 2);
});

test("R2: a tied name disagreement is a conflict, not a coin toss", () => {
  // Same entity id, same avatar, same instant, different name, different snapshot key. The first
  // correction compared only the URL, so "Alternate Keeper" won by sitting first.
  for (const [where, mutate] of [
    ["within one record", (b) => {
      const c = structuredClone(aiCapture(b, AI.wardenHalfEclipse));
      c.snapshotKey = "different-snapshot";
      c.data.username = "Alternate Keeper";
      b.captures.unshift(c);
      return b;
    }],
    ["last in the record", (b) => {
      const c = structuredClone(aiCapture(b, AI.wardenHalfEclipse));
      c.snapshotKey = "different-snapshot";
      c.data.username = "Alternate Keeper";
      b.captures.push(c);
      return b;
    }],
  ]) {
    const r = scenario({ files: { [AI_0914_BUNDLE]: mutate } });
    assert.equal(r.ok, false, `${where} must be refused`);
    assert.match(r.error.message, /at the same instant \(2026-09-14T16:20:36\.505Z\) disagree about its name/);
  }
});

test("R2: a tied game-asset name disagreement is caught the same way", () => {
  const r = scenario({
    files: {
      [AI_0914_BUNDLE]: (b) => {
        const c = structuredClone(b.captures.find((x) => x.proc === "gameAsset.get" && x.input.id === "7EmVo6GH5GL4YtQTDrbDR"));
        c.snapshotKey = "different-snapshot";
        c.data.name = "renamed vault";
        b.captures.unshift(c);
        return b;
      },
    },
  });
  assert.equal(r.ok, false);
  assert.match(r.error.message, /disagree about its name/);
});

test("R2: observations that agree may still coalesce", () => {
  const r = scenario({
    files: {
      [AI_0914_BUNDLE]: (b) => {
        const c = structuredClone(aiCapture(b, AI.wardenHalfEclipse));
        c.snapshotKey = "a-second-identical-read";
        b.captures.unshift(c);
        return b;
      },
    },
  });
  assert.ok(r.ok, r.ok ? "" : String(r.error));
  assert.equal(r.built.dossier.roster.find((e) => e.aiId === AI.wardenHalfEclipse).name, "Warden of the Half Eclipse");
  assert.deepEqual(r.built.lint.fatal, [], fatalText(r.built));
});

test("R3: a cross-route failure link cannot reorder the route or move the full clear", () => {
  // The reviewer's witness. Every success link is retained; b1_1 fails to d5_victory, and d3_1 pays
  // 20,000. The all-edge BFS pulled d5_victory forward, so the LAST payout in that order was d3_1
  // and the real 125,000 victory was demoted to an intermediate.
  const r = scenario({
    files: {
      [MARROW_BUNDLE]: editQuest(MARROW, (q) => {
        q.content.objectives.find((o) => o.id === "b1_1").failObjectiveId = "d5_victory";
        q.content.objectives.find((o) => o.id === "d3_1").reward_money = 20000;
        return q;
      }),
    },
  });
  assert.ok(r.ok, r.ok ? "" : String(r.error));
  const s = r.built.dossier.structure[MARROW];
  const rewards = r.built.dossier.rewards[MARROW];
  assert.deepEqual(s.successPath.slice(0, 6), ["d1_1", "b1_1", "d1_2", "b1_2", "d1_3", "b1_3"],
    "the route is walked over success edges; a failure link is not a step in it");
  assert.equal(s.successPath[s.successPath.length - 1], "win");
  assert.equal(rewards.fullClear.objectiveId, "d5_victory");
  assert.deepEqual(rewards.fullClear.reward, { money: 125000, tokens: 25, prestige: 10 });
  assert.deepEqual(rewards.intermediateCashOuts.map((n) => n.objectiveId), ["d3_1"]);
  assert.equal(r.built.dossier.encounters.find((e) => e.questId === MARROW).cadenceText,
    "4 recurring fights then 1 keeper fight, repeated 5 times");
});

test("R3: an optional battle is not part of the cadence", () => {
  // The reviewer's witness. An opening choice leads to a battle that only reaches `fall`. The
  // combined sequence reported five recurring fights before the first keeper - a run no player
  // can make.
  const r = scenario({
    files: {
      [MARROW_BUNDLE]: editQuest(MARROW, (q) => {
        const o = structuredClone(q.content.objectives.find((x) => x.id === "b1_1"));
        o.id = "optional_exit_battle";
        o.nextObjectiveId = "fall";
        q.content.objectives.push(o);
        q.content.objectives[0].nextObjectiveId.unshift({ text: "Leave after fighting", nextObjectiveId: o.id });
        return q;
      }),
    },
  });
  assert.ok(r.ok, r.ok ? "" : String(r.error));
  const e = r.built.dossier.encounters.find((x) => x.questId === MARROW);
  assert.equal(e.cadenceText, "4 recurring fights then 1 keeper fight, repeated 5 times");
  assert.equal(e.battles, 25, "the presented sequence is the route");
  assert.equal(e.offRouteBattles, 1, "and the optional battle is counted, not hidden");
  assert.deepEqual(e.sequence.slice(0, 2).map((x) => x.objectiveId), ["b1_1", "b1_2"]);
  const off = e.sequence.find((x) => x.objectiveId === "optional_exit_battle");
  assert.equal(off.onSuccessPath, false);
  assert.equal(off.index, null, "an off-route battle must not take a number in the sequence");
  // it still counts as a reachable battle, and the roster still knows the AI it fields
  assert.equal(r.built.dossier.structure[MARROW].counts.battles, 26);
  assert.equal(r.built.dossier.structure[MARROW].counts.routeBattles, 25);
});

test("R3: a loop through success edges on the route is refused", () => {
  const r = scenario({
    files: {
      [MARROW_BUNDLE]: editQuest(MARROW, (q) => {
        q.content.objectives.find((o) => o.id === "d3_1").nextObjectiveId = [{ text: "Back", nextObjectiveId: "d1_2" }, { text: "Advance", nextObjectiveId: "b3_1" }];
        return q;
      }),
    },
  });
  assert.equal(r.ok, false);
  assert.match(r.error.message, /the route to completion loops through .* along success edges/);
});

test("R3: a rooted cycle that exists only through a failure link is reported, not refused", () => {
  // The reviewer's hardening case. The pinned flow validator rejects a cycle, so the record is
  // malformed - but the route a player walks is still perfectly well defined, so refusing the whole
  // build would be the wrong answer.
  const r = scenario({
    files: {
      [MARROW_BUNDLE]: editQuest(MARROW, (q) => {
        q.content.objectives.find((o) => o.id === "b2_1").failObjectiveId = "b1_1";
        return q;
      }),
    },
  });
  assert.ok(r.ok, r.ok ? "" : String(r.error));
  assert.deepEqual(r.built.dossier.structure[MARROW].cycles, ["b1_1", "b2_1"]);
  assert.match(warnText(r.built), /loops through b1_1, b2_1 once failure links are followed/);
  assert.match(warnText(r.built), /the pinned flow validator rejects a cycle/);
  assert.equal(r.built.dossier.encounters.find((e) => e.questId === MARROW).cadenceText,
    "4 recurring fights then 1 keeper fight, repeated 5 times");
  assert.deepEqual(r.built.lint.fatal, [], fatalText(r.built));
});

test("an ordinary sentence opener is not a stale name", () => {
  // The reviewer's nonblocking case: prefixing the valid summary with "Ultimately, " was fatal.
  const r = scenario({
    spec: (s) => {
      s.story.marrow.text = `Ultimately, ${s.story.marrow.text.charAt(0).toLowerCase()}${s.story.marrow.text.slice(1)}`;
      return s;
    },
  });
  assert.ok(r.ok, r.ok ? "" : String(r.error));
  assert.deepEqual(r.built.lint.fatal, [], fatalText(r.built));
});
