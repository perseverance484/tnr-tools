# Skyglass Project — Sealwright Encounter / Stage 2 Combat Draft

**Status:** PROPOSAL / DIRECTOR COMBAT AND DIFFICULTY APPROVAL REQUIRED. Not frozen, no manifest, no live game actions.  
**Baseline:** `perseverance484/tnr-tools@0eb57de20877d266dde666229ae4c68e8fbcf4c0`.  
**Approved structural route:** `state/ghost_ship_skyglass_expansion_design.md` and `state/ghost_ship_skyglass_graph_patch.json` (RUL-2026-10-10-003).  
**Approved reward scope:** `state/ghost_ship_skyglass_reward_decisions.md` (Skyglass Reliquary route reward, separate Katana and Crown loop).  
**Combat pool authority:** `state/ghost_ship_shared_pool_migration.json` plus generated `skills/building-tnr-content/data/32b_DATA_pool.json` (82 shared jutsu codes).  
**Evidence:** `harvests/inbox/tnr_results_1790826836406.json` contains October 1 baseline of existing elite and boss multipliers.

## Identity and design objective

The **Sealwright** was a highly trained shinobi engineer entrusted with isolating a damaged impression-lattice branch of the Ghost Ship. His preserved higher-fidelity impression discovered deteriorating reconstructions and quarantined their records, but the Captain's preservation command overrode his attempts to stop the system. Skyglass still reconstructs him as the archive's custodian. The character is **not undead, a modern technician, or a generic spellcaster**.

**Encounter identity:** defensive **containment specialist** who survives through wards and disruption, suppresses the player's offensive momentum, and punishes unprotected aggression. Not a damage-race duplicate of First Blade; not a stun-lock or insta-kill boss. Defeating him releases the Reliquary as a **quest-completion reward** rather than a second independent AI drop.

**Combat slot:** The new `b_sealwright` battle in the Quarantined Archive. One Sealwright, battle entered directly from `d_sealwright`; on loss `r_sealwright` returns to `d_sealwright`. The fight is the second combat on the successful secret route after Core Horror. The existing `w_secret` gives exactly one Skyglass Reliquary on completion and terminates the quest.

## Proposed player-facing tactical character

**Contain, unravel, recover.** The Sealwright establishes a defensive barrier, wears down the player's offensive potential, interferes with recovery from debuffs, and removes excessive buffs. He does not chase with heavy burst damage or repeated 100% stuns. The player can exploit his comparatively moderate damage and the windows between his defensive reapplications.

This should feel like fighting the person who built the ship's seal safety systems, not like fighting the Captain again.

## Six shared-pool jutsu candidates

| Priority | Code | Shared jutsu | Role | Current pool effect summary | AP / CD |
| --- | --- | --- | --- | --- | --- |
| 1 | **B22** | Compression Barrier | Defensive opener / repeat ward | Absorb 20% for 3r + Decrease Damage Taken 25% for 3r | 40 / 5 |
| 2 | **S27** | Weakening Strike | Containment pressure | Damage 40 + Decrease Damage Given 20% for 2r | 60 / 4 |
| 3 | **S32** | Lingering Strike | Prevent immediate cleansing | Damage 40 + Cleanse Prevent 100% for 2r | 60 / 4 |
| 4 | **S31** | Unraveling Strike | Remove excessive buffs | Damage 40 + Clear 100% | 60 / 5 |
| 5 | **B33** | Piercing Judgment | Counter shields without one-shot power | Pierce 55 + Increase Damage Taken 25% for 2r | 60 / 7 |
| 6 | **S41** | Steady Strike | Cooldown-safe filler | Damage 30 | 60 / 3 |

**Behavior:** `includeDefaultRules:false`, ordered shared-pool use (exact engine rule objects later generated from schema): prioritize self B22 when available; in range, apply S27, then S32, then S31, B33 and S41 as cooldowns permit; move toward a target when no attack is available. AI uses the actual pool's range gates, not guessed distances. On review consider conditionalizing S31 (Clear) so it is not wasted when no enemy buffs are present, and B33 (Pierce) for target shields; do not author unsupported generic condition predicates.

**Risk to validate:** B22's shared 40 AP stance action must resolve correctly alongside 60 AP damage actions in actual AI combat; verify the shared-pool jutsu's equipped state, rules and IDs from latest committed captures before exact manifest. Defending with both Absorb and Decrease Damage Taken can create a lengthy fight; evaluate turn length and cumulative pressure offline before director tune lock. There is no new bespoke jutsu.

## Relative difficulty proposal — unapproved values

| Record | Captured Level / Rank | Stats × | Pools × | Purpose |
| --- | --- | ---: | ---: | --- |
| Oathkeeper | 100 / JONIN | 2.0 | 2.5 | technical duelist |
| Wayfinder | 100 / JONIN | 2.0 | 3.0 | ranged control |
| Sentinel | 100 / JONIN | 3.0 | 3.5 | heavy defense/controller |
| First Blade | 100 / JONIN | 3.0 | 3.5 | optional elite |
| **Sealwright (proposal)** | **100 / JONIN** | **2.5** | **3.0** | technical containment elite |

This puts Sealwright **below First Blade/Sentinel in raw multipliers** but more demanding than Oathkeeper through defensive denial and encounter knowledge. Proposed `regeneration:60`, with stat, general, element and any armor bindings to be specified based on pool and game constraints. These are **user-owned numerical tuning proposals**, not implementation defaults.

## Completion and player guidance

- One opening elite encounter, no unseen reinforcements, no separate phase-two AI and no random extra boss.
- Loss → retry via existing reset pattern. Do not award the Reliquary on boss damage or before `w_secret`.
- On victory, return to `d_reliquary_claim`; the archive's reconstruction persists, but the player may remove one Reliquary and depart.
- Do not grant Crown fragments, Skyglass Katana, or the Crystal directly from the Sealwright AI.
- Player can learn: shields/defenses protect the custodian; breaking through them and using controlled pressure is more effective than relying exclusively on long-lived buffs.
- The Secret route is a **two-combat route** (Core Horror then Sealwright) with fixed seal puzzle; no forced battle added to the Crowned Captain farm.

## Director decisions needed for combat freeze

1. Is the **containment-control** identity compelling and distinct from existing Oathkeeper/Sentinel?
2. Approve or revise **2.5x stats / 3.0x pools**, Level 100/JONIN, before final AI implementation.
3. Review the six-code kit: the **Cleanse Prevent / weakening** combination and defensive barrier can be frustrating or engaging depending on duration; decide whether to keep S32 or prefer a less restrictive shared action.
4. Confirm the baseline location/battle environment is the **Quarantined Archive** and that no separate Sealwright AI loot should be added.

On approval, Fable can translate a frozen version into exact shared-pool IDs and ordered AI rules with captured game/source schemas, with offline validation and independent review. No live experimentation or game mutation is authorized.
