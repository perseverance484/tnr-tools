# TNR Tag Design Audit and Proposal Framework

**Status:** DESIGN AUDIT / PROPOSAL FRAMEWORK — no new tags approved  
**Repository baseline:** `perseverance484/tnr-tools@18c6a2554c1bf9231e00e46108a5a7faf66387aa`  
**Game-source pin used for mechanics:** `studie-tech/TheNinjaRPG@bdec2883`  
**Lead role:** Content Designer  
**Scope:** player-facing combat tags, with emphasis on straightforward utility that earns a slot in strict 1v1 PvP  
**Live-game activity:** zero requests / zero writes

## 1. Executive conclusion

The current combat vocabulary is already broad. The generated `AllTags` union contains **76 tags**. The strongest opportunity for new utility is therefore **not another standalone modifier, another hard-prevention tag, or another subsystem that tracks several rounds of battle state**.

The best proposal model is:

> **Start with a common existing combat mechanic, identify one important interaction it does not currently support, and add a simple companion/rider tag that changes exactly that interaction.**

This fits both the existing engine and the design target.

The engine already has a native companion-tag pattern: `wound`, `vamp`, and `consume` are rejected unless `damage` or `pierce` appears on the same action. The validator therefore already supports the concept of “this tag only makes sense when paired with X.”

That pattern is especially suitable for new 1v1 utility because:

- the player can understand the rule in one sentence;
- the tag modifies a mechanic they already understand;
- it creates a meaningful variant without replacing the base mechanic;
- the three-tag limit naturally prices the utility;
- it usually reuses an existing combat event hook instead of inventing a new battle-wide state machine;
- its power can be bounded locally instead of scaling unpredictably with fight length.

The director-provided examples illustrate the right shape even though they are **not approved**:

- a Shield companion that changes Shield’s interaction with Pierce;
- a Poison companion that changes what happens each time Poison triggers.

By contrast, the recent cooldown-control concepts exposed a poor shape: their strength increased sharply as the opponent’s normal jutsu rotation depleted, creating late-fight lockout risk and requiring more rules to stay fair. That is exactly the kind of design this framework should reject before implementation work begins.

---

## 2. Evidence and source precedence

This audit uses the repository’s current authority system.

Primary contract evidence:

- `45c_DATA_constructors.json` — current generated tagged-shape union; authoritative inventory of tag constructors.
- `45g_DATA_checks.json` — generated/law-backed authorability and cross-field checks.
- `docs/ENGINE_LAWS.md` — effect timing, stacking, companion requirements, and other engine laws.
- `skills/building-tnr-content/references/jutsu.md` and `balance.md` — player-jutsu and balance doctrine.

Pinned source checked directly:

- `app/src/validators/combat.ts`
- `app/src/libs/combat/tags.ts`
- `app/src/libs/combat/process.ts`
- `app/drizzle/constants.ts`

### Source disagreement surfaced

The AI reference still describes its effect vocabulary as the “full canonical list” and elsewhere refers to 72 tag literals. The current generated `45c` union contains **76**. Per `docs/00_INDEX.md` / doctrine, the generated contract wins. This report therefore uses the 76-tag generated set as the exclusion baseline.

This report does **not** promote itself into engine canon and does not replace `45c`, `45g`, or `ENGINE_LAWS.md`.

---

## 3. Task-specific design constraints

For this design exercise, new utility tags should satisfy the following director constraints:

- PvP is balanced around **strict 1v1**, not team combat.
- New effects should have value in ordinary 1v1 fights.
- Existing prevention effects are already numerous; another “Prevent X” should be exceptional.
- Utility should be straightforward enough to read and reason about quickly.
- The normal turn shape is commonly one 60 AP jutsu plus one 40 AP jutsu.
- Jutsu cooldowns are long enough that concepts depending on rapid rotation/repetition are poor fits.
- A new tag must be useful enough to justify engine complexity, not merely novel.

The 100 AP turn and the 40/60 content convention are already repository doctrine. The cooldown-shape observations above are task-specific director input for this design pass and are not promoted here as a new engine law.

---

## 4. Existing tag landscape

The 76 tags fall into six broad design families.

| Family | Count | Tags | Design saturation |
|---|---:|---|---|
| Direct damage and lethal outcomes | 7 | `damage`, `pierce`, `poison`, `wound`, `afterburn`, `recoil`, `onehitkill` | Mature. Several distinct damage models already exist. |
| Damage modifiers and reactive conversions | 10 | `increasedamagegiven`, `decreasedamagegiven`, `increasedamagetaken`, `decreasedamagetaken`, `weakness`, `reflect`, `absorb`, `lifesteal`, `vamp`, `consume` | Very mature. Raw throughput modifiers are especially saturated. |
| Defense, healing, and resource pools | 13 | `heal`, `increaseheal`, `decreaseheal`, `healprevent`, `shield`, `barrier`, `finalstand`, `onehitkillprevent`, `drain`, `increasepoolcost`, `decreasepoolcost`, `increasemaxpools`, `decreasemaxpools` | Mature. New simple +/- resource or healing tags are unlikely to add enough. |
| Stats and action economy | 8 | `increasestat`, `decreasestat`, `increasecooldown`, `decreasecooldown`, `increaserange`, `timecompression`, `timedilation`, `stun` | Broad coverage. New global economy manipulation risks overlap or lockout. |
| Control, cleansing, prevention, movement, combat state | 22 | `buffprevent`, `cleanseprevent`, `cleanse`, `clearprevent`, `clear`, `debuffprevent`, `disarm`, `elementalseal`, `fleeprevent`, `flee`, `moveprevent`, `move`, `redirection`, `robprevent`, `rob`, `sealprevent`, `seal`, `stealth`, `stunprevent`, `summonprevent`, `summon`, `immunity` | Most saturated family. Avoid expanding by symmetry alone. |
| Meta, transfer, system, and noncombat | 16 | `activatesagemode`, `clone`, `copy`, `marriageslotincrease`, `noncombatincreasereskins`, `injectjutsus`, `mirror`, `noncombatconsumereward`, `noncombatgainskill`, `repair`, `removebloodline`, `rollbloodline`, `rollsagemode`, `unlockitemvariant`, `unknown`, `visual` | Mostly not useful as the model for new simple PvP utility. |

### 4.1 Prevention is already overrepresented

There are **12 direct `*prevent` tags**:

`buffprevent`, `cleanseprevent`, `clearprevent`, `debuffprevent`, `fleeprevent`, `healprevent`, `moveprevent`, `onehitkillprevent`, `robprevent`, `sealprevent`, `stunprevent`, `summonprevent`.

There is also `immunity`, which specifically blocks prevention effects from being applied.

That is enough evidence to treat “add the missing prevent counterpart” as a default rejection, not a default design pattern. A new prevention tag should only be considered when it creates a qualitatively different 1v1 interaction rather than completing a naming symmetry.

### 4.2 The engine already has many scalar opposites

The vocabulary already contains several +/- pairs:

- damage given up/down;
- damage taken up/down;
- healing up/down;
- pool cost up/down;
- max pools up/down;
- stats up/down;
- basic-action cooldown up/down;
- time-compression/time-dilation AP-cost directionality.

This makes “the opposite of an existing modifier” a weak source of new ideas. Symmetry is not enough to justify a tag.

### 4.3 Reactive damage riders are a strong existing pattern

Pinned source defines eight post-damage modifier types:

- `wound`
- `afterburn`
- `reflect`
- `recoil`
- `lifesteal`
- `absorb`
- `vamp`
- `consume`

These are strategically important because they hook into damage that is already being processed, then change one consequence of that event.

This is a useful model for future utility: **reuse a known trigger and change one result**.

### 4.4 Same-action companion tags are already first-class

`SuperRefineEffects` currently enforces:

- `wound` requires `damage` or `pierce`;
- `vamp` requires `damage` or `pierce`;
- `consume` requires `damage` or `pierce`.

This is the closest existing architectural precedent to the desired new-tag direction.

A companion requirement has three advantages:

1. **Legibility:** the player can reason from the base tag.
2. **Balance cost:** the companion consumes one of the same jutsu’s limited tag slots.
3. **Implementation containment:** the new effect can often operate inside the existing base tag’s event path.

### 4.5 Shared cooldowns are already an explicit balance lever

The pinned source currently puts **17 tags** on `SHARED_COOLDOWN_TAGS`:

`barrier`, `buffprevent`, `cleanse`, `cleanseprevent`, `clear`, `clearprevent`, `consume`, `debuffprevent`, `drain`, `increasepoolcost`, `moveprevent`, `pierce`, `poison`, `seal`, `stun`, `summon`, `vamp`.

Therefore a new proposal should explicitly say whether it:

- creates its own shared-cooldown identity;
- inherits the practical recurrence limit of its companion;
- needs no shared cooldown because its base mechanic already constrains it.

This should be decided deliberately rather than discovered during implementation.

---

## 5. What the current tags teach us about good utility

### Pattern A — modify an existing combat transaction

Examples:

- `reflect`: incoming damage causes reflected damage;
- `absorb`: incoming damage restores pools;
- `lifesteal`: dealt damage restores health;
- `consume`: same-action dealt damage becomes a shield;
- `recoil`: dealt damage creates self-damage;
- `afterburn`: incoming damage creates additional damage.

These tags are easy to understand because the trigger is already visible: **damage happened**.

**Design lesson:** prefer “when X happens, change one consequence of X” over “for the next several rounds, maintain a new invisible rules engine.”

### Pattern B — modify an existing status mechanic

Examples:

- damage-modifier effects alter how Damage resolves;
- heal modifiers alter Heal;
- `increasepoolcost` changes resource cost;
- `increaserange` changes a known basic-action attribute;
- `weakness` changes susceptibility to already-defined categories.

**Design lesson:** a new tag is easier to justify when the base mechanic remains recognizable after modification.

### Pattern C — hard control or hard prevention

Examples:

- Stun;
- Disarm;
- Elemental Seal;
- Bloodline Seal;
- movement prevention;
- buff/debuff prevention;
- the many specific prevent tags.

These are straightforward but the family is already crowded. New additions here tend to reduce available choices rather than create new ones.

**Design lesson:** do not reach for denial unless the interaction cannot be expressed more positively or conditionally.

### Pattern D — transfer / board-state mechanics

Examples:

- Copy;
- Mirror;
- Clone;
- Summon;
- Redirection.

These are mechanically distinctive but require more targeting, state, priority, cap, or entity rules.

**Design lesson:** these are poor default models for the requested straightforward 1v1 utility batch.

### Pattern E — repeated-state / timing mechanics

Examples:

- Poison reacts to resource spending;
- Wound retains original-damage state;
- Copy/Mirror retain transferred effects and budgets;
- time effects alter AP costs.

These can be excellent mechanics, but only when the state is compact and visible.

**Design lesson:** one local counter or multiplier is acceptable; a battle-wide ledger of prior actions/cooldowns should face a much higher bar.

---

## 6. Why recent proposal directions failed

This section records design-process lessons, not rejected mechanics as candidates.

### Too much symmetry

Several ideas were essentially “Shatter, but for another buff class.” That creates vocabulary bloat without opening a new play pattern.

**Rule:** do not propose a family merely because one member is useful.

### Existing mechanics were not excluded first

Heal reduction, resource-cost pressure, cooldown modification, seals, movement control, and multiple prevention effects were already present.

**Rule:** every brainstorm begins by comparing against the current generated 76-tag set.

### Team/multi-target assumptions slipped into a 1v1 game

Target substitution, ally protection, and similar concepts make more sense in party combat than in TNR’s PvP design target.

**Rule:** if the mechanic’s primary fantasy needs a third combatant, reject it for this workstream.

### Long-cooldown cadence invalidated rotation mechanics

A mechanic that rewards repeatedly cycling different jutsu sounds good abstractly but does not fit a combat system where most jutsu stay unavailable for many rounds.

**Rule:** proposals must be tested against actual turn/cooldown cadence before they reach naming/tuning.

### Global cooldown manipulation had a bad power curve

The combined Overload/Stasis line was weak while many choices remained available and potentially overwhelming once the normal rotation was exhausted.

**Rule:** reject mechanics whose utility grows fastest as the opponent’s option count approaches zero.

### Complexity was compensating for a weak core idea

When a mechanic needs exceptions, per-round limits, per-jutsu eligibility, memory rules, and lockout safeguards before it feels fair, the original concept is probably not simple utility.

**Rule:** if the explanation keeps growing to save the mechanic, discard the mechanic.

---

## 7. Recommended proposal method: the interaction-edge method

Do not begin with names.

Begin with an existing **high-value 1v1 mechanic** and map its important interactions.

For each existing mechanic, ask:

1. What starts it?
2. What does it affect?
3. What currently counters it?
4. What does it currently ignore or bypass?
5. What happens when it triggers repeatedly?
6. What happens when it breaks, expires, is cleared, or is cleansed?
7. Does the engine already expose that event in `tags.ts` / `process.ts`?
8. Is there one missing interaction that would create a useful build choice?

Then propose a tag that changes **one edge** of that interaction graph.

### Good source mechanics for this method

High-signal bases include:

- Shield;
- Poison;
- Damage Reduction;
- Pierce;
- Wound / Afterburn;
- Heal;
- Absorb / Reflect / Lifesteal / Consume;
- resource-cost modification;
- Cleanse / Clear;
- Stun;
- Seal;
- Stealth.

These mechanics already occur in normal 1v1 combat and have known hooks.

### Poor starting points

Avoid beginning from:

- “what status does another game have?”;
- “what prevent counterpart is missing?”;
- “what opposite modifier is missing?”;
- multi-ally targeting;
- arbitrary battle-history tracking;
- full cooldown-board manipulation;
- a name with no identified interaction gap.

---

## 8. Proposal gates

A candidate should pass all of these before numbers are tuned.

### Gate 1 — 1v1 relevance

Can the mechanic matter in an ordinary duel with exactly two players?

If it mainly becomes interesting with allies, multiple enemies, aggro, or target swapping, reject it.

### Gate 2 — existing-tag exclusion

Can the same player-facing result already be produced closely enough by a current tag or two-tag combination?

If yes, reject it unless the new tag changes a genuinely important interaction rather than convenience or wording.

### Gate 3 — one-sentence rule

Can the player-facing behavior be stated in one sentence without nested conditions?

If not, simplify or reject it.

### Gate 4 — common-state value

Will the mechanic matter in a normal fight often enough to justify one of only 2–3 tag slots?

A tag that only matters in a rare edge case should normally be an interaction rule on another tag, not a standalone effect.

### Gate 5 — choice, not merely throughput

Does the effect change a decision, matchup, timing window, or build interaction?

“X% more of the same number” has a higher burden than a tag that changes how two mechanics interact.

### Gate 6 — bounded power curve

Does its value remain understandable from early fight to late fight?

Reject mechanics that become dramatically stronger simply because the opponent has fewer remaining options.

### Gate 7 — local state

Can the mechanic operate from:

- the companion effect;
- the current action;
- the current consequence;
- one small counter on the effect itself?

Prefer that over global history, per-jutsu ledgers, or multi-round hidden state.

### Gate 8 — counterplay without hard denial

Can the opponent still make a meaningful choice?

A good utility tag pressures or changes efficiency. It should not casually become “you cannot use your kit.”

### Gate 9 — engine-seam fit

Does an existing runtime hook already know when the relevant event happens?

Examples:

- damage packet;
- shield absorption;
- poison trigger;
- resource spending;
- healing;
- cleanse/clear;
- effect application;
- effect expiration.

Reusing a hook is strongly preferred.

### Gate 10 — tag-slot economics

Does the tag’s value justify consuming a tag slot?

For companion tags, this is often naturally healthy: the specialized version of a Shield, Poison, or attack gives up another possible tag.

---

## 9. Preferred new-tag archetypes

Ordered from most promising to least promising for this workstream.

### Tier A — companion interaction modifier

> Must be on the same jutsu as an existing tag and changes one rule of that tag.

This is the preferred archetype.

Why:

- proven validator pattern;
- minimal new player vocabulary;
- clear build tradeoff;
- naturally bounded;
- usually low/medium implementation complexity.

### Tier A — reactive rider on an existing event

> When an already-understood event occurs, add or modify one consequence.

Examples of existing architecture: Reflect, Absorb, Lifesteal, Afterburn, Consume.

This is also strong when it does not merely add more damage.

### Tier B — simple status modifier

> Alters one attribute of an existing status/action in a straightforward way.

Useful, but the current system already has many scalar modifiers, so novelty must be strong.

### Tier C — standalone control

> Adds a new state that changes what the player may do.

High burden because TNR already has extensive control/prevention vocabulary.

### Tier D — battle-wide subsystem

> Tracks rotations, histories, multiple cooldowns, or several conditional states.

Avoid for this batch unless the mechanic is transformative enough to justify substantial implementation and UX complexity.

---

## 10. Proposal card template

Every future candidate should be written in this compact form before discussion expands.

### Name
Player-facing name + proposed internal slug.

### One-line rule
Exactly what the tag does in one sentence.

### Base interaction
What existing tag/action/event this modifies.

### Companion requirement
None, or “must be paired with X on the same action.”

### Trigger
One of: cast / damage dealt / damage received / shield absorbs / shield breaks / poison triggers / resource spent / heal / cleanse / clear / effect applied / effect expires / other.

### Effect
What single behavior changes.

### Timing
Instant, cast-round setup, next-round active, per-trigger, expiration, etc. Must be checked against law 75 rather than assumed.

### Stacking
Choose explicitly:

- no stack;
- refresh duration;
- replace magnitude;
- stack additively;
- stack multiplicatively;
- ramp with cap.

### Removal / prevention
State how Cleanse, Clear, Buff Prevent, Debuff Prevent, and any relevant specific prevention interact.

### Copy / Mirror
Eligible or excluded. This must be explicit for any transferable buff/debuff.

### Shared cooldown
None / inherits practical cadence from companion / add to `SHARED_COOLDOWN_TAGS`.

### 1v1 use case
One ordinary duel situation where the tag earns its slot.

### Counterplay
What the opponent can actually do differently.

### Existing-tag comparison
Name the closest current tags and explain why they cannot already produce this interaction.

### Engine seam
Expected implementation location:

- validator only;
- `tags.ts`;
- `process.ts`;
- constants/shared-cooldown list;
- copy/mirror eligibility;
- new state field.

### Balance values
TBD unless explicitly ruled by the director.

---

## 11. Implementation-complexity classes

Design proposals should carry an implementation class before approval.

### Low

- same-action companion check;
- change one existing branch in a known event;
- no new persistent battle state.

This is the ideal class.

### Medium

- adds one small counter/multiplier to an effect;
- uses an existing trigger repeatedly;
- requires explicit stacking/cap logic.

Still appropriate if the player-facing gain is strong.

### High

- tracks multiple jutsu or prior actions;
- rewrites target selection;
- adds global battle state;
- changes several unrelated systems;
- needs many exceptions to prevent lockout.

A High-complexity tag should be presumed rejected unless it creates a major new playstyle.

---

## 12. Complete current-tag inventory

This appendix is an exclusion map for ideation, not a replacement for the generated contracts.

### Direct damage / lethal

- **damage** — direct formula/static/percentage damage; instant.
- **pierce** — direct damage that bypasses normal damage reduction and shield absorption.
- **poison** — reacts to the afflicted user spending Chakra/Stamina and deals damage from that spend.
- **wound** — same-action Damage/Pierce companion; stores original hit damage and applies wound damage over later turns.
- **afterburn** — converts a portion of qualifying incoming damage into additional afterburn damage; Pierce excluded.
- **recoil** — converts a portion of the afflicted user’s dealt damage into self-damage; Pierce excluded.
- **onehitkill** — chance-based immediate lethal effect.

### Damage modifiers / reactive conversions

- **increasedamagegiven** — outgoing damage multiplier.
- **decreasedamagegiven** — outgoing damage reduction.
- **increasedamagetaken** — incoming damage multiplier.
- **decreasedamagetaken** — damage reduction.
- **weakness** — scoped vulnerability by item/jutsu/element/stat/general categories.
- **reflect** — converts qualifying incoming damage into reflected damage.
- **absorb** — converts qualifying incoming damage into Health/Chakra/Stamina restoration.
- **lifesteal** — ongoing damage dealt restores Health.
- **vamp** — same-action Damage/Pierce companion; immediate heal from that action’s damage.
- **consume** — same-action Damage/Pierce companion; converts that action’s damage into a temporary shield.

### Defense / healing / pools

- **heal** — restores selected pools.
- **increaseheal** — increases healing given.
- **decreaseheal** — reduces healing given.
- **healprevent** — prevents healing effects.
- **shield** — temporary HP; current process lets Pierce, Reflect, and Wound bypass shield absorption.
- **barrier** — battlefield structure with health and absorption percentage.
- **finalstand** — successful effect prevents reduction below 1 HP.
- **onehitkillprevent** — prevents One Hit Kill.
- **drain** — periodic Health/Chakra/Stamina drain.
- **increasepoolcost** — increases selected resource costs.
- **decreasepoolcost** — decreases selected resource costs.
- **increasemaxpools** — increases maximum/current pools.
- **decreasemaxpools** — decreases maximum/current pools.

### Stats / action economy

- **increasestat** — increases selected stat/general categories.
- **decreasestat** — decreases selected stat/general categories.
- **increasecooldown** — increases cooldown of selected adjustable **basic actions**.
- **decreasecooldown** — decreases cooldown of selected adjustable **basic actions**.
- **increaserange** — increases range of selected adjustable **basic actions**.
- **timecompression** — increases affected action AP cost by 10.
- **timedilation** — decreases affected action AP cost by 10.
- **stun** — reduces next-turn AP; existing stuns use maximum AP reduction rather than stacking.

### Control / cleanse / prevention / movement / state

- **buffprevent** — prevents buffs.
- **cleanseprevent** — prevents Cleanse.
- **cleanse** — removes negative effects.
- **clearprevent** — prevents Clear.
- **clear** — removes positive effects.
- **debuffprevent** — prevents debuffs.
- **disarm** — prevents weapon use.
- **elementalseal** — prevents selected-element jutsu use.
- **fleeprevent** — prevents Flee.
- **flee** — attempts to leave battle.
- **moveprevent** — prevents movement/redirection.
- **move** — battlefield movement effect.
- **redirection** — instant push/pull.
- **robprevent** — prevents Rob.
- **rob** — steals pocket ryo in eligible 1v1 combat.
- **sealprevent** — prevents Bloodline Seal.
- **seal** — seals base bloodline effect.
- **stealth** — stealth state; existing engine law notes stealth blocks attacking.
- **stunprevent** — prevents Stun.
- **summonprevent** — prevents Summon.
- **summon** — creates a combat summon.
- **immunity** — blocks specified prevention effects from being applied.

### Meta / transfer / system / noncombat

- **activatesagemode** — runtime-only; explicitly rejected on authored records.
- **clone** — creates a scaled clone combatant.
- **copy** — copies eligible positive effects from opponent to self, with transfer eligibility/priority/cap rules.
- **marriageslotincrease** — noncombat account/system effect.
- **noncombatincreasereskins** — noncombat account/system effect.
- **injectjutsus** — injects specified jutsu.
- **mirror** — mirrors eligible negative effects from self to opponent, with transfer eligibility/priority/cap rules.
- **noncombatconsumereward** — noncombat reward behavior.
- **noncombatgainskill** — noncombat skill grant.
- **repair** — repair behavior.
- **removebloodline** — item-only bloodline removal effect.
- **rollbloodline** — item-only bloodline roll effect.
- **rollsagemode** — item-only sage-mode roll effect.
- **unlockitemvariant** — item-variant unlock behavior.
- **unknown** — schema member / internal fallback; not a useful design target.
- **visual** — visual-only effect.

---

## 13. Recommended next design workflow

For the next ideation pass:

1. Pick **6–10 common 1v1 base mechanics** rather than brainstorming free-form names.
2. For each base mechanic, draw its current interaction edges.
3. Identify only the gaps that would matter in ordinary duels.
4. Prefer companion/rider solutions.
5. Write each surviving idea as one proposal card.
6. Reject any card that fails the gates before discussing exact percentages, durations, or names.
7. Present only the strongest few to the director.
8. After director selection, hand the approved mechanic to Fable for implementation analysis against the pinned source; do not implement unapproved candidates.

A good output from this process should be **a small number of obvious, legible interactions**, not a large taxonomy of clever effects.

## 14. Bottom line

The system does not need more tags merely because mechanical gaps can be named.

It needs tags that:

- matter repeatedly in 1v1;
- cannot already be approximated well;
- change one meaningful interaction;
- fit into a one-sentence rule;
- reuse a known combat hook;
- stay bounded throughout the fight;
- and are worth sacrificing a scarce tag slot for.

The best default search space is therefore **companion tags and reactive riders around strong existing mechanics**, not new prevention families or new battle-wide subsystems.
