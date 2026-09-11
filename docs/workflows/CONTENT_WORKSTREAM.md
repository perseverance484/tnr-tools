# Workflow — Content Workstreams

Use when a TNR content project (event, quest, mission arc) is large enough that one conversation cannot finish it.

A **content workstream** makes the repository the bridge between conversations. A top-level planning conversation commits the roadmap and its durable resources; later specialised conversations initialize from the repository and execute one bounded task, without needing the predecessor chat.

The roadmap is **coordination state, not canon.** `docs/00_INDEX.md` remains the only precedence table, `state/active-context.md` and `state/status.json` remain the global session state, and doctrine, engine laws, generated contracts, captures, art specs and `state/prompt_<task>.md` build contracts all keep their existing owners. The roadmap points at them and never restates them.

## 1. Layout

```text
state/workstreams/INDEX.md               generated projection of all workstreams
state/workstreams/<slug>/roadmap.json    canonical coordination source — edit this
state/workstreams/<slug>/ROADMAP.md      generated projection
scripts/content_workstream.py            validate / render / list / next / init
```

`roadmap.json` is the editable source. Both Markdown files are generated and say so at the top; never hand-edit them.

## 2. Session initialization

When the user says something equivalent to:

> Initialize session from repo. Workstream: `One Perfect Crop`. Task: `art.scene_characters`.

the session should:

1. verify the live repository and the current `main` SHA;
2. read `state/active-context.md`, `state/status.json`, `docs/00_INDEX.md`, `docs/RULINGS.md`, `CHATGPT.md` and the relevant role/workflow files as normal;
3. run the initializer, which is a deterministic view of the roadmap and not itself an authority:
   ```
   python3 scripts/content_workstream.py init <slug> --task <task-id>
   ```
4. confirm the task is `READY` or `IN_PROGRESS` and that its dependencies and resources are real — the initializer refuses and explains when they are not;
5. read the task's `required_resources` plus the completed upstream evidence the packet lists;
6. state the objective, the completion gates, and any user-owned decisions still open;
7. work **only that task**, unless new evidence genuinely requires a roadmap change;
8. at a durable stopping point, update the task's status, evidence and `resume_note`, then re-validate and re-render.

A healthy workstream needs no predecessor transcript. If the packet cannot be executed from the repository alone, that is a roadmap defect: fix the roadmap rather than filling the gap from memory.

Fable / Claude Code follows the same routing, with one addition: when an explicit `state/prompt_<task>.md` implementation brief exists, **that brief is the build contract**, and the roadmap task is the pointer to it, not a substitute for it.

## 3. A task is a session-sized packet

Do not model every individual image, node or small artifact as its own task. Group work that benefits from one loaded context and one production mode.

Prefer **one** task when all of these hold:

- same production mode and tools;
- same reference set or nearby context;
- the work can be completed coherently in one conversation;
- there is value in visual or narrative consistency across the outputs.

**Split** when:

- a user decision gates the second half;
- a different authority/source stack is needed;
- a Lane A implementation or review boundary begins;
- mixing asset classes risks image-generation context contamination;
- the session would grow too large to reconstruct or verify cleanly.

Worked examples:

- **Good** — all scene characters in one art session, generated and QC'd one at a time.
- **Good** — all AI avatars in a separate art session.
- **Bad** — one roadmap task per individual character portrait.
- **Bad** — icons and scene characters in one generation task, because their visual and reference modes differ.

"One task" means one conversation and one context. Inside an art task, the art workflow's one-asset-at-a-time generate/QC rhythm still applies.

## 4. Statuses

| Status | Means |
|---|---|
| `PLANNED` | known work, not yet executable |
| `READY` | a fresh session can execute it now from repository evidence alone |
| `IN_PROGRESS` | started and paused; carries a `resume_note` |
| `BLOCKED` | named blocker or open user decision prevents it |
| `REVIEW` | delivered, awaiting independent audit |
| `COMPLETE` | gates satisfied and evidence recorded |
| `SKIPPED` | deliberately not done |
| `SUPERSEDED` | replaced by other work |

Two rules carry most of the weight:

**`READY` means executable from the repository.** If a critical input exists only in chat history, an ephemeral attachment or a sandbox path, the task is not `READY`. Say so in a blocker. The validator rejects absolute paths, `/mnt/data`, `/tmp`, `sandbox:` and `~/` in durable resources, and rejects a `READY` or `IN_PROGRESS` task whose required resource does not exist.

**`COMPLETE` needs evidence, not a claim.** A conversation saying the work is finished is not evidence, and neither is a sentence written into `roadmap.json`. A `COMPLETE` task must carry at least one **verifiable anchor** — something a later session can go and check:

| Evidence kind | Anchors `COMPLETE`? |
|---|---|
| `path`, `capture` | yes, when the repository file exists |
| `sha` | yes, when it is an exact lowercase 40-hex commit id |
| `decision`, `validator`, `approval` | only when they also name a committed `source` path that exists |
| `note` | **never** |

The validator rejects a `COMPLETE` task with an empty `evidence` list, one whose evidence is all unanchored claims, evidence pointing at a file that does not exist, and a malformed `sha`. Unanchored `note`/`decision`/`approval` entries remain useful *alongside* an anchor — they explain what the anchor means.

**A `COMPLETE` workstream must have no unfinished tasks.** When the top-level `status` is `COMPLETE`, every task must be `COMPLETE`, `SKIPPED` or `SUPERSEDED`; otherwise the generated `INDEX.md` and `ROADMAP.md` would advertise completion that the task table contradicts. `ACTIVE` and `BLOCKED` workstreams are not constrained this way — an active workstream legitimately holds `READY` and `BLOCKED` work at the same time.

If a conversation stops partway, set `IN_PROGRESS` with a concise `resume_note` and the current durable outputs. Do not mark partial work `COMPLETE` to advance the roadmap.

## 5. User-owned decisions stay visible

Balance, rewards, rarity, publishing, final art direction, final content acceptance and every live action remain the user's. A task gated on one of these says so in `blockers` / `open_decisions` rather than inventing a value to make the roadmap green. The initializer surfaces them, and the ones open elsewhere in the workstream, as context.

## 6. Top-level planning conversation

Once enough requirements are known, the planning conversation should:

1. establish a concise durable content/design source, or point at existing committed material;
2. enumerate the full expected workstream from design through readback;
3. group work into session-sized tasks by context and tooling affinity;
4. mark dependencies and user-owned decision gates;
5. commit every durable resource and pointer available;
6. mark a task `READY` only when a future session could execute it from repository evidence alone;
7. render the roadmap;
8. keep the workstream updated when scope or sequencing changes.

The planning conversation remains useful as a coordinator, but after the roadmap exists it is no longer a required memory source.

## 7. Commands

```bash
python3 scripts/content_workstream.py validate --all
python3 scripts/content_workstream.py render --all
python3 scripts/content_workstream.py render --check     # fails if a projection is stale
python3 scripts/content_workstream.py list
python3 scripts/content_workstream.py next <slug>
python3 scripts/content_workstream.py init <slug> --task <task-id>
python3 scripts/content_workstream.py --selftest
```

All of them are deterministic, stdlib-only and socket-free. Nothing here contacts ChatGPT, GitHub, the TNR API or an image generator, and nothing here performs a game write.

Re-render after every roadmap edit; `render --check` is the drift gate.

## 8. Lane boundaries are unchanged

The workstream is an orchestration layer only.

- Routine content/design/art production continues through the established Lane B content workflow.
- Code/tooling changes and substantial Fable implementation still use Lane A branch ownership, exact-SHA handoff and independent review under `docs/DEVELOPMENT_WORKFLOW.md`.
- `state/prompt_<task>.md` remains the normal substantial ChatGPT→Fable implementation contract; a roadmap task points at that brief once it exists.
- The user remains the only live-game actor.

The workstream does not replace `state/digest.json`, `state/active-context.md` or `state/status.json`, does not introduce a second precedence system, and does not make GitHub Issues a content authority.
