
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
