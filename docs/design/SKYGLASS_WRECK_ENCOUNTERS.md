# Skyglass Wreck: encounter design (draft for director review)

Status: DRAFT (roles, behaviour and floor arcs). Every number is set and checked in the offline harness
(`harness/skyglass_wreck_sim/`, branch `fable/skyglass-wreck-sim`) against RUL-2026-10-26-006 / -007 before any live edit.
Player model: level-100 Jonin, capped stats, full Kitsune set, level-capped PvE jutsu (director, 2026-10-28). Calibration: live damage settings (director, 2026-10-28: curve 2, gen_weight 1, advantage_min 0; the rest match code
defaults) and the solo anchor "good level-100 players beat The Captain solo in 8-10 rounds; a tough fight".

## Principles

1. **Every enemy has one job players can read and answer.** No enemy is just a health pool with a big hit.
2. **Each floor teaches one idea; the boss floor combines them.**
3. **1-2 waves per floor, 3-4 enemies a wave.** The baseline party is strong (director, 2026-10-28: level-100 Jonin with
   capped stats, a full Kitsune set and level-capped PvE jutsu; three of them make two-enemy waves light work). Costs to
   budget: pools refill only between floors, a wave spawns on the far side (1-2 rounds of walking), and a floor battle's
   round counter runs across its waves, so a later wave's openers gate on distance or health, not `round_lower_than`.
4. **Dungeon-only copies.** The live crew also fight in the hunts and quests; the dungeon gets its own records (an
   endgame set and a level-50 set), so tuning here never moves the hunts.
5. **Threat from mechanics, not stacked damage.** The live crew carry +350-470% damage given; the copies trade most of
   that for behaviour (focus fire, protection, telegraphed bursts).

## Rule vocabulary available (validators/ai.ts)

Targets: CLOSEST_OPPONENT, RANDOM_OPPONENT, LOWEST_HEALTH_OPPONENT, HIGHEST_MAX_HEALTH_OPPONENT, HIGHEST/LOWEST_ENMITY_OPPONENT,
CLOSEST_ALLY, RANDOM_ALLY, LOWEST_MAX_HEALTH_ALLY, HIGHEST_MAX_HEALTH_ALLY, SELF, empty-ground targets, barrier targets.
Conditions: health_below (self), distance_lower/higher_than (to the rule's target), player_within_range, round_lower/greater_than,
specific_round, has_effect (self), target_has_effect. Actions: specific/random/highest-power jutsu or item, combo, move, end turn.
Not available: "an ally is below X% health" and "I do not have effect X"; designs avoid needing them.

## Roles

| Enemy | Role | Behaviour players learn |
|---|---|---|
| Deck Warden | Line holder | Closes in and pins the closest player (root/snare), then grinds. Easy to kill; punishes standing still. |
| Seal Charge | Fuse | Walks at the nearest player and detonates on a fixed round of the floor. Kill it or step away. |
| Core Canister | Area denial | Plants itself; erupts around itself on a fixed rhythm. Fight away from it. |
| Core Horror | Bruiser | Slow; huge hits on whoever is closest; hits harder under 50% health. Kite it. |
| Wayfinder | Controller | Keeps distance, displaces and slows players, marks a target that the rest focus. |
| Arsenal Keeper | Artillery | Stays back; long-range volleys; arms Seal Charges (wave pairing). Reach him first. |
| Skyglass Sentinel | Guardian | Shields or buffs the closest ally every few rounds; taunts. Kill order matters. |
| First Blade | Assassin | Ignores the front line and hunts the LOWEST_HEALTH_OPPONENT; burst on low targets. Protect the weak. |
| Oathkeeper | Duelist | Debuffs (seal/disarm-style) whoever has the highest enmity; punishes the party's main damage dealer. |
| The Captain | Mini-boss | Command buffs on allies, a heavy combo at range 5; mid-fight surge at 50%. |
| Sealwright | Support | Seals and slows players, cleanses/heals allies (via ally targets); kill first or the fight drags. |
| Crowned Captain | Final boss | Three phases by health (100-60 / 60-30 / under 30): duelist, then calls hazards, then a desperate burst with Final-Stand-style protection. |

## Mechanics toolkit (engine-supported; each verified in the harness before use)

| Mechanic | Engine basis | Use | Animation |
|---|---|---|---|
| Telegraphed danger zones | ground effects become user effects on whoever stands on the tile at round processing (`process.ts`) | Arsenal Keeper shells marked hexes; Core Canister shards; boss phase 2 | zone sigil |
| Skyglass barriers | `barrier` tag (HP, absorb %, sprite); targets `BARRIER_BETWEEN`, `BARRIER_BLOCKING_CLOSEST_OPPONENT` | Sentinel walls off allies; enemies break player walls | barrier sprite (still) |
| Afterimage clones | `clone` tag (2+ rounds) | Wayfinder decoys; Crowned Captain splits in phase 2 (mid-fight bodies without summons) | clone shimmer |
| Marks and focus fire | debuff + `target_has_effect` conditions | Wayfinder marks a player; allies focus the mark | mark sigil |
| Defensive windows | `reflect` / `mirror`, `stealth` | Sentinel's mirror ward; First Blade vanishes, then hits the lowest-health player | reflect shimmer |
| Visible fuses | `visual` tag | Seal Charge arming glow until it detonates | arming glow |
| Boss phase moments | self buffs on `health_below` | crown aura at phase 2; Final Stand crown shatter | crown aura, crown shatter |
| Threat roles | enmity, `increaseaggro`/`decreaseaggro`, `HIGHEST/LOWEST_ENMITY_OPPONENT`, aggro halos (2026-10-11) | Wardens and Captain take the top threat; First Blade the lowest; Oathkeeper punishes the top threat | (UI halos) |
| Support | `CLOSEST_ALLY`, `LOWEST_MAX_HEALTH_ALLY` targets | Sealwright heals and cleanses; Sentinel shields | none |

To verify in the harness: zone timing (damage on landing, or from the next round), clone and barrier behaviour under AI
control, movement jutsu and summons with ground targets (director doubts AI movement jutsu work). Animations join the art
batch as ANIMATION assets (vertical strips) once the mechanics are confirmed.

## Endgame floor layout (director, 2026-10-28)

| Floor | Wave 1 | Wave 2 |
|---|---|---|
| 1 | Deck Warden x3 + Seal Charge | none |
| 2 | Deck Warden + Seal Charge x2 | Deck Warden x3 |
| 3 | Skyglass Sentinel + First Blade + Deck Warden | none |
| 4 (mini-boss) | Deck Warden x2 + Oathkeeper | The Captain + Wayfinder |
| 5 (boss) | Deck Warden x2 + First Blade + Core Canister x2 | Crowned Captain + Sealwright |

**Hazards are never reinforcements** (director): Seal Charges and Core Canisters do not move, so a hazard in a later wave
just sits on the far side and detonates harmlessly. They appear only in a floor's first wave.

**Openers in later waves.** A floor battle's round counter runs across its waves, so `round_lower_than 2` never fires for
a wave-2 enemy. Two fixes inside the current rules: (1) put the opener first with no condition and let the jutsu's
cooldown stop it repeating (a new enemy always starts with its cooldowns ready); (2) gate it on distance ("every player is
more than 5 hexes away"), which is true on a later wave's first turn because it spawns on the far side. Where an opener
needs a longer cooldown than its shared jutsu record has, the dungeon copy gets its own copy of that jutsu (the hunts keep
theirs). The harness checks every opener fires once per fight.

## Level 40-60 version (10-15 min)

Same arcs with level-50 copies and lighter kits: floors 1-4 at two enemies, the boss floor without Sealwright; the
Crowned Captain keeps two phases. Target ~18-20 rounds. Loot: entry tier only (RUL-2026-10-26-007).

## Harness acceptance checks (per version)

- Average party: full clear in the target minutes at 15 s per turn; about 1 run in 5 wipes once; no floor wipes the party
  more than 1 run in 10.
- Every enemy's signature rule fires in at least 70% of fights it appears in; no enemy spends more than 25% of its
  actions idle or walking after round 2.
- Top damage share per floor matches the floor's idea (e.g. First Blade's damage lands on the lowest-health player).

## Open (director)

Role assignments and floor ideas above; the boss's phase moves; whether hazards (Seal Charge, Core Canister) stay in the
easy version.
