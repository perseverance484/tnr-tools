# AP model live gate: launch checklist for the fresh session (from main)

Read this whole file, then PREFLIGHT.md and SESSION_NOTES.md. Notes here are a colleague's claims: check each against the repo and the game before relying on it.

## Authority and scope
- Approved head: fable/ai-player-hook-proof @ e6686d39735a6065dd53afa7c402725878cfed60 (review 2cf1969e closes C1/C2; bf2231f6, aa73867c, e6686d39 approved). Merged to main 05:48Z Nov 16 as d20d7514, ruling RUL-2026-11-16-162 at fb4000dd (main head then). player/, .claude/ and the hook-relay evidence on main are identical to e6686d39. Do not edit any fable/* branch.
- The director's words: "Go. Turn the pilot off, AP model is in charge now" (05:27Z) and "Its over. Begin" (05:30Z, Nov 16).
- Reviewer's scope for the first live gate: ONE live PvP session, Haiku tnr-relay started as a SUBAGENT, upkeep activities OFF, token figures recorded, anything in live/hook/late/ counted.
- DECIDED, the director 05:42Z Nov 16: "Short, upkeep off to test and measure token reduction. Then we go full bore". So THIS run: short, upkeep off, measure tokens. The 10-hour upkeep-on run comes after, as a separate launch.
- Length, the director 05:44Z: "Just 1 battle". The run hunts until ONE fight ends, then shuts down in order (home, sleep, lock released). scripts/one_fight_stop.sh sets end_session=true at the first fight_end event after launch (tested 05:45Z against a fake repo). A 2-hour safety cap (7200 s, prep thread's reversible default) stands behind it in case no fight comes.
- Hunt rules to keep (his words in memory): level 100s only, 85-99 only with a public win rate of 60%+ (hidden = skip), humans only, do-not-attack list. KNOWN GAP: the brain's own filter is MIN_LEVEL = 90 with no win-rate check (player/config.py, pvp_hunt.py); no setting changes it, and code is not changed. The director must say whether that is acceptable for this test before step 6.
- Do-not-attack: do_not_attack.md on main lacks Keoshi and Jazu (no end date per his words). Add them through the brain's own setting at configure time (step 5). Sector 210/event players: the hunt is not expected to go to 210; if status shows sector 210, set end_session=true.
- Never: relay_without_hooks=true, payments, chat, moderation, Flee, other players' data. Do-not-attack: Keoshi, Jazu, AngelSaber (no snipe), sector 210/event players. Never his real name.

## 1. Readiness (this container)
1. `git fetch origin && git merge-base --is-ancestor e6686d39735a6065dd53afa7c402725878cfed60 origin/main` must succeed, and HEAD must contain it. `ls .claude/agents/tnr-relay.md` must exist.
2. The Agent tool's type list must include `tnr-relay`. If not, stop: agents only load at session start.
3. `ToolSearch select:mcp__Tnr__callEndpoint` must load (matches the agent file's tools: line).
4. Python 3, Node, `node forge/tools/run_lock.mjs status` works, git can push to main (the lock tool needs it).
5. `uname -s` = Linux.

## 2. Preflight (this container counts as a new machine)
1. Accept the trust dialog once: `python3 ops/ap_model_session/scripts/accept_trust.py` (it works on the repo root the kit sits in; pass another folder as its argument). It drives interactive `claude` in a pty from a bare env, presses Down then Enter on "Yes, I trust this folder". Check `/root/.claude.json` projects shows the repo root true. (First try in the old container pressed Enter on the default "No, exit": the Down key is required.)
2. From a bare env shell at the repo root, NOT a --try run:
   ```
   env -i PATH="$PATH" HOME="$HOME" LANG=C.UTF-8 TERM=xterm HTTPS_PROXY="$HTTPS_PROXY" https_proxy="$HTTPS_PROXY" NO_PROXY="$NO_PROXY" no_proxy="$no_proxy" NODE_EXTRA_CA_CERTS=/root/.ccr/ca-bundle.crt SSL_CERT_FILE=/root/.ccr/ca-bundle.crt python3 docs/reviews/evidence/ai_player_hook_relay/preflight.py --form subagent --bare-env
   ```
3. Pass = exit 0 and last line `"the agent file's hooks are run on this machine": true`. If it ever says a call was answered not by the stand-in, or it can't tell whether a call went: STOP and tell the director (possible game read).

## 3. Exclusive ownership
1. `node forge/tools/run_lock.mjs status` must show not held. The old hunt pilot stopped and released at 05:29Z. A scheduled "jutsu training refill" routine may claim the lock while it is free: if it holds it, wait for its release; do not touch that routine.
2. No `player.brain run` from an older version: `pgrep -f "player.brain run"` prints nothing.
3. Live folder: the repo's own `state/player/dauntless/live` (gitignored). `TNR_PLAYER_LIVE` must be UNSET in this shell and in the hooks' environment (`env | grep TNR_PLAYER_LIVE` empty).
4. `python3 -m player.brain stopped` (list). In a fresh container no relay from before can be running, so `python3 -m player.brain stopped all` is true; say it only after confirming that.
5. Do not claim the lock by hand: the brain claims and renews it.

## 4. Deadline (before hunting is enabled)
1. Record in SESSION_NOTES.md: launch time (UTC) and safety cap = launch + 7200 s for this one-battle run (36000 for the later 10-hour run).
1b. Start the one-fight stop in the background, from the repo root: `ops/ap_model_session/scripts/one_fight_stop.sh "$PWD" <launch_epoch>` (run_in_background). Its log is one_fight_stop.log next to this file.
2. Main timer, in this container, independent of the model: `ops/ap_model_session/scripts/arm_deadline.sh "$PWD" <deadline_epoch>`. It writes deadline_timer.pid; `scripts/check_deadline.sh` shows it alive. (Mechanics smoke-tested 05:40Z with a harmless command.)
3. Backup, server-side: `mcp__claude-code-remote__create_trigger` with `run_once_at` = deadline, DEFAULT target (fires into THIS session, not a fresh one; send_later starts a separate run that cannot reach this container's live folder). Prompt: "Deadline reached: from the repo root run `python3 -m player.brain set end_session=true`, confirm it applied in status.json, and keep the relay running for the orderly shutdown." Keep the trigger_id in SESSION_NOTES.md.
4. Relay rotations never reset the deadline.

## 5. Configure
THIS run (gate scope, the director's pick):
```
python3 -m player.brain set mode=hunt paused=false director_mode=false end_session=false relay_without_hooks=false 'activities={"pvp_hunt":true,"training":false,"restock":false,"repair":false,"equipment":false,"bank":false}' 'do_not_attack=["Keoshi","Jazu"]'
```
(If the brain refuses an activity name or says one cannot be switched off, read the refusal, keep the rest off, and note it. do_not_attack only adds names; it never removes do_not_attack.md entries.)
```
```
Later 10-hour run (not now): same with all six activities true. Keep existing spending limits, reserves, exclusions, endpoint restrictions.

## 6. Start and supervise
1. Agent tool: `subagent_type: tnr-relay`, prompt `Begin.`, run in background.
2. Within the first minutes confirm: `live/status.json` run_lock held, mode hunt; `live/client.json` hooks = relay id; `live/hook/log.jsonl` shows pre/post hooks; no STOP about hooks.
3. Report start time and state to the director.
4. On `STOP rotate`: confirm the old subagent ended, start a new tnr-relay with `Begin.`, then `python3 -m player.brain stopped TOKEN` for the old token.
5. Hook refusal or unexplained failure: investigate; never set relay_without_hooks.
6. Watch events.jsonl for stalls, held calls, spending, lock-renewal failures.

## 6b. Token measurement (the point of this run)
- Before launch, note `wc -l live/tokens.jsonl` (0 in a fresh container).
- Every heartbeat and at the end: `python3 ops/ap_model_session/scripts/token_report.py state/player/dauntless/live` and append the JSON to SESSION_NOTES.md under "Token figures".
- Every batch must show hooks true. Any batch with hooks false is a finding: report it.
- Count files in live/hook/late/ (the script does) and report the number.
- Compare plan_count_per_batch with PROOF.md (4,200-4,400 a batch) and state the reduction vs the pre-hook relay as measured, not assumed. Check one tokens.jsonl line by hand against the relay's transcript usage before quoting figures.
- Copy live/tokens.jsonl, live/hook/log.jsonl and the final status.json into ops/ap_model_session/run1/ at the end (the live folder is gitignored and dies with the container).

## 7. Keep the container above idle (the director: it must never go idle)
- Always keep at least one background task running in this session: a heartbeat Bash job `sleep 1200; cd <repo> && python3 -m player.brain status | head -60; ops/ap_model_session/scripts/check_deadline.sh` with run_in_background. When it completes you are woken: read it, act, and start the next heartbeat in the same turn. Never end a turn without a heartbeat or relay running.
- The relay subagent itself runs in the background and wakes you when it stops.
- Optionally a Monitor on `live/events.jsonl` for "stall" or "finding" lines.
- Each wake: check relay alive, lock held, timer alive, append a line to SESSION_NOTES.md.

## 8. End
At the deadline: ensure end_session=true applied (timer or trigger or by hand). Keep a working relay for combat, travel home and sleep. Do not substitute paused=true; do not kill the relay because time is up. Done = profile shows ASLEEP at home (sector 177, 13,8 is home per the last read), relay ended, `run_lock.mjs status` not held. Then cancel_deadline.sh and delete the backup trigger if unfired. Report start/end, fights and outcomes, spending, token figures, count of files in live/hook/late/, interruptions, findings. If shutdown can't complete, report the real state and blocker.
