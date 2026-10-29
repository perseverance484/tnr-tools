# Workflow — Skyglass consistency check

**Status:** Lane A tooling for RUL-2026-10-28-028 item 3. Runs before push/319 and before any later Skyglass manifest is
handed over, alongside `validate.py` (it does not replace it).

**Tool:** `scripts/skyglass_check.py` · **Design data:** `state/skyglass_design/design_data.json` ·
**Tests:** `python3 -m unittest scripts/test_skyglass_check.py` (fixtures in `scripts/fixtures/skyglass_check/`)

The check compares generated manifests with the design of record, so content cannot drift from it silently. It is
deterministic, stdlib-only and socket-free: it reads repository files and makes no request of any kind.

## Run it

```text
python3 scripts/skyglass_check.py push/319_skyglass_update.json   # one manifest (all checks apply)
python3 scripts/skyglass_check.py                                 # every push/*.json write manifest
python3 scripts/skyglass_check.py --json ...                      # machine-readable findings
```

Each finding names the file, the item (`items[i] entity/slot id 'label'`), the field path and the problem.

| Exit | Means |
|---|---|
| 0 | no ERROR (WARN lines may remain) |
| 1 | at least one ERROR |
| 2 | a manifest could not be read or parsed |

A manifest passed by path gets every check. With no path, every `push/*.json` that has write items is read: the ones
whose file name contains `skyglass` or `crownhold`, or that touch a record in the design data (by id, or a create by
name), get every check; every other write manifest gets only the empty-profession-list check (check 2b), because that
rule holds for any manifest. Read-only captures carry no items and are skipped.

**WARN `pending`:** the design names a record that does not exist yet (no id anywhere in the repository), such as Galley
Stores, the Echo Jar or the Crownbreaker badge. The option cannot be verified, so it is a warning, not an error. Once
the record exists, put its id in the design data (with the file that holds it) and the warning becomes a real check.

## Checks

| Check | Rule | Source of record |
|---|---|---|
| `design` | the design data still matches its prose sources; every id is still in the file it cites | below |
| `picks` | each known run's `rewardMode` is `choose`, `rewardPickCount` matches, and the option cards are exactly the design's options; a retired record (the Armory Requisition) may only be hidden | loot tables §4a; RUL-2026-10-28-016 |
| `win-only` | (a) a `start_battle` / `defeat_opponents` objective carries no reward field with a value except `reward_hunter_items(_ids)` / `reward_gathering_items(_ids)`; (b) anywhere in any manifest (quests, objectives, packages, item effects) a profession flag that is `true` has a non-empty id list | RUL-2026-10-28-022, -023 |
| `chest-text` | every item with a `noncombatconsumereward` weighted cache states its rates, rolls and fixed rewards (convention below) | loot tables §0 |
| `voice` | player-facing text has none of the story bible's "Never use" words (whole word, any case) and no "seven-bladed" | story bible, Voice |
| `chart-tier` | chart rarity matches its tier | RUL-2026-10-28-028 item 4 |
| `prof-chest` | an edited profession chest has the rarity and hunt/gather flag of §4b; a hunt's profession id lists hold only that profession's chests of the area's tier | loot tables §4b; RUL-2026-10-28-023 |

**Option cards** follow the engine exactly (source-verified, theninjarpg@2af4b320 `libs/rewardChoice.ts`
`buildRewardChoiceCards`, `validators/rewards.ts`:172-202): every positive amount field (ryo, exp, tokens, ...) is one
card; every id in a `reward_items` entry is one card with that entry's quantity; every jutsu, bloodline, sage mode, badge
and title id is one card; every reward package with a reward is one card holding its whole payload. The `number` (drop
chance) of a `reward_items` entry does not matter in choose mode. A package sent without a `rewards` snapshot cannot be
compared and is a warning.

**"Carries a reward"** (check 2a) means a value other than `0`, `false`, `null`, `""`, `"NONE"`, `"None"`, `[]` or
`{}`. Builder defaults that are zero or empty are fine.

**Player-facing text** (check 4) is every `name`, `description`, `successDescription`, `failDescription`,
`drawDescription`, `fleeDescription`, `battleDescription`, `displayName` and choice `text` inside a quest, item, jutsu or
other record's `data`, including effect descriptions; for AIs only `username`. Objective ids, AI rule descriptions,
asset records and the manifest's own item labels are not player-facing and are not scanned. The word list is read from
the story bible at run time, so editing the bible's "Never use" line changes the check; words match whole, without
inflection (`lift` matches "lift", not "lifts").

## Chest description convention (loot tables §0)

Every item whose effects include a `noncombatconsumereward` with `rewardMode: "weightedCache"` must send its
`description` in the same edit (an edit that sets the cache without the text fails: the live text could not be shown to
match). The description may open with story voice and the explanation §0 asks for; somewhere in it, it must state:

1. **Each tier and its chance:** `<Tier name> <p>%`, using the tier names of the cache. Tiers that share a name are
   stated once with their summed chance (the Archive Chart Case's two Legendary tiers, 3 + 5, read `Legendary 8%`).
   Zero-weight tiers are left out. No other `Common/Uncommon/Rare/Epic/Legendary/Mythic <n>%` may appear.
2. **The rolls:** one fixed count is `<n> roll` / `<n> rolls` (digits), and no other roll count may be mentioned; a
   distribution states every count with its chance, `<n> rolls <p>%`.
3. **Fixed rewards** (any other `noncombatconsumereward` effect on the item, paid on every opening): ryo as
   `<amount with thousands commas> ryo`, exp as `<amount> exp`, items as `<item name> ×<quantity>` (`x` accepted).
   An item whose name is not known to the repository (design data, `answers/names_item.json`, or a named item in the
   same manifest) is a warning.

**Percentages:** cache weights are basis points (10000 = 100%). The stated value is the exact percentage rounded half
up to a whole number, or to one decimal below 1% (`50` → `0.5%`). Only that canonical form passes.

Separators are free; the house style is the middle dot. Examples:

```text
A sealed coffer from the Core's own stores. 1 roll: Common 69% · Rare 24% · Epic 5% · Legendary 2%.

Crownhold's own coffers. Every opening pays 150,000 ryo, then 3 rolls 60% · 4 rolls 30% · 6 rolls 10% of:
Common 45% · Rare 35% · Epic 15% · Legendary 5%.
```

This convention is the checker's machine-readable reading of §0; the wording around the rates stays the director's.

## The design data

`state/skyglass_design/design_data.json` is the machine-readable form of the prose tables. It was derived once from:

| Section | Derived from | Kept honest by |
|---|---|---|
| `picks.runs` | loot tables §4a | each run stores its §4a row and option cell verbatim (`doc_row`, `doc_options`); any edit to a §4a row, a new or removed row, or a change to the bold pick rule is a `design` error until the data is re-derived |
| `items` | ids already in the repository | every literal id names the file that holds it (`source`) and must still be found there; the Crownbreaker badge resolves at run time from `state/crownhold/ids.json` (`id_from`) |
| `chart_tiers` | RUL-2026-10-28-028 item 4 table | each tier stores its RULINGS row verbatim |
| `profession_chests` | loot tables §4b; chest ids from `answers/names_item.json` | each area stores its §4b row prefix verbatim |
| `retired` | RUL-2026-10-28-016 item 3 | ids checked in their source files |
| `voice` | story bible "Never use" line | parsed at run time; only the extra "seven-bladed" phrase lives in the data |

Interpretations made while deriving (attack these in review):
- Low Tide Run "Pouch" = the Elemental Tool Pouch (the single pouch, RUL-2026-10-28-003); "Inro" = Medicine Inro.
- Night Watch's two "+ 10,000 ryo" options are package cards, as the Low Tide Run's are (§1 places both "with 10,000 ryo").
- Captain's Purse = a 100,000 ryo card (RUL-2026-10-25-010 item 3).
- The Crownhold jutsu = Lastlight (RUL-2026-10-25-006), id from `push/crownhold.gen.py`.
- Tainted runs: the Rotted Reliquary takes the Sealed Reliquary's options and the Burning Heading takes The Fall's, pick 2.
  Their Lantern 30% / Core Rot 40% are drops, not pick options, and are not checked here.
- Run quests are matched by quest id where one exists, otherwise by the quest's name on a create.

**When the design changes:** change the canonical doc first (the loot tables, the story bible or RULINGS), run the
check (it reports the divergence), then update the design data's options and verbatim fields to match, and re-run.
Never edit the doc text to match the data.

**When a pending record is created:** put its id in `items` with the repository file that now holds it.

## Not covered

The check reads manifests, not the live game: a record last written by an archived manifest is not re-checked. It does
not check drop rates, ladders, the Wreck's drops, the tainted runs' extra drops, the failed-run Core Rot consolation,
the area material id lists themselves beyond the chest tier, or the tier of chests other than the eight profession
chests ("Chests take their tier the same way", RUL-2026-10-28-028 item 4, is not yet mapped to records).
