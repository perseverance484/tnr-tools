# J. Migration and Builder retirement

**Status:** planning only. Nothing here deprecates, modifies or uninstalls the Builder, moves a release pin, migrates a manifest contract or touches the live game; the pass forbids all of that (`00_CONTEXT.md` §00.4, brief §16). This section states the conditions under which the Builder stops being needed, how the operator is told, what fallback exists at each stage, and what the storage and contract migrations must guarantee. Every date and ordering decision stays the director's (K-11).

**Scope.** J answers four questions and no others. First, which measurable gates end the Builder's job (§J.1), taking `B_PARITY_MATRIX.md` §B.4's gates G-01 to G-10 as given and adding the three the parity matrix does not carry. Second, what the transition looks like while both tools are installed on one origin (§J.2). Third, what a Forge Next release must do to the data already on the operator's phone (§J.3) and to the two contracts the repository depends on, manifests in (§J.4) and results out (§J.5). Fourth, what the release, pin and loader mechanics of an actual retirement are (§J.6) and what is explicitly not retired with the write path (§J.7). Section F owns the architecture design that these requirements constrain, section G owns phase placement, section I owns the test strategy. None of F, G or I is on disk at this SHA (`docs/forge_next/` holds `00_CONTEXT`, `A`, `B`, `C`, `D_IA_AND_JOURNEYS`, `D_VISUAL_SYSTEM`, `E`, `H`, `J` and `K`; Observed). J therefore states requirements and sequence only, names those sections as owners, and **carries no phase numbers of its own**. There is one ordering in J and it is the stage ladder in §J.2.

**Method and inputs.** `B_PARITY_MATRIX.md` §B.4 is the text of record for gates G-01 to G-10. The two middle columns of §J.1's table are **pointers, not the gate**: they are short enough to read at a glance and they do drop clauses, so where a pointer and §B.4 differ, §B.4 wins. Only G-11 to G-13 are stated in full here, because no other section carries them. That is `CLAUDE.md` §7 applied honestly: a pointer that says it is a pointer is not a second copy of the rule. Evidence read for this section: `evidence/parity-matrix.json` (61 capability rows, 7 hard and 9 conditional blockers), `evidence/harvest-evidence.json` (42 committed bundles, 41 manifests: 35 JSON plus 6 zip packs), the repository's own zip census re-derived in this pass (Observed: 9 committed push packs in total, 6 of them inside the harvest census scope; §J.4), `evidence/repo-consumers.json` (the bundle contract row by row), `A_ARCHITECTURE_MAP.md` §A.5, §A.8 and §A.10, `C_WORKFLOW_INVENTORY.md` §C.2 for which workflows still run on the Builder, `H_RISK_REGISTER.md` R-09, R-10, R-15, R-19, and the code cited inline. The design panel produced no architecture or data synthesis at this SHA (only a visual synthesis and the two information-architecture proposals exist in the panel output), so **panel synthesis unavailable at this SHA; the storage-migration recommendation in §J.3 is derived by the planning owner** from the code and R-09, with two alternatives kept and the reason each lost. `F_ARCHITECTURE_RECOMMENDATION.md` is not on disk at this SHA either, so §J.3 states migration requirements only and names section F as the owner of the journal v2 record design.

**Reconciliation rows applied.** U-J-01 (retirement gates gain a research-read tier, ingress parity including local zip packs and Studio-branch manifests, and the R-19 parity-guard fix; the Builder read path stays until the research tier lands) is applied in §J.1 rows G-11 to G-13, §J.2 stage 2 and §J.7. U-J-02 (additive journal v2 for sync state and Studio records, fixtures from real exported journals, readable-or-refused by the previous version) is applied in §J.3.

**Evidence tiers.** Claims here carry the tiers `docs/00_INDEX.md` defines. Source-verified means a line of code or committed text was read for this section. Behaviour-proven means a committed artefact records the behaviour. Observed means a count or listing taken from the repository. Inferred marks anything that would need a real browser, a real device or an external service to confirm, and no tier is upgraded anywhere below. The Inferred claims in this section are named in place: that jsDelivr keeps serving a pinned bundle commit after the file leaves `main` (§J.2 stage 5, §J.6 step 3) and that persistent storage is actually granted on the operator's browser (§J.3). Every other claim below is Source-verified, Behaviour-proven or Observed at this SHA.

**Abbreviations.** `SSC` = `docs/design/FORGE_NEXT_SAFETY_STATE_PRESENTATION_CONTRACT.md`, `CPY` = `docs/design/FORGE_NEXT_UI_COPY_AND_STATE_LANGUAGE.md`, `RB` = `docs/design/FORGE_NEXT_REPO_BACKED_STUDIO_ARCHITECTURE.md`, each at `chatgpt/forge-quest-studio-foundation@824c4d58` and cited as `ABBR:line`. Files that exist only on that branch carry the prefix `824c4d58:`. Unprefixed `forge/src/*`, `skills/*`, `.github/*` paths are `main@305a28f`.

## J.1 Retirement gates

G-01 to G-10 are `B_PARITY_MATRIX.md` §B.4's gates and keep their ids, wording and owners there. G-11 to G-13 are added by this section because the parity matrix's rows do not cover them: a capability row cannot carry the persistence tier that research reads land in, the ingress surface as a whole, or a repository guard that breaks on Forge output. **The last column is derived from the stage ladder and from nothing else.** It names the stage whose entry condition includes the gate, so a gate and a stage can never disagree: the ladder is the ordering and the column is a view of it. J carries no phase column at all. The earliest phase in which a gate can honestly be measured is section G's to place, and section G does not exist at this SHA, so no phase number appears here to be contradicted later. Where a gate also waits on a user-owned decision, that decision is named in the table that follows the gates rather than folded into the ordering.

Owners are not repeated here either. `B_PARITY_MATRIX.md` §B.4 records them, and the pattern holds for the three new rows: Fable measures every Lane A clause, the director owns the G-10 ruling, and any clause that needs a real device or a real live tap belongs to the operator.

Every gate below is written so that it can actually be reached. Two were not, and both were rewritten rather than defended: G-12 no longer waits on the ruling that waits on it, and G-13 no longer asks for an exit status the code cannot produce. Both changes are stated in the rows themselves.

| Gate | What must be true | Measured how | Evidence today | Phase |
|---|---|---|---|---|
| G-01 | Zip push packs run in Forge with byte-ledger verification (`B_PARITY_MATRIX.md` §B.4) | Fixture replay of the four spent packs plus one user-controlled live smoke pack | 6 committed zip packs carried all 26 asset creates and the 31-quest icon swap; Forge has no zip reader (`evidence/harvest-evidence.json`; P-06, P-07) | 1 |
| G-02 | The audited registry covers the procedures real research uses (§B.4) | Registry rows transcribed from the pin with the auth invariant test; `push/05` and `push/06` replay to a bundle `harvest.py index` reads | `procedure()` throws for anything outside the 43 rows (`forge/src/transport/procedures.mjs:70-73`); both manifests ran on Builder v4.32 on 2026-09-12 | 1 |
| G-03 | Paged and filtered list captures with persisted bodies (§B.4) | Journalled input equals sent input; the archived `*.gen.py` generators emit byte-identical manifests from a Forge bundle | `list()` refuses any non-name path (`forge/src/budget/reader.mjs:72-78`); summary captures carry no body (`forge/src/runner/runner.mjs:589`) | 1 |
| G-04 | Partial quest edits without an escape hatch (§B.4) | Fixture over the archived `{hidden}` and `{image}` shapes, plus a named refusal for the raid columns | 6 manifests needed `skipPreflight` on the Builder (`evidence/harvest-evidence.json`) | 2 |
| G-05 | Enum and task-vocabulary preflight derived from the pin (§B.4) | Derived sets with provenance; a typo costs no live row in FakeGame | Forge refuses unknown keys but never values (`forge/src/runner/validate.mjs:16-21`) | 2 |
| G-06 | In-tool recovery: retry a FAILED step, safe re-run of a finished manifest, idmap import/export/reset (§B.4) | Three fixtures, one per clause; the retry is journalled as a new phase attempt, never a second create | No Forge path; `Retry` may only be used where repeating is proven safe (CPY:576-578) | 4 |
| G-07 | Evidence preservation and honesty (§B.4) | Device save without a PAT; a null point read recorded as absent, not persisted; `harvest.py verify` agrees | Three null bodies were reported as persisted success in `tnr_results_1789124514980.json` (P-58) | 1 |
| G-08 | Live write proof through Forge (§B.4) | One user-controlled Forge job committed to `harvests/inbox` with outcome success and `harvest.py verify` exit 0 | All 7 committed Forge bundles are capture-only with `entries: []` (`evidence/harvest-evidence.json`) | 3 |
| G-09 | Gates green on `main` (§B.4) | `cd forge && npm test` at 100% on the released `main`, reported with the exact count | 292 of 293 at `main@305a28f`; the pin commit removes the marker the test requires (`A_ARCHITECTURE_MAP.md` §A.10; R-11) | 0 |
| G-10 | Retirement ruling and loader decommission (§B.4) | A `docs/RULINGS.md` entry naming dropped capabilities, the satisfying Forge release SHA and the decommission instruction | No such ruling exists; `pin_release.py` still pins both loaders (`.github/scripts/pin_release.py:13-16`) | 6 |
| **G-11** | **Research-read tier.** Every registry entry carries a persistence tier, export refuses anything above its tier, and the tier is visible before the read runs | A test asserts a local-only capture never reaches an exported bundle and that a projected capture exports exactly the declared fields; the before/after persistence statements exist (SSC:297-324) | Full persistence is allowlisted to seven point reads under 512 KiB (`forge/src/storage/captures.mjs:58-66`), enforced at parse (`forge/src/runner/manifest.mjs:131-137`); no tier concept exists. Blocked by K-06 and K-17 | 1 |
| **G-12** | **Ingress parity.** Every path a manifest can legitimately arrive by is reachable in Forge, or is recorded as deliberately dropped in the G-10 ruling | An ingress inventory test enumerates the accepted sources and asserts each one lands in the same preflight; a Studio-branch build reaches the runner only through the promotion contract | Forge lists `push/*.json` on the default branch only (`forge/src/ui/app.mjs:188-190`, `forge/src/github.mjs:28-34`); zip packs, device files and paste have no route (P-02, P-06); a Studio build ends in a text export today (`824c4d58:forge/src/studio/ui.mjs:3-4`). Blocked by K-39 for the Studio half | 3 and the Studio phase |
| **G-13** | **Parity guard green.** A Forge results bundle no longer breaks the repository's own session guard | `validate.py --parity` exits 0 on a committed Forge bundle, `session_close.py --guards` is green with a Forge bundle newest in the inbox, and `forge/test/harvest.test.mjs` carries the regression | `parity()` iterates `checks` unconditionally (`skills/building-tnr-content/scripts/validate.py:198-199`), Forge emits `checks: null` (`forge/src/ui/app.mjs:382`) and the guard runs on the lexically newest bundle (`skills/building-tnr-content/scripts/session_close.py:93-101`). R-19 | 0 |

Read across sections, each gate is the thing that lets one real workflow leave the Builder. The mapping is what makes "Builder can be retired" testable rather than rhetorical.

| Gate | Workflows it releases (`C_WORKFLOW_INVENTORY.md`) | Parity rows behind it |
|---|---|---|
| G-01 | W-09 zip push packs, and the image half of W-02 | P-06, P-07 |
| G-02, G-11 | W-05 research reads outside the registry | P-10, P-13 |
| G-03 | W-06 paged list captures, W-07 census to generator, and the Forge half of W-14 | P-11, P-12 |
| G-04, G-05 | W-03 edits and repairs, including the partial-edit shapes | P-23, P-33, P-36 |
| G-06 | W-12 retry, safe re-run and idmap hygiene | P-21, P-45, P-55 |
| G-07 | W-08 full-capture evidence and W-13 evidence preservation | P-14, P-40, P-50, P-58 |
| G-08 | W-02 and W-03 as live write paths, and W-11 recovery proven in the real browser | P-20, P-25, P-31, P-39 |
| G-12 | W-01 manifest staging and discovery, and the ingress half of W-24 | P-02, P-04, P-05, P-06 |
| G-13 | W-21 session guards, and the repository half of W-13 | none, this is a repository defect not a parity gap |
| G-09, G-10 | none directly; they are the release hygiene and the ruling that let the others be acted on | P-59, plus the drop list |

Two properties of this table matter more than its rows. It is **additive to B**: no gate id is renumbered and no gate text is rewritten here. And it is **not a schedule**: a gate passing is a fact about the code and the committed record, while the decision to act on a passed gate is K-11.

## J.2 Transition posture

The posture is deliberately conservative because the failure mode is asymmetric. Keeping the Builder installed for another month costs nothing measurable; removing it one gate too early strands the workflows in `C_WORKFLOW_INVENTORY.md` W-05, W-06, W-07, W-09 and W-12, which is R-10.

| Stage | Entry condition | What the operator does | Builder state | Fallback if Forge fails |
|---|---|---|---|---|
| 0. Today | none | Every write, zip pack, list capture and research read runs on the Builder; Forge runs capture-only jobs | installed, pinned, first choice for real work | n/a, the Builder is the working tool |
| 1. Forge writes proven | G-08, G-09, G-13 | Write manifests move to Forge one package at a time; the Builder stays the tool for anything Forge refuses | installed, pinned, unchanged | tap the same manifest on the Builder; the two tools share `tnr_bk_idmap_v1`, so ids created by one are known to the other (`forge/src/storage/compat.mjs:4-5`) |
| 2. Write path retired first | G-01 to G-07, G-11 | Forge is the only tool used for mutations; the Builder is used for research reads and list captures only | installed and pinned; "read-only" is operator discipline, not a code state, because the bundle has no mode switch | the Builder still runs a write manifest if Forge is broken; nothing was removed |
| 3. Read path retired | G-11 and G-12 measured, and the research tier actually shipped | Research and census reads move to Forge | installed but unused | the Builder is still installed and still works |
| 4. Deprecated | K-11 ruling | The operator is told the Builder is deprecated and is asked to stop using it | installed, unused, announced as deprecated | uninstall is not yet done, so the fallback is a single tap away |
| 5. Decommissioned | G-10 ruling committed | The operator uninstalls the Builder loader in ViolentMonkey and `pin_release.py` stops pinning it | uninstalled; `builder_bundle.js` archived out of the repository root | reinstall the archived loader; its `@require` is pinned to an immutable commit (`builder_loader_user.js:10`), so an installed copy does not depend on the file staying on `main` (Inferred: this relies on jsDelivr continuing to serve that path, which is an external fact this pass cannot verify) |

The ladder is drawn for one still-open option and says so: **K-11 option (b) then (a)**. A different ruling reorders it rather than invalidating it. If the director takes (a) first, stages 2 and 3 swap and the research-read gates move ahead of the write gates; if the director declines a staged retirement altogether, stages 1 to 4 collapse into the single decision at stage 5. What does not change under any option is the entry condition of each stage, because those are measurements, not preferences. As drawn: the write path goes first because it carries the mutation risk, and the read path follows only once the research tier of G-11 has landed. Stage 2 is the honest resting point until then.

**A passed gate can regress.** Gates are statements about a moment, and two of them depend on the game rather than on this repository. G-02 and G-11 rest on procedure rows transcribed from the pin, and the drift measurement for this pass found Forge's surfaces identical between the pin and the game head, which is a fact about 2026-09-12 and not a guarantee (R-05). The transition therefore treats the source-drift check as a standing gate rather than a one-time one, and stage 5 is the only irreversible step. Before it, a regression means dropping back a stage; after it, a regression means reinstalling an archived loader, which is why stage 5 waits on a ruling and not on a schedule.

**Two loaders on one origin (R-15).** Both loaders match the whole game origin (`forge_loader_user.js:6-7`, `builder_loader_user.js:5-6`), and Forge removes the Builder's two root nodes while it is mounted through a class allowlist and a mutation observer (`forge/src/ui/takeover.mjs:53,170-172`). Three requirements follow for the whole transition. The suppression stays scoped to `k-fab` and `k-pn` and is never widened to a generic selector. The suppression is never used as the deprecation mechanism, because a silently hidden Builder is indistinguishable from a broken one. And Forge's overlay must keep releasing the observer on unmount (`forge/src/ui/takeover.mjs:166-169`), so that a stage-2 operator can drop back to the Builder in the same tab.

**How the operator is informed.** There is no notification channel in either tool today; the only operator-facing release signal is the loader refresh step the release ritual already produces (`C_WORKFLOW_INVENTORY.md` W-20) and the Settings screen's own About block (`forge/src/ui/screens.mjs:325`). The transition therefore uses the channels that already exist: the release note that accompanies each pin, the Settings About block carrying the Forge version and the current stage, and, at stage 4, a one-line deprecation statement. Wording is owned by CPY and not drafted here; the reserved-term rules apply, in particular that `Retry` is not used for anything the Builder used to retry unsafely (CPY:576-578). Timing of stages 4 and 5 is K-11.

| Channel | Exists today | Used from stage | Carries | Owner of the words |
|---|---|---|---|---|
| Release note beside each pin | yes, as the operator's refresh step (W-20) | 1 | which gates this release closed, and what to keep using the Builder for | Fable, from the gate results |
| Settings About block (`forge/src/ui/screens.mjs:325`) | yes | 2 | the Forge version and the current transition stage | CPY |
| One-line deprecation statement | no, must be added | 4 | that the Builder is deprecated, and what replaces each dropped capability | CPY, timing K-11 |
| `docs/RULINGS.md` entry | yes as a mechanism, no entry exists | 5 | the ruling itself, per gate G-10 | director |

A deliberate omission: no in-tool banner is proposed inside `builder_bundle.js`. Adding one is a code change to a bundle that is otherwise frozen, on a tool that is being removed, and the repository already has a channel the operator reads every release.

**What the transition must never do.** Five anti-patterns follow from the evidence rather than from taste.

1. Never use Forge's node suppression as the deprecation mechanism. A Builder hidden by an observer is indistinguishable from a Builder that broke, and the operator loses the fallback exactly when a Forge failure made them need it (R-15).
2. Never mark a gate passed on Inferred evidence. G-01, G-07 and G-08 each have a clause that only a real device or a real live tap can settle, and those clauses are the director's and the operator's to close, not the planning owner's (`CLAUDE.md` §6).
3. Never combine the retirement commit with a release pin. The pin job rewrites both loaders in one run (`.github/scripts/pin_release.py:54-55`); a failure in the middle of a combined change leaves an unpinned loader on the device.
4. Never migrate by clearing storage. The journal is the write-ahead record of live mutations, and clearing it to avoid a migration is the one action that turns an ambiguous `SENT` into an unrecoverable one (R-09).
5. Never let the Builder's removal and the Forge feature that replaces it ship in the same release. The gate proves the replacement first; the removal is a separate, later, ruled step.

## J.3 Storage and settings migration

What is on the operator's phone today is listed in `A_ARCHITECTURE_MAP.md` §A.5. This table states what a Forge Next release may do to each store. Nothing in it is optional: R-09's failure mode is a release that cannot read an open job that holds a `SENT` item, which would strand a real live write with no reconciliation path.

| Store | Requirement | Why |
|---|---|---|
| `tnr_forge_job_v1:<jobId>` | Keep the key prefix exactly as it is even when the record version becomes 2. The prefix is a key name, the version is the `v` field, and they are independent (`forge/src/storage/journal.mjs:21-22,181`) | A renamed prefix makes every open job invisible to `listJobIds()` on a rolled-back bundle, which is silent loss rather than a refusal |
| same | Journal v2 is additive: new fields only, no removal, no renaming, no change to an existing field's meaning. The step is registered as `MIGRATIONS[1]` exactly as the code's own note describes (`forge/src/storage/journal.mjs:405-407`) | The migration chain is version-by-version and refuses a gap (`forge/src/storage/journal.mjs:414-420`) |
| same | A v1 bundle must refuse a v2 record by name and keep the raw text exportable, never rewrite it. This already holds: `migrate()` throws for a newer version (`forge/src/storage/journal.mjs:413`), `listJobs()` collects the record in `broken` with its raw text (`forge/src/storage/journal.mjs:220-228`), and every write path reads first, so a refusal cannot be followed by a clobbering write (`forge/src/storage/journal.mjs:183-184,198-206`) | This is the rollback story: reinstalling the previous pinned loader must degrade to a loud refusal plus an export, not to a lost job |
| same | A migration that throws parks the record instead of dropping it, the way corrupt shared keys are already parked under a `.corrupt` sibling (`forge/src/storage/compat.mjs:13-16`) | R-09 mitigation: never delete a v1 record on failure |
| IndexedDB `tnr_forge` | A version-3 upgrade is additive in the same sense as the v2 upgrade, which added `capture_snapshots` and left `captures` untouched (`forge/src/storage/captures.mjs:30-33`) | Snapshots are immutable evidence of a read that happened; an upgrade that rebuilds them destroys evidence |
| `tnr_bk_idmap_v1`, `tnr_bk_gh_v1` | Keep both names and both shapes through retirement. Do not fork a Forge-private copy (`forge/src/storage/compat.mjs:4-5`) | The idmap is the only cross-tool memory of `srcId` to id and is embedded verbatim in every exported bundle (`forge/src/ui/app.mjs:396`); a fork would break the stage-1 fallback and G-06 |
| `tnr_bk_gh_v1` (PAT) | No migration, no copy to a new key, no silent scope change. A wider scope is a user decision (K-15 for the admin device, K-26 for the operator device) | The stored value is a credential; `RUL-2026-09-08-001` discourages long-lived pasted credentials and the Studio seam already asks for more than contents write |
| `tnr_forge_sendlog_v1`, `tnr_forge_snap_v1:*`, `tnr_forge_lease_v1:*` | Treat as live operational state, not history. A release may read them but must tolerate their absence | They are per-job and per-tab and are dropped on completion (`A_ARCHITECTURE_MAP.md` §A.5) |
| `tnr_forge_quest_studio_draft_v1` | Branch-only today, and the Studio's own per-request durability is R-18 and K-39. If Studio records enter the journal they enter as v2 additive fields under the same rules as every other row here | One draft key per device is not a journal and must not be treated as one |

**Fixtures.** The migration test corpus is built from **real exported journals**, not hand-written objects. The export path that produces them exists today as a text blob in the journal card (`forge/src/ui/screens.mjs:320` calling `exportText()` at `forge/src/storage/journal.mjs:398-401`), so collecting fixtures is an operator action on the device, and it must happen **before** the upgrading release ships. The corpus needs at minimum one `DONE` job, one `INCOMPLETE` job, one `PAUSED` job holding an `ORPHANED` item, one job with a `SENT` item, and one deliberately broken record. Section I owns the test shape. Note the constraint that shapes this: there is no file download without a PAT today (P-50, gate G-07), so a fixture leaves the phone either through a copy and paste or through a repository commit.

| Fixture | Why the corpus needs it | What a migration bug would look like without it |
|---|---|---|
| A `DONE` job with verified items | the common record, and the one the export path produces most often | fields silently dropped from history |
| An `INCOMPLETE` job with a drift or unread item | non-terminal verification state must survive the version bump | a job that reads as finished after upgrade |
| A `PAUSED` job with an `ORPHANED` item | the orphan card is the only surface for a two-phase create that half landed | an orphan that disappears from the Jobs screen |
| A job holding a `SENT` item | the exact R-09 failure: an ambiguous live write that must stay reconcilable | a stranded write with no path back |
| A deliberately broken record | proves the parking behaviour rather than assuming it | a record deleted by the upgrade |
| A journal exported by the previous release, replayed through the previous release after the new one wrote | proves the rollback direction, not just the upgrade direction | a rollback that loses the newest jobs silently |

**Eviction is part of the migration story, not separate from it.** Forge asks for persistent storage best-effort on mount and records only what the browser answered (`forge/src/ui/app.mjs:408-409`); whether the operator's Firefox Android grants it is Inferred, and the whole journal exists because eviction happens. A version bump is a moment of elevated risk: the operator may upgrade the loader on a phone that is already under storage pressure. Two requirements follow. The migration step must be cheap enough to run on every read without rewriting every record eagerly, so an interrupted upgrade leaves a mix of v1 and v2 records rather than a half-rewritten store. And the fixture corpus above must be collected before the upgrading release, not after, because an evicted journal cannot be exported retroactively.

**Recommendation and alternatives** (planning owner's, panel synthesis unavailable at this SHA). Recommended: additive v2 under the existing key prefix with `MIGRATIONS[1]` and a refusal-plus-export rollback. Alternative (b), a new key namespace `tnr_forge_job_v2:` with dual-read, loses because a rolled-back bundle stops seeing the new namespace entirely, converting a loud refusal into silent invisibility, which is precisely R-09. Alternative (c), a sidecar store holding the new fields with the journal untouched, loses because it creates two write-ahead records for one job and the single pre-send flush is the invariant the journal exists to hold (`forge/src/storage/journal.mjs:330-335`). Section F owns what the v2 fields actually are, including any repository-sync state and any Studio per-request record.

## J.4 Manifest contract compatibility

The manifest contract does not change in this pass and should not change in the first Forge Next phases. Three requirements follow.

1. **Existing validated manifests keep working unchanged.** Every manifest in `push/` and `archive/spent-manifests/` must continue to parse and plan without edits. This is measurable with the corpus that already exists: 35 committed JSON manifests and 6 zip packs (`evidence/harvest-evidence.json`). Backward compatibility first is a brief principle (§15), and a contract migration is out of scope (§16).
2. **No second door into the runner.** Whatever ingress G-12 adds, every manifest passes the same preflight: `parseManifest`, the validator's unknown-key refusal (`forge/src/runner/validate.mjs:81`) and the lints, including the hidden-on-create rule (`forge/src/runner/lints.mjs:64-68`). A Studio-generated manifest is not privileged by having been machine-generated; the promotion contract is K-39 and the state today is an explicit refusal to enter the runner (`824c4d58:forge/src/studio/ui.mjs:3-4`), which RB's separation of compile from execution requires (RB:269-284).
3. **Ingress is enumerated, not assumed.** The current ingress is exactly one route: `.json` files listed from the push directory on the default branch (`forge/src/ui/app.mjs:188-190`, `forge/src/github.mjs:28-34`). Local `.zip` push packs (P-06), local `.json` and paste (P-02), other directories or refs (P-04) and Studio-branch builds (`A_ARCHITECTURE_MAP.md` §A.8 item 6) are each either built or recorded as dropped in the G-10 ruling. Silence is not a disposition.

The enumeration, as it stands at this SHA:

| Route | Builder today | Forge today | Gate | Disposition question |
|---|---|---|---|---|
| Repository directory pick, any directory, `.json` or `.zip` | yes, prompts for the directory and lists both extensions (`builder_bundle.js:826-831`) | push directory, `.json` only, default branch only (`forge/src/ui/app.mjs:188-190`) | G-12 | is a directory other than the push directory wanted at all (P-04) |
| Multi-select batch from that list | yes, number, list, range or all (`builder_bundle.js:833-841,859-871`) | one manifest per job (`forge/src/ui/app.mjs:209-225`) | G-12 | drop or build, no committed run proves the need (P-05) |
| Device file, `.json` or `.zip`, sniffed by magic bytes | yes (`builder_bundle.js:822`) | none | G-01 for the pack half | offline and fast iteration only (P-02) |
| Paste into a textarea | yes, the same textarea the loader fills | none, the only textarea is the read-only export | G-12 | same question as the device file (P-02) |
| Zip pack parsed in page with its `imgSizes` ledger | yes (`builder_bundle.js:496`) | none | G-01 | build, it is a hard blocker (P-06, P-07) |
| Studio-branch generated manifest | not applicable, the Studio is newer than the Builder | text export only, by design (`824c4d58:forge/src/studio/ui.mjs:3-4`) | G-12 | the promotion contract is K-39 |

A note on what this section is not claiming. That the committed corpus parses is a statement about parsing, not about running: only G-08 turns a parsed manifest into a proven live write, and the corpus contains shapes (raid columns, content-less quest edits) that Forge deliberately refuses today and that gate G-04 exists to settle.

## J.5 Results and harvest contract compatibility

The results bundle is the only artefact that leaves the phone, and four repository consumers read it. The retirement plan must not change what they receive, except to fix what is already broken.

| Consumer | What it reads | Requirement through the transition |
|---|---|---|
| `harvest.py verify` | `cfg`, `outcome`, `entries[].state`, `entries[].verdict`, `captures[].ok` (`skills/building-tnr-content/scripts/harvest.py:322-337`) | Keep Forge's fail-closed branch exactly as it is. A Forge bundle is already judged more strictly than a Builder bundle and that asymmetry is correct |
| `validate.py --parity` | `checks` (`skills/building-tnr-content/scripts/validate.py:201`) | G-13. Either Forge emits a real check inventory or parity skips `cfg: "forge"` bundles explicitly. Today Forge has no machine-readable inventory at all: its lint ids exist only inside message text (`forge/src/runner/lints.mjs:64-68`), so the honest option is real work, not a rename |
| `session_close.py --guards` | the lexically newest inbox bundle (`skills/building-tnr-content/scripts/session_close.py:93-101`) | Once G-13 passes, a Forge bundle being newest is no longer a red guard. Until then every Forge run puts pressure on the operator to produce a Builder bundle, which is a hidden retirement blocker (R-19) |
| `build_answers.py` | `captures[].data` as a list of rows (`.github/scripts/build_answers.py:76-96`) | This is the sharpest sequencing constraint in the section. No Forge bundle can feed `answers/` today, because summary captures carry no body (`forge/src/runner/runner.mjs:589`) and full persistence is limited to seven point reads (`forge/src/storage/captures.mjs:58-66`). Retiring the Builder's read path before G-03 and G-11 silently stops the catalog refresh in W-14 |

**What an honest `checks` inventory would have to be.** The validator's inventory is the union of the named checks it implements from the generated `45g` blocks and every lint rule whose surfaces include the builder (`skills/building-tnr-content/scripts/validate.py:180-192`). Forge implements a different and partly overlapping set: it refuses unknown top-level and nested keys from the pinned field sets rather than validating values (`forge/src/runner/validate.mjs:81`), and it ports some lints by id in message text only. So emitting `checks` from Forge is not a formatting change; it requires deciding which of Forge's refusals are the same check as the validator's, and the parity report would then be a true statement about two different tools. The cheaper option, skipping `cfg: "forge"` bundles in `parity()`, is honest as long as the skip is explicit and reported, and it is the option that unblocks the session guard first. Both are recorded here because G-13 is the only gate whose fix is entirely inside repository tooling and could land in phase 0 with no Forge release at all.

The same table is the reason stage 3 in §J.2 sits behind the research tier rather than beside it. `harvest.py`'s Builder branch is not deleted at retirement either: 35 committed Builder bundles remain readable evidence and the legacy semantics stay in place for them.

## J.6 Release, pin and loader mechanics of a retirement

What changes at decommission, and what never does, is mechanical and small. `pin_release.py` iterates a two-entry `TARGETS` tuple and rewrites one `@require` per loader to a jsDelivr URL pinned to the release commit, strips the pending markers and stamps the Forge version from `forge/package.json` (`.github/scripts/pin_release.py:13-16,21-29,31-41`).

| Step | What it touches | Ordering constraint |
|---|---|---|
| 1. G-10 ruling committed | `docs/RULINGS.md` | Must name the Forge release SHA that satisfied G-01 to G-09 and G-11 to G-13, and list every dropped capability |
| 2. `TARGETS` drops the Builder pair | `.github/scripts/pin_release.py:13-16` | Must happen **in the same commit as or before** the Builder loader leaves the repository root. `pin(...)` reads the loader file first (`.github/scripts/pin_release.py:20-22`), and the Builder entry is iterated first, so a missing loader with a stale `TARGETS` fails the pin job before Forge is pinned at all |
| 3. Builder artefacts archived | `builder_bundle.js`, `builder_loader_user.js` | Archive, do not delete: the fallback in §J.2 stage 5 depends on the loader text still existing somewhere reachable |
| 4. Operator uninstalls the loader | the device | User-owned. The Builder loader carries no `@updateURL` or `@downloadURL` (`builder_loader_user.js:1-11`), so it can never be retired remotely and never auto-updates itself away |
| 5. Release note and Settings About | release ritual, `forge/src/ui/screens.mjs:325` | The operator refetches the Forge loader as usual (W-20) |

**Rolling back a Forge release.** The rollback of a Forge Next release is not part of the Builder retirement, but it is the fallback that makes each stage safe, so it is stated once. The operator edits the installed loader's `@require` back to the previously pinned commit, or reinstalls the previous loader text; nothing on the repository side is reverted, because the pin lives in the loader (`forge_loader_user.js:12`). The previous bundle then meets whatever the newer one wrote: a v2 journal record is refused by name and stays exportable (§J.3), an additive IndexedDB upgrade leaves the older stores intact, and the retained `tnr_bk_*` keys are unchanged by design. That is the whole reason §J.3's requirements are phrased as readable-or-refused rather than as a one-way migration.

What never changes: pinning is by immutable commit SHA and not by a moving ref, which is the difference from the Builder's runtime contract fetch (`A_ARCHITECTURE_MAP.md` §A.8 item 1); the loader refresh stays a user action on the device; and no part of retirement touches the game, since the Builder's removal is a userscript change and nothing else (`CLAUDE.md` §6).

The bundle itself is not special-cased by any of this. Forge ships as one built bundle checked by the existing release tooling, and the retirement changes what the release pins, never how it is built or verified.

One coupling to carry into phase 0: the release-loader test is red on `main` after every pin (`A_ARCHITECTURE_MAP.md` §A.10, R-11), and G-09 requires it green. The fix exists on the ChatGPT branch and integrating it is a one-writer question, not a Fable edit (RM-05).

## J.7 What is not retired

Retiring the Builder's write path does not retire these. Each line names the capability, what still holds it, and the gate that would release it.

- **Research reads outside the audited registry.** P-10 and P-13. Held by the Builder until G-02 and G-11 both pass and K-17 has named the procedures and K-06 the tier. Last real use was 2026-09-12 on Builder v4.32 (`evidence/harvest-evidence.json`).
- **Paged and filtered list captures, and capture bodies for every read.** P-11 and P-12. Held until G-03. The census-to-generator loop in W-07 and the catalog refresh in W-14 both depend on them.
- **Zip push packs and the byte ledger.** P-06 and P-07. Held until G-01. Every image-bearing package in the record shipped as a pack.
- **Multi-manifest batch builds.** P-05, which is a GAP but not a blocker because no committed bundle proves a batch run. This is a candidate for deliberate drop in the G-10 ruling rather than a build target; the adversarial re-read of P-05 also found that a batched file which wrote nothing is still reported as a tick, so reproducing the behaviour faithfully would reproduce a defect.
- **Paste and device-file manifest input.** P-02, conditional. The rulings that make the repository the owner of durable artefacts point away from a device-file ingress, so this is a G-10 disposition question, not an automatic gap to fill.
- **Retry, safe re-run and idmap hygiene.** P-45, P-21 and P-55, held until G-06. Note that "retry" here means the Builder's rebuild of error rows; Forge's replacement is a re-drive that is journalled as a new phase attempt and never as a second create, and the word itself is reserved (CPY:576-578).
- **Builder-only conveniences with no committed use.** The repository directory prompt (P-04), the loader HEAD self-check (P-16) and the on-demand doctor diagnostics (`A_ARCHITECTURE_MAP.md` §A.8 item 9) are GAP rows with no retirement-blocker status. They are listed in the G-10 ruling as deliberate drops or as small follow-ons, and they never gate a stage.
- **Everything Forge is not supposed to absorb.** The repository-side workflows in `C_WORKFLOW_INVENTORY.md` §C.6 are not part of this migration in either direction.

## J.8 Open decisions

Routed to `K_USER_DECISIONS.md` by id, with no recommendation restated here.

- Timing and staging of deprecation and removal, including when stages 4 and 5 of §J.2 happen: **K-11**.
- The persistence tier that gate G-11 depends on: **K-06**; the procedures gate G-02 and G-11 may add: **K-17**.
- The promotion contract that gate G-12's Studio half depends on: **K-39**.
- Credential scope on the two devices, which the transition inherits rather than settles: **K-15** and **K-26**.
- Whether placeholders and orphans may ever be deleted, which bounds what G-06 recovery may offer: **K-16**.
- Source-pin refresh before implementation and whether the shipped bundle is minified, both of which change what a release and its rollback look like: **K-13** and **K-14**.
- Every gate in §J.1 is measurable by Fable, but the decision to act on a passed gate is the director's; the ruling that records it is gate G-10 and its content is **K-11**.
