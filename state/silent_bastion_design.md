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
  - **Maintenance Passage:** skip the fourth regular battle; no recovery/buff; fight the commander under **Security Alert** (temporary disadvantage).
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
| High Command | 16–20 | **War General** (working title) | Next commander to design; not yet approved. |
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

Design the **High Command / War General** as the fourth boss, markedly tougher than Replicant Zero, emphasizing command-grade suppression and intelligent tactical decisions without simply cloning the Sealwright's seven-move dual-Clear rotation. Present candidate jutsu and priorities to the director **one boss at a time**. Do not edit manifests, user-owned balance, or the live game without separate approval.
