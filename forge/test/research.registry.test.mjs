// The research-read registry and the capture-tier policy it carries
// (state/prompt_forge_next_phase1.md, RUL-2026-09-17-001 and RUL-2026-09-17-002).
//
// The claims this file exists to hold:
//
//   - a procedure is readable because a committed work package demanded it and its contract was
//     audited at a named pin, NEVER because the game would answer it;
//   - a read's input is validated and canonicalized before transport, and the SAME canonical value
//     is what gets sent, what the cache is keyed on and what the journal records;
//   - a mutation cannot enter the registry by any route.
//
// Nothing here contacts the game. Every read is driven through FakeClient, and the paths asserted
// against source are asserted against the transcription in transport/procedures.mjs plus the line
// references recorded there, not against a live request.

import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import {
  RESEARCH_READS, RESEARCH_PATHS, REPO_SAFE_PATHS, REGISTRY_PIN, TIERS, MAX_PAGES,
  DEFAULT_RESEARCH_TIER, ResearchError, researchRow, requireRow, admissibleTiers, tierAtMost,
  canonicalInput, canonicalKey, pointInput, pageInput, pageContract, readMode, registryProblems,
} from "../src/research/registry.mjs";
import { PROCEDURES, MUTATION_PATHS } from "../src/transport/procedures.mjs";
import { FULL_PERSIST_PATHS } from "../src/storage/captures.mjs";
import { parseManifest, ManifestError } from "../src/runner/manifest.mjs";

// ---------------------------------------------------------------- 1: admission is demand-driven
test("every research row names a query that the audited source registry actually has", () => {
  assert.deepEqual(registryProblems(), []);
  for (const path of RESEARCH_PATHS) {
    assert.ok(PROCEDURES[path], `${path} has no source row`);
    assert.equal(PROCEDURES[path].kind, "query", `${path} must be a read`);
    const row = RESEARCH_READS[path];
    assert.ok(TIERS.includes(row.tier), `${path} tier`);
    assert.ok(row.source, `${path} must record where at source it was audited`);
    assert.ok(row.demand, `${path} must name the committed work package that demanded it`);
  }
});

test("no mutation can enter the research registry, by any spelling", () => {
  for (const path of MUTATION_PATHS) {
    assert.equal(researchRow(path), null, `${path} is a mutation and must have no research row`);
    assert.throws(() => requireRow(path), ResearchError, path);
    // and a manifest cannot smuggle one in as a capture either
    assert.throws(
      () => parseManifest({ items: [], capture: { after: [{ proc: path, input: { id: "x" } }] } }),
      /not in the audited research-read registry/,
      path);
  }
});

test("an unapproved non-content path is refused at parse, before any transport", () => {
  // Every one of these exists in some form at source or in the wider API; none has a row, because
  // no committed manifest has demanded one. Discoverability is not admission.
  for (const proc of ["combat.getGraph", "combat.getBattleHistoryEntry", "profile.getPublicUsers",
                      "gameAsset.getAllFolders", "jutsu.getAll", "quests.getAll", "user.getProfile", "nonsense.at.all"]) {
    assert.throws(
      () => parseManifest({ items: [], capture: { after: [{ proc, input: {} }] } }),
      /not in the audited research-read registry/,
      `${proc} must be refused`);
  }
});

test("the committed registry descriptor is reproducible from the registry module", async () => {
  // The descriptor is a projection, not a second authority. If it can be hand-edited into
  // disagreeing with the module, a reviewer reading the table is reading a claim rather than the
  // code, which is exactly the failure mode this repository's generated-artefact rule exists for.
  const { render } = await import("../tools/derive_registry.mjs");
  const committed = readFileSync(new URL("../RESEARCH_REGISTRY.md", import.meta.url), "utf8");
  assert.equal(committed, render(), "RESEARCH_REGISTRY.md is stale; run `node tools/derive_registry.mjs`");
});

test("registry provenance names the source pin, and it is the pin the generated contracts carry", () => {
  assert.match(REGISTRY_PIN, /^[0-9a-f]{40}$/);
  for (const name of ["fields.json", "nested.json"]) {
    const j = JSON.parse(readFileSync(new URL(`../src/runner/${name}`, import.meta.url), "utf8"));
    assert.equal((j._provenance || j._meta || {}).pin, REGISTRY_PIN, `${name} pin must equal the registry pin`);
  }
});

test("the two Phase 1 additions carry the exact source facts audited at the pin", () => {
  // combat.ts:382 and :530 at 345d18ac, both protectedProcedure .query() with no
  // ratelimitMiddleware composed at the call site, both .meta({ mcp: { enabled: true } }).
  for (const path of ["combat.getBattleEntries", "combat.getBattleHistory"]) {
    assert.deepEqual(PROCEDURES[path], { kind: "query", limited: false, mcp: true, auth: "protected" }, path);
    assert.match(RESEARCH_READS[path].source, /combat\.ts:\d+/, `${path} must cite its source line`);
    assert.match(RESEARCH_READS[path].demand, /^push\/\d+_/, `${path} must name a committed manifest`);
  }
  // getBattleEntries is the only paged row, and its shape is the source's own limit/offset
  assert.deepEqual(pageContract("combat.getBattleEntries"),
    { mode: "offset", limitKey: "limit", offsetKey: "offset", defaultLimit: 30, maxLimit: 500 });
  // getBattleHistory has no pagination at source, and Forge does not invent one
  assert.equal(pageContract("combat.getBattleHistory"), null);
});

// ---------------------------------------------------------------- 2: tiers and their ceilings
test("new non-content rows default to local-only and nothing was added to repo-safe", () => {
  assert.equal(DEFAULT_RESEARCH_TIER, "local-only");
  for (const path of ["combat.getBattleEntries", "combat.getBattleHistory"]) {
    assert.equal(RESEARCH_READS[path].tier, "local-only", path);
    assert.deepEqual(admissibleTiers(path), ["local-only"], `${path} may not be asked for anything wider`);
    assert.equal(RESEARCH_READS[path].project, null, `${path} admits no projected fields without a reviewed edit`);
  }
  // the repo-safe class is exactly the Phase 0 content-record point reads, carried over verbatim
  assert.deepEqual([...REPO_SAFE_PATHS].sort(), [
    "ai.getAiProfile", "bloodline.get", "gameAsset.get", "item.get", "jutsu.get", "profile.getAi", "quests.get",
  ]);
  assert.deepEqual([...FULL_PERSIST_PATHS].sort(), [...REPO_SAFE_PATHS].sort(),
    "the persistence allowlist is derived from the registry, not a second list beside it");
});

test("tier order is narrow to wide, and a ceiling admits itself and everything narrower", () => {
  assert.deepEqual([...TIERS], ["local-only", "projected", "repo-safe"]);
  assert.deepEqual(admissibleTiers("quests.get"), ["local-only", "projected", "repo-safe"]);
  assert.deepEqual(admissibleTiers("jutsu.getAllNames"), ["local-only"]);
  assert.equal(tierAtMost("local-only", "repo-safe"), true);
  assert.equal(tierAtMost("repo-safe", "local-only"), false);
  assert.equal(tierAtMost("projected", "local-only"), false);
  assert.equal(tierAtMost("nonsense", "repo-safe"), false, "an unknown name is never admitted");
});

test("widening a capture past its row's ceiling is refused, and the message names the mechanism", () => {
  const ask = (proc, input, persist) => () => parseManifest({ items: [], capture: { after: [{ proc, input, persist, select: ["battleId"] }] } });
  for (const persist of ["repo-safe", "full", "projected"]) {
    assert.throws(ask("combat.getBattleHistory", {}, persist),
      /the registry admits "local-only" for this path, not .*; widening a tier is a reviewed registry edit, not a manifest key/,
      persist);
  }
  // the tier it DOES admit parses
  assert.equal(parseManifest({ items: [], capture: { after: [{ proc: "combat.getBattleHistory", input: {}, persist: "local-only" }] } })
    .capture.after[0].tier, "local-only");
});

// ---------------------------------------------------------------- 3: canonical input
test("an input outside the audited contract never reaches the wire", () => {
  const bad = (proc, input) => assert.throws(() => canonicalInput(proc, input), ResearchError, `${proc} ${JSON.stringify(input)}`);
  bad("combat.getBattleEntries", { battleId: "b", nope: 1 });                       // unknown key
  bad("combat.getBattleEntries", { limit: 10 });                                    // missing required
  bad("combat.getBattleEntries", { battleId: "b", userFilter: "everyone" });        // outside the enum
  bad("combat.getBattleEntries", { battleId: "b", limit: "10" });                   // wrong type
  bad("combat.getBattleEntries", { battleId: "" });                                 // empty id
  bad("combat.getBattleHistory", { combatTypes: ["COMBAT", "NOT_A_TYPE"] });        // outside the enum
  bad("combat.getBattleHistory", { combatTypes: [] });                              // empty filter
  bad("jutsu.getAllNames", { id: "x" });                                            // takes no input
  // The shape push/06 actually uses passes, and an absent optional stays ABSENT rather than being
  // defaulted: a default Forge invented would make the stored provenance differ from what the
  // server was sent, which is the one thing requirement 7.4 forbids.
  const sent = canonicalInput("combat.getBattleEntries", { battleId: "b1", limit: 500, userFilter: "all", showBasicActions: true });
  assert.deepEqual(sent, { battleId: "b1", limit: 500, userFilter: "all", showBasicActions: true });
  assert.deepEqual(Object.keys(sent), ["battleId", "limit", "userFilter", "showBasicActions"], "key order is the registry's");
  assert.ok(!("offset" in sent) && !("refreshKey" in sent) && !("checkBattle" in sent));
  // and the shape push/05 uses
  assert.deepEqual(canonicalInput("combat.getBattleHistory", { combatTypes: ["COMBAT", "SPARRING", "CLAN_BATTLE", "TOURNAMENT", "RANKED_SPARRING", "KAGE_PVP", "RANKED_PVP"] }),
    { combatTypes: ["COMBAT", "SPARRING", "CLAN_BATTLE", "TOURNAMENT", "RANKED_SPARRING", "KAGE_PVP", "RANKED_PVP"] });
});

test("canonical key order is the registry's, so the same request is the same cache identity", () => {
  const a = canonicalInput("combat.getBattleEntries", { battleId: "b1", limit: 5, userFilter: "all" });
  const b = canonicalInput("combat.getBattleEntries", { userFilter: "all", limit: 5, battleId: "b1" });
  assert.deepEqual(a, b);
  assert.equal(canonicalKey(a), canonicalKey(b), "key order in the manifest is not part of the request");
  // ...and anything that IS part of the request changes it
  const differs = [
    { battleId: "b2", limit: 5, userFilter: "all" },
    { battleId: "b1", limit: 6, userFilter: "all" },
    { battleId: "b1", limit: 5, userFilter: "user" },
    { battleId: "b1", limit: 5, userFilter: "all", offset: 5 },
    { battleId: "b1", limit: 5, userFilter: "all", showBasicActions: false },
  ];
  for (const d of differs) {
    assert.notEqual(canonicalKey(canonicalInput("combat.getBattleEntries", d)), canonicalKey(a), JSON.stringify(d));
  }
  // array ORDER is part of the input that gets sent, so it is part of the identity
  const t1 = canonicalKey(canonicalInput("combat.getBattleHistory", { combatTypes: ["COMBAT", "SPARRING"] }));
  const t2 = canonicalKey(canonicalInput("combat.getBattleHistory", { combatTypes: ["SPARRING", "COMBAT"] }));
  assert.notEqual(t1, t2);
  // an input-free procedure has one identity and it is not the string "{}"
  assert.equal(canonicalInput("jutsu.getAllNames", {}), null);
  assert.equal(canonicalKey(null), "");
});

test("the key that names a point read comes off the row, not a table beside it", () => {
  assert.deepEqual(pointInput("jutsu.get", "j1"), { id: "j1" });
  assert.deepEqual(pointInput("profile.getAi", "u1"), { userId: "u1" }); // routers/profile.ts:1121
  assert.throws(() => pointInput("combat.getBattleHistory", "x"), /not a single-record point read/);
});

test("read mode is derived from the row's own contract", () => {
  assert.equal(readMode("quests.get"), "point");
  assert.equal(readMode("quests.getAllNames"), "list");
  assert.equal(readMode("combat.getBattleHistory"), "query");
  assert.equal(readMode("combat.getBattleEntries"), "query");
});

// ---------------------------------------------------------------- 4: explicit paging bounds
test("page inputs advance by the page size and never alias page 0", () => {
  const c = canonicalInput("combat.getBattleEntries", { battleId: "b1", limit: 100 });
  assert.deepEqual(pageInput("combat.getBattleEntries", c, 0), c);
  assert.deepEqual(pageInput("combat.getBattleEntries", c, 1), { battleId: "b1", limit: 100, offset: 100 });
  assert.deepEqual(pageInput("combat.getBattleEntries", c, 3), { battleId: "b1", limit: 100, offset: 300 });
  // an explicit starting offset is respected rather than overwritten
  const c2 = canonicalInput("combat.getBattleEntries", { battleId: "b1", limit: 10, offset: 5 });
  assert.deepEqual(pageInput("combat.getBattleEntries", c2, 2), { battleId: "b1", limit: 10, offset: 25 });
  // the server's own default is used when the manifest does not set one (combat.ts:397)
  const c3 = canonicalInput("combat.getBattleEntries", { battleId: "b1" });
  assert.deepEqual(pageInput("combat.getBattleEntries", c3, 1), { battleId: "b1", offset: 30 });
  // a procedure that is not paged at source cannot be walked
  assert.throws(() => pageInput("combat.getBattleHistory", canonicalInput("combat.getBattleHistory", {}), 1), /not paged at source/);
});

test("paging bounds are explicit at parse: no crawl, no unpaged walk, no limit past the audit", () => {
  const cap = (extra) => ({ items: [], capture: { after: [{ proc: "combat.getBattleEntries", input: { battleId: "b1" }, persist: "local-only", ...extra }] } });
  assert.equal(parseManifest(cap({})).capture.after[0].pages, 1, "one page unless the manifest asks for more");
  assert.equal(parseManifest(cap({ pages: 4 })).capture.after[0].pages, 4);
  assert.throws(() => parseManifest(cap({ pages: MAX_PAGES + 1 })), new RegExp(`over the ${MAX_PAGES}-page ceiling`));
  for (const pages of [0, -1, 1.5, "3", null]) assert.throws(() => parseManifest(cap({ pages })), ManifestError, String(pages));
  // an unpaged procedure cannot be asked for more than one page
  assert.throws(
    () => parseManifest({ items: [], capture: { after: [{ proc: "combat.getBattleHistory", input: {}, persist: "local-only", pages: 2 }] } }),
    /is not paged at source/);
});
