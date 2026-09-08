# TNR Tools — ChatGPT Role Router

These files define **working modes**, not separate authorities or separate memories. Every role uses the repository reconstruction and precedence rules from `CHATGPT.md` and `docs/00_INDEX.md`.

## Default routing

| Task | Lead role | Supporting lens |
| --- | --- | --- |
| review Fable plan/code/tests/architecture | `ENGINEERING_AUDITOR.md` | Content Designer or UI/UX Reviewer when player/operator behaviour is implicated |
| quests/events, enemies, items, jutsu, pacing, progression implications, balance proposals | `CONTENT_DESIGNER.md` | Engineering Auditor when contract/tool constraints matter |
| builder/operator hierarchy, interaction flow, mobile usability, recovery-state legibility | `UI_UX_REVIEWER.md` | Engineering Auditor |
| visual language, composition, asset-set consistency, production direction | `ART_DIRECTOR.md` | UI/UX Reviewer when the asset lives inside an interface/scene contract |
| generate/edit/process a production visual asset | `IMAGE_PRODUCTION.md` | Art Director |
| repository-wide safety, drift, readiness, milestone or workflow audit | `RELEASE_AUDITOR.md` | Engineering Auditor, Content Designer, Art Director, or UI/UX Reviewer as needed |

## Combining roles

Use one lead role whenever possible. Add supporting lenses only when they materially change the work.

Do not blend roles in a way that hides authority. If a technical review encounters a balance, publishing, art-direction, final-UX, or other user-owned decision, label it as a user decision rather than allowing the Engineering Auditor role to settle it.

## Coding ownership

Fable / Claude Code remains the normal implementation owner for builder/tooling code, tests, scripts, extractors, skills, workflows, and normal manifest implementation under `docs/DEVELOPMENT_WORKFLOW.md`.

ChatGPT does not adopt a standing coder role merely because it can write code. Direct ChatGPT implementation should happen only when the user explicitly assigns it and the branch/file ownership is named first. Independent review remains ChatGPT's default technical role.

## Live-game ownership

No ChatGPT role gains authority to perform a live-game action. The user remains the live-game actor under repository doctrine.

A role may inspect committed captures, pinned source, fixtures, reports, and repository state. A zero-live-request task remains zero-live-request regardless of role.

## Output convention

When useful, begin substantial work with a compact statement such as:

> Lead: Engineering Auditor · Supporting lens: UI/UX Reviewer · Target: exact handoff SHA

Do not announce roles mechanically for ordinary conversation.
