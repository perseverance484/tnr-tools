# Silent Bastion authoring — offline native validation

Validates the package in `state/silent_bastion_authoring/` against `studie-tech/TheNinjaRPG@0651b039a466516a8fe24fc13b56f60dea11b7eb`. Results: `docs/reviews/SILENT_BASTION_AUTHORING_OFFLINE_RESULTS.md`.

```bash
harness/silent_bastion_authoring/run.sh          # generators --check, preflight, gates A + C, C99 D/R/E on the compiled quest
harness/silent_bastion_authoring/run.sh ai       # one gate (ai|content)
```

The isolation is the same as `harness/silent_bastion_condensed99/`: git, bun 1.4.x, python3, `unshare`, Docker, a socket-only throwaway MySQL, no network inside tests, no credentials, no engine edits.

| File | Gate | What runs |
| --- | --- | --- |
| `engine/a_ai.test.ts` | **A** (pure) | All 20 AI units against `AiRule`, the server cap `AI_PROFILE_MAX_RULES`, `insertAiSchema` (incl. innate passives) and `JutsuValidator` (exclusives). Range-gate law and pool-vs-capture drift. **Commander behaviour** through the real decision engine (`performAIaction`) with real captured jutsu records, rule by rule. Router-faithful multi-round loops (`alignBattle` → `performAIaction`, as `routers/combat.ts`) that check for exhaustion give-ups, Split Image once, the Final Stand lifecycle, AR1 and the cooldown probe. Tempest Cleave self-hit probe |
| `engine/c_content.test.ts` | **C** | Compiled quest: `QuestValidator`, flow/save/reward-choice validators, node-by-node equality with the locked `alt99_f4gate`, dialog gating, text presence, puzzle wiring and planted clues, starting-effect allowlists and targets, 625 routes / 16–20 fights. **DB:** real `quests.update` save of the compiled quest; real `ai.updateAiProfile` save of all 20 profiles plus a 21-rule negative control; Countermand stored-row `ItemValidator` |
| `tools/check_validate.py` | **V** | Runs `skills/building-tnr-content/scripts/validate.py` on the composer's validation-only manifest. Passes only when the error set equals the documented one; any new error, or any documented error that disappears, fails the gate (`results/validate_py.txt`) |
| C99 `d_defect` / `r_runtime` / `e_edges` | **D, R, E** on the compiled quest | The frozen C99 runtime gates, with `TNR_COMPILED_QUEST` pointing the fixture at `compiled/quest.candidate.json`. They cover recovery and C1, 18 full attempts with carryover / Medical 100 / player-side effects / Beacon / Arakane hard-fail, and the edge cases |

`engine/lib/units.ts` loads the design, compiles the rule DSL with the engine's own constructors, and builds battles on the router's own grid (`getBattleGrid`). User-jutsu cooldowns come from `originalCooldown`, as in real battle state.

**Fixture limits.**

- Gate A drives AI decisions against a passive player. No damage outcomes, balance or player AI are simulated.
- An adjacent target reads below path length 2 on this grid, so adjacency scenarios use path distance ≥3. Gate A3 also covers distance 2 for Tempest Cleave.
- Runtime gates impose battle outcomes with the upstream settlement pattern.
