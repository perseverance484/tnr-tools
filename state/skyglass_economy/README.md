# Skyglass economy model

A model of the whole Skyglass event economy you can rerun, built so the director can retune any rate and see time-to-goal for three
player types. This is analysis only: it made zero live requests and used no credentials. Nothing in `push/` or any manifest changed.

```bash
python3 state/skyglass_economy/model.py            # about 4 minutes; writes out/*.csv
python3 state/skyglass_economy/model.py --quick    # smoke test (60 players per cell)
```

- **`inputs.json`** holds every rate, with its `source` (file:line, ruling id or harness result) or a `flag`
  (ASSUMPTION / PROPOSED / PLACEHOLDER / TOGGLE / CONFLICT). To change a rate, edit its `v` and rerun.
- **`recommended.json`** holds the proposed changes as dotted-path overrides. The model runs `current` (inputs.json as
  is) and `recommended` (all changes applied together).
- **`out/`**
  - `activity_yields.csv`: expected items per run and per hour for every activity (the uber per player type, the Haul
    per route policy), plus the Tide/Roster loop.
  - `time_to_goal.csv`: p50/p90 in hours and weekends, without and with trade, for each player type and goal.
  - `flows.csv`: sources and sinks per weekend (8 simulated weekends, 200 players).
  - `recommended_changes.csv`: each change with its rationale and its effect on its own, then the combined before/after.
  - `run_meta.json`: the run settings.
- The model uses the standard library only. A fixed seed makes it deterministic: two full runs gave identical CSVs.

## How it works

- **Time.** Time is continuous play hours, and weekends = hours / hours per weekend (Casual 3, Dedicated 10, Hardcore
  25). Inventory carries over: the event repeats every weekend and nothing is capped per day.
- **Policy.** At each step the player takes the first action that applies:
  1. buy a missing shard with Salvage (rarest first);
  2. assemble An Invitation in Glass (4 distinct shards, self-service);
  3. fight the uber;
  4. run the best chart held: Lantern, then tainted, then steep (when Rot ≥ 3) or run an Epic chart, then a Haul page,
     then Watch > Archive > Foundry > Buried Cache > Roster > Tide;
  5. otherwise farm the full Wreck (a party of three; every drop rolls per member).
- **Picks.** Take cards that feed the ladder (the Archive Chart Case, the Foundry chart) and the Skyglass Token where no
  chart card exists. Commons take the Inro (see finding 5). Crownhold takes the Crown's Hoard.
- **Haul route.** Casual and Dedicated take the highest-EV measured route on each page. Hardcore takes the route with
  the most expected Reserve chests.
- **Runs.**
  - A failed run costs half its minutes (the Wreck: its one-hour clock) and pays nothing (RUL-2026-10-31-080).
  - Press-on rooms are always taken: a loss there keeps the ending (`push/skyglass_charts.gen.py:387-396`,
    `push/skyglass_update.gen.py:199`).
  - Steeping is on (RUL-2026-10-30-060 item 10).
- **Monte Carlo.** 400 players per cell, each followed for up to 600 play hours. A goal not reached by then is reported
  as `>cap`, with a steady-state estimate (Heartglass ln2/(keys/h × clear); Remainder N/(keys/h × clear)).
- **Trade variant** (simple, as asked):
  - duplicate shards swap 1:1 for a missing one;
  - 50% of loot value buys missing shards at a fair price, defined as the Dedicated policy's ryo-equivalent income per
    hour × its hours per shard produced. That is 118M ryo now and 22M recommended.
  - Keys, Remnants and variant tokens are never traded in the model.

## Time to goal (weekends, p50 / p90, no trade → with trade)

| Goal | Casual (3 h) now | Casual rec. | Dedicated (10 h) now | Dedicated rec. | Hardcore (25 h) now | Hardcore rec. |
|---|---|---|---|---|---|---|
| First chart run | 0.2 / 0.6 | same | 0.06 / 0.2 | same | 0.03 / 0.07 | same |
| First Haul run | 0.6 / 1.8 | same | 0.16 / 0.5 | same | 0.08 / 0.2 | same |
| First Crownhold | 3.5 / 9.4 | same | 0.8 / 2.8 | same | 0.4 / 1.2 | same |
| **First Invitation** (target 4 / 1-2 / <1) | **19.3 / 25.6** → trade 12.9 | **3.9 / 5.3** → trade 2.6 | **5.8 / 7.7** → trade 3.9 | **1.2 / 1.6** → trade 0.8 | **2.3 / 3.1** → trade 1.5 | **0.49 / 0.65** → trade 0.3 |
| Heartglass (first clear) | est ~400 | 80 / >200 | est ~71 | 14 / 52 | 9.7 / >24 | 2.1 / 6.9 |
| The Remainder | est ~4,600 | est ~440 | est ~820 | est ~79 | est ~100 | 10 / 17 (at 4 Remnants) |
| All 12 skins (tokens) | 10.4 / 18.5 | same | 3.5 / 5.3 | same | 1.4 / 2.3 | same |
| All 6 boss variants | >cap for ~55% | same | >cap for ~55% | same | >cap for ~55% | same |

"same" means the change does not touch that goal (differences are Monte Carlo noise). The full table is in
`out/time_to_goal.csv`.

## Top findings

1. **The Invitation is 4-5× too slow, and its pace is set by Salvage, not the drops.** With the proposed rates a
   dedicated player makes about 0.32 shards a weekend from drops (Keel 0.18, Crown 0.10, Tide 0.04, Ledger 0.03) and
   0.44 from Salvage. Every player type needs about 55-58 play hours for a key, against a target of about 12 hours for
   all three. The targets come to the same number of hours: 4×3, 1-2×10 and <25. The model's policy is the same for
   every type except the Haul route and the uber clear rate.
2. **The Shard of the Ledger is a dead end.** Reserve chests come only from step-5 lockers or the Ore Vault, so the
   highest-value route pays one on 1 page in 6. The result is 0.007 Ledger shards per Haul run (0.024 even when chasing
   Reserves). Fix R1 ties the shard to the Haul clear.
3. **Haul pages are about 3× the RUL-2026-10-30-060 target.** A dedicated 10-hour weekend gets 4.1 Haul runs (target
   about 1.5). The earlier `tools/economy.py` (rule-cap branch) counted 2 pages, not 6 (`w["haul"] += 2 * haul_wreck`),
   so the 1.26 it measured, and the 2.4%/3% chosen from it, are about 3× low. This is left unchanged here: it is a
   director-set live value, and R1 relies on the Haul volume.
4. **The uber's long goals do not suit Casual or Dedicated players.**
   - At the brief's clear rates (3% / 5% / 15%), even with R1-R6 the Heartglass takes a median of 80 / 14 / 2
     weekends.
   - The Remainder at 8 Remnants needs about 53 keys at 15%: about 22 hardcore weekends with R1-R6, and 100 or more
     today.
   - Remnants come in at 0.007 a dedicated weekend today.
   - The clear rate, not drop rates, dominates here (R7 is a proposal; there is no target).
5. **Outliers.**
   - **(a) The Tide↔Roster loop.** The Low Tide pick offers a Watch Roster and the Night Watch pick offers a Tide
     Chart, both at a 100% clear. A player who always takes the chart card loops forever, solo and with no party:
     2 Buried Cache charts and 3 Core Rot an hour, about 10× the Wreck's Rot rate.
   - **(b) Boss variants.** The First Blade and Wayfinder variants come at about 0.02 a dedicated weekend (about 45
     weekends each), so "all boss variants" is out of reach for about 55% of every type within the cap.
   - **(c) Dry streaks.** At 1% Keel, 37% of players go 100 Wreck clears without one (1.7% at the recommended 4%).
6. **Pile-ups and sinks.**
   - Medicine Inro (4.5) and Elemental Tool Pouch (5.9) pile up each dedicated weekend.
   - Core Rot is fully spent for Dedicated and Hardcore players, but casual players bank about half (1.06 in, 0.55
     out).
   - Lanterns are all spent (about 0.9 Crownhold a dedicated weekend).
   - Salvage has one sink in this policy: shards.
   - With R5/R6 a shard costs 35 Salvage, less than an Archive or Watch chart (40).

## Recommended changes (`recommended.json`)

| Id | Change | Dedicated first-key p50 hours, this change alone (now 57.6) |
|---|---|---|
| R1 | Ledger shard: 5% per Reserve chest → **15% per Haul clear** | 46.7 |
| R2 | Keel shard 1% → **4%** per full Wreck clear | 49.4 |
| R3 | Crown shard 15% → **40%** per Crownhold clear | 45.2 |
| R4 | Tide shard 3% → **25%** (Sealed Reliquary, The Fall, both tainted runs) | 46.1 |
| R5 | Salvage 3 → **5** per full clear (Faded 1 → 2) | 37.1 |
| R6 | Shard exchange 100 → **35** Salvage | 25.3 |
| R7 | The Remainder 8 → **4** Remnants (optional; no target) | n/a |

Together, R1-R6 bring the first Invitation to 3.9 / 1.2 / 0.49 weekends (p90 5.3 / 1.6 / 0.65). Each change alone
falls far short, because the key waits on the rarest of four shards. After R1-R6, Salvage still buys about 57% of
shards. If the director wants drops to dominate, raise R2-R4 further and the Salvage cost back up together.

## Assumptions (all editable in inputs.json)

- **Run times.**
  - Harness minutes at **15 s per round**.
  - Wreck: 23.0 min (rule-cap §7) plus **3 min party overhead**.
  - **0.5 min claim overhead** per run.
  - **A failed run costs half its minutes**.
  - Press-on rooms: **+1 to 2 min**.
- **Uber.**
  - **32.5 min** per fight (the brief's 25-40); a loss costs **60%** of that.
  - Clear rate per attempt: **Casual 3%, Dedicated 5%, Hardcore 15%**, flat (no learning curve).
  - Exp and ryo: 0 (RUL-095 gives no figure).
- **Crownhold:** the clean route at 75%.
- **Haul.** Route clear rates are the harness's 40-seed values (±15 points).
- **Captain's Watch:** no terms, at 80%.
- **Break the seal:** off; the echo fight has no measurement.
- **Item values.**
  - Ryo values come only from the loot tables and the Haul doc.
  - Coffer, Token, Galley Stores and charts are valued at 0 (no price data); this only affects the trade budget.
- **Trade.** A 50% budget share, a 1:1 shard swap, and the auto fair price.
- **Solo pyramids** (held): off by default. Their 6 min / 95% are placeholders.
- **Players.** All three types are level-100 endgame players who can always form a Wreck party.
- **Pending rulings and conflicts.**
  - Crownbreaker is excluded (deferred).
  - The second Heartglass (5 Remnants, RUL-095 item 3) is off.
  - **CONFLICT:** RUL-2026-11-01-093 says the key is untradeable; the brief says keys are tradeable. The model never
    trades keys, so this does not change the results.
