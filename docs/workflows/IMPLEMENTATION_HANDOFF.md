# Workflow — Implementation Handoff

Use when Fable / Claude Code freezes implementation for independent review.

The purpose is to make the repository and exact SHA sufficient evidence even if the implementation conversation disappears.

## 1. Freeze the target

Before handoff:

- finish all intended commits in scope;
- push the branch;
- verify the remote branch head;
- stop changing the handed-off SHA until review returns.

If a blocking correction is unavoidable before review starts, issue a new handoff with the new exact SHA.

## 2. Required handoff fields

### Repository / refs

- repository: `perseverance484/tnr-tools`;
- implementation branch;
- exact base SHA;
- exact head SHA;
- intended integration target (normally current `main` unless the task says otherwise).

### Scope

- one-sentence objective;
- changed files/directories;
- behaviour implemented;
- task/pass boundary;
- what explicitly was not implemented.

### Verification

List exact commands and results for:

- tests;
- fixture generation;
- build/bundle regeneration/diff;
- validators/selftests;
- doctrine/law/generated-data gates;
- static checks/greps;
- any task-specific safety harness.

Do not say only "tests pass." Give enough detail to identify what ran.

### Source/provenance

When applicable identify:

- exact pinned `studie-tech/TheNinjaRPG` SHA;
- external package/version used for parity checks;
- generated contract/report versions and producer commands;
- captures/fixtures used;
- whether generated artifacts were rebuilt or merely consumed.

### Risk / debt

List:

- known defects/debt;
- deliberate deviations from the plan/brief;
- inferred/unverified browser or live-session risks;
- migration/compatibility assumptions;
- user decisions still open;
- anything the author believes the reviewer should attack especially hard.

## 3. Live-game statement

State explicitly:

- whether any live request was made;
- whether any game write was made;
- whether any live credential/session material was used;
- browser/live-session checks not performed.

For zero-live-request tasks, the expected handoff should make clear that the review target was built/tested without contacting the game.

## 4. Generated/bundled artifacts

If the task checks in generated or bundled output:

- identify its source files/build command;
- state whether regeneration is deterministic/reproducible;
- state whether the checked-in output matches a fresh build;
- identify any generated file intentionally left stale and why.

## 5. Correction handoff

After review fixes, return a new exact head SHA and summarize:

- which findings were accepted/rejected;
- files changed for each accepted finding;
- tests/gates rerun;
- whether any wider architecture/assumption changed;
- whether a narrow re-review is safe or full relevant scope should be repeated.

The reviewer, not the author, decides whether the evidence supports a narrow re-check.

## 6. Suggested compact template

```text
Repository: perseverance484/tnr-tools
Branch: fable/<task>
Base: <sha>
Head: <sha> (FROZEN)
Integration target: main @ <verified sha>

Objective:
Changed:
Not begun / out of scope:

Verification:
- <command> — <result>

Source/provenance:
- game source: <repo @ sha>
- generated/fixture inputs: ...

Known debt/deviations:
Open user decisions:
Unverified browser/live/session items:
Live requests/writes/credentials used: none / explain if explicitly authorized
```
