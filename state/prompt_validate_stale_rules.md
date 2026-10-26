# Build brief: retire two stale validation rules (Lane A)

- **Ruling:** RUL-2026-10-25-009 (director, 2026-10-25). Context: RUL-2026-10-25-008.
- **Branch:** `fable/validate-stale-rules` from current `main`. One writer. Independent ChatGPT review of a frozen SHA
  (`docs/workflows/IMPLEMENTATION_HANDOFF.md`, `docs/workflows/FABLE_REVIEW.md`).
- **Game source:** read, never run. Use the pins the repository's generated contracts already use (`forge/src/runner/
  nested.json` and `fields.json` `_meta.pin`); cite file and line at that pin. Confirm upstream `main` has not changed
  the cited schemas.
- **Live-game requests:** 0. No credentials.

## Problem

`skills/building-tnr-content/scripts/validate.py --strict` (the mandatory manifest gate) disagrees with the game's own
schemas and with Forge in two places, so correct manifests fail the gate and only run under one-off exceptions
(push/261, push/262):

1. **L06 on `wound`.** validate.py (`LFORM` check, about line 1035) and Forge `forge/src/runner/lints.mjs`
   (`FORMULA_TAGS`, about line 29/97) demand both `statTypes` and `generalTypes` on `damage`, `pierce` and `wound`.
   The game's `WoundTag` (`app/src/validators/combat.ts`) spreads `IncludeGeneralsAndElements` only: it has
   `generalTypes`, no `statTypes`, and `calculation` is `percentage` only. A manifest that sends `statTypes` on a wound
   is refused by Forge's pre-send key check ("the server's validator would drop it silently"); one that omits it fails
   validate.py.
2. **Law 14 / L05 `preferredStat`.** validate.py `AI_CREATE_REQUIRED` and `check_ai_create` (about lines 488 and
   699-713) require `preferredStat` on every AI create. Upstream migration 0056 dropped the column; Forge already
   stopped requiring it (`forge/src/runner/lints.mjs` comment at line 25; `forge/test/post0056.test.mjs`), and refuses
   the key as unknown. `docs/ENGINE_LAWS.md` law 14 and `skills/building-tnr-content/references/ai.md` (line 774, the
   §-checklist at 526) still state the old requirement.

## Scope

1. **validate.py:** L06 requires `statTypes` only on the tags whose game schema has it (derive or cite: `damage`,
   `pierce`), and `generalTypes` on all three; law 14 no longer requires or enumerates `preferredStat`. Keep every other
   requirement of law 14 (`rank`, `regeneration`, `preferredGeneral1/2`). If the per-tag key sets are available from a
   generated contract, use them rather than a hand list.
2. **Forge `lints.mjs` L06:** the same per-tag rule, so Forge and validate.py agree. Bundle rebuild, budget check, version
   bump and release-pending marker as the Forge release rules require (`docs/BUILDER_APP_NOTES.md`).
3. **Law and references:** law 14's `preferredStat` clause and any L06 wording that names `wound` + `statTypes` go
   through the law-reconciliation process (RUL-2026-09-08-004): change the canonical owner (`docs/ENGINE_LAWS.md`),
   regenerate projections with the repository tools, never hand-edit a generated projection; update
   `references/ai.md` and any routed reference that restates the rule (cite, do not proliferate: CLAUDE.md §7).
4. **Tests:** validate.py self-tests (or fixtures) proving a wound without `statTypes` and an AI create without
   `preferredStat` pass, and a damage/pierce without `statTypes` still warns; Forge tests for L06 per tag. Existing
   `post0056` tests stay green.
5. **Exceptions:** after the fix, `validate.py --strict` on push/261 and push/262 reports no diagnostics, which voids
   their ledgers by their own terms (`scripts/validate_exception.py`). Record that in the handoff; do not edit the
   ledgers.

## Out of scope

Any other lint or law; content manifests; the dungeon or suggest-mode branches; live requests.

## Gates

`npm test` in `forge/` (Node 24, full history), `npm run build` + `git diff --quiet -- forge_bundle.js`,
`check_bundle_budget.mjs`, `check_release_pin.mjs`; validate.py self-tests; `doctrinemap.py`, `render_doctrine.py
--check`, `build_packs.py --check`, `lawmap.py`; `pack_skills.py` if `skills/` changed (dist must match the skillpack
workflow); `validate.py --strict` on push/261 and push/262 shows 0 diagnostics. Report exact commands and exit codes.
Hand off per `docs/workflows/IMPLEMENTATION_HANDOFF.md` with a frozen SHA.
