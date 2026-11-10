# History rewrite, 2026-11-09 (RUL-2026-11-09-143 part 2)

The director's real first name was removed from the whole history of this repository
(`D-no-real-name`). Every commit id changed. This file is the record; the id map beside it
resolves any old id cited in a doc, a ruling, a review or a handoff.

## What was changed

| Where | Before | After |
|---|---|---|
| Commit messages | 12 messages (2026-11-07 to 2026-11-10) contained the name | the name replaced with `dauntless` |
| File contents, every version | 100 file versions across 48 paths, back to the first upload (2026-06-28) | the name replaced with `dauntless` |
| Author and committer name | 10 commits under a name containing it | `dauntless` |
| Author and committer email | 66 commits with an address containing it | `noreply@anthropic.com` |
| The first version of `scripts/check_no_real_name.py` | a selftest fixture that could be reversed into the name | a made-up word |

Nothing else in any file or message changed. 358 of 365 branch tips have a byte-identical tree
before and after; the other 7 held the name in a tracked file.

## How

- Tool: `git filter-repo` (a40bce548d2c) on a full mirror, with one text rule (the name as a whole
  word), applied to file contents and messages, plus a name and an email callback.
- Scope: all 365 branches. Pull-request refs cannot be rewritten by a push (see "Not done").
- The run lock was held and all 38 workflows were paused for the push, then restored.
- Verified on the private copy before pushing, and again on a fresh clone of all 365 branches
  after: 0 commit messages, 0 file versions, 0 identities contain the name; `git fsck` clean.

## Old ids

`HISTORY_REWRITE_2026-11-09_commit_map.txt` lists `old new` for every commit. A document that
cites a commit by an id from before 2026-11-10 01:50 UTC is citing the old id: look it up there.
The old `main` tip was `2a1db48b`; the new one was `122b2b21`.

## What everyone must do

- **Re-clone.** Any clone or session made before the rewrite must be thrown away, not pulled or
  merged: pushing from one would bring the old history back. The CI guard
  (`.github/workflows/no-real-name.yml`) refuses a push that carries the name in its commit
  messages or files.
- **Loaders.** `forge_loader_user.js` and `builder_loader_user.js` on `main` now pin the bundles
  at the new id of the same release commit (bundle bytes identical). An installed loader still
  points at the old id. It keeps working until GitHub removes the old commits; update the
  installed loader from `main` before that.

## Not done here

- **GitHub still holds the old commits.** They are no longer on any branch, but a public
  repository keeps unreachable commits reachable by id, and the 129 pull-request refs still
  point into the old history. Only the repository owner can ask GitHub Support to remove cached
  views and unreachable commits, and to deal with the pull-request refs. Until then the rewrite
  is incomplete in that sense.
- **Branch `fable/rewrite-probe`** was created to test that a forced push was permitted. It could
  not be deleted from this session (branch deletion is refused here). It holds one empty commit
  and can be deleted.
- The `harvests/inbox` results bundles and sent push manifests had the name replaced like every
  other file, in history as well as at the tip.
