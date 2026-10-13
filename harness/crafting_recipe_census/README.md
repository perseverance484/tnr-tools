# Crafting Recipe Census (read-only)

Builds a verified list of every craftable item and its ingredients. It is the input for designing
the Reagent, Armorer's and Field Supply Caches. Source pin:
`studie-tech/TheNinjaRPG@641040531176f91a3076fe5f32592ba18197a8c0`.

The census reads only. It creates, edits and publishes nothing, and it touches no quest. The Ghost
Ship quest capture (`push/89_ghost_ship_quests_fresh_capture.json` and its results) is separate.
This harness neither reads nor writes it.

## Why a console script and not a Forge `capture` manifest

Forge 0.5.x `capture` runs a fixed list of reads. It cannot follow `nextCursor` and then point-read
ids it has only just learned (see the `_note` in `push/66_player_facing_jutsu_census.json`). This
census needs both steps, so the operator runs a small console script instead.

## Operator steps on a phone (userscript)

1. In the browser where the Forge loader userscript is already installed, open this URL. The
   userscript manager offers to install it:
   `https://raw.githubusercontent.com/perseverance484/tnr-tools/claude/crafting-recipe-census-pln5za/harness/crafting_recipe_census/crafting_recipe_census.user.js`
2. Open `https://www.theninja-rpg.com/#craft-census`. The `#craft-census` arms that tab only, and
   a panel appears at the bottom of the page. On every other page and tab the script does nothing.
3. Tap **Run**. The panel updates every second. Keep the tab open and the screen on; if the phone
   kills the tab, reopen the armed URL and tap **Run** to resume.
4. When the status says `complete`, tap **Download** and move the saved file into
   `harvests/inbox/`.

**Stop** pauses the run. **Reset** discards the saved state. **Close** removes the panel and
disarms the tab.

The userscript adds only the panel. The census code is the console script below, loaded with
`@require` from an immutable commit; `userscript.test.mjs` checks that the pin matches the
committed `crafting_recipe_census.console.js`. If that file changes, the `@require` SHA must be
moved to the new commit.

## Operator steps on a computer (console)

1. Open any `https://www.theninja-rpg.com/` page. Logged in or not makes no difference, because the
   script sends no cookies.
2. Open DevTools → Console, paste the whole of `crafting_recipe_census.console.js`, then run
   `await TNRCraftCensus.run()`.
3. Wait for it to finish. Expect about 2.5 s per request: roughly 4 list requests, then one
   request per craftable item, then the 4 list requests again. `await TNRCraftCensus.status()`
   shows progress.
4. Run `await TNRCraftCensus.download()`. This saves
   `tnr_crafting_census_raw_<start-ms>_complete.json`. Put the file in `harvests/inbox/`.

If the run halts, the status line says why (`RATE_LIMIT`, `AUTH`, `CONTRACT`,
`TRANSIENT_EXHAUSTED` or `STOPPED`). The state is saved in IndexedDB, so to resume, paste the
script again and run `run()` again. After a `RATE_LIMIT` halt the script waits out a 65 s cooldown
before it sends anything else. `reset()` throws the saved state away. A private window with
IndexedDB disabled cannot persist state, so use a normal window.

## Safety properties

The code enforces each of these, and `census_script.test.mjs` tests each one:

| Property | How |
| --- | --- |
| Read only | GET only, and only to `item.getAll` and `item.getItemWithCraftingRequirements`. Any other procedure throws before fetch. One procedure per request. |
| No credentials | `credentials: "omit"`. No cookie or session goes out, and the script never reads one. Both procedures are `publicProcedure` queries with no role check at the pin. |
| No account penalty | The server rate limit is 60 requests per 60 s per procedure. If a logged-in caller goes over it, the server takes 1% of money and bank and bumps `movedTooFastCount` (`trpc.ts` `ratelimitMiddleware`). Anonymous requests are keyed by IP, so that penalty cannot reach the operator. |
| Throttled | One request per `throttleMs`: 2500 ms by default, and never below 1500 ms. |
| Halt, don't hammer | A 429 or `TOO_MANY_REQUESTS`, an auth error or a `BAD_REQUEST` halts at once, with no retry. Network and 5xx errors retry at most 3 times with backoff, then halt. |
| Resumable | State is saved after every request. A resumed run is byte-identical to an uninterrupted one (tested). |
| No publishing | `download()` writes a local file. Nothing is uploaded. |

### List filter

`item.getAll` runs with `{canBeCrafted:true, hidden:<false|true>, limit, cursor}`. Each hidden
state gets its own pass, starting at cursor 0 and continuing until `nextCursor` is null. The
script also sets `minCost`, `minRepsCost` and `minSeichiSilverCost` to INT32_MIN. `itemDatabaseFilter`
otherwise defaults those three filters to `>= 0`, which would silently drop a negative-cost
craftable. Widening them only adds rows.

## Offline build

```
python3 harness/crafting_recipe_census/build_census.py harvests/inbox/tnr_crafting_census_raw_<ms>_complete.json
```

The builder writes `reports/crafting_recipe_census/craftable_recipes.json`; use `--out` to change
the path. The build makes no network request. It writes the file and exits 0 only when the verdict
is **COMPLETE**, which requires all of the following:

- The capture finished under script 1.0.0 and the pinned source.
- Each pass ran cursor 0..n with no gaps.
- Every non-terminal page was full and pointed to cursor+1, and the terminal page returned
  `nextCursor: null`.
- Every row matches the filter, and no id repeats.
- Every id has an `ok` detail read whose columns equal its list row.
- The confirmation passes, taken after the detail reads, equal the first passes row for row.
- The request log names only the two read procedures.

Any failure gives **INCOMPLETE**, with reasons. The builder refuses to write an INCOMPLETE census
unless you pass `--allow-incomplete`, and exits 2 either way. `--check` rebuilds the census and
fails if the file at `--out` differs.

### Output: `craftable_recipes.json`

- `coverage`: the list filter, the pages of each pass (cursor, rows, nextCursor), whether each pass
  ended on a null cursor, drift between first and confirmation passes, detail outcomes, request
  counts by procedure and outcome, and any halts.
- `totals`: the craftable count, split into visible and hidden, plus how many players can craft at
  the pin and how many are blocked, the number with and without a recipe, the number of distinct
  ingredients, and counts by rarity, item type and minimum crafting rank, plus flag counts.
- `items[]`: one entry per craftable item. Each entry has:
  - `id`, `name`, `itemType`, `rarity` and `hidden`, plus the shop, trade, hunt, gather and event
    fields;
  - `ingredients[]`: the id, name and quantity of each ingredient, whether it is `missing`, and the
    ingredient's own hidden and source fields;
  - `craft`: the minimum crafting rank and its experience, minutes per unit (static for
    consumables), the experience the craft gives, and the output bucket;
  - `use_restrictions`: required level, bloodline and the other `required*` fields. These gate
    using the item, not crafting it;
  - `flags`, `blocked` and `craftable_by_players_at_pin`.
- `ingredients[]`: each distinct ingredient, its source fields, the recipes that use it with
  quantities, and the total units across all recipes.

Flags come from the craft guards in `occupation.ts` at the pin. The **Blocking** flags mean
`craftItem` refuses the item for every player:

| Flag | Meaning |
| --- | --- |
| `HIDDEN_OUTPUT` | The item itself is hidden. |
| `EVOLUTION_ITEM` | `parentItemId` is set. |
| `EMPTY_RECIPE` | The item has no requirement rows. |
| `MISSING_INGREDIENT` | A requirement row points to an item that no longer exists. |
| `NONPOSITIVE_QUANTITY` | A requirement quantity is below 1. |

The **Advisory** flags are:

| Flag | Meaning |
| --- | --- |
| `HIDDEN_INGREDIENT` | An ingredient is hidden. |
| `DUPLICATE_INGREDIENT` | The same ingredient appears on more than one row. `craftItem` checks rows one at a time. |
| `SELF_INGREDIENT` | The item is one of its own ingredients. |
| `LEGENDARY_FORGEMASTER_ONLY` | Only the Forgemaster rank can craft it. |
| `INGREDIENT_ACQUISITION_UNKNOWN` | An ingredient has no source flag in the census (craftable, hunted, gathered, in shop or traded). The census cannot see quest, AI or chest drops, so check this before designing a cache around that ingredient. |

`DETAIL_NOT_READ` also blocks an item. It means the detail read failed or is missing, so the
recipe is unknown. A COMPLETE census never carries it.

## Tests (socket-free)

| Command | What it covers |
| --- | --- |
| `node --test harness/crafting_recipe_census/census_script.test.mjs` | The console script against an in-process fake server and a virtual clock: pagination to null in both hidden states, anonymous GET-only to allowed procedures, throttle gaps, 429, 401, 403 and 400 halts, transient retry and exhaustion, resume byte-identity, stop and resume, and the guards. |
| `node --test harness/crafting_recipe_census/userscript.test.mjs` | The userscript wrapper: game-origin match only, `@grant none`, `@require` pinned to a commit whose console script equals the committed one, no requests of its own, inert in an unarmed tab, panel buttons drive the census, the panel re-attaches after body is cleared, and Close disarms the tab. |
| `node harness/crafting_recipe_census/make_fixture.mjs --check` | `fixtures/raw_complete.json` is the real script's output on the fake world. |
| `python3 harness/crafting_recipe_census/selftest.py` | The builder with sockets disabled: the clean fixture is COMPLETE with the expected counts, flags and restrictions; 12 mutations each fail closed; the CLI refuses INCOMPLETE; `--check` works; the fixture reproduces. |

`fake_server.mjs` follows the pinned `getAll` semantics: the hidden default, `min*Cost >= 0`
defaults, ordering by cost, repsCost and id, offset paging, and the `nextCursor` rule. It also
follows the detail relation shape. It is a model of the source, not a recording of live data.
