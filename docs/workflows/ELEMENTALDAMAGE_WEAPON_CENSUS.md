# Workflow — elementaldamage WEAPON census (operator procedure)

**Use when:** the director wants the complete, current list of WEAPON records that carry an `elementaldamage` effect, with exact record bodies, to decide which (if any) need a scaling repair.

**Who does what:** the director alone runs Forge against the live game. Fable/Claude never sends a live request. Nothing in this workflow writes to the game.

**Brief:** `docs/handoffs/ELEMENTALDAMAGE_WEAPON_CENSUS_CAPTURE_IMPLEMENTATION_20261020.md` (ChatGPT, branch `chatgpt/elementaldamage-weapon-census-handoff-20261020` @ `38740f228958020ec183bbf0950e288e455c5698`).
**Code:** `forge/src/runner/census.mjs` (Forge 0.9.0 and later). **Manifest:** `push/132_elementaldamage_weapon_census.json`. **Ledger:** `scripts/elementaldamage_census_ledger.py`.

## What the census does

One Forge job, two stages, both read-only:

| Stage | Reads | Kept |
| --- | --- | --- |
| A. Inventory | `item.getAll` with `itemType:"WEAPON"`, `limit:100`, explicitly `hidden:false` and then `hidden:true`, cursor 0 upward until `nextCursor:null`. The whole crawl runs **twice** and both passes must match exactly. Then one more crawl with `effect:["elementaldamage"]` as a cross-check. | A projection per row only: `id, name, itemType, hidden, updatedAt, effectTypes, effectsMalformed`. No raw list body is stored or exported. |
| B. Point reads | One `item.get {id}` with `persist:"full"` for every inventoried WEAPON whose effects contain `type:"elementaldamage"`, plus every row whose effects are **malformed**: not an array, or ANY member that is not an object with a non-empty string `type` (`[null]`, `[{power:30}]`, `["elementaldamage"]`). Such a row cannot be ruled out, so it is captured, never dropped. | The exact record body, in Forge's immutable capture-snapshot store, then in the results bundle. |

Each point read is checked: read ok, one row, body persisted, same id, `itemType` WEAPON, and `updatedAt` equals what Stage A saw; for a tagged target also `effects` is an array and the tag is still there. A malformed target's body is captured as evidence whatever its shape. A changed `updatedAt` is **STALE / RECAPTURE REQUIRED**.

**Why two scans:** `item.getAll` is offset-paginated (sorted by cost, repsCost, id). An item created, deleted or repriced while the crawl runs can shift rows between pages, so one pass cannot prove it saw everyone. If the two passes differ, the census says **UNSTABLE**, names the changed ids, and sends no point reads.

**Why the filter is only a cross-check:** the game's `effect` filter is `JSON_SEARCH` for any equal string anywhere in `effects`, not the effect `type`. The census decides membership by the parsed `type` itself. Rows the filter finds but the census does not (`filterOnly`) are listed for review; an exact hit the filter misses fails the inventory.

## Budget and time

Both procedures are public and rate-limited. Forge's existing budget allows 30 requests per path per minute (half the server's 60). With `limit:100`, Stage A costs about `2 × (ceil(visible/100) + ceil(hidden/100) + 2) + filtered pages` list reads; Stage B costs one `item.get` per tagged weapon. Forge waits instead of exceeding the budget, so a census of a few hundred weapons takes a few minutes. Do not run another Forge job against `item.getAll` or `item.get` at the same time.

## Procedure

1. **Before running:** avoid editing WEAPON items in the game while the census runs (an edit makes Stage A UNSTABLE or a point STALE, which is safe but means running again).
2. In Forge (0.9.0 or later), open **Manifests** and select `132_elementaldamage_weapon_census`.
3. Check the card. It must say **Read-only census item.weapon.elementaldamage**, name `hidden:false AND hidden:true`, and say **0 writes**. The button reads **Run census**. If it says anything else, stop.
4. Tap **Run census** and confirm. Signing in is not required for these public reads, but being signed in is harmless.
5. Watch the run screen. The banner reads `Census <VERDICT>: N records (V visible, H hidden), T to capture, A/T full bodies accepted · zero mutations`.
6. **If it pauses** (rate limit, network, Pause button): wait for any countdown, then **Resume**. A pause during Stage A restarts the inventory from cursor 0 (half a crawl is never kept). A pause during Stage B continues at the next weapon; reads already done are not repeated. Reloading the tab is safe at any point.
7. When it finishes, Forge exports `harvests/inbox/tnr_results_<n>.json` (committed if GitHub sync is on; otherwise use **Export results** and commit the file).

**Verdicts:**

| Verdict | Meaning | Next step |
| --- | --- | --- |
| `COMPLETE` | Both partitions fully paged, two scans agree, cross-check consistent, every target's body captured and accepted. A census with zero targets is also `COMPLETE`. | Build the ledger. |
| `UNSTABLE` | The two scans disagreed. No point reads were sent. | Stop editing, run the manifest again as a new job. |
| `STALE` | A target changed between Stage A and its point read. Its body is kept but not accepted. | Run again. |
| `AMBIGUOUS` | Every body was captured, but at least one target's effects were malformed, so whether it carries the tag was never decided. Never `COMPLETE`. | Read the malformed record(s) in the ledger's **Ambiguous** list; resolve explicitly (fix the record in the game, then run a fresh census). |
| `FAILED` | A page broke the source contract (malformed, wrong type or partition, repeated id, bad cursor, failed read), the cross-check disagreed, or a body failed acceptance / persistence. The bundle's `census.problems` and per-capture `problems` name it. | Read the problem; usually run again. |
| `INCOMPLETE` | Exported while paused. The bodies already read are in the bundle. | Resume and export again. |

Only `COMPLETE` is green; nothing else is ever presented as complete.

## Building the ledger (Fable, offline)

```
python3 scripts/elementaldamage_census_ledger.py harvests/inbox/tnr_results_<n>.json
```

Writes `reports/elementaldamage_census/tnr_results_<n>.ledger.json` (machine-readable, keyed by item id) and `.ledger.md` (readable summary). Exit 0 only for a COMPLETE census whose evidence the ledger re-verified itself; 1 if the ledger was written but the census is not complete; 2 if the bundle is not a census.

The ledger re-derives the counts, the target set and each point's acceptance from the exported rows and bodies rather than trusting the bundle's verdict, and lists any disagreement under `ledgerErrors`.

Per `elementaldamage` effect it records the calculation, power, `statTypes`, `generalTypes`, bloodline flags, the full original effect and its sha256, and one classification:

- `formula / missing statTypes`, `formula / missing generalTypes`, `formula / both missing` — **candidates** for director review;
- `formula / both present` and `non-formula / scaling not applicable` — **controls**;
- `malformed or ambiguous` — manual review;
- `already-staged Stormrender` — `cLXXf8RJv5l9B_gGsYN2a`, **ALREADY STAGED** as push/131 (integrated by PR #76, which superseded PR #73), never a new repair.

`statTypes:[]` and an absent `statTypes` are missing; `statTypes:["None"]` is present and stat-scaling-positive (legacy `"Highest"` is saved as `"None"`). Each dynamic tag on an item is classified separately. Ordinary `damage` effects are listed as context only.

## STOP / REVIEW gate

The ledger is observed evidence. A missing selector is a candidate, not proof the design is wrong, and **no repair is approved by producing it**. After the ledger:

1. Fable submits the candidate list, keyed by item id, for the director's decision.
2. The director approves or rejects each id. There is no blanket approval.
3. Only approved ids get a minimal repair manifest, built from the captured full effects, through the normal fetch-merge, `mode:"suggest"` or edit, and read-back workflow.
4. Repair manifests that assert an `elementaldamage` effects array need Forge 0.8.1 or later: the generated-contract refresh that once blocked PR #73 landed in PR #76 (`forge/src/runner/nested.json`, skill `45c`/`45g` at TheNinjaRPG@85cecae). The census itself never depended on it.
