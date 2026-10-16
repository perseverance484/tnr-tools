# Ghost Ship: The Last Directive — Silent Bastion design

> **CURRENT JOINT DESIGN STATUS — 2026-10-16.** Both `alt99_f4gate` (99 objectives; four interior divisions, RUL-2026-10-16-002) and the **Arsenal-or-Research, choose-exactly-one completion reward** pilot (RUL-2026-10-16-001) are director-approved **design directions**. Beacon B1 is now **SETTLED** by RUL-2026-10-16-003: debit one Beacon **at expedition start (`startQuest`)**, never refunded on abandonment/failure and no second payment for checkpoint retries. The executable reward choice and Weighted Cache open/receipt path still need Fable's **separate native offline proof**. Exact recipe choices, quantities, weights, rarity/tradability, reward economy, Arakane player Combat Protocol, art and publication are **not approved**. The operative Fable implementation contract is `state/prompt_silent_bastion_complete_authoring.md`; older superseded five-division/first-battle wording below is historical. Shared reward sources were adopted from `chatgpt/recipe-aligned-reward-caches-20261016@fb744e713873a99812b7c6e9ec8631769ef9ff9a` before scoped current-status edits. No live requests/writes.

> **2026-10-16 DIRECTOR APPROVAL — NATIVE-TESTED `alt99_f4gate` SELECTED (RUL-2026-10-16-002).** The earlier `state/silent_bastion_condensed99_candidate.json` remains an archived *failed* starting candidate (native defect C1), NOT the authoring graph. Use `harness/silent_bastion_condensed99/graphs/alt99_f4gate.json` as the **selected 99-node topology**, from Fable's frozen proof `claude/silent-bastion-budget-validation-69za5u@74eeb328f05d4258056b0a1c531619ffcf852ce3` / `docs/reviews/SILENT_BASTION_CONDENSED99_NATIVE_RESULTS.md`. This variant inserts a dialog after recovery_later WIN to keep the reset from firing during the recovery battle, and folds each fourth-fight intro into its Command Terminal choice; it retains commander approach dialogs on both correct and Security Alert Maintenance paths. All four divisions, 16 regular encounter identities, four commanders, four distinct puzzles, post-fourth Medical full-heal / Combat buff, 50%-pool recovery loop, one terminal outcome, and 16–20 successful-route battles remain. Tested against game `13d40c4c1509ecf44262aba1b5120266011ea786`; require current game-source reconciliation and downstream authoring/validation, do not call it current-release-proven.
>
> **Reward direction (separate approval):** `RUL-2026-10-16-001` is recorded on `chatgpt/recipe-aligned-reward-caches-20261016@a5e92bae5ceeba3d3212ca66f157ad0f54dca335`: after successful Pyramid completion, offer a player pick of **exactly one** of Arsenal/Research native recipe-aligned caches. Native quest choice requires `content.rewardMode:"choose"`, `content.rewardPickCount:1`, and both cache item IDs in **quest-level** `content.reward.reward_items` (not objective `win_quest` rewards); verify Battle Pyramid save/claim compatibility offline on the build engine. No extra graph nodes, mid-floor drops or retry-loop cache payouts. Quantities/recipe targets/weights/rarity/trade/art/publishing remain unapproved. Beacon entry timing B1 was **subsequently accepted** by the director under RUL-2026-10-16-003; Arakane's Combat Protocol stand-in and other implementation gates remain open. No game requests or writes authorized.
>


> **CURRENT DIRECTOR-APPROVED SCOPE — 2026-10-15, RUL-2026-10-15-001.**
> The prior five-division, 178-node discussion in this document is retained as **historical design**, not the current implementation target. The director selected **four full interior divisions**, deleting the exterior **Outer Garrison / The Gatewarden** in response to both the objective budget and the intended appearance of a completely deserted installation. The operational four are **I Experimental Armory (legacy graph D2), II Skyglass Research (D3), III High Command (D4), IV Command Sanctum (D5)**. There are **16 regular encounter slots + four commanders**, yielding **16–20 actual fights** on a successful route, including four unique Security puzzles and all three terminal paths. The **99-node candidate** at `state/silent_bastion_condensed99_candidate.json` is selected for **offline native proof**, not accepted as validated quest content.
>
> **EXTERIOR / FIRST IMPRESSION.** The Silent Bastion's exterior is apparently abandoned: **no active visible perimeter defenses, outward patrols, guards, or gatekeeper battle.** Silence and absence of resistance should convince an entrant the Skyglass headquarters was deserted long ago. Only after entry do still-functioning interior mechanisms and reconstructed military personnel gradually contradict that first impression. Do not introduce a replacement entry boss or exterior garrison defense. The Skyglass Beacon remains the Ghost Ship-sourced entry item; the approved Beacon consumption is **on expedition start** under RUL-2026-10-16-003. Keep the original mysterious post-Arakane directives and unrevealed origin.
>
> **MECHANICAL RULES STILL IN FORCE.** Each retained division has three required regular encounters, an optional fourth, one commander, and one unique three-choice Maintenance puzzle. A wrong Maintenance answer still skips the fourth encounter but applies **player-side Security Alert**. After fighting the fourth, the player chooses **Medical (set all pools to 100% for that commander)** or **Combat (temporary player-side buff)** at the protocol dialog. Wins carry player pools; losses before Arakane restart the current division at **50% pools** via the **unverified** source-native recovery-fight/reset-bridge design; Arakane loss fails the entire attempt. The retained four commanders' abilities/lore remain as previously approved, with earlier candidate/final distinctions preserved. Per-division player-facing numbering is **I–IV** even though stable symbolic objective IDs still use `d2`–`d5` until native proof.
>
> **REVIEW GATE.** Static graph checks pass on the 99-node design, but the real `reset_quest` tracker/runtime behavior is **not proven**. No engine change or live-game action is permitted; Fable must run the native offline proof and reconcile it with the one-shot authoring contract before producing a release-ready manifest. Source `docs/reviews/SILENT_BASTION_NODE_BUDGET_OPTIONS_2026-10-15.md`; disposition of The Gatewarden is **removed from this Pyramid**, not repurposed to a new encounter.


**Status:** Director-approved design decisions and open design questions. **Design only;** not a build manifest, game publication, or authorization for live requests/writes.
**Saved:** 2026-10-13.
**Reference baseline:** `perseverance484/tnr-tools@057acddb986b50e486ccf550fac00b68fff51490`; pinned game source reviewed `studie-tech/TheNinjaRPG@67341a1fa1567b9b33827b802e48120e5d797a15`.
**Related continuity:** `state/ghost_ship_skyglass_expansion_design.md`, `state/ghost_ship_hybrid_kit_proposal.md`, `state/ghost_ship_skyglass_sealwright_combat_draft.md`, `docs/00_INDEX.md`, `docs/DOCTRINE.md`.
**Director authority:** All final balance, rewards, item/drop rules, prose, AI behavior acceptance, publication, and game writes remain user-owned.

## Premise — accepted

The **Silent Bastion** is the apparently abandoned but still operational mountain headquarters of the **Skyglass Project**. The rare consumable **Skyglass Signal Beacon**, obtained through the Ghost Ship, grants entry to **Ghost Ship: The Last Directive**, an isolated Battle Pyramid.

The Bastion reveals that the Ghost Ship is receiving **newly generated orders** from an apparently functioning military command network, not merely replaying its last mission. The original commanders died long ago, but their reconstructed chakra impressions and the command infrastructure continue operating. Defeating the Supreme Commander ends this expedition, **not** the larger operation. This develops the Ghost Ship's preservation-order mystery without turning its preserved impressions into undead.

## Pyramid structure — approved direction; implementation pending

- Five divisions, each with four ordinary encounters followed by one commander. Baseline: 25 battles. At the end of each division's third regular encounter, a **Military Command Terminal** allows:
  - **Maintenance Passage:** solve one short puzzle. Correct: clean skip of the fourth regular battle. Incorrect: skip it with temporary **Security Alert**. No recovery or combat buff either way.
  - **Medical Protocol:** defeat the fourth regular enemy; enter the commander fight with **full HP/CP/SP (100%)** (RUL-2026-10-14-001; was 75%).
  - **Combat Protocol:** defeat the fourth regular enemy; enter the commander fight with its division-specific temporary combat buff; no recovery.
- **RUL-2026-10-14-001:** Medical is a **full heal** via battle-start `givePools: 100`. Medical and Combat are chosen in a dialog **after** the single fourth fight; that dialog routes to separate commander battle nodes carrying each protocol's values (none on the fourth enemy). Exact numbers for buffs and Security Alert remain subject to balance review. Earlier illustrative Security Alert: 10% increased damage taken for 2 rounds.
- **Ordinary wins and successful division transitions carry pools forward unchanged.** A proposed automatic 100% refill after defeating division commanders was **retracted** by the director; do not reintroduce it.
- **Defeat in battles 1–24**, including the first four division commanders, restarts the **current division** at **50% HP/CP/SP**, with no extra Beacon paid on the checkpoint loop. Defeat to the **Supreme Commander** (battle 25) fails the entire Pyramid; abandonment also ends the attempt. A new attempt needs a new Beacon.
- The isolated-pyramid game source preserves defeated users at a minimum of 1 HP in the run rather than hospitalizing them; an authored checkpoint reset and 50% battle-start pools must be verified end to end.
- **Superseded by RUL-2026-10-16-003:** A new attempt consumes one Beacon **at expedition start** (`startQuest`), regardless of whether its first battle begins. There is no refund on abandoning or failing, and retries within the attempt do not charge another Beacon.
- All five bosses: **innate `sealprevent` 100% for 99 rounds** to stop standard Seal from disabling their passive AI effects. This does not mean immunity to all control or all kinds of sealing.
- Ordinary enemies: resource chip/attrition for appropriately equipped endgame players, not frequent immediate deaths or excessive crowd control. Division commanders are Ghost Ship Captain-class-or-harder signature fights with increasingly sophisticated AI. Actual multipliers and results require balance fixtures.

**Consolidated all-five-boss move and AI-profile dossier:** [`state/silent_bastion_commander_roster.md`](silent_bastion_commander_roster.md). The dossier distinguishes approved roster decisions from remaining unapproved AI/level/balance proposals.

## Division roster — current status

| Division | Encounters | Commander | Status / encounter identity |
| --- | --- | --- | --- |
| Outer Garrison | 1–5 | **The Gatewarden** | **Director-approved rename (2026-10-14)** of Garrison Marshal. Introductory defensive counter-boss: absorb, reflection, anti-shield Pierce, heavy counterattack, no healing or hard control. |
| Experimental Armory | 6–10 | **Master of Arms** | **Name and enhanced ten-jutsu combat identity approved**: dangerous AP/control combos, vulnerability setup, overdrive. |
| Skyglass Research Division | 11–15 | **Replicant Zero** | **Name, origin lore and eleven-jutsu reconstruction encounter approved**; see below. |
| High Command | 16–20 | **The Grand Marshal** (*The Second*) | Name and role approved; full combat kit remains proposed. |
| Command Sanctum | 21–25 | **Supreme Commander Arakane** | Name, character history, final reveal, signature and Countermand approved; detailed AI candidate in `state/silent_bastion_arakane_ai_profile.md`. Only boss whose defeat of the player fails the Pyramid. |

## Master of Arms — accepted design notes

Ten-jutsu roster: **Piercing Judgment** (B33), **Cataclysm Detonation** (B14), **Recoil Slam** (B28), **Tempest Cleave** (director-specified existing jutsu; ID not yet supplied), **Fighter's Poise** (B37), **Rapid Fire** (S07), **Tempo Fracture** (B08), **Sovereign Ascendance** (B10), **Sovereign Fetters** (B16), **Nullifying Wave** (B32).

- Tempest Cleave: **45 EP damage, 35% increased damage taken, 30% afterburn** per director. It **replaces Scorching Rend**, keeping roster count at ten. Need exact jutsu ID / full live record before implementation.
- Actively **combo Tempo Fracture and Sovereign Fetters** to disrupt AP and seal bloodline effects. Do **not** stagger these deliberately to make the fight easier.
- Tempest Cleave is the setup for **Cataclysm Detonation** or other ordinary damage; Piercing Judgment's Pierce is a **flat shield/defensive counter**, not an IDG-scaling nuke/setup assumption.
- Prioritize **Sovereign Ascendance below 60% HP** rather than waiting until 35%; ensure combat-duration timing and rule fallthrough are tested.
- **Nullifying Wave** is a counter to heavily buffed players; an IDG threshold of 71 is the inherited working proposal. All numeric effectiveness/boss multipliers remain subject to tests/director acceptance.

## Replicant Zero — approved name and origin lore (2026-10-13)

**Approved in full:** The Research Division commander is named **Replicant Zero**, replacing the placeholder *Chief Researcher*.

**Approved lore addition:** Replicant Zero **was not merely the scientist behind Skyglass reconstruction: he was its first successful human subject**. His experiment established the process that later made preservation and reconstruction of the Ghost Ship's crew possible. Although his original body died long ago, the Bastion continues reconstructing his preserved chakra consciousness. He repeatedly recreates himself, attempts to replicate an opponent's techniques/enhancements, and refuses to let his experiment end. This is preserved consciousness, **not undeath**, and it belongs to the Silent Bastion expansion's proposed historical reveal.

**Director-accepted encounter identity:** A difficult, enduring fight built around replication, reconstruction, defense, draining, and healing. Eleven existing shared-pool jutsu:

| Pool | Jutsu | Purpose |
| --- | --- | --- |
| B06 | Split Image | Signature reconstruction clone |
| B07 | Stolen Form | Copy an opponent's enhancements |
| B13 | Hexweave | Damage + vulnerability / recovery suppression |
| B15 | Feast of Marrow | Drain and resource pressure |
| B22 | Compression Barrier | Absorb + damage reduction |
| B23 | Bulwark Charge | Shield and offensive reinforcement |
| B29 | Devouring Wave | Damage and absorb |
| B34 | Mirror Edge | Reflect counterattack |
| B35 | Reaping Strike | Damage and healing |
| S35 | Second Wind | Emergency heal |
| S07 | Rapid Fire | Reliable fallback |

Intended AI: barrier/Hexweave opening; **Split Image on round 2** (initially one deployment per battle); attack through Hexweave → Feast of Marrow → Devouring Wave; **Stolen Form** against high enemy IDG (working threshold 71); **Bulwark Charge below 65% HP**, **Second Wind below 40%**, with Reaping Strike to sustain offense. The player may counter temporary defenses with Clear, healing with Heal Prevent, and clone pressure by killing the replica. Native clone scaling, AI fallback, 11-move action economy, timing and actual fight difficulty require offline verification before a build or balance freeze.

**Important distinction:** The above lore/name/encounter direction were explicitly approved. Exact AI rule objects, stats, innate damage, clone behavior at real boss scaling, visual art, terminal buff strength, item economy and live records remain **unimplemented/unverified**, not silently canonized from this prose.

## Current next step

Design the **Supreme Commander** as the fifth and final boss, preserving the mystery of newly generated military orders. Present candidate abilities and AI behavior for the director's review. Do not edit manifests or operate the live game without separate approval.

## Design approvals — 2026-10-13

**Division IV name:** The Grand Marshal. **Epithet:** The Second. The Supreme Commander's trusted right hand, highest authority below the Commander, and the officer whose advice and independent tactical judgment the Commander trusted enough to permit him to question orders. Other generals answered to him. The earlier name *War General* is superseded. His proposed suppression kit remains pending final review.

**Command Terminal shortcuts:** A successful one-question puzzle grants a clean shortcut past the fourth regular encounter with no downside. A wrong answer still grants the shortcut, but applies the short-lived Security Alert disadvantage against the boss. Every division gets a unique, logically solvable three-choice puzzle. This supersedes the earlier always-penalized shortcut. Medical and Combat Protocol options continue to require defeating the fourth enemy.

**Next:** Design the Supreme Commander, the final boss.

## Supreme Commander — approved core and signature revision (2026-10-13)

**Boss status:** The director approved the name **Supreme Commander Arakane**, the character/history and post-defeat storyline, the fourteen-jutsu direction (with Recoil Slam replaced by the exclusive elemental-seal nuke), the five-round signature, and the separate equipped **Countermand** item. **Exact AI rule profile, item implementation, quantitative stats and balance remain subject to review/tests.**

- The title **Supreme Commander** is intentionally misleading. The player should believe that reaching and defeating the highest-ranking commander will end the new orders. In the **final scene**, a freshly issued directive proves that command issuance continues without him. Preserve the mystery of the actual origin; do not spoil this before the ending.
- Distinguish him from The Grand Marshal's total suppression, Master of Arms' offensive combos, and Replicant Zero's reconstruction and sustain. The Commander is a highly adaptable counter-strategist, with a desperate endgame.
- Approved signature name: **The Last Directive**.
- **Approved signature effects:** **Final Stand for 5 rounds**, **Increased Damage Given for 5 rounds**, and **Clear Prevent for 5 rounds**. Activates based on his HP reaching **about 30%**, through priority native health-conditional AI. This **supersedes** the earlier 1-round Final Stand / 2-round damage buff + increased-damage-taken draft. **No increased-damage-taken tag belongs in the approved signature.** Exact IDG power, jutsu AP/cooldown, and chance values beyond the approved duration remain balance/design decisions.
- The director explicitly requires enough boss durability, uptime and usable AP/pools to cast this near-death ability rather than getting burst down before the trigger. Use test fixtures around the threshold, not unapproved automatic immunity/recovery.
- The director requests an anti-kiting response: when the player refuses to approach, use the opportunity for self-buffing and **Veilstep**, exploiting their opportunity to buff, then **Clear** to punish that setup. This intent is approved but the specific timing needs adjustment to match the engine.

**Current director-approved candidate roster (14), revised:** B18 Apex Hunger, B07 Stolen Form, S34 Purging Stance, B09 Veilstep, EA04 Zephyr Lance, B13 Hexweave, B17 Worldbreaker Chorus, **exclusive final-phase elemental-seal nuke** (replaces B28 Recoil Slam), B27 Scorching Rend, B05 Devouring Grasp, B26 Braced Strike, B20 Surging Overflow, S07 Rapid Fire, exclusive The Last Directive.

**Source-verified caveats at** `studie-tech/TheNinjaRPG@67341a1fa1567b9b33827b802e48120e5d797a15`:

- `app/src/libs/combat/actions.ts` `availableUserActions` **disables all jutsu and basic Clear while the caster is stealthed**, even defensive/support jutsu. With native **B09 Veilstep (Stealth 2 rounds)** the Commander cannot reliably cast a Clear **on the very next round** as originally imagined. Preserve the kite-punishment idea with **Clear as soon as stealth expires**, or do not cast Veilstep on the route requiring next-round Clear. Allow movement during stealth; limit inappropriate repeated stealth cycles.
- `app/src/libs/combat/tags.ts` `applyFinalStandDamage` prevents lethal incoming damage below 1 HP while a positive-round jutsu-sourced Final Stand is in effect; `clearPrevent` prevents native Clear when active. A 5-round signature is structurally expressible (`app/src/validators/combat.ts`, FinalStand/ClearPrevent/IDG tags); verify actual lifetime with combat fixtures.
- Native `health_below` is **strictly less** than the configured integer threshold (`app/src/libs/combat/ai_v2.ts`), so an exact trigger **at 30%** versus **below 30%** needs explicit acceptance of the available boundary semantics.
- With the health-trigger rule alone, the signature may re-cast after cooldown while the boss stays low HP. A long (e.g. 99-round) cooldown is a **proposal**, not an approved value, to avoid unintentional repeated Final Stand.
- B18 Apex Hunger provides 99-round IDG and stat increases and must **not be cast repeatedly** without deliberate balance acceptance: offensive modifiers compound.

**Earlier proposed refinements, now partly superseded:** the proposed **B28 Recoil Slam → B34 Mirror Edge** substitution is **rejected/superseded** by the approved **B28 → exclusive final-phase elemental-seal nuke** substitution. The separate **B27 Scorching Rend → B32 Nullifying Wave** suggestion (ranged Clear) remains **unapproved** and must not be silently applied. Use conditional Copy-then-Clear versus heavy buff users, Pierce versus shields, Cleanse versus disabling effects, Hexweave into Worldbreaker as punishment, an opening self-buff plus selective Veilstep against kiting, and The Last Directive at the director-approved near-death threshold. Continue movement while stealthed. Balance and title/name details remain for director review. **Supreme Commander Arakane** is the director-approved encounter name; preserve the explicit commander title and do not reveal the true source of new orders until the final scene.

**Next:** Validate the ordered candidate at `state/silent_bastion_arakane_ai_profile.md` against pinned game source and offline combat fixtures before any executable implementation. No live requests, commits to main, or production changes are authorized.

### Approved Countermand item — native item path requires validation

At pinned game source `67341a1f`, `app/src/libs/combat/actions.ts` **allows equipped, usable item/weapon actions while their owner is stealthed**, and `app/src/libs/combat/ai_v2.ts` supports `use_specific_item`. `app/tests/libs/combat/seal_stealth.test.ts` exercises that availability. Because **jutsu** and basic Clear cannot be used while stealthed, the exact requested **buff → Veilstep → next-turn Clear** might instead be accomplished with a **new AI-only active item** (working name **Countermand Seal**) that carries a native Clear tag and is actually equipped on the boss. This could strip enemy buffs from stealth and, in open combat, combine with B07 Stolen Form as a Copy-then-Clear combo using 60+40 AP if a 40-AP item is selected. Item effect, targeting, cooldown, equipment, and AI fallback **require offline proof**. The director approved **Countermand** as a new boss-use item and its anti-kite identity; exact item fields and reliable AI interaction still require tests. No extra loot, reward, or art decision is implied. It would preserve the director's **original approved 14-jutsu roster** intact, unlike the proposed B28/B27 substitutions above.

## Supreme Commander — approved ultimate attack revision (2026-10-13)

**Director decision:** Replace **B28 Recoil Slam** outright. The Supreme Commander retains a **14-jutsu roster** containing two exclusive moves: the preexisting support-phase **The Last Directive** and a new **ultimate offensive jutsu** (name **not yet accepted**; `Extermination Order` is an optional working title only).

**Director-approved attack properties:**
- **Damage 80 EP** (ordinary damage, not Pierce).
- **Elemental Seal**, **2 rounds** (affects the opponent's eligible elemental 60 AP jutsu).
- **Cleanse Prevent**, **2 rounds** (prevents the opponent from immediately cleansing the applied debuffs while active).
- **AI activation rule:** Use this nuke **only while the Supreme Commander's Final Stand is active**. Make it his **highest-priority damaging technique** in that endgame window when in range and off cooldown. The long-term support `The Last Directive` still triggers below approximately 30% HP and grants **Final Stand 5r + Increased Damage Given 5r + Clear Prevent 5r**. Its approved near-death trigger is unchanged.
- **Open for director or test-driven freeze:** Jutsu name, range, AP, cooldown, Elemental Seal power, Cleanse Prevent power, damage classification, and exact AI-order tie-breaking. Three effects (damage + seal + cleanse prevention) fit the existing three-tag content doctrine. Do not assume unapproved 100% proc chance.

**Source checks:** At `studie-tech/TheNinjaRPG@67341a1fa1567b9b33827b802e48120e5d797a15`, `app/src/validators/combat.ts` provides `ElementalSealTag`, `CleansePreventTag` and the damage tag; `app/src/libs/combat/actions.ts` applies Elemental Seal to **elemental 60 AP** jutsu, not every elemental action. `app/src/libs/combat/ai_v2.ts` supports conditional `has_effect` on `finalstand`, **but threshold 0 is unconditionally true**, and the condition sums matching effect power without an explicit activity check. Candidate rule must set threshold **at least 1** and be offline-tested to reject zero-duration/expired Final Stand before freezing or publishing. Validate Final Stand timing, increased-damage multiplication, application/cleanse prevention overlap, range/cooldown fallback, and deterministic end-of-buff handoff. No live game requests/writes.

### 2026-10-13 AI candidate saved

The name **Supreme Commander Arakane**, his established humanity and Skyglass command history, the post-defeat autonomous-order reveal, and the boss-only **Countermand** item are approved. The final-stage signature remains **Final Stand 5r + Increased Damage Given 5r + Clear Prevent 5r**, triggered below approximately 30% health, with **80EP Damage + Elemental Seal2r + Cleanse Prevent2r** on the exclusive nuke while Final Stand is active. The latest **20-rule native AI candidate** and Stealth weapon fallback design live in `state/silent_bastion_arakane_ai_profile.md`. The previous 32-rule proposal is superseded because the pinned game's `AI_PROFILE_MAX_RULES = 20`, enforced on server updates. It is a design proposal, **not an approved executable AI profile**. No user-game requests/writes.

### 2026-10-13 rule-cap and Stealth continuity correction

**Source-verified:** The pinned game `app/drizzle/constants.ts` defines `AI_PROFILE_MAX_RULES=20`, enforced by `app/src/server/api/routers/ai.ts`. The earlier 32-rule Arakane design cannot be saved and is superseded by the exact **20-rule candidate** in `state/silent_bastion_arakane_ai_profile.md`. `includeDefaultRules:false` and a guaranteed unconditional end-turn fallback are required.

**New proposed equipped fallback:** In addition to the approved, nonconsumable **Countermand** item, equip **Solar Bow** (40AP/r5/CD3) and **Crossbow** (40AP/r3/CD0), in distinct hand slots. Their stats came from pinned **historical SQL seed**, not a fresh current record, and need readback/fixture validation. During Veilstep, Arakane can use equipped items and weapons even though all jutsu/basic attacks are disabled. Crossbow's zero cooldown provides repeated close-range actions, and end-turn protects against forfeiting when no legal attack remains. **Chakra Pill II** is optional only and not needed for the dependable fallback; current pill effects/cooldowns are unverified. The director requested the fallback but has not yet accepted these exact two equipment selections.

### 2026-10-14 — Gatewarden naming ruling

The Outer Garrison boss's final display name is **The Gatewarden**. This **replaces Garrison Marshal everywhere in prospective content and presentation**. His approved six-move combat identity and introductory difficulty are otherwise unchanged. Previously generated posters still showing Garrison Marshal are outdated presentations and must be corrected if reused; this naming decision does not authorize image editing or any live-game change.
