# Forge Next planning package

**Status:** PLANNING PACKAGE. No implementation was performed, no live game request was made, no credential or session material was used or requested, no game source was executed, and no doctrine, engine law, source pin, manifest contract or published content changed. Director decisions are open and nothing in this package settles one.

**Base:** `main@305a28f992e33194fbba279a3f32e698dfb2b67f`. **Planning branch:** `claude/forge-next-planning-v3frzi` (a stated deviation from the `fable/*` prefix in `docs/DEVELOPMENT_WORKFLOW.md` §3, recorded in `docs/forge_next/00_CONTEXT.md`). **Lane:** A, planning and discovery only. **Planning owner:** Fable / Claude Code. **Independent reviewer:** ChatGPT.

This file is the entry point. It is a map of the package, not a summary of it. Every claim below is carried in full, with citations, by the section it names.

---

## 1. What Forge Next is, and why this pass happened

Forge Next is the proposed next generation of Forge: **one content-operations workspace for TNR** that can replace the Builder for all normal content work and that adds a Content Admin experience for human review, edit, preview and publish. The planning contract states the goal as ten properties, of which the load-bearing ones are full Builder parity so the Builder can be retired rather than maintained in parallel, a manifest that behaves like a job package rather than a JSON file, first-class capture workflows, a Content Admin who does not have to read manifests or relay through the operator, mobile-first usability on the real userscript workflow, and less operator friction without weaker mutation safety.

The contract is `state/prompt_forge_next_planning.md` at `chatgpt/forge-next-planning@70c151616f09c6ec729cb05afb30faa2c6331183`. It forbids implementation in this pass.

Two amendments arrived mid-pass and were read as new planning inputs on the existing branch. Neither branch was merged, rebased onto, or modified.

| Amendment | SHA | What it added |
|---|---|---|
| Approved visual north star | `chatgpt/forge-next-planning@0bb5a54b1025ba49ff6b09aa9606f23102f4dca3` | The director-approved dark TNR operations console: product character, persistent shell, Command Center, content lanes, first-class Content Admin, explicit operation contexts. Its §12 separates what is binding from what is illustrative. |
| Consolidated design lane and director rulings | `chatgpt/forge-quest-studio-foundation@824c4d58075d0265c717ef25c02485614f3096cf` | `RUL-2026-09-12-001` (one shared Quest Studio with subtype adapters; Mission is a subtype, not a parent product) and `RUL-2026-09-12-002` (Forge is the translation, orchestration and presentation layer; the repository owns durable facts and contracts), ten architecture-neutral UI contracts, the Tier B product proposals, and a ChatGPT-owned Quest Studio foundation slice. |

The predecessor UI conversation's transcript reconciliation had not landed at `824c4d58`. Every style-board difference therefore stays a labelled director question rather than a later ruling.

---

## 2. What was found

**The current architecture, in a paragraph.** Forge 0.4.0 is 27 implementation modules under `forge/src` plus two derived JSON contracts, composed once in `compose()`. Everything below `ui/` is already UI-independent and injectable: the write-ahead journal in `localStorage`, the capture cache and immutable capture snapshots in IndexedDB, the tRPC transport with a 43-row audited procedure registry that throws on anything unknown, the per-path rate budget that halts instead of retrying, the manifest parser and pre-send validator, the runner and the reconciler. The leak runs the other way: `forge/src/ui/app.mjs` owns roughly 250 lines of domain logic (harvest mapping, capture materialisation, export, the auth-blocking preview, the confirm policy) that a second shell or a native host would have to duplicate. That is section A's central finding, and it is what decides the architecture recommendation. The Builder v4.32 is one 105 KB bundle with no tests, no journal, retry as its recovery model, and contracts fetched at load from a moving ref.

**Parity headline (section B).** Sixty-one capability rows: Forge is the safer tool on 24, matches the Builder on 8, differs deliberately on 6, and has no path at all on 23. Eight of those gaps are hard retirement blockers and nine are conditional. The pattern is worth stating once: the blockers are not exotic features. They are how a package and its images arrive (zip push packs and the byte ledger), how research is read (procedures outside the audited registry, paged list reads with an input, exported bodies), and what happens when a run goes wrong (retrying a failed step, re-running a finished manifest without duplicating creates). Forge was built to make writes safe; the Builder is still the only tool that can read broadly and repair. Thirteen objective gates, `G-01` to `G-13`, turn each blocker into something measurable.

**Content Admin headline (section E).** For all seven classes Forge touches today plus guide and badge, the full draft to review to edit to publish to delete loop is composed **entirely of procedures that already exist**. Twenty-two of twenty-five content-class rows are zero-game-change `YES` and three are `PARTIAL`. There is no publish toggle anywhere in the content routers: publishing is a whole-record `<class>.update` with the lifecycle field set. Four cross-cutting facts bound the product. Hidden is a listing and play gate, not confidentiality, so drafts are readable by id from any account. No content procedure checks a version, so two admins silently overwrite each other. The game exposes no approval state on any class. And a role denial arrives as an HTTP 200 `success:false` that transport cannot tell from any other refusal, so an authorization signal cannot be rendered truthfully without a director ruling on what to do about it.

**Quest Studio foundation status.** The ChatGPT-owned slice at `824c4d58` (Quest Source, a request branch, a dispatch-only Actions worker, `quest_compile.py`, a Mission adapter, and a Forge seam) is read here as architecture and roadmap **evidence only**. It is not a frozen review target, this package neither patches nor re-plans it, and the roadmap assumes its independent review rather than its current head. Under the one-writer rule, findings about it go to its owner.

---

## 3. The recommendation

**Architecture (section F): extract a headless `ForgeCore` first, then replace the shell against it, screen by screen.** Not "evolve", and not "replace the UI in one bet"; the sequenced form of both. Phase 0 measures and moves domain logic below the seam with the UI byte-identical. Only then does the surface change, one destination at a time, with the class names today's tests select on preserved. Sixteen modules are preserved unchanged or changed only additively; the four that are replaced or split are all under `forge/src/ui/`. The single execution-core edit in the whole programme is one additive, advisory event emitter in the runner that may not write the journal or advance an item state. The ratio is the argument: the part of Forge carrying 277 of the 293 test cases is the part that does not need to change, and the part that needs to change most carries 16. Two alternatives are kept with the reason each lost, and the load-bearing claims are all checkable by grep, diff or a socket-free test rather than taken on trust.

**Information architecture (section D): operation-first destinations, content lanes as the second axis.** The first level is the consequence the operator is about to have on production; content type is a filter and an entry point, not a destination that owns work. The decisive evidence is that Forge already derives the consequence class from the parsed plan, and that no content-type axis resolves for a package carrying two entity types or mixing reads with writes. The content-type alternative and the two-axis alternative are both kept, with the content-type proposal's own weakness list reproduced rather than paraphrased away. Labels, destination lists, mode taxonomy and lane taxonomy are **not** settled here; they are director decisions pending transcript reconciliation.

**The safety spine, which does not change.** Write-ahead journalling before the request leaves; `SENT` reconciled and never retried, with no transition back to `PLANNED`; two-phase create recovery through pre-create id snapshots with orphans surfaced for a human decision; no automatic deletion anywhere; pre-send validation that fails closed on unknown keys; the verdict read from the decoded application outcome, never from HTTP status; read-back of asserted fields with drift and unread kept non-terminal; the rate budget that halts rather than retrying a 429; game cookies and session material never in artifacts; the GitHub credential kept separate from game auth; and every live write behind an authenticated human tap. Section F preserves each of these byte-for-byte, and section G asserts them as standing gates in every phase rather than closing them once.

---

## 4. Roadmap headline

Nine phases. Each leaves a working Forge on the operator's phone and is reviewable on its own SHA. "Gated by" names what must be settled or true before the phase can be frozen; the retirement gates a phase makes measurable are in `G_ROADMAP.md` §G.1.1.

| Phase | One line | Gated by |
|---|---|---|
| 0 Foundations | Green `main`, one CI job, the measurement harness, domain logic below the seam with the UI byte-identical | K-13, K-14, K-60; nothing else |
| 1 Research and capture | Persistence tiers, paged and filtered list captures, audited registry rows, honest capture verdicts | phase 0; K-06, K-17 |
| 2 Shell and design system | The approved north star as tokens, components and one scoped stylesheet over the existing screens | phase 0; K-02, K-20 to K-24, K-31, K-32, K-33, K-56, K-57, K-58 |
| 3 Manifest and recovery | Preflight, run, halt, orphan, results, journaled repository sync, plus the ingress and edit-shape parity slices | phases 0, 1, 2; K-12, K-15, K-16, K-59 |
| S Quest Studio | Absorb the reviewed seam: promotion contract, durable Studio state, registry-driven UI, one shell | phases 0, 2, 3; the seam reviewed and integrated; K-25 to K-27, K-36 to K-40, K-46, K-49, K-50 |
| 4 Content Admin read | Queue, record detail, diff, preview, review package. No publish act | phases 1, 2, 3; K-03, K-04, K-05, K-08, K-09, K-10, K-16, K-34, K-47, K-52, K-53 |
| 5 Publish | The flip, read-back gated, with its own authority lane and confirmation | phase 4; K-07, K-12, K-30, K-54, K-55 |
| W Project Workspace | Workstream state rendered as one human workspace, read-only first | phases 2, 3; K-28, K-43, K-44 |
| 6 Builder retirement | Close the remaining gates, record the ruling, decommission the loader | phases 1, 3, the operator's live proof; K-10, K-11 |

Phases 0, 1 and 2 are the critical path. **Phase 0 is the only phase that can be briefed first**: it has no shell dependency, no admin dependency, no Studio precondition and no capture-policy decision.

**Explicitly not in the roadmap:** any TheNinjaRPG source change; an AI assistance layer in the Studio; Guide Studio and the infographic lane as production lanes; the guide content class until the pin moves; canonical-owner changes such as structured blocker codes in `mission.py` or profile-shape enforcement, which need their own Lane A briefs; re-implementing or patching anything on the ChatGPT Studio branch; a competing release-loader fix on a Fable branch; Studio v1.5 and v2 scope; any deletion affordance; and widening the full-capture allowlist or the 512 KiB ceiling as a side effect of a phase. `G_ROADMAP.md` §G.4 states where each lives instead.

---

## 5. Decisions the director must make before implementation can start

By id only. `K_USER_DECISIONS.md` is the owner of every entry, with the options, the practical consequence and an advisory recommendation where one is justified. Nothing here is settled.

**Blocks the first brief (phase 0):** **K-13** source-pin refresh before implementation; **K-14** whether the shipped bundle is minified; **K-60** who integrates the release-loader test fix that today lives on the ChatGPT branch, under one-writer discipline. All three change what phase 0's drift and size gates assert, and K-60 decides when a green baseline exists at all.

**Blocks the second brief (phase 1):** **K-06** capture data classification and what may persist to the public repository; **K-17** research-read registry expansion.

**Blocks the shell (phase 2), all pending predecessor-transcript reconciliation:** **K-02** and **K-20** navigation model and destination lists; **K-21**, **K-22**, **K-23**, **K-24**, **K-32**, **K-33** mode taxonomy, colours, type scale, lane taxonomy and button variants; **K-31**, **K-56**, **K-57**, **K-58** art, wordmark, theme and confirmation placement. **K-01** is ruled; what remains under it is token acceptance at the phase-2 freeze.

**Shapes the product rather than a phase:** **K-11** Builder deprecation timing; **K-55** whether a delegated Content Admin performs the publish act at all, which is a doctrine question no phase may assume the answer to; **K-15** with **K-26**, which decide one credential on one device across two phases and cannot be ruled separately; **K-10**, whose default for this pass is no game-source change.

Fifty-eight entries are registered, K-01 to K-60 with `K-18` and `K-19` left as unused numbering gaps. `K_USER_DECISIONS.md` §K.0 records the three rulings already made during the pass and what stays open under each.

---

## 6. Package map

Every file below is committed under `docs/forge_next/` at the frozen SHA.

| File | What it answers | Who should read it |
|---|---|---|
| `00_CONTEXT.md` | Provenance, boot sequence, source pins, method, constraints honoured, package layout | everyone, first |
| `A_ARCHITECTURE_MAP.md` | What Forge 0.4.0 and Builder v4.32 actually are today, module by module, with the seam and the state machines | reviewer, implementer |
| `B_PARITY_MATRIX.md` | 61 capability rows, 8 hard and 9 conditional retirement blockers, 10 gates | reviewer, director on K-11 |
| `C_WORKFLOW_INVENTORY.md` | The content workflows that really run here, with evidence, and what Forge must not absorb | reviewer, IA reader |
| `D_IA_AND_JOURNEYS.md` | Recommended IA, alternatives, mockup reconciliation, screens, journeys, confirmation model | director, UX reviewer |
| `D_VISUAL_SYSTEM.md` | The approved direction as tokens, components and binding state and motion rules | director, UX reviewer |
| `E_CONTENT_ADMIN_FEASIBILITY.md` | Per-class source audit: lifecycle, read, edit, publish, preview, roles, audit, zero-game-change verdict | director on K-03 to K-09, reviewer |
| `F_ARCHITECTURE_RECOMMENDATION.md` | Preserve, replace, abstract, migrate, per module, plus the brief's 18 technical questions | implementer, engineering auditor |
| `G_ROADMAP.md` | The nine phases with objective, files, prerequisites, gates, rollback and retirement impact | director, implementer |
| `H_RISK_REGISTER.md` | 31 risks with evidence, how each would bite, and the gate that bounds it | reviewer |
| `I_TEST_STRATEGY.md` | Test architecture, static gates, per-phase gate map, and the operator-owned browser and live smoke | implementer, reviewer |
| `J_MIGRATION_AND_RETIREMENT.md` | The retirement gate ladder, transition posture, storage and contract migration, what is not retired | director on K-11, implementer |
| `K_USER_DECISIONS.md` | The 58-entry decision register, and the three rulings already made | director |
| `evidence/*.json` | The parity and admin matrices with their verification state, plus registry gap, drift, harvest evidence, repository consumers, test and CI inventory, current-UX audit, visual synthesis, and the contrast checker (`contrast.py`) | auditor checking a row |
| `wireframes/` | `index.html`, seventeen screen pages `wf01` to `wf17` each showing phone 390 and desktop 1280, `src/` to regenerate them, `review/` with seven rendered JPEG captures | director, UX reviewer |
| `design/` | The approved concept mockup as a committed copy, with its provenance pointer | director, UX reviewer |

Two notes on this map. `D_IA_AND_JOURNEYS.md` §D.3.1 counts sixteen wireframe pages; seventeen are on disk, because `wf17_degraded_states` was added after that table was written. And the section-17 independent-review handoff, `docs/handoffs/FORGE_NEXT_PLANNING_HANDOFF.md`, is **forthcoming**: it is not on disk at the time this entry point was written.

---

## 7. How to review this, how to act on it, and what happens meanwhile

**Reviewing it.** The audit target is the exact frozen SHA, not the branch name. The handoff named above carries the section-17 fields and the repository's own handoff format (`docs/workflows/IMPLEMENTATION_HANDOFF.md`): exact base and head SHAs, every artifact actually committed, the gate commands and results, the source pins inspected, the open decisions, the items that stayed pending only because the predecessor transcript was unavailable, and the explicit statement that no implementation, live request, live write or credential use occurred. Read that file, then read `00_CONTEXT.md`, then the section that carries the claim being checked. A row's evidence tier and verification status are stated in the section that owns it; `B_PARITY_MATRIX.md` §B.1 and `E_CONTENT_ADMIN_FEASIBILITY.md` §E.1 are what a reviewer should rely on before drawing a conclusion from a matrix row, not any summary of them.

**Acting on it.** Two steps, in order. First a ruling on the blocking decisions in section 5 above, recorded in `docs/RULINGS.md` with the operative rule moved to its canonical owner. Then a Lane A implementation brief for phase 0 and nothing else, committed as `state/prompt_<task>.md` in the existing pattern, pinning the ten headings `G_ROADMAP.md` §G.5 lists: base SHA and branch with one named owner, the K-60 assignment, K-13 and K-14, the exact file list below the seam that may be touched, the DOM fixture set and its byte-identical acceptance, the CI shape, the bundle budget numbers, the storage promise, the socket-free requirement, and what is out of scope. A phase does not start without that brief. Independent review of this package is not, by itself, approval of the roadmap; the director approves the roadmap separately.

**The Builder meanwhile: nothing happens to it.** It stays installed, pinned and the first choice for the work Forge cannot do. This package deprecates nothing, uninstalls nothing, and moves no pin. Retirement happens by measured gates and a recorded ruling, never by decree, and the failure mode is asymmetric: another month of two tools costs nothing measurable, while removing the Builder one gate early strands proven work with no escape path.

---

## 8. Provenance

**Base:** `main@305a28f992e33194fbba279a3f32e698dfb2b67f`, verified at the start of the pass and again at each amendment. The planning branch changes no file under `forge/`, `skills/`, `state/`, `docs/design/` or `.github/`.

**Source pins inspected**, all on read-only clones of the public game repository, nothing executed, no request to any game host: upstream head `36c5873b`, Forge global pin `345d18ac`, protected-auth task pin `bdec2883`. Design and ruling evidence was consumed read-only from `chatgpt/forge-quest-studio-foundation@824c4d58` and `chatgpt/forge-next-planning@0bb5a54b`; neither branch was merged, rebased onto, or modified. The planning contract is `state/prompt_forge_next_planning.md` at `chatgpt/forge-next-planning@70c15161`.

**Gates run in this session, read-only, none piped in a way that masks its exit code:**

| Gate | Result |
|---|---|
| `skills/building-tnr-content/scripts/doctrinemap.py` | exit 0; 21 assertions, 18 referenced, 16 surfaces, 0 errors, 0 warnings |
| `render_doctrine.py --check` | exit 0, all projections current |
| `build_packs.py --check` | exit 0, all packs and TOCs current |
| `lawmap.py` | exit 0; 93 laws, 93 matrix rows, 77 citations across 35 files, 0 errors, 5 warnings |
| `cd forge && npm test` | 293 tests, 292 pass, 1 fail: the release-loader marker test, the known red baseline recorded as R-11 and gate G-09 |

This package changes no file those gates own.

**Constraints honoured (brief §16):** no Forge production implementation; no Builder deletion or deprecation; no live game request; no live game write; no use, request or export of session cookies or credentials; no TheNinjaRPG code change; no release-pin movement; no manifest contract migration; no doctrine or law change to fit a proposed UI; no publishing or live content change.
