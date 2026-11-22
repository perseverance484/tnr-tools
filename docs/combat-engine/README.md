# Combat engine knowledge base

A machine-readable map of TNR's combat engine and all 96 tags, written so Claude can load it and reason
from it. Built read-only from `studie-tech/TheNinjaRPG` @ `29cd91b` (2026-11-21). Evidence tier:
**source-verified** (file and line in every tag file), except `overlaps` links, which are design judgement.
`docs/ENGINE_LAWS.md` remains the law text of record; where this disagrees with a law, re-read the cited
source line and raise it rather than blending the two.

## Files

| File | Holds | Use it when |
|---|---|---|
| [engine.md](engine.md) | Round and turn flow, the A0-A12 stages inside one action, effect lifecycle, prevent rule, the full damage formula, stacking and caps, base fields | You need *when* or *in what order* something happens |
| [tags/&lt;tag&gt;.yaml](tags/) | One file per tag: in-game text, real behavior, polarity, prevented_by, copy/mirror/potency/immunity eligibility, stage, live_from, own fields as zod expressions, live usage, source lines, interactions | You need what one tag really does |
| [tags.json](tags.json) | All 96 tag files in one object | Loading everything at once |
| [interactions.json](interactions.json) | 11 link kinds and 282 directed links with notes | You need what touches what |
| [exclusions.yaml](exclusions.yaml) | Exclusion areas, the overlap rule, open space, past proposals and verdicts | Before proposing any new tag |

Link counts: removes 64, prevents 45, transfers 33, boosts 32, weakens 29, counters 27, overlaps 22, bypasses 12, feeds 12, disables 5, shares 1.

## Rules for new tag proposals

1. Read `exclusions.yaml`. A proposal whose core effect falls in an owned area is out, whatever its numbers,
   trigger or target. Changing *when* or *how much* doesn't make it new.
2. Check `interactions.json` for `overlaps` links and the `tags/` files of the nearest tags.
3. Check `past_proposals`: Bulwark, Fuse, Strip, Leash, Dampen and Hijack are out; Prolong passes.
4. Don't propose a new tag until Brandon asks for one.

## Tags by area

| Area | Tags |
|---|---|
| Damage now | [damage](tags/damage.yaml), [pierce](tags/pierce.yaml), [elementaldamage](tags/elementaldamage.yaml), [onehitkill](tags/onehitkill.yaml), [weakness](tags/weakness.yaml) |
| Damage later | [wound](tags/wound.yaml), [afterburn](tags/afterburn.yaml), [poison](tags/poison.yaml), [drain](tags/drain.yaml), [diffuse](tags/diffuse.yaml), [curse](tags/curse.yaml) |
| Damage scaling | [increasedamagegiven](tags/increasedamagegiven.yaml), [decreasedamagegiven](tags/decreasedamagegiven.yaml), [increasedamagetaken](tags/increasedamagetaken.yaml), [decreasedamagetaken](tags/decreasedamagetaken.yaml), [increasepotency](tags/increasepotency.yaml), [decreasepotency](tags/decreasepotency.yaml), [increasestat](tags/increasestat.yaml), [decreasestat](tags/decreasestat.yaml), [increasemastery](tags/increasemastery.yaml), [decreasemastery](tags/decreasemastery.yaml) |
| Soak damage | [shield](tags/shield.yaml), [barrier](tags/barrier.yaml), [absorb](tags/absorb.yaml), [siphon](tags/siphon.yaml), [consume](tags/consume.yaml), [finalstand](tags/finalstand.yaml) |
| Send it back | [reflect](tags/reflect.yaml), [parry](tags/parry.yaml), [recoil](tags/recoil.yaml), [mirror](tags/mirror.yaml) |
| Healing | [heal](tags/heal.yaml), [lifesteal](tags/lifesteal.yaml), [vamp](tags/vamp.yaml), [increaseheal](tags/increaseheal.yaml), [decreaseheal](tags/decreaseheal.yaml), [healprevent](tags/healprevent.yaml) |
| Remove effects | [clear](tags/clear.yaml), [cleanse](tags/cleanse.yaml) |
| Take effects | [copy](tags/copy.yaml) |
| Protection | [buffprevent](tags/buffprevent.yaml), [debuffprevent](tags/debuffprevent.yaml), [clearprevent](tags/clearprevent.yaml), [cleanseprevent](tags/cleanseprevent.yaml), [stunprevent](tags/stunprevent.yaml), [sealprevent](tags/sealprevent.yaml), [summonprevent](tags/summonprevent.yaml), [onehitkillprevent](tags/onehitkillprevent.yaml), [robprevent](tags/robprevent.yaml), [immunity](tags/immunity.yaml) |
| Deny actions | [stun](tags/stun.yaml), [seal](tags/seal.yaml), [elementalseal](tags/elementalseal.yaml), [stealth](tags/stealth.yaml), [disarm](tags/disarm.yaml), [timecompression](tags/timecompression.yaml), [increasepoolcost](tags/increasepoolcost.yaml), [increasecooldown](tags/increasecooldown.yaml) |
| Speed up actions | [timedilation](tags/timedilation.yaml), [decreasepoolcost](tags/decreasepoolcost.yaml), [decreasecooldown](tags/decreasecooldown.yaml), [injectjutsus](tags/injectjutsus.yaml), [increaserange](tags/increaserange.yaml) |
| Position | [move](tags/move.yaml), [moveprevent](tags/moveprevent.yaml), [redirection](tags/redirection.yaml) |
| Extra fighters | [summon](tags/summon.yaml), [clone](tags/clone.yaml) |
| Pools and money | [increasemaxpools](tags/increasemaxpools.yaml), [decreasemaxpools](tags/decreasemaxpools.yaml), [rob](tags/rob.yaml) |
| Escape | [flee](tags/flee.yaml), [fleeprevent](tags/fleeprevent.yaml) |
| Enemy AI focus (PvE) | [increaseaggro](tags/increaseaggro.yaml), [decreaseaggro](tags/decreaseaggro.yaml) |
| Sage mode | [activatesagemode](tags/activatesagemode.yaml) |
| Outside battle or cosmetic | [increaseregeneration](tags/increaseregeneration.yaml), [decreasecookingtime](tags/decreasecookingtime.yaml), [decreasecraftingtime](tags/decreasecraftingtime.yaml), [decreasefarmingtime](tags/decreasefarmingtime.yaml), [decreasegatheringtime](tags/decreasegatheringtime.yaml), [increasegatheringyield](tags/increasegatheringyield.yaml), [increasehuntingyield](tags/increasehuntingyield.yaml), [increasejutsuslots](tags/increasejutsuslots.yaml), [marriageslotincrease](tags/marriageslotincrease.yaml), [noncombatincreasereskins](tags/noncombatincreasereskins.yaml), [noncombatconsumereward](tags/noncombatconsumereward.yaml), [noncombatgainskill](tags/noncombatgainskill.yaml), [noncombatquest](tags/noncombatquest.yaml), [repair](tags/repair.yaml), [removebloodline](tags/removebloodline.yaml), [rollbloodline](tags/rollbloodline.yaml), [rollsagemode](tags/rollsagemode.yaml), [unlockitemvariant](tags/unlockitemvariant.yaml), [unknown](tags/unknown.yaml), [visual](tags/visual.yaml) |

## Regenerating

`_build/` holds the two scripts as run (they expect the game clone at `/tmp/tnrgit/repo` and the Nov 21 tag
usage table): `data.py` holds the hand-checked behavior text and links, `kb.py` parses `validators/combat.ts`,
`tags.ts`, `process.ts` and `util.ts` for fields and line numbers and writes `tags/`. When the game source moves past `29cd91b`, re-read the handlers cited in each file before trusting a
line; line numbers will drift first.
