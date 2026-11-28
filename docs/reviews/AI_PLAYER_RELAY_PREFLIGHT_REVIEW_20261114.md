# Frozen review: relay prompt/reader and operator preflight

Reviewed 2026-11-14. Repository: `perseverance484/tnr-tools`.

| Target | Frozen SHA | Verdict |
| --- | --- | --- |
| A: `fable/ai-player-hook-relay` | `bf2231f6a6ce13816747390f71479fbe19776fd5` | **Approved for the requested delta** |
| B: `fable/ai-player-hook-proof` | `65974c0259f01afdfc8ccc20fa448af06009a0f5` | **Request changes before running this preflight on the operator's connected machine** |

A's base is `51fac81d712b65936dba14bf340ac957975da3e4`; it is the merge base of A and that base. A is also the merge base of A and B. Both remote Fable heads matched the supplied SHAs at start and before publication. Shared `main` was `cb0247064b3a935aa96a8d728396e7ce7fa248c8` at start and `7b0c2b2bddb244da2ecae296babc33a89dad2ceb` before publication; this review does not propose integration to main. The report branch is `chatgpt/review-ai-player-relay-preflight-20261114`, based on B. No implementation file or Fable branch was changed.

## Answer to B's question

**With Claude Code honoring `--strict-mcp-config` as intended, the generated config routes MCP calls only to the local stand-in. I found no network client or live-connector forwarding in that stand-in. I did not demonstrate a bypass of that CLI isolation.**

However, the claimed independent safeguards and the fallback consequence are not sound. Guard mode can produce gameplay calls; the missing-call watchdog becomes ineffective when the stand-in never creates its log; and the initialization check is a polling observer with fail-open parsing, not a dispatch barrier. The preflight can also return success without proving its stated hook coverage. Thus I cannot approve the unconditional operator promise that this check makes no game request, or the handoff's fallback claim that isolation failure can cost only one profile read.

All reproductions below are offline: fixture-fed brain calls, local files, and mocked subprocesses/threads. No Claude session was launched by the reviewer. No preflight or proof was run against a real connector. Zero live-game requests, writes, or credentials used.

## Findings on B

### B1 — Guard mode does not impose the claimed profile-only ceiling

**Confirmed defect in the preflight's safety argument; blocking.** Locations at B: `preflight.py:61-62`; `proof.py:143-144`, `186-202`; claims in `preflight.py:21-24` and the handoff's guard 5.

The script sets `mode=guard` and disables five upkeep activities. It does not disable recovery, travel, or battle, and does not install a preflight-specific endpoint restriction. Those activities are deliberately active in the normal player:

- `player/activities/recovery.py:26-29,69-71`: hospitalization takes priority regardless of hunt/guard mode and plans `hospital.npcHeal`.
- `player/activities/travel.py:17-28`: an in-progress trip plans `travel.finishGlobalMove` regardless of mode.
- `player/activities/battle.py:48-49`: a battle is available regardless of mode.

Reproduction using `player.tests.support.Rig(mode="guard")`, with the same five upkeep activities disabled as the proof, first calling `tick()` and then `tick(user(...))`:

| Profile response | Next admitted batch |
| --- | --- |
| AWAKE, healthy | `profile.getUser` |
| HOSPITALIZED | `hospital.npcHeal`, `profile.getUser` (no hold) |
| TRAVEL | `travel.finishGlobalMove`, `profile.getUser` |
| BATTLE with a battle ID | `combat.getBattle`, `combat.getBattleEntries` (no hold) |

These are the real brain's admitted call descriptions; nothing was dispatched. The stand-in always supplies the healthy AWAKE fixture unless controlled otherwise, so run 14b and pf2 do not test this ceiling. The ordinary relay hooks authorize the brain's batch; they do not add a profile-only policy.

The external three-batch stop counts answers in the **stand-in** log. If another connector is answering, that count does not advance. Even with the missing-call watchdog working, its two-second allowance is not a guarantee that no follow-on batch can be dispatched, especially for a hospitalized profile with no hold. A rehearsal directory bypasses the live run lock; it does not disable gameplay decisions. The repository already says “Never give a rehearsal a relay that can reach the game” (`player/OPERATOR.md`, Run lock).

**Smallest robust correction:** enforce a preflight-specific restriction before dispatch, independent of game state and of the hooks whose registration is being tested. Permit only the intended own-profile probe shape and impose an explicit call bound, or isolate transport so that only the stand-in is reachable. Do not change the ordinary player's correct guard behavior to fix the test harness. Revise the safety claims to the bound actually enforced, and test hospitalized, traveling, and battle responses offline.

### B2 — A missing stand-in log disables the missing-call watchdog

**Confirmed defect; blocking defense-in-depth failure.** Location: `proof.py:208-215`.

The hook log and game log are opened in one `try`. If `game.jsonl` is absent, the handler sets **both** `released` and `came` to zero, erasing evidence of a released call. Every poll repeats that reset, so `behind` never starts. This is precisely a case to handle when the stand-in did not start or another server answered instead.

I ran the actual nested watchdog with a fake process, a clock advanced by its sleeps, and one hook row `{"hook": "pre", "refused": null}`:

| Stand-in log | Result |
| --- | --- |
| Absent | No kill after 5.1 simulated seconds |
| Exists with only `{"at": "connected"}` | Kill after 2.1 simulated seconds, `released=1`, `came=0` |

Run 14c exercises the second case: `fake_connector.note()` preserves the `connected` row even with `unseen=true`. It therefore cannot establish behavior when the file is missing. With no fake answers, the three-batch stop also never fires; the overall 150-second clock is what remains in preflight.

**Correction:** read the counts independently, retain released calls when the game log is absent, and treat unreadable/lost monitoring evidence as a failure. Add missing-file and unreadable-file cases alongside the existing connected-but-unlogged-call case. State explicitly that a detector after dispatch cannot retract a call already sent.

### B3 — The initialization observer fails open and does not gate dispatch

**Confirmed defect; blocking defense-in-depth failure.** Location: `proof.py:169-184,222-224`.

The relay starts before the checking threads. The checker recognizes only lines beginning with the exact bytes `{"type":"system","subtype":"init"`. Valid JSON with spaces or different key order is ignored. An absent initialization event is also ignored until the process ends or the global clock expires; malformed matching JSON can kill the checking thread without ending the relay. There is no successful-initialization acknowledgment required before a call can run.

Using the actual nested function and a fake process, an unexpected server in compact JSON was killed immediately. The identical event serialized by ordinary `json.dumps` was not killed after five simulated seconds. No init event was likewise not killed. The compact control confirms that the comparison itself works; the failure is the byte-prefix filter and absence of a fail-closed admission state. The committed 2.1.325 runs use the compact format, so this is not a claim that those recorded runs evaded the check.

Even in the compact case, polling every 50 ms can only detect after the subprocess starts. It is not proof that zero calls escaped before termination. `p.kill()` targets the Claude process, not a verified shutdown of every descendant or cancellation of an already dispatched request.

**Correction:** parse complete JSON objects by their fields, reject missing/malformed initialization within a short bounded startup phase, propagate watcher failures to the result, and prevent tool dispatch until the checks succeed if this is to count as a prevention guard. Verify shutdown/reaping of the processes the harness starts. Keep the distinction between prevention and after-the-fact detection explicit in the operator documentation.

### B4 — The operator gate can pass partial or stale hook evidence

**Confirmed defect; blocking correctness of the gate.** Locations: `preflight.py:63-74,91-113`; `proof.py:121,226-231`; `fake_connector.py:57-58`.

`ran` requires only nonzero bash/pre/post counts and at least one fake call, with fake calls no greater than pre count. It does not require three calls, one completed result hook per call, matching call identities, a valid end reason, or a successful child invocation. A timeout is printed as `{"exit": "ended by the clock"}`, not `ended`, so the gate does not reject it by that field either.

Offline reproduction: three fake profile calls, three pre hooks, one bash hook, and only **one** post hook yield `"the agent file's hooks ran": true`. Returning process exit 1 does not change that answer. This contradicts the function's “for every call” contract and the operator instruction to rely on exit 0.

There is a second practical route to the same false pass: named `OUT` directories can be reused. The game and hook logs append, the live directory is retained, and no run identity or starting offset filters old evidence. With those logs already present, I mocked a valid inventory probe followed by both new relay invocations failing before any hooks. The real `preflight.main()` still returned **0** and reported both forms successful. The documented default without `OUT` creates a fresh temporary directory, so it avoids this stale-directory variant, but not the insufficient-coverage predicate.

**Correction:** allocate a fresh run directory (or refuse nonempty output), bind evidence to the current run/session, require the intended completed calls and matching pre/result-hook evidence, and return a structured terminal status distinguishing intentional stop from timeout/startup failure/watcher failure. Validate that status in preflight; do not blindly require a zero Claude exit when intentionally terminating it is the expected success path.

## Audit of the five guards and dependencies

| Guard | What holds | Limit / required follow-up |
| --- | --- | --- |
| 1. Strict MCP config | Both inventory and relay commands include `--strict-mcp-config --mcp-config`; generated config contains only `Tnr`, launching the absolute local `fake_connector.py` with Python. No HTTP/SSE/remote URL is generated. | The underlying CLI's treatment of an installed real connector was not independently exercised. This remains the primary prevention boundary; the local tests do not prove a CLI isolation bypass. |
| 2. Inventory before relays | Preflight rejects unexpected server names, additional same-name MCP tools, and missing inventory before calling `form`; these three rejection cases passed with mocks. | The probe is **not tool-less**: it disallows only `mcp__Tnr__callEndpoint`, retaining default built-ins and potentially other MCP tools if guard 1 fails. It runs to completion before inventory is examined, and normally uses a temporary-directory cwd while relays use the repository root. It does not prove an identical project/settings context. Make the no-call condition mechanical; do not count the “ready” prompt as a tool restriction. |
| 3. Relay init observer | Recognized compact unexpected inventory triggers kill in the offline control. | B3. It is an observer, not a launch/dispatch gate. Missing/malformed/unrecognized init must fail closed. |
| 4. Released-call observer | Existing fake log with zero calls triggers the documented kill. | B2. Missing log suppresses the detector. Counts also do not establish per-call identity and do not cover a relay whose pre hooks never ran. |
| 5. Rehearsal guard brain | Own-environment path explicitly overrides `TNR_PLAYER_LIVE`, `TNR_PLAYER_FIGHTS`, and `TNR_PLAYER_NO_DAEMON`. Three healthy fake-profile answers are the intended external stop signal. | B1. Rehearsal is state/run-lock isolation, not read-only operation. The stop depends on the fake log, and neither guard mode nor polling enforces “one read only.” |

`fake_connector.py` implements stdio JSON-RPC and answers from `player.tests.support` fixtures. Its server path contains no network forwarding. Its self-test launches that same local script and passed. It is deliberately a permissive game stand-in: `callEndpoint` can receive endpoint names besides `profile.getUser`, returning fixture data or success. It is not an endpoint firewall. Its fixture and imports were inspected as well as its own source.

The `--own-env` review covered code and mocked environment propagation, including verifying that inherited live-folder settings are replaced. It did not exercise an actual operator shell, installed Claude configuration, permission settings, plugins, trust state, or real connector. Neither inherited configuration nor a server's displayed name is a transport identity proof.

RUL-158 confines proof to the stand-in; RUL-159 leaves the live gate to the director; RUL-160 point 1 specifies zero game requests for the operator check. The generic allowance for live profile reads in `CLAUDE.md` does not relax that task-specific contract. `player/OPERATOR.md:112-117` should direct the operator only to a corrected, reviewed check. `PROOF.md`'s historical runs remain evidence of their stated stand-in environment, not proof that these untested failure paths work.

## A: approved checks and limits

The exact diff `git diff 51fac81d bf2231f6` contains the two code/prompt commits and their handoff, with no hook or brain implementation change.

- **995625fe:** the new instruction is in step 2, before Rules and the dedicated `put` exception. `put` still explicitly requires one line at a time, waiting for each result, so the added same-message rule does not erase that exception. The agent body equals `player/RELAY.md`. The prompt has **312 words**; the test and design both move the strict bound from under 300 to under 320. The new test checks placement and both sequencing instructions. This meets RUL-160 point 2. The tests protect wording; the committed model runs, not string assertions, are the evidence for actual model compliance.
- **f4d042d0:** `_blocks` retains assistant messages, user result messages, and legacy rows without a type; it ignores debug/event rows such as `api-request-blob`. Thus the supported real call/result rows remain readable and copied debug calls no longer become strays. `find_transcript` still sees real Bash tokens. `_usage` is unchanged; the debug-copy shape in scope has no usage to count.
- **Hooks do have a dependency on this reader:** `hooked._look` calls `relay._span` to recover a result when a result hook failed to persist it. Consequently, the handoff's “results come through hooks” explanation alone is insufficient. I checked this recovery path and token accounting too: all 86 hook tests passed with transcript rows converted to typed assistant/user messages and debug copies inserted, including result copies. Recovery of late/failed results and accounting assertions still passed. This supports the requested no-regression conclusion for the supported transcript shapes.

No blocking finding on A. This is not a fresh approval of every earlier player design decision or an authorization to play. Previously disclosed fallback reliability, trusted-folder registration, real connector behavior, and live fight timing remain outside what this offline delta review establishes.

## Verification

| Command / check | Result |
| --- | --- |
| On exact A: `python3 -W ignore::ResourceWarning -m unittest discover -s player/tests -t .` | **636 tests, OK**, 98.697 s, no skips |
| On exact A: `python3 -W ignore::ResourceWarning /workspace/scratch/review_typed_transcripts.py` | **86 hook tests, OK**, 5.129 s, no skips; scratch wrapper injects typed messages and API debug copies |
| On exact B: `python3 docs/reviews/evidence/ai_player_hook_relay/fake_connector.py --selftest` | Exit 0; local stdio stand-in only |
| On exact B: `python3 /workspace/scratch/review_preflight.py` | All asserted offline reproductions/control cases passed: B1-B4, config/env construction, and inventory rejection |
| `git diff bf2231f6 65974c0 -- player .claude` | Only `player/OPERATOR.md`; no different player implementation/tests requiring a duplicate full-suite run |
| `git diff --check 51fac81d bf2231f6`; `git diff --check bf2231f6 65974c0` | Both exit 0 |
| On B: `python3 scripts/rulings_index.py --check` | Exit 0; 330 rulings, index current |
| Report staged: `git diff --cached --check`; `python3 scripts/check_no_real_name.py`; `python3 scripts/check_large_files.py` | Exit 0 each; zero name hits and no disallowed large files in the populated sparse checkout, including this report |

Scratch tests are not implementation changes and are not committed, per the review workflow. The harness replaces **all** subprocess starts in `proof.main()` with mocks, captures its actual nested watcher functions through a fake Thread, and advances a simulated clock for each watcher. Preflight success/rejection tests likewise mock subprocess launches. Only the separately listed fake-connector self-test starts a connector process, which is the local fixture server. Scratch script SHA-256 values:

- `review_preflight.py`: `5047cac890b0b8d7f9fb61980e546cea6fb268e46d035e9b4b72ff88c75e1264`
- `review_typed_transcripts.py`: `1906083335459c5b594deaa28c38e49e9ed278c774495ce233a440bd2f3d95bf`

Minimal reproduction of B1, from B's root (constructs batches only):

```python
from player.tests.support import Rig, user
for status in ("HOSPITALIZED", "TRAVEL", "BATTLE"):
    r = Rig(mode="guard")
    print(r.calls(r.tick()))
    print(r.calls(r.tick(user(status=status, bid="offline-battle"
                             if status == "BATTLE" else None))))
```

Minimal predicate reproduction of B4: in a temporary `OUT`, write three `game.jsonl` rows with `at="came", endpoint="profile.getUser"`; write `live/hook/log.jsonl` with one bash, three pre, and one post row, each `refused=null`; mock `preflight.proof` to return `returncode=1, stdout="", stderr="failed"`. `preflight.form(OUT, "main", "agent")[0]` is `True`. For B2/B3 the exact fixture inputs and positive controls are above; the watchdog source lines identify the complete failing branches.

## Next step

Fable should correct B1-B4 and the overstatements in the five-guard explanation on its own branch, add offline failure-path tests, and return a new frozen SHA. Re-review can focus on the preflight/proof/fake-connector boundary, affected operator text, and any new enforcement surface. If the correction changes ordinary hook/brain behavior, those paths require renewed review too. A's two changes need not be reopened if unchanged. The operator preflight and AP1 live gate have not been started by this review.
