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
| `chest-text` | every item with a `noncombatconsumereward` weighted cache follows the coloured tier-line format, with `Always:` for fixed rewards and a roll line only when the count varies (below) | loot tables §0; RUL-2026-10-28-030 |
| `voice` | player-facing text has none of the story bible's "Never use" words (whole word, any case) and no "seven-bladed" | story bible, Voice |
| `chart-tier` | chart rarity matches its tier | RUL-2026-10-28-028 item 4 |
| `prof-chest` | an edited profession chest has the rarity and hunt/gather flag of §4b; a hunt's profession id lists hold only that profession's chests of the area's tier | loot tables §4b; RUL-2026-10-28-023 |

**Option cards** follow the engine exactly (source-verified, theninjarpg@2af4b320 `libs/rewardChoice.ts`
`buildRewardChoiceCards`, `validators/rewards.ts`:172-202): every positive amount field (ryo, exp, tokens, ...) is one
card; every id in a `reward_items` entry is one card with that entry's quantity; every jutsu, bloodline, sage mode, badge
and title id is one card; every reward package with a reward is one card holding its whole payload. A direct item card
is guaranteed, so the `number` (drop chance) of a direct `reward_items` entry does not matter. A package card is granted
whole, chances included, so it is compared on its complete payload: every scalar amount, every item id with its
quantity **and drop chance**, content ids, structural outcomes (rank, village, mastery promotion, hunter/gathering drops
with their id lists), nested packages and any other `reward_*` field that carries a value. A design package option means
exactly its components, items guaranteed (chance 100): `Pouch + 10,000 ryo` is not met by 10,000 ryo plus a 1% chance
of the pouch, nor by a package that adds anything else. A package sent without a `rewards` snapshot cannot be compared
and is a warning.

**Retired records** (the Armory Requisition) may only be hidden: the item must be an `edit` whose whole `data` is
`{"hidden": true}`. Any other field (a description, content, effects, a reward anywhere) is an error.

**"Carries a reward"** (check 2a) means a value other than `0`, `false`, `null`, `""`, `"NONE"`, `"None"`, `[]` or
`{}`. Builder defaults that are zero or empty are fine.

**Player-facing text** (check 4) is every `name`, `description`, `successDescription`, `failDescription`,
`drawDescription`, `fleeDescription`, `battleDescription`, `displayName` and choice `text` inside a quest, item, jutsu or
other record's `data`, including effect descriptions; for AIs only `username`. Objective ids, AI rule descriptions,
asset records and the manifest's own item labels are not player-facing and are not scanned. The word list is read from
the story bible at run time, so editing the bible's "Never use" line changes the check; words match whole, without
inflection (`lift` matches "lift", not "lifts").

## Chest description format (RUL-2026-10-28-030, loot tables §0)

The format of record is the HTML template in loot tables §0; this is how the checker reads it. Every item whose effects
include a `noncombatconsumereward` with `rewardMode: "weightedCache"` must send its `description` in the same edit (an
edit that sets the cache without the text fails: the live text could not be shown to match). The description is split
into lines on `<br>`; the story line and `<b>Each roll:</b>` are free text and not checked.

1. **One coloured tier line per tier**, matched exactly as
   `<span style="color:#xxxxxx"><b>{Tier} {p}%</b></span> · {items}`:
   - colour by tier name: Common `#9ca3af` (grey), Rare `#3b82f6` (blue), Epic `#a855f7` (purple), Legendary
     `#f59e0b` (gold); a tier with any other name has no colour and fails;
   - `{p}` is the tier's weight in whole percent, rounded half up (weights are basis points, 10000 = 100%); tiers that
     share a name are summed and get one line (the Archive Chart Case's two Legendary tiers, 3 + 5, read
     `Legendary 8%`); zero-weight tiers get no line;
   - `{items}` lists the tier's entries in cache order, joined with ` <i>or</i> ` or ` or `; past three entries, the
     first three then ` and more` (`, and more` accepted). An item reads `Name`, or `Name ×n` when the quantity is above
     1. An entry that bundles several items joins them with ` + ` (the ruling does not cover bundles; this is the
     checker's reading). Tags inside the list are ignored when comparing. An item whose name the repository does not
     know (design data, `answers/names_item.json`, or a named item in the same manifest) makes that tier's list a
     warning instead of a check;
   - no line may name a tier the cache lacks, and a tier rate written outside this format (e.g. a plain
     `Legendary 2%`) fails.
2. **`<b>Always:</b> …`** appears if and only if the item has a fixed reward (another `noncombatconsumereward` effect,
   paid on every opening). Its entries are split on ` · `, `, `, ` + `, ` and ` or ` or ` and compared whole, as a
   multiset, with the item's fixed rewards: ryo as `150,000 ryo`, exp as `5,000 exp`, items as `Name`, or `Name ×n`
   above 1 (so `Medicine Inro ×1` and `Medicine Inro ×99` both fail for a fixed Medicine Inro). A fixed reward the line
   leaves out, and an entry the item does not grant, are both errors. An item name containing one of the separators
   would be split; none of the Skyglass items does.
3. **A roll line** is required only when the roll count varies: `<min>–<max> rolls` (an ASCII hyphen is accepted),
   e.g. `<i>3–6 rolls.</i>`. A fixed roll count is not required, because the item card already shows the cache's roll
   odds; a roll line on a fixed-count cache is a warning (§0: "not repeated").

Example (the Sealed Treasury shape):

```html
<i>Crownhold's own coffers.</i><br><br>
<b>Always:</b> 150,000 ryo<br>
<i>3–6 rolls.</i><br>
<b>Each roll:</b><br>
<span style="color:#9ca3af"><b>Common 45%</b></span> · Imperial Gold ×5<br>
<span style="color:#3b82f6"><b>Rare 35%</b></span> · Rare Jewels ×10<br>
<span style="color:#a855f7"><b>Epic 15%</b></span> · Imperial Gold ×15<br>
<span style="color:#f59e0b"><b>Legendary 5%</b></span> · Unobtanium ×5
```

The rendering itself is checked on the director's phone through a hidden test item (§0); this tool checks the text only.

## The design data

`state/skyglass_design/design_data.json` is the machine-readable form of the prose tables. It was derived once from:

| Section | Derived from | Kept honest by |
|---|---|---|
| `picks.runs` | loot tables §4a | each run stores its §4a row and option cell verbatim (`doc_row`, `doc_options`); any edit to a §4a row, a new or removed row, or a change to the bold pick rule is a `design` error until the data is re-derived. The values are bound too: every run's `pickCount` and `options` are re-parsed from the §4a cell on each run (the header's `(pick 1)`, a row's `**pick N**`; options split on ` / `, packages on ` + `, `N ryo`, `Name ×n`), and data that disagrees with the parsed values is an error |
| `picks.doc_aliases` | §4a's short names | names §4a uses that are not an item's own name (`Pouch`, `Inro`, `Crown Fragment`, `Crownhold badge`, `Crownhold jutsu`); `Captain's Purse` is a 100,000 ryo money alias whose ruling sentence (RUL-2026-10-25-010) is checked verbatim, and whose `money` must equal the ryo amount that sentence states. Every other option name must equal an item's name exactly |
| tainted runs | §4a "pick 2 from their rare's options" | `options_from` plus `doc_evidence`: the §5 lines tying each tainted run to its rare chart and that chart to its run, checked verbatim; `options_from` must equal the run those two lines derive |
| `items` | ids already in the repository | every literal id names the file that holds it (`source`) and must still be found there; the Crownbreaker badge resolves at run time from `state/crownhold/ids.json` (`id_from`) |
| `chart_tiers` | RUL-2026-10-28-028 item 4 table | each tier stores its RULINGS row verbatim |
| `profession_chests` | loot tables §4b; chest ids from `answers/names_item.json` | each area stores its §4b row prefix verbatim |
| `retired` | RUL-2026-10-28-016 item 3 | ids checked in their source files |
| `voice` | story bible "Never use" line | parsed at run time; only the extra "seven-bladed" phrase lives in the data |
| tier colours (in the script, `TIER_COLOURS`) | loot tables §0 template (RUL-2026-10-28-030) | each colour/tier pair must still appear in §0's template |

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
