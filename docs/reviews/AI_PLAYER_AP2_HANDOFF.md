# AI player overhaul, phase AP2, first part: implementation handoff

Workflow: `docs/workflows/IMPLEMENTATION_HANDOFF.md`. Written 2026-11-12; issued again 2026-11-13 on AP1's
corrected head.

```text
Repository: perseverance484/tnr-tools
Branch: fable/ai-player-ap2
Base: ce1be6e98eb39550e79806c5c8f9da87f67fa4eb (fable/ai-player-ap1: the approved split of brain.py, 25308e2a,
      and on it AP1's correction after the review of e4a267cd)
Supersedes: c720743a005a1fd2c5833b7549f6055d83f34f43, the first handoff of this part, which stood on 25308e2a.
      Not rebased: this head is c720743a, a merge of fable/ai-player-ap1 at ce1be6e9, and this note brought
      up to date.
Head: the commit that brings this note up to date (FROZEN; the exact SHA is in the handoff message)
Integration target: the AI player line. Nothing of it is on main; main was at d0428e9d when this was written.
```

## What this is, and what it stands on

The director ruled that AP2 is reviewed in two parts (RUL-2026-11-12-154). This is the first: everything of
AP2 that is built. The second waits for playbooks or rules and is listed under "Not begun".

It stands on two things, and one of them is not accepted yet:

- the split of `brain.py`, approved at `25308e2a` (`chatgpt/review-ai-player-brain-split` @ `11a0d5df`);
- AP1's head `ce1be6e9`. That is `7cf7d73c`, which was accepted (H1), and two corrections of H2: `e4a267cd`
  (a takeover is counted; protocol 3), reviewed with one medium finding left, and `ce1be6e9` (a takeover is
  saved in three writes and no word is taken for it meanwhile; protocol 4), **which has not had its
  re-check**. Nothing of AP2 depends on how that comes out. If it changes code, I merge the change in and
  issue a new SHA, as I have done here.

**A correction to the first handoff.** At `c720743a` this note said that `e4a267cd` "has not had its
re-check". It had. The review was on the remote and had not reached me
(`chatgpt/review-ai-player-ap1-rereview11-lane-a` @ `219515fe`); I had not looked.
`docs/reviews/AI_PLAYER_AP1_REREVIEW12_HANDOFF.md` has the account and the correction.

**What changed since `c720743a`.** Nothing of AP2's own. `git diff c720743a HEAD` is AP1's correction, which
is `git diff 25308e2a ce1be6e9` (ten files), and this note. The three files both lines touch
(`player/world.py`, `player/OPERATOR.md`, `player/tests/test_brain_package.py`) merged without a conflict. A
review of `c720743a` that is under way loses nothing by moving here: outside this note, `git diff ce1be6e9
HEAD` and `git diff 25308e2a c720743a` are the same change, line for line.

The review target is `git diff ce1be6e9 HEAD`: outside this note, 29 files, 2,285 lines added and 28 removed.

## Objective

The upkeep of the character on the brain (brief AP2): keep the consumables stocked, the gear repaired, the
training queue filled, the right loadouts on, the money where it should be, end a session properly, and hold
the account's run lock while it plays.

## What is built

| Where | What it does |
|---|---|
| `player/activities/restock.py` (238 lines) | A pass over the battle consumables: put a carried stack back in its slot, take what is stored at home, buy in the item shop for ryo up to the target, else a buyout at the auction house under the item's cap. The shop is paid from the pocket, each purchase out of what the one before left; the reserve is held against pocket and bank together |
| `player/activities/repair.py` (61) | An equipped item under a quarter of its durability is repaired: Repair Kits first, then ryo; neither twice in ten minutes |
| `player/activities/training.py` (222) | The jutsu queue: every free place goes to the target whose next level is lowest, up to the cap; a refused target is left a day, or ten minutes when the refusal is about the moment. Energy trains the stat that trails, in the village, and enough of it is worth the trip. Unspent experience levels intelligence and willpower and is then split |
| `player/activities/equipment.py` (91) | Writes what is equipped where the planners read it; puts the backup thrown weapon in an empty slot; selects the PvP 1 loadouts for a hunt and at the end of a session. PvP 1 is selected and never edited |
| `player/activities/bank.py` (90) | RUL-2026-11-12-153: over 200,000 in pocket goes to the bank; for a training fill the pocket is filled to 10,000,000 and the rest goes back; for a shop purchase the pocket cannot pay, to its price and never past 200,000. Never under the reserve |
| `player/activities/session.py` | At home with the session ending, the last upkeep has its turn before the character sleeps |
| `player/runlock.py` (163), `player/brain/core.py` | RUL-2026-11-12-154: the brain claims the account's run lock as `player` before a session's first call, renews it, sends no call without it, and gives it back. Only the brain of the account's own live folder; every other brain is a rehearsal |
| `player/world.py`, `player/calls.py`, `player/combat.py`, `player/gates.py`, `player/console.py` | My items in the world model; the calls and their columns; the item catalog and the equipped feed for the combat tools; the spend caps from the director's settings; the lock's state in the status file |
| `player/OPERATOR.md` | "The run lock": what the operator must and must not do |

Two things touch what AP1's reviews accepted, and I name them so that they are looked at:

- **The profile read asks for one more column**, `userData.earnedExperience` (`calls.py` `USER_SEL`). Every
  profile read of the player carries it.
- **`Brain._decide` and `Brain._paced` ask the lock** before anything is planned, and again where every batch
  is paced. For a rehearsal, which is every brain but the account's own, both are no-ops: the 422 tests of the
  base pass. Three lines in two of them (`test_activities.py`, `test_brain.py`) changed with AP2's first cut,
  for the rig's new switches: the upkeep is off in a test unless the test asks for it. What they assert did
  not change.

## The run lock, more closely

It is the one part that writes outside the live folder, so here is exactly what it does.

- **It only runs the existing tool**, `forge/tools/run_lock.mjs`, in a process of its own: `claim --holder
  player --job "play session" --ttl 60 --instance <the live folder>`, `heartbeat --token`, `release --token`.
  The tool makes one commit on `main` a write and decides who wins; the brain writes nothing to git itself.
- **No call without it.** Asked before any activity plans (so no plan is made that is then not sent), and again
  in `_paced`, through which every batch goes, the fight's last resort too.
- **Renewed every 15 minutes**, the workflow's interval. In a fight a renewal is put off until under ten
  minutes of lease are left: it is a push and takes a moment.
- **Lost or lapsed, it stops.** A renewal that finds the lock taken stops every call at once. One that cannot
  be pushed leaves the lease to run: calls go until a minute before the last expiry the tool confirmed.
- **Given back** when the session is over (asleep), when the player is asleep outside hunt mode, and when the
  director pauses it outside a fight. Not for a fresh relay.
- **Who claims.** `runlock.own_folder`: the brain whose live folder is `state/player/<account>/live`. Any other
  folder is a rehearsal: it never runs the tool, and `status.json` says "rehearsal". This is what keeps every
  test, replay and review script from ever touching `main`. It also means a session run with `TNR_PLAYER_LIVE`
  pointing elsewhere has no lock; the operator's page says so in bold.
- **The token** is in `world.json` (`records.run_lock`) so that a restarted brain goes on with its claim. It is
  never in `status.json`.

## Verification on the head's parent (the merge commit)

Everything below was run again on the merge. Where a figure differs from the first handoff's, AP1's correction
is why: its 13 tests are in the suite now.

| Command | Result |
|---|---|
| `python3 -W ignore::ResourceWarning -m unittest discover -s player/tests -t .` | `Ran 480 tests`, `OK`, three runs in a row, none skipped |
| The AP2 tests alone: `test_upkeep` (43), `test_runlock` (12), `test_wiring` (17), `test_brain_package` (8) | 80 tests, `OK` |
| The real lock tool against a repository made in a temporary folder (`test_runlock.TheRealTool`, 3 tests) | claim, refusal while held, renewal, release, the quiet minute for another runner, none for the same instance; a session of the brain from its first call to asleep; a repository that cannot be reached. The real `main` is never named |
| Sixty-six planted defects in the AP2 code, in throwaway worktrees | below |
| The eleven defects planted for AP1's correction, on this code | every one fails at least one test, in the same numbers as on AP1's head |
| The scripts of the review of `e4a267cd` (`write_window.py`, four modes; `save_faults.py`), unchanged | what they give on AP1's head, case for case: no call, all 30 held, the same counts. The scripts' clock moves 7 s here where it moves 9 on AP1's head; at `c720743a` it did already |
| `python3 -m player.tests.test_walk 200 300` | 200 walks, 5,481 calls, no problem: the figures of the base |
| `python3 -m unittest scripts/test_player_allowlist.py scripts/test_player_catalog.py` | `Ran 46 tests`, `OK` |
| `python3 scripts/player_allowlist.py check`, and `report --check` | exit 0, both |
| The four pilot tests | exit 0 each |
| `rulings_index.py --check`, `check_large_files.py`, `check_no_real_name.py` (files and commits), `git diff --check` | exit 0 each |

The planted defects. On the first run 65 of the 66 failed at least one test. One passed them all: PvP 1 counted
as selected when only one of its two loadouts had answered. The code was right and nothing held it to that; a
test does now (`test_one_loadout_answered_is_not_both_selected`). The table is from a second run of all 66 on the
final code; the unchanged code passes. A third run, on the merge, gives the same table row for row.

| Planted defect | Tests that fail |
|---|---|
| restock: a purchase is not held to what the pocket can pay | 3 fail |
| restock: the reserve is not held against pocket and bank | 1 fails |
| restock: the day's cap does not bound a purchase | 1 fails |
| restock: what costs reputation counts as sold for ryo | 1 fails |
| restock: an auction listing over the item's cap is bought | 1 fails |
| restock: an auction listing in another currency is bought | 1 fails |
| restock: what is stored at home is not taken out first | 1 fails |
| restock: a carried stack is not put back in its slot | 1 fails |
| restock: a pass never ends while the shop says no | 1 fails |
| restock: a read that keeps failing is asked for without end | 1 fails |
| restock: the bank is not asked when the pocket cannot pay for one | 1 errors |
| restock: the pocket is asked to hold more than its limit | 2 fail |
| restock: two purchases of one pass are each sized by the whole pocket | 1 fails |
| repair: an item at half its durability is repaired | 1 fails |
| repair: a refused repair is tried again at once | 1 fails |
| repair: ryo is tried before the kits | 10 fail |
| repair: what is carried but not equipped is repaired too | 1 fails |
| training: the highest next level is queued first | 2 fail |
| training: a target at the cap is queued | 2 fail |
| training: a refused target is asked for again at the next look | 1 fails |
| training: a refusal for want of money costs the target a day | 1 fails |
| training: energy is trained wherever the character stands | 1 fails |
| training: energy always goes to willpower | 1 fails |
| training: a fill does not wait for the bank | 2 fail |
| training: the bank is not asked before a fill | 2 fail |
| training: the wish for ten million outlives the fill | 1 fails |
| training: unspent experience all goes to intelligence | 2 fail |
| training: any crumb of experience is worth a call | 1 fails |
| training: refused experience is tried again every ten minutes | 1 fails |
| training: experience is assigned again at once while the profile still shows it | 1 fails |
| calls: a stat is left out of the experience call | 1 fails |
| calls: the profile read does not ask for unspent experience | 1 fails |
| equipment: PvP 1 is selected on guard too | 1 fails |
| equipment: an empty thrown slot does not take the backup | 1 fails |
| equipment: a refused selection is tried again at once | 1 fails |
| equipment: one loadout answered counts as both selected | 1 fails |
| equipment: what is equipped is not written for the planners | 8 fail, 1 errors |
| bank: the pocket is never brought down to its limit | 5 fail |
| bank: the surplus is banked while training still wants it | 1 fails |
| bank: the bank is taken under the reserve | 2 fail |
| bank: twenty million is drawn for training | 2 fail |
| bank: a wish is honoured after it has run out | 2 fail |
| bank: a refused transfer is tried again at once | 1 fails |
| bank: restock is not told that the pocket can pay | 1 fails, 1 errors |
| bank: an empty pocket is not filled | 1 fails |
| session: the character sleeps without the last upkeep | 1 fails |
| run lock: calls are planned whether or not the lock is held | 5 fail, 3 errors |
| run lock: the place where every batch is paced does not ask | 1 fails |
| run lock: the claim is never renewed | 3 fail |
| run lock: a fight does not put a renewal off | 1 fails |
| run lock: a short lease is not renewed in a fight | 1 fails |
| run lock: a lock that was taken is played on | 1 fails |
| run lock: calls go right up to the lease's end | 1 fails |
| run lock: a failed renewal ends the claim | 1 fails |
| run lock: a failed renewal is tried again at every tick | 1 fails |
| run lock: the lock is kept when the session is over | 1 fails, 1 errors |
| run lock: the lock is given back for a fresh relay | 1 fails |
| run lock: the lock is kept while the director has the player paused | 1 fails |
| run lock: a brain on any folder claims | 47 fail, 28 errors |
| run lock: the account's own folder is a rehearsal too | 1 fails |
| run lock: the token is written to the status file | 1 fails |
| run lock: the tool is asked at every tick while another has the lock | 1 fails |
| run lock: the wait is said again at every ask | 1 fails |
| run lock: the claim is made under another label | 3 fail |
| run lock: the claim does not name this brain's own instance | 2 fail |
| run lock: the claim is kept in memory only, and lost at a restart | 5 errors |

## Size

Player code 5,351 lines in 29 files (base: 4,285 in 23); tests 9,111 lines (8,027). No new file is over the
AP6 budget of 400 lines: the largest are `restock.py` 238 and `training.py` 222, and `brain/core.py` is 387.
`world.py`, which both lines add to, is 360. Over the budget, as before: `activities/battle.py` 685 and
`budget.py` 408. Sixteen functions branch more than 12 ways, the same sixteen as at the base; none of them is
AP2's. Config constants 51 (49): `POCKET_LIMIT`, `TRAINING_DRAW`. Nothing ships switched off.

## Source and provenance

- **No game source was read for this.** The flows are the pilot's: `state/player/dauntless/tools/restock.py`
  (ported rule by rule), `jutsu_training.md`, `ryo_plan.md`, and the allowlist's notes.
- **Input shapes** are from the captured surface, `data/mcp_surface.json` (2026-11-11). It was consumed, not
  captured again.
- **Item records** (what the shop sells and for what, durability) come from the combat tools' catalog
  (`harness/pvp_turn`), read through `combat.item_record`; the wiring test reads the real catalog.
- **The allowlist** is unchanged but for the wording of two prerequisites (`bank.toPocket`, `bank.toBank`), and
  its review page is rendered again and current.

## Risk and debt

1. **None of it has met the game.** What the game answers to a purchase, a training call or a bank transfer is
   taken from the pilot's notes. Three places rest on one line of a note each: the profile's field
   `earnedExperience`; that an assignment takes amounts, not totals; and the words of a refusal for want of
   money ("money", "afford", "funds").
2. **Two calls here cannot be taken back**: `profile.useUnusedExperiencePoints` and a purchase. Both follow a
   standing order of the director's, are spaced in time, and stop on a refusal.
3. **The run lock needs the session's machine to be able to push to `main`**, with `node`. It makes a commit
   every 15 minutes while a session runs: about a hundred a day. A brain that dies holds the lock for up to an
   hour. Claims and renewals run inside the brain's tick and take a second or more.
4. **A rehearsal is told from a session by its folder alone.** I chose it because the opposite default would
   let a test or a review script claim the real lock. The price is in "Who claims" above.
5. **The player does not yet end its session when a content job is queued** (the player brief, 4.5). It holds
   the lock until its session ends or it is paused.
6. **My readings of the two rulings** are marked as mine in the ledger: 100,000 left in pocket by a transfer and
   a refill under 20,000 (RUL-153); experience to whichever of the two stats trails, and 1,000 as worth a call.
7. Where I would look hardest: the two places that ask the lock; every path that spends (the gate, the pocket,
   the reserve, the day's cap); and what a restart in the middle of a pass or a claim leaves behind.

## Not begun

- AP2's second part: the skill tree, a sensei, the training captcha, changes to PvP 2, owned upgrades (their
  endpoints are `proposed` on the allowlist and wait for a playbook), and level transfers (no rule yet for
  which jutsu gives to which).
- From the token decisions (RUL-2026-11-12-154 item 3): light polls on his turn, which change the fight's
  reads and are a change of their own with its own review; the script that starts short-lived relays, which
  needs Duet's machine.
- A live run. The gate of AP2 is 24 hours live with the queue never idle and no ask-first breach.

## Live-game statement

Zero live requests: no connector call, no game write, no credential or session material. The run lock on the
real `main` was neither read nor written by anything here; the tests that run the lock tool point it at a
repository in a temporary folder. No live relay and no browser session were exercised.
