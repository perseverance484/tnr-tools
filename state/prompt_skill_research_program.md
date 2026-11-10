# Skill research program: plan

Status: PLANNED (director, 2026-11-09, RUL-2026-11-09-138). It is a new phase that starts after the
skill overhaul (`state/prompt_skill_overhaul.md`) completes P7. Until then this file is the plan, not
a build contract. Each topic below becomes its own approved brief (`state/prompt_research_<topic>.md`)
when its turn comes.

---

## 1. Why

The overhaul captures what we already know. This program adds what the wider craft knows, and keeps
the skills improving after the overhaul ends. Each topic runs one loop:

```
research  ->  principles  ->  tools  ->  evals  ->  (real use)  ->  lessons  ->  back into the skill
```

- **Research:** a deep, sourced study of how the craft is practised (talks, books, postmortems,
  studio writing, academic work where it exists).
- **Principles:** the findings that apply to TNR's constraints, written into the skill's references
  with citations, each stating which TNR constraint it was checked against.
- **Tools:** every principle that can be computed becomes a script, so agents apply it instead of
  remembering it.
- **Evals:** requests added to the skill's eval set that show the gain against the skill before the
  topic.
- **Lessons:** after each real project, what was slow or wrong goes back into the skill as a reviewed
  change.

---

## 2. Order of topics

| # | Topic | Feeds | Why this order |
|---|---|---|---|
| R1 | Combat VFX and animation | animating-tnr-combat | The widest gap between our practice and established craft, the most visible to players, and the topic the director asked for first. |
| R2 | Encounter and boss design | designing-tnr-content: rule patterns, boss grammar, simulator targets | Telegraph readability and difficulty tuning are well studied in action and raid games. |
| R3 | Rewards and economy | designing-tnr-content: payout model | Faucets and sinks, drop-rate design and weekly pacing decide whether events feel worth playing. |
| R4 | Game writing | designing-tnr-content: writing guide | Battle text, barks and story told through logs are the voice players read every turn. |
| R5 | Quest and event structure | designing-tnr-content: quest structure catalogue | Variety, pacing and retention in quest design. |

R1 starts first. R2 to R5 can follow in any order the director sets, and two can run at once if
they feed different skills.

---

## 3. How a topic runs

Each topic is four steps, each ending in a reviewed handoff and a director checkpoint.

| Step | Who | Delivers | Director checkpoint |
|---|---|---|---|
| A. Research plan | Claude (planning) | The topic brief: questions, source plan, TNR constraints, out-of-scope list | Approve the questions |
| B. Research | A research agent (deep research, sourced) | `docs/research/<topic>/REPORT.md` + `SOURCES.md` | Read the findings summary |
| C. Synthesis | Implementer (Fable) | Principles added to the skill's references; tool specs; eval requests | Approve which principles become rules |
| D. Build | Implementer (Fable) | Tools with selftests; evals run before and after; packaged skill | Install |

ChatGPT reviews C and D at exact SHAs, as with the overhaul.

---

## 4. Research protocol (all topics)

- **Questions first.** Each topic brief lists the questions the research must answer. The research
  answers those and records anything important it found outside them separately.
- **Source quality, best first:**
  1. Practitioners describing their own shipped work (GDC and similar talks, studio blogs,
     postmortems, books by working artists and designers).
  2. Academic or peer-reviewed work (perception, readability, player behaviour).
  3. Widely used craft references and tutorials from established artists.
  4. General articles, only to find tier 1-3 sources.

  Every finding cites at least one tier 1-3 source. A claim with no such source is labelled as
  unsourced opinion and cannot become a rule.
- **Translate to TNR.** Every finding is checked against TNR's real constraints before it can become
  a principle. For R1 these are:
  - 50 px rendition with linear filtering;
  - clips of 2.5 hex heights;
  - clips over fighters;
  - load skew between neighbouring hexes;
  - hex grid;
  - turn-based rounds;
  - mobile players.

  A finding that does not survive translation is recorded as "does not apply, because …".
- **Disagreement.** Where sources disagree, the report says so and gives the director the options;
  it does not average them.
- **No copying.** The research describes techniques and principles in its own words. It never brings
  in other games' art, frames or proprietary assets. Visual references are linked, not committed.
- **Length.** The REPORT is decision-ready: findings, principles, open questions. Detail goes in an
  appendix.
- **Live game.** Research makes no live game requests. Tools are built offline against fixtures and
  the pinned game source.

---

## 5. R1: Combat VFX and animation (first topic)

### 5.1 Questions

**Motion and timing**

1. How do 2D VFX artists structure an effect in time (anticipation, impact, dissipation), and what
   frame counts and holds work at about 20 fps (our 50 ms per frame)?
2. Which easing and spacing curves are standard for each motion (launch, impact, fall, fade,
   expansion), and how are they applied to flipbook frames rather than tweens?
3. Smear frames, impact frames and hit-stop: how they are used in 2D games and anime, and what
   survives in a 20-40 frame clip.

**Shape and readability**

4. Shape language for effects: how silhouette, direction and edge style make an effect read as
   heavy, fast, sharp or magical, especially at small sizes.
5. How do fighting games and MMOs make telegraphs and danger zones readable among other effects?
   Covers colour coding, contrast, pulsing, layering order and clutter limits.
6. Readability at very small scales: what pixel and indie artists do to keep an effect legible at 50
   px, including outlines, value bands and minimum feature sizes.

**Value and colour**

7. How to build an elemental colour ramp: hue shifts, the hot core with cool falloff, saturation
   placement. How to fake glow and bloom without real HDR.
8. Contrast against varied backgrounds (our light and dark boards) and against characters: value
   separation rules artists use.

**Technique**

9. Flipbook versus procedural particles versus hand-drawn effects: when each is used in 2D games,
   and what a procedural toolkit for flipbook output usually contains.
10. Effects that join across tiles or cells (our slicing problem): any precedent in tile-based or
    tactics games.
11. Ground effects and persistent hazards: how games show what lingers and for how long, and how
    they keep it from hiding the board.

**Process**

12. How VFX teams review effects: checklists, playback at speed, judging in-game rather than in
    isolation.
13. Naruto-style effects: how the anime and the licensed games show elements (fire, water,
    lightning, wind, earth, crystal, sealing) and what makes them read as "ninja".

### 5.2 Out of scope

3D VFX pipelines, shaders, engine particle systems we cannot run, audio, and anything needing a
change to the game's renderer.

### 5.3 Expected tools (the build step confirms them against the findings)

- **Timing library:** easing curves and named timing templates (e.g. "heavy impact 28f: 6
  anticipation, 2 impact, 3 hold, 17 dissipate"), used by every primitive.
- **Primitive library:** parameterised generators for shockwave rings, slash arcs, shard bursts,
  sparks and embers, smoke, ground cracks, light blooms, seal circles and impact frames. Each outputs
  strips at the engine's sizes.
- **Palette ramps:** per element and per owner, following the director's colour rules (no green;
  cyan only for safe hexes, except the Refraction line).
- **Readability checker:** scores a strip at true scale. It checks contrast against both boards,
  coverage of fighters and meters per frame, flicker and stray pixels, peak hold, feature size at
  50 px, and the round's clutter budget. It fails loudly; it does not just warn.
- **Composer:** layers primitives, offsets timing, adds skew-safe holds at seams. It sits on the
  overhaul's `slice.py`, `tagwire.py` and `preview.py`.

### 5.4 Evals added

- "A fire slash on one target."
- "A crystal shatter across a 3-hex line."
- "A water pool that lingers 2 rounds."
- "A seal circle omen then eruption."

Each is scored before and after the topic on three things: the readability checker's score, the
director's 1-5 score, and the time taken.

---

## 6. R2-R5: starting questions (expanded in each topic's brief)

- **R2 Encounter and boss design.**
  - Telegraph design and fairness.
  - Phase structure.
  - Enrage and soft timers.
  - Anti-camping and positional pressure.
  - Difficulty targets for skilled and average players.
  - How raid designers tune clear rates.
  - Rule patterns that read clearly in a turn-based log.
- **R3 Rewards and economy.**
  - Faucets and sinks.
  - Reward schedules and pity systems.
  - Weekly and event pacing.
  - Inflation control.
  - How a payout reads as fair for different effort levels.
  - Event currency design.
- **R4 Game writing.**
  - Battle text and barks.
  - Telling a story through logs and environmental text.
  - Voice consistency across many writers (and agents).
  - Naruto-flavoured register without copying.
  - Clue-carrying text.
- **R5 Quest and event structure.**
  - Quest archetypes and variety.
  - Pacing within an event.
  - Retention mechanics (dailies and weeklies) without fatigue.
  - Optional depth for veterans.
  - Onboarding new players.

---

## 7. Where things live

- **Research:** `docs/research/<topic>/REPORT.md`, `SOURCES.md` (link, author, date, tier, what it
  supports) and `APPENDIX.md`.
- **Principles:** the owning skill's `references/` file, each principle citing its finding and source.
- **Tools:** the owning skill's `scripts/`, with selftests. Shared helpers go in a common module the
  skills import, not in copies.
- **Evals:** the owning skill's `evals/`, with results recorded per run.
- **Lessons from real use:** a short `LESSONS.md` per skill, turned into reviewed changes at the next
  topic or overhaul pass.

---

## 8. Decisions for the director when R1 starts

1. Approve the R1 questions (§5.1), adding or cutting.
2. Which research agent runs step B: a deep-research session, or a Claude agent with web research.
3. How much the visual references may include: links only (default), or short committed GIFs of our
   own test renders imitating a technique.
4. The readability checker's pass thresholds: proposed from the research, then ruled.
