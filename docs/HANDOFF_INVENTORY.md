# TNR HANDOFF INVENTORY — DRAFT

Status: DRAFT, uncommitted. Intended path `docs/HANDOFF_INVENTORY.md` on `main` of
`perseverance484/tnr-tools` once dauntless approves.

Purpose: opening brief for ChatGPT, taking over as auditor, design collaborator and
visual asset specialist. Claude Code takes implementation. This file states what data
exists, where it lives, and what still has to be moved out of the Claude project before
that project can be retired.

---

## 0. ROLE MAP AFTER RESTRUCTURE

| Lane | Owner |
|---|---|
| Design, audit, prose, communication layer | ChatGPT |
| Visual assets (generation + direction) | ChatGPT |
| Code, scripts, manifests, repo surgery | Claude Code |
| Rulings, balance, publishing, all game pushes | dauntless |

Non-negotiables carried over: dauntless never appears by real name, only the username.
Nothing ships unvalidated. Everything ships `hidden: true`. All game writes are a manual
tap by dauntless — no automated write path exists or is permitted.

---

## 1. ALREADY IN THE REPO (no extraction needed — read it directly)

`github.com/perseverance484/tnr-tools`, branch `main`. This is canon and memory. ChatGPT
should treat it as authoritative over anything recalled from chat.

### Laws and doctrine — `docs/` (10 files)
- `ENGINE_LAWS.md` — 93 numbered laws, the text of record
- `10_LAWS_core.md` — cross-cutting laws
- `00_INDEX.md` — router, precedence table, evidence tiers, task routing
- `DOCTRINE.md` — single source; the mounted project instructions are rendered from it
- `mounted_instructions.tmpl`, `active_context.tmpl` — render templates
- `DRIFT.md`, `COMPACTION_RUNBOOK.md`
- `PLAN_2026-08-30_stack_optimization.md` (executed), `PLAN_2026-09-03_builder_app.md` (open)

### Skills — `skills/` (106 files)
- `building-tnr-content/` — `SKILL.md`, `12b_LAWS_coverage.md`, `references/`
  (ai, quest, jutsu, item, event, balance, lines, pipeline), `packs/` (pre-assembled
  task excerpts), `data/`, and 33 scripts including `session_open.py`, `session_close.py`,
  `validate.py`, `factory.py`, `harvest.py`, `lawmap.py`, `schema_extract.py`,
  `schema_diff.py`, `mission.py`, `enemy.py`, `calc.py`, `sim_damage.py`, `sim_turns.py`
- `producing-tnr-art/` — `SKILL.md`, `references/`, `data/` (art spec, frames, rank icons),
  and `rawqc.py`, `chroma.py`, `artpreflight.py`, `shotlist.py`

### Generated contract files — repo root
- `45c_DATA_constructors.json` — effect tag constructors
- `45g_DATA_checks.json` — shared check config (builder preflight + validate.py)
- `32b_DATA_pool.json` — pool codes
- Generated from `studie-tech/TheNinjaRPG` by `schema_extract.py`; never hand-edited

### Live-state layer
- `answers/` — name/id catalogs: jutsu, item, ai, asset, quest, plus `hot.json` and `INDEX.md`
- `harvests/` + `harvests/inbox/` — 37 results bundles, the read-back record of every push
- `push/` — 55 staged manifests, numbered, plus `.gen.py` generators
- `state/` — 33 files: `digest.json` (board of record), `active-context.md` (handoff),
  art backlogs, wiring maps, prose passes, Tenth Name rebuild iterations, thread init prompts
- `reports/code_audit_2026-09-02.json` — 12-finding Claude Code audit

### Builder
- `builder_bundle.js`, `builder_loader_user.js` — the ViolentMonkey userscript, currently v4.32
- `dist/` — installable skill zips
- `EVENT_SHEET.md` / `.docx` — staff-facing event design canvas

### Archive
- `archive/` — research brief and report (stack optimization), rollout plan, source audit,
  spent manifests, wedge diagnosis, prior project/repo eras

---

## 2. LIVES ONLY IN THE CLAUDE PROJECT (must be extracted)

This is the actual work of the handoff. Ordered by cost of loss.

### 2.1 Project instructions (mounted paste)
Rendered projection of `docs/DOCTRINE.md` + `mounted_instructions.tmpl`. The doctrine text
is already in the repo. **What is NOT in the repo: the GitHub PAT, which is carried inline
in the mounted instructions.** See §4.

### 2.2 Claude's memory layer
A structured summary of working context that was never written to the repo verbatim. Content
overlaps repo canon heavily but carries some things not stated anywhere in `docs/`:
- The mission standard as narrative rule ("short stories / anime episodes, not murder
  mysteries" — one want in the first minute, one antagonist, one fight, one truth in a line,
  a cost at the end)
- The rank rubric: rank is set by who you are expected to fight, not raw difficulty
- The motive-audit framework: every actor needs a stated reason for their method and a stated
  reason for not doing the obvious cheaper thing
- Communication and artifact conventions
Extraction: transcribe into `docs/` as a design doctrine file. Status: NOT DONE.

### 2.3 Conversation corpus — approximately 35 sessions, 2026-08-20 to 2026-09-04
The largest unextracted body. Repo state records *what* was decided; the transcripts record
*why*, and record the rejected alternatives. Broad eras:

| Era | Dates | Contents |
|---|---|---|
| Pre-Forsworn content | 08-20 → 08-26 | Larry the Fish event, Bloodcore Bars, Genin Trials/KGK, Blacksteel Tides, D-mission waves, Five Masters proposal, Crimson Reckoning / The Nameless Thorn, One White Ear, Copies Not Thefts, The Unsigned enemy line |
| Toolchain construction | 08-26 → 08-28 | Builder v4.16 → v4.23, schema_extract build-out, law reconciliation to 83 then 93, skills packaging, art spec + house style ratification |
| Forsworn build | 08-28 → 09-01 | Ten missions, nine AI, prose passes, the wedge diagnosis, avatars, backgrounds, map pins, rank icons, publish wave |
| Stack optimization | 08-30 | 3-session arc: audit → deep research → implementation (11 work orders, builder v4.28/4.29) |
| Restructure era | 09-02 → 09-04 | Code audit batch 1, law provenance report, events onboarding, builder app redesign, mission flatten |

Not yet extracted from these: the full ruling ledger (many rulings exist only as chat text),
rejected design iterations (e.g. the Forsworn naming ladder went through ~10 rejected sets),
art direction rationale, and root-cause narratives for bugs already fixed.

### 2.4 Ephemeral container artifacts
Work that ran in Claude's container and was never committed:
- Ad-hoc PIL/numpy compositing pipelines for art processing (the repo toolchain is
  stdlib-only; porting these is an owed item)
- Cast sheets, enemy roster cards, infographics, posters, annotated support screenshots
- Session-local diagnostic scripts
Recoverable only by re-derivation or by pulling files back out of the conversations.

### 2.5 Uploads inside conversations
Game source zips, harvest JSONs, raw art generations, screenshots. The processed outputs
mostly landed in the repo; the raws largely did not.

---

## 3. NOT IN EITHER — live game state

The game database is the only authority for current record contents. Neither the repo nor the
transcripts can answer "what does record X look like right now." Capture-first is law: read it
back, never assume. `answers/` is a name/id catalog, not record contents.

---

## 4. FLAGS FOR CHATGPT AND FOR DAUNTLESS

1. **Credential.** The container PAT (`tnr-container`, contents RW on `tnr-tools` only) is
   carried inline in the Claude project instructions. `tnr-tools` is a **public** repo — this
   inventory, and anything else committed, must never contain it. If ChatGPT is being given
   repo access, it should get its own fine-grained token, and the existing one should be
   rotated as part of the restructure. Recommend rotation regardless, since the token has been
   pasted into a chat surface across many sessions.

2. **The PAT cannot push `.github/workflows/`.** Workflow installs require dauntless via the
   GitHub web UI. Any plan that assumes agent-side workflow edits is wrong.

3. **Hard platform constraint.** Samsung Android, Firefox mobile, ViolentMonkey. No desktop,
   no devtools. Any tool proposal that assumes a desktop is dead on arrival.

4. **Open board items that a new collaborator will trip over:**
   - `push/46_missions_flatten.json` is committed and UNRUN, awaiting tap
   - `push/45_mission_ai_self_target_fix.json` unrun (no conflict with 46)
   - Older prose manifests for Old Ghost and The Tenth Name are unrun and would silently
     re-inflate those missions if tapped after 46
   - All ten missions are `hidden: false` and live; tapping reassigns node ids under any
     player mid-mission
   - Law provenance report received, spot-verified, NOT adopted: 93 laws sorted ENGINE 36 /
     PARTIAL 19 / NOT_IN_SOURCE 26 / DOCTRINE 11 / CONTRADICTED 1. Laws 19 and 23 confirmed
     wrong. `ENGINE_LAWS.md` is untouched. This reconciliation is the next big pass.
   - Doctrine rewrite to match the 4-node mission shape is deferred by ruling until player
     feedback lands
   - The Tenth Name has no dedicated enemy AI

5. **Known-wrong laws.** Do not treat `ENGINE_LAWS.md` as source-verified in bulk. 26 of 93
   laws are not in the source at all. Evidence tiers in `00_INDEX.md` govern.

---

## 5. PROPOSED EXTRACTION ORDER

1. Rotate the PAT; issue ChatGPT its own scoped token.
2. Transcribe the memory layer (§2.2) into a committed design doctrine file.
3. Sweep the conversation corpus for unrecorded rulings and land a single ruling ledger.
4. Decide scope on pre-Forsworn era history (§2.3 row 1) — largest unbounded chunk.
5. Port the ad-hoc art compositing pipeline into stdlib scripts in the art skill.
6. Retire the Claude project once 1–5 are done.

---

## 6. OPEN QUESTIONS — FOR CHATGPT TO RETURN A POSITION ON

Numbered so answers can be returned by number. These are positions to propose; dauntless rules.

**Q1 — Credential posture.** Own scoped fine-grained token for ChatGPT, or read-only access
plus Claude Code as the sole writer? State which, and what scope. Rotation of the existing
container PAT is assumed either way.

**Q2 — Pre-Forsworn history scope.** Extract design rationale from the 08-20 to 08-26 era
(Larry the Fish, Borrowed Awakening, Crimson Reckoning / The Nameless Thorn, Genin Trials,
Bloodcore Bars, Five Masters, One White Ear, Copies Not Thefts), or treat that content as
shipped-and-done with only its live ids mattering? This is the largest unbounded chunk of
work in the handoff.

**Q3 — Ruling ledger format.** Many rulings exist only as chat text. Propose the shape of a
single committed ledger: flat append-only file, per-domain files, or rows in `state/`.
Include how a ruling is superseded.

**Q4 — Law reconciliation sequencing.** 93 laws sort ENGINE 36 / PARTIAL 19 / NOT_IN_SOURCE 26
/ DOCTRINE 11 / CONTRADICTED 1. Laws 19 and 23 are confirmed wrong. Propose an order: fix the
contradicted two first, or sweep by class, or split `ENGINE_LAWS.md` into engine-verified and
doctrine files. Note that doctrine rewrite for the new mission shape is already deferred
pending player feedback, so the two passes may collide.

**Q5 — Art pipeline ownership.** The ad-hoc PIL/numpy compositing that produced most shipped
art was never committed; the repo toolchain is stdlib-only. Propose whether the art lane keeps
stdlib discipline (port the work) or gets an explicit dependency exception.

**Q6 — Communication layer contract.** Define what ChatGPT hands to Claude Code and in what
form — briefs in `state/`, issues, or manifests. The current pattern is a written brief
committed to `state/` and pasted as a prompt.

**Q7 — Claude project retirement.** Confirm the retirement gate: is it §5 items 1-5 complete,
or something narrower?
