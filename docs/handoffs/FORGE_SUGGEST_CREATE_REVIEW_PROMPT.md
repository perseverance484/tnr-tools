# Forge suggest-mode creates: independent review prompt

~~~text
You are the independent reviewer for a Lane A code change in perseverance484/tnr-tools. Review only; do not patch the
Fable branch. Follow docs/workflows/FABLE_REVIEW.md.

TARGET
- Branch: fable/forge-suggest-create (frozen)
- Head (audit target): 92d8103afd5f5d2ccc5b0ca2ffcd265805d4d233
- Base: 02d8b438d9fb21fe1f3596b2fbcb51f05111e83e
- Brief: state/prompt_forge_suggest_create.md (RUL-2026-10-25-001)
- Handoff: docs/handoffs/FORGE_SUGGEST_CREATE_HANDOFF.md (on main)
- Game source: studie-tech/theninjarpg@2aed7e4903cc68e18c01e0adb7aec8f39ddffc64 (read only, never run)

Verify the head SHA first. If the branch has moved, stop and report.

SAFETY: zero live-game requests, no credentials, fixtures and the in-process fake desk only.

WHAT IT DOES: suggest-mode manifests may now include slot "create" items, sent to contentReview.create with
entityId null (a CREATE suggestion the desk applies only on approval). AI creates and references to a suggested
create are refused at parse; quests stay unsuggestible.

READ: docs/00_INDEX.md; the brief; the handoff; at the pin app/src/validators/contentReview.ts,
app/src/libs/contentReview/submit.ts (createStaffProposal, applyProposal path), app/src/server/api/routers/contentReview.ts
(create, getQueue, toSummary); the diff 02d8b43..92d8103.

GATES TO REPRODUCE (Node 24, full history): cd forge && npm test (651/651); npm run build && git diff --quiet --
forge_bundle.js; node tools/check_bundle_budget.mjs; node tools/check_release_pin.mjs; check_manifest.mjs and
validate.py --strict on push/254 with "mode": "suggest" and a NEW_CONTENT suggestion block. Report exact commands and
exit codes without masking them.

ATTACK FIRST: the five risks in the handoff, especially the journal CONFIRMED -> SENT exemption and duplicate CREATE
suggestions after a lost response. Then: that edits behave exactly as before; that a create's payload matches what
the desk validates; that refs/images resolve before the send and a ref to a suggested create cannot slip through
(targetId, nested data, typed refs).

REPORT: findings with severity (blocker / should-fix / note), file:line, invariant, reproduction, suggested fix;
what you checked clean; what needs a live session; verdict (approve / approve with fixes / reject).
~~~
