# Bloodright follow-up: CONFIRMED-item recovery

The user supplied Claude Code's independent follow-up review on 2026-10-08.
It reviewed PR #29 at `d2cf853f5461e06ad5233f83c5dc9de2cb28b5d5` and PR #30
at `f74da803d0c0d36eefc13fa5fb1a084ddc754412`, against game source
`1ccdaf078a58101872675e459c8e755b495d4c83`. The review closed R1–R4 and verified
the raw-manifest guards and BEE package, but identified N1 (medium): a CONFIRMED
item could permanently block another same-bloodline job without an operator recovery path.

## Correction

Paused or incomplete jobs now offer **Mark failed (leave as is)** for each CONFIRMED
Bloodright item. The operator must confirm. The action uses the existing CONFIRMED → FAILED
transition; it never treats an unverified write as successful, retries it, or deletes a record.
The journal retains its target ID, timestamps, drift details and verification status, and adds
an explicit operator-resolution record. Exports retain that evidence. Known bindings are kept;
a missing binding is recovered from the confirmed ID without overwriting a newer binding.

The action refuses any SENT item in the job, a running job, non-CONFIRMED/non-Bloodright items,
and an active other-tab lease. The core also refuses while any local job is running.
Lease scope is recovered from persisted job provenance after reload, so recovery does not
require attaching the frozen manifest or lose its bloodline lease. The UI disables recovery
when confirmation is unavailable or SENT items remain. No transition table was relaxed.

Dependent items in the old job still require verified parents. A fresh preview becomes possible
after all unresolved obligations are resolved, and captures the current preimages. A deleted
target still requires explicit binding repair: failure resolution does not erase its saved ID
or grant permission to create a replacement. Temporary visibility loss can still be resumed.

## Verification

The drift regression first reproduced the prior lockout: skipped CONFIRMED item refused,
new preparation blocked, no operator-resolution method available. The correction has four
new regression tests covering drift, permanent target loss/reload, guards/lease ownership,
and the UI's cancel/confirm/export behavior. Tests also verify zero recovery requests,
preserved drift/IDs, continued parent blocking and a fresh preview with the changed preimage.

Author validation (Node 24.19.0, full history):

- `npm test`: **559 passed**, zero failures/skips; 35 Bloodright tests and the new UI recovery test.
- Import and boundary checks: zero violations; core public-action contract updated deliberately.
- Repeated builds: SHA-256 `01f752e46e749050e115da7d5638c863ccf3ec708ca966a715c47ce167b70fa8`.
- Bundle budget: **377,733 raw / 85,355 gzip**, within the unchanged proposed 386,000 / 88,000 limits.
- `npm run fixtures`: existing fixtures unchanged. Release-pin check clean; skill ZIP unchanged.
- Pinned Bloodright contract derivation: byte-identical.
- Doctrine map, doctrine projection and pack checks: passed. `git diff --check`: clean.

The new exact frozen SHA and CI results are supplied in the PR handoff. Original
independent review verdicts apply only to their original SHAs; this is an author correction
requiring focused independent re-verification.

## Content and release boundaries

PR #30 retains the user-approved 20 Silver / 99 rounds for all 12 BEE nodes and 17 effects.
Generated descriptions, existing-folder visibility and the proposed bundle-budget increase
remain separate user decisions. No game requests, staff/browser session, merge to main,
release or pilot execution occurred. The loader remains 0.5.1, with 0.6.0 pending.
