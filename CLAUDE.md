# Claude Code / Fable entry point

Fable is the normal implementation owner for TNR tooling and content. Start with
the user's task and its source contract. Verify the target revision once. Do not
load every workstream, historical ruling or global state projection first.

| Task | Required route |
|---|---|
| Inspect existing missions | `python3 scripts/tnr.py context missions.check --rank A` |
| Content build/edit | `skills/building-tnr-content/SKILL.md` and its selected pack |
| Resume a project | `python3 scripts/tnr.py workstream init <slug> --task <id>` |
| Code/tooling/infrastructure | `docs/DEVELOPMENT_WORKFLOW.md` and the committed task brief |
| Art | `skills/producing-tnr-art/SKILL.md` and applicable workflow |

`docs/00_INDEX.md` owns precedence, `docs/DOCTRINE.md` shared rules, and
`docs/ENGINE_LAWS.md` numbered laws. Read task-relevant sections. Generated
contracts own shapes, captures own observations, and design sources own intent.
Relevant user rulings constrain the task; historical decision records do not
replace their canonical owners. Update owners and regenerate projections.

Lane A uses a Fable-owned branch, one writer, exact-SHA handoff and independent
review. Freeze review targets. Lane B retains routine validated content delivery.
Follow `docs/workflows/IMPLEMENTATION_HANDOFF.md`; list actual gates and evidence.
Use existing tools and meaningful regression tests. No unrelated refactoring.

Only the user operates the live game. Never obtain or fabricate game credentials.
Use native environment authentication for repository work; do not embed a PAT in
instructions or Git URLs. Balance, rewards, publishing, art direction and final
acceptance remain user-owned. Approved user scope takes precedence over defaults.

Read-only queries do not edit shared state. Task outcomes belong to their owning
workstream; the global digest is navigation. Run `python3 scripts/tnr.py verify`
for repository-infrastructure changes, plus affected product tests/builds. Do not
interpret NOT APPLICABLE checks as successful verification of that capability.

Use the name dauntless in artifacts. Preserve repository privacy rules; never
include prohibited franchise material or copy proprietary prose.
