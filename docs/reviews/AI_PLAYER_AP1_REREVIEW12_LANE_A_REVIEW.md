# AP1 independent re-review, Lane A — ce1be6e9

Repository: `perseverance484/tnr-tools`. Frozen head: `ce1be6e98eb39550e79806c5c8f9da87f67fa4eb`. Code commit: `1f9baa216c83d4aa3ab34a8a22d418ebcd474866`. Reviewed diff: `25308e2a4f2ee905f1bf3412c3f7f85c1811c62f..ce1be6e9`. Review date: 2026-11-13.

**Verdict: request changes. The original H2 cases are corrected, but a concurrent `World` reader can reopen the same identity failure. One medium finding. H1 remains closed, including the protocol-3 predecessor e4a267cd.**

I read the REREVIEW12 handoff first, then Implementation Handoff section 5 and the report at `219515fe`. The approved split is the base, not a change re-audited here. Scope was takeover identity during and after saving, crash boundaries, protocol 4 and retained controls. Settled policy and AP2 are outside this review.

## Original reproductions and controls

I extracted `write_window.py` and `save_faults.py` directly from `219515fe` and ran them unchanged on the frozen head.

| `write_window.py` mode | Result |
|---|---|
| `window` | Separate-process `stopped all` queues no takeover word while the resident holds its lock. Later restored snapshot: no calls, 30 held rows, counts 1 then 2. The script fails its old assertion that the word names the later hold. |
| `failed` | No calls, 30 held rows. Counts are 2 then 3; the script stops at its obsolete count-1 assertion. This original script has no brain lock, so `stopped` recovers the abandoned-looking save, and the same Brain counts again on retry. |
| `before` | Passes unchanged: the word does not name the later restored takeover; no calls, 30 held rows. |
| `after` | Passes unchanged: the same safe result. |

The production-shaped failed-save test, with the brain lock held, also passes: no takeover word is queued while that Brain remains home. The original `save_faults.py` counter-failure case passes. Its world-failure case stops at the old expected count; removing only that count assertion and its final count assertion permits observation: the restart gets a new identity, the old word releases zero rows, and same-Brain recovery finishes at count 2. These are legitimate changes forced by the three-write protocol.

## 1. Medium — a concurrent World reader can falsely finish an active save

Locations at this head:

- `player/world.py:145`: every `World(...)` construction calls `counted`, without checking the brain lock.
- `player/world.py:89-95`: `counted` raises the count and clears `saving` solely because the marker is set.
- `player/world.py:183-186`: the active writer captures `n` before its first write and finishes with that captured `n + 1`.
- `docs/reviews/AI_PLAYER_AP1_REREVIEW12_HANDOFF.md:267`: known limit 4 explicitly includes a script constructing `World` while the original brain is alive, and claims the name moves on and nothing is released.

That last safety claim holds for a construction **after a failed save has returned**, followed by a new save attempt. It does not hold for construction **during the active three-write attempt**.

I added only `from player.world import World; World(live)` to the acknowledgement subprocess in the original `window` reproducer. The reader does not call `save`, alter the ledger, disable a lock or synthesize an acknowledgement row. The original resident is still inside its save and demonstrably holds `brain.lock`.

Sequence:

1. The resident installs hold A from the old file and count 0. Its save captures `n = 0`, then writes `(0, saving=True)`.
2. Before its world write, the separate reader constructs `World(live)`. The constructor assumes the active save is abandoned and writes `(1, saving=False)` despite the resident's lock.
3. `stopped all` in that process now sees the old file plus count 1 and queues a word for B. Its lock-aware recovery guard never runs: the reader has already cleared the marker.
4. The resident saves its original hold A and finishes with its cached `n + 1`, also 1. It does **not** count again from the reader's count.
5. Only the original world bytes and mtime are restored later. The untouched counter remains 1, so that later takeover is B. The retained old word releases it.

Observed on the frozen target:

```text
resident_has_brain_lock: true
first_hold / saved_hold: A
word / later_listing: B
count_after_save: 1
calls: profile.getUser, travel.getSectorData, stealth.useSensory, combat.getBattleHistory
elapsed: 9 seconds
loose_update: 0
final_count: 2
```

The word was over a minute old; the defect is its identity authorizing a different takeover, not shortening the tail of a valid word. `takeovers.json` was never deleted, restored or manually edited. The old package had exited, and the acknowledgement was truthful about its actors being stopped.

### Refutation and scope qualification

Without the additional constructor, the same separate-process observation is refused and the later takeover retains all 30 rows. The before/after controls stay safe. The difference is the new constructor side effect, not scheduling an unprotected `stopped` implementation.

I found no built-in CLI path that automatically constructs a second `World` outside the brain lock while the resident saves. This finding is specifically the concurrent script-reader behavior that the handoff explicitly says is safe. It should not be described as a routine CLI-only reproduction. It nevertheless reproduces the promised identity failure through that advertised case; the passing tests exercise sequential recovery or lock-aware `stopped`, not a second `World` construction during the active attempt.

**Required correction:** an ordinary reader must not mark an active writer's save abandoned. Perform abandoned-save recovery under ownership exclusion, as `_on_disk` already attempts, or keep plain `World` construction read-only and put recovery in an explicitly owned path. Also ensure an active save cannot finish using a generation made stale by a concurrent recovery. Retain the normal CLI, failed-save, crash and before/after controls. Apply the existing protocol-change rule to any change in release semantics; no new policy ruling is needed.

### Runnable reproducer

Save the following as `/tmp/ap1-world-reader.py`, then run from the frozen repository root:

```sh
PYTHONPATH=. python3 /tmp/ap1-world-reader.py window
```

Git history must contain `7cf7d73c`. The script uses that real package to produce the source world model, as the original review did. It prints the observations and exits 0 while asserting the defect on this head. All emitted calls are observed local instructions, never game requests. Relative to the original `write_window.py`, only the acknowledgement child's `World` import and construction were added.

```python
import io,json,os,pathlib,subprocess,sys,time
from unittest.mock import patch
from player import brain,relay
from player.world import World,takeovers
from player.tests.test_rereview5 import by_the_version_at
from player.tests.test_rereview9 import OLD_PROGRAM
from player.tests.test_relay import token_of
from player.tests.test_rereview6 import calls_of

mode=sys.argv[1] if len(sys.argv)>1 else 'window'
live,made=by_the_version_at('7cf7d73c5cb235801b66e4b4763cb63e1bc7b14e',OLD_PROGRAM,'pending')
path=pathlib.Path(live)/'world.json'
raw=path.read_bytes(); stamp=path.stat().st_mtime_ns
now=[made['now']+120]; real=brain.Brain; write=World._write
observed={'mode':mode}
def say(*names):
    out=io.StringIO(); brain.stopped(live,list(names),out); return json.loads(out.getvalue())
def nxt(token=None):
    out=io.StringIO(); brain.next_batch(live,token,out,lambda t:now.__setitem__(0,now[0]+max(0,t)))
    return out.getvalue().splitlines()
with patch.dict(os.environ,{'TNR_PLAYER_NO_DAEMON':'1','TNR_TRANSCRIPT':live+'/none','TNR_PLAYER_FIGHTS':live+'/fights'}),patch.object(time,'time',lambda:now[0]),patch.object(brain,'Brain',lambda live:real(live,clock=lambda:now[0])):
    home=real(live,clock=lambda:now[0])
    observed['first_hold']=home.budget.loose()[0][1]
    if mode=='before': observed['word']=say('all')
    def interleave(p,obj):
        if p==str(path) and mode=='window' and not observed.get('word'):
            observed['count_when_word_said']=takeovers(live)
            probe=brain._lock(live)
            observed['resident_has_brain_lock']=probe is None
            if probe is not None: probe.close()
            child="import sys,time; from player import brain; from player.world import World; time.time=lambda:float(sys.argv[2]); World(sys.argv[1]); brain.stopped(sys.argv[1],['all'])"
            said=subprocess.run([sys.executable,'-c',child,live,str(now[0])],cwd=os.getcwd(),env={**os.environ,'PYTHONPATH':os.getcwd()},capture_output=True,text=True,timeout=5,check=True)
            observed['word']=json.loads(said.stdout)
        write(p,obj)
    if mode=='failed':
        def fail_world(p,obj):
            if p==str(path): raise OSError('injected world save failure')
            write(p,obj)
        with patch.object(World,'_write',staticmethod(fail_world)):
            home._save()
        observed['count_when_word_said']=takeovers(live)
        observed['word']=say('all')
        home._save()  # the same brain recovers and saves the original hold, without recounting
    else:
        with patch.object(World,'_write',staticmethod(interleave)):
            observed['resident_exit']=brain.run(live,forever=False)
    if mode=='after': observed['word']=say('all')
    observed['saved_hold']=[c[3] for c in relay.read(str(path))['budget']['calls'] if c[1]=='update'][0]
    observed['count_after_save']=takeovers(live)
    now[0]+=120
    path.write_bytes(raw); os.utime(path,ns=(stamp,stamp))
    observed['later_listing']=say()
    started=now[0]
    lines=nxt(token_of(nxt()[0]))
    observed['calls']=calls_of(lines); observed['elapsed']=now[0]-started
    observed['loose_update']=sum(1 for c in relay.read(str(path))['budget']['calls'] if c[1]=='update' and c[2:3]==['loose'])
    observed['final_count']=takeovers(live)
    print(json.dumps(observed))
    assert observed['count_after_save']==1
    assert observed['final_count']==2
    if mode in ('window','failed'):
        if mode=='window': assert observed['resident_has_brain_lock']
        assert observed['word']['stopped']==observed['later_listing']['still_held']
        assert observed['calls'] and observed['elapsed']<60
        assert not observed['loose_update']
    else:
        assert observed['word']['stopped']!=observed['later_listing']['still_held']
        assert not observed['calls']
        assert observed['loose_update']==30
```

## Three-write crash behavior and remaining controls

I independently interrupted `World.save` before any write and immediately after each of its three successful atomic replacements, released the brain lock as process death would, and restarted under the lock. After completing recovery, I restored only the original world bytes/mtime and checked the first acknowledgement against the later hold.

| Interruption | `(count, saving)` after interruption | At restart | Old word releases rows of the later restored takeover |
|---|---|---|---:|
| Before write 1 | `(0, false)` | `(0, false)` | 0 |
| After write 1 | `(0, true)` | `(1, false)` | 0 |
| After write 2 | `(0, true)` | `(1, false)` | 0 |
| After write 3 | `(1, false)` | `(1, false)` | 0 |

All later restored takeovers retain 30 rows. Before any successful write, a restart can correctly keep the original takeover's identity. After the world write, a restart correctly keeps the actual hold already stored in the current ledger while completing the pending count. These are distinct from constructing an extra reader during a still-active save.

I also moved the original operator probe to immediately before write 3. It can acknowledge the **actual hold in the saved current ledger** then, despite `saving=True`; the later restored takeover remains held. Thus “no name between the first and third writes” is an overstatement in the handoff. The important property is not deriving a future identity from an incomplete foreign-file/count pair. Acknowledging an already-persisted row at that point was safe in this control and is not another finding.

The existing identity, same-bytes/same-mtime, stable-before-save, quiet-minute, selective-release and result-idempotence controls pass. The added package export test also passes; I did not reopen the approved split.

## Protocol 4: H1 remains closed

The actual e4a267cd package is treated as protocol 3, not as this version. I additionally reran the earlier H1 harness with only its maker SHA changed to e4a267cd:

- Pending, receipt and already-installed-hold modes emit no calls. The old defect assertions are refuted.
- Acknowledgement permits two new calls after 60.5 seconds.
- Changing only the maker to this frozen head gives the positive pending and receipt controls: four calls after their own eight-second wait, no update hold.

The suite's three real-e4a267cd-resident tests pass: left running, ended during the wait and ended first. Its pending/receipt/ledger test also passes. These ran without skipping. The current client, request-name/content, answer, receipt and ledger protocol controls retain the explicit predecessor-number case. No H1 redesign is required by this result.

## Verification

| Check at ce1be6e9 | Result |
|---|---|
| `python3 -W ignore::ResourceWarning -m unittest discover -s player/tests -t .` | 422 tests, OK, none skipped |
| `python3 -W ignore::ResourceWarning -m unittest -v player.tests.test_rereview11 player.tests.test_rereview10 player.tests.test_rereview8` | 41 tests, OK, none skipped |
| Current `test_rereview11.py` against production code at 25308e2a | 12 failures, no errors |
| Original `write_window.py`, four modes; original `save_faults.py` | Outcomes described above |
| Additional crash-boundary and third-write observer controls | Safe outcomes above |
| Added concurrent-World-reader reproducer | Four calls after 9 seconds, zero loose update rows; defect reproduced |
| Actual e4a267cd and current-maker H1 controls | Outcomes above |
| `python3 -W ignore::ResourceWarning -m unittest scripts/test_player_allowlist.py scripts/test_player_catalog.py` | 46 tests, OK |
| `player_allowlist.py check` and `report --check` | Zero violations; current |
| `rulings_index.py --check` | 322 rulings; current |
| `check_large_files.py` | Clean |
| `check_no_real_name.py --commits 25308e2a..ce1be6e9` | Zero hits |
| `git diff --check` | Clean |

For the base discrimination run, the current tests were copied to a temporary extraction of the base production code. Only the missing `generation`, `seen`, `LOOKS` and `SAVING` names were supplied in the test process so it could load. Six failures cover the finding and adjacent behaviors; two concern unavailable new helper behavior; four test e4a267cd against its own protocol on the base. They should not be described as twelve independent reproductions of H2. No base production file was patched.

I did not repeat all 78 author-reported mutations, the 200-walk campaign, fuzzes, simulated fights or unchanged legacy pilot tests for this scope. The full suite includes its small deterministic walk regression. Those models do not cover the additional constructor interleaving above, so their passing result does not refute it. No power-loss/fsync guarantee or live performance claim is made.

The next correction can stay narrow: ownership of abandoned-save recovery and its interaction with an active save's captured count, with the existing reader, failure, crash and protocol controls retained. Counter-file loss/rollback remains the separately disclosed limit; this finding does not depend on it.

Only this report is published on `chatgpt/review-ai-player-ap1-rereview12-lane-a`. No existing tracked file or implementation file changed in the review checkout, and no `fable/*` branch was modified. Historical extractions, altered test copies and scratch scripts stayed outside the checkout.

**Zero live-game requests, game writes, live credentials or live session material used.** No live relay/browser session was exercised.
