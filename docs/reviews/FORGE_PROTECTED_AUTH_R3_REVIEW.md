# Forge protected-auth independent review — round 3

**Repository:** `perseverance484/tnr-tools`  
**Implementation branch:** `fable/forge-protected-auth`  
**Intended base:** `2855825ca215b48c1b04522c2a40948dd8cefe02`  
**Previous rejected head:** `3b6c566eef5459fe16f104d5ee21accbc4e0f6c8`  
**Reviewed frozen head:** `e2bab901cdcab15018a80eadefefe64ae565d0e5`  
**Review branch:** `chatgpt/review-forge-protected-auth-r3`  
**Verdict:** APPROVED / ready for integration and release workflow

## Scope

This is the narrow round-3 review authorized by `FORGE_PROTECTED_AUTH_R2_REVIEW.md`: the two surviving FPA-2 SESSION paths plus the carrier-source documentation correction. Current `main` remains the intended base and the Fable branch is one commit ahead of the round-2 target. No live-game request or write was made.

## FPA-2 path A — CLOSED

Both protected `profile.getAi` reads inside `Runner._rules()` now classify a SESSION result through `Runner._authRefused()`.

- Before profile toggle: a server `UNAUTHORIZED` invalidates shared auth and pauses without terminalizing the item.
- After a successful `ai.toggleAiProfile`: a server `UNAUTHORIZED` leaves the item `CONFIRMED` at phase `rules`, so no rules write is sent against the dead session and a later successful auth re-check can resume from the exact remaining step.

This closes the half-configured-AI failure identified in round 2 and is directly applicable to One Perfect Crop's AI/profile build path.

The new targeted tests exercise refusal before toggle, refusal after a landed toggle, zero additional protected work before a successful re-check, and successful completion afterward.

## FPA-2 path B — CLOSED

Reconciliation now distinguishes a server-proven SESSION failure from an ordinary unreadable/ambiguous record.

`Reconciler._ensureSession()` wraps its read sites and raises `AuthRefused` only for SESSION. `Runner.resume()` catches that condition, invalidates the shared auth state, pauses, and leaves the SENT item untouched. It therefore does not manufacture an `ORPHANED` adopt/skip decision merely because the operator's session expired between the resume gate and the reconciliation read.

The targeted reconciliation regression leaves the item SENT, never ORPHANED, and records a SESSION pause. This preserves the existing mutation-ambiguity contract while making auth interruption recoverable.

## FPA-3 documentation correction — CLOSED

The pin-reconciliation note now distinguishes server routing from client navigation correctly:

- `/` is a valid route under the root provider tree;
- `proxy.ts` does not server-redirect the signed-in operator;
- `HomeLanding.tsx` may client-navigate after hydration, including to `/profile`;
- that client route change stays within the same document/root provider context and Forge's overlay is outside the Next root.

The residual fact that the eventual carrier page may have its own game traffic is explicitly left for the live smoke rather than presented as source-proven harmlessness.

## Round-3 adversarial checks

I tried to refute the fixes against the exact frozen source rather than relying on the handoff summary.

- `AuthRefused` carries only path + decoded error and does not gain direct access to credentials or auth state.
- `_rules()` throws the existing `Paused` result from `_authRefused()`, so `_runItem()` does not fall through to its terminal ordinary-failure transition.
- The post-toggle item is transitioned to `CONFIRMED/rules` before the second `profile.getAi`, which makes that state safely resumable after re-auth.
- `resume()` catches `AuthRefused` before generic reconciliation failure handling; `_pause()` remains the owner of lease release.
- Reconciliation's other non-SESSION failures retain their pre-existing ORPHANED behavior.
- No carrier/session architecture, procedure-table semantics, credential model, or journal state model changed in round 3.

No surviving integration blocker was found in the authorized review surface.

## Gates and limits of this review

Fable reports:

- `npm test`: 293/293 pass;
- deterministic source build / checked-in bundle equivalence;
- fixtures no diff;
- release-pin check green;
- dual-pin auth comparison exit 0;
- doctrine/packs/doctrinemap exit 0;
- lawmap 0 errors / 5 baseline warnings.

This review environment inspected the exact implementation and targeted tests but did not independently execute those local npm/build commands. Browser/Violentmonkey/real-Clerk behavior remains intentionally unverified until the post-release operator smoke defined by the task brief.

## Integration and first live verification

The reviewed SHA is ready for normal Lane A integration because the confirmed blockers are closed and `main` still matches the intended base.

After integration, use the existing Forge release-pin workflow rather than manually rewriting the immutable loader pin. The first real production-session verification remains read-only:

`push/04_one_perfect_crop_bandit_ai_probe.json`

Expected result: 5/5 `profile.getAi` reads succeed, 5/5 requested full bodies persist, zero mutations. A successful read-only smoke is the gate before One Perfect Crop proceeds to any protected content write.
