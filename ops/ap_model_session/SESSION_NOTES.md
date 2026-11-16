
# Run 2 (full upkeep, 10 battles)
- Launch (UTC): 2026-11-16T18:45:23Z (epoch 1794854723). Safety cap = launch + 36000 s = 2026-11-17T04:45:23Z (epoch 1794890723).
- Base: main @ 5171e19c (PR 124 merged). Kit from claude/project-thread-wjpnej @ 318fe60.
- Readiness: ancestor e6686d39 OK, tnr-relay agent loaded, Tnr tool loads, node/python OK, push dry-run OK, Linux.
- Preflight: trust accepted; preflight.py --form subagent --bare-env EXIT 0, hooks true, 3/3/stand-in, kept in /tmp/tnr_preflight_q6wqvsk7.
- Ownership: lock not held; no brain process; TNR_PLAYER_LIVE unset; stopped all = true (fresh container).
- Stop: n_fight_stop.sh 10 fights. tokens.jsonl lines before launch: 0 (no live folder).

## Token figures
- Fight stop: n_fight_stop.sh detached (pid 854), log n_fight_stop.log. Timer pid 795 (deadline_timer.pid). Backup trigger: trig_01DqJBYTXs6kjQtRCVSEhR9Q at 2026-11-17T04:45:23Z.
- 2026-11-16T18:46:53Z start check:
```
{
 "batches": 4,
 "batches_with_hooks": 4,
 "game_calls_carried": 5,
 "plan_count_total": 38490,
 "plan_count_per_batch": 9623,
 "plan_count_per_call": 7698,
 "plan_count_per_fight_batch": null,
 "max_context": 7464,
 "files_in_hook_late": 0,
 "proof_reference": "PROOF.md: 4,200-4,400 a batch (one-message form), estimate 97-98% under the pre-hook live relay"
}
```
- 2026-11-16T18:52:27Z rotation 1: old relay 154753 ended, new relay be5e9c healthy. Fight 1: WON vs Mamba rd 8, Full Potion used at 619 HP.
- 2026-11-16T18:57:05Z rotation 2: relay be5e9c ended (110 tool uses, ~4 min), new 9b78e9 healthy. Fight 2: WON vs bilatralamia rd 3. Findings: 4 game refusals (battle state changed / action no longer possible) and planner out-of-time in rd 1 (fell back to defensiveStance).
- 2026-11-16T19:00:11Z rotation 3: relay 9b78e9 ended (71 tool uses, ~3 min), new relay healthy; traveling, 2 fights so far.
- 2026-11-16T19:05:29Z rotation 4: new relay 61f77f healthy. Fight 3: WON vs Noziroh rd 2. Fight 4: WON vs Mamba rd 7 (2nd fight vs Mamba). Bank: 9,899,219 ryo to pocket for training (within 10m draw). Full Potions used: 3 so far.
- 2026-11-16T19:06:54Z heartbeat 1:
```
{
 "batches": 142,
 "batches_with_hooks": 142,
 "game_calls_carried": 365,
 "plan_count_total": 2923092,
 "plan_count_per_batch": 20585,
 "plan_count_per_call": 8008,
 "plan_count_per_fight_batch": 24612,
 "max_context": 32242,
 "files_in_hook_late": 0,
 "proof_reference": "PROOF.md: 4,200-4,400 a batch (one-message form), estimate 97-98% under the pre-hook live relay"
}
```
- Finding: per-batch plan count 20,585 (fight batch 24,612) vs PROOF.md 4,200-4,400; max_context 32,242 despite 12k rotation rule. 0 files in hook/late; all 142 batches hooks true.
- 2026-11-16T19:09:10Z rotation 5: new relay healthy. Fight 5: WON vs Uesugi rd 2. Training refused once (queue full), left 0.2 h.
- 2026-11-16T19:12:41Z rotation 6: new relay healthy, traveling; 5 fights.
- 2026-11-16T19:22:56Z rotation 7 (relay 6 ran 257 tool uses, ~10 min, 59k). Fight 6: LOST vs Shisui rd 13; hospitalized, Full Potion refused (in hospital), recovery healed, armor repaired with Repair Kits.
- Finding (bank/training churn): bank draws ~9.9m to pocket for training, training finds queue full, ~9.9m goes back to bank (18:47, 19:05, 19:22). No net spend, but wasted calls each cycle. Draw is a fill-to-10m target, not cumulative.
- 2026-11-16T19:27:10Z heartbeat 2:
```
{
 "batches": 276,
 "batches_with_hooks": 276,
 "game_calls_carried": 723,
 "plan_count_total": 6629953,
 "plan_count_per_batch": 24022,
 "plan_count_per_call": 9170,
 "plan_count_per_fight_batch": 29622,
 "max_context": 50805,
 "files_in_hook_late": 0,
 "proof_reference": "PROOF.md: 4,200-4,400 a batch (one-message form), estimate 97-98% under the pre-hook live relay"
}
```
- 2026-11-16T19:28:43Z rotation 8: new relay started.
- Fight 7: WON vs Mamba rd 5 (3rd fight vs Mamba this run). Relay healthy, hunting @ sector 99.
- 2026-11-16T19:31:58Z rotation 9: new relay started.
- 2026-11-16T19:34:57Z rotation 10: new relay started.
- 2026-11-16T19:42:51Z rotation 11: new relay started.
- Fight 8: LOST vs Selaphiel rd 11. Bank/training churn again (9,950,142 to pocket).
- 2026-11-16T19:44:12Z DIRECTOR: end run early after fight 8 (bad decisions). end_session=true set by hand.
- 2026-11-16T19:45:45Z END: end_session applied 19:44:14Z; home 177, run lock released 19:44:42Z; profile read: ASLEEP, sector 177 (13,13), 5050/5050 HP, pocket 100,000, bank 934,695,653. Brain and n_fight_stop stopped, timer cancelled, backup trigger deleted.
- Final token figures:
```
{
 "batches": 390,
 "batches_with_hooks": 390,
 "game_calls_carried": 1019,
 "plan_count_total": 10730565,
 "plan_count_per_batch": 27514,
 "plan_count_per_call": 10530,
 "plan_count_per_fight_batch": 34913,
 "max_context": 50805,
 "files_in_hook_late": 0,
 "proof_reference": "PROOF.md: 4,200-4,400 a batch (one-message form), estimate 97-98% under the pre-hook live relay"
}
```
- Spending: no shop purchases. Training ~4.5m ryo (jutsu kbrQuf to lvl 19/20; the 19:22 bank cycle put back 5.43m of a ~10m pocket). 4 Full Potions used, Repair Kits once (19:22). No large ramen used at all (director asked for ramen after every fight).
- Postmortem.py crashed (IndexError, postmortem.py:169) on both losses.
