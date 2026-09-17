# Forge Next — final input verification before implementation

**Status:** VERIFIED FOR PHASE-0 CONTRACT WITH EXPLICIT SUPERSEDING NOTES
**Date:** 2026-09-16
**Repository:** `perseverance484/tnr-tools`
**Reviewer:** ChatGPT — Engineering Auditor, supporting Release Auditor lens
**Operational `main` observed:** `b42c2afd5ceb3cd2e1f1eaa6f1e082cfc419cbea`
**Live-game requests/writes:** none

## 1. Frozen inputs verified

### Quest Studio

- accepted implementation: `chatgpt/forge-quest-studio-foundation@5ba636d85fe2dbd4e4bf0e2baa6070cdd7321b15`
- final independent review: `claude/quest-studio-final-review@82bb686370f3f8cbbe57068fe42b887c90fdf48d`
- verdict: `APPROVE_WITH_NONBLOCKING_FOLLOWUP`

The final review independently reproduced 315/315 Forge tests with zero failures/cancellations on Node 22 while CI reproduced 315/315 on Node 24, and it closed the prior F1/F2/F5 findings. The accepted slice is sufficient as a downstream integration input.

### Forge Next planning

- reconciled planning package: `claude/forge-next-planning-reconciled@ba51a28a99a7748e61de0c2768bd73ab9c65c856`
- parent planning package: `claude/forge-next-planning-v3frzi@22f1fc43f8e316d0ec8412d5595a7cd0936f98d0`

The reconciliation correctly points to the accepted Quest Studio SHA, records source-push with a Contents-only browser credential, carries the Workflows-write security invariant, preserves the ForgeCore architecture and just-in-time decision model, and retains the repository-only Studio rehearsal gate.

## 2. Superseding notes that implementation must use

These are documentation/reconciliation mismatches, not architecture blockers. They must not be silently inherited by an implementation brief.

### V1 — K-26 director half is already settled

`K_USER_DECISIONS.md` still labels K-26 "OPEN, now ratify or revert", and `G_ROADMAP.md` still lists K-26's director half as a Studio-phase precondition.

That is stale relative to the director ruling already implemented and reviewed:

- `RUL-2026-09-16-002` fixes the operator-device repository credential to **Contents: write only**;
- **Actions write is not allowed**;
- **Workflows write is not allowed**;
- source-push is the accepted initial trigger model that satisfies that scope.

The engineering details of branch retention, run observability and later transport replacement remain engineering work. The director credential-scope half is closed and must not be re-asked.

### V2 — evidence-summary generator wording is still overstated

The planning handoff still says `docs/forge_next/evidence/gen_evidence_summary.py` regenerates both matrices' summary strings.

The script actually:

- regenerates the prose `summary` and tally metadata for `parity-matrix.json`;
- updates `verification.method` and `verification.scope_note` for `admin-feasibility.json`;
- does **not** regenerate an admin-matrix prose summary string.

Implementation may rely on the evidence rows and verification metadata, but must not repeat the broader producer claim.

### V3 — the accepted Quest Studio does have manifest-digest binding

`00_CONTEXT.md` still carries an older architectural criticism that the Studio result has "no manifest hash in the envelope".

That is stale at the accepted SHA. `quest_compile.py` computes SHA-256 over the generated manifest and emits `generated.manifestSha256`; `forge/src/studio/repository.mjs` requires a 64-hex digest, re-hashes the fetched manifest, and refuses a mismatch.

Any later promotion contract must preserve this binding rather than re-invent it.

## 3. Current-main divergence

The accepted Quest Studio tree and current operational `main` diverge at merge-base `305a28f992e33194fbba279a3f32e698dfb2b67f`.

At verification time the accepted Studio is 40 commits behind current `main` and contains a large design/implementation history not present on `main`. It must **not** be merged wholesale merely to begin Phase 0.

The reviewed Studio SHA remains the evidence/reference target. Its eventual integration requires a deliberate fresh-main reconciliation that preserves at least:

- `RUL-2026-09-16-001` from current `main`;
- `RUL-2026-09-16-002` from the accepted Studio line;
- the reviewed source-push trust boundary;
- manifest-digest binding;
- exact source-revision correlation;
- the final review's nonblocking follow-ups.

## 4. Upstream game-source observation

Public `studie-tech/TheNinjaRPG` `main` was observed at `1fd355ab92cec78148130e02c8d38834836c3181` while this verification was written.

This is an observation, not a Phase-0 pin. The Phase-0 implementer must re-verify the upstream head at task start and rerun the planning package's required Forge-relevance drift check. Phase 0 measures drift; it does not silently adopt source changes or move generated-contract pins.

## 5. Verdict

The two frozen workstreams are sufficient to author the unified Phase-0 implementation contract.

The reconciled planning branch is not treated as literal truth where V1-V3 above contradict later reviewed evidence. Those notes are explicit contract inputs, not silent edits to Fable's frozen planning branch.

Phase 0 may begin after the implementation owner verifies fresh `main` and creates a Fable-owned branch. It has no director-decision blocker and must make no live-game request or write.
