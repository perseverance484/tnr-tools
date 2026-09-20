// The negative fixtures the plan names (§8), each one a mutation of the real Godstorm evidence.
//
// Every scenario below is a way the finished Godstorm poster actually went wrong, or a way the
// next one could. A green golden fixture only proves the tooling agrees with correct evidence; it
// is these that prove it disagrees with the wrong kind - and that it disagrees for the RIGHT
// reason, which is why each case asserts the finding code and the text, not just that something
// failed.

import { test } from "node:test";
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";
import { join } from "node:path";
import { scenario, fatalsOf, fatalText, editQuest, dropAi, AI, MARROW, STORMCOURT, REPO } from "./presentation.scenario.mjs";
import { parseSpec } from "../presentation/spec.mjs";
import { PresentationError } from "../presentation/errors.mjs";
import { STATUS } from "../presentation/assets.mjs";

const MARROW_BUNDLE = "harvests/inbox/tnr_results_1789829183863.json";
const STORM_BUNDLE = "harvests/inbox/tnr_results_1789842714086.json";
const AI_0914_BUNDLE = "harvests/inbox/tnr_results_1789402842027.json";

// ---------------------------------------------------------------------------------------------
// 1. Old floor cash-out / chest data trying to override current rewards
// ---------------------------------------------------------------------------------------------

test("a spec may not carry a rewards table at all", () => {
  // The direct form of the failure: the poster's numbers were AUTHORED, so nothing could disagree
  // with them when the content changed. The parser refuses the key by name and says who owns it.
  let err = null;
  try {
    parseSpec({
      schema: "tnr.presentation.spec.v1", evidence: "evidence.json", template: "event-poster", title: "Godstorm",
      rewards: { floor1: { money: 20000, chest: "Marrow Cache" } },
    });
  } catch (e) { err = e; }
  assert.ok(err instanceof PresentationError, "a spec carrying rewards must be refused");
  assert.match(err.message, /"rewards" is a dossier fact, not a presentation choice/);
  assert.match(err.message, /dossier\.rewards/);
  assert.match(err.message, /second content database/);

  for (const key of ["cashOuts", "chests", "battles", "keepers", "cadence", "rosterNames", "counts"]) {
    assert.throws(() => parseSpec({
      schema: "tnr.presentation.spec.v1", evidence: "e.json", template: "event-poster", title: "T", [key]: {},
    }), (e) => e instanceof PresentationError && /is a dossier fact/.test(e.message), `spec.${key} must be refused`);
  }
});

test("the old per-floor cash-outs cannot come back through an unreachable node", () => {
  // The indirect form: the removed reward nodes are still IN the record, just unreachable. Reading
  // rewards off every node in the array is exactly how a poster resurrects them.
  const r = scenario({
    files: {
      [MARROW_BUNDLE]: editQuest(MARROW, (q) => {
        q.content.objectives.push({
          id: "old_floor1_cashout", task: "dialog", description: "Floor 1 cleared.",
          reward_money: 20000, reward_tokens: 5, reward_prestige: 2, reward_items: ["chest_marrow_cache"],
          nextObjectiveId: [], attackers: [], opponentAIs: [],
        });
        return q;
      }),
    },
  });
  assert.ok(r.ok, r.ok ? "" : String(r.error));
  const rewards = r.built.dossier.rewards[MARROW];
  // the current answer is untouched
  assert.deepEqual(rewards.fullClear.reward, { money: 125000, tokens: 25, prestige: 10 });
  assert.deepEqual(rewards.intermediateCashOuts, []);
  assert.deepEqual(rewards.rewardItems, []);
  // and the stranded node is named rather than silently ignored
  assert.deepEqual(rewards.unreachableRewardNodes, ["old_floor1_cashout"]);
  const warned = r.built.lint.warnings.filter((f) => f.code === "unreachable-reward");
  assert.equal(warned.length, 1);
  assert.match(warned[0].message, /old_floor1_cashout still carries a reward but nothing reaches it; it is historical/);
});

test("a cash-out that IS reachable is reported instead of folded into the full-clear reward", () => {
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
  const warned = r.built.lint.warnings.filter((f) => f.code === "intermediate-cash-out");
  assert.equal(warned.length, 1);
  assert.match(warned[0].message, /must not fold it in/);
});

// ---------------------------------------------------------------------------------------------
// 2. A missing keeper under coverage:"all"
// ---------------------------------------------------------------------------------------------

test('coverage "all" catches a keeper no selected record can name', () => {
  const r = scenario({ files: { [AI_0914_BUNDLE]: dropAi(AI.wardenHalfEclipse) } });
  assert.ok(r.ok, r.ok ? "" : String(r.error));
  // it still FIGHTS - the battle node is untouched - so the roster is 18 and one of them is blind
  assert.equal(r.built.dossier.roster.length, 18);
  const missing = r.built.dossier.roster.find((e) => e.aiId === AI.wardenHalfEclipse);
  assert.equal(missing.resolved, false);
  assert.equal(missing.name, null);
  const fatal = fatalsOf(r.built, "roster-incomplete");
  assert.equal(fatal.length, 1, fatalText(r.built));
  assert.match(fatal[0].message, /coverage is "all" but ai 3XMsIV6Yv4jy-uaJAe52f cannot be named/);
  // and its tile has no art either, which is its own fatal rather than a blank square
  assert.equal(fatalsOf(r.built, "asset-missing").length, 1);
});

test('coverage "all" catches a spec entry list that omits one keeper', () => {
  const r = scenario({
    spec: (s) => {
      const all = Object.keys(s.roles);
      s.roster = { coverage: "all", entries: all.filter((id) => id !== AI.keeperHushedHours) };
      return s;
    },
  });
  assert.ok(r.ok, r.ok ? "" : String(r.error));
  const fatal = fatalsOf(r.built, "roster-omission");
  assert.equal(fatal.length, 1, fatalText(r.built));
  assert.match(fatal[0].message, /omits ai s6LjnqhSW85pIxYRM76Fw \(Keeper of Hushed Hours\)/);
});

test("a roster that lists a stranger is refused too", () => {
  const r = scenario({
    spec: (s) => {
      s.roster = { coverage: "all", entries: [...Object.keys(s.roles), "someOtherAiId"] };
      return s;
    },
  });
  assert.ok(r.ok, r.ok ? "" : String(r.error));
  assert.equal(fatalsOf(r.built, "roster-stranger").length, 1, fatalText(r.built));
});

test("an AI that fights but carries no role annotation is refused", () => {
  const r = scenario({
    spec: (s) => { delete s.roles[AI.mothTyrant]; return s; },
  });
  assert.ok(r.ok, r.ok ? "" : String(r.error));
  const fatal = fatalsOf(r.built, "unannotated-role");
  assert.equal(fatal.length, 1, fatalText(r.built));
  assert.match(fatal[0].message, /The Moth Tyrant\) fights in 1 battle\(s\) but the spec gives it no role/);
});

test("a role annotation cannot invent an enemy that fights nowhere", () => {
  const r = scenario({
    spec: (s) => { s.roles.notARealAiId = "keeper"; return s; },
  });
  assert.ok(r.ok, r.ok ? "" : String(r.error));
  const fatal = fatalsOf(r.built, "extraction");
  assert.ok(fatal.some((f) => /names ai notARealAiId, which fights in no reachable battle/.test(f.message)), fatalText(r.built));
});

// ---------------------------------------------------------------------------------------------
// 3 and 4. Swapped art, and wrong art of exactly the right size
// ---------------------------------------------------------------------------------------------

test("a swapped AI image is refused: the bound bytes are not what this character serves", () => {
  const r = scenario({
    spec: (s) => {
      s.assets[`ai:${AI.umbralReaver}`] = "art/godstorm/ai_godstorm_marrow_starless_monk.webp";
      return s;
    },
  });
  assert.ok(r.ok, r.ok ? "" : String(r.error));
  const fatal = fatalsOf(r.built, "asset-mismatch");
  assert.equal(fatal.length, 1, fatalText(r.built));
  assert.match(fatal[0].message, /Umbral Reaver currently serves/);
  assert.match(fatal[0].message, /this is not this entity's art/);
});

test("wrong art of EXACTLY the right size is refused, and not because of its size", () => {
  // The whole reason the image-pack contract exists: a 1.7 MB master rode into a live run behind a
  // 207 KB filename, and a byte ledger is what caught it. A ledger cannot catch the next one, where
  // the replacement happens to be the same size. Here the working-tree file is a different image
  // padded to the same length, and the pack entry is regenerated to agree with it, so every
  // self-consistent check passes. What refuses it is the blob at the commit the pack names.
  const real = readFileSync(join(REPO, "art/godstorm/ai_godstorm_marrow_umbral_reaver.webp"));
  const other = readFileSync(join(REPO, "art/godstorm/ai_godstorm_marrow_starless_monk.webp"));
  const sameSize = Buffer.concat([other.subarray(0, real.length)], real.length);
  assert.equal(sameSize.length, real.length, "the fixture must be byte-for-byte the same LENGTH");
  assert.notEqual(createHash("sha256").update(sameSize).digest("hex"), createHash("sha256").update(real).digest("hex"));

  const swappedSha = createHash("sha256").update(sameSize).digest("hex");
  const r = scenario({
    extraFiles: { "art/godstorm/ai_godstorm_marrow_umbral_reaver.webp": sameSize },
    files: {
      // the pack is "regenerated" to match the new file: same bytes count, new digest
      "archive/spent-manifests/push-2026-09-19/53_godstorm_failed_items_repair.json": (m) => {
        m.imagePack.files["ai_godstorm_marrow_umbral_reaver.webp"].sha256 = swappedSha;
        return m;
      },
    },
  });
  assert.ok(r.ok, r.ok ? "" : String(r.error));
  const entry = r.built.dossier.assets.entries.find((e) => e.name === "Umbral Reaver");
  assert.equal(entry.bytes, real.length, "the fixture's point is that the size still matches");
  assert.equal(entry.declaredBytes, real.length);
  assert.equal(entry.refVerified, false);
  assert.equal(entry.status, STATUS.MISMATCH);
  const fatal = fatalsOf(r.built, "asset-mismatch");
  assert.equal(fatal.length, 1, fatalText(r.built));
  assert.match(fatal[0].message, /blob at the commit the pack names/);
  assert.ok(!/bytes|size|length/i.test(fatal[0].message.replace(/the bytes that were uploaded/, "")), "the refusal must not rest on a byte count");
});

test("art bound to a file no selected pack names is refused", () => {
  const r = scenario({
    spec: (s) => { s.assets[`ai:${AI.umbralReaver}`] = "art/style_refs/whatever.webp"; return s; },
  });
  assert.ok(r.ok, r.ok ? "" : String(r.error));
  const fatal = fatalsOf(r.built, "asset-mismatch");
  assert.equal(fatal.length, 1, fatalText(r.built));
  assert.match(fatal[0].message, /not bound by any selected image pack/);
});

test("a bound path that tries to escape the repository is refused", () => {
  const r = scenario({
    spec: (s) => { s.assets[`ai:${AI.umbralReaver}`] = "../../etc/passwd"; return s; },
  });
  assert.ok(r.ok, r.ok ? "" : String(r.error));
  assert.equal(fatalsOf(r.built, "asset-mismatch").length, 1, fatalText(r.built));
});

// ---------------------------------------------------------------------------------------------
// 5. A scene background declared a top-level location
// ---------------------------------------------------------------------------------------------

test("a scene background cannot be named as a top-level location", () => {
  // Upper Court, Binding Dais Active and Binding Dais Released were the old poster's "locations".
  // They are three gameAsset records, two of which are one room in two states.
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
// 6 and 7. Stale dialogue anchors, and stale wording
// ---------------------------------------------------------------------------------------------

test("a narrative anchored to an objective id that does not exist is refused", () => {
  const r = scenario({
    spec: (s) => { s.story.marrow.sourceObjectives = ["d1_1", "d4_99", "d5_victory"]; return s; },
  });
  assert.ok(r.ok, r.ok ? "" : String(r.error));
  const fatal = fatalsOf(r.built, "extraction");
  assert.ok(fatal.some((f) => /objective id "d4_99" does not exist in any selected current quest record/.test(f.message)), fatalText(r.built));
});

test("a narrative anchored to a node the graph no longer reaches is refused", () => {
  const r = scenario({
    files: {
      [MARROW_BUNDLE]: editQuest(MARROW, (q) => {
        // the node stays in the record but nothing points at it any more - the exact shape of a
        // stale anchor that still "resolves" against a raw objective list
        for (const o of q.content.objectives) {
          if (Array.isArray(o.nextObjectiveId)) o.nextObjectiveId = o.nextObjectiveId.filter((c) => c.nextObjectiveId !== "b4_1");
          if (o.nextObjectiveId === "b4_1") o.nextObjectiveId = "d5_1";
        }
        return q;
      }),
    },
    spec: (s) => { s.story.marrow.sourceObjectives = ["d1_1", "d4_1", "d5_victory"]; return s; },
  });
  assert.ok(r.ok, r.ok ? "" : String(r.error));
  // d4_1 is the dialog BEFORE b4_1; severing b4_1 strands the rest of that floor
  const fatal = fatalsOf(r.built, "extraction");
  assert.ok(fatal.length, fatalText(r.built));
});

test("old Tower/Dawnless wording cannot be supplied as a current narrative source", () => {
  // The anchors are real and current. Only the prose is stale, which is what an anchor check alone
  // cannot see: the summary names things the selected evidence has never heard of.
  const r = scenario({
    spec: (s) => {
      s.story.marrow.text = "The player descends the Dawnless Tower beneath Stormcourt, where the Unbroken Thread kept the elder sister, and climbs toward the Ashen Gate.";
      return s;
    },
  });
  assert.ok(r.ok, r.ok ? "" : String(r.error));
  const fatal = fatalsOf(r.built, "extraction");
  const text = fatal.map((f) => f.message).join("\n");
  for (const stale of ["Dawnless", "Tower", "Ashen", "Gate"]) {
    assert.match(text, new RegExp(`names "${stale}"`), `"${stale}" must be reported as unsupported wording:\n${text}`);
  }
  assert.match(text, /appears in none of its source objectives and in no current record of this subject/);
});

test("the wording check does not fire on prose the current evidence does carry", () => {
  const r = scenario({
    spec: (s) => {
      s.story.marrow.text = "Tally-marks record the elder sister's captivity for the Unbroken Thread, and the Warden of the Half Eclipse guards the stair beyond the divided threshold.";
      return s;
    },
  });
  assert.ok(r.ok, r.ok ? "" : String(r.error));
  assert.deepEqual(r.built.lint.fatal, [], fatalText(r.built));
});

test("a narrative with no source anchor at all is refused by the parser", () => {
  assert.throws(() => parseSpec({
    schema: "tnr.presentation.spec.v1", evidence: "e.json", template: "event-poster", title: "T",
    story: { marrow: { text: "Something happened." } },
  }), (e) => e instanceof PresentationError && /must cite at least one source objective id/.test(e.message));
});

// ---------------------------------------------------------------------------------------------
// 8. Missing or unverified evidence
// ---------------------------------------------------------------------------------------------

test("an evidence record whose file is not there refuses the build", () => {
  const r = scenario({
    evidence: (e) => {
      e.records.find((x) => x.id === "marrow-quest").path = "harvests/inbox/tnr_results_0000000000000.json";
      return e;
    },
  });
  assert.equal(r.ok, false);
  assert.match(r.error.message, /evidence "marrow-quest": harvests\/inbox\/tnr_results_0000000000000\.json could not be read/);
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
  assert.match(r.error.message, /the quests\.get capture for OSADdXqostbyVliCxWk6k did not read back ok/);
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
  assert.match(r.error.message, /holds quest "someOtherQuestId"/);
});

test("an evidence path that tries to leave the repository is refused before anything is read", () => {
  for (const bad of ["../secrets.json", "/etc/passwd", "harvests/../../x.json", "harvests\\inbox\\x.json"]) {
    const r = scenario({
      evidence: (e) => { e.records.find((x) => x.id === "marrow-quest").path = bad; return e; },
    });
    assert.equal(r.ok, false, `${bad} must be refused`);
    assert.match(r.error.message, /path /);
  }
});

test("an evidence package that states a fact is refused", () => {
  // The package selects sources. The moment it can carry a number, it is a second database.
  const r = scenario({
    evidence: (e) => { e.records[0].battles = 25; return e; },
  });
  assert.equal(r.ok, false);
  assert.match(r.error.message, /unknown key "battles"/);
});

test("an evidence package with no quest record has nothing to present", () => {
  const r = scenario({
    evidence: (e) => { e.records = e.records.filter((x) => x.kind !== "quest"); return e; },
  });
  assert.equal(r.ok, false);
  assert.match(r.error.message, /selects no quest record/);
});

test("the failed run that supplies Marrow Vaults is reported, not hidden and not used blindly", () => {
  const r = scenario({});
  assert.ok(r.ok, r.ok ? "" : String(r.error));
  const warned = r.built.lint.warnings.filter((f) => f.code === "evidence");
  assert.ok(warned.some((f) => /tnr_results_1789829183863\.json is from a run whose outcome was "failed"/.test(f.message)), "the run outcome must be surfaced");
  assert.deepEqual(r.built.lint.fatal, [], "a capture that read back ok is still evidence");
});

// ---------------------------------------------------------------------------------------------
// 9. Historical-only art where exact-current is required
// ---------------------------------------------------------------------------------------------

test("art this character used to serve is refused as historical, not mistaken for a swap", () => {
  // The five Marrow avatars were replaced on 2026-09-19. Binding a file whose upload became the
  // PRE-replacement avatar is a different mistake from binding somebody else's portrait, and the
  // remedy is different too, so the registry must tell them apart.
  const older = JSON.parse(readFileSync(join(REPO, AI_0914_BUNDLE), "utf8"));
  let oldAvatar = null;
  const find = (node) => {
    if (Array.isArray(node)) return node.forEach(find);
    if (!node || typeof node !== "object") return;
    if (node.userId === AI.umbralReaver && typeof node.avatar === "string") oldAvatar = node.avatar;
    Object.values(node).forEach(find);
  };
  find(older);
  assert.ok(oldAvatar, "the 09-14 bundle must carry Umbral Reaver's earlier avatar");

  const r = scenario({
    files: {
      // the packed file is recorded as having been uploaded to the avatar the character served
      // BEFORE the repair run replaced it
      [STORM_BUNDLE]: (b) => {
        b.idmap["ai_godstorm_marrow_umbral_reaver.webp"] = oldAvatar;
        return b;
      },
    },
  });
  assert.ok(r.ok, r.ok ? "" : String(r.error));
  const entry = r.built.dossier.assets.entries.find((e) => e.name === "Umbral Reaver");
  assert.equal(entry.status, STATUS.HISTORICAL);
  assert.match(entry.notes.join(" "), /is the art Umbral Reaver served at 2026-09-14/);
  const fatal = fatalsOf(r.built, "asset-historical");
  assert.equal(fatal.length, 1, fatalText(r.built));
  assert.match(fatal[0].message, /Exact-current art is required for a named entity tile/);
  assert.equal(fatalsOf(r.built, "asset-mismatch").length, 0, "historical art must not be reported as a swap");
});

test("a deterministic render refuses art that is current but not materialised", () => {
  // P1 makes zero live requests, so thirteen of the eighteen are exact-current-remote. That is a
  // warning here and a REFUSAL the moment a caller says it intends to render deterministically,
  // which is the contract P2 has to meet.
  const warnOnly = scenario({});
  assert.ok(warnOnly.ok);
  assert.deepEqual(warnOnly.built.lint.fatal, []);
  assert.equal(warnOnly.built.lint.warnings.filter((f) => f.code === "asset-remote").length, 13);

  const strict = scenario({ requireExactBytes: true });
  assert.ok(strict.ok);
  const fatal = fatalsOf(strict.built, "asset-not-materialised");
  assert.equal(fatal.length, 13, fatalText(strict.built));
  assert.match(fatal[0].message, /materialised into the content-addressed cache and hashed first/);
});

// ---------------------------------------------------------------------------------------------
// Spec hygiene
// ---------------------------------------------------------------------------------------------

test("the spec parser is closed: an unknown key is refused rather than ignored", () => {
  assert.throws(() => parseSpec({
    schema: "tnr.presentation.spec.v1", evidence: "e.json", template: "event-poster", title: "T", tittle: "typo",
  }), (e) => e instanceof PresentationError && /unknown key "tittle"/.test(e.message));
});

test("a spec of the wrong schema version is refused", () => {
  assert.throws(() => parseSpec({ schema: "tnr.presentation.spec.v2", evidence: "e.json", template: "event-poster", title: "T" }),
    (e) => e instanceof PresentationError && /schema must be "tnr\.presentation\.spec\.v1"/.test(e.message));
});

test("a spec may not invent a template or a role", () => {
  assert.throws(() => parseSpec({ schema: "tnr.presentation.spec.v1", evidence: "e.json", template: "poster", title: "T" }),
    (e) => /template must be one of/.test(e.message));
  assert.throws(() => parseSpec({
    schema: "tnr.presentation.spec.v1", evidence: "e.json", template: "event-poster", title: "T", roles: { x: "miniboss" },
  }), (e) => /role must be one of/.test(e.message));
});
