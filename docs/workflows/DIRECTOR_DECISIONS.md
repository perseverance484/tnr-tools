# Workflow — User / Director Decisions

Use when Fable or ChatGPT encounters a decision reserved to the user by repository doctrine or a decision whose player-facing consequence should not become accidental canon through implementation order.

## 1. Identify the decision

A decision belongs here when it affects areas such as:

- balance or exact tuning;
- rewards, rarity, drop rates, difficulty gates, enemy counts;
- publishing / hidden-to-live timing;
- final content direction or acceptance;
- final player-facing UX where multiple valid experiences exist;
- art direction or final visual acceptance;
- whether a risky production workflow should change;
- any other class explicitly reserved by `docs/DOCTRINE.md` or a task contract.

Do not escalate ordinary engineering details that are already settled by source/contracts/tests.

## 2. Separate design from implementation

Present the decision in practical terms:

- what the player/operator will experience;
- what changes if option A vs B is chosen;
- what is reversible vs costly to undo;
- what engineering/tooling consequence follows each option;
- what evidence exists and what remains unknown.

Do not bury the choice inside a code-level question.

## 3. Do not let implementation settle it silently

Until resolved:

- stop the dependent permanent choice from becoming accidental canon;
- use an explicit placeholder only if the user approves that placeholder strategy;
- keep prototypes/reversible explorations clearly labeled;
- do not treat an existing live value as approval merely because it exists.

## 4. Record the ruling in the correct owner

After the user decides, record the result only where it belongs:

- cross-surface rule → `docs/DOCTRINE.md` and its projection process if that is the canonical owner;
- engine law → `docs/ENGINE_LAWS.md` through the law/reconciliation process;
- task/implementation choice → the governing plan/brief/handoff if that is sufficient;
- operational state → existing `state/` machinery;
- art-production status → existing art backlog/produced state where applicable.

Do not create a second canonical ruling database under `docs/agents/` or `docs/workflows/`.

## 5. Shared-workstream rulings

If both an active Fable branch and an active ChatGPT/art/review branch depend on the same newly settled ruling, use the smallest safe coordination mechanism from `docs/DEVELOPMENT_WORKFLOW.md`.

Do not edit both agents' active branches directly.

## 6. Decision prompt format

When useful, present a decision compactly as:

**Decision:** what must be chosen  
**Why it matters:** player/operator consequence  
**Evidence:** what we know  
**Option A:** consequence/tradeoff  
**Option B:** consequence/tradeoff  
**Recommendation:** optional, with reasoning  
**Can defer?:** yes/no and what happens if deferred

A recommendation is advisory. The user still owns the ruling.
