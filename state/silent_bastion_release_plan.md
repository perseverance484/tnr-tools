# Silent Bastion — release-design plan (proposal)

**Status:** DESIGN / NOT RELEASE-READY. This is planning evidence, not an approved build manifest, approved combat balance, validated quest graph, or authorization for a live request/write.
**Owner:** ChatGPT (design/audit); Fable/Claude Code (normal implementation and offline tests); dauntless (balance, rewards, final player-facing copy/art acceptance, all live actions and publication).
**Repository planning refs (2026-10-14):** `main@1da18301e8e4660cedf3daa3e80893a2ac918f2b`; `chatgpt/silent-bastion-design-20261013@9252025a55784b8919d0a92556f55c1cbce42b7e` before this document; merge-base `057acddb986b50e486ccf550fac00b68fff51490`.
**Game source:** `studie-tech/TheNinjaRPG@c82dc7f8ee76cb9ac498c0689f71b6f13bfe69dd` for reviewed authoring schemas/quest runtime, with earlier pinned design analysis at `67341a1fa1567b9b33827b802e48120e5d797a15`. Re-verify game source and registry before manifest construction.
**Authorities:** `docs/00_INDEX.md`, `docs/DOCTRINE.md`, `docs/ENGINE_LAWS.md`, `docs/workflows/CONTENT_WORKSTREAM.md` (on current main), `docs/DEVELOPMENT_WORKFLOW.md`, `skills/building-tnr-content/references/{quest,ai,balance,item}.md`; current proposals in `state/silent_bastion_design.md`, `state/silent_bastion_commander_roster.md`, `state/silent_bastion_arakane_ai_profile.md`.

## 1. Event contract to preserve

- **Title:** Ghost Ship: The Last Directive. **Location:** Silent Bastion, mountain headquarters of the Skyglass Project, accessed by **one Skyglass Signal Beacon** obtained through Ghost Ship.
- **One new isolated `battlepyramid` quest**, not five quests; five divisions × (four regular encounters + one division commander) = **25 fights on a full route** or **20 fights using five shortcuts**. Four mandatory dialogs/gates per five-fight sequence must be structurally protected.
- **Player pools carry** after all ordinary wins and all successful division transitions. No free full recovery.
- After the third regular fight, **Maintenance Passage** skips the fourth on success; on a wrong answer it still skips the fourth but adds temporary **Security Alert** for the boss. **Medical Protocol** requires fighting the fourth, then sets all HP/CP/SP to 75% of maximum at the boss start (can lower a higher pool). **Combat Protocol** requires fighting the fourth, then applies its temporary combat buff **to the player** at the commander battle start; no recovery. All numbers/effects await director balance freeze.
- Loss during fights 1–24 should restart **the same division from its first regular encounter**, with **50% HP/CP/SP** and no additional Beacon. Loss to final Arakane or abandonment ends the full run. The event must not silently change any of these rules to fit tooling.
- The final reveal is that new military orders arrive **after Arakane is defeated**; do not reveal the unknown issuer earlier. Preserved chakra impressions are reconstruction, not undead.
- All five commanders have approved innate **Seal Prevent 100 / 99 rounds** against standard bloodline Seal (not generic control immunity). Gatewarden is the accepted name; Garrison Marshal is superseded.
- Every created/updated live entity is staged `hidden:true`, then requires separate dauntless-controlled verified game write and operator/content-admin publication decision.

## 2. Intended quest graph; implementation NOT yet proved

```text
D_i entry -> D_i fight1 -> B_i1 -> D_i fight2 -> B_i2 -> D_i fight3 -> B_i3
  -> D_i terminal
     ├─ Maintenance puzzle
     │    ├─ correct -> D_i boss_clean -> B_i boss_clean
     │    └─ wrong   -> D_i boss_alert -> B_i boss_alert [applyDebuffs]
     ├─ Medical -> D_i fight4_med -> B_i4_med -> D_i boss_med
     │             -> B_i boss_med [givePools=75]
     └─ Combat  -> D_i fight4_combat -> B_i4_combat -> D_i boss_combat
                   -> B_i boss_combat [applyBuffs]
  -> (after winning exactly one boss variant) -> next division D_(i+1) entry,
     or final aftermath and one win_quest at division V.
```

Every `start_battle` must be immediately dialog-gated. Branch-specific boss battle nodes may be needed because `givePools` / `applyBuffs` / `applyDebuffs` are authored on the battle objective and no branch-local temporary variable is proven. Duplicate battle nodes **must not** duplicate rewards or allow parallel objectives. Every losing battle must have a fail edge. Scope is one boss encounter per chosen branch, not multiple bosses. The five unique puzzles each offer exactly three logically solvable choices and explicit outcome feedback; themes are patrol routing, armory safety, original-vs-replica, authorization, and contradictory orders.

**Feasibility blocker: 50%-only-on-retry.** `givePools` is set on a battle start, not on `reset_quest`; attaching 50% to the ordinary division opening would overwrite carried pools after a clean division win. The native reset/branch flow must be modeled and offline-proven to apply 50% only after a defeat, across repeated retries, without offering a free recovery branch. Do not claim this is solved by a generic reset pointer. If not authorable in the existing runtime, report an explicit engine gap and a user-owned design/code decision before implementation.

**Source evidence:** `app/src/validators/objectives.ts` supports optional `givePools` 0–100 and `applyBuffs` / `applyDebuffs` for battle objectives; `app/src/libs/quest.ts` carries these to combat; `app/src/server/api/routers/combat.ts` applies them to initiating human players, not to the AI. Missing `givePools` preserves carry. Quest guide §3.7 requires dialog-gated individual battle actions and correct fail/reset graph edges. One entry-item payment at first battle is tracked via `entryPaid` and still needs run/retry regression tests.

## 3. Content production packets and open gates

| Packet | Minimum artifact and acceptance gate | Present status |
| --- | --- | --- |
| **A. Engine feasibility + quest graph** | Deterministic 5-division branch graph; precise checkpoint-loss and terminal semantics; fail/abandon/Beacon-once tests; exactly one root and one successful ending; no premature fight or reward. | **NEXT / unproven** |
| **B. Terminal puzzles and protocols** | Five authored three-choice puzzles, correct/wrong feedback, route-specific boss start effects and Security Alert; sign-off on each buff. | Design direction accepted; exact values conflicting/unapproved. |
| **C. Regular opponents** | Four encounter slots per division = 20 regular fights; choose unique-versus-reused AI templates, role/kit/difficulty escalation, no excessive lockout or accidental AI loot. | Not authored. Proposal: 2 complementary regular templates per division, reused intentionally if approved. |
| **D. Commander data** | Five complete kits, caps-compliant ordered AI rules, native range gates, fallbacks, stats/multipliers/pools, gear and deterministic offline combat fixtures. | Gatewarden 6, Master of Arms 10, Replicant Zero 11, Arakane 14 memberships accepted; Grand Marshal 12-move roster still a candidate. Most executable rules untested. |
| **E. Entry + rewards** | One Beacon item and approved Ghost Ship source/rate; pyramid completion reward/loot, limits, availability/expiry; no unintended floor farming; test 100-cap constraints. | All economy numbers and reward content open; fresh source/captures required before altering Ghost Ship. |
| **F. Narrative + visual assets** | Entry/terminal/puzzle/boss transitions, end reveal, accepted Skyglass-consistent Bastion scenes, item/jutsu icons and enemy avatars; art spec/processing/preview gates. | Concept only; no Bastion art production acceptance. |
| **G. Build and independent review** | Fable's reproducible exact-schema manifests, contract checks, graph validator, native AI fixtures, preflight/harvest plan, ChatGPT exact-SHA independent audit. | Blocked by A–F. |
| **H. Hidden deployment and publication** | Fresh full captures; `hidden:true` writes performed **only** by dauntless, read-back by approved operator workflow, subsequent explicit director/admin publication approval. | Not authorized. |

The newly integrated workstream orchestration at `docs/workflows/CONTENT_WORKSTREAM.md` should coordinate these sessions after the design branch is meaningfully synchronized with `main` and `scripts/content_workstream.py validate/render` can run. Do **not** fabricate a generated roadmap projection by hand.

## 4. Important contradictions to resolve before player-facing freeze

1. **Combat Protocol disagreement:** The latest Discord block presents player buffs (I DDT20/3r; II Stun Prevent100/2r; III IDG25/3r; IV Seal Prevent100/2r; V Clear Prevent100/3r); `state/silent_bastion_commander_roster.md` instead labels I defense, II offensive IDG, III shield, IV Seal Prevent and V unspecified. Public-copy approval is not automatically a balance freeze. Choose one set through explicit director approval and update its owning design source.
2. **Arakane protocol is currently not authorable as proposed:** at game `c82dc7f8`, `app/src/validators/combat.ts` `questBuffTypes` includes `decreasedamagetaken`, `stunprevent`, `increasedamagegiven`, `sealprevent`, `debuffprevent`, but **excludes `clearprevent`**, even though Clear Prevent exists as a general combat tag. `applyBuffs` therefore rejects the advertised 100% Clear Prevent3r. Options require director choice: replace with a supported and thematically useful buff, or commission a separately reviewed game-code contract change; do not silently emit unsupported tag.
3. **Division IV's Seal Prevent is not redundant with boss immunity:** boss innate protects **the boss**, whereas Combat Protocol applies to **the player**. The roster's redundancy claim mixes targets and is incorrect.
4. **Commander specifics still open:** Grand Marshal roster/20-rule implementation, Arakane's two historic-seed weapons and Countermand item, Tempest Cleave's real current record, Arakane exclusive names/AP/CD/range/proc powers, 20-rule Final Stand gating/Stealth action economy, numerical difficulty and attrition tests. Strong double-IDG/DDG effects must be evaluated multiplicatively.
5. **Quest release timing/limits:** `maxAttempts` and `maxCompletes` cap at 100 in the current validator; the director must choose intended lifetime repeatability/availability and Beacon scarcity. No default maximum should accidentally block the event.

## 5. Next director-facing decision

**First:** agree to run a narrow **A: offline quest-feasibility spike** before writing rewards or commissioning the full AI/art roster. This spike must prove (or explicitly fail) the 50%-only-on-retry checkpoint and four boss-route variants using the pinned runtime; the output becomes the structural contract for Fable. In parallel, request a director decision on the Arakane Combat Protocol alternative and whether the Discord list is a working buff proposal or is intended as a numeric freeze.

**No live requests, credentials, game writes, manifest generation, art production, publication, or production readiness are implied by this plan.**
