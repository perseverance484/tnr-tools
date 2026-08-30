# CLOSEOUT.md - how to end a TNR session

> **Mounted addendum 2026-08-30.** Under mounted-repo sessions the repo IS the bundle:
> laws land in docs/ENGINE_LAWS.md + 12b, tool patches commit straight to /skills/
> (skillpack rebuilds dist), results ride harvests/inbox/, and NEXT_SESSION.md's job is
> done by state/active-context.md, rewritten at every close. closeout.py and the forsworn/
> zip layout below are the pre-mount procedure - use them only from a session that cannot
> push. The checks still bind: regenerate-don't-copy, validate everything staged and record
> the exact output, open items with owners.

The test this procedure has to pass: **a fresh session, with no memory of this one, can pick up
the work from the bundle alone and not repeat a mistake we already paid for.**

The previous closeout passed that test. It cost this session about ten minutes of reading and
saved it several hours. Everything below exists because something was nearly lost.

## When to run it

Any of:

- the session is ending
- context is getting long enough that early findings are at risk
- a push cycle finished, whether or not it worked
- a hard-won law was discovered, which is worth an immediate partial closeout on its own

Do not wait to be asked. A closeout that is one turn early costs a turn; one that is one turn
late costs the session.

## What goes in the bundle

    forsworn/
      README.md                  one screen: what this is, state, what to do first
      docs/
        NEXT_SESSION.md          the handoff. Written TO the next session, second person.
        DIFFS_FROM_SOURCE.md     every place our tools or docs disagree with the live game
        LAWS_LEARNED.md          new engine and builder laws found this session, with evidence
        STYLE.md                 house voice, current and complete
        <registry/plan docs>     faction bible, implementation plan, whatever is live
      push/                      every staged manifest, numbered in run order
      sheets/                    the source of truth for content, one per mission
      storyboards/               current renders, regenerated at closeout, never stale
      tools/                     every patched or new script, plus a PATCHES.md
      results/                   the raw results bundles from every push this session

## The five things that are actually lost without it

1. **Laws paid for with a failed push.** Each one cost a real round trip. Write it with the
   evidence that proved it, not just the conclusion, so the next session can tell a verified
   law from a guess.
2. **Tool patches.** A skill reinstall reverts every one. `PATCHES.md` lists each patched file,
   what changed, and why, so the diff can be re-applied or upstreamed.
3. **Which live records are already written.** Ids and their state. Without this a re-push
   either duplicates records or is avoided out of fear.
4. **Working preferences.** Voice rulings, naming rules, process. These are expensive to
   rediscover and embarrassing to get wrong twice.
5. **My own failure modes.** The single highest-value section. Written plainly, as things the
   next session will do again unless warned.

## Steps

1. **Regenerate, do not copy.** Re-render every storyboard from its sheet and re-run every
   validator. A stale artifact in a closeout is worse than a missing one, because it is trusted.
2. **Run `selfcheck.py` and `validate.py` on everything staged.** Record the exact output in
   the README. "0 errors" only means something if it says which file and when.
3. **Diff the tools against the skills.** Anything that differs goes in `tools/` and is listed
   in `PATCHES.md`. Use `cmp`, not memory.
4. **Write `LAWS_LEARNED.md` first, while the reasoning is fresh.** Each entry: the law, the
   evidence, the file that now enforces it. If nothing enforces it, say so.
5. **Write `NEXT_SESSION.md` last**, once everything else exists, so it can point at real files.
6. **Copy in the raw results bundles.** They are the only primary evidence of what the server
   actually did, and summaries lose the detail that matters later.
7. **State the open items with owners.** Anything waiting on the content admin, on art, or on a
   capture, listed plainly rather than buried in prose.

## What NEXT_SESSION.md must contain

- state in one line: what is built, what is pushed, what is verified
- the start ritual: which files to read, in what order, before touching anything
- what exists, with ids
- what is not done, and what is blocked on whom
- the laws that will bite immediately if unknown
- how dauntless works, and the failure modes to watch for in yourself
- standing rules: nothing handed over unvalidated, say what ran, everything ships hidden, a push
  echo is not a read-back, a filtered capture proves nothing

## Assembly

`closeout.py` builds the bundle from the working directory and refuses to write one that is
missing a required document or carries a storyboard older than its sheet. Run it, then read the
README it produces as if you had never seen the project. If it does not orient you, it is not
finished.
