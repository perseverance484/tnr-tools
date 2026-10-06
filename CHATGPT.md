# ChatGPT entry point

Use the user's requested task as the starting point. Verify the target repository
revision once, then load only the matching task packet. Do not perform a global
session ritual or propose another task when the user already supplied one.

| Request | Start here |
|---|---|
| Check existing missions | `python3 scripts/tnr.py context missions.check --rank A`, then the printed command |
| Existing jutsu art | `python3 scripts/tnr.py context jutsu.art` |
| Resume a content workstream | `python3 scripts/tnr.py workstream init <slug> --task <id>` |
| Build/edit content | `skills/building-tnr-content/SKILL.md`, then its task pack |
| Code review | `docs/workflows/FABLE_REVIEW.md` and the exact frozen target |
| Art production | `docs/workflows/ART_PRODUCTION.md` |
| Repository audit | `docs/agents/RELEASE_AUDITOR.md` |

Without a checkout, resolve the GitHub ref once and read the task's generated view
and evidence at the same commit. Read `answers/missions_A.md`; fetch
`answers/missions_A.json` for deeper provenance when needed (also B/C/D/S).
Label these as committed observations.

`docs/00_INDEX.md` owns precedence. `docs/DOCTRINE.md` owns shared rules;
`docs/ENGINE_LAWS.md` owns numbered law text. Read relevant sections when needed.
`docs/RULINGS.md` records decisions; load relevant entries, not the whole history.
Do not mix observed records, generated contracts and design intent.

ChatGPT normally reviews and designs; Fable normally implements. Explicit user
implementation assignments override that default. For repository writes, load
`docs/DEVELOPMENT_WORKFLOW.md`: use a ChatGPT-owned branch, preserve other writers,
and arrange independent review of code you author. A read-only query requires
no branch or shared-state update. User-owned decisions and all live-game actions
remain the user's. Repository access does not authorize game requests or writes.

State lives in the selected workstream. `state/digest.json` is a navigation summary;
its two projections are alternative views, not additional required readings.
Record durable task outcomes and evidence in their owning workstream. Use
`docs/workflows/IMPLEMENTATION_HANDOFF.md` for substantial implementation handoffs.
Keep handoffs compact and fielded; place the final handoff in a fenced code block
at the end of the response. Never invent IDs, verification, freshness or completion.

Use the name dauntless in artifacts. Preserve repository privacy rules; never
include prohibited franchise material or copy proprietary prose.
