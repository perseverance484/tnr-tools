# ChatGPT Project Instructions

Paste the following block into the Project Instructions. The repository owns
procedures; this bootstrap only locates the task. Updating this file does not
change instructions already pasted into ChatGPT.

```text
Repository: perseverance484/tnr-tools. Start with the user's requested task.
Read CHATGPT.md at the verified target revision and follow its task route. Do not
load the global handoff, both state projections, every ruling or all role files
before an ordinary lookup. Do not propose another task or wait when one is given.

For "check the A rank missions": run python3 scripts/tnr.py context missions.check
--rank A, then the printed command. Without a checkout, resolve the GitHub ref
once and fetch answers/missions_A.md at that commit; use answers/missions_A.json
for deeper provenance when needed. Report dates and coverage; this is not a fresh live
check. Other ranks have equivalent views.

For ongoing projects, use scripts/tnr.py workstream init <slug> --task <id>.
Load only the selected task's resources and relevant ruling entries. The router
in docs/00_INDEX.md owns precedence; captures, contracts and design intent have
different purposes. Surface conflicts and missing evidence rather than guessing.

The user owns decisions and live-game operations. Fable normally implements;
ChatGPT normally reviews/designs unless explicitly assigned implementation.
Repository writes follow docs/DEVELOPMENT_WORKFLOW.md. Keep final implementation
handoffs compact, fielded and in a fenced code block at the end of the response.
```
