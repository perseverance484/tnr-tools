# Crafting Recipe Census - Lane A implementation handoff

- **Repository:** `perseverance484/tnr-tools`
- **Branch:** `claude/crafting-recipe-census-pln5za` (assigned implementation branch)
- **Base:** `main@fe4e69cbf88b49665c9ddcd6189e9ab4c833f123`
- **Head:** the exact SHA is reported in the handoff message. This file cannot contain its own commit SHA.
- **Integration target:** `main`
- **Owner:** Fable / Claude Code
- **Source pin:** `studie-tech/TheNinjaRPG@641040531176f91a3076fe5f32592ba18197a8c0`

## Objective

A read-only census of every craftable item and its ingredients, in both hidden states, with
coverage verified mechanically. It is the input for designing the Reagent, Armorer's and Field
Supply Caches.

## Changed files

Everything is new, under `harness/crafting_recipe_census/`:

| File | Role |
| --- | --- |
| `crafting_recipe_census.console.js` | Operator console script. It pages `item.getAll` (`canBeCrafted:true`) for `hidden:false` and then `hidden:true` until `nextCursor` is null, point-reads each id with `item.getItemWithCraftingRequirements`, then repeats both list passes as a confirmation. It is throttled and resumable through IndexedDB, and `download()` saves the raw capture. |
| `build_census.py` | Offline builder: raw capture to `craftable_recipes.json`. It fails closed with an INCOMPLETE verdict and supports `--check`. |
| `fake_server.mjs` | In-process model of the two pinned procedures, plus a virtual-clock environment. |
| `census_script.test.mjs` | Node tests for the console script. |
| `make_fixture.mjs`, `fixtures/raw_complete.json` | A deterministic fixture written by running the real script against the fake world. |
| `selftest.py` | Socket-blocked builder tests. |
| `crafting_recipe_census.user.js` | Phone-friendly userscript (added after the first handoff at `d6e4589`). It `@require`s the console script pinned to `42a1db0fbf22c61ced73eab6047436d637fc7940` (runtime 1.0.1) and adds a Run / Stop / Download / Reset / Close panel. It is inert unless the tab is armed with `#craft-census`, and issues no request of its own. |
| `userscript.test.mjs` | Tests for the userscript: header, pin fidelity, inert when unarmed, buttons, re-attach after hydration, and disarm. |
| `README.md` | Operator steps, safety properties, output contract and tests. |

Also new: `docs/handoffs/CRAFTING_RECIPE_CENSUS_HANDOFF.md` (this file). No existing file was
modified.

## Source facts relied on (read at the pin, not executed)

These are in `app/src/server/api/routers/item.ts`, `occupation.ts`,
`app/src/server/api/trpc.ts` and `app/drizzle/constants.ts`.

- **`item.getAll`** is a `publicProcedure` with `limit` 1..500.
  - It uses offset paging: `cursor*limit`, ordered by `cost`, `repsCost`, `id`.
  - `nextCursor` is null when a page returns fewer rows than `limit`; otherwise it is `cursor+1`.
  - When `hidden` is omitted the filter sets it to false. `canBeCrafted` filters only when it is
    given. `minCost`, `minRepsCost` and `minSeichiSilverCost` default to 0 and are applied as `>=`.
  - There is no role check on hidden rows.
- **`item.getItemWithCraftingRequirements`** is a `publicProcedure`. It takes `{id}` and returns
  the item with `craftingRequirements[{requirementItemId, quantity, requirementItem}]` and
  `requiredBloodline`. It returns NOT_FOUND when the id is absent.
- **`craftItem` guards:**
  - The player must have the CRAFTING occupation.
  - It rejects an item that is hidden, not `canBeCrafted`, has `parentItemId` set (an evolution
    item), or has no requirements.
  - The player's crafting rank must allow the item's rarity, per `CRAFTING_TIMES_MINS`.
  - Consumables use static times.
  - COOKING output must fit the carried cooking bucket.
  - `requiredLevel` and bloodline are not checked during a craft.
- **Rate limiter:** `slidingWindow(60, "60 s")` per procedure, keyed on the user id or, when there
  is none, the IP. Going over the limit while logged in takes 1% of money and bank and increments
  `movedTooFastCount`. For that reason the script uses `credentials:"omit"`: the requests are
  anonymous, so the penalty cannot reach the operator.

## Verification (exact commands, run at head)

| Command | Result |
| --- | --- |
| `node --test harness/crafting_recipe_census/census_script.test.mjs` | 14 tests, 14 pass, 0 fail |
| `node --test harness/crafting_recipe_census/userscript.test.mjs` | 7 tests, 7 pass, 0 fail |
| `node harness/crafting_recipe_census/make_fixture.mjs --check` | `fixture current` |
| `python3 harness/crafting_recipe_census/selftest.py` | 20 tests OK (sockets disabled in-process) |
| `python3 skills/building-tnr-content/scripts/doctrinemap.py` | exit 0 |
| `python3 skills/building-tnr-content/scripts/render_doctrine.py --check` | exit 0 |
| `python3 skills/building-tnr-content/scripts/build_packs.py --check` | exit 0 |
| `python3 skills/building-tnr-content/scripts/lawmap.py` | exit 0 |

The doctrine, law and pack gates were run only to confirm nothing moved. This change does not
touch `skills/` or the doctrine documents.

## Deviations, debt and things to attack

1. **min*Cost widened to INT32_MIN.** The brief says `item.getAll (canBeCrafted=true)`. The default
   `>= 0` cost filters would silently drop a negative-cost craftable, so the script widens them.
   This only adds rows.
2. **A console script, not a Forge capture manifest.** Forge `capture` cannot follow `nextCursor`
   and then read the ids it discovers. `pipeline.md` §1.4b warns against bespoke capture
   userscripts for jobs the builder does natively. This job is not one the builder can do.
3. **Anonymous requests are inferred to work, not observed.** Logged-out visitors reach both
   procedures through public item pages. If proxy or edge middleware rejects anonymous
   `/api/trpc` GETs, the script halts with `AUTH` and does no harm. It never falls back to sending
   credentials.
4. **Shared IPs.** With anonymous requests, the rate-limit bucket is shared by everyone on the same
   IP. At 24 requests per minute a 429 is unlikely. If one happens, it halts the run and costs the
   operator nothing.
5. **Strict snapshot rule.** Any edit to a craftable item between the first and confirmation
   passes makes the census INCOMPLETE. The fix is to rerun after `reset()`.
6. **`DUPLICATE_INGREDIENT` is advisory only.** `craftItem` validates each row on its own against
   the same inventory snapshot, so the real cost of a duplicated ingredient is ambiguous. The
   census reports each row; it does not sum them.
7. **The first phone run (userscript 1.0.0) made 0 requests and showed no error.** The root
   cause is unconfirmed. The candidates were a hung or blocked IndexedDB, or the userscript
   manager's sandbox hiding the census object. Separately, the panel swallowed `run()`
   rejections, which explains why nothing was shown. Runtime 1.0.1 fixes all three:
   - every storage operation is bounded, with a fallback from IndexedDB to localStorage and then
     to memory;
   - the census is published on both the sandbox global and the page window;
   - the panel shows errors and the census log.

   The capture format stays 1.0.0, so build_census.py is unchanged. jsDelivr serving the pinned
   commit was not checked from the container, because the proxy denied the request.
8. **Userscript on Android is untested in a real manager.** The panel was tested in a fake DOM
   only. The blob download in `download()` is the most likely thing to differ between mobile
   browsers.
9. **The fake server is a model of the pinned source, not a live recording.** The first real raw
   capture is the first live evidence of the response shapes.

## Live-game statement

- **Live requests by the agent:** 0. **Game writes:** 0. **Credentials or session material
  used:** none.
- **Not performed:** no browser run against the live site, no real raw capture, no live
  `craftable_recipes.json`. `reports/crafting_recipe_census/` does not exist until the builder
  runs on an operator capture.
- **Not begun:** cache design (Reagent, Armorer's, Field Supply), any manifest, any quest work.
- **Ghost Ship:** the fresh Ghost Ship quest capture was not read or modified, and no quest writes
  were made.
