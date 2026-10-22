# Two Tails armor: stats proposal (offensive counterpart to Kitsune)

**Status:** PROPOSAL for the director (balance is the director's call, CLAUDE.md section 10). Nothing is built
until a version is approved. Asked 2026-10-22: "adjust the stats of the Two Tails set to be an offensive version
of the Kitsune set, with slightly higher pools ... a slightly stronger counterpart to Kitsune with a more
offensive theme" (RUL-2026-10-22-002).
**Source:** push/204 capture, `harvests/inbox/tnr_results_1792629744565.json` (2026-10-22). Engine reads at
studie-tech/TheNinjaRPG@a744c04.

## How armor effects add up (source-verified)

- Armor `increasedamagegiven` and `decreasedamagetaken` (percentage, no element) are folded into battle-start
  totals and **added together** across all worn gear (`libs/combat/process.ts` `buildPreBattleGearModifiersForUser`):
  damage dealt × (1 + total damage-boost points / 100); damage taken × (1 − total DR points / 100), with the
  system floor applied after. Their `statTypes` do nothing.
- `increasemaxpools` with `calculation: static` adds a flat amount; with `percentage` it adds a share of the
  wearer's max pool, so it scales with level.

## Kitsune set (RARE, 6 pieces worn; Pants and Pants-F are the same stats)

| Slot | Piece | Effects |
|---|---|---|
| Head | Kitsune Mask | damage taken −15%, damage dealt +10% |
| Chest | Kitsune Armor | damage taken −15%, max health +500 |
| Hands | Kitsune Gauntlets | max health +500, stats +20% (offence and defence) |
| Waist | Kitsune Belt | absorb 30% of damage as health (5 rounds), stats +20% (offence) |
| Legs | Kitsune Pants / Pants-F | stats +20% (offence and defence), damage dealt +20%, max health +200 |
| Feet | Kitsune Tabi-Shoes | stats +20% (offence and defence), damage dealt +20% |
| **Set** | | **damage dealt +50%, damage taken −30%, max health +1,200, stats +20% on 4 pieces (3 of them both ways), absorb 30% for 5 rounds** |

Shape: two tags per piece (legs three), a balanced set that leans defensive (30 points of DR, absorb).

## Two Tails today (LEGENDARY, 5 pieces; no belt)

| Slot | Piece | Effects |
|---|---|---|
| Head | Zukin | damage dealt +15%, absorb 35% into health, chakra and stamina (35 rounds), highest stats +15% |
| Chest | Shozoku | damage dealt +15%, highest stats +20%, max health +25% (percentage, 40 rounds) |
| Hands | Tekkou | damage dealt +15%, max chakra and stamina +30% (percentage, 45 rounds), highest stats +20% |
| Legs | Tabi | damage dealt +15%, chakra and stamina costs −20% (20 rounds), highest stats +15% |
| Feet | Jaki-Tabi | damage dealt +15%, highest stats +20%, cleanse and clear cooldowns −30 |
| **Set** | | **damage dealt +75%, highest stats +15-20% on all 5, percentage pools, absorb 35%, cost cut, cooldown cut** |

Today Two Tails is not a mirror of Kitsune: three tags on every piece, percentage pools that scale with the
wearer, and utility tags (cost cut, cleanse/clear cooldown) Kitsune does not have.

## Proposal A (recommended): Kitsune's shape, defense swapped for offense, pools about 20% higher

Each piece mirrors its Kitsune counterpart. Kitsune's defensive tags become offensive ones: damage reduction
becomes damage dealt, absorb becomes lifesteal (sustain earned by attacking), and stats boost offence only.
Health pools are static like Kitsune's, about 20% higher (500 → 600, 200 → 250).

| Slot | Piece | Kitsune counterpart | Proposed effects |
|---|---|---|---|
| Head | Zukin | Mask: DR 15, damage +10 | **damage dealt +15%, lifesteal 10%** |
| Chest | Shozoku | Armor: DR 15, health +500 | **damage dealt +15%, max health +600** |
| Hands | Tekkou | Gauntlets: health +500, stats +20 both | **max health +600, stats +20% (offence)** |
| Legs | Tabi | Pants: stats +20 both, damage +20, health +200 | **stats +20% (offence), damage dealt +20%, max health +250** |
| Feet | Jaki-Tabi | Tabi-Shoes: stats +20 both, damage +20 | **stats +20% (offence), damage dealt +25%** |
| **Set** | | | **damage dealt +75%, max health +1,450, stats +20% (offence) on 3 pieces, lifesteal 10%, no damage reduction** |

Against Kitsune: +25 damage points and lifesteal; +250 health (about 21% more); no damage reduction (Kitsune
has 30 points) and one fewer stats piece (Two Tails has no belt). It hits much harder, holds a little more
health, and takes full damage: an offensive counterpart that is slightly stronger overall, fitting LEGENDARY over
RARE. Durations, cost and other fields stay as they are; rounds follow Kitsune (100 for damage and stats, 20 for
max health; lifesteal 100).

## Dials (pick any)

1. **Keep a little defense:** Zukin's lifesteal becomes damage taken −10% (set: 10 DR points vs Kitsune's 30).
2. **More casting fuel instead of only health:** Tekkou's +600 health becomes +300 chakra and +300 stamina.
3. **Stronger lifesteal:** Zukin lifesteal 15% instead of 10%.
4. **Keep stats on highest generals** (today's "Highest") instead of all four generals offence-only.

## What changes for players today (please read)

- **Pools drop at higher levels.** Today Shozoku gives +25% max health and Tekkou +30% max chakra and stamina,
  which grow with the wearer. Proposal A uses flat values like Kitsune (+600). For a wearer with 8,000 max
  health, Shozoku goes from about +2,000 to +600 health. Keeping percentage pools (scaled to stay "slightly above
  Kitsune" at typical levels) is an option if this is too steep.
- **Removed:** the Zukin's 35% absorb, Tabi's −20% chakra/stamina cost, Jaki-Tabi's cleanse/clear cooldown cut,
  and stats on two pieces (5 → 3).
- **Unchanged:** damage dealt total (+75%), names, icons, text (text can follow in a separate ticket once stats
  are settled, since the current descriptions name the old effects).

## Next step

Approve Proposal A (or with dials). I then build a suggest-mode ticket that changes only `effects` on the five
items, each effect composed from a live exemplar of its tag, re-read the items first if the capture is stale, and
pass both gates. Descriptions that name removed effects (Zukin, Tabi, Jaki-Tabi) would follow as a text ticket.
