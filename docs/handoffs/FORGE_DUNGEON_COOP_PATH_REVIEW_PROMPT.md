# Forge 0.9.1 dungeon mount path: independent review prompt

~~~text
You are the independent reviewer for a Lane A fix in perseverance484/tnr-tools. Review only; do not patch the Fable
branch. Follow docs/workflows/FABLE_REVIEW.md.

TARGET
- Branch: fable/forge-dungeon-coop-path (frozen)
- Head (audit target): c45fbb9399b5728b3471cbc3b3901101b23f7f2e
- Base: a10d8be4ca5eb24da6778dfcec3bc905ab077a98
- Handoff: docs/handoffs/FORGE_DUNGEON_COOP_PATH_HANDOFF.md (on main)
- Game source pin: studie-tech/theninjarpg@107d7a86894f806a4c9cec89effef5992118a0ed (read only, never run)
Verify the head SHA first. If the branch has moved, stop and report.

SAFETY: zero live-game requests, no credentials or session material.

THE BUG: Forge 0.9.0 called "dungeon.getAll"; the live server answered NOT_FOUND because root.ts mounts coopRouter at
`coop` and routers/coop.ts mounts dungeonRouter at `dungeon`. The fix renames every path to coop.dungeon.* and makes the
extractor derive and guard the mount chain.

CHECK
1. At the pin, trace root.ts -> coop.ts -> dungeon.ts and confirm the tRPC paths are coop.dungeon.getAll / .save, and
   that the client's batch URL shape (/api/trpc/coop.dungeon.save?batch=1) is what the server expects for nested routers.
2. Any remaining bare "dungeon." procedure string in forge/src or the bundle (grep both). Procedure tables, budget
   metering (limited path), the composed-limiter exception, reconciliation and journal keys must all use the new path.
   Could a journal or budget record written under the old key by 0.9.0 confuse 0.9.1? (0.9.0 wrote nothing live, but
   it may have persisted local budget/journal state.)
3. The extractor's mount assertions fail closed on a renamed, duplicated or additional mount; the new tests prove it.
4. Every other Forge contract path: is any other router nested (not mounted directly in root.ts)?
5. The fake game must now refuse a bare dungeon.* path; confirm no test still passes only because the fake is lenient.
Reproduce: cd forge && npm test (718/718); node tools/derive_dungeon.mjs <pin> --check; npm run build && git diff
--quiet -- forge_bundle.js; node tools/check_release_pin.mjs; node tools/check_bundle_budget.mjs (expected to FAIL by
145 raw / 126 gzip: a director decision recorded in the handoff). Report exact commands and exit codes; do not pipe a
gate in a way that hides its exit code.

REPORT: per finding severity (blocker / should-fix / note), file:line, invariant, reproduction, suggested fix; what you
checked and found clean; what needs a live session. Verdict: approve, approve with fixes, or reject.
~~~
