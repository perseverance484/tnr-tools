# AI player run 2 follow-up: independent review

Date: 2026-11-17. Reviewer: ChatGPT. **Verdict: changes requested.**

The token correction and the three desperate-lookahead modes check out. The requested guarantees are not all met: an unsuccessful heal still permits a new attack, AI postmortems silently skip their turn analysis, the no-engine review test needs an undeclared runtime directory, and `keep`'s explicit-path validator accepts unrelated files inside the fights tree. The Ring assertion is a reasonable change of scope, with a smaller test weakness described below.

## Target and boundaries

- Repository: `perseverance484/tnr-tools`.
- Frozen implementation: `fable/ai-player-run2-followup` at **`e051d0622d9861032b583276b8b95cd96d1d6287`**.
- Comparison base and verified merge-base: **`0b52988dec3a018cabae7b3aa36363b82407ca01`**.
- Review branch: `chatgpt/review-ai-player-run2-followup-20261117`, based directly on that target.
- Read `docs/reviews/AI_PLAYER_RUN2_FOLLOWUP_HANDOFF.md` first. Also read the repository review workflow, operating guides, relevant rulings, implementation, tests, and recorded evidence.
- `main` had advanced to `f22ebcaf793f1922a7de0528355be1fa3453c63f` at clone and `18b3de5fc2b689b84161e34833c582c3d0c7003c` at the final pre-publication ref check. Neither was substituted for the specified base. The fable ref still matched the target at that check.
- This branch adds only this review. No implementation change, merge, game request, game write, run lock, relay/model session, or live credential use. Test processes ran with IPv4/IPv6 socket creation denied; `keep` push reproductions used a temporary local bare repository.

## Findings

### F1 — P2: the full-health rule still permits an attack after a failed heal

**Contract mismatch; retained behavior, not a new regression in the threshold arithmetic.** Relevant locations: `player/config.py:47`, `player/activities/recovery.py:34-35,60-62`, `player/activities/pvp_hunt.py:64-67`, and `player/tests/test_activities.py:99-105`.

RUL-2026-11-17-165 says never to start a fight with HP missing. `HEAL_BELOW = 1.0` correctly initiates healing at 5049/5050. But when the next profile still has the same HP, recovery marks HP healing broken for 600 seconds and becomes unavailable. Neither the hunt nor its attack gate requires full HP. A target in the next scan is attacked during that interval.

Reproduced through the real brain with its existing offline `Rig`:

```python
from player.tests.support import Rig, user, scan, res
r = Rig()
target = ('user_testOpponent', 'Target', 10, 10, 'AWAKE', 100,
          'enemyVillage', None, None)
a = r.tick(user(hp=5049), scan([target]))
b = r.tick(res('item.consume', {'success': False, 'message': 'Unavailable'}),
           user(hp=5049), scan([target]))
print(a['activity'], r.calls(a))
print(b['activity'], r.calls(b))
```

Observed:

```text
recovery ['item.consume', 'profile.getUser']
pvp_hunt ['jutsu.getPublicUserJutsus', 'combat.attackUser', 'profile.getUser']
```

The two new tests establish the threshold and closing-batch potion, not the promised invariant after an unsuccessful heal. An existing test explicitly expects hunting to resume after an unchanged heal. The handoff acknowledges this limitation; that disclosure is accurate, but the unconditional ruling/config claim remains unfulfilled.

**Smallest correction:** retain the retry backoff, but prevent initiating a fight while known HP is below maximum. Cover unsuccessful/no-change healing followed by a valid target, recovery to full HP, and continuation of an already-running battle. Update the older test so suppressing potion retries does not imply permission to attack.

### F2 — P2: AI postmortems return successful-looking empty turn analysis

**Incomplete fix / misleading report.** Changed locations: `state/player/dauntless/tools/postmortem.py:113-119,133`; downstream cause: `state/player/dauntless/tools/engine_check.py:34-39`.

`critique.opponent_of` correctly finds the AI. However, `postmortem.review` still obtains positions from `EC.positions`, which filters actors to `user_` IDs and returns immediately unless it finds two players. Consequently, no turn reaches `swings`, and the new `engine` field remains `True`, even with the engine explicitly absent.

Full `postmortem.review` on the committed Arsenal Keeper log `1nKLV-oUazfAEWA6OSfBi` produced:

```text
log rows: 9
distinct rounds where I acted: 2
EC.positions: 0
postmortem: opp='Arsenal Keeper', engine=True, turns=[], errors=4
```

The replay-rule review runs, but the per-turn opponent/read/damage/choice analysis does not. The command no longer crashing must not be interpreted as full postmortem coverage. `test_review_tools.py` exercises the AI path only through the critique CLI; its postmortem integration case is a player-vs-player loss, so it misses this.

**Smallest correction:** either support the selected AI actor throughout position construction, or explicitly report the per-turn analysis as unsupported/unmeasured with a reason and no affirmative engine flag. Add an AI postmortem test that verifies coverage or an explicit limitation, not just exit status. This does not require pretending the existing PvP-specific critique rules are appropriate for every AI.

### F3 — P2: the new no-engine integration test fails in a clean checkout

**Reproducibility gap in the claimed no-engine path; underlying helper predates this change.** Locations: `state/player/dauntless/tools/tests/test_review_tools.py:74-90`, `postmortem.py:135`, and `engine_check.py:85`.

The first run of `test_review_tools.py` at the target exited 1 before reaching `swings`:

```text
FileNotFoundError: .../state/player/dauntless/fights/live/ECHK_bases.json
```

`EC.exact_inputs` writes into `fight_bases.LIVE` without creating it. `fights/live/` is gitignored and absent from a fresh clone. Setting `TNR_POSTMORTEM_OUT` to a temporary directory isolates the final report but does not redirect or create this intermediate directory.

After explicitly creating `state/player/dauntless/fights/live/`, the identical test command passed all four checks: the loss contained 12 turns, six replay findings, `engine=False`, and null regrets/swings. This isolates the failure to runtime-directory preparation, rather than the `swings` calculation.

**Smallest correction:** make the intermediate writer establish its directory, and make the test independent of an existing play checkout. Prefer redirecting intermediate bases into the test's temporary folder as well. Re-run the test with no pre-existing runtime directories.

### F4 — P2: `keep` does not enforce its stated per-fight file boundary

**Contract mismatch in the touched validator; broad subtree acceptance is inherited.** Location: `player/keep.py:62-67`, especially `rel.startswith(home)` at line 65.

The new kit allowlist itself is appropriately narrow: exact membership in the selected log's player IDs, excluding self, AI IDs, and malformed IDs. However, the other half of `_rel` accepts every path below `state/player/<account>/fights/`, independent of `bid`. The updated module promises that any other path is refused, and the validator now calls its rejection “not a file of this fight.” That is stronger than the implementation.

In a temporary working repository with a temporary local bare `origin`, both of these calls successfully committed and pushed the named file under fight A's commit message:

```python
keep.keep('fightA', [f'{fights}/fightB_entries.json'])
keep.keep('fightA', [f'{fights}/unrelated.txt'])
```

No real repository remote was used for these reproductions. Conversely, unrelated-player, self, and AI kits were rejected. `fight_files('fightA')` returned only its own entries and the named opponent's kit. Thus the normal collector passes, but an explicit path supplied through the public `keep(..., paths=...)` API bypasses the claimed exact-file boundary. The current positive-path tests do not disprove that bypass.

**Smallest correction:** validate against the exact five artifact paths for this `bid`, plus its authorized kit paths, instead of the whole fights-directory prefix. Add negative tests for another fight's file and an arbitrary file inside the otherwise permitted subtree. Reject them before Git fetch/commit/push.

## Checks that held

### 1. Token definition and independent run 2 recount

`PROOF.md` defines `0.1 * cache_read + 1.25 * cache_written + fresh_input + 5 * output`. `relay._usage` at `player/relay.py:219-228` makes `in = fresh + written + cached`; `proof_read.py:148-150` subtracts cached and written from that total. `player.tokens.plan_count` agrees, including the conservative fallback when cache counts are absent. The new hourly plan total and `brain tokens` use the same function.

Data provenance: `ops/ap_model_session/run2/tokens.jsonl` from `origin/claude/ap-live-run-dauntless-goqgbz` at **`fe5848b17bd89d5cefff42534c0599fd1ca7dca5`**, blob **`c0e5e56214b6d5ad59c24f9146868d0a593bce83`**. Extracted with `git show` into scratch, never copied into the player's live folder. An independent Decimal calculation agreed with `plan_count` on every row.

| Rows | Count | Weighted total | Mean per batch |
|---|---:|---:|---:|
| All | 390 | 1,922,780.60 | 4,930.206667 |
| Battle tagged | 222 | 1,215,453.15 | 5,475.014189 |
| Other | 168 | 707,327.45 | 4,210.282440 |

Other checks: all 390 have hooks and cache figures; 1,019 calls; rounded weighted total 1,922,781; weighted cost per call 1,887; mean context 19,123, maximum 50,805. Rounded per-batch components are cache read 2,190, cache write 853, output 1,885, plus fresh input 2.34359 (914 total). The erroneous formula reproduces 27,514.268205 per batch.

The 67 rows with aggregate input greater than last-request context average 6,770.679104; the remaining 323 average 4,548.436842, consistent with the handoff's multiple-request comparison. Operator-session tokens are absent and cannot be inferred from this log. The relay-replacement savings estimates and run 1's count were not independently re-established.

### 2. `swings` and `opponent_of`

`swings([], n)` and mismatched-length results correctly produce the falsey `UNMEASURED` sentinel and exactly `n` null scores. A complete result list preserves legal exchanges and individual rejected bundles as `None`. This keeps the existing guarded damage access and regret calculation safe. The missing-engine player loss passes once the intermediate directory exists (F3).

`opponent_of` preserves player preference and actor order, falls back to the first non-self AI actor, and returns `None` for a self-only/empty-actor log. The critique CLI handles the AI fixture and emits a useful error instead of a traceback for a self-only log. The issue is its downstream use in postmortem (F2), not the helper's tested selection contract. Multi-opponent/team correctness was not established.

### 3. Desperate lookahead

The setting defaults to `all`. Under `all`, the additional `P.desperate` bookkeeping does not change `rank` ordering, the candidate prefix, or the lookahead calculation. `alive` limits lookahead to `min(LA_K, P.desperate)` leading survival candidates; `off` returns the existing order before any lookahead. Outside desperation, all modes retain the ordinary lookahead behavior. Budget and fewer-than-two-scored-candidates behavior remain unchanged.

The new synthetic test passed the exact orders and lookahead-call counts for all three modes and the non-desperate control. The DDXXD fixture produced:

| Mode | Fired line | Reported death probability |
|---|---|---:|
| `all` | Basic Heal + Chakra Resistance | 99% |
| `alive` | Thunder's Judgement + Basic Heal | 67% |
| `off` | Thunder's Judgement + Basic Heal | 67% |

Independent differential check: loaded base and target planner source in separate fresh Python processes against the **same target data/kits**, with the setting unset and a fixed clock so all 20 lookahead candidates could be evaluated. Full scored ranking and full reranked order were identical on `ddxxd_r8.txt` (588 candidates), `mamba_r5.txt` (833), `mamba_r3.txt` (627), and `anbu_r3.txt` (515). This isolates the setting's default; it does not claim the six added kits cannot change decisions versus the complete base tree. It also does not eliminate ordinary wall-clock budget sensitivity.

### 4. Saved kits

All six added kit files are byte-for-byte identical to their versions on the run branch identified above. Normal collection deduplicates opponent IDs, accepts only matching `user_[A-Za-z0-9]+` IDs, and excludes self. Unrelated-player, self, and AI kits were rejected before any push; author tests also cover presenting the same kit for a different fight. The remaining exact-file-boundary issue is F4.

### 5. Healing threshold

Both new tests pass: 5049/5050 and 4900/5050 trigger healing before hunting; full HP does not. The closing batch heals at 5000/5050, does not heal at full HP, and leaves a lost fight's zero HP to the hospital path. These are sound tests of the threshold change, but do not establish the broader “never start wounded” rule (F1).

### 6. Is the changed Ring check fair?

**Yes as a test of the selected move, with a P3 coverage caveat.** Requiring every movement candidate in the top twelve to leave the Ring was stronger than the selection rule: candidates with different follow-up ranges need not share the same useful destination. At this target the fifth line is `replace@5,3 -> stormblade -> basic`; the selected line is `replace@9,1 -> jewel -> stormblade`. The selection leaves the Ring. The adjacent tests still check the 54 ground tiles and the actual 0.8-versus-1.0 damage multiplier when landing on/off them. I found no basis to restore the old blanket top-twelve requirement.

However, at `tests/test_critique.py:271-273`, missing `FIRE` becomes `fire or []`, and `all(...)` then passes vacuously. In a scratch mutation of subprocess output, deleting **only the round-5 FIRE line** still let the whole test exit 0. Changing its emitted movement destination to `(7,5)` correctly made the test exit 1. Thus it does catch a bad emitted Phantom Step/Replacement, but does not prove the advertised move was emitted at all.

**Suggested test refinement:** assert successful subprocess exit and a valid nonempty `FIRE` result before inspecting movement destinations. Keep the selected-move criterion and the direct ground-effect assertions. If this particular fixture is intended to require a movement action, assert that explicitly too; do not impose it as a general planner rule.

## Verification record

All commands below used the target implementation, Python 3, no engine app, `TNR_LEARN=0`, and an inherited scratch `LD_PRELOAD` shim rejecting `AF_INET`/`AF_INET6` socket creation. No production transport was invoked. Scratch scripts and logs remained outside the tracked tree in `/workspace/scratch/run2-review/`.

| Check | Result |
|---|---|
| `python3 -W ignore::ResourceWarning -m unittest discover -s player/tests -t .` | 681 tests, OK |
| `python3 -W ignore::ResourceWarning state/player/dauntless/tools/tests/test_review_tools.py` | Fresh clone: exit 1 (F3). After creating ignored `fights/live/`: exit 0, all four checks |
| `python3 -W ignore::ResourceWarning state/player/dauntless/tools/tests/test_loss_fixes.py` | Exit 0; all three modes and real DDXXD fixture checked |
| `python3 -W ignore::ResourceWarning state/player/dauntless/tools/tests/test_critique.py` | Exit 0; 75 assertions |
| `python3 -W ignore::ResourceWarning state/player/dauntless/tools/tests/test_planner2.py` | Exit 0; parity 4000/4000 |
| `python3 -W ignore::ResourceWarning -m unittest docs/reviews/evidence/ai_player_hook_relay/test_preflight.py` | 44 tests, OK; no relay sessions launched |
| `python3 docs/reviews/evidence/ai_player_hook_relay/fake_connector.py --selftest` | Exit 0 |
| Independent Decimal token recount | All 390 rows agree |
| Independent base/head planner comparison, four isolated fixtures | Full rankings and lookahead orders identical |
| Failed-heal brain reproduction | Attack emitted while HP remains 5049/5050 (F1) |
| Committed AI log through full `postmortem.review` | Empty turn analysis with `engine=True` (F2) |
| Temporary local Git `keep` reproduction | Unauthorized kits rejected; unrelated in-tree files pushed (F4) |
| Ring subprocess-output mutations | Missing FIRE: exit 0; on-Ring emitted move: exit 1 |
| `python3 scripts/rulings_index.py --check` | 337 rulings; index current |
| `python3 scripts/check_large_files.py` | 17 grandfathered large files; 0 unallowed |
| `python3 scripts/check_no_real_name.py` | 0 hits |
| `git diff --check 0b52988d HEAD` | Exit 0 |

The two committed loss reports' internal totals agree with the handoff: Shisui 12 turns / 1,502 summed regret / 11 low-probability replies / six replay findings; Selaphiel 10 / 3,119 / eight / four. I did not rerun the game engine at `df864509f8b33f4c9cf8332fd416ab511d2f0478`, `tune_real`, or the simulator win-rate experiments. Those engine-derived measurements remain author evidence, not independently reproduced results of this review. No browser/live behavior was tested.

## Next step

Fable should correct F1-F4 or return an explicit, narrower contract for review, and strengthen the Ring output assertion. Return a new frozen SHA. A focused re-review can cover healing after failure, postmortem coverage/status and fresh-directory startup, exact `keep` path validation, and the Ring test, provided no wider planner/data changes are included. Preserve the verified token formula and the default `all` behavior. This review does not authorize integration or live play.
