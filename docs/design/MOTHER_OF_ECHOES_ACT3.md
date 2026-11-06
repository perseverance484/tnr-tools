# The Mother of Echoes: Act III, analysed and redesigned

**Status:** design proposal for the director (2026-11-05). Design and simulation only. Live-game requests: 0. No live
records were changed. Nothing here is approved until the director rules on section 6.

**The brief (director, 2026-11-05):** "Sounds like it needs a solid looking at. Lets do a deep analysis of what it is now
and what an ideal act 3 should look like. We should be building on established mechanics in the first 2 acts and making
them more difficult, more expansive, more powerful. We want to make this line an evolution of Sayo, we want to mirror
that energy. The fight gets harder as she gets stronger but its still the same mechanics, just turned up in speed and
intensity. We want it to be difficult not monotonous."

**Standing intent this doc is held to:** a puzzle fight won by reading the floor and the moves; everything readable on
screen; perfect execution clears about 50–70% and near-perfect humans about 0–10% (whole fight); Act III eruptions are
lethal (6,500 flat pierce against 6,250 HP). Approved today and assumed throughout: Sayo stun immune; the Lancet ramp
clearable; the Silence's heal-back raised to be Act I's Clear target; Act I staggered.

**Sources**

| Source | Pin |
|---|---|
| Fight script and its Act III findings | `docs/design/MOTHER_OF_ECHOES_FIGHT_SCRIPT.md`, main @ `7695252c` (**[FS]**) |
| Spec, AI rules | `fable/mother-of-echoes-sim` @ `700a0d6b`, `harness/skyglass_wreck_sim/mother_of_echoes_spec.json` (**[spec]**) |
| Baseline params | the sim agent's working `params_pT18.json` (today's approvals: stun immunity, clearable ramp, Silence absorb 35, Act I stagger), copied as `results/act3/params_base_pT18.json` on the prototype branch |
| Prototype | `fable/mother-of-echoes-act3` @ `8e367043` (section 5) |
| Engine | theninjarpg @ `3314d122`, read only (**[eng]**); the harness runs it in process, socket-free |
| What the player sees | `docs/design/COMBAT_ANIMATION_ENGINE.md` (**[AE]**), `docs/design/MOTHER_OF_ECHOES_ART.md` (**[ART]**) |
| Text and quest flow | `docs/design/MOTHER_OF_ECHOES_JUTSU_TEXT.md` (**[TXT]**), `push/mother_of_echoes.gen.py` |

Evidence labels: **[spec]** a record or rule in the spec; **[eng]** read in engine source; **[sim]** an offline sim
result from this work; **[FS]** the fight script; **[I]** inference.

---

## 0. The short answers

- **What Act III is now.** Three loops of one verb each: leave a fan (100–60%), stand on one of three fixed stars
  (60–25%), outlast a 6-round "cannot fall" while the ceiling comes down (below 25%). Almost none of it is the Sayo the
  player has fought for two acts. Started fresh, a perfect player needs a median **29 rounds**; with Acts I–II's damage
  carried in, 47 [FS]. 43% of turns end with 20+ AP unspent, 71% of the damage a perfect player takes has no tell, and
  a player who stands on the north star and never moves clears **9 of 20** [sim].
- **Why the end stalls.** Not AP drain. The engine's shared cooldown: Shatterfall Gives Way and The Names Flood In are
  pierce with cooldown 2, so each locks every other pierce action of hers, every Glassfall pane included, for 3 rounds.
  The pane marker expires before the lock does. A second bug makes the Opening Pane rule unreachable (section 1.3).
- **The ideal Act III.** The same verbs, faster, larger, layered and lethal, in three phases. **Lucid** (100–60%):
  Refraction every turn with no rest turns, Facet's gaps, a follow-the-player bar, and her own Cradle fused with
  Stillness, which one Clear from exactly 4 hexes breaks. **Every Name, Remembered** (60–25%): a warned heal cut that
  spares the stars, then Act II's etchings come back, each covering one star, so the screen shows three safe stars and
  your memory says one of them is lying. **A Good Impression** (below 25%): every turn a third of the ceiling falls with
  an echo of Act I or Act II, the follow mark becomes a lethal line through you, her guard stays open and she walks to
  you. Open-guard windows: ×4, ×3, ×2.
- **Prototype result** (Act III alone, from full HP, 40 seeds for perfect / real / average, 20 for ignore and camp):
  perfect **39/40**, real **24/40**, average **1/40**, ignore **0/20**, camp **0/20**; median **17 rounds** (target
  15–20); the Saint idles in **0%** of her turns (was 11%); a real player's damage taken is **66–72% readable** (was
  48%). Still to tune: Phase I runs long (median 12 rounds) and Phase III short (median 3).
- **Decisions needed:** listed in section 6. The big ones: the cut list (The Quiet, Shatterfall, the Held Breath and
  Breathless Pull, The Long Hush all leave Act III), DR 40 → 25, how lethal the Phase I follow bar is, and the heal cut
  (10 rounds, sparing the stars, warned at 70%).

---

## 1. Act III as it is

### 1.1 Cast and loop

| Unit | HP | Notes [spec] |
|---|---|---|
| Sayo, Saint of Stillness | 60,600 (pools 12) | DR 40 plus AI Heavy Armor; damage rows 2.41; stun immune (approved today); enrage (The Glass Remembers) at round 80 |

Her 20 rules, in order:

| # | Rule | AP | Cooldown |
|---|---|---|---|
| 1 | The Glass Remembers, round > 80 | 100 | 0 |
| 2 | The Long Hush below 25%: `finalstand` for 6 rounds; marks the first Glassfall third | 40 | 99 |
| 3–7 | Glassfall (Heart Recast, Opening, First, Second, Last Pane), each on its marker: crush a third (6,500), mark the next | 100 | 0 |
| 8 | End turn below 25% | | |
| 9 | Shatterfall Gives Way, on its marker: a 19-hex fan from her feet, 6,500, 3-round pool | 100 | **2** |
| 10 | The Names Flood In, on its marker: everything but the three stars, 6,500 | 100 | **2** |
| 11 | Breathless Pull, on its marker: pull 1 and stun anyone off a star | 60 | **2** |
| 12 | Every Name in the Glass after the Pull: heavy everywhere but the stars | 40 | 3 |
| 13 | No One Is Mended below 60%: no healing anywhere for **20 rounds**, no warning | 20 | 99 |
| 14 | The Held Breath below 60%: control everywhere but the stars | 60 | 4 |
| 15 | Hush Where They Refused below 60%: a random star becomes a 3-round pool | 40 | 3 |
| 16 | The Quiet within 5: +8% damage taken and −8% healing for 6 rounds, stacking; Cleanse locked for a round | 60 | 2 |
| 17 | Shatterfall: mark the fan | 40 | 3 |
| 18 | Glass Lancet within 5: a hit and a 7% ramp stack | 60 | 1 |
| 19 | End turn while the fan is marked | | |
| 20 | Close in | | |

Played out, that is three loops:

- **100–60%:** The Quiet; Shatterfall mark and a Lancet; Gives Way; repeat. The one thing to read is a fan in front of
  her every third turn. Step out of it (1–3 hexes) and attack.
- **60–25%:** No One Is Mended once; then The Held Breath, Pull with Every Name, the Flood, a Hush on a star with The
  Quiet; repeat, with Shatterfall in the gaps. The one thing to read is "stand on one of three fixed stars."
- **Below 25%:** she cannot fall for 6 rounds while the ceiling comes down a third at a time.

### 1.2 The numbers

The fight script [FS §5] ran whole encounters, so the player arrives with whatever Acts I–II left. The baseline here
runs Act III alone, from full HP, 20 seeds per cell, at today's params, so it compares like for like with the prototype
in section 5. "Real" is the elite player model that misreads 15% of new tells; "camp" stands on one hex (the north star,
6,2) and never moves.

| Measure | [FS], carried HP, perfect | Fresh: perfect | real | average | ignore | camp |
|---|---|---|---|---|---|---|
| Act III cleared | 5 of 6 entered | **19/20** | **13/20** | 3/20 | 0/20 | **9/20** |
| Rounds, median of wins | 47 | **29** (27–30) | 30 | 61 | – | 33 |
| Saint idle turns | 18% | **11%** | 10% | 3% | 0% | 15% |
| AP per turn: move / attack / buff / Clear+Cleanse / unspent | 0.47 moves per turn; 67% of turns with AP left | 5 / 56 / 14 / 6 / **19** | 4 / 61 / 15 / 6 / 14 | 2 / 51 / 23 / 9 / 14 | | |
| Turns ending with ≥ 20 AP unspent | | **43%** | 38% | 34% | | |
| Damage taken: readable / filler / enrage | 20 / 70 / 10 | **24 / 71 / 4** | 48 / 52 / 0 | 32 / 68 / 0 | | |
| Damage taken per fight | | 5,436 | 6,222 | 10,177 | | |

All eleven camp deaths were Shatterfall when she walked up to them. Nothing else in the act reaches a player who never
moves off the north star.

### 1.3 Two defects under the stall [eng, sim]

The fight script recorded that the finale stalls (its D2: after The Long Hush the Saint casts at most one pane, then
idles until she dies) and guessed AP drain. The causes are these:

1. **The shared cooldown.** `pierce`, `stun`, `drain`, `clearprevent`, `cleanseprevent` and a dozen more are
   shared-cooldown tags (`drizzle/constants.ts:261-282`). Using an action with **cooldown > 0** that carries one locks
   every other action of the caster sharing that tag for 3 rounds (`applyActionCooldowns`,
   `libs/combat/actions.ts:1461-1490`). Shatterfall Gives Way and The Names Flood In are pierce with cooldown 2, so each
   locks every Glassfall pane (also pierce) for 3 rounds, and the 1-round pane marker expires first. A one-off probe
   shows it (trace on the prototype branch, `results/act3/trace_base_glassfall_probe_seed3.txt`): in seed 3 all four
   Glassfall records are unavailable on the turn after The Long Hush and available the turn after that, once the marker
   has gone. The same lock is behind half of Act I's marks never
   erupting; the sim agent's uncommitted `gcdSafeBlasts` already sets those blasts to cooldown 0, and Act III needs the
   same treatment.
2. **A marker that can never pass.** The Long Hush's "first pass" marker is `decreasecooldown`. `decrease*` tags are
   stored with negative power once cast, and `has_effect` sums power against a threshold of at least 1
   (`libs/combat/ai_v2.ts:428-438`), so the Opening Pane rule never fires.

So the 14 dead rounds at the end of the fight script's seed 1 [FS §5.4] are not a design choice. The finale as written
never runs.

### 1.4 Why it is monotonous

1. **One verb per phase, repeated.** "Leave the fan" every third turn, then "stand on a star" every fourth. Neither
   changes as she weakens. The first cycle is the whole lesson and every later cycle repeats it.
2. **Almost none of it is Sayo.** Acts I–II teach lines that break next turn, the mirror, the follow-the-player ring,
   Cradle, Stillness, Etching and Recast, and the open guard. Act III uses none of them. The Quiet, Shatterfall and the
   Held Breath are new verbs, so the climax teaches instead of testing.
3. **Nothing rewards a read.** With no open-guard window, a turn where you read correctly hits no harder than one where
   you didn't. When the kit is on cooldown there is nothing worth spending AP on: 43% of turns end with 20+ AP unspent.
4. **The danger is not on the floor.** 71% of a perfect player's damage taken is the Glass Lancet and The Quiet, which
   have no tell. The readable set pieces barely touch someone who reads.
5. **The one heal-timing beat is invisible.** No One Is Mended lands at 60%, for 20 rounds, with no warning.
6. **No answer verbs.** Until today Clear had no target (the Lancet's `clearprevent` protected everything); Cleanse
   answers only The Quiet.
7. **The climax is a wait.** `finalstand` makes her unkillable for 6 rounds by design, and the broken chain (1.3) turns
   that into 14 rounds of hitting a statue.
8. **Standing still wins** 45% of the time.

---

## 2. The vocabulary Acts I and II teach

All of this is on screen in Acts I–II, with art, text and a rule the player has learned before Act III.

| Verb | Act | The tell | The read | The answer |
|---|---|---|---|---|
| **Refraction** (three lines, then the far three) | I | Heavy Heartglass tiles on 27 hexes | A mark is a promise kept on her next turn | Step off; spend the rest of the turn |
| **Facet** (both sets, mirrored) | I, below 60% | Heavy on both line sets | "The gaps are all there is" | Stand in a gap (rows 0, 3, 6, 9) |
| **Lucid Refraction** (break and redraw at once) | I, Silence dead | The lines break and new ones are already up | No rest turns | Step every turn |
| **The Silence Turns** (follow-the-player mark) | I | A heavy ring under you | It follows you; camping is punished | Leave it before you act again |
| **Stillness → Nothing Moves** | I | A violet ring of radius 3 round the Silence | Distance is safety | Leave the ring, or Clear the caster (its marker is a positive effect) |
| **The Hush** | I–II | Dark linger pools | Don't end a turn in one | Path round them |
| **Cradle and the Feeler** | I | The Cradle loop braids round Sayo | She is untouchable while something holds her | Remove the holder |
| **The Silence's heal-back** (absorb 35, approved today) | I | Aura on the Silence | A buff you can take away | **Clear** it |
| **The Lancet ramp** (clearable, approved today) | all | Her glow thickens per stack ([FS] R3) | Her hand steadies over time | **Clear** resets it |
| **Etching → Recast** | II | A gold lattice for one round; the log names the region | Remember the region and the order | Stand where the glass never glowed |
| **The ×3 open guard** | II | The guard ring on her after each Recast | The read pays out as damage | Burst into the window |
| **The Worn** | II | Rises, sweeps, mends | Target priority | Kill Hana |
| **The three who refused** (the stars) | III today | Cyan safe tiles | Three places the flood never takes | Stand there |

---

## 3. The ideal Act III

### 3.1 Principles

1. **Same verbs, turned up.** Every Act III move is an Act I or Act II move made faster (no rest turns), larger (more of
   the floor), layered (two reads at once) or stronger (lethal). No new verbs. The stars stay, as the anchor of Phase II.
2. **Every turn of hers puts a new read on the floor.** No idle turns, no stalls, no `finalstand`. Every mark erupts on
   her next turn, because every eruption has cooldown 0 and the shared cooldown can never delay it (1.3).
3. **Every read pays.** Each phase has an open-guard window that only a correct read reaches: one turn long, so shorter
   than Act II's three, and bigger.
4. **Her buffs have an answer.** Clear has a target in every phase, and using it is a real decision (60 AP, range 4,
   cooldown 10).
5. **The climax is short and loud.** Below 25% everything comes back at once for a few rounds, her guard stays open, and
   she walks to you.
6. **Every loss is a readable mistake.** Every lethal hit has a tell on screen the turn before, except the Phase II
   etching, which is a memory test the fight has already taught (exactly as in Act II).

### 3.2 Phase structure

| Phase | HP | Story beat | Acts I–II verbs, evolved | Window | Rounds: target / prototype median |
|---|---|---|---|---|---|
| **I. Lucid** | 100–60% | Sayo's glass, without rest | Refraction every turn; Facet; Hold Still; Stillness and Cradle fused on her; the Lancet ramp | Facet Breaks: guard open ×4, one turn in four | 6–8 / **12** |
| **II. Every Name, Remembered** | 60–25% | The Silence folds back in: memory and the names | Warned heal cut; Act II's etchings (each holds one star), then Every Name, then a flood that takes the etching too; the Hush | The Names Flood In: guard open ×3 | 5 / **4** |
| **III. A Good Impression** | below 25% | "Hold still. You will make for a good impression." | A rolling clock: a third of the ceiling falls with an echo of Act I or II each turn; the follow mark becomes a lethal line through you; she walks to you | every turn: guard open ×2 | 3–4 / **3** |

Phases change only on a turn with nothing pending (after Facet Breaks, after a Hush on a star), so a phase change never
strands a mark. The cost is up to three turns of slack around each threshold.

### 3.3 Phase I: Lucid (100–60%)

*The lines she drew in Act I, with no rest turns, while the Silence she carries holds her.*

Each of her turns is a 60-AP chain step followed by a 40-AP extra, the first extra in this order that applies: The Silence
Holds Her (below 95%, cooldown 6) → Nothing Moves (if the ring is up) → Remainder Lancet (within 5, cooldown 2) → Hold
Still (within 5). The chain is a 4-turn cycle:

| Turn | Her chain step (60 AP) | Your screen next turn | What you do |
|---|---|---|---|
| T1 | **Refraction**: the near lines A (27 hexes) | Heavy lines A (Remainder material) | Step off A |
| T2 | **Lucid Refraction**: A breaks (6,500, 3-round pool), and the far lines B are drawn in the same action | Lines B; A's broken glass | Step off B |
| T3 | **Facet**: B breaks, and both sets are drawn (A∪B, 54 hexes) | Both sets: only the gaps are safe (rows 0, 3, 6, 9 and the line ends) | Get into a gap |
| T4 | **Facet Breaks**: A∪B break. **Her guard opens ×4 for one turn.** | The guard ring on her | **Burst**: best skills, the Chakra Pill |
| (T1) | Below 60%: **No One Is Mended** instead, and Phase II begins | | |

**What is new, and what it evolves from:**

- **Lucid every turn.** In Act I, Lucid Refraction is the reward for killing the Silence first. Here it is her normal
  cadence: something breaks and something new is drawn every turn. That is the "speed".
- **Hold Still** (40 AP, origin TARGET, range 5): the hex under you and the hexes north and south of it go still and
  drain 50% of your max HP each time you act there. This is the Silence Turns made faster and harsher, with one
  deliberate change: a 3-hex bar, not a ring. A ground drain is copied onto whoever ends an action on it, and the copy
  lasts the round (`libs/combat/process.ts:395-412`). Walking out of a radius-1 ring therefore takes two actions and
  two drains unless Replacement (cooldown 2) is up, and the lines already spend Replacement. In the first prototype loops
  the ring killed perfect players who did exactly what the tell said (traced: loop L3, seed 5, two drains a turn until
  dead). Any side step clears a bar. *(This same
  property of Act I's Silence Turns is flagged for the Acts I–II owner in 4.6.)*
- **The Silence Holds Her** (40 AP, cooldown 6, below 95%): her own Cradle, with the Silence inside her. For 3 rounds she
  takes 75% less damage and absorbs 30% of what lands, and the Cradle loop plays on her. It rides the absorb, which has
  positive power and so renders, unlike Act I's `decreasedamagetaken`. The floor within 3 of her goes still, which is
  Act I's Stillness, now centred on her. Next turn **Nothing Moves** hits anyone still within 3 for 2,500 pierce and a
  stun: your next turn is lost and you stand in whatever is marked. *The answer has changed.* There is no feeler to kill.
  The hold is hers, and every part of it is a positive, non-innate effect, so **one Clear strips the Cradle, the absorb,
  the Stillness marker (Nothing Moves never comes) and every ramp stack at once** (`tags.ts:1179-1260`). Clear has range
  4 and Stillness has radius 3, so the answer is to stand exactly 4 hexes from her. That is the act's best spatial read.
- **Remainder Lancet** (40 AP, cooldown 2, range 5): the Act III Lancet. It costs 40 AP instead of 60 so it fits beside
  a chain step, carries the same 7% ramp per stack, and has no `clearprevent`, so a Clear resets it.
- **The Names Stir** (20 AP, once, below 70%): the warning for Phase II (3.5).

### 3.4 Phase II: Every Name, Remembered (60–25%)

*The Silence folds back into her. The names in the glass rise, the three who refused stay dry, and the glass remembers
what she etched in Act II.*

Entry, on the first clean turn below 60%: **No One Is Mended** (100 AP). The hush floor covers the hall **except the
three stars** for 10 rounds. Then a 4-turn cycle (one combo, every turn exactly 100 AP), run three times with a
different etching each time:

| Turn | Her action (100 AP) | Your screen next turn | What you do |
|---|---|---|---|
| C1 | **Etching: Rime** (the north band, which holds the north star) + **The Hush Rises** (6 pools, 8% drain, no healing) | The lattice, for this one round; the log names it ("traces the north of the hall") | Remember it. Fight. |
| C2 | **Every Name in the Glass**: heavy everywhere but the three stars; the stars light up | Heavy floor, three cyan stars. The etching has faded. | **Stand on a star the etching did not cover.** Stars are 3–4 hexes apart: Replacement, or 30–40 AP of walking. |
| C3 | **The Names Flood In: Rime**: everything but the stars floods, **and so does the etched region**, its star included (6,500). **Her guard opens ×3 for one turn.** | The guard ring | Burst from the star. A star near her is worth more. |
| C4 | **Hush Where They Refused** (a random star becomes a 3-round pool) + **The Hush Rises** | Linger on one star; new pools | Reposition. On a star, wounds still close. |

Cycle 2 etches **Ember** (the south band, south star) and cycle 3 **Heart** (the centre, middle star). Each Act II
etching holds exactly one star: Rime the north (6,2), Heart the middle (5,5), Ember the south (6,8). Seam holds none. So
the memory test is Act II's, sharpened to one question: *which star did she etch?*

Why this is "the same mechanic, turned up": in Act II the read was "remember the region and stand outside it." In Act
III, **the screen tells you three stars are safe and your memory tells you one of them is lying.** The visible safe tile
and the remembered danger disagree, and the player has to trust memory over the screen, which is exactly the Saint's
theme: the glass remembers.

### 3.5 The heal cut, redesigned: warned, and a choice

| | Today | Proposed |
|---|---|---|
| Warning | none | **The Names Stir** at 70%: a one-round preview of the hush floor over everything but the stars, and the line *"The names press up against the glass from below. 'Soon nothing here will mend. Except where the three refused.'"* |
| When | the turn she drops below 60% | the first clean turn below 60%, so the player decides when by how hard they push from 70% |
| How long | 20 rounds | 10 rounds (about all of Phase II) |
| Where | the whole floor | everywhere **except the three stars**: where the three refused, wounds still close |

The choice: between 70% and 60% the player can top up while healing still works everywhere, or push through and carry
what they have. Lifesteal is the real kit's only HP sustain (Eclipse Drain, the Chakra Pill, gear); the Energy Potion
restores chakra and stamina only. In Phase II, healing is positional: stand on a star to mend. But the stars are also
where the flood is survived, one is etched and one is hushed, so the star you heal on and the star you survive on are
not always the same star.

### 3.6 Phase III: A Good Impression (below 25%)

*"Hold still. You will make for a good impression."* Everything she has drawn comes back at once.

Entry, on the first clean turn below 25% (after a Hush on a star): **A Good Impression** (60 AP) marks the first pane.
Then every turn:

| Her turn | Step (60 AP) | Extra (40 AP) | Your screen | What you do |
|---|---|---|---|---|
| each | **Glassfall: an echo pane** falls (6,500): a third of the hall **plus one echo**. Pane 1 is third A + **Act I's near lines**, pane 2 is third B + **Act II's Heart**, pane 3 is third C + **Act II's Seam**, then round again. The next pane is marked. **Her guard is open ×2.** | **Every Line Through You** if you are within 5: a 9-hex column through you, **lethal** (100% drain) the next time you act there. Otherwise **she walks to you.** | The next pane (about half the hall), the column through you, the guard ring | One side step that clears both, then burst |

The panes cover 46–53% of the floor and the column adds up to 9 hexes. Any side step clears a column (four of your six
neighbours). The echoes are drawn in their own act's heavy material: [ART] already has `tile_moe_heavy_i_a3` and
`tile_moe_heavy_ii_a3`, so the Act I lines come back in Heartglass and the etchings in Act II's cracked glass. The whole
fight returns, in the order you learned it and in the glass you learned it in.

**Why this is a climax, not a wait:** there is no `finalstand`; every turn has a lethal read *and* a ×2 window; she closes
the distance herself, so the player never stalls trying to reach her; it lasts about three turns.

### 3.7 Damage budget and length

| | Target | Prototype (perfect, fresh, 40 seeds) |
|---|---|---|
| Saint HP | 60,600 (pools 12, unchanged); **DR 40 → 25** | as target |
| Phase I | 40% in 6–8 turns: about 1,800 per normal turn, ×4 on one turn in four | median 12 turns (8–20): **too long** |
| Phase II | 35% in one cycle (5 turns): the ×3 flood does most of it | median 4 (4–8) |
| Phase III | 25% in 3–4 turns at ×2 every turn | median 3 (2–7) |
| Whole act | **15–20 rounds** | **median 17** (interquartile 15–22) |
| Saint idle turns | ~0 | **0%** |
| AP | mostly on reads: moves, Clear, bursts | unspent 14–16 per turn (was 19); turns with ≥ 20 unspent 31–35% (was 43%) |

### 3.8 How you lose

| Mistake | Phase | What happens | Readable? |
|---|---|---|---|
| Standing in a line | I | 6,500: death | Heavy tiles the turn before |
| Standing on the Hold Still bar | I | 50% per action: two actions kill | Heavy bar under you, "Hold still." |
| Within 3 of her when Nothing Moves lands | I | 2,500 and a lost turn, standing in the next lines | Violet ring round her |
| Not clearing the Cradle | I | ×0.25 damage for 3 turns; the ramp keeps climbing | Cradle loop on her, ramp glow |
| Pushing past 60% low | II | 10 rounds with no healing off the stars | The Names Stir |
| The etched star | II | 6,500 | Memory: the lattice and the log line two turns before |
| Off a star at the flood | II | 6,500 | Heavy everywhere, safe stars |
| In the pane or its echo | III | 6,500 | Heavy tiles, in the echo's own glass |
| On the column | III | death | Heavy column through you |
| Too slow | all | The Glass Remembers at round 36 | None: there is still no countdown art (4.6) |

The prototype's deaths match this table: real players die to the flood (the etched star or off a star), to Glassfall and
to the follow marks; perfect play died once in 40 runs, trapped by a column with no single-action escape.

---

## 4. Implementation plan (record level)

### 4.1 Records

Ids are spec placeholders, mapped to live ids by the generator as today (law 17). All of these belong to the Saint
alone, so nothing here changes a record another boss holds.

| Id (prototype) | Name | AP | CD | Target / method | Effects |
|---|---|---|---|---|---|
| `moe-saint-refraction` | Refraction | 60 | 4 | GROUND, COORDINATES: lines A | carrier `tg_heavy` (1 round); marker `fleeprevent` (mA) |
| `moe-saint-lucid-refraction` | Lucid Refraction | 60 | 0 | GROUND: lines A | pierce 6,500 static; act3 pool (`decreaseheal` 50, `increasedamagetaken` 20, 3 rounds); carrier on lines B; marker `summonprevent` (mB) |
| `moe-saint-facet` | Facet | 60 | 0 | GROUND: lines B | pierce 6,500; pool; carrier on A∪B; marker `elementalseal` (mF) |
| `moe-saint-facet-breaks` | Facet Breaks | 60 | 0 | GROUND: A∪B | pierce 6,500; pool; `weakness` ×4 SELF 1 round (`moe_guard_open`); marker `disarm` (clean) |
| `moe-saint-hold-still` | Hold Still | 40 | 0 | GROUND, COORDINATES origin TARGET, range 5: (0,0), (0,±1) | carrier `tg_heavy`; `drain` 50% (option: 100%) for 1 round |
| `moe-saint-the-silence-holds-her` | The Silence Holds Her | 40 | 6 | GROUND, AOE_SPIRAL_SHOOT 3 | carrier `tg_control`; marker `robprevent` (positive: Clear cancels Nothing Moves); `decreasedamagetaken` 75 SELF 3 rounds; `absorb` 30 SELF 3 rounds (`moe_cradle` loop) |
| `moe-saint-nothing-moves` | Nothing Moves | 40 | 0 | CHARACTER, AOE_SPIRAL_SHOOT 3 | pierce 2,500 static; stun (100 AP) |
| `moe-saint-remainder-lancet` | Remainder Lancet | 40 | 2 | OTHER_USER, SINGLE, range 5 | the Lancet hit; `increasedamagegiven` 7% SELF 9 rounds; **no** `clearprevent` |
| `moe-saint-the-names-stir` | The Names Stir | 20 | 99 | GROUND: every hex but the stars | carrier `moe_hush_floor` (1 round): the warning |
| `moe-saint-no-one-is-mended` | No One Is Mended | 100 | 99 | GROUND: every hex but the stars | `decreaseheal` 100 + `healprevent` 100 for 10 rounds (`moe_hush_floor`); phase marker `increasecooldown` +1 (99 rounds) |
| `moe-saint-etching-{rime,ember,heart}` | Etching: Rime / Ember / Heart | 40 | 0 | GROUND: Act II regions A, B, D | carrier `tg_etch` (1 round). **Recommended: reuse Act II's `moe-etching-a/-b/-d` as they are** (same pattern, AP, cooldown and art) |
| `moe-saint-hush-rises` | The Hush Rises | 60 | 0 | GROUND, RANDOM 6 non-star hexes | `healprevent` + `drain` 8% for 6 rounds (`tg_linger`) |
| `moe-saint-every-name` | Every Name in the Glass | 100 | 0 | GROUND: every hex but the stars | carrier `tg_heavy`; carrier `tg_safe` on the stars |
| `moe-saint-flood-{rime,ember,heart}` | The Names Flood In: X | 100 | 0 | GROUND: every hex but the stars ∪ region X | pierce 6,500; `weakness` ×3 SELF 1 round |
| `moe-saint-hush-where-they-refused` | Hush Where They Refused | 40 | 0 | GROUND, RANDOM 1 star | `healprevent` + `drain` 3% for 3 rounds; marker `fleeprevent` (cycle end) |
| `moe-saint-a-good-impression` | A Good Impression | 60 | 99 | GROUND: pane 1 | carrier `tg_heavy`; marker `disarm` (gA); phase marker +1 |
| `moe-saint-echo-pane-{a,b,c}` | Glassfall: First / Second / Last Echo | 60 | 0 | GROUND: third k ∪ echo k | pierce 6,500; pool; `weakness` ×2 SELF 1 round; carrier on the next pane; next marker (`summonprevent` / `fleeprevent` / `disarm`) |
| `moe-saint-every-line` | Every Line Through You | 40 | 0 | GROUND, COORDINATES origin TARGET, range 5: column (0, −4…4) | carrier `tg_heavy`; `drain` 100% for 1 round |
| `moe-the-glass-remembers` | (shared enrage, unchanged) | 100 | 0 | | rule moves to round > 36 |

That is 24 new records (21 if the Act II etchings are reused). **Retired from the Saint (15):** The Quiet, Shatterfall,
Shatterfall Gives Way, Every Name in the Glass, The Names Flood In, No One Is Mended, The Held Breath, Breathless Pull,
Hush Where They Refused, The Long Hush, Glassfall a / b / c / Opening / Heart Recast. Because only the Saint holds them,
eight can be **edited in place** into their successors, keeping their live ids and art wiring (law 18: unequip, edit,
re-equip): Every Name → `every-name`; The Names Flood In → `flood-rime`; No One Is Mended → its successor; Hush Where They
Refused → its successor; The Long Hush → `a-good-impression`; Glassfall a / b / c → the three echo panes. The Glass
Lancet keeps its Acts I–II role; the Saint stops using it.

Saint record: pools 12 (60,600), **DR 25** (was 40), damage rows 2.41, `stunprevent` (approved), AI Heavy Armor.

### 4.2 Rules (exactly 20; the last is unconditional)

| # | Rule | Conditions |
|---|---|---|
| 1 | The Glass Remembers | round > 36 |
| 2 | Echo pane A | has `disarm`; phase ≥ 2 |
| 3 | Echo pane B | has `summonprevent`; phase ≥ 2 |
| 4 | Echo pane C | has `fleeprevent`; phase ≥ 2 |
| 5 | Every Line Through You → the player | phase ≥ 2; player within 6 (path length; range 5, law 40) |
| 6 | Move toward the player | phase ≥ 2 |
| 7 | A Good Impression | below 25%; has `fleeprevent` (cycle end); phase ≥ 1 |
| 8 | Combo: the Phase II cycle ×3 (18 ids: etch, rises, every name, flood, star hush, rises; Rime, Ember, Heart) | phase ≥ 1 |
| 9 | Facet Breaks | has `elementalseal` |
| 10 | Facet | has `summonprevent` |
| 11 | Lucid Refraction | has `fleeprevent` |
| 12 | No One Is Mended | below 60%; has `disarm` (clean turn) |
| 13 | End turn | phase ≥ 1 |
| 14 | Nothing Moves | has `robprevent` |
| 15 | The Names Stir | below 70% |
| 16 | Refraction | none (cooldown 4) |
| 17 | The Silence Holds Her | below 95% |
| 18 | Remainder Lancet → closest | within 5 |
| 19 | Hold Still → the player | player within 6 |
| 20 | Move toward the closest opponent | none |

Why the order works: chain steps cost 60 AP and extras 40, so no mark can erupt in the turn it is drawn (60 + 60 > 100).
Phase II and III rules sit above Phase I's and are gated on the phase counter, and rule 13 keeps Phase I's extras out
of Phase II. Phase entries need a "clean" marker, so they never strand a pending mark. The prototype spec validates
(JutsuValidator for every jutsu, AiRule for every rule, insertAiSchema, 20 rules, unconditional last rule).

### 4.3 Markers

| Marker | Type | Sign | Why this type |
|---|---|---|---|
| Lines A drawn (mA), cycle end, pane C next | `fleeprevent` | negative | No captured player jutsu applies it; reuse across phases is safe because Phase III rules also need phase ≥ 2 and the Phase III entry needs phase ≥ 1 |
| Lines B drawn (mB), pane B next | `summonprevent` | negative | 1 of 1,237 captured jutsu |
| Facet drawn (mF) | `elementalseal` | negative | 1 of 1,237; her jutsu are not elemental |
| Clean turn, pane A next | `disarm` | negative | none captured; her jutsu carry `jutsuWeapon` NONE, so nothing is hidden |
| Stillness pending | `robprevent` | **positive** | So a Clear on her cancels Nothing Moves, as in Act I |
| Phase counter | `increasecooldown` (power 1, static, 99 rounds) | negative | Sums: 1 = Phase II, 2 = Phase III |

Rules the first prototype loops taught:
- **Never use a `decrease*` type as a marker.** It is stored with negative power once cast, so `has_effect` never
  passes (the first cycle-end marker, `decreasedamagegiven`, never fired; the same bug as The Long Hush).
- **Never use a type players put on bosses.** `increasedamagetaken` is on 223 of 1,237 captured jutsu (Captain's Decree,
  Paper Bombs and others); used as a pane marker it fired 11 panes unmarked in 20 runs. `decreasedamagegiven` is on 114
  (count from `harvests/inbox/tnr_results_1792732003454.json`).
- **Lethal chain markers are negative, so a Clear never cancels a set piece.** Only Stillness, which Act I already
  taught is cancellable, is positive.

### 4.4 Engine facts this relies on

| Fact | Where |
|---|---|
| Shared cooldown: any action with cooldown > 0 carrying `pierce` / `drain` / `stun` / … locks the caster's other actions with that tag for 3 rounds. Every eruption and drain here has cooldown 0. | `drizzle/constants.ts:261-282`; `libs/combat/actions.ts:1461-1490` |
| `has_effect` sums power against a threshold ≥ 1; it does not check rounds; `decrease*` powers are negative | `libs/combat/ai_v2.ts:428-438` |
| Clear removes positive, non-innate effects on the target and positive ground effects on its hex; any live `clearprevent` blocks the whole Clear. Boss record effects are innate (`fromType` bloodline) and survive. | `libs/combat/tags.ts:1179-1260` |
| COORDINATES with origin TARGET offsets the pattern from the clicked hex; the click must be within the jutsu's range, and jutsu range is capped at 5 | `libs/combat/targeting.ts`; `libs/hexgrid.ts:108-138`; `validators/combat.ts:1978` |
| A ground effect is copied onto whoever ends an action on its hex, for 1 round; a drain copy hits on every action that round | `libs/combat/process.ts:395-412`; `tags.ts:2152-2156` |
| `use_combo_action` replays a sequence from the AI's own used actions; an end turn breaks it, so every step is exactly 100 AP | [spec] proof P1 |
| `weakness` `dmgModifier` up to 50 | `validators/combat.ts:1100-1116` |
| No "not has effect" or "health above" condition: phase logic is done with rule order and counters | `validators/ai.ts` |
| A ground mark shows for the rest of its cast round and all of the next | [AE §0.6] |
| Everything the AI does between two clicks lands in one snapshot | [AE §2.3] |

### 4.5 Art

Nothing new is strictly required; everything below exists in the art3 set [ART].

| Piece | Asset |
|---|---|
| Phase I line marks, Hold Still, Every Line, Every Name | `tg_heavy`, Act III material (`tile_moe_heavy_iii_a3`, `anim_moe_heavy_glint_iii_a3`, `anim_moe_heavy_appear_iii_a3`) |
| Line breaks (Lucid, Facet, Facet Breaks) | the Remainder Shatterfall strip (`anim_moe_shatterfall_w*_a3`) as one band per line: wiring only. (Act I's `anim_moe_refraction_a3` is Heartglass, the wrong material here.) |
| Guard open (×4, ×3, ×2) | `anim_moe_guard_open_v2` |
| The Silence Holds Her | `anim_moe_cradle_v2` loop on the absorb; `tile_moe_control_dark_a3` ring; Nothing Moves `anim_moe_still_dark_v2` |
| Remainder Lancet and its ramp | `anim_moe_lancet_v2`; the Saint aura strip (`anim_moe_aura_*_a3`, held in `FX3_UNWIRED`) on the ramp's `increasedamagegiven`, which thickens per stack ([FS] R3) |
| The Names Stir, No One Is Mended | `moe_hush_floor` (`tile_moe_linger_dark_a3`); the stars stay clean. Optional new: a faint variant for the preview |
| Etchings | `tg_etch` (Act II's lattice, unchanged: the glass remembers Act II as it was) |
| The Names Flood In | `anim_moe_flood_mask_v1` and its 4-band wave |
| Hush Rises, Hush on a star | `tile_moe_linger_dark_a3` |
| A Good Impression, echo panes | `anim_moe_glassfall_w0..2_a3`; echo marks in their own act's heavy tile (`tile_moe_heavy_i_a3` for the Act I lines, `_ii_a3` for the Act II regions), one carrier per echo |
| Optional new | a column-drop appear for Every Line Through You; an Act III (black and teal) etch lattice if the director prefers the corrupted look over Act II's |

Text: 24 records need [TXT] entries in the approved voice. The prototype's battle lines are a starting draft
("Hold still. I want to see you in the light."; "The Silence folds around her. The floor around her goes still.";
"Every name in the glass floods the hall, and the glass remembers the rime."). The killing blow is never animated
[AE §0.11], so `w_clear` should open on the last pane falling ([FS] R12).

### 4.6 Risks

1. **No rule headroom.** Exactly 20 rules. Any addition needs a merge (for example The Names Stir folded into a chain
   step).
2. **Combo fragility.** Each Phase II step must be exactly 100 AP and always castable; all are BATTLEFIELD GROUND casts,
   so they always are. An interrupted cycle restarts at its etching, which is benign.
3. **Marker pollution.** `summonprevent` and `elementalseal` each appear on one captured player jutsu. A player who puts
   one on her could trigger a chain step early (an unmarked hit). Re-check against the live catalog before build.
4. **TARGET range 5.** Hold Still and Every Line only fire within 5. Kiting at 6+ avoids them but gives up damage, and in
   Phase III she walks to you.
5. **Lethal follow marks.** The Phase III column (and the Phase I bar, if the director picks lethal) kill on a misread.
   The bar or column is drawn under the player with a "Hold still." line; it is the act's most frequent lethal check.
6. **Solvability.** 10 of 738 perfect-player turns (40 runs) started with no free hex within 5 clear of every mark
   (pets on stars or side steps count as blocked). One perfect death in 40 came from this.
7. **Turn order.** The sim seats the player before her each round, which matches the Act I live log. Verify on the
   practice quest.
8. **The enrage has no countdown art**, as today.
9. **For the Acts I–II owner:** Act I's Silence Turns ring has the same two-drain trap as the first Hold Still (3.3);
   the skilled sim policy drinks the Energy Potion below 50% HP, but the potion restores chakra and stamina only.
10. **Sim limits.** The sim player cannot plan: it does not save Replacement for the bar, hold damage at 61% to top up,
    or pick the star nearest her. Perfect results are a floor on what a planner can do; real results include the 15%
    misread model and no other human error.

---

## 5. Prototype

**Branch:** `fable/mother-of-echoes-act3` @ `8e367043`, off `fable/mother-of-echoes-sim` @ `700a0d6b`. For baseline parity it
includes a snapshot of the sim agent's *uncommitted* Acts I–II flags (`rampClearable`, `act1Stagger`, `sayoStunImmune`,
`gcdSafeBlasts`, `markArtRounds`), applied verbatim from its working tree so the hunks merge cleanly. The new Act III is
behind `act3v2.on` (default off), so nothing changes for Acts I–II or for anyone running the sim agent's params.

**Added to the harness:** the Act III v2 records, rules, bookkeeping and policy (`engine/moe_lib.ts`: `J3`, `MK3`,
`A3_DEFAULTS`, `saintRulesV2`); per-act AP spent per player turn by category, boss idle %, damage split (readable /
filler / enrage), phase start rounds (`engine/moe.ts`); `--start-hp` for Act III-only runs; the sim player remembers the
etched star (from the next combo step, as for Act II) and tops up with lifesteal after The Names Stir. Results, params
and the validated spec are under `harness/skyglass_wreck_sim/results/act3/`.

**Loops** (Act III alone, from full HP, 20 seeds unless stated):

| Loop | Change | Perfect | Real | Median rounds | Notes |
|---|---|---|---|---|---|
| base | today's Act III (pT18) | 19/20 | 13/20 | 29 | camp 9/20, idle 11% |
| L1–L3 | first build, pools 12/10, DR 40/30 | 16/20 at L3 | – | 23 | found: the follow ring's two-drain trap; `decrease*` marker; player debuffs firing panes |
| L4 | DR 25, markers fixed, Hold Still bar 25% | 14/20 | 14/20 | 18.5 | Phase III: she stood still and the player could not reach her (2 enrages); cross trapped 4 |
| **L5** | she walks in Phase III; column not cross; Facet ×4; Cradle 75%; Hold Still 50% | **19/20** | **12/20** | **17** | average 0/20, ignore 0/20, camp 0/20 |
| L5, seeds 101–120 | confirmation | **20/20** | **12/20** | 17.5 | average 1/20 |
| L5, from 50% HP | carry-over check | 20/20 | 10/20 | 18 | lifesteal refills a perfect player |
| L6 | L5 with a lethal Hold Still bar | 17/20 | 10/20 | 18 | perfect loses 2 to bars with no clean step |

**L5, pooled (40 seeds for perfect, real and average; 20 for ignore and camp), against the baseline:**

| Measure | Baseline perfect | L5 perfect | Baseline real | L5 real | L5 average |
|---|---|---|---|---|---|
| Cleared | 19/20 | **39/40** | 13/20 | **24/40** | 1/40 |
| Rounds, median of wins | 29 | **17** | 30 | **17** | 32 (1 win) |
| Phase lengths I / II / III (median) | – | 12 / 4 / 3 | – | 9 / 4 / 3 | – |
| Saint idle turns | 11% | **0%** | 10% | **0%** | 0% |
| AP per turn: move / attack / buff / Clear+Cleanse / unspent | 5 / 56 / 14 / 6 / 19 | 8 / 52 / 21 / 4 / **15** | 4 / 61 / 15 / 6 / 14 | 7 / 50 / 24 / 4 / 14 | 6 / 43 / 33 / 5 / 14 |
| Turns ending with ≥ 20 AP unspent | 43% | **33%** | 38% | 32% | 27% |
| Damage taken per fight | 5,436 | **3,008** | 6,222 | 5,918 | 8,631 |
| Damage taken: readable / filler | 24 / 71 | 31 / 69 | 48 / 52 | **69 / 31** | 74 / 25 |
| Deaths | enrage 1 | column 1 | Every Name 5, Shatterfall 2 | **Every Name 10, Glassfall 3, follow marks 2, lines 1** | follow marks 13, Every Name 9, lines 7, Lancet 6, Nothing Moves 3, enrage 1 |
| Ignore / camp | 0/20 / **9/20** | 0/20 / **0/20** | | | |

**Reading the result.**
- **The structure works.** Every Saint turn does something, every mark erupts on time (no unmarked eruption for perfect or real players after L4; 4 in 40 average runs, not yet traced),
  the windows carry the damage, and the act lands in the target 15–20 rounds. Camping no longer wins. Real players now
  die to the act's own reads: the etched star, the flood, the follow marks.
- **Perfect play almost always clears Act III from full or half HP** (39/40, 20/20 from 50%). A perfect player takes
  about 3,000 damage across the act, nearly all Lancet chip, and refills it through lifesteal. Against the 50–70% target
  for the whole fight, that leaves the perfect-play failures to Acts I–II. If the director wants Act III to fail some
  perfect players too, the levers are the lethal Hold Still bar (L6: 17/20), less lifesteal value under the heal cut, or
  DR.
- **Real players clear 60% of fresh Act IIIs** (baseline 65%). The deaths now come from reads, not chip, but Act III
  alone does not yet separate real from perfect as sharply as Act II. Whole-fight real stays near 10% only if Acts I–II
  keep cutting real players at today's rates.
- **AP use improved, but less than hoped.** Unspent AP fell from 19 to 15 per turn. The rest is the sim kit: 13 jutsu,
  mostly cooldown 7. Moves rose from 5 to 8 AP per turn; Clear is used about once per fight.
- **Still to tune:** Phase I runs long (median 12 turns against a target of 6–8) because Phase II can start only on the
  clean turn of a 4-turn cycle; Phase III is often 2–3 turns because the ×3 flood carries her well past 25%. The next loop
  would try Facet ×5 or a Phase II gate at 65%, and the flood at ×2.5 to leave more for the climax.

---

## 6. Decisions for the director

1. **The structure.** Approve the three phases (Lucid; Every Name, Remembered; A Good Impression) and the cut list: The
   Quiet, Shatterfall, The Held Breath and Breathless Pull, The Long Hush (`finalstand`) and the old Glassfall chain
   leave Act III.
2. **Length and toughness.** Saint DR 40 → 25 at 60,600 HP: 29 → 17 rounds fresh.
3. **The Phase I follow mark.** Hold Still as a 3-hex bar at **50%** (L5) or **lethal** (L6: perfect 17/20, real 10/20).
   And confirm the bar shape over Act I's ring (the ring's two-drain trap, 3.3).
4. **The heal cut.** 10 rounds instead of 20, sparing the three stars, warned by The Names Stir at 70%, landing on the
   first clean turn below 60%.
5. **The windows.** ×4 (Facet Breaks), ×3 (the flood), ×2 (every pane). Optionally ×5 and ×2.5, the next loop's levers.
6. **Her Cradle.** The Silence Holds Her: 75% damage reduction and 30% absorb for 3 rounds, cooldown 6, with Stillness
   radius 3. One Clear strips all of it plus the ramp. This changes Act I's lesson ("kill the holder") to "Clear the
   holder" by design.
7. **The Remainder Lancet.** A Saint-only Lancet (40 AP, cooldown 2, clearable ramp), with the shared Glass Lancet left
   to Acts I–II.
8. **Phase II reuses Act II's etchings** (Rime, Ember, Heart) and their art unchanged.
9. **Enrage at round 36** (was 80).
10. **Text and art.** A [TXT] pass for 24 records; the optional new art (the Stir preview, a column drop, a corrupted
    etch lattice); `w_clear` opening on the last pane.

---

## 7. Ship pass (2026-11-05, RUL-2026-11-05-123 item 5: ships Friday 2026-11-06)

The director approved the direction and decisions 1–9 as recommended above. Decision 10, the text, is drafted but still
pending. Package: `fable/mother-of-echoes-act3` @ `11ec84e4`, one commit on top of `fable/mother-of-echoes-sim` @
`3eb8abab`.

**Changes since section 5:**
- **The player's own hex is never part of a follow mark.** The live log confirms a ground drain binds whoever stands on
  its hex when any action resolves (sim agent, `3eb8abab`), so a mark that includes the player's hex cannot be dodged.
  Hold Still is now (0, ±1), (0, ±2) and Every Line Through You is (0, ±1…4). The player can step aside or hold still;
  walking along the line is what kills. No Act III mark is a ring, so there is no two-drain trap.
- **The Act II etchings are reused** (`moe-etching-a/-b/-d`). That leaves 21 new records; the Saint holds 25 jutsu.
- **Phase I line pools last 1 round instead of 3.** Hold Still and Every Line fire only within 3 hexes; otherwise she
  walks toward the player. Without these, a pool-aware player and a Saint casting from 4–5 hexes stalled into the enrage.
- **Tuning, with two deviations from the approved numbers, both needed for a real climax:**
  - Facet Breaks stays ×4, panes ×2, Cradle 70% damage reduction.
  - **The flood is ×2, not ×3.**
  - **Phase III starts below 35%, not 25%.**
  - With ×3 and 25%, the flood window killed her before Phase III in 8 of 20 runs.
- **Decision 3 by the full-fight rule:** full-fight perfect play cleared 9/20 (45%), below 50%, so the Hold Still bar
  stays at 50%. A lethal bar gave the identical 9/20: no player in the sim ever stood on it.

**Results (20 seeds):**

| Run | Perfect | Real | Average | Ignore | Camp | Rounds (median) | Phases I / II / III |
|---|---|---|---|---|---|---|---|
| Act III alone, from full HP | 20/20 | 11/20 | – | – | – | 17 | 8 / 4 / 5 (19 of 20 reach III) |
| Full fight, Acts I–III | **9/20** (Act I 16/20, Act II 10/16, Act III 9/10, 1 enrage) | **0/20** (11 die to Act II Recasts) | 0/20 | 0/20 | 0/20 | – | – |

The Saint idled on 0% of her turns. Act III is no longer where perfect play is lost; Acts I and II are.

**An Absence (the Silence's anti-camping summon, being added by the sim agent):**
- **No room left.** Act III v2 uses all 20 rules, and every turn spends exactly 100 AP: a 60+40 chain in Phases I and
  III, the 100-AP combo in Phase II.
- **Phase II needs no new rule.** An Absence can replace one Hush Rises step in the Phase II combo (C4: Hush on a star
  plus An Absence instead of Rises).
- **Phase I would need a slot.** The only slot that can safely be freed is rule 13, the end turn on phase ≥ 1, which
  matters only if a combo step fails (never seen). An Absence would then replace the Lancet or Hold Still as the 40-AP
  extra.
- **Phase III needs nothing.** Every Line already does anti-camping.
- **Unfair combinations to keep out:**
  - A pool beside a star during C2–C3: the stars are 3–4 hexes apart, the etching removes one and the Hush another.
  - A pool on the side-step hexes of the Hold Still bar or the Every Line column.
  - A pool on the ring 4 hexes from her while she is cradled: that is where the Clear has to be cast from, just outside
    Stillness.

**Fixes to make Act III v2 behave correctly on the upstream engine (cb755375), from the sim agent, 2026-11-06:**
1. **The Phase II cycle-end marker moved from `fleeprevent` to `onehitkillprevent`.**
   - The Refraction opener (MK3.a) and pane C also used `fleeprevent`.
   - As a result, the Phase II Hush let Lucid Refraction fire with nothing drawn: 10 unwarned blasts and 5 perfect-play deaths in 30 runs.
2. **Facet Breaks cooldown went from 0 to 2.**
   - It could re-fire the round after its own break while its marker was still live: 1 unwarned blast in 240 runs.
   - A cooldown of 1 doesn't block this, because the engine treats an action as ready once rounds passed ≥ cooldown (actions.ts:316-318).
   - No intended break is lost: the chain already spaces breaks at least 4 rounds apart.
3. **Lethal hits are `onehitkill` power 100 with target INHERIT.** The captured donor shape has target SELF, which cast the kill on the Saint herself.
4. **Nothing Moves cooldown went from 0 to 3.** Its pierce could re-fire the round after its mark with nothing drawn (1 unwarned blast in 240 runs, seed 408). The shared-cooldown table locks only the caster's *other* pierce actions, not the same jutsu, so the "one flat pierce per caster per 3 rounds" spacing (RUL-2026-11-06-128) has to be enforced by the jutsu's own cooldown.

**Final spec:** `fable/mother-of-echoes-sim` @ fd3531153df7a1dfa9f4e559b39d1ad50055a0f6 (engine cb755375). It is variant (a)+(b): Act III enrage at round 17, plus a 15% Act I OHKO chance.

Final confirmation, 30 runs per profile:

| Profile | Clears |
|---|---|
| Perfect | 18/30 (60%) |
| Real | 3/30 (10%) |
| Real, Silence first | 3/30 (10%) |
| Average, camp, ignore | 0/30 each |

- Unwarned blasts: 0.
- Panes landing on safe hexes: 0.
- Recasts on unetched hexes: 0.
