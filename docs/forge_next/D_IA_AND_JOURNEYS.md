# D. Information architecture and user journeys

**Status:** PLANNING, no implementation. No live game request, no credential material, no game-source change. Part of the Forge Next planning package; context, pins, evidence tiers and method are in `00_CONTEXT.md`.
**Base:** `main@305a28f992e33194fbba279a3f32e698dfb2b67f`. Every `forge/src` line cite is taken at that tree. Files that exist only on `chatgpt/forge-quest-studio-foundation@824c4d58` carry the prefix `824c4d58:`.
**Companion:** the visual system is `D_VISUAL_SYSTEM.md` (tokens D2.2, components D2.3, state and motion D2.4, departures D2.5). This section does not restate a token or a construction; it names D2.3 components and says where they go.

Abbreviations, each `docs/design/<file>` at `chatgpt/forge-quest-studio-foundation@824c4d58`, cited as `ABBR:line`: SSC = FORGE_NEXT_SAFETY_STATE_PRESENTATION_CONTRACT.md, MOB = FORGE_NEXT_MOBILE_ACCESSIBILITY_AUDIT.md, WCM = FORGE_NEXT_WORKFLOW_COMPONENT_MAP.md, WFA = FORGE_NEXT_WIREFRAME_ANATOMY.md, SCN = FORGE_NEXT_UX_SCENARIO_MATRIX.md, IRM = FORGE_NEXT_INTERACTION_RISK_MATRIX.md, QS = FORGE_NEXT_QUEST_STUDIO.md, RB = FORGE_NEXT_REPO_BACKED_STUDIO_ARCHITECTURE.md, MS = FORGE_NEXT_MISSION_STUDIO.md, WSP = FORGE_NEXT_CONTENT_PROJECT_WORKSPACE.md, BRF = `state/prompt_forge_next_planning_resume_after_ui_recovery.md`.

## D.0 Scope, method and what stays open

This section answers brief §13-D and the brief's §6, §7, §8 and §11 IA questions. It recommends one information architecture for phone and desktop, keeps the alternatives, maps every element of the approved concept mockup to a disposition, inventories the screens, and writes the journeys including Content Admin, Quest Studio and the Project Workspace. It settles nothing the user owns.

**Method, and the panel status.** The design panel produced two completed independent IA proposals and was stopped before a third and before a judged synthesis: `scratchpad/design/ia-operation.json` (operation-oriented destinations) and `scratchpad/design/ia-content-type.json` (content-type-oriented destinations). Both were read in full. **Panel synthesis unavailable at this SHA; the recommendation below is the planning owner's, built by comparing two independent proposals against the evidence rather than by a judged panel.** The comparison inputs were those two proposals, `C_WORKFLOW_INVENTORY.md` (frequency and risk mix), `MOB` (phone ergonomics), `B_PARITY_MATRIX.md` and `E_CONTENT_ADMIN_FEASIBILITY.md` (what is actually backed), and the Forge code at `main@305a28f`. Both proposals' weakness lists are reproduced in D.1 rather than summarised away.

**Rule for every journey in D.4.** Each journey lists its WCM workflow id, the WFA anatomy section for its screens, the SCN scenarios it covers, and a HOLD status where the capability is unproven. A journey step that depends on a capability the game or Forge does not have is marked HOLD or needs-capability-first and is never written as a phase deliverable (WCM:607-629, components that must not invent capability).

**What is open, and stays open.** Navigation labels, the exact destination lists, the operation-mode taxonomy and colours, and the content-lane taxonomy are director decisions: K-20 (and K-20a for the phone shell), K-21, K-22, K-24, with K-33 as the sub-decision on derived versus selectable mode. All are marked pending predecessor-transcript reconciliation (BRF:57-73). The words used below are the recommendation's defaults and match the committed wireframes so that a reviewer sees one vocabulary, not two. No wireframe and no table here freezes a nav label, a mode colour or a lane name (WFA:564).

## D.1 Recommended information architecture

### D.1.1 The model

**Operation-first destinations, content lanes as the second axis.** The first level is the consequence the operator is about to have on production. Content type is a filter and an entry point, not a destination that owns work.

The decisive evidence is derivability plus the read/write mix. Forge already derives the consequence class from the parsed plan: `const readOnly = s.plan.length === 0` (`forge/src/ui/screens.mjs:120`), and `runner.mjs:160` computes capture-only from the same shape. A content-type axis cannot be derived for a package that carries two entity types, and no axis at all resolves cleanly for the packages that carry reads and writes together: `C_WORKFLOW_INVENTORY.md` C.4 records 21 capture-only manifests against 23 manifests carrying captures alongside writes, and one zip pack mixing eight asset creates with ten quest edits.

### D.1.2 Desktop rail destinations

Eight rows in four visual groups on a 232 px rail (`D_VISUAL_SYSTEM.md` D2.3 NavRail [WCM AppShell navigation, WCM:34]). Every row's feed is state Forge already holds, so opening a destination costs zero game budget.

| Destination (default label) | Purpose | Who | Risk class | What feeds it without a live poll |
|---|---|---|---|---|
| Command Center | Can Forge act; what is unfinished or ambiguous; what waits for review; the shortest path to today's task | both | read | `journal.resumable()` and `listJobs()` (`storage/journal.mjs:360-366`, `:221-228`), `jobOutcome` (`journal.mjs:76-88`), `AuthState.describe()` (`transport/auth.mjs:219`), `Budget.status()` (`budget/bucket.mjs:204-216`), the GitHub listing cache (`ui/app.mjs:196-207`) |
| Capture & Research | Zero-mutation packages, the capture library, and (after K-17) a bounded ad-hoc read | operator | read | picker entries whose parsed plan is empty (`screens.mjs:120`); capture cache and snapshots (`storage/captures.mjs:58-66`) |
| Build & Update | Packages that can change the game: discover, preflight, run, verify, sync | operator | mutation | picker entries with at least one plan item; manifest summaries from the listing cache (`app.mjs:186-192`) |
| Quest Studio | Authoring with zero live footprint: one Studio, subtype adapters, repository compile | operator | config | local draft plus build state (`824c4d58:forge/src/studio/ui.mjs:378-390`); subtype registry (`824c4d58:skills/building-tnr-content/data/49_DATA_quest_studio_subtypes.json`) |
| Content Admin | Record-level review, edit, preview, publish for a holder of a content role | admin | publish | a repository-backed review record read through the same listing path; the record itself only on open. HOLD, see D.4.6 |
| Jobs & Recovery | Every job this device knows about, its decisions and its results | both | recovery | `journal.listJobs()` including `journal.broken` (`journal.mjs:221-228`) |
| Projects | Read-only projection of `state/workstreams/<slug>/roadmap.json` | both | config | repository read; `REVIEW` is already a task status (`scripts/content_workstream.py:54-63`) |
| Settings | Keep the tool correct on this device; diagnostics as a second view | both | config | `readGh` (`app.mjs:400`), `AuthState`, `Budget.status()`, storage persistence (`app.mjs:408-411`) |

### D.1.3 Phone navigation

Five bottom items plus a More sheet, matching MOB's durable direction of large labelled icons and a compact five-item primary set (MOB:355-360).

| Slot | Item | Maps to | Badge |
|---|---|---|---|
| 1 | Home | Command Center | orphan count when `journal.ambiguous()` is non-empty |
| 2 | Work | Build & Update | SENT dot, PAUSED dot |
| 3 | Capture | Capture & Research | none |
| 4 | Jobs | Jobs & Recovery | orphan count, INCOMPLETE dot |
| 5 | More | MoreSurface sheet: Quest Studio, Content Admin, Projects, Captures library, Settings, Diagnostics, Export journal | gold-outline pending count on the Content Admin row |

MOB records that the destinations, whether Admin belongs in the primary phone set, badge treatment and the behaviour of More are all still unresolved (MOB:361-367). K-20a owns them. Two variants are offered rather than one: (i) Admin promoted into slot 4 when the role read succeeds, pushing Jobs into More; (ii) Quest Studio promoted into slot 3 once the promotion contract exists (K-39). Neither is recommended before the transcript reconciliation lands.

### D.1.4 Why this model, from C's mix and the phone

1. **Frequency and risk point in opposite directions, which is exactly what an operation axis expresses.** C.4 class 1 (research and evidence) is the most frequent workload and carries no mutation risk; class 9 (admin review and publish) is the rarest and the most consequential. Operation-first gives the frequent action the shallowest path and no confirmation, and gives publishing its own destination, colour family and confirmation.
2. **The classification is already computed and already trusted.** `screens.mjs:120` and `runner.mjs:160` derive read-only from the parsed plan today. An IA that mirrors a computed fact cannot drift from it.
3. **The Builder-only shapes cluster on one side.** C.4.1 ranks the shapes that keep Builder installed: generator-fed capture bodies (P-12), zip packs (P-06), paged or filtered list captures (P-11), procedures outside the registry (P-10), `select` projection (P-13). Four of those five are reads. One destination can carry one honest capability statement for them instead of repeating "not supported yet" in seven content lanes.
4. **Recovery is a phase of a job, not a place, and today's split is a catalogued defect.** The orphan decision renders on the Jobs screen (`screens.mjs:29-31`, `:55-70`) while the pause that produced it renders on the Run screen (`screens.mjs:216-220`). The recommendation keeps a Jobs & Recovery destination for history and cross-screen visibility, but puts the decision inline on the job that owns it (D.3 BU-3).
5. **Phone ergonomics.** Operation-first fits five bottom items with no hub indirection: the two dominant journeys (open a package, capture from live) are one tap from Home. A seven-lane content-first model cannot be five tabs and needs a hub, which its own author records as a weakness.

### D.1.5 Alternative (b): content-type-oriented destinations, and why it lost

The proposal is one destination per content class (Quests, AI, Assets, Jutsu, Items, Bloodlines, Guides-placeholder) with the cross-class objects (Packages, Jobs & Recovery, Projects) staying cross-class, phone nav Home / Content / Jobs / More, and Admin's queue grouped by the same classes.

Its case is real and is recorded here rather than paraphrased away. Every committed write and capture is keyed by class; capability, publish gate, preview path and history support differ per class, so a class-first shell can state truthfully what Forge can do for each class; the game's own staff surface is class-first; and an operator usually knows the class before the operation.

It lost on four counts.

| Reason it lost | Evidence |
|---|---|
| Cross-class packages have no home. A lane's package list is a filtered view that depends on parsing cached manifest text, which today lives under the game read cache path `github.contents` (`app.mjs:196-207`; the design smell is recorded at `A_ARCHITECTURE_MAP.md:139`) | the proposal's own weakness list |
| The model's most natural screen carries the largest capability debt. A per-lane Records list needs a paged, filtered live list; `CachedReader.list` refuses anything but name paths (`forge/src/budget/reader.mjs:73-86`), which is P-11 GAP and a retirement blocker | `B_PARITY_MATRIX.md` P-11; gate G-03 |
| Rail breadth. Thirteen desktop destinations against the K-20 advisory of seven or fewer, and seven lanes cannot be five phone tabs, so lanes sit behind a Content hub | the proposal's DEP-3 and DEP-4 |
| Two lanes have no committed work (Items, Bloodlines) and one is a placeholder pending K-13, K-17 and K-29 (Guides). Honest, but it ships empty rooms | C.4 class counts; `E_CONTENT_ADMIN_FEASIBILITY.md` CA-08 |

The recommendation keeps its best ideas: lanes survive as the second axis with real tints and glyphs (`D_VISUAL_SYSTEM.md` D2.3 LaneCard [WCM ContentLaneCard, WCM:52-54]), the per-class capability card becomes the honest "what Forge can do for this class" block on the lane landing (wireframe `wf02_lane_quests`), and the admin queue groups by class.

### D.1.6 Alternative (c): the two-axis model, not elaborated

The brief names a third option: goal at the first level, content type at the second (or the reverse). No proposal elaborated it and no judge scored it. It is recorded as an option, not a recommendation, with the shape it would take and the cost it would carry.

- Shape: the first level stays the six-to-eight operation destinations; the second level inside Capture & Research, Build & Update and Content Admin becomes a persistent lane selector rather than a filter chip, so a lane choice survives navigation.
- What it would buy: lane-first browsing as a primary path rather than a Command Center entry, which is the recommendation's weakest point and the content-type proposal's strongest.
- What it would cost: two selectors to keep in sync on a 390 px phone, and a second place where a mixed-entity package has no correct answer.
- Status: not elaborated at this SHA. If the director wants lane-first browsing to be primary, this family should be elaborated before the shell phase rather than approximated by promoting lanes inside the recommended model.

## D.2 Mockup element reconciliation

Every block, lane, destination and quick action of the approved concept, with its disposition and the evidence. `D_VISUAL_SYSTEM.md` D2.5 owns the visual departures; this table owns the structural ones. The amendment's own §12 marks labels, destinations, lane names, colours and geometry as illustrative, so a rename here is not a character change.

| Mockup element | Disposition | Maps to | Evidence |
|---|---|---|---|
| Dashboard | keep, rename open | Command Center (HM-1) | every block has a local source (D.1.2); K-20 owns the word |
| Create Content | regroup | Quest Studio (ST-1, ST-2) | only the quest family has an authoring path; the subtype registry marks one subtype supported (`824c4d58:forge/src/studio/ui.mjs:234-246`); RUL-2026-09-12-001; R-16 |
| Capture | keep, rename Capture & Research | CR-1 to CR-5 | P-09 and P-14 are Forge strengths; the rename covers the ad-hoc reads the destination must eventually hold (P-10, P-11, P-12) |
| Edit & Write | regroup, no operator destination | AD-3 (admin record edit) and BU-2 (an edit package) | Forge has no operator-facing record editor; every committed quest edit was a manifest (C.4 class 2); R-16 |
| Validate | drop as a destination | ValidationSummary on BU-2, PreflightSummary on CR-2, build result on ST-3 | validation is per package (P-32, P-35) and canonical validation runs in the repository (RUL-2026-09-12-002); balance is user-owned (`CLAUDE.md` §10) |
| Manifest & Deploy | rename and regroup | Build & Update (BU-1 to BU-3) | P-03, P-17, P-39, P-41 to P-43 all live here; "Deploy" is dropped so that running a hidden package is never read as making content player-visible |
| Content Admin | keep, first class | AD-1 to AD-7, HOLD | brief §8; `E_CONTENT_ADMIN_FEASIBILITY.md` E.1 headline: the loop is composed of procedures that already exist, for the seven Forge classes plus guide and badge |
| Library | regroup into two | CR-4 Captures library (evidence on this device) and AD-6 Content library (live records) | different authorities over different things; AD-6 additionally needs paged list support (`budget/reader.mjs:73-86`; P-11, gate G-03) |
| Reports | needs-capability-first | JR-1 plus the Command Center activity list; repository reporting stays in the repository | no reporting source exists in Forge; `answers/` and catalogs are repository workflows (C.6); R-16, R-19 |
| Settings | keep, split | SE-1 Settings, SE-2 Diagnostics | today one screen mixes a credential form with raw diagnostics (`screens.mjs:216-220` region and the settings screen); F-19 and F-15 both live there |
| Quick action: New Content (Skill, Item, Enemy, Event) | rename and narrow | "New quest" to ST-1 | only the quest family has an authoring path; RUL-2026-09-12-001 |
| Quick action: Capture from Live | keep | CR-1, and CR-3 after K-17 | the most frequent real action (C.4 class 1) |
| Quick action: Validate Content (rules, balance, format) | drop | none | no standalone target; balance is reserved (`CLAUDE.md` §10); R-16 |
| Quick action: Create Manifest (package for deployment) | needs-capability-first | ST-3 to ST-4, disabled with the reason | the Studio ends in a text export today (`824c4d58:forge/src/studio/ui.mjs:469-480`); K-39 |
| Quick action: Resume work | add | HM-1 ActiveWorkCard primary | `journal.resumable()` (`journal.mjs:360-366`) is the one quick-action source that exists today |
| Quick action: Review pending content | add when the role read succeeds | AD-1 | HOLD until K-03 and the queue store (K-09) |
| Lane: COMBAT (Skills, Enemies, AI, Encounters) | keep, rename candidate | filter over the `jutsu`, `ai` and `aiProfile` recipes (`forge/src/runner/recipes.mjs:11-20`) | K-24 open |
| Lane: ITEMS (Gear, Consumables, Materials) | keep | filter over the `item` recipe (`recipes.mjs:11-20`) | CA-02 zero-game-change; K-24 open |
| Lane: QUESTS & EVENTS | keep, hosts Quest Studio | filter over the `quest` recipe plus the Studio entry | C.4 class 2 makes quest edits the dominant write; RUL-2026-09-12-001 |
| Lane: LOCATIONS (Zones, Maps, Travel) | drop or replace | replacement candidate "Scenes & Assets" over the `gameAsset` recipe | no Forge capability for zones or travel; the backed neighbour is CA-04 gameAsset, where every committed asset create went; R-16 |
| Lane: CHARACTERS (NPCs, Factions, Dialogues) | regroup into Combat | the `ai` recipe | the only character record Forge touches is a `userData` row with `isAi` (CA-06); R-16 |
| Lane: SYSTEMS (Mechanics, Configuration) | drop | none | runtime configuration with no Forge path (CA-25), and balance knobs are excluded by ownership; R-16 |
| Lane: Guides (added) | needs-capability-first placeholder | labelled lane placeholder | CA-08 says the loop is feasible with zero game change, but the class is post-pin and needs a pin move plus registry rows (K-13, K-17, K-29) |
| Home: welcome hero with painted art | keep the block, change the material | CSS atmosphere plus a small inline vector | `D_VISUAL_SYSTEM.md` D2.5 item 3; K-31 |
| Home: System Status with green "Operational" rows | keep the block, change the claims | ReadinessCard with four lamps from held state | D2.5 item 5; a health domain renders only when its source exists (D2.3.5); R-16, R-03 |
| Home: Recent Activity with free coloured dots | keep, change the dots | ActivityRow with the real job or record pill | D2.5 item 6 |

## D.3 Screen inventory

Screen ids use a two-letter destination prefix: `HM` Command Center, `CR` Capture and Research, `BU` Build and Update, `ST` Quest Studio, `AD` Content Admin, `JR` Jobs and Recovery, `PR` Projects, `SE` Settings. They are this section's own namespace and do not collide with the matrix ids used elsewhere in the package (`P-`, `CA-`, `CC-`, `W-`, `R-`, `K-`, `G-`).

Screen ids are introduced by this section. The wireframe column points at `docs/forge_next/wireframes/<id>.html` (phone 390 and desktop 1280 in one page). Component names are `D_VISUAL_SYSTEM.md` D2.3, with the WCM equivalent in brackets on first use.

| Id | Name | Purpose | Key content | Primary actions | Risk badge | Phone | Desktop | Wireframe | D2.3 components |
|---|---|---|---|---|---|---|---|---|---|
| SH0 | Entry splash | Arm the tab, hand off to a real game route, explain a dead end | destination sentence, hop count, dead-end guidance | Open the game and sign in; Try again | read | single column, 52ch | centred 520 px | none | Brand/Wordmark |
| SH1 | AppShell | One frame: identity, session truth, navigation, and a static statement that a mutation, publish or recovery is in flight | session lamp, Close, Back, top-bar underline | navigate; Close; Re-check session | read | 56 px top bar, BottomNav 56 px plus safe area | 232 px rail | every page | AppShell [WCM AppShell, WCM:32-34], NavRail, BottomNav, MoreSurface |
| SH2 | More surface | Hold secondary destinations without hiding that they exist | 56 px rows; Content Admin rendered as a labelled placeholder when the role read fails | open a destination; Close | read | dialog sheet | not rendered | none | MoreSurface |
| SH3 | ConfirmationSurface | Arm one consequential action: restate counts, name records, show the flip in words | counts, record names with their current pill, session lamp, one primary plus Cancel | Start live write / Publish / Adopt / Re-send / Run N full captures | mutation | docked bottom sheet | centred 480 px | `wf13_publish_confirm` | ConfirmationSurface [WCM ConsequenceConfirmation, WCM:76-78] |
| HM-1 | Command Center | Is anything ambiguous, what is unfinished, can Forge act, where do I start | orphan card first when present, active work, quick actions, lanes, readiness, activity | the job's own primary; Adopt or Skip; quick actions; open a lane | read | attention first, hero shrinks to a strip | hero, 2/3 and 1/3 columns, lanes full width | `wf01_command_center` | ReadinessCard [WCM SystemHealth, WCM:40-42], ActiveWorkCard, QuickActionTile [WCM ActionCard, WCM:48-50], LaneCard, ActivityRow, StatePill |
| HM-2 | Lane landing | One workflow class in one place, with an honest capability statement | capability card, records from committed captures and catalogs, packages touching the class, Studio entry | open a record; open a package; open the Studio; Refresh from live (explicit) | read | stacked sections | two pane | `wf02_lane_quests` | LaneCard, StatePill, WorkPackagePicker |
| CR-1 | Research home | Get to a read fast | zero-mutation packages, capture library entry, ad-hoc read entry disabled with its reason | open a package; Refresh; open library | read | tap replaces the list with the detail | 380 px list plus detail | `wf03_manifest_discover` (picker anatomy) | WorkPackagePicker [WCM, WCM:56-58], Banner |
| CR-2 | Read package preflight | State the consequence before the tap | READ ONLY band with counts, capture rows marked FULL or SUMMARY, the repository-persistence sentence, validation | Run N reads, zero mutations | read | sticky band, one primary in a sticky bar | band at the top of the content column | `wf09_capture_preflight` | ModeBand [WCM OperationHeader, WCM:44-46], PreflightSummary, CaptureRow [WCM CapturePersistence, WCM:100-102], ValidationSummary |
| CR-3 | Ad-hoc read | One bounded read without a manifest | procedure chooser limited to the registry, inputs, budget preview, scope sentence | Read (disabled, with the reason); Save to library | read | full-screen form | chooser plus result | none (HOLD) | ActionButton (disabled with reason), BudgetMeter |
| CR-4 | Captures library | Two stores, two consequences | read cache and immutable snapshots with distinct wording and confirmation strength | invalidate one; clear cache; delete snapshot | read | two headed sections | two columns | `wf10_captures_library` | MaintenanceAction [WCM, WCM:124-126], CaptureRow |
| CR-5 | Capture evidence | Prove what was read | procedure path, the input actually sent, scope sentence, bytes, two separate verdicts, raw body behind a disclosure | Copy key; Delete snapshot | read | disclosure, never miniaturisation | right inspector | none | EvidencePanel [WCM, WCM:88-90], CaptureRow |
| BU-1 | Packages | Work that can change the game, with the last outcome told honestly | rows with entity mix, counts, image count, outcome-coloured last-run tag | open; Refresh; Search | mutation | 56 px rows | list plus detail | `wf03_manifest_discover` | WorkPackagePicker, StatePill, Banner |
| BU-2 | Package preflight | Everything the operator must know before a live write | LIVE WRITE band with counts, blockers versus advisories, image slots, plan rows, manifest hash, raw disclosure | Start job, writes N records; pick an image | mutation | band sticky, plan rows wrap | summary left, plan and validation right | `wf04_preflight_live_write` | ModeBand, PreflightSummary [WCM, WCM:60-62], ValidationSummary [WCM, WCM:68-70], DependencyInput [WCM, WCM:72-74], OperationCounts [WCM, WCM:64-66] |
| BU-3 | Job detail (run and recovery) | One screen for a job's whole life, including the decision it waits on | progress, count line, item rows, budget, halt card, orphan card inline under the paused item | Reconcile and resume; Resume; Re-read unverified; Pause after this item; Adopt / Skip / Re-send | recovery | decision where the pause is, actions in separated regions | progress left, evidence inspector right | `wf05_run_live`, `wf06_halt_sent`, `wf07_orphan_decision` | SegmentedProgress [WCM JobProgress, WCM:80-82], ItemRow [WCM ItemProgress, WCM:84-86], RecoveryCard [WCM RecoveryDecision, WCM:96-98], BudgetMeter, Banner |
| JR-1 | Jobs | Every job this device knows about, including the ones it can no longer read | active, paused, ambiguous, finished; damaged journal records with a raw export | open a job; Export journal; Delete finished jobs | recovery | grouped list | list plus detail | `wf16_jobs_settings` | StatePill, MaintenanceAction |
| JR-2 | Results | The truthful statement of one job, and whether the evidence left the device | result summary line per question, a separate sync lamp, a persistent export card | Sync to repository; Copy bundle; Open evidence | read | export is a state of the screen | summary left, bundle right | `wf08_results_sync` | ResultSummary [WCM, WCM:104-106], StatusTile, Banner |
| JR-3 | Item evidence | The expert view of one item in one place | ids, procedure path, journal record, diff rows, asserted keys, capture key, budget | Copy id; Copy payload | read | own route | right inspector | none | EvidencePanel, DiffView [WCM, WCM:116-118] |
| ST-1 | Studio home | One Studio, one subtype chooser; maturity stated, never implied | subtype cards with maturity, open drafts, last build result | New quest (enabled only where the adapter is ready); open a draft | config | cards stack, reasons stay as captions | card grid plus recent drafts | `wf14_quest_studio` | QuickActionTile, StatePill (neutral maturity tag) |
| ST-2 | Quest draft | Author in human language over one Quest Source | brief, storyboard, encounters, assets, decisions; advisory checks labelled advisory | Save draft; Compile | config | one step per screen, graph as a focused pan and zoom view | steps, editor, build panel | `wf14_quest_studio` | Banner/Callout, DiffView (revision diff) |
| ST-3 | Compile and build result | Show the canonical verdict and never invent one | submitted revision, status, blockers as decision cards, errors, generated manifest path | Compile; Refresh build status; open a decision card | config | status first, blockers next | result panel beside the editor | `wf14_quest_studio` | Banner/Callout, StatePill |
| ST-4 | Promotion handoff | The seam between authoring and execution, closed until it is ruled | generated manifest path, a disabled promote control with its reason, the current copy-and-commit fallback | Copy manifest; Send to Build & Update (disabled) | config | one card | same card | `wf14_quest_studio` | ActionButton (disabled with reason) |
| PR-1 | Projects | One row per workstream, projected, never stored twice | title, status, task counts, blocked count, open-decision count, provenance line | open a project; Refresh | config | rows | rows plus summary | `wf15_project_workspace` | StatePill, StatusTile |
| PR-2 | Project workspace | What do I do next and why is it blocked | readiness strip, needs attention, work plan, open decisions, evidence, review package | open a task brief; Resume here; Open evidence; edit (disabled until K-28) | config | attention first | header, attention column, decisions column | `wf15_project_workspace` | Banner/Callout, StatePill, ActionButton (disabled with reason) |
| AD-1 | Review queue | What waits for a human decision, in content terms | queue entries, each record's content pill, class filter, explicit Refresh with its cost | open an entry; Refresh; Filter | publish | 56 px rows, human title first | queue plus detail | `wf11_admin_queue` | AdminReviewCard [WCM, WCM:112-114] (HOLD), StatePill |
| AD-2 | Record detail | What this record is, what changed, whether it is safe to publish | human change summary, grouped fields, the lifecycle field in words, the unhide-gate result, dependencies, freshness line | Edit; Preview; Publish; History | publish | one column, sticky actions | detail left, preview right | `wf12_admin_detail` | AdminReviewCard, DiffView, StatePill |
| AD-3 | Record edit | Change permitted fields through real controls | per-class form over the fetched whole record, pending diff, the whole-record write warning, a staleness re-read before send | Save changes; Cancel | mutation | one field per row | form left, diff right | `wf12_admin_detail` | DiffView, ConfirmationSurface |
| AD-4 | Preview | Show what a player would see where a renderer honestly exists | class renderer, or a neutral "no player renderer for this class" state | Re-read; Back | read | frame fills the width | frame in the right column | `wf12_admin_detail` | PreviewFrame [WCM Preview, WCM:623-625] |
| AD-5 | Publish | Make the flip unmistakable, permission aware and provable | PUBLISH band, the flip in words, gate result, role and session, dependency warnings | Publish 1 record; Cancel | publish | docked sheet, armed confirm | centred sheet | `wf13_publish_confirm` | PublishControl [WCM, WCM:120-122] (HOLD), ModeBand, ConfirmationSurface |
| AD-6 | Content library | Browse live records by class and visibility | paged list per class, a visibility filter, the honest disclosure about hidden reads | open a record; Load more; Filter | read | rows, explicit paging | list plus detail | none (needs G-03) | WorkPackagePicker pattern, StatePill |
| AD-7 | Record history | Who changed what, with the limits of the native trail stated | native log entries where the class is covered, Forge captures where it is not, a provenance line | open a capture; Back | read | chronological rows | rows plus diff panel | none | DiffView, ActivityRow |
| SE-1 | Settings | Say where every secret goes and refuse a configuration that cannot work | credential as a status line, sync that refuses to be on without a credential, role readiness, storage, version and pin | Save; Forget credential; Re-check session | config | grouped rows | two columns | `wf16_jobs_settings` | StatusTile/HealthRow, MaintenanceAction |
| SE-2 | Diagnostics | Everything the tool knows about itself, in one place | auth describe as rows, budget per path, journal export, damaged records, storage keys, the request log | Export journal; Copy diagnostics; Clear read cache | config | grouped rows | two columns | `wf16_jobs_settings` | HealthRow, BudgetMeter, EvidencePanel |

### D.3.1 Wireframe set and its coverage

The minimum wireframe set is the required scenario list at SCN:467-480, cross-checked with the priority phone cases at MOB:391-402 and with the provisional-structure list at WFA:552-562. Sixteen pages are committed under `docs/forge_next/wireframes/`, each showing phone 390 and desktop 1280 in one page. Each answers the seven questions every consequential wireframe must answer in visible order (WFA:14-20) and demonstrates the component states a style prototype must include (WFA:538-548). None freezes a nav label, a mode colour or a lane name (WFA:564).

| Required scenario (SCN:467-480) | Wireframe | Screen id |
|---|---|---|
| S-01 healthy command center | `wf01_command_center` | HM-1 |
| S-02 auth blocked | `wf01_command_center` (readiness lamp states) | HM-1 |
| S-08 full capture preflight | `wf09_capture_preflight` | CR-2 |
| S-09 live-write preflight | `wf04_preflight_live_write` | BU-2 |
| S-13 running work | `wf05_run_live` | BU-3 |
| S-18 ambiguous SENT recovery | `wf06_halt_sent` | BU-3 |
| S-22 orphan resolution | `wf07_orphan_decision` | BU-3 |
| S-27 verification unread | `wf08_results_sync` (result summary states) | JR-2 |
| S-28 verification drift | `wf08_results_sync`, with the diff in `wf12_admin_detail` | JR-2, JR-3 |
| S-34 read succeeded, body not persisted | `wf09_capture_preflight`, `wf10_captures_library` | CR-2, CR-4 |
| S-39 live verified, repository sync failed | `wf08_results_sync` | JR-2 |
| S-51 publish confirmation (provisional) | `wf13_publish_confirm` | AD-5 |
| S-52 publish not verified (provisional) | `wf13_publish_confirm` | AD-5 |
| S-59 mobile warning plus sticky action | every phone column; the chrome stack rule is D2.3.3 | BU-2, CR-2 |

Four further pages cover surfaces the required list does not name because they did not exist when it was written: `wf02_lane_quests` (the lane landing that carries the second axis), `wf14_quest_studio`, `wf15_project_workspace` and `wf16_jobs_settings`. `wf03_manifest_discover` covers the discovery anatomy (WFA:102) that S-05 and S-06 exercise.

## D.4 Journeys

Every journey names its WCM workflow, the WFA anatomy sections that govern its screens, the SCN scenarios it covers, and its HOLD status. Tap counts are from the phone layout and exclude the repository session that authored the manifest.

### D.4.1 Dashboard and home

WCM Workflow A (WCM:128). WFA §2 global shell (WFA:24) and §3 Command Center (WFA:43). SCN S-01, S-02 (SCN:467-468). No HOLD.

| n | Screen | Action | What is shown | What is fail-closed |
|---|---|---|---|---|
| 1 | SH0 | open Forge from the bookmark | the destination sentence and the hop count | a dead end is explained with the next action, not a stack trace (`forge/src/main.mjs:75-80`, `:155-166`) |
| 2 | HM-1 | (automatic) render | orphan card if `journal.ambiguous()` is non-empty, then active work, quick actions, lanes, readiness, activity | no lamp is green by default and a domain with no wired source renders "not checked" (D2.3.5); no block issues a live request |
| 3 | HM-1 | tap the job's own primary | the label carries the semantics: Reconcile and resume, Resume, or Re-read unverified items | the control is disabled with its reason, never hidden, when the session is not ready or the budget is tripped (`budget/bucket.mjs:204-216`; D2.3.4) |

Phone taps to value: 0. The screen answers the first question above the fold.

### D.4.2 Manifest discover, preflight, run, verify, sync

WCM Workflows B, C, F, G, H, I, N (WCM:161, :199, :279, :313, :335, :354, :450). WFA §4 discovery (WFA:102), §5 preflight (WFA:130), §7 live-write run (WFA:221), §8 verification incomplete (WFA:268), §11 result summary (WFA:355). SCN S-09, S-13, S-27, S-28, S-39, S-59. No HOLD; three steps are needs-capability-first and are marked below.

Phone taps from Home to an armed live write: 4 (Work, package row, Start job, armed Confirm).

The brief's thirteen steps (§7), each marked against `main@305a28f`. The evidence column is the owner; `C_WORKFLOW_INVENTORY.md` C.5 holds the full per-step evidence and is not restated.

| Step | Screen | Status | Cite |
|---|---|---|---|
| 1 discover from repo, workstream, `push/` | BU-1, CR-1 | partial | listing is `push/` on `main` only (`ui/app.mjs:186-192`); no workstream-aware discovery |
| 2 drag, drop, paste, import | BU-1 | new | P-02 GAP; no local input path in `forge/src` |
| 3 parse and classify automatically | BU-1, BU-2 | exists | P-17; the picker summary is computed on listing (`app.mjs:196-207`) |
| 4 title, provenance, content types, entity count, operations | BU-2 | partial | `screens.mjs:84-90` renders title, number and a summary; operation counts are the OperationCounts component, not built |
| 5 validation blockers and advisories | BU-2 | exists, keys only | pre-send unknown-key refusal (`runner/validate.mjs:81`); P-33 GAP for enum and bound checks |
| 6 captures, reads, writes, uploads distinct | BU-2, CR-2 | partial | capture-only banner (`screens.mjs:118-122`); image slots (`screens.mjs:144-148`); no per-operation breakdown |
| 7 live-state diff and preflight where safe | BU-2 | partial | fetch-merge validates inside the run; no pre-run diff (P-40) |
| 8 zero-mutation versus mutation-capable stated | CR-2, BU-2 | exists | `screens.mjs:120`; `runner/runner.mjs:160` |
| 9 explicit operator action to run | SH3 | exists, to be replaced | `window.confirm` today (`ui/app.mjs:172-175`); D.5 replaces it |
| 10 live per-item and per-phase progress | BU-3 | partial | item rows and pause banners exist (`screens.mjs:216-220`); the request log is collected and never rendered (P-57) |
| 11 safe pause, resume, reconcile | BU-3 | exists, unproven live | `runner.mjs:187-193` refuses to run a job holding SENT; `resume()` reconciles first (`runner.mjs:242`); gate G-08 |
| 12 read-back and result summary | JR-2 | exists, two defects | asserted-key read-back (`runner/validate.mjs:217-225`); null body counted as success (P-58, gate G-07) |
| 13 sync, export, archive with no copy and paste | JR-2 | partial | commit path (`app.mjs:400-406`); no download without a credential (P-50); the export card is prepended and destroyed by the next refresh (`app.mjs:180-184` with `ui/dom.mjs:27`) |

Fail-closed points that must survive the redesign: `SENT` is flushed to the journal before the request leaves (`storage/journal.mjs:330-336`); `SENT` has no transition back to `PLANNED` (`journal.mjs:39-47`); the verdict comes from the decoded application outcome, not HTTP (`transport/outcome.mjs:36-42`); a job with SENT items cannot be run, only resumed (`runner.mjs:187-193`); `DONE` carries a separate outcome lamp because `jobOutcome` can be `unverified` while the pill says done (`journal.mjs:76-88`, against today's `styles.mjs:44`).

### D.4.3 Research and capture, including FULL persistence

WCM Workflows D and E (WCM:232, :253). WFA §6 read-only capture (WFA:187), §15 evidence panel (WFA:465). SCN S-08, S-34, and the capture and evidence scenarios at SCN §9. No HOLD for summary reads; the ad-hoc read (CR-3) is needs-capability-first.

Phone taps: 3 for a summary read (Capture, package row, Run). 4 for a full capture, because the fourth is the armed confirmation.

| n | Screen | Action | What is shown | What is fail-closed |
|---|---|---|---|---|
| 1 | CR-1 | tap Capture | zero-mutation packages, the library, the ad-hoc entry disabled with "needs registry expansion" | the disabled control keeps its reason as a caption, so the operator learns why Builder is still installed (P-10, P-11, P-12) |
| 2 | CR-2 | open a package | READ ONLY band; each capture path marked FULL or SUMMARY | a full-capture package renders the persistence advisory naming the paths; a summary package does not (`storage/captures.mjs:58-66` is the allowlist) |
| 3 | CR-2 | Run | summary: runs immediately; full: ConfirmationSurface restating that bodies reach a public repository | confirmation is spent where it buys evidence (D.5); IRM classes R2 for a summary read and R3 for a full capture (IRM:170-201) |
| 4 | BU-3 style run view | watch | per capture, two separate verdicts: read ok or failed, and body persisted or not, with the persist error | a successful read never stands in for a persisted body; a null point read must be a distinct absent verdict (P-58, gate G-07) |
| 5 | CR-4, CR-5 | open the library | read cache and immutable snapshots as two stores with different wording and confirmation strength | snapshot deletion says the body can only return from another read; the GitHub listing cache stops living under the game read cache (`app.mjs:196-207`) |

### D.4.4 Recovery: SENT reconciliation, orphan decision, INCOMPLETE re-read

WCM Workflows J, K, I, L, M (WCM:373, :392, :354, :413, :432). WFA §9 ambiguous SENT (WFA:299), §10 orphan decision (WFA:326), §8 verification incomplete (WFA:268). SCN S-18, S-22, S-27. IRM class RX, which exists because the risk comes from uncertainty rather than from the action's normal side effect (IRM:150-160). No HOLD.

Phone taps to a decision: 3 (Open from the Home orphan card, Adopt on a candidate row, armed Confirm).

| n | Screen | Action | What is shown | What is fail-closed |
|---|---|---|---|---|
| 1 | HM-1 | open Forge; the orphan card is pinned above active work | what is uncertain, whether a request may have left, what reconciliation found, that an ordinary retry is unsafe, the recommended next safe action | nothing is preselected and no control is labelled Retry (D2.3.2, D2.3.6) |
| 2 | BU-3 | tap Open | the job with a RECOVERY band, the halt card naming the pause reason, and the orphan card inline under the paused item | this repairs today's split, where the decision renders on Jobs (`screens.mjs:29-31`, `:55-70`) and the pause renders on Run (`screens.mjs:216-220`) |
| 3 | BU-3 | tap Adopt on a candidate row | candidate rows with the name first and the id in mono, copyable | today the id renders above the name (`screens.mjs:55-57`); the order is reversed. Adopt, Skip and Re-send sit in separate regions |
| 4 | SH3 then BU-3 | confirm, then Reconcile and resume | the item moves ORPHANED to CONFIRMED; the job resumes at the next phase | `SENT` to `PLANNED` does not exist (`journal.mjs:39-47`); `run()` refuses a job holding SENT and `resume()` reconciles first (`runner.mjs:187-193`, `:242`); a job with SENT items cannot be deleted (`journal.mjs:277-283`) |

INCOMPLETE re-read is the same screen with a different primary: "Re-read unverified items" is a read-only continuation, so it does not confirm (D.5).

### D.4.5 Content Admin: queue, detail, edit, preview, publish

WCM Workflows Q and R (WCM:506, :539). WFA §13 admin queue, which is explicitly a capability placeholder (WFA:421), and §14 publish confirmation, which is explicitly provisional (WFA:448). SCN S-47, S-49, S-51, S-52 (the last two provisional per SCN:478-479).

**HOLD.** Every step of this journey is a placeholder until `E_CONTENT_ADMIN_FEASIBILITY.md` is ruled on and K-03, K-04, K-05, K-07, K-08 and K-09 are answered. Forge has no publish or unhide action at all today (`A_ARCHITECTURE_MAP.md:171`; the PublishControl row is HOLD at `A_ARCHITECTURE_MAP.md:257`), and no approval field exists in the game, so AdminReviewCard must not invent an approval state with no durable backing store (WCM:607-629). The wireframes render the controls as visible placeholders (WFA:550-562).

Phone taps once the capability exists: 4 for review and publish with no edit; 7 with an edit.

| n | Screen | Action | What is shown | Status |
|---|---|---|---|---|
| 1 | AD-1 | tap Content Admin | queue entries in content terms with each record's content pill | HOLD on the queue store (K-09) and the role read (K-52); the destination renders as a labelled placeholder when the role read does not succeed |
| 2 | AD-2 | tap a record | human change summary, grouped fields, the lifecycle field named in words, the unhide-gate result, dependencies, a freshness line | partial: the per-class lifecycle facts are source-verified in E; the summary source differs per class because native history does not cover every class |
| 3 | AD-4 | tap Preview (optional) | the class renderer, or a neutral "no player renderer exists for this class" state | HOLD per class (K-05); Preview must not claim fidelity the game does not have (WCM:607-629) |
| 4 | AD-3 | tap Edit (optional) | a per-class form over the fetched whole record, with the pending diff | HOLD on K-04 and K-08; the write is whole-record, so a staleness re-read immediately before send is mandatory |
| 5 | AD-3, SH3 | Save changes, then confirm | the write is journaled as a single-item job and inherits SENT, CONFIRMED and read-back | the admin sees a record result, never the job vocabulary; the journal below the seam is unchanged |
| 6 | AD-5 | tap Publish | PUBLISH band, the flip in words, the gate result, the session lamp and the role | HOLD: no publish recipe exists (`A_ARCHITECTURE_MAP.md:171`); the control is disabled with its reason when the role or the gate is unmet |
| 7 | SH3, AD-2 | confirm | the content pill stays HIDDEN and shows SENT until the read-back returns | the pill flips only on a verified read-back, never on HTTP success (`transport/outcome.mjs:36-42`) |

### D.4.6 Quest Studio compile loop

WCM has no workflow row for authoring; the loop is C.2 W-24 and is governed by QS and RB. WFA §5 preflight anatomy applies only after promotion, not to the compile. SCN has no authoring scenarios at this SHA. RUL-2026-09-12-001 (one Quest Studio, subtype adapters) and RUL-2026-09-12-002 (the repository compiles) are the owners.

**Planning only.** The seam is ChatGPT-owned at `824c4d58` and is not a frozen review target here. Nothing in this journey is re-planned or patched on the Fable branch.

Tier A shell surfaces, per QS §4 (QS:84-131): Overview and brief, Storyboard, Semantic flow, Encounter layer, Scene and assets layer, Policy, eligibility and rewards, Research and reuse, Preview, Compile and build, Review and package. The subtype changes the policy and the recipe, not the application (QS:133). Which surfaces ship in which slice is QS-5 and stays open.

Tier A phone model, per QS §13 (QS:398-412): Brief, Storyboard, focused node editor, Choices and Route controls, Encounter cards, Decisions, Assets, Preview, Compile status. The full graph may open as a focused pan and zoom view, but precise drag wiring is never the only way to edit routes. Compilation continues remotely while the UI shows "Building", and the Studio refreshes when the report lands. Layouts stay open (QS-13).

Mission-subtype detail, Tier B under that Tier A shell, per MS §3.2 (MS:94-104): Author fields are ordinary editable controls; Profile fields are read-only inherited values with a source label; Fixed fields are read-only policy; Generated fields are status and preview only; Null-by-design fields are suppressed but inspectable; `AWAITING_RULING` is a blocking decision card and never a plausible default. The policy view labels each value's source in the same words the document uses: "From C-rank mission profile", "Fixed by hidden-first doctrine", "Generated from art shot list", "Awaiting director ruling" (MS:303-306). The construction of the decision card should reuse the D2.3 Banner/Callout warn construction, and the inverted ORPHANED emphasis only if the director accepts that reuse. Open, not settled here.

**State vocabulary.** The Studio's sync and build states are the RB §11 list, used verbatim: `Draft saved locally`; `Repository revision saved`; `Build requested`; `Building`; `Build result received`; `Repository unavailable / retry save`; `Build failed`; `Build blocked by design decision` (RB:269-278). These sit on SSC axis F, the publication and content lifecycle axis (SSC:99-105), never on axis B, the execution lifecycle (SSC:34-40), because a Studio build never touches the game. RM-06 records the same separation for the roadmap.

Phone taps from Home to a requested build, once the draft exists: 4 (More, Quest Studio, open the draft, Compile).

**Implementation gap, recorded as a fact and not settled here.** At `824c4d58` the shell renders five states: no build, busy ("Building in the repository..."), error ("Repository request failed"), waiting ("Build still running") and result (`824c4d58:forge/src/studio/ui.mjs:378-390`). `Repository revision saved`, `Build requested` and `Repository unavailable / retry save` are not distinct. "Repository request failed" is a GitHub-only, retry-safe class, and it is the one place a "Try again" control is allowed in the Studio, because nothing was sent to the game (D2.3.6).

| n | Screen | Action | What is shown | Status |
|---|---|---|---|---|
| 1 | ST-1 | choose a subtype | cards from the registry with maturity stated; only the ready adapter is enabled (`824c4d58:forge/src/studio/ui.mjs:234-246`) | exists at 824c4d58 |
| 2 | ST-2 | author, then Save draft | brief and storyboard over one Quest Source; advisory checks labelled advisory | exists, narrow; R-20 records the browser-versus-canonical drift risk |
| 3 | ST-2 | Compile | the source is saved to a request branch and a build is requested (`824c4d58:forge/src/studio/repository.mjs:73-90`) | exists at 824c4d58; the trigger and credential scope are K-26 |
| 4 | ST-3 | read the verdict | valid, blocked or failed; a blocked build renders a decision card naming the reserved decision, never a default | exists; the classification is prose-coupled (R-21) and is presented as "the compiler reported a decision is missing" |
| 5 | ST-3 | decide, then recompile | the decision card, then a new revision and a new build | open: how a decision resolves into the source is QS-5 and K-49 |
| 6 | ST-4 | promote | the generated manifest path and a disabled promote control with its reason | HOLD. Today's end state is a text export of the generated manifest (`824c4d58:forge/src/studio/ui.mjs:469-480`); K-39 owns the promotion contract |
| 7 | BU-2 | the same preflight | the promoted package enters the ordinary LIVE WRITE preflight with no separate path | HOLD until step 6; this is the point of the loop, so that a Studio build is never a second execution path |

Fail-closed in this journey: a compile is not an execution and never touches the game, so no Studio state may borrow the execution vocabulary; a build whose result file never lands is rendered as an explicit unknown rather than as a slow queue or a failure (K-38); a blocked verdict renders the reserved decision and never a plausible default (MS:94-104); and the promotion control stays disabled with its reason rather than hidden, so the operator sees the seam instead of guessing at it.

### D.4.7 Project workspace projection

W-25 in C.2. WSP is the proposal owner. WFA has no anatomy section for it; the readiness strip and needs-attention block reuse WFA §12 system-health anatomy (WFA:395). No SCN scenarios exist at this SHA.

| n | Screen | Action | What is shown | Status |
|---|---|---|---|---|
| 1 | PR-1 | open Projects | one row per `state/workstreams/<slug>` with task counts and a provenance line naming the commit read | new; the projection is read-only |
| 2 | PR-2 | open a project | readiness strip, needs attention (blocked tasks, unresolved decisions, missing evidence), work plan, open decisions, evidence, review package | new |
| 3 | PR-2 | act | open a task brief, resume, open evidence; any write back to `roadmap.json` is disabled with its reason | HOLD on K-28. `REVIEW` already exists as a task status (`scripts/content_workstream.py:54-63`), so the review handoff is the first candidate for a narrow validated write |

Phone taps to the next action on a project: 3 (More, Projects, project row). Fail-closed: the projection carries a provenance line naming the commit it was read at, so a stale projection cannot pass as current coordination state; every write control is disabled with its reason; and an unresolved decision is rendered as a decision card, never as a default value.

Validation and rendering stay in `scripts/content_workstream.py` (C.6). Forge projects this state and does not become a second store of it (RUL-2026-09-12-002).

## D.5 Confirmation model

The owner of which action gets a confirmation is IRM: the classes R0 to R6 plus RX (IRM:35-168) and the 28-row action matrix (IRM:172-201). This section does not restate them. `D_VISUAL_SYSTEM.md` D2.3 ConfirmationSurface is the construction; the IRM matrix decides which actions get it. The meaning of every state word is SSC (SSC:107-415) and the construction of each state is D2.2 and D2.4.

Four consequences follow for this IA.

1. **Reads never confirm.** A summary capture run is IRM class R2 with a concise preflight and no modal (IRM:174-201). Today Forge confirms it, which is the single largest avoidable tap in the most frequent workflow.
2. **One confirmation per job, with the counts restated.** A live-write package is IRM class R4: one armed ConfirmationSurface for N items, not N dialogs. The per-item safety is the journal, not the dialog (`journal.mjs:330-336`).
3. **Publishing is IRM class R5** and its confirmation level is K-12, which is open. The wording half of K-12 is pending predecessor-transcript reconciliation. The IA reserves the surface and does not choose the level.
4. **Recovery is RX, not a generic modal.** Reconcile, Adopt, Skip and a safe later-phase re-send each get a dedicated recovery presentation that states what is known, what is uncertain, what will be read or sent next, why the offered action is safe, and what remains if the user skips (IRM:150-168).

`ConfirmationSurface` replaces `window.confirm` for live write, publish and re-send. Today `App.confirm` is `globalThis.confirm` (`ui/app.mjs:172-175`) and it is the only consequence surface in the product. Local destructive maintenance (clear read cache, delete a snapshot, delete finished jobs, forget the credential) keeps the native dialog until the sheet covers it, and each of those controls keeps its own sentence rather than sharing one generic danger style with "Skip (leave as is)" (`screens.mjs:68-70`).

## D.6 Operation-mode header

The mode band is a 44 px full-width strip rendered before any item list, the same height in every mode so content never jumps. Construction is `D_VISUAL_SYSTEM.md` D2.3 ModeBand [WCM OperationHeader, WCM:44-46] with the count chips [WCM OperationCounts, WCM:64-66].

**Derived, never selected.** The mode comes from the parsed plan, the journal or the action in flight. READ ONLY when the parsed plan has zero write items, which is how Forge already decides (`screens.mjs:120`). LIVE WRITE when the plan has at least one create or update. RECOVERY when the job is paused or incomplete or holds any SENT or ORPHANED item. PUBLISH only on an admin publish action, which is HOLD. A mode selector reads as a permission and must not imply that choosing Publish grants it (WCM:607-629). K-33 is the director's, and a selectable mode remains an option for them.

**Counts vocabulary.** Reads, captures (with the FULL subset named separately), creates, updates, uploads, publishes. Sources: capture entries for reads and captures, plan item ops for creates and updates, image refs for uploads. Publishes has no source today and is rendered as zero or omitted, never fabricated (`A_ARCHITECTURE_MAP.md:171`). Deletes is never rendered: no delete recipe has a caller and no authorized delete workflow exists (IRM's matrix marks a live-record delete as not currently authorized, IRM:201). During a run the counts are recomputed from the journal rather than the plan, so a resumed job shows what is left.

**Placement.** Phone: 44 px sticky under the 56 px top bar, the mode word plus the two most consequential counts for that mode, with a chevron that expands the rest; a readiness blocker line replaces the counts when the session is not ready. Desktop: 44 px at the top of the content column, never over the rail, with the full chip row visible.

**Absence is a signal.** Settings, Diagnostics, the captures library, the Studio draft and the admin queue render no band, so the presence of a band means the screen can touch, or has touched, production.

**Review.** Whether Review is a fifth mode or a workflow state is K-21 and is open. The recommendation renders Review as a workflow state on admin rows and does not add a fifth band, pending that ruling.

## D.7 Authority lanes

One product, two authorities. Content Operations acts on packages and jobs. Content Admin acts on records. They share the runner, the journal and every safety invariant, and they share nothing in their vocabulary.

**Structural distinction.** Content Admin is its own destination with its own second level. No admin screen is reachable from a Build & Update screen and no Build & Update screen is reachable from an admin screen except through the rail or the bottom nav. The admin lane renders no manifest text, no procedure path, no journal state, no item pill, no budget row, no capture key and no orphan card. Those live only under Build & Update, Capture & Research and Jobs & Recovery.

**Visual distinction.** Pill families are disjoint and that is the primary cue: the admin lane uses only the content pills (HIDDEN, DRAFT, PUBLISHED, plus SENT while a publish is in flight); the operator lane uses the job and item pills from the journal vocabulary (`journal.mjs:39-47`). Gold is the admin and publish family and appears in the operator lane only as the PUBLISHED content pill. Crimson is the operator live-write family and appears nowhere in the admin lane, so an admin never sees a LIVE WRITE band. Construction and exact tokens are D2.2 and D2.4.

**How a job result becomes a review item.** The operator runs a package; hidden records are created or updated; the journal records the entity id, the manifest path and the manifest hash per item; the results bundle is committed (`app.mjs:400-406`). Forge then writes a repository-backed review handoff naming the package, the records by id and class, and who staged them. The admin queue reads that repository state through the same GitHub listing path that feeds the picker, costing no game budget, and resolves an entry to its live record only when the entry is opened. The disposition is written back to the same repository record, so the operator sees it in the project workspace and on the package's last-run tag. Nothing about approval is claimed to be live game state, and no second canonical content database is created: the game owns the records, the repository owns the review state, Forge owns neither (RUL-2026-09-12-002). The exact store and shape are K-09 and K-47 and are not settled here.

## D.8 Risk visibility

SSC owns the meaning of every state and the hierarchy of certainty (SSC:107-415). `D_VISUAL_SYSTEM.md` D2.3 and D2.4 own the construction. This section states only where each SSC axis is shown in this IA.

| SSC axis | Where it is shown in this IA |
|---|---|
| A, operation capability | the ModeBand on every actionable screen, and the derived mode chip on every package row so a package never changes meaning when it moves between Capture & Research and Build & Update |
| B, execution lifecycle | ItemRow pills and SegmentedProgress on BU-3; the count line above them; the ActiveWorkCard on HM-1; never in the admin lane |
| C, verification and evidence | the separate outcome lamp beside DONE on JR-1 and JR-2; the two separate capture verdicts on CR-2 and CR-5; DiffView on JR-3 |
| D, authorization and session | the global session lamp in the AppShell, with a denial rendered per action rather than as a session state, pending K-34 |
| E, supporting systems | ReadinessCard and HealthRow on HM-1 and SE-1; BudgetMeter on BU-3, hoisted into the pause card when the budget is tripped (D2.3.4) |
| F, publication and content lifecycle | content pills in the admin lane, and the Studio's compile and build states, which sit here and never on axis B (SSC:99-105; RM-06) |

Two IA-level rules follow. A toast is never the sole carrier of SENT, an auth refusal, INCOMPLETE, an orphan or a persistence failure; it echoes a durable banner (R-25). And an outcome colour never carries a non-outcome meaning, so the picker's green "ran" tag and the image picked and missing tags stop borrowing the VERIFIED and FAILED pill classes (`screens.mjs:84-90`, `:144-148`, with `styles.mjs:44`).

## D.9 Progressive disclosure

| What | Where it lives | Note |
|---|---|---|
| Raw manifest | BU-2, behind a "Raw" disclosure | there is no raw manifest view at all today; the only raw JSON the operator sees is the export card (`app.mjs:180-184`) |
| Journal record | JR-3, behind "Journal record"; whole-journal text export in SE-2 | damaged records get a row on JR-1 with a raw export, because `journal.broken` is collected and never rendered (`journal.mjs:221-228`) |
| Procedure paths and budget | BU-3, in a Technical group on phone and a right inspector on desktop | `Budget.status()` per path (`bucket.mjs:204-216`) |
| Payloads and diffs | DiffView is the default presentation; raw JSON sits behind a "Raw" disclosure inside it | today drift renders as stringified pairs (`screens.mjs:249-253`), which is how a bad write has to be understood |
| Capture bodies | CR-5, behind a disclosure, never auto-expanded | |
| Admin lane | no disclosure into manifests, journals or procedures; the deepest disclosure is the record's raw field list and its native history | an operator who also holds the role reaches those through Build & Update |
| Studio | the Quest Source behind a disclosure on ST-2; the build envelope behind a disclosure on ST-3; compiler and worker revisions always visible as provenance | |

The rule is progressive disclosure, never miniaturisation: consequence copy does not drop below the type floor and ids wrap in their own mono region rather than being sliced, against today's 120-character slice of plan keys (`screens.mjs:136-140`).

## D.10 Mapping from the current five screens, and what an existing user relearns

| Today | Becomes | Why |
|---|---|---|
| Jobs (`screens.mjs:26-33`) | HM-1 attention blocks, JR-1 full list, BU-3 for the decision | the screen mixes a dashboard, a history list and a recovery decision; the decision moves beside the pause that requires it |
| Manifests (`screens.mjs:84-90`) | CR-1 for zero-mutation packages, BU-1 for write-capable ones, BU-2 as its own route | one list mixes both consequences today with no visible difference, and the selected card is appended below the whole list |
| Run (`screens.mjs:216-220` region) | BU-3 with recovery inline, JR-2 as a durable results screen | the auto-opened bundle card is destroyed by the post-run refresh (`app.mjs:180-184`, `dom.mjs:27`) |
| Captures (capture screen) | CR-4 library, CR-5 evidence | the two stores keep their distinct wording; the GitHub listing cache stops being listed as a game capture (`app.mjs:196-207`) |
| Settings (settings screen) | SE-1 Settings, SE-2 Diagnostics | a credential form and raw diagnostics currently share one screen |
| (none) | Quest Studio, Projects, Content Admin, SH3 | the Studio exists only at `824c4d58`; Projects and Content Admin do not exist |

What an existing user relearns, in order of surprise:

1. The landing screen is the Command Center, not Jobs. Nothing redirects: a resumable job badges the destination and pins a card on Home.
2. The single manifest list splits by derived consequence, so a package can move between Capture & Research and Build & Update when its plan changes. One search covers both and every row shows its mode chip.
3. The green "ran" tag becomes outcome-coloured and says which run and when.
4. DONE stops being green on its own and carries a separate outcome lamp.
5. Summary-only capture runs stop confirming.
6. Five horizontally scrolling text tabs become five bottom items plus More, and nav and Close targets rise to the touch floor.
7. Builder stays installed and pinned throughout, and every capability that is still Builder-only renders as a disabled control naming its gate.

Nothing in the journal, the transition table, the reconciler, the budget or the transport changes during the shell migration, and storage keys are unchanged.

## D.11 Departures from the approved direction

Consolidated with `D_VISUAL_SYSTEM.md` D2.5, which owns the visual departures. These are the structural ones this section adds. Each names the smallest correction and the evidence.

| Id | Departure | Smallest correction | Evidence | Character change |
|---|---|---|---|---|
| D-IA-1 | "Create Content", "Edit & Write" and "Validate" do not become operator destinations | the authoring door is Quest Studio; record editing exists only in the admin lane; validation is a step of a package | R-16; C.4 class 2 (every committed edit was a manifest); CA-01 to CA-08 | no |
| D-IA-2 | Three lanes are replaced and one is added as a placeholder | Locations becomes Scenes & Assets; Characters folds into Combat; Systems is dropped; Guides is a labelled placeholder | R-16; CA-04, CA-06, CA-08, CA-25; `recipes.mjs:11-20` | no; K-24 owns the final set |
| D-IA-3 | Recovery is not a separate decision surface from the job that produced it | Jobs & Recovery stays a destination for history and badges; the decision renders inline on BU-3 | `screens.mjs:29-31`, `:55-70` against `screens.mjs:216-220` | no |
| D-IA-4 | The Content Admin lane carries no mode band while reading; a PUBLISH band appears only on the publish surface and while a publish is in flight | as stated | the amendment asks for a persistent operation context on actionable flows; the admin surface is overwhelmingly a reading surface | **yes**, surfaced for the director under K-21 and K-30 |
| D-IA-5 | On a 390 px phone the Command Center orders attention above the hero, the quick actions and the lanes | reorder, and shrink the hero to a strip | MOB:393 (Command Center with one active resumable job and one system blocker is the first priority phone case) | no; a reorder, flagged because it changes what the director saw |
| D-IA-6 | Quest Studio and Projects sit under More on the phone rather than in the primary five | as stated, with a promotion variant offered | authoring has zero live footprint and ends in a copy-and-commit today (`824c4d58:forge/src/studio/ui.mjs:469-480`); K-39 | no; K-20a owns it |
| D-IA-7 | "Preview Content, see exactly how it looks" is scoped per class and must not promise a render for every class | per-class renderer or a neutral "no player renderer exists for this class" state | CA-04, CA-05, CA-08; Preview must not claim fidelity (WCM:607-629) | no |
| D-IA-8 | Reports is dropped or rendered as a labelled placeholder for v1 | run history is JR-1 and the Command Center activity list; content reporting stays a repository workflow | R-16; C.6 | no |

## D.12 Open decisions routed to K

Listed by id only. Items marked pending follow BRF:57-73.

- K-02 top-level navigation model. This section recommends option (a) with lanes as the second axis; (b) and (c) are kept in D.1.5 and D.1.6.
- K-20 and K-20a exact destination lists, labels and the phone shell (pending predecessor-transcript reconciliation).
- K-21 operation-mode taxonomy, including whether Review is a mode; D-IA-4 needs an answer either way (pending).
- K-22 exact mode colours and tokens (pending).
- K-23 typography scale (pending).
- K-24 content-lane taxonomy (pending).
- K-33 mode derived versus selectable; recommended derived (pending).
- K-01 final visual style and degree of polish.
- K-03, K-04 Content Admin permission scope and whether the admin may execute arbitrary writes.
- K-05 which classes get first-class forms and previews in v1.
- K-06 capture data classification, which bounds CR-2 and CR-3.
- K-07 which operations are eligible for few-tap publish.
- K-08 staged package versus direct hidden-record edit, which decides whether the admin lane gains a package concept.
- K-09 and K-47 where approval state and review annotations live.
- K-12 publishing UX and confirmation level (wording half pending).
- K-16 deletion policy; no delete count is rendered in the mode band and no delete control is offered.
- K-17 research-read registry expansion; CR-3 stays disabled until it is ruled.
- K-11 Builder deprecation timing; the IA assumes Builder stays installed.
- K-15 credential model, widened by the Studio's needs (K-26).
- K-28 how much repository-backed project state Forge may edit; PR-2 is read-only until ruled.
- K-30 late Content Admin and publish visual details (pending).
- K-31 background and lane art in v1.
- K-34 whether a role-denial signal exists; without it no authorization lamp is rendered.
- K-35 whether ABORTED gets a producer or leaves the vocabulary.
- K-39 promotion gate; ST-4 is a disabled control until ruled.
- K-42 flagship end-to-end workflow.
- K-46 graph editing depth in Studio v1.
- K-49 policy override workflow, which the ST-3 decision card depends on.
- K-52 how the admin surface learns the signed-in account's role.
- K-53 whether balance-bearing classes appear in a Content Admin surface at all.
- K-54 whether the product says plainly that hidden does not mean secret.
