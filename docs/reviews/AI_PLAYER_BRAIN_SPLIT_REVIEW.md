# AI player brain split — independent review, Lane A

Repository: `perseverance484/tnr-tools`. Implementation branch: `fable/ai-player-brain-split`. Frozen head: `25308e2a4f2ee905f1bf3412c3f7f85c1811c62f`. Code commit: `0158936569ee1583a32f08d8cdd23fbdb0929146`. Base: `e4a267cd1ab5ff85c3b2399bab713f2870da6ccb`. Reviewed 2026-11-12.

**Verdict: approve the split within the requested scope. No blocking finding.** The implementation moves the existing logic, preserves the five specified patch points and the command-line/process paths, and makes no additional player behavior change that I found. The two supplied evidence scripts are useful diagnostic comparisons, with the limitations below; independent checks cover their relevant gaps at this head.

I read `AI_PLAYER_BRAIN_SPLIT_HANDOFF.md` first, then `IMPLEMENTATION_HANDOFF.md`. This review covers the move, package lookups/exports, entry point, resident startup/locking, and the two comparison scripts. AP1's underlying behavior and AP2 are outside scope. This approval does not change the separate AP1 review verdict at the base SHA.

## Source movement and the seven changed lines

The production delta is exactly the removal of `player/brain.py` and addition of `player/brain/{__init__,__main__,core,resident,client}.py`. No other production Python file changed. The code commit and frozen head differ only by the handoff document. All existing test files are byte-for-byte unchanged; the only added test file is `test_brain_package.py`.

The supplied `moved_check.py` reports 55 old definitions (36 top-level definitions/constants plus 19 methods), 51 unchanged as source text, no missing definitions and no new ones. Its four changed definitions have precisely the seven reported line substitutions:

| Definition | Lookups redirected through the package |
|---|---|
| `resident.serve` | `answer` |
| `resident.run` | `_lock`, `Brain`, `serve` |
| `client._exchange` | `_await` |
| `client._await` | `_lock`, then `serve(Brain(...), ...)` |

There are **eight redirected name occurrences on seven source lines**: the last line contains both `serve` and `Brain`.

I independently parsed the old file and all four implementation modules. After normalizing only those eight `B.name` occurrences for the five permitted names, their full definition ASTs are equal. This comparison includes decorators, default arguments, constants, the entire `Brain` class and all its methods. The `_client` context-manager decorator is present and unchanged. I also inspected the module-level imports and entry-point code separately; no executable initialization or hidden policy change was added.

The relocation introduces ordinary package metadata changes: functions' `__module__`, source paths and traceback locations now identify their submodules. Those are not evidence of changed decision or delivery logic. The added documentation/import lines account for the increase from 4,128 to 4,185 player lines. Function branching is unchanged. This is a structural split, not a claim that AP6's simplification work has been completed.

## Package names and patch behavior

I loaded the old module into an isolated namespace against the otherwise unchanged production modules, rather than relying only on the hard-coded test list. All **57 original non-dunder names** are exported by `player.brain`; the only additional non-dunder names are `core`, `resident` and `client`. The constants retain their values, imported dependencies still refer to the same objects, and an independent check of **123 global bindings** found no unexpected target change. The package docstring retains the old command-usage paragraph exactly and appends the stated module-location note.

`resident.B` and `client.B` are the actual `player.brain` package object. Their imports do not call through the partially initialized package: the lookups happen when the functions run, after initialization. The six package tests pass, including all specified patched paths:

- Replacing package `Brain` and `serve` affects the resident loop and the client's in-process fallback.
- Replacing package `_lock` affects both the resident and `_await`.
- Replacing package `answer` affects `serve`.
- Replacing package `_await` affects `_exchange`.

The old tests also exercise those same patch points without any edits. Patches to methods of the shared `Brain` class or attributes of shared modules such as `brain.time` and `brain.subprocess` continue to reach the implementations.

I found the earlier report's `exec(..., brain.__dict__)` reproducer in `AI_PLAYER_AP1_REREVIEW4_REVIEW.md` on `chatgpt/review-ai-player-ap1-rereview4`. Its original compilation/setup prefix runs unchanged against the package, including calling the resulting `stopped` function. No missing namespace dependency occurs. I did not rerun that script's subsequent full-suite/walk sections as a separate mutation campaign; the old string replacements no longer plant their historical defect on this base.

**Compatibility boundary:** re-exporting a name does not make every future rebinding of that package attribute propagate into submodule globals. For example, rebinding an internal helper or imported class on `brain` is different from patching the actual object or its defining module. The implementation deliberately preserves the five named patch seams, not a general module-attribute forwarding mechanism. The repository's existing uses and the namespace reproducer inspected here fit that boundary; I found no required consumer broken by it. The claim that all old names remain available is supported, but should not be read as a promise about arbitrary new monkeypatches of every export.

## Entry point, automatic startup and the lock

`__main__.py` imports the package's `main` and passes its return code to `sys.exit`. The old dispatch body is unchanged. The bad-command usage paragraph is unchanged, and the CLI comparator reports matching exit codes and normalized output for all 19 observations: default/status, bad command, settings, five `next` cases, three `put` cases, three `stopped` cases, a second resident, process discovery and SIGTERM.

The new package tests start a resident explicitly and show it answers through the files while an in-process `Brain` constructor is patched to fail. They also show the second resident returns 1 and that `/proc` retains the `player.brain run` command line. This supports the operator's `pgrep -f "player.brain run"` path.

The supplied tests and CLI comparator set `TNR_PLAYER_NO_DAEMON=1`, so they do **not** by themselves exercise `brain next` automatically launching a resident. I tested that path independently in real processes for both the extracted base package and the split, with that environment variable removed:

| Observation | Base | Split |
|---|---|---|
| First `next` greets without a resident | Yes | Yes |
| Following `next TOKEN` launches an actual resident | Exactly one | Exactly one |
| Resident holds `brain.lock` | Yes | Yes |
| Another `brain run` exits without taking over | Exit 1 | Exit 1 |
| Further `next TOKEN` is served while the same resident holds the lock | Yes; token advances | Yes; token advances |
| SIGTERM releases the lock | Yes | Yes |

This exercised the actual `_await -> subprocess.Popen([python, '-m', 'player.brain', 'run'])` path, without mocking `Popen` or creating the resident manually. Each run used a fresh temporary live directory. Cleanup targeted only processes whose environment named that directory. No printed call instruction was executed against the game.

## The two supplied evidence scripts

Neither script is an enforcing acceptance gate: a zero process exit is not a claim of semantic equality. I inspected the output and supplemented it as follows.

**`moved_check.py`:** it reports differences/missing/new names but does not fail on them. Its `ast.get_source_segment` comparisons omit a function's decorators; it also excludes imports and module-level entry-point behavior. As a sensitivity control, I removed only `@contextlib.contextmanager` from a temporary copy of `client.py`. The checker still exited 0 and printed the same 51-of-55 result and seven substitutions as the untouched candidate. The real candidate does retain the decorator, as verified independently. If this script is promoted to a CI gate, include decorators and other relevant AST structure and enforce an explicit difference allowlist.

**`cli_compare.py`:** all 19 printed observations matched on this run. Its normalization removes timestamps, relay identities and numeric timing fields such as `hold` and `wait`, so it cannot establish timing equality. It compares stdout/stderr/exit codes, while the reported live-folder comparison is only a top-level filename listing—not saved-file contents or recursive directory contents. Its comparison loop uses `zip`, it does not assert equal transcript lengths or fail on differences, and resident cleanup is not protected by `finally` if a preceding operation fails. These are non-blocking limits of a diagnostic script, not observed regressions in the split. Before using it as an automated gate, enforce the comparisons, protect cleanup, and make any claimed persisted-state comparison explicit.

For this head, the full source/decorator/global-binding checks establish unchanged logic and data-writing code, the actual CLI run covers packaging and dispatch, and the separate startup check covers the daemon path omitted by the script. I do not infer correctness of AP1's original behavior from those comparisons.

## Verification

| Command/check | Result |
|---|---|
| `python3 -W ignore::ResourceWarning -m unittest discover -s player/tests -t .` | 409 tests, OK, none skipped |
| `python3 -W ignore::ResourceWarning -m unittest -v player.tests.test_brain_package` | 6 tests, OK |
| `python3 docs/reviews/evidence/ai_player_brain_split/moved_check.py e4a267cd player/brain/core.py player/brain/resident.py player/brain/client.py player/brain/__init__.py` | 55 definitions; 51 source-identical; exactly the seven stated substitutions; none missing/new |
| `PYTHONPATH=. python3 docs/reviews/evidence/ai_player_brain_split/cli_compare.py e4a267cd` | 19/19 normalized observations match; identical top-level filename lists |
| Independent AST, exports and global-binding check | Equal definitions including decorators after the exact eight lookups are normalized; 57 names; 123 binding checks |
| Independent automatic resident startup check | Base and split both pass startup, further delivery, exclusion and SIGTERM cleanup |
| Original review namespace-execution prefix | Runs without changes or missing names |
| `python3 -W ignore::ResourceWarning -m unittest scripts/test_player_allowlist.py scripts/test_player_catalog.py` | 46 tests, OK |
| `python3 scripts/player_allowlist.py check` and `report --check` | Zero violations; report current; package is scanned |
| `python3 scripts/rulings_index.py --check` | 322 rulings; index current at the target |
| `python3 scripts/player_size.py` | 4,185 player lines / 23 files; 7,744 test lines; same 16 functions over 12 branches |
| `python3 scripts/check_large_files.py`, `python3 scripts/check_no_real_name.py --commits e4a267cd..HEAD`, `git diff --check` | Clean |

The independent checks are published with this report:

```sh
PYTHONPATH=. python3 docs/reviews/evidence/ai_player_brain_split_review/independent_move_check.py
PYTHONPATH=. python3 docs/reviews/evidence/ai_player_brain_split_review/resident_spawn_check.py
```

They require the repository root as the working directory and the base commit in Git history. I did not repeat the author's 68 mutations, fuzzes, simulated fights or 200 walks; the move comparison and focused process evidence are the relevant additional checks here. Existing behavior tests were run as regression controls, not as a new AP1 acceptance review.

Only this report and two independent check programs are published on `chatgpt/review-ai-player-brain-split`. The reviewed code and supplied evidence scripts remain unchanged. No `fable/*` branch was modified. **Zero live-game requests, game writes, live credentials or session material used. No live relay/browser session exercised.**
