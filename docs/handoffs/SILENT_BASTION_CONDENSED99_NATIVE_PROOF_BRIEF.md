# Ghost Ship: The Last Directive — 99-node native proof and authoring gate

**Status:** DIRECTOR-SELECTED DESIGN / NATIVE OFFLINE PROOF REQUIRED. Scope authorized for offline proof and future content drafting only; NOT approval of a generated manifest, balance, rewards, art or publication.

## Repository and ownership

- Repository: `perseverance484/tnr-tools`.
- Director-approved scope ruling: `docs/RULINGS.md`, **RUL-2026-10-15-001**; operative design `state/silent_bastion_design.md`.
- Design candidate: `state/silent_bastion_condensed99_candidate.json` — **99 objective nodes**, source-mirrored structural checks only (not native tested).
- Prior proof: `claude/silent-bastion-phase1-validation-9628h6@33be3cd2fe504d508ade2ab04d15e45f4c752ed3`, `harness/silent_bastion_phase1/` and `docs/reviews/SILENT_BASTION_PHASE1_NATIVE_RESULTS.md`. Prior 178-node r2 proof is regression reference, **not** proof for the 99-node design.
- Planning branch: `chatgpt/silent-bastion-node-budget-20261015` (verify live head before starting; do not infer SHA from branch name).
- Main at last inspection: `43ce6b2d22736cd90e3de52e66f620570e67888f`. Upstream game at last inspection: `studie-tech/TheNinjaRPG@13d40c4c1509ecf44262aba1b5120266011ea786`. Verify both at start and pin the actual test version; the previous proof ran at `c82dc7f8ee76cb9ac498c0689f71b6f13bfe69dd`.
- One writer: **Fable** on a separate `claude/*` or `fable/*` branch; ChatGPT independently reviews frozen exact head SHA. Never write Fable's Phase1 validation branch or main as part of this proof.

## Exact gameplay and story contract

The facility's exterior appears **abandoned and undefended**. No exterior sentries, garrison patrols or gatekeeper encounter. **The Gatewarden / Outer Garrison and its patrol puzzle are removed** from this Pyramid; do not recycle him as an interior mandatory fight.

Player-facing divisions are **I Experimental Armory, II Skyglass Research, III High Command, IV Command Sanctum**. Internal symbolic IDs remain **D2–D5** to preserve provenance during proof. Each division still includes four regular encounter slots + its original commander (20 distinct opponents total), three mandatory regular fights, a terminal and one security puzzle, one optional fourth regular, and its commander. **16–20 actual fights per victorious run**. Four puzzles: armory disable sequence, original-vs-replica, authorization, contradictory directives. No exposed unknown command issuer before Arakane's defeat; the first three surviving commanders' identities and all accepted kits survive unchanged.

Terminal structure: Maintenance puzzle correct → clean boss, wrong → same shortcut + player-side Security Alert. Fighting the fourth regular → a **post-fight** protocol-choice dialog → Medical sets player HP/CP/SP to **100% at commander battle** (`givePools:100`) or Combat gives **player-side** temporary buff at commander. All explicit Combat numbers and Security Alert strength remain candidate until director signoff.

Every ordinary victory carries pools into the next fight and division; **loss at any ordinary fight or one of the first three commanders** must return to the **same division's first regular enemy at 50% HP/CP/SP** and use no extra Beacon. Loss to Arakane hard-fails the Pyramid. One Beacon charged at the first initiated fight, not merely quest start. Exactly one reward at completion; repeated defeats do not refund payment.

## 99-node structure and the exact problem to prove

Candidate count: **45 dialogs, 40 start_battle nodes, 12 reset_quest nodes, one win and one fail = 99**. The 40 battle nodes represent **20 unique opponent slots** including route variants.

Each retained division carries its normal forward path plus two recovery-fight templates:
1. First regular loses → `dN.lost_first` dialog → `bN.recovery_first` REG1 copy with `givePools:50`. Recovery WIN proceeds directly to `dN.n.f2`; recovery LOSS enters `rN.reset_first` reset to `dN.lost_first`.
2. A later regular or nonfinal commander loses → `dN.lost_later` dialog → `bN.recovery_later` REG1 copy with `givePools:50`. Recovery WIN triggers `rN.reset_later_win` reset target `dN.n.f2` (**already visited**, avoiding a forward graph cycle); recovery LOSS triggers `rN.reset_later_loss` reset target `dN.lost_later`.
3. Arakane LOSS → `f.arakane` terminal, no reset.

All ordinary `nextObjectiveId` and `failObjectiveId` edges are acyclic; **only the `resetObjectiveId` field encodes a logical rewind**. The question is whether the engine tracker/cursor actually reactivates the intended `dN.n.f2` after the recovery WIN→reset, with no incorrect stale done state or automatic fight skip. This is **not yet behavior-proven**.

## Required native offline proof

- Verify pinned game-source semantics (latest `app/src/libs/quest.ts` `applyQuestResets`, `getNewTrackers`, `app/src/libs/objectives.ts`, validators/routers and current QuestValidator), then update the existing Phase1 fixture compiler **only** to map the new symbolic shape (`resetTarget`, `startPoolsPercent`, extra recovery nodes). Do **not** patch the game source or implement new engine fields.
- Run `verifyQuestObjectiveFlow`, `verifyQuestContentForSave`, QuestValidator, graph single-root/reachability/no-cycles, and full objective save on the complete 99-node fixture. All battles must have dialogue predecessors (including the post-fourth-fight protocol choice).
- Prove each of four divisions: initial REG1 loss; two consecutive recovery REG1 losses; recovery win and return to REG2; defeat at REG2/3/4; defeat on **each** clean, Security Alert, Medical and Combat boss variant; recovery success returning to REG2 via `reset_quest`; multiple subsequent failures/retries without stale progress or wrong division reset. Test with earlier divisions fully completed and verify they are never reset.
- Verify effective pools through actual router-driven start/settle flow: exactly 50% at each recovery fight start, after the recovery WIN the **actual end-of-fight pools carry** into REG2 (not another automatic set-to-50), normal division transitions carry, and Medical commander sets 100% only on selection. Check counterparty does not receive player-side protocol effects.
- Verify 16–20 battles per clean run, one commander each division, no duplicate boss starts, correct opponent IDs, no premature terminal/reward, Beacon consumed exactly once, Arakane defeat closes attempt and releases isolation, replay doesn't pay final reward twice. Recheck F1/F2 entry-item anomaly, F3 repetitive battle settlement income, F4/F5 dialogue disclosure as applicable.
- Restore/resume after pause and quest version edit; consider Logbook client active objective after reset (source and/or local browser proof). A no-Beacon run must not be misreported as verified successful.
- Record exact runner commands, upstream SHA, test counts, deterministic re-run, SHA-256 input provenance and findings in `docs/reviews/SILENT_BASTION_CONDENSED99_NATIVE_RESULTS.md` and update or separate harness and graph compilation artifacts. No source change to `studie-tech/TheNinjaRPG`.

## Pass/fail decision

**PASS:** all intended routes, resets, pools, gate effects and invariants hold under the real pinned runtime. Then update the one-shot content-authoring plan to **4 divisions, 16 regular AIs + four commanders, four puzzles, all 99 objective texts** and finish content drafts with the previously approved design values and new **deserted exterior** staging. All balance/economy/art still require director sign-off. Do not create clickable production manifests under `push/` or publish.

**FAIL:** report minimal reproducible failure and which native contract blocks it. Explore alternative **content-only** arrangements within 100 nodes. Do **not** ask for or perform engine modifications, conceal a failed test, or silently cut another commander or puzzle. Return options for director acceptance first.

**Integration caveat:** branch `docs/RULINGS.md` at Phase1 design contains `RUL-2026-10-14-001` for Medical100; current main contains the same numeric ID for an unrelated art ruling. **Flag this historical ID collision for explicit reconciliation** at integration rather than treating either unrelated ruling as a replacement. Neither automatic overwrite nor accidental duplicate ID is acceptable.

**Safety:** Live-game requests **0**, writes **0**, credentials **none**, engine modifications **0**. No live game state, real deployment, rewards or publication touched by this handoff.
