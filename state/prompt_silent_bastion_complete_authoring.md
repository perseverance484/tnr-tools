# Ghost Ship: The Last Directive — one-pass complete Pyramid authoring contract

> **2026-10-16 DIRECTOR APPROVAL — NATIVE-TESTED `alt99_f4gate` SELECTED (RUL-2026-10-16-002).** The earlier `state/silent_bastion_condensed99_candidate.json` remains an archived *failed* starting candidate (native defect C1), NOT the authoring graph. Use `harness/silent_bastion_condensed99/graphs/alt99_f4gate.json` as the **selected 99-node topology**, from Fable's frozen proof `claude/silent-bastion-budget-validation-69za5u@74eeb328f05d4258056b0a1c531619ffcf852ce3` / `docs/reviews/SILENT_BASTION_CONDENSED99_NATIVE_RESULTS.md`. This variant inserts a dialog after recovery_later WIN to keep the reset from firing during the recovery battle, and folds each fourth-fight intro into its Command Terminal choice; it retains commander approach dialogs on both correct and Security Alert Maintenance paths. All four divisions, 16 regular encounter identities, four commanders, four distinct puzzles, post-fourth Medical full-heal / Combat buff, 50%-pool recovery loop, one terminal outcome, and 16–20 successful-route battles remain. Tested against game `13d40c4c1509ecf44262aba1b5120266011ea786`; require current game-source reconciliation and downstream authoring/validation, do not call it current-release-proven.
>
> **Reward direction (separate approval):** `RUL-2026-10-16-001` is recorded on `chatgpt/recipe-aligned-reward-caches-20261016@a5e92bae5ceeba3d3212ca66f157ad0f54dca335`: after successful Pyramid completion, offer a player pick of **exactly one** of Arsenal/Research native recipe-aligned caches. Native quest choice requires `content.rewardMode:"choose"`, `content.rewardPickCount:1`, and both cache item IDs in **quest-level** `content.reward.reward_items` (not objective `win_quest` rewards); verify Battle Pyramid save/claim compatibility offline on the build engine. No extra graph nodes, mid-floor drops or retry-loop cache payouts. Quantities/recipe targets/weights/rarity/trade/art/publishing remain unapproved. `alt99_f4gate` selection does **not** settle Beacon charge-timing discrepancy B1, Arakane's Combat Protocol stand-in, or other outstanding implementation gates. No game requests or writes authorized.
>


> **SUPERSEDING DIRECTOR SCOPE — 2026-10-15 (RUL-2026-10-15-001). DO NOT EXECUTE THE HISTORICAL FIVE-DIVISION / 178-NODE REQUIREMENTS BELOW AS WRITTEN.** The selected project is **four full interior divisions**, 16 regular encounter identities + 4 commanders, 4 Security puzzles, and **16–20 actual battles** per winning run; no visible exterior defenses or Gatewarden battle. **99-node graph candidate**: `state/silent_bastion_condensed99_candidate.json`. Play-facing I–IV map to source `d2`–`d5`. The authored four regular encounters in each division, post-fourth-fight protocol (Medical: full `givePools:100`; Combat: player buff), Maintenance bypass/alert, first-fight Beacon payment, carry-forward pools, 50%-pool replay, and Arakane failure remain unchanged. The recovery fight's `reset_quest` bridge is **NOT NATIVE VALIDATED**; first run the scoped offline proof in `docs/handoffs/SILENT_BASTION_CONDENSED99_NATIVE_PROOF_BRIEF.md`. Only after passing this gate may Fable proceed with four-division content drafting. If native proof fails, report a content-only fallback for director decision; no engine changes. All old counts of five divisions/20 regular enemies/25 encounters/91 dialogs/178 nodes below are **historical, not authoring targets**. No game writes or publication.
>

**Status:** DIRECTOR-REQUESTED EXECUTION PLAN / NOT CONTENT ACCEPTANCE OR RELEASE AUTHORIZATION. One comprehensive **offline draft-authoring pass**. The director reports one minor Phase 1 validation issue will be fixed separately; assume a correction will arrive, **continue Phase 2 authoring now**, and require evidence of the correction before final integration. Do not silently certify Phase 1 or rewrite its known findings.
**Lead implementation:** Fable / Claude Code, on a **new `claude/*` or `fable/*` authoring branch**, sole writer. **Independent reviewer:** ChatGPT after frozen-SHA handoff. **Director:** final balance, economy, rewards, content acceptance, art, publication, and every live-game action.
**Repository:** `perseverance484/tnr-tools`.
**Authoring-plan base:** frozen Fable Phase 1 r3 `33be3cd2fe504d508ade2ab04d15e45f4c752ed3`, `claude/silent-bastion-phase1-validation-9628h6`. The plan lives on its **own ChatGPT planning branch**, not on Fable's branch. At plan authoring, `main@83690aa7394e3253e1a3860b81bba0a0641577fe` (diverged from Phase 1), and current game source `studie-tech/TheNinjaRPG@56e45fab2c87fe9d50c9beba519b616955e5c329`.
**Native Phase 1 proof engine:** `studie-tech/TheNinjaRPG@c82dc7f8ee76cb9ac498c0689f71b6f13bfe69dd`. Upstream has moved **54 commits** by plan authoring, including quests, objectives, combat, and validators. Reconcile engine differences and re-run targeted native gates on the **actual build pin**, rather than claiming c82 proof covers 56e automatically.

## 0 — Read, reconcile, and retain ownership

Read `state/active-context.md`, `state/status.json`, `docs/00_INDEX.md`, `docs/RULINGS.md`, `docs/DOCTRINE.md`, `docs/ENGINE_LAWS.md`, `CHATGPT.md`, `docs/DEVELOPMENT_WORKFLOW.md`, `docs/agents/README.md`, `docs/agents/CONTENT_DESIGNER.md`, `docs/workflows/CONTENT_WORKSTREAM.md`, and routed `skills/building-tnr-content/references/{quest,ai,jutsu,item,balance,pipeline}.md`. Read the full, exact following sources before generating any content:

- `state/silent_bastion_design.md` (accepted story, terminal, combat themes).
- `state/silent_bastion_commander_roster.md` (all five bosses, exact selected shared-pool moves, candidate AI concepts).
- `state/silent_bastion_arakane_ai_profile.md` (20-rule Arakane proposal and Stealth equipment).
- `state/silent_bastion_release_plan.md` (owner decisions and source contradictions; some historic paragraphs are superseded).
- `state/silent_bastion_phase1_graph.json` **r2** (178 nodes; native-tested structure).
- `docs/RULINGS.md#RUL-2026-10-14-001` (on the Fable r3 branch; authoritative director update).
- `docs/reviews/SILENT_BASTION_PHASE1_NATIVE_RESULTS.md`, `docs/handoffs/SILENT_BASTION_PHASE1_NATIVE_HANDOFF.md`, and `harness/silent_bastion_phase1/` including test output, graph compiler, and provenance.
- Current shared jutsu pool `skills/building-tnr-content/data/32b_DATA_pool.json`, relevant generated contracts/answer catalogs, Ghost Ship Skyglass AI/quest comparators and pinned game code; use captures rather than outdated answer seeds when a current live record is essential.

**Precedence/reconciliation:** treat `RUL-2026-10-14-001` as superseding all **75% Medical** text and all **protocol-before-fourth-fight** sketches. Do not merge incompatible old graphs/prose. Correct any derivative text/data to `givePools:100` and the post-fourth-fight Protocol dialog. Combat Protocol and Security Alert are **effects on the PLAYER at the commander battle start**, not the boss. Disregard older boss-buff descriptions in the roster. No undocumented "final" decisions are conferred by this plan.

**Source boundaries:** GitHub repository and pinned public game source retrievals are permitted; **zero requests to theninja-rpg.com, zero live game API calls, zero game writes, zero credentials/cookies/session**. No manifests under live-clickable `push/` before operator acceptance. Do not edit Fable's still-active Phase 1 branch or `main` as part of this work. Do not modify generated `state/active-context.md`/`state/status.json` by hand.

## 1 — Precisely preserve the Phase 1 progression contract

Use the **r2, 178-objective symbolic graph**, rather than rebuilding it from prose:
- 91 dialogs, 80 symbolic battle nodes across normal/retry lanes and route variants, 5 reset nodes, one `win_quest`, one `fail_quest`. This is **25 distinct encounter slots**, not 80 different fights; each player route sees **20–25** combats.
- Five divisions of four regular slots + one commander; exactly one commander fight per division per run. Same `D1.REG1` ... `D5.BOSS` identities used consistently across all normal/retry/terminal paths.
- Each battle is immediately preceded by a dialog or the director-approved Protocol-choice dialog; no back-to-back `start_battle` shortcuts that trigger pre-activation.
- After third regular: terminal; Maintenance passage -> one distinct 3-answer puzzle (correct: clean skip fight4; wrong A/B: still skip fight4, Security Alert player debuff), OR fight fourth regular -> **post-fight protocol dialog** -> Medical commander (HP/CP/SP set to **100%**) or Combat commander (division-specific **player** buff). **Never apply Medical/Combat effects to fight4.**
- Ordinary and commander wins carry HP/CP/SP across battles and divisions unchanged except explicitly chosen Medical. Every loss on fights 1–24 restarts the same division from the first regular fight at **50% of maximum on all three pools**; retries charge no extra Beacon. Defeat to Arakane fails the whole quest. Abandon ends attempt.
- One Skyglass Signal Beacon is consumed on the **first actually initiated battle of a new attempt**, not when opening the quest screen. Preserve entryPaid across retries; future new attempt charges again.
- One post-Arakane aftermath `d.aftermath` followed by one successful `w.complete`, with rewards exactly once. No reward/drop duplications from duplicate route-specific boss nodes.
- Preserve isolated `battlepyramid`, `consecutiveObjectives:true`, and per-battle correct AIs and fail edges. Name I commander **The Gatewarden** (not Garrison Marshal).
- Use symbolic node IDs as stable keys for all authored prose and rewards; compiling normal/retry lanes from shared content must not mutate the tested graph topology.

**Phase 1 carry-forward:** The engine-native r3 report shows normal route/retry/reward checks passing (45 tests; 73 upstream preflight). It separately records **F1** crafted-API dialog progression after a failed first battle, **F2** startQuest admission without Beacon, **F3** repeat battle XP/ryo on retry, and **F4/F5** public data access to quest/hidden text. The director anticipates repair of the reported minor issue. **Author draft content concurrently, but do not mark final build verified until the exact fix SHA, scope and relevant r3 reproducer regressions are available.** F3 is a director economy choice, not an engine test bug; F4/F5 mean the ending cannot be guaranteed secret from data-mining and must not be advertised as technically inaccessible.

## 2 — One-shot authoring scope: all remaining content, one coherent packet

Produce complete, **director-reviewable** draft content for the whole Pyramid in this pass. Do not stop after a single division or leave mechanical placeholders masquerading as finished design. Work in the following dependency order, committing logical checkpoints on the assigned Fable authoring branch. Where director-owned choices are not yet ratified, **author explicit, executable-if-accepted CANDIDATE alternatives**, document their source and impact, and separate them from LOCKED/APPROVED values. Do not interrupt with serial questions; collect a single final decision docket. An unsupported choice is a named blocker, not permission to change an accepted mechanic.

### Packet A. Five divisions / 20 regular opponents

Author **20 distinct regular encounter records** (one per `D1.REG1`...`D5.REG4`), not unlabeled placeholder fights. Each gets:
- unique credible name, visual identity, military/research role, short combat and introduction text, jutsu equipment list, attributes/generals/pools/regeneration and explicitly calculated difficulty candidate;
- **2 complementary archetypal kit families per division** to keep 20 individuals coherent and economical; variants must still be meaningfully different in role, priorities, equipment or debuffs;
- 3–6 fitting existing shared-pool techniques by verified literal ID, with a clear one-line intent and no invented tags/illegal 40AP damage; profile with <=20 native rules, range+1 gates, cooldown/affordability fallthrough and safe unconditional last action;
- progressive chip damage, AP/resource wear and situational answers **without boss-level permanent control, repeated oppressive Stun/Seal, huge sustain or sudden unsignaled lethality**. D1 is approachable and D5 difficult, but each regular must leave a plausible pool attrition trajectory; don't make regular enemies another boss roster;
- verify all 25 encounter identities map to exactly one owned AI per unique slot and the boss route variants point to the **same** intended commander AI.

Names, exact numeric stats and equipment for all 20 regulars are **new content proposals requiring director review**, not already accepted. Reuse existing pool jutsu rather than inventing an unnecessary 20 × 4 set of new spells. Flag any source-record dependency or AI drops: the director previously observed unreliable AI drops; **do not put progression-critical rewards exclusively on AI drops**.

### Packet B. Five commanders, all moves, real rule profiles and difficulty

Honor **The Gatewarden (6 moves)**, **Master of Arms (10)**, **Replicant Zero (11)**, **The Grand Marshal (12 candidate)**, and **Supreme Commander Arakane (14 + Countermand item)** from the canonical roster. Design a complete ordered **<=20-rule** profile for **each** (not only Arakane); `includeDefaultRules:false` with an explicit safe end-turn or equivalent. Preserve director-approved identities, no omitted jutsu without recorded reasons, no unsanctioned changes to approved signatures.

Mandatory behaviors:
- Gatewarden: Compression Barrier, Reflect/pierce counters, Warrior's Poise when low, introductory boss, no healing or hard-lockout.
- Master of Arms: aggressive Tempo Fracture + Sovereign Fetters; Tempest Cleave IDT35 / Afterburn30 -> Cataclysm Detonation; Sovereign Ascendance under 60% HP; anti-buff Clear; do **not** deliberately spread dangerous effects to be gentle. **Tempest Cleave is an EXISTING director-specified jutsu; its definitive live ID/record were not supplied. Do not invent one or silently use an unconfirmed seed ID.** Author a typed dependency gate until director provides/approved capture identifies the record.
- Replicant Zero: first successful human reconstruction subject, preserved impression rather than undead; Clone round2 once, Copy significant buffs, barrier/absorb/drain/heal; Second Wind below ~40%, Bulwark Charge below ~65%; test cloned AI interaction.
- Grand Marshal: title `The Second` and lore approved; 12-move suppression/positional control kit is **still a candidate**. Keep separate candidate approval, test stacking DDG60 ×2/IDT60, dual Clear shared-cooldown and no-damage setup loops, no healing unless director decides otherwise.
- Arakane: approved adaptive identity; innate Seal Prevent100/99; only one opening Apex Hunger (99-round buffs must not stack repeatedly), Copy then Countermand Clear, Pierce against shields, Veilstep anti-kiting, mixed 60AP jutsu / 40AP item turns. Approved **The Last Directive** at **HP below 30%**: Final Stand 5 rounds + IDG 5 rounds + Clear Prevent 5 rounds (IDG magnitude **open**). Exclusive **80 EP nuke + Elemental Seal2r + Cleanse Prevent2r**, **usable only while ACTUAL Final Stand is active**. `Extermination Order` remains a **working name** unless director explicitly approves it. The source `has_effect` raw-power check can misread expired statuses: a ghost Final Stand must **never** satisfy the ultimate condition; isolate/test strict phase gating, and escalate if native condition cannot ensure this.
- **Countermand** is an approved, boss-only reusable Clear item. Its power/AP/range/CD/equipped slot are still candidate fields. Historic Solar Bow + Crossbow stealth fallbacks are **proposed**; confirm exact current source IDs/equip slots/AI item behavior with approved evidence, no finite pill as sole Stealth action. Ensure final 20-rule Arakane profile's move/weapon/order fallthrough is actually valid and not blocked by item cooldown/GCD.
- Test a low-CP/SP Arakane crossing 30%, huge burst skipping threshold, high-IDG passive uncopyable buffs, Shield/Pierce and target selection in 1v1. Final Stand duration must be actually five rounds, no accidental premature nuke or endless invulnerability. No new "safety" immunity without director approval.

Complete numeric stat/pool/multiplier and ability drafts using **transparent comparator math** against approved Ghost Ship/Crowned Captain fixtures and current source damage defaults. Output a candidate table (regular tier progression, commander progression and base caps). **Do not assert final balance** or that tests against source defaults equal tuned production PvP. Mark all untouched user-owned multipliers / rewards as proposals. No default immortality/99-round offensive ramps except deliberate approved content.

### Packet C. Five puzzles, terminal, dialogue and narrative

Author **all 91 graph dialogs** with coherent, proofread player copy, keyed by exact node ID (including both normal and retry lanes). Parameterize shared narrative where appropriate and compile all 91, but ensure branch-specific text stays accurate. Include:
- separate first-contact, fourth-fight, commander approach and successful transition text for each division; short, strong mechanical feedback without decorative motivational slogans;
- five unique **three-choice, one-answer-only** logically solvable Security Override puzzles using information the player can find in **earlier accessible** scene, battle or terminal text; short question, three plausible answers, explanation/feedback for right and both wrong answers; no random passwords or dependence on unreachable art; lock to current attempt and no guess-until-correct;
- themes **patrol routing, Armory disable sequence, authentic versus reconstructed impressions, military authorization, old-versus-new order discrepancy**. Later puzzles may foreshadow the command mystery but must not prematurely expose the final issuer;
- Maintenance/Medical/Combat choices with exact approved consequences: success clean bypass, wrong bypass plus player Security Alert, fourth fight required for protocols, Medical **full heal**, Combat **PLAYER** buff. One correct branch and two incorrect branches per puzzle;
- Commander individuality: The Gatewarden (defender), Master of Arms (weapon strategist), Replicant Zero (first reconstruction subject), Grand Marshal (trusted independent right hand), Arakane (sole apparent ultimate authority);
- aftermath **only after** defeating Arakane: a **newly issued Ghost Ship directive** arrives with unknown origin; do not resolve the external issuer. Historical staff are preserved chakra imprints, not zombies. The final scene should satisfy director-approved narrative while noting engine `quests.get` can expose text outside the intended reading order.

All original IDs/edges from r2 preserved; dialogue must use supported HTML/choice shapes and meet mobile readability, explicit consequence and spelling checks. Provide a human-readable script and a deterministic compiled per-node mapping. No extra mandatory farm fight added to any shortcut.

### Packet D. Protocols, Security Alert and starting effects — keep disagreements explicit

**Approved:** Medical `givePools:100` on commander only; correct shortcut no effect; wrong shortcut short player Security Alert; Combat buff targets player at commander only. **Strengths and precise content of buffs/debuffs not yet frozen.** Produce a proposed ledger with visual and balance rationale, branch ID, target, tag, power, duration and source status.

Known **illustrative Discord values** from existing release plan (not automatically frozen):
- D1 Combat: `decreasedamagetaken`20% / 3 rounds.
- D2 Combat: `stunprevent`100 / 2 rounds.
- D3 Combat: `increasedamagegiven`25% / 3 rounds.
- D4 Combat: `sealprevent`100 / 2 rounds (**player-side**, therefore not redundant with boss immunity).
- D5 Combat: `clearprevent`100 / 3 rounds — **INVALID for quest `applyBuffs`** at the pinned c82 engine and still missing from `questBuffTypes` in the current `56e45fab` validator. Don't hand it to a validator as real content. Propose >=1 supported thematic replacement and document changed meaning; **director must approve** before release use. Optionally outline an engine change as a distinct reviewed task, not an automatic shortcut.
- Security Alert working example: player IDT10% / 2 rounds; **proposal**.
- Keep effect lifetime, valid positive/negative direction, allowed tag enum, target player/AI, power and round count tested for **all four boss routes per division, both lanes**. Each starts with exactly its intended effect/no effect; Medical is not a buff.

### Packet E. Entry item, rewards and repeat farming — candidate economy only

Draft the **Skyglass Signal Beacon** entry item, its Ghost Ship acquisition proposition(s), appearance/description, stack/trade settings and consumed-on-first-fight semantics. Draft **complete Pyramid completion reward options** (baseline + optional cache tiers/drop table where appropriate), with rarity, tradability, quantities, probability math and expected value. Provide **two clearly contrasted economy proposals** so the director can approve/adjust one final package **without reopening content authoring**. Avoid assuming a new Ghost Ship drop rate or altering an existing Ghost Ship quest/caches in a staging write.

**F3 farm consequence:** retried regular victories pay normal battle XP/ryo repeatedly unless gains are scaled. Demonstrate economics for worst-case retry-loop abuse (one Beacon; unlimited division retries). Provide:
- Option A: accept ordinary repeated settlement (no economy prevention);
- Option B: reduce/zero battle gains on retry-lane encounters via engine-supported `scaleGains` only where evidence proves scope and does not affect final quest rewards;
- optionally additional rate cap if implemented by quest/source and explicitly approved.
Leave user-owned farming policy open; verify any proposed `scaleGains` scheme end to end. No reward granted by wrong puzzle or reset node. `maxAttempts` / `maxCompletes` must be within source limit 100; values are director decisions, **do not import another event's 100/1 cap without approval**.

### Packet F. Art & presentation readiness (NO unapproved generated art)

Produce an **asset-by-asset shotlist** for 25 AI avatars (20 regular, 5 commander), appropriate scene backgrounds (one visual anchor per division, terminals, Command Sanctum, final reveal), Beacon and Countermand item icons, both exclusive Arakane jutsu icons, and any new reward icon that the chosen economy would require. Specify exact target type and owner, ratio/byte/style requirements by reading `skills/producing-tnr-art/data/25x_DATA_art_spec.json`, with imagery calibrated from `art/ghost_ship_skyglass/` **approved actual images**. Record which references are approved assets vs art inspiration; do not copy the existing Ghost Ship decks into the new mountain fortress or invent noncanonical floating architecture.

**Art acceptance is a separate director-owned gate.** Write prompts/briefs and source-key placeholders; do not fabricate `@img` files, upload, generate 25 portraits unattended, use unapproved stock art, or quietly reuse an existing avatar as a "final" new boss. If a hidden offline draft can validate without images, label the limitation. A visible save requires suitable `sceneCharacters`; Fable's Phase1 report explicitly observed the validation requirement.

## 3 — Deliverables to commit as ONE reviewer-ready package

Fable chooses deterministic exact filenames, but the package must contain these **separable artifacts** (do not stop after conceptual Markdown):

1. **Full content census**: 25 slot identities + mapping to all 80 graph battle nodes, 20 regular AI records, five commander AI records, every jutsu ID and equipment choice; each field tagged `APPROVED`, `CANDIDATE`, `NOT_RECORDED` or `BLOCKED` where warranted. E.g. `state/silent_bastion_authoring/encounter_catalog.json`.
2. **Complete prose**: one canonical human script with five puzzles, clue/answer rationale, and 91 generated dialog entries with unique IDs, plus the ending `d.aftermath` (do not claim secrecy from API). E.g. `state/silent_bastion_authoring/dialogue.md` and `quest_dialogs.json`.
3. **Protocol ledger**: all four commander entry routes × five divisions × normal/retry; approved medical settings, candidate Combat and alert effects, D5 unsupported issue and director alternatives. E.g. `protocols.json`.
4. **Combat census**: minion and boss jutsu/AI/item records, exact AI rule objects, 20-cap proof, conditional/fallback coverage, innate passives and numeric tuning assumptions. E.g. `ai_profiles.json`, `combat_balance_candidates.md`. Use validated existing IDs or explicit unresolved external refs, never fabricated IDs.
5. **Economy review sheet**: Beacon/crafting/quest reward options, retry XP/ryo consequences, drop table math, item source provenance, `maxAttempts` choices. E.g. `economy_decisions.md`.
6. **Art shotlist and briefs**: committed text/structured indices, **no unapproved image binaries**. E.g. `art_shotlist.md`.
7. **Deterministic offline compiler/generator** using real generated game contract (do not hand-author a 178-node JSON payload twice). Build into `state/silent_bastion_authoring/generated/` or a non-`push/` review-only directory until director approvals. Show 178 graph nodes compile exactly, resolve as many refs as possible and mark all unresolved values. Emit an application-ready `push/` manifest **only after** the director accepts every relevant content/economy/art number and every release preflight is green; never enable `skipPreflight` to make a release look green.
8. **Native offline evidence and tests**: extend/consume `harness/silent_bastion_phase1/` fixtures; add `harness/silent_bastion_authoring/` or equivalent covering combat (not solely imposed settlements), rule-gate validation, quest outcomes, player starting buffs and no leaks, 50%-only-retry, Final Stand & Stealth, income exploitation, performance, art-link absence, supported tag validation. Save exact commands, exit codes, engine SHA and SHA-256 outputs. Explicitly distinguish tests run vs not run.
9. **Consolidated review report** `docs/reviews/SILENT_BASTION_AUTHORING_OFFLINE_RESULTS.md`: full check matrix; exact accepted/proposed/blocked items; sign-off docket **one table** with all user decisions; residual upstream issues/source drift; no claims of player playtest or live parity.
10. **Frozen-SHA handoff** `docs/handoffs/SILENT_BASTION_AUTHORING_HANDOFF.md`: branch/base/merge-base/head, file index, tests, bundle provenance, no-live boundary, known risks, director approval blockers, and reviewer next step. Update/sync a `state/workstreams/silent_bastion/roadmap.json` **only through** the actual `scripts/content_workstream.py new/validate/render` workflow if the full project needs cross-session tracking; do not hand-edit generated roadmap projections or pretend blocked production is complete.

If complete content is impossible without a director-owned exact value or missing record, still deliver a **complete renderable candidate dossier** and a fail-closed generator that lists exactly which inputs remain. Don't call it a release-ready manifest. Avoid leaving an accidentally selectable production write manifest under `push/`.

## 4 — Required verification / definition of done

**Preflight:**
- Verify current repository `main`, plan SHA, Fable r3 frozen SHA, any corrected Phase1 SHA and current game SHA before starting; record all. Compile the **r2** structure; reconcile source drift from c82 to 56e (or later) and run the existing Phase1 tests where possible. **Do not overwrite another agent's branch**.
- Verify the terminal/pool/user-buff semantics against game validators; `clearprevent` not allowed in current quest `applyBuffs`; test any proposed substitute. Full schema re-extraction/diff before adopting changed source contract.

**Content:**
- Exactly 5 divisions, 20 distinct regular slots, 5 commanders, 5 puzzles each with 3 valid answers, all 91 dialog nodes populated, 178 nodes/80 battle-node routes intact, all 25 encounter slots mapped. 20–25 battles per successful route, exactly 5 commander fights, one completion, no accidental simultaneous/premature battle on normal route. Preserve Medical100 and the 50% retry checkpoint.
- Boss kits: 6/10/11/12/14 moves; all 5 innate Seal Prevent100/99; every AI ≤20 schema-valid rules with exact range gates and a safe fallback; equipment available, no immortal self-buff loops. Grand Marshal combat remains a candidate pending ratification.
- Offline tests for at least five character archetypes (close-range burst, shield/tank, ranged kiter, buff-heavy, healer/control), player start debuffs/buffs and long retry loops. Don't paper over a failing fixture with a test skip or invented in-engine immunity.
- Quest funds/XP/reward logic include possible retry farming and once-only final reward. Item art/source/costs and canonical results reproduced from repo refs, not guessed from old printout.
- Run `factory.py` / domain constructors, `validate.py` in its documented working dir on **every manifest candidate eligible for it**, native QuestValidator and objective-flow checks on full compiled record, AI schemas and source-inspired combat fixtures. **Zero errors** for what is declared validated; report unvalidated blocked outputs separately, never `skipPreflight`.
- Pin tests/evidence (repeat run for deterministic portions) and supply exact-SHA frozen review handoff. Output must be reproducible without ephemeral chat/ZIP-only state.

**Integration / scope gate:**
- Phase1 correction proof is a prerequisite for **final acceptance**, not a reason to stall independent content drafting. Re-run the F1/F2 reproducer and entry-item flow after the correction; report whether F3/E10 changes. Current main/game divergence must be reconciled through an explicit reviewed integration, not a blind fast-forward.
- Final balance/rewards/names/rarities/visuals remain director decisions. Do **not** perform any live game request/write, create game entities, reveal/activate hidden content, use live credentials, merge into main, or publish. Any game-source code fix goes on a **separate owner-approved engineering lane**.

## 5 — One-shot workflow discipline

Execute Packets A→F and generator/test/report in a **single Fable authoring session**, with commits per coherent packet and one final frozen review SHA. Use sensible documented assumptions where safe; label them `CANDIDATE`. Do not stop halfway to ask for cosmetic or routine decisions. **Stop only** if proceeding requires violating a locked director rule, using unauthorized live access, falsifying evidence or introducing an unreviewed game-code patch. Otherwise keep working offline and present **one comprehensive decision docket at the end** rather than interrupting for approvals.

**Completion of this task means a fully drafted, repo-committed, traceable, offline-validated Pyramid content package ready for director decisions and independent audit — never that the event is approved for publication or that the Phase1 engine issue is repaired.**
