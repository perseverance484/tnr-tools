# Ghost Ship: The Last Directive — Silent Bastion design

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
  - **Medical Protocol:** defeat the fourth regular enemy; enter the commander fight with **75% HP/CP/SP starting pools**.
  - **Combat Protocol:** defeat the fourth regular enemy; enter the commander fight with its division-specific temporary combat buff; no recovery.
- The 75% value is a **set-to percentage** through the reviewed battle-start `givePools` mechanism, not a floor/true heal. This can reduce a higher existing pool; user-facing descriptions and graph implementation must not pretend otherwise. Exact numbers for buffs and Security Alert remain subject to balance review. Earlier illustrative Security Alert: 10% increased damage taken for 2 rounds.
- **Ordinary wins and successful division transitions carry pools forward unchanged.** A proposed automatic 100% refill after defeating division commanders was **retracted** by the director; do not reintroduce it.
- **Defeat in battles 1–24**, including the first four division commanders, restarts the **current division** at **50% HP/CP/SP**, with no extra Beacon paid on the checkpoint loop. Defeat to the **Supreme Commander** (battle 25) fails the entire Pyramid; abandonment also ends the attempt. A new attempt needs a new Beacon.
- The isolated-pyramid game source preserves defeated users at a minimum of 1 HP in the run rather than hospitalizing them; an authored checkpoint reset and 50% battle-start pools must be verified end to end.
- The entry item is consumed once at the first battle of a new attempt in the reviewed source; do not misstate it as consumed merely by opening the Pyramid screen.
- All five bosses: **innate `sealprevent` 100% for 99 rounds** to stop standard Seal from disabling their passive AI effects. This does not mean immunity to all control or all kinds of sealing.
- Ordinary enemies: resource chip/attrition for appropriately equipped endgame players, not frequent immediate deaths or excessive crowd control. Division commanders are Ghost Ship Captain-class-or-harder signature fights with increasingly sophisticated AI. Actual multipliers and results require balance fixtures.

## Division roster — current status

| Division | Encounters | Commander | Status / encounter identity |
| --- | --- | --- | --- |
| Outer Garrison | 1–5 | **Garrison Marshal** | Accepted introductory boss: defense, reflect, counterattacks, limited sustained control, no heal. |
| Experimental Armory | 6–10 | **Master of Arms** | **Name and enhanced ten-jutsu combat identity approved**: dangerous AP/control combos, vulnerability setup, overdrive. |
| Skyglass Research Division | 11–15 | **Replicant Zero** | **Name, origin lore and eleven-jutsu reconstruction encounter approved**; see below. |
| High Command | 16–20 | **The Grand Marshal** (*The Second*) | Name and role approved; full combat kit remains proposed. |
| Command Sanctum | 21–25 | **Supreme Commander** | Intended climax; details not yet designed. Only boss whose defeat of the player fails the whole Pyramid. |

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

**Boss status:** The director approved the Supreme Commander's foundational identity and prior proposed fourteen-jutsu concept, with a specific revision to his exclusive signature. **Name, final refined roster, rule priorities, stats and balance remain open.**

- The title **Supreme Commander** is intentionally misleading. The player should believe that reaching and defeating the highest-ranking commander will end the new orders. In the **final scene**, a freshly issued directive proves that command issuance continues without him. Preserve the mystery of the actual origin; do not spoil this before the ending.
- Distinguish him from The Grand Marshal's total suppression, Master of Arms' offensive combos, and Replicant Zero's reconstruction and sustain. The Commander is a highly adaptable counter-strategist, with a desperate endgame.
- Approved signature name: **The Last Directive**.
- **Approved signature effects:** **Final Stand for 5 rounds**, **Increased Damage Given for 5 rounds**, and **Clear Prevent for 5 rounds**. Activates based on his HP reaching **about 30%**, through priority native health-conditional AI. This **supersedes** the earlier 1-round Final Stand / 2-round damage buff + increased-damage-taken draft. **No increased-damage-taken tag belongs in the approved signature.** Exact IDG power, jutsu AP/cooldown, and chance values beyond the approved duration remain balance/design decisions.
- The director explicitly requires enough boss durability, uptime and usable AP/pools to cast this near-death ability rather than getting burst down before the trigger. Use test fixtures around the threshold, not unapproved automatic immunity/recovery.
- The director requests an anti-kiting response: when the player refuses to approach, use the opportunity for self-buffing and **Veilstep**, exploiting their opportunity to buff, then **Clear** to punish that setup. This intent is approved but the specific timing needs adjustment to match the engine.

**Original approved candidate roster (14):** B18 Apex Hunger, B07 Stolen Form, S34 Purging Stance, B09 Veilstep, EA04 Zephyr Lance, B13 Hexweave, B17 Worldbreaker Chorus, B28 Recoil Slam, B27 Scorching Rend, B05 Devouring Grasp, B26 Braced Strike, B20 Surging Overflow, S07 Rapid Fire, exclusive The Last Directive.

**Source-verified caveats at** `studie-tech/TheNinjaRPG@67341a1fa1567b9b33827b802e48120e5d797a15`:

- `app/src/libs/combat/actions.ts` `availableUserActions` **disables all jutsu and basic Clear while the caster is stealthed**, even defensive/support jutsu. With native **B09 Veilstep (Stealth 2 rounds)** the Commander cannot reliably cast a Clear **on the very next round** as originally imagined. Preserve the kite-punishment idea with **Clear as soon as stealth expires**, or do not cast Veilstep on the route requiring next-round Clear. Allow movement during stealth; limit inappropriate repeated stealth cycles.
- `app/src/libs/combat/tags.ts` `applyFinalStandDamage` prevents lethal incoming damage below 1 HP while a positive-round jutsu-sourced Final Stand is in effect; `clearPrevent` prevents native Clear when active. A 5-round signature is structurally expressible (`app/src/validators/combat.ts`, FinalStand/ClearPrevent/IDG tags); verify actual lifetime with combat fixtures.
- Native `health_below` is **strictly less** than the configured integer threshold (`app/src/libs/combat/ai_v2.ts`), so an exact trigger **at 30%** versus **below 30%** needs explicit acceptance of the available boundary semantics.
- With the health-trigger rule alone, the signature may re-cast after cooldown while the boss stays low HP. A long (e.g. 99-round) cooldown is a **proposal**, not an approved value, to avoid unintentional repeated Final Stand.
- B18 Apex Hunger provides 99-round IDG and stat increases and must **not be cast repeatedly** without deliberate balance acceptance: offensive modifiers compound.

**Proposed refinements to review, not yet approved:** swap **B28 Recoil Slam → B34 Mirror Edge** (eliminate self-damage and add tactical Reflect), and **B27 Scorching Rend → B32 Nullifying Wave** (needed native ranged Clear; r5, 60 AP), keeping the roster at 14. Use conditional Copy-then-Clear versus heavy buff users, Pierce versus shields, Cleanse versus disabling effects, Hexweave into Worldbreaker as punishment, an opening self-buff plus selective Veilstep against kiting, and The Last Directive at the director-approved near-death threshold. Continue movement while stealthed. Balance and title/name details remain for director review. A proposed personal name may accompany the player-facing title, but **Supreme Commander** must remain prominent to preserve the final reveal.

**Next:** Present refined names, lore, twelve-to-fourteen-move tactical priorities, 5-round Final Stand timing, and corrective anti-kite implementation for director acceptance. No live requests, commits to main, or production changes are authorized.

### Anti-kite refinement candidate — newly verified native item path (not approved)

At pinned game source `67341a1f`, `app/src/libs/combat/actions.ts` **allows equipped, usable item/weapon actions while their owner is stealthed**, and `app/src/libs/combat/ai_v2.ts` supports `use_specific_item`. `app/tests/libs/combat/seal_stealth.test.ts` exercises that availability. Because **jutsu** and basic Clear cannot be used while stealthed, the exact requested **buff → Veilstep → next-turn Clear** might instead be accomplished with a **new AI-only active item** (working name **Countermand Seal**) that carries a native Clear tag and is actually equipped on the boss. This could strip enemy buffs from stealth and, in open combat, combine with B07 Stolen Form as a Copy-then-Clear combo using 60+40 AP if a 40-AP item is selected. Item effect, targeting, cooldown, equipment, and AI fallback **require offline proof**. This is an optional new entity requiring explicit director approval; no extra loot, reward, or art decision is implied. It would preserve the director's **original approved 14-jutsu roster** intact, unlike the proposed B28/B27 substitutions above.
