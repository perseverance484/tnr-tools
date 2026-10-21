# QA ticket pipeline — find, fix, submit, track (Forge Next Phase 1 as stage one)

**Status:** SHELVED 2026-10-21 (director: "skip this for now, seems excessive"). Kept for reference; not under review and not an implementation contract.  
**Date:** 2026-10-21  
**Repository:** `perseverance484/tnr-tools`  
**Drafted from:** `main@43af7ddf6ba50303330a79e9ebf9fbdd5c663282`  
**Implementation owner:** Fable / Claude Code  
**Independent reviewer:** ChatGPT  
**Director:** dauntless  
**Decision of record:** RUL-2026-10-21-006 (this project is next; Forge Next Phase 1 is its stage one)  
**Builds on, does not replace:** `state/prompt_forge_next_phase1.md` (READY/FROZEN, 2026-09-17). Its policy, scope limits, tests and gates all still apply to stage one; §3 below lists the only additions.  
**Upstream game source inspected while drafting:** `studie-tech/TheNinjaRPG@dcf1cea` (2026-10-20) — reverify at implementation start  
**Live-game policy for implementation and review:** ZERO LIVE REQUESTS / ZERO LIVE WRITES

---

## 1. Why

The repository can already find content problems and submit fixes, but it cannot learn what happened to them.

| Step | What exists | Gap |
|---|---|---|
| Find | `scripts/qa_live.py` (offline, 30/30 self-test): 2,800 findings on 2026-10-20, each with record id, check code, severity S1–S5, certainty and a suggested fix (`docs/reviews/QA_LIVE_2026-10-20.findings.json`) | One snapshot. Its data came from 34 public reads sent by an agent session under a standing exception that was proposed but never approved |
| Fix | Manifests written by hand, one ticket per push (push/132–143), plus `docs/reviews/QA_REVISIT_2026-10-20.md` | No link from a fix back to its finding; no record of what is open |
| Submit | Forge suggest mode (0.8.x) sends edits to the game's content review desk | Works |
| Track | Forge's **Check suggestions** writes each status into the browser journal only | **Broken.** All 92 suggestions in committed bundles still read `PENDING`. Outcomes and reviewer reasons never reach the repository, and are lost when a job leaves the journal |

The director cannot see the outcomes of the 92 suggestions sent on 2026-10-19 and 2026-10-20. Closing that loop is the first deliverable.

## 2. Goal

A repeatable loop, operator-run at every live step:

1. **Snapshot:** capture the live catalog and the review desk's state into committed bundles.
2. **Detect:** run `qa_live.py` over the snapshot.
3. **Ticket:** add each new finding to a ledger; never duplicate an open ticket.
4. **Fix:** generate suggest-mode manifests for mechanical fix classes; raise decision tickets for the rest.
5. **Submit:** the operator runs the manifests in Forge.
6. **Track:** the next snapshot records each suggestion's status and reason in the ledger.
7. **Verify:** a ticket closes only when a later snapshot shows the finding gone.

## 3. Stage one — Forge Next Phase 1, with three additions

Implement `state/prompt_forge_next_phase1.md` as frozen: capture tiers (`repo-safe`, `local-only`, `projected`), the fail-closed research-read registry, input-aware paged reads, honest non-success evidence, and every test and gate it lists. Phase 1 deliberately admits a procedure only "when a committed, reviewed research manifest/work package actually needs it" (RUL-2026-09-17-002). This brief is that work package. It adds:

### 3.1 Review-desk registry rows

| Procedure | Facts at `dcf1cea` (reverify) | Tier |
|---|---|---|
| `contentReview.getQueue` | `protectedProcedure`. Input `reviewQueueSchema`: `status` (one of PENDING, APPLIED, REJECTED, OUTDATED, REVERTED; required), `category?`, `source?` (AGENT, STAFF), `entityType?`, `cursor` = row offset, `limit` 1–50 (default 25). Returns `{items, nextCursor, canReview}`. Non-reviewers see only their own suggestions. PENDING sorts by `createdAt` ascending, others by `statusChangedAt` descending. | `projected` (D2) |
| `contentReview.getProposal` | `protectedProcedure`. Input `{id}`. Returns the proposal or `null` for non-staff or someone else's (non-reviewer). | `projected` (D2) |

Both must be recorded with a **side-effect note**. When the caller can review, both run `refreshProposalFreshness` (`libs/contentReview/outdate.ts`). That marks PENDING rows whose basis changed as OUTDATED (`markOutdated` writes). The review desk does the same when a reviewer opens it, but it means these are queries that can write. See D3.

`getQueue` paging is an offset that shifts when rows go OUTDATED mid-read (the server returns `offset + limit - outdated.size`). The paged-read contract must use the server's `nextCursor` verbatim, bound the page count, and record a partial walk as partial.

Forge already calls both procedures from suggest mode (`forge/src/review/contract.json`, pinned at `2aed7e4`). The new rows reuse those audited facts at the declared pin; they do not move the pin.

### 3.2 Catalog snapshot rows (only if D1 = Forge)

`jutsu.getAll`, `item.getAll`, `quests.getAll`, `bloodline.getAll`, `gameAsset.getAll` and the five `getAllNames` lists, all `query` / `public`. Each `getAll` is paged, and `hidden: true` returns hidden records for jutsu, item, quests and bloodline. `gameAsset.getAll` ignores `hidden` and needs one `type` filter per asset type. The 2026-10-20 pass needed 34 calls in total.

Tier `repo-safe`. These are the same content records the audited point reads (`jutsu.get` etc.) already persist in full, so the rows hold no new class of data. They are much larger, though (about 16 MB raw for the whole catalog), so:

- page bodies stay under the existing per-body ceiling (`MAX_FULL_CAPTURE_BYTES`, 512 KiB), or the implementation proposes a separately reviewed ceiling for this class, with an honest failure above it;
- a snapshot may span several manifests and bundles. The ledger tooling joins them by capture time.

### 3.3 One snapshot manifest family

Repository-generated, read-only capture manifests that take one consistent snapshot: the catalog (if D1 = Forge), then `getQueue` for every status, for `source: STAFF` and for `source: AGENT` (D4). They start and end with the same `getAllNames` counts, so a record created mid-snapshot shows up as a change; the fresh AI census push/157–161 used this pattern. They contain no mutations, are refused in suggest mode, and run only when the operator chooses.

**Out of stage one:** the generators, the ledger and any change to suggest mode itself.

## 4. Stage two — the ticket ledger (repository tooling)

### 4.1 Files

```text
state/tickets/ledger.json     canonical; edited only by scripts/tickets.py
state/tickets/TICKETS.md      generated projection; never hand-edited
scripts/tickets.py            validate / bootstrap / import / sync / plan / render
```

It is not a content workstream: workstreams hold session-sized project tasks, while tickets are record-sized and number in the hundreds.

### 4.2 A ticket

| Field | Meaning |
|---|---|
| `key` | Stable identity: `<check code>:<entity>:<record id>`. A re-run that finds the same defect finds the same ticket. |
| `findings` | The finding rows (severity, certainty, evidence, suggested fix, snapshot id) that opened or re-confirmed it |
| `record` | Entity, id, name, hidden flag at the latest snapshot |
| `class` | `mechanical` (a generator may fix it) or `decision` (needs a ruling, CLAUDE.md §10) — see D5 |
| `state` | See 4.3 |
| `fix` | Manifest path and commit, and the exact fields changed |
| `suggestion` | Review-desk id, title tag, submitted at, status, `rejectReason`, `reviewNote`, `outdatedReason`, status changed at |
| `ruling` | RUL id for `decision`, `wont_fix` or `deferred` outcomes |
| `history` | Append-only transitions with snapshot or bundle references |

### 4.3 States

```text
OPEN ──► READY (mechanical) ──► STAGED (manifest committed) ──► SUBMITTED (suggestion id known)
  │                                                                │
  └──► DECISION_NEEDED ──► READY | WONT_FIX | DEFERRED (ruling)    ├──► APPLIED ──► VERIFIED (finding gone in a later snapshot)
                                                                   │        └──────► REOPENED (finding still present)
                                                                   ├──► REJECTED (reason kept) ──► READY | WONT_FIX
                                                                   ├──► OUTDATED ──► READY (rebuild from fresh record)
                                                                   └──► REVERTED ──► OPEN
```

Every transition comes from evidence: a findings file, a committed manifest, a results bundle, a snapshot or a ruling. None comes from free-text editing. `tickets.py validate` fails on an illegal transition.

### 4.4 Commands

- `bootstrap`: create SUBMITTED tickets for the 92 historical suggestions from the committed push/125–156 bundles (their journal items carry the suggestion ids), matched to `QA_LIVE_2026-10-20` findings where a ticket number or record id links them.
- `import <findings.json>`: open tickets for new keys; re-confirm existing ones; mark any VERIFIED ticket that has a finding again as REOPENED.
- `sync <bundle> [...]`: apply review-desk statuses from stage-one snapshot bundles.
- `plan`: list the next READY batch under the invariants in §6 and emit generator input.
- `render`, `validate`.

## 5. Stage three — generators and the loop

- **Generators:** one per mechanical fix class. Each produces a suggest-mode manifest with a specific per-record rationale (RUL-2026-10-19-007) and records `STAGED`. Candidate first classes, subject to D5: `TXT-PLACEHOLDER`, `TXT-EMPTY` (only where a line can be derived, not invented), `TXT-TYPO`, `TXT-ARTICLE`, `TXT-NAME-SPACE`, `REF-REWARD`, `REF-QUEST-PREREQ` where the intended target is unambiguous, and `IMG-BROKEN-SCENE` where a replacement asset exists. Written prose stays director-reviewed, as for the battle-line pass.
- **Decision tickets:** balance (`OUT-*`, `AI-STATS-*`), rewards, retiring or hiding content, new art. They produce a short decision list for the director, never a manifest.
- **The loop:** snapshot → `qa_live.py check` → `tickets.py import` and `sync` → `plan` → generate → operator submits → next snapshot. One cycle per operator session; nothing runs in the background (Phase 1 §5.4).

## 6. Invariants

1. **One open suggestion per record.** A suggestion carries the whole record, so a second one on the same record can undo the first if approved after it (the Bloodthorn Cache case). `plan` refuses a record that has a SUBMITTED ticket, or a PENDING AGENT or STAFF proposal in the latest snapshot.
2. **OUTDATED is rebuilt, never re-sent.** Any edit to the record before approval outdates the suggestion; the fix is regenerated from a fresh record.
3. **Jutsu an AI has equipped.** Editing an equipped jutsu severs that AI's combat link (laws 18, 60), and a suggestion applies whenever a reviewer approves it, so the unequip and re-equip cannot be timed around it. `plan` must flag any jutsu ticket whose record is equipped by an AI in the latest census, and keep it out of suggest batches, until the director picks a pattern: a direct write between an unequip and a re-equip, as push/162–177 did, or unequip, then suggest, then re-equip after APPLIED, as push/126–128 did.
4. **What suggest mode cannot do:** quests are refused (objective locations are hidden from non-editors), as are creates that later items reference and Bloodright trees. `plan` routes those tickets to the direct-write path or to a decision.
5. **The game's own audit.** The game runs an automated content audit (`source: AGENT`, submitted from CI) whose next run reads reviewers' rejection reasons. Our tickets never duplicate a record it has pending (invariant 1).
6. **The ledger is evidence, not authority.** Doctrine, engine laws, rulings and generated contracts keep their owners (CLAUDE.md §3). A ticket never settles balance, rewards, rarity, publishing or final prose (CLAUDE.md §10).

## 7. Director decisions

Settled: **RUL-2026-10-21-006**, this project with Phase 1 as stage one.

Open — each needs an answer before the stage that uses it:

| # | Decision | Options | Recommendation | Needed by |
|---|---|---|---|---|
| D1 | How catalog snapshots are taken | (a) operator-run Forge capture manifests (§3.2–3.3); (b) approve the standing public-read exception proposed in `QA_LIVE_2026-10-20.md` so an agent session reads the public catalog directly | **(a).** It keeps every live read operator-run and inside Forge's audited transport, and stage one is building the paged reads anyway. (b) is faster to start but widens the CLAUDE.md §6 boundary | Stage one |
| D2 | What review-desk data may enter the public repository | `projected` fields: `id, title, category, status, source, createdAt, statusChangedAt, expiresAt, rejectReason, reviewNote, outdatedReason, targets[].{entityType, entityId, operation, fields}`. Exclude `createdBy`, `reviewedBy` (staff usernames), `agentName`, `runUrl`, `targets[].name/image` and all change bodies | **Approve the list as written.** `reviewNote` is free text a reviewer types; it is the "why" you asked for, but it lands in a public repository | Stage one |
| D3 | Admit queries that can mark OUTDATED | (a) admit both, with the side effect recorded and the read confined to snapshot manifests; (b) read only non-PENDING statuses (`getProposal` still refreshes, so PENDING truth would be lost) | **(a).** It changes nothing a reviewer opening the desk would not change | Stage one |
| D4 | Read AGENT proposals too | (a) STAFF and AGENT, AGENT projected to `id, status, source, targets[].{entityType, entityId}` for de-duplication; (b) STAFF only | **(a)** | Stage one |
| D5 | Which finding classes are mechanical | The candidate list in §5 | Approve per class; start with the text classes | Stage three |
| D6 | Equipped-jutsu pattern (invariant 3) | Direct write between an unequip and a re-equip, or unequip → suggest → re-equip after APPLIED | Decide per batch; the direct write is proven at scale (push/162–177) | Stage three |

## 8. Scope

**In scope:** Phase 1 as frozen plus §3; the snapshot manifest generator; `scripts/tickets.py`, its schema, self-test and projection; bootstrapping the 92 historical suggestions; the first generator classes once D5 is decided; the `qa_live.py` changes needed to name its snapshot and emit stable keys.

**Out of scope:** everything Phase 1 excludes (visual shell, Quest Studio, Content Admin, Publish, generic API browsing, background polling); any change to suggest-mode submission; approving, rejecting or reverting suggestions; auto-submitting anything; settling any balance or reward finding; adopting a new game-source pin inside this task.

## 9. Mandatory task start

Phase 1 §3, plus:

1. re-measure the Forge baseline; Phase 1's numbers are Phase 0's. At drafting, Forge is `0.8.1` and `forge_bundle.js` is 412,173 bytes raw against a 420,000 / 100,000 budget (`forge/tools/check_bundle_budget.mjs`), so there is very little headroom. Apply Phase 1 §10 to any raise;
2. reverify the §3.1 facts at Forge's declared pin and at current upstream; split a pin adoption if they disagree materially;
3. read `docs/design/FORGE_SUGGEST_MODE_SCOPE.md`, `forge/src/review/contract.json`, `scripts/qa_live.py`, `docs/reviews/QA_LIVE_2026-10-20.md` and `QA_REVISIT_2026-10-20.md`, and the push/125–156 bundles;
4. read RUL-2026-09-17-001/002, RUL-2026-10-19-007, RUL-2026-10-20-001 and RUL-2026-10-21-002..006.

## 10. Tests and gates

- **Stage one:** every Phase 1 §9 test, plus: both review rows refused for a mutation-shaped input; the projection exports exactly the D2 fields and nothing nested beyond them; a fake `getQueue` that outdates rows mid-walk advances by the server's `nextCursor` and reports a walk cut short as partial; side-effect notes present in the registry; snapshot manifests contain zero mutations and are refused in suggest mode.
- **Stage two:** `tickets.py --selftest`, covering every legal and illegal transition, key stability across two imports, REOPENED on a regressed finding, the one-open-suggestion lock against STAFF and AGENT pendings, and bootstrap over fixtures shaped like the committed push/125–156 bundles. `validate` and `render --check` are gates on every ledger change.
- **Stage three:** each generator's output passes `validate.py --strict` and `forge/tools/check_manifest.mjs`; its rationales are per record; no generator emits a balance, reward or decision-class change.
- Canonical Forge CI, doc guards where `skills/` or doctrine change (CLAUDE.md §8), gates never masked.

## 11. Live-game boundary

Implementation and review: zero live requests and zero writes. Fixtures, fake transport and committed bundles only. In operation, every live read and every submission is an operator action in Forge (CLAUDE.md §6), unless D1 (b) is approved, and then only within that ruling's conditions.

## 12. Handoff

Per stage, through `docs/workflows/IMPLEMENTATION_HANDOFF.md`, with a frozen SHA and independent review before integration:

- **Stage one:** the Phase 1 §14 handoff, plus the three registry rows, their source evidence and side-effect notes, the projection, and the snapshot manifests.
- **Stage two:** ledger schema, self-test counts, and a bootstrap run over the committed bundles that shows the 92 suggestions.
- **Stage three:** the generator classes enabled, and the first batch's ledger diff.

Stage two may start once stage one is frozen for review; it needs only committed bundles and fixtures. Stage three waits for D5, and for D6 wherever a batch touches equipped jutsu.

## 13. Not begun

No code, ledger, manifest or snapshot exists for this project yet. The 92 historical outcomes stay unknown until the first snapshot. Meanwhile the director can read them off the game's review desk page, and `bootstrap` will take them as manual evidence with the source noted.
