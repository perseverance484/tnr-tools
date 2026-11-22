# Combat engine knowledge base

A machine-readable map of TNR's combat engine and all 96 tags, written so Claude can load it and reason
from it. Built read-only from `studie-tech/TheNinjaRPG` @ `29cd91b` (2026-11-21). Evidence tier:
**source-verified** (file and line in every tag file), except `overlaps` links, which are design judgement.
`docs/ENGINE_LAWS.md` remains the law text of record; where this disagrees with a law, re-read the cited
source line and raise it rather than blending the two.

## Files

| File | Holds | Use it when |
|---|---|---|
| [engine.md](engine.md) | Round and turn flow, the S0-S16 stages inside one action, effect lifecycle, the three kinds of prevent check, the full damage formula, per-packet mitigation, post-damage readers and caps, Diffuse, stacking, base fields, likely game bugs | You need *when* or *in what order* something happens |
| [tags/&lt;tag&gt;.yaml](tags/) | One file per tag: in-game text, real behavior, polarity, prevented_by and prevent_check, copy/mirror/potency/immunity eligibility, stage (S0-S16), live_from, applies, own and inherited fields as resolved zod expressions, live usage, source lines (handler, dispatch pass, sort rank), interactions | You need what one tag really does |
| [tags.json](tags.json) | All 96 tag files in one object | Loading everything at once |
| [interactions.json](interactions.json) | 12 link kinds and 302 directed links with notes | You need what touches what |
| [exclusions.yaml](exclusions.yaml) | Exclusion areas, the overlap rule, open space, past proposals and verdicts | Before proposing any new tag |
| [rules.json](rules.json) | 16 numeric engine constants (caps, base pools, timing, stacking), each with its source line | A tool or claim needs a number, not prose |

Link counts: removes 64, prevents 43, transfers 33, boosts 32, weakens 31, counters 30, overlaps 22, feeds 20, bypasses 18, disables 5, hides 3, shares 1. `hides` is an action gate (the source removes actions carrying the target tag from the holder's list); `prevents` notes say whether the check is age-compared or any age.

## Who reads it

- **PvP planner** (`state/player/dauntless/tools/`): `combat_map.py` loads `tags.json`, `interactions.json` and
  `rules.json`. `planner2.py`, `turn.py` and `shotplan.py` take their absorb, reflect, lifesteal, afterburn and parry caps
  from it. `python3 combat_map.py --check` and `tests/test_combat_map.py` fail when a planner table (Clear and Cleanse
  sides, kind-to-tag names, hostile ground kinds, cap literals) drifts from the map; only `--check --game PATH`
  (and the test, when a checkout is at `TNR_GAME_SRC` or `/tmp/tnrgit/repo`) also checks `rules.json` against the
  game source. `python3 combat_map.py TAG` prints what
  the engine does with a tag, for replay reviews and live reads.
- **Skills**: designing-tnr-content (tag exclusions), tnr-pvp-combat, tnr-replay-analysis,
  designing-tnr-pve-encounters, building-tnr-content and simulating-tnr-combat read it for engine claims. The map
  wins over memory and over prose notes; where it disagrees with ENGINE_LAWS, re-read the cited line.

## Rules for new tag proposals

1. Read `exclusions.yaml`. A proposal whose core effect falls in an owned area is out, whatever its numbers,
   trigger or target. Changing *when* or *how much* doesn't make it new.
2. Check `interactions.json` for `overlaps` links and the `tags/` files of the nearest tags.
3. Check `past_proposals`: Bulwark, Fuse, Strip, Leash, Dampen and Hijack are out; Prolong passes.
4. Don't propose a new tag until the director asks for one.

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

`_build/` holds the build. Run from `docs/combat-engine/_build` with the game clone at `GAME`:

```bash
export PYTHONDONTWRITEBYTECODE=1
GAME=/tmp/tnrgit/repo          # a clean git checkout of studie-tech/TheNinjaRPG at the pinned commit
OUT=$(mktemp -d)
python3 extract.py $GAME $OUT/tags_resolved.json --legacy-raw $OUT/tags_raw.json
python3 edges.py ../interactions.json                       # link edits from curation.py; idempotent
python3 kb.py $GAME data.json $OUT/kb --extract $OUT/tags_resolved.json --interactions ../interactions.json
diff -ru ../tags $OUT/kb/tags                               # review, then copy tags/ and tags.json over
python3 rules.py $GAME ../rules.json                        # a copy without .git needs --revision FULL_SHA
python3 ../../../state/player/dauntless/tools/combat_map.py --check --game $GAME
```

- `extract.py` resolves every tag schema from `validators/combat.ts`: helpers, spreads (across imports),
  `.extend/.omit/.pick`, multi-line expressions. It exits 1 if anything is left unresolved.
- `data.json` (committed here) is the curated input kb.py reads: each tag's exclusion area, polarity, copy and
  mirror eligibility, fallback behavior text and its live usage counts from Nov 21. `data.py RAW USAGE [OUT]`
  rebuilds it from extract.py's `--legacy-raw` output and a usage table (`| tag | jutsu | pvp-legal |` rows; the
  Nov 21 table is in the project files, not this repo). Only rerun it to change those fields; it blanks the
  `overlaps` notes in its output, which kb.py no longer reads.
- `curation.py` is the hand-checked layer from the PR #129 review: stages, behavior text, live_from, applies,
  prevent_check, link edits and kind definitions. Change engine facts here, with a source line.
- `kb.py` writes `tags/` and `tags.json`. Sort ranks are read only from the `EFFECT_SORT_RANK` map (following
  spreads), dispatch passes from `applyEffects`, and every extra citation is looked up at its definition.
- Pins are the full 40-character SHA everywhere (`tags.json`, `tags/*.yaml`, `interactions.json`, `rules.json`, `exclusions.yaml`), so output doesn't depend on git's abbreviation setting. `extract.py`, `kb.py` and `rules.py` exit 1 on a checkout with local changes, and on a copy without git metadata unless `--revision FULL_SHA` (extract.py, rules.py; kb.py takes the pin from the extract output) names its commit. `rules.py` reads the constants from HEAD's git objects. Run in order, the steps above reproduce the committed files byte for byte.
- `combat_map.py --check` checks the planner against the map (polarity tables, tag names, hostile ground kinds, no numeric cap literals). With `--game PATH` (or `TNR_GAME_SRC`) it also requires one full pin across `rules.json`, `tags.json` and `interactions.json`, then re-reads every rules.json constant from that pinned commit's git objects (never the working tree) and compares value, symbol and file:line; a copy without git metadata fails. `TNR_COMBAT_MAP` swaps only the data files; the reader code comes from this checkout. Nothing re-reads tags.json, interactions.json or engine.md against the game; those are hand-checked in `curation.py`.

When the game source moves past `29cd91b`, re-read the handlers cited in each file before trusting a line; line
numbers will drift first.
