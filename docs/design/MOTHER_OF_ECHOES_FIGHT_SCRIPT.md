# The Mother of Echoes: fight script

**Status:** design target (RUL-2026-11-05-119 item 5: "the fight script is the design target alongside the clear rates").
Written 2026-11-05 for the director. Design and analysis only. Live-game requests: 0. No records were changed.

**What this is.** A round-by-round rehearsal of the fight as it is built today. For each beat it gives what the boss
does, what the screen shows, what the player should do, and what happens if they don't. It then audits engagement and
readability and ranks the changes that would make the fight play the way it should.

**Sources (numbers are current but still moving; the sim agent is iterating):**

| Source | Pin |
|---|---|
| Fight spec, AI rules, params | `fable/mother-of-echoes-sim` @ `700a0d6b` (`harness/skyglass_wreck_sim/mother_of_echoes_spec.json`, `overrides/moe.params.json`). This is a local, unpushed sim commit. The live build pins `780907a7` (`push/mother_of_echoes.gen.py` `SPEC_REF`), which has no boss auras, no Silence stalk and no anchored Stillness. |
| Sim runs used here | Re-run offline at `700a0d6b` with final params: 20 seeds, cells `elite_perfect_real:play` and `elite_real:play`; traces for seed 1 (all acts) and seeds 2–3 (Act III alone). Earlier loops come from `results/pass6_wip/L11..L15_*` and the commit log. |
| Engine | theninjarpg @ `3314d122`. Read only; the harness runs it in-process and socket-free. |
| What the player sees | `docs/design/COMBAT_ANIMATION_ENGINE.md` (cited **[AE §n]**), `docs/design/MOTHER_OF_ECHOES_ART.md` (**[ART]**) |
| In-fiction hints | `docs/design/MOTHER_OF_ECHOES_JUTSU_TEXT.md` (**[TXT]**, approved 2026-11-05) |
| Quest flow | `push/mother_of_echoes.gen.py` |
| Live tester | `harvests/battle_logs/moe_practice_dauntless_2026-11-05.txt` (**[LOG]**, spec `7fdaa5da`, before the Lancet retune) |

Evidence labels: **[spec]** is a record or rule in the spec. **[eng]** was read in engine source. **[sim]** is an offline
sim result. **[LOG]** is the live log. **[I]** is my inference.

---

## 0. The short answers

The director's questions, answered with today's build:

- **Can the player look at the screen and tell what the boss is doing?** Mostly, for floor threats. Every eruption has
  its own tile, and every tile is still on screen during the player's turn [AE §0.6]. Buffs and the clock are the gap.
  The Glass Lancet ramp (the fight's clock) has no art. Its only trace is a log line ("damage given increased by up to
  7%"). The four proposed boss auras have no art wired yet: their strips are held as `FX3_UNWIRED` in the gen script.
  There are no damage numbers on the canvas, and HP bars show only for a hovered fighter [AE §1.4]. Act I also puts 3
  to 5 new threats on screen at once, because every AI action in a chain lands in a single snapshot [AE §2.3].
- **Do we have dangerous, clearable boss buffs that say "clear me"?** **No.** Every Glass Lancet puts `clearprevent`
  on Sayo for 9 rounds [spec `moe-glass-lancet`], and while any live `clearprevent` is on her, Clear fails outright
  [eng `tags.ts:3581-3604`, `clear` at `:1252`]. Sayo I and the Saint throw a Lancet almost every other turn. So the
  proposed Heartglass reflect, the Remainder lifesteal and Lucid (+20% damage, 99 rounds) can never be cleared in
  practice. The only clearable boss buff is the Silence's absorb, and at 10% it is not worth Clear's cost: 60 AP and a
  **10-round cooldown** [eng `actions.ts` basicClear]. The Act II Etching shield (600 HP against 60,600) is noise.
- **Do we want 8,000 more damage while moving every round?** Today the dodge is cheap. A perfect player averages about
  **one hex (10 AP) of forced movement per turn** in every act [sim]. Pressure comes from HP attrition (pools, the
  Lancet), not from the dodge eating the turn. Damage is what decides the fight. Act II has a real burst window: the
  ×3 "guard open" after each Recast supplies about 60% of the act's damage. Acts I and III have no window at all.
- **Do we want them to heal and buff?** Only Act III asks for heal timing (No One Is Mended blocks healing for 20
  rounds at 60%), and nothing warns the player beforehand. Buffs are fire-and-forget; nothing in the fight rewards
  buffing at a particular moment.
- **What are we trying to get the player to do?** The intended skills are: *read the floor* (Act I), *remember the
  floor* (Act II), and *find the only safe floor and keep finding it* (Act III). The intended choices are kill order,
  target priority and the burst window. Today Act I does what it should but teaches too much at once. Act II is the
  best act. Act III is a long turret phase: median 47 rounds for a perfect player, two thirds of turns end with AP
  unspent, and the Saint idles in 18% of her turns [sim].
- **Where it stands:** perfect play clears 5 of 20 (target 50–70%). Real-elite play clears 0 of 20 (target 0–10%)
  [sim, final params]. The recommendations below add *answers* (Clear targets, burst windows, visible buffs) rather
  than lowering numbers. That raises perfect play without helping misreaders, which is the puzzle intent.

---

## 1. The player's journey

**Act I: The Glasswright and the Deep. *Lesson: the floor tells you everything, one turn ahead.*** Sayo is skyglass
and light. Crystal lines run across the floor and shatter on her next turn. Her shadow, the Silence, has stood up off
the floor and hunts the player with stilled ground and feelers from the deep. The fantasy is a duel with an artist who
paints your death a turn in advance. The lesson: a mark is a promise kept on her next turn, so step off it and spend
the rest of the turn fighting. Read the board before you act. A feeler in the hall means Sayo is untouchable, so kill
it first. The emotional beat is mastery under pressure. By the end the player is reading two bosses' tiles at once and
choosing who dies first, and each order changes what the survivor becomes.

**Act II: The Stilling. *Lesson: remember what she showed you.*** The glass climbs her body and the Silence's black
cracks creep into it. Sayo stops warning. She etches a region of the hall, the gold lattice fades, and a few turns
later the glass *remembers* it with no mark at all, lethal and in the order she drew it. Every Recast opens her guard
for one turn, so the reward for remembering is the act's damage. The fantasy is outthinking her. The lesson: watch the
etchings and the log, stand where the glass never glowed, and hit hard while her guard hangs open. The emotional beat
is tension, then release: three quiet turns of drawing, then a burst of dodge, dodge, punish.

**Act III: A Good Impression. *Lesson: the hall is hers now; survive the room.*** The Silence folds into her and she
becomes the Saint: black Remainder glass. She shuts off healing across the whole floor and floods everything except
the three places where the Worn once refused her. The fantasy is the last stand of someone who will not be stilled.
The lesson: find the three dry places and move between them as she poisons them one by one, cleanse in the gap when
she stops channelling, and enter the last phase with the HP you will need, because nothing mends. The emotional beat
should be dread, then defiance, and finally the ceiling coming down a third at a time while she refuses to fall. (The
killing blow is never animated [AE §0.11], so the act's last line has to land in the dialog, not on the canvas.)

---

## 2. Shared grammar (what every act relies on)

**Player budget [eng]:** 100 AP per turn (`util.ts:2993`). Move costs 10 AP per hex. Replacement Technique costs 20
and cannot be used while rooted. Clear and Cleanse each cost **60 AP, have range 4 and have a 10-round cooldown**
(`actions.ts` basicClear and basicCleanse). Clear strips *positive* non-innate effects; Cleanse strips the player's own
*negative* effects (`validators/combat.ts:1388-1475`; boss record effects are innate, `fromType: "bloodline"`, and
cannot be cleared, `combat.ts:4133`). Health, chakra and stamina carry between acts with no refills (quest
`carryPools`). The sim's elite player has 6,250 HP.

**Turn order:** it follows `usersState` initiative and is fixed for the battle. In the live log the player acted first,
then the Silence, the Feeler, the pet and Sayo [LOG]. The sim trace puts Sayo before the Silence. Either way, a mark
cast on a boss's turn erupts on that boss's next turn, and **the player gets exactly one turn in between to read it and
respond.**

**Tile language [ART custom set]:** *heavy* (ember-rimmed glass ring: an eruption is coming), *control* (violet links
around a glass eye: stun or pull), *linger* (bile through crazed glass: a pool that hurts while you stand in it),
*safe* (cyan diamond with a star), *etch* (gold-white lattice: remember this). Each act's material shifts from
Heartglass to the Remainder.

**Engine facts that shape the script [AE]:**
- A 1-round mark is on screen for the rest of its cast round and the whole next round, so it is still visible under
  the eruption (§0.6; accepted, RUL-2026-11-05-119 item 3).
- Everything the AI does between two player clicks appears in one snapshot. Nothing is sequenced (§2.3).
- `decrease*` tags on characters are invisible (§0.5). Cradle's art was moved onto its `clearprevent` so that it shows
  [ART].
- There are no floating numbers. HP bars show only for the selected or hovered fighter (§1.4).
- The killing blow is not animated (§0.11).

**The clock:** each Glass Lancet adds +7% damage given for 9 rounds. Stacks multiply, so about 10 live stacks reach
1.97× [spec; commit `7fdaa5da`]. Each boss also has a hard enrage, The Glass Remembers: Act I round 60, Act II after
cycle 4, Act III round 80.

---

## 3. Act I: The Glasswright and the Deep

### 3.1 Cast and budget

| Unit | HP | Notes [spec] |
|---|---|---|
| Sayo, Mother of Echoes | 10,100 | DR 15 plus AI Heavy Armor; Cradled (−90% damage taken) while a Feeler lives |
| The Silence | 5,050 | DR 25 |
| A Feeler of the Deep (summon) | 2,500 | 8 rounds; about 3 per fight (61 Listenings in 20 runs) [sim] |
| Your Likeness (summon, Sayo below 40%) | 6,000 | 3 rounds; can be outlasted |

**Damage budget (perfect elite) [sim]:** remove about 15,150 boss HP plus about 7,500 Feeler HP in a **median 13
rounds** (won fights). That is roughly **1,750 HP per round** of output, about 1.6 attacks per turn at 1,100–1,800 per
hit on Sayo (seed-1 trace). The live check is consistent: the director's Thunderclap did 120.5 to a Cradled Sayo,
about 1,205 un-Cradled [LOG]. **Forced vs free:** 0.98 moves per turn (about 10 AP) and 0.08 Clear or Cleanse per turn.
34% of turns end with AP left. **Outcome:** Act I clear rate 11 of 20 (55%). Deaths: 6 on readable mechanics, 3 on
filler (Glass Lancet). Damage taken splits 57% readable and 43% filler.

### 3.2 Her loop

Rule order is in the spec, `moe-ai-sayo` rules 1–20 and `moe-ai-silence` rules 1–13.

| Round | Sayo (acts last) | The Silence | Feeler |
|---|---|---|---|
| 1 | **Refraction** (40 AP): 27-hex heavy line set, plus +reflect aura (proposal) and a **Lancet** (60) if within 5 | **The Silence Turns** (cd 4): heavy hex plus ring *under the player*; 40% max-HP drain on their next action if still there. Then **The Listening** (Feeler) | Cradle on Sayo, then Grasp if within 2 |
| 2 | **Refraction Breaks** (100 AP): 3,030 pierce (48% of 6,250) on the lines, plus a 1-round pool (−50% heal, +20% damage taken) | **The Hush** (pools, cd 3), or **Stillness** (cd 3) if the player is within 2: a control ring of radius 3 round her | Cradle every turn |
| 3 | **Far Refraction** (the other line set) + Lancet | **Nothing Moves** if Stillness was cast: 3,030, stun, −50% heal and +20% damage taken for 3 rounds. Otherwise the Hush, the Listening or idle | Cradle |
| 4 | Far Refraction Breaks | … | … |
| below 60% | **Facet**: both line sets at once (mirror), narrow gaps; Facet Breaks next turn | | |
| below 40% | **Your Likeness** (60 AP) | | |
| Silence dead | **Lucid** (+20% damage, 99 rounds, visible aura) → **Lucid Refraction**: break and re-mark in the same turn, so there are no rest turns | | |
| Sayo dead first | | **Unbridled**: Hush (with damage) and a Feeler every turn | |
| round 60 | The Glass Remembers (enrage) | same | |

The cadence is mark, break, mark, break. On mark turns she has 60 AP spare, which goes into a Lancet whenever the
player is within 5. If the player stays 6 or more hexes away, she walks instead of throwing (rules 17–18).

### 3.3 Beats

| Beat | The tell on screen | What the player should do | If they don't |
|---|---|---|---|
| Refraction / Far Refraction | Heavy Heartglass tiles on 27 hexes, appearing 2× (3× under the player) [ART table], plus the log line *"Hold still. I want to see you in the light."* | Step off: usually 1–2 hexes (10–20 AP). Then fight. | 3,030 pierce (48%) and a 1-round pool debuff |
| Facet (below 60%) | Both line sets at once | Find the gap between a line and its mirror ([TXT]: "the gaps … are all there is") | Same, 3,030 |
| The Silence Turns | A heavy hex and ring **under you** | Move 2 hexes (20 AP) before your next action | 40% max-HP drain (about 2,500) |
| Stillness | A violet control ring, radius 3, round the Silence | Get out of 3 range of her. Or Clear the Silence: its marker (`robprevent`) is a positive effect, so Clear cancels Nothing Moves [eng]. This is unhinted. | 3,030, a stun (lose your next turn, which usually means standing in the next line), and a 3-round debuff (Cleanse it) |
| The Hush pools | Dark linger tiles, 8 rounds | Don't end your turn in one | 2%/round drain plus no healing |
| The Listening → Feeler | Feeler rises (`anim_moe_rise`) next to you; the **Cradle loop braids round Sayo** [ART: moved to `clearprevent`, now visible] | **Switch target to the Feeler** (2,500 HP). Stay more than 2 hexes from it. | Sayo takes −90% damage. Grasp roots you for 1 round, so you cannot step off a mark; only Cleanse frees you. |
| Glass Lancet | Lancet hit art on you; log line "damage given … +7% for 9 rounds" and "cannot be cleared for 9 rounds". **The ramp itself is invisible.** | Nothing to dodge. Mitigate it (DR buffs), stand more than 5 hexes away to make her walk, or kill faster. | Mean 11.4% max HP per hit, max 23.9% [sim]. Rises with every throw. |
| Kill order | Both bosses' HP, on hover only | **Choose:** Silence first gives Lucid (Sayo +20% and no rest turns) but no more Feelers or pools. Sayo first leaves the Silence Unbridled (pools and a Feeler every turn) but only 5,050 HP to chew through. | n/a (both lines can be won) |
| Your Likeness | A summon rises framed in a silvered ring | Outlast it (3 rounds) or burst it if it blocks your line to Sayo | Your Own Strike: pierce, about 360 per hit [sim trace] |

### 3.4 Sample perfect run: rounds 1–8

Annotated from sim trace seed 1 (final params). Sayo starts at (8,5) and the Silence at (11,4); spawn seats vary live.

| R | Screen at the start of your turn | Your turn (AP) | Then the bosses |
|---|---|---|---|
| 1 | Clean floor | Open with buffs and a long-range AoE on Sayo and the Silence (100) | Sayo: **Refraction** and a Lancet (about 600). The Silence: **Silence Turns** under you, plus a Feeler. The Feeler: Cradle and Grasp. *Five new things land in one snapshot.* |
| 2 | Heavy lines; a heavy ring under you; Feeler beside you; Cradle on Sayo | **Dodge** 2 hexes off the ring and the lines (20). Hit the **Feeler** (60). Spend the rest (20). | Refraction **Breaks** (you are clear). The Silence marks **Stillness**: you are within 2 of it. |
| 3 | A violet ring around the Silence; line pools fading | Step 1 out of the ring (10), then wait or buff | **Nothing Moves** hits empty floor. Sayo: **Far Refraction** and a Lancet. |
| 4 | Far lines; Feeler still up | Step off the line (10). AoE the **Feeler and the Silence** (60): the Silence drops to 44%. Fire one more skill (30). | Far Refraction does not break in this trace (see §8, D1). The Silence lays a Hush pool. |
| 5 | A pool near you; Feeler dead; **Cradle gone** | Burst Sayo (100): Sayo goes from 98% to 76%, the Silence to 12% | Sayo: Refraction and a Lancet. A new Feeler and Cradle. |
| 6 | Lines, Feeler, Cradle | Dodge (10). Hit the Feeler. | Breaks miss. The Silence falls to 4% to splash damage. |
| 7 | Silence nearly dead | Finish the Silence. **Kill-order beat:** Sayo wakes, **Lucid** aura on her. | Sayo: Lucid and Far Refraction |
| 8 | The Lucid aura; no Silence, no Feelers | Burst Sayo while the floor is quiet (Sayo 68% → 43%) | A Lancet for 1,495 (24%: the ramp plus Lucid) |

From round 9 on, Sayo drops below 40% and casts Your Likeness, then Facet. The player dodges Facet and sits through 3
rounds of the Likeness. They win at round 13 with 10% HP. They carry **that 10% into Act II**.

---

## 4. Act II: The Stilling

### 4.1 Cast and budget

| Unit | HP | Notes [spec] |
|---|---|---|
| Sayo, Glasswright of the Stilling | 60,600 | DR 55, stun-immune, ×3 damage taken for 1 round after each Recast (`weakness` dmgModifier 3, SELF) |
| The Gate Porter (Worn), cycle-1 lull | 5,000 | Doorward Sweep: pierce plus a 1-hex push, which can push you into a pool or a pattern |
| Sister Hana (Worn), cycle-2 lull | 5,000 | **Worn Mending heals Sayo 8% (about 4,850) every turn**, which is more than a player's normal round |
| Cadet Tomo (Worn), cycles 3+ | 5,000 | Tether: pierce plus a 3-hex pull |

**Damage budget (perfect elite) [sim]:** 60,600 in a **median 19 rounds**, about 3,200 per round. A normal round is
about 2 hits × 1,200 (about 4%). A guard-open round is about 2 hits × 3,600 (about 12%). Over a cycle (6 normal plus 3
guard rounds) about 60% of the damage comes from the guard windows. **Forced vs free:** 0.97 moves per turn (about 10
AP), no Cleanses, 29% of turns end with AP left. **Outcome:** 6 of 11 entered won. Deaths: 3 on pools and drain, 2 to
the Porter's sweep. Damage splits 66% readable and 34% filler. Real-elite play: 1 of 11, with **6 deaths to a
misremembered Recast**. That is the act working as intended.

### 4.2 Her loop

Combos from `spec.combos`. One etching turn is Etching (40 AP) plus The Hush Rises (60 AP).

| Cycle | Etch turns (one region each) | Recast turns (same order, unmarked, 6,500 lethal) | Lull |
|---|---|---|---|
| 1 | Rime (A, north), Ember (B, south), Seam (C, west) | A, B, C | The Glass Falls Quiet, then the Porter, The Glass Turns and Lancets |
| 2 | Heart (D, wide centre), A, C, B | D, A, C, B | the same, with **Hana** |
| 3 | C, A, Hail (E, scatter), A, B | C, A, E, A, B | Tomo |
| 4 | E, B, D, B, C | E, B, D, B, C | then enrage |

On every etching turn **The Hush Rises** puts 10 random pools on the floor (15% max-HP drain per round, no healing, 10
rounds). By the Recast phase, 30–50 pool hexes overlap the "safe" floor the player has to remember.

### 4.3 Beats

| Beat | The tell on screen | What the player should do | If they don't |
|---|---|---|---|
| Etching (×3–5) | Gold-white lattice over the region, visible in the cast round and the next [ART tg_etch]. The log names it ("traces the north of the hall"), and the Stilling shield aura appears (proposal; 600 HP). | **Memorise the region and the order.** Fight freely: these are her free turns, and yours. | Nothing yet |
| The Hush Rises | Linger pools appear at random | Don't stand in them. Plan a Recast-safe hex that is also dry. | 15%/round drain, no healing. **The top Act II killer.** |
| Recast (×3–5 in a row) | **No mark.** The Recast payoff art plays, then a linger pool stays 3 rounds. The **guard-open ring** shows on Sayo [ART moe_guard_open v2]. | Before her turn, stand outside the region that comes due next. **During guard open, burst**: the strongest skills and the Chakra Pill go here. | 6,500 pierce: death at full HP |
| The Glass Falls Quiet (lull) | Dust motes beside Sayo for 2 rounds [ART moe_lull] | Reposition, and deal with the Worn | n/a |
| The Glass Turns | A heavy hex and ring under you | Move 2 hexes | 50% max-HP drain |
| Hana | Mend art on Sayo; her HP climbs | **Switch target and kill Hana.** At 4,850 healed per turn she undoes your damage. | The act stretches past cycle 4 and hits the enrage |
| Porter or Tomo | Sweep or tether art | Keep a buffer from pools and patterns: their push and pull move you onto bad floor | Pushed or pulled into a Recast or a pool |

### 4.4 Sample perfect run: rounds 1–9 and 15–19 (seed 1)

| R | Screen | Your turn | Sayo |
|---|---|---|---|
| 1 | Clean floor; you are at **10% HP** carried from Act I | Energy Potion, buffs, an opener (100) | Etching: **Rime** (north lattice) and Hush Rises |
| 2 | North lattice; 10 pools | Buff and lifesteal attack (heal up) | Etching: **Ember** (south) and Rises |
| 3 | South lattice; 20 pools | Move to the middle, clear of north, south and pools (20). Attack (80): up to 4,455 HP. | Etching: **Seam** (west) and Rises |
| 4 | West lattice; 30 pools; *she is about to recast north* | Stay in the dry centre-east and attack (100) | **Recast: Rime** (north breaks, you are safe). **Guard open.** |
| 5 | Guard ring on Sayo; *south is next* | **Burst** (Chakra Pill, then your best skill): Sayo 87% → 80%. Step east (20). | Recast: Ember. Guard open. |
| 6 | Guard ring | **Burst**: 79% → 69% | Recast: Seam. Guard open. |
| 7 | Guard ring | **Burst**: 67% → 60%. Step (10). | **Falls Quiet**; the Porter rises and sweeps you |
| 8 | Porter adjacent; lull dust | Dodge the Porter (10). Attack. | **The Glass Turns** under you, a Lancet, a sweep |
| 9 | Heavy ring under you | Dodge (10). Recover. | A Lancet; sweep |
| 15 | Cycle 2 (Heart, Rime, Seam, Ember) etched; 27% | Attack | **Recast: Heart** (centre). Guard open. |
| 16–18 | Guard ring each turn | **Dodge to the remembered safe side** (west and south edge), then burst | Recasts: Rime, Seam, Ember |
| 19 | Guard ring | The kill (21% → 0) | n/a |

Act II is the fight working as designed. The memory is real (real-elite deaths are misreads), the reward for the read
is the damage, and the moves are varied: the safe region changes with every Recast.

---

## 5. Act III: A Good Impression

### 5.1 Cast and budget

| Unit | HP | Notes [spec] |
|---|---|---|
| Sayo, Saint of Stillness | 60,600 | DR 40; no stun immunity in this spec (RUL-2026-11-05-119 item 2 adds it) |

**Damage budget (perfect elite) [sim]:** 60,600 in a **median 47 rounds** with the Act I and II carry-over, or 25–33
rounds when started fresh (seeds 2 and 3). That is about **1,300 HP per round**. **Forced vs free:** 0.47 moves per
turn, 0.08 Clear or Cleanse per turn, and **67% of turns end with AP unspent**. **The Saint idles in 57 of 313 turns
(18%).** **Outcome:** 5 of 6 entered won (one enrage at round 80). Damage taken: 20% readable, 70% filler, 10% enrage.
**A perfect player is barely touched by the act's readable mechanics.** Its danger is Lancet chip (mean 14.4% per
hit) and The Quiet.

### 5.2 Her loop

Saint rules 1–20 [spec].

| Phase | Her turns |
|---|---|
| **The Quiet (100–60%)** | Alternates **The Quiet** (the channel: +8% damage taken and −8% healing, stacking, 6 rounds, *cannot be cleansed while she channels*) with **Shatterfall** (heavy fan from her feet, 19 hexes, plus the lifesteal aura (proposal)) + Lancet → **Shatterfall Gives Way** (6,500 lethal, 3-round pool). |
| **Every Name in the Glass (60–25%)** | Opens once with **No One Is Mended**: healing blocked across the whole floor for 20 rounds. Then a loop: **The Held Breath** (control everywhere except the 3 stars) → **Breathless Pull** (everyone off a star is pulled and stunned) plus the **Every Name** mark (heavy everywhere except the stars) → **The Names Flood In** (6,500 lethal off-star) → **Hush Where They Refused** (one star becomes a pool) plus The Quiet → repeat. Shatterfall keeps coming. |
| **The Long Hush (<25%)** | Final stand for 6 rounds (cannot fall), then **Glassfall**: a third of the ceiling falls each turn and the next third is marked (a clock), plus a Heart Recast echo of Act II. |
| round 80 | The Glass Remembers |

### 5.3 Beats

| Beat | The tell on screen | What the player should do | If they don't |
|---|---|---|---|
| The Quiet | Quiet hit art on you. The debuffs are partly invisible: `decreaseheal` hides [AE §0.5]. Log line only. | Cleanse **in the turn after her channel lapses** (`cleanseprevent` lasts 1 round). Once per 10 rounds, so pick the stack. | Stacking damage taken and healing cut |
| Shatterfall | Heavy fan of Remainder glass from her feet | Get out of the fan (1–3 hexes) | 6,500: death |
| No One Is Mended (at 60%) | The whole floor turns to hush floor | **Before pushing her under 60%, top up HP**: nothing heals for 20 rounds | You enter a 20-round no-heal phase low. **No warning exists today.** |
| The Held Breath / Breathless Pull | Control everywhere; **3 cyan stars** | Stand on a star | Pulled toward her and stunned, which costs the next turn and the dodge |
| Every Name / The Names Flood In | Heavy everywhere; 3 stars | Be on a star | 6,500: death |
| Hush Where They Refused | One star becomes a pool | Move to another star | 3%/round drain, no healing |
| The Long Hush / Glassfall | A heavy third of the floor; it rotates | Stay out of the marked third. It moves like a clock ([TXT]: "the fall goes round the hall the way a clock does"). | 6,500 |

### 5.4 Sample perfect run: rounds 1–20, then the dead stretch (seed 1)

| R | Screen | Your turn | Saint |
|---|---|---|---|
| 1 | Clean floor | Opener and buffs | The Quiet on you; Shatterfall fan |
| 2 | Fan in front of her | Step out of the fan (20); attack | Gives Way: misses |
| 3–6 | Quiet stacks | **Mostly dodging and waiting**: rounds 3–6 have no attacks (the policy keeps out of the fan and her reach) | The Quiet; Shatterfall and Lancet; Gives Way |
| 7–15 | The Quiet and fan, alternating | Attack 1–2× per turn from outside the fan. Cleanse at round 10. | 100% → 63% over 9 rounds |
| 16 | **No One Is Mended**: no healing for 20 rounds; Held Breath | (You should have topped up here.) Step to a star. | Held Breath |
| 17–19 | Stars | Hold a star, attack from it | Pull (misses); Every Name; Flood (misses); Hush on a star |
| 20–31 | Rotating stars, the fan, The Quiet | Star-hop, attack | 40% → 25% |
| 32 | Below 25% | n/a | **The Long Hush** |
| 33 | One third heavy | Stay out of it | Glassfall: First Pane |
| **34–47** | **Nothing new** | Attack an idle boss for 14 rounds | **wait, wait, wait…** (see §8, D2) |

---

## 6. Engagement audit

| Recurring player action | Decision or chore? | Why |
|---|---|---|
| Step off a heavy mark (Acts I and III) | **Mostly a chore** after the second cycle | Two fixed line sets alternate. The answer is obvious and costs 10–20 AP. Facet and the Silence Turns add variety. |
| Step off the Silence Turns / Glass Turns ring | Chore, but a good one | It follows you, so it breaks camping (its job). It is one extra move. |
| Leave Stillness range | Small decision | It competes with "stay near to hit the Silence" |
| Kill the Feeler (Cradle) | **Real decision**: target priority | It costs a turn of Sayo damage and gains 10×. It is readable now that the Cradle loop renders. |
| Kill order, Sayo or Silence | **Real decision** | Each order changes the survivor (Lucid vs Unbridled). Make sure players can see this is a choice: both outcomes are hinted [TXT Lucid, Listening Unbridled]. |
| Remember the Etchings (Act II) | **Real puzzle** | Memory plus order plus pools plus push/pull. The best part of the fight. |
| Burst in guard open (Act II) | **Real timing decision** | About 60% of the act's damage. The tell is clear (the guard ring). |
| Kill Hana | **Real target priority** | 4,850 heal per turn makes it obvious, provided the heal is readable (mend art plus HP on hover) |
| Clear | **Absent** | There is no worthwhile clearable target. Sayo is clear-proof via the Lancet; the Silence's absorb is 10%. Players with a Clear in their kit have nothing to aim it at. |
| Cleanse | Decision in Act III (timing around The Quiet's lockout); reactive elsewhere (Grasp root, Nothing Moves debuff) | The 10-round cooldown makes it a real resource. The Grasp-root-on-a-mark moment is the best Cleanse beat. |
| Heal timing | **Mostly absent.** One unwarned beat in Act III at 60%. | Pools block healing locally, so "heal off the pool" is a small decision |
| Buff timing | **Absent** except the Chakra Pill into guard open | Buffs are fire-and-forget |
| Stand on a star (Act III) | **Chore** after the first time | Three fixed stars, star-hop on Hush. Low choice, long duration. |
| Attack | Pure DPS race in Act III phase 1 (fan and Quiet) and in the dead Long Hush stretch | Nothing to read beyond the fan |

**Where are the real choices?** Kill order, the Feeler, Hana, the guard window and Cleanse timing. Act II has three of
them; Act III has one.

**Where is it a DPS race with nothing to read?** Act III phase 1 (63% of her HP at 1–2 attacks per turn while dodging
a fan) and the Long Hush stretch once it stalls. In Act I, once the Silence is dead and the Feelers stop, it is mark,
break, Lancet.

**Where might players be confused?**
1. *The clock is invisible.* The Lancet ramp has no aura, so a 24% Lancet "comes from nowhere" [sim max 23.9%; LOG
   R1 4,638 before the retune].
2. *Marks that do not erupt.* In the sim about half of Act I line marks never break (Refraction marked 106 times,
   landed 52). Unexplained no-shows teach players that marks are optional. See §8, D1.
3. *A boss that stops acting.* The Silence idles in 29% of its turns (77 of 263), the Saint in 18%. The live log
   shows "The Silence stands and does nothing" in 2 of 3 rounds [LOG #5, #18, #24].
4. *Act I overload.* A Refraction, a ring under you, a Feeler, Cradle and a Lancet all arrive in **one snapshot** on
   round 1 [AE §2.3]. The tutorial act is the densest act.
5. *No warning before No One Is Mended.* A 20-round heal block arrives at 60% with no tell.
6. *Clear in the kit, nothing to clear.* A player who tries Clear on Sayo gets "resists being cleared" [eng
   `preventResponse`] and burns a 10-round cooldown.

---

## 7. Readability audit

"Visible" means the art renders by the engine rules (cited). The fourth column says how the threat can be answered:
clear (C), cleanse (Cl), dodge (D), kill (K), or nothing.

| Threat / buff | Act | Visible on screen? | Answer | Intended response |
|---|---|---|---|---|
| Refraction / Far Refraction / Facet marks | I | **Yes**: heavy tile, loop, appear ×2–3 [ART; AE §4] | D (C would cancel the Refraction and Facet Breaks if Sayo were clearable, because `increaserange` and `robprevent` are positive, but not the Far Breaks, whose `fleeprevent` is negative) | Step off |
| Breaks pool (1 round) | I | Yes, linger tile [ART] | D; the debuff is Cl | Don't stand in it |
| **Heartglass reflect 10% (proposal)** | I | **No.** Aura strip held in `FX3_UNWIRED`. The `reflect` tag has no art. Log line only. | **Not C** (Lancet `clearprevent`) | n/a. It is noise at 10%. |
| Glass Lancet hit | all | Yes, a hit on you (Act I material) | none (range-gated at 5) | Mitigate it, or keep range |
| **Lancet ramp (+7%/stack, 9 rounds)** | all | **No.** `increasedamagegiven` has no art; log line only. | **Not C, by design** ([TXT]: "nothing can wash that steadiness from her hand") | Kill faster |
| **Lancet `clearprevent` (9 rounds)** | all | **No**; log line only | n/a | n/a. *It also makes every other Sayo buff unclearable* [eng `preventCheck`]. |
| Lucid (+20%, 99 rounds) | I | **Yes**: `moe_lucid` aura [ART] | **Not C** in practice (Lancet) | Accept it as the price of killing the Silence first |
| Your Likeness | I | Yes: rise art and avatar | K or D (outlast 3 rounds) | Outlast it |
| The Hush pools | I | Yes, dark linger tile | D | Avoid |
| **The Silence absorb 10% (proposal)** | I | Partly: a library shove appear on cast, no loop | **C (works)** | Not worth 60 AP and a 10-round cooldown at 10% |
| Stillness ring → Nothing Moves | I | Yes, control tile ring | D; **C on the Silence cancels it** (unhinted); the debuff is Cl | Leave the ring |
| The Silence Turns | I | Yes, heavy hex and ring under you | D | Move 2 |
| Feeler / Cradle | I | Yes: the rise, the avatar, the **Cradle loop on `clearprevent`** [ART custom set] | **K the Feeler.** Not C (Cradle carries its own `clearprevent`, unclearable by design, [TXT] Cradle) | Switch target |
| Grasp root | I | Yes, grasp hit | Cl (the only escape; Replacement is blocked while rooted) | Stay more than 2 from the Feeler |
| Etching | II | Yes, etch lattice, rounds N and N+1 | Remember it | Memorise it |
| **Stilling shield 600 (proposal)** | II | Yes: shield is positive power, so its static renders | C when no Lancet in the last 9 rounds (she throws only in lulls) | Ignore it; 600 is noise |
| The Hush Rises | II | Yes, linger tile | D | Avoid |
| Recast | II | **No mark, by design.** Payoff art and the pool afterwards. | D, from memory | Stand outside the remembered region |
| Guard open (×3 taken) | II | **Yes**: `moe_guard_open` ring on Sayo [ART] | n/a | **Burst** |
| Lull / Worn | II | Yes: dust, rises, strikes, mend | K (Hana) | Kill Hana; space from the Porter and Tomo |
| The Glass Turns | II | Yes | D | Move 2 |
| Cycle counter (enrage after 4) | II | **No** (the `increasecooldown` counter has no art) | none | n/a |
| The Quiet stacks | III | **Partly**: the hit art shows; the `decreaseheal` half is invisible [AE §0.5]; the `cleanseprevent` window has no art | Cl, timed | Cleanse after the channel |
| Shatterfall fan | III | Yes, heavy | D | Leave the fan |
| **Remainder lifesteal 15% (proposal; being replaced)** | III | **No** (held strip) | **Not C** (Lancet) | n/a |
| No One Is Mended | III | Yes, *when it lands* | none | Top up beforehand (unwarned) |
| Held Breath / Pull | III | Yes: control tiles plus safe stars | D (stars) | Star |
| Every Name / Flood | III | Yes: heavy plus stars | D (stars) | Star |
| Hush on a star | III | Yes, linger | D | Switch star |
| Long Hush final stand | III | **No art on `finalstand`**; log line | none | Know she can't fall |
| Glassfall thirds | III | Yes, heavy, rotating | D | Follow the clock |
| Enrage (all acts) | all | **No countdown** | none | Kill before round 60 / cycle 4 / round 80 |

**The specific answers.**
- *Dangerous clearable boss buffs that signal "clear me":* **none.** Lucid is the only dangerous visible buff, and it
  is unclearable.
- *Unclearable by design:* the Lancet ramp ([TXT] Glass Lancet: "only time lets it go") and Cradle ([TXT] Cradle:
  "nothing can pry the hold loose but that"). Both are hinted in the fiction. **Unclearable by accident:** everything
  else on Sayo (reflect, lifesteal, Lucid, and the Act II shield after a lull Lancet). The Lancet's `clearprevent` is
  target-wide, not effect-wide; the engine has no "protect this one effect" option [eng `preventCheck`].
- *Is unclearability communicated?* In the fiction, yes. On screen, no: there is no art for `clearprevent` (except
  Cradle's) and none for the ramp. The player learns it by burning a Clear.

---

## 8. Defects seen while rehearsing (for the sim agent)

| # | What | Evidence | Status |
|---|---|---|---|
| D1 | About half of Act I line marks never erupt (Refraction 106 marked / 52 landed; Facet 23 / 11). In seed 1, both Far Refraction marks fizzle. | [sim] final20, seed-1 trace r3→r4, r7→r8, r11→r12 | Consistent with player stuns draining her AP (the issue behind RUL-2026-11-05-119 item 2) and a shared blast cooldown. The sim agent's working tree (uncommitted) is adding `sayoStunImmune`, `gcdSafeBlasts` and `markArtRounds`. **Verify land ≈ mark after them.** |
| D2 | The Act III Long Hush and Glassfall chain stalls. After The Long Hush the Saint casts at most one pane, then idles until death (seed 1: 14 idle rounds; seed 3: no pane at all). | [sim] traces s1, s2, s3; Glassfall 5 marked / 3 landed in 6 Act IIIs | Glassfall is a 100-AP cast, and the Saint has no `stunprevent` in this spec, so AP drain is the likely cause, as in D1. Same fix; **verify** the chain runs A→B→C→A. |
| D3 | The Silence idles in 29% of its turns | [sim] idle 77 of 263; [LOG] "stands and does nothing" | By design when everything is on cooldown. See R6. |
| D4 | Act I opens with 5 new threats in one snapshot | seed-1 r1; [AE §2.3] | See R5 |

---

## 9. Recommendations, ranked

Each item gives the spec change, the expected effect, and whether it needs **[DIRECTOR]** approval. Expected effects
are directional estimates [I]; each needs a sim loop.

**R1. Land stun immunity and blast-cooldown safety, then re-verify the script (P0, before release).** *Spec:* add
`stunprevent` (100, 100 rounds) to `moe-ai-sayo.effects` and `moe-ai-saint.effects` (Sayo II has it), per
RUL-2026-11-05-119 item 2. Set Breaks, Glassfall and Flood to `cooldown: 0` where a shared cooldown can delay a marked
blast (the sim agent's `gcdSafeBlasts`). *Effect:* every mark comes due (D1) and the Long Hush finale exists (D2). Act
III gets harder (a real last phase), and Act I gets more honest. *Not a decision:* it is already ruled. It just has to
reach the spec, followed by a 20-run check of mark vs land and Glassfall casts.

**R2. Give Act I a real "clear me" buff on the Silence (no Lancet change needed).** *Spec:* `moe-hush` and
`moe-hush-unbridled` effect `absorb`: power 10 → **35–40**, rounds 3; wire `anim_moe_aura_silence_a3` as its
`staticAnimation` (the strip already exists). *Why the Silence:* it has no `clearprevent`, so Clear works [eng], and
Clear also strips its Stillness marker (`robprevent` is positive), which cancels Nothing Moves. One Clear (60 AP, range
4, cooldown 10) therefore buys "she stops healing off your hits, and her stun ring fizzles". That is a visible,
dangerous, clearable buff with a double payoff. (The violet ring stays drawn until it expires, because ground tiles are
not on her hex [eng `removeEffects`]. The log line "was cleared of all positive status effects" is the
confirmation.) Update [TXT] The Hush with a hint (e.g. "…and the deep drinks every
blow until something clean breaks its hold"). *Effect:* Clear becomes a timing decision about every 10 rounds, the
Silence-first line gets easier, and the perfect clear rate rises. **[DIRECTOR]** (balance, text).

**R3. Make the clock visible: put an aura on the Lancet ramp.** *Spec:* `moe-glass-lancet.effects[1]`
(`increasedamagegiven`, SELF, 9 rounds): set `staticAnimation` to a subtle "steadying" loop. `increase*` damage
modifiers render as appear plus loop with no server duplicate [AE §1.3 a′], and every stack is its own record drawn on
top of the others [AE §3.3], so **the glow thickens with each stack and thins as stacks expire**. It is a free,
diegetic stack counter. *Effect:* the gradual clock the director asked for becomes readable, and "why did that Lancet
hit 24%" disappears. No balance change. **[DIRECTOR]** art direction only.

**R4. Decide what the Lancet's `clearprevent` is for. Today it silently cancels every Sayo buff design.**
*Option A (recommended):* drop `clearprevent` from `moe-glass-lancet`. Clear then strips the ramp, the aura and Lucid,
once per 10 rounds: "reset the clock" becomes the high-value Clear in all three acts, and R3 shows when it is worth it.
The [TXT] Glass Lancet line changes ("…only time, or a clean break, lets it go"). Side effects to accept or fix: Clear
would also cancel a pending Refraction, Facet or Shatterfall eruption (their markers are positive) but not Far
Refraction or Every Name (negative markers), and it could stall the Glassfall clock (`robprevent` and
`onehitkillprevent` are positive). Either accept that as a "shatter her focus" counter, or move every marker
to a negative type (`fleeprevent`, `summonprevent`, `disarm`, `elementalseal`) so that Clear never cancels a mark.
*Option B:* keep the Lancet clear-proof and **cut the reflect, shield and lifesteal auras**: they can never be
answered and add no readable decision. *Effect of A:* perfect play gains a tool in every act, so clear rates rise
toward the 50–70% target without lowering damage. Misreaders gain little. **[DIRECTOR]** (it reverses an approved text
and a design intent).

**R5. Teach Act I one thing at a time.** *Spec:* add the condition `round_greater_than 3` to the Silence's The Silence
Turns rule (`moe-ai-silence` rule 7), and `round_greater_than 1` to its Listening rule (rule 9). Rounds 1–3 then teach
"lines break next turn" with only pools beside them; the Feeler and Cradle arrive in round 2, and the follow-the-player
ring in round 4. *Effect:* fewer early filler and overload deaths (Act I has 9 perfect deaths in 20 runs), and a clean
tutorial beat. Anti-camping is untouched after round 3. **[DIRECTOR]** (pacing).

**R6. Turn the Silence's idle turns into a readable tell, not dead air.** *Spec:* replace the bare `end_turn` (rule 13)
with a 0-damage 20-AP "The Silence listens" visual on the Feeler's next spawn hex (or on itself) when Listening is 1
round off cooldown. *Effect:* every Silence turn shows something, and the next Feeler is pre-announced. That makes it a
positioning decision: don't stand where the deep is listening. Low cost. **[DIRECTOR]** (a new jutsu record plus art
reuse).

**R7. Give Act III a burst window and shorten it.** *Spec:* append `weakness` (SELF, 1 round, `dmgModifier` 2,
`staticAnimation` `moe_guard_open`) to `moe-breathless-pull` ("breathless" after she exhales). Optionally cut Saint HP
60,600 → about 45,000. *Effect:* phase 2 gains a "hold the star nearest her and punish the exhale" decision. Star
choice becomes risk/reward (near star = burst, far star = safe). The act drops from about 47 to about 30 rounds and the
67% of turns with AP left shrinks. **[DIRECTOR]** (balance). This could also be the Saint's replacement buff slot: a
*vulnerability* she shows, rather than a buff the player cannot touch.

**R8. Telegraph No One Is Mended, so heal timing becomes a decision.** *Spec:* a new Saint rule, `health_below 66`, runs
once (cooldown 99) and casts a 20-AP visual-only "The Names Stir" with `moe_hush_floor` appear art and a log line ("The
names press against the glass. Soon nothing here will mend."). Hint it in [TXT]. *Effect:* players who read it hold
damage at about 61%, heal and buff, then push. That is the heal-timing moment the director asked for. **[DIRECTOR]** (a
new record and text).

**R9. Make Act II's Hush Rises readable instead of random.** *Spec:* `moe-hush-rises` `coordinateTargeting` →
`RANDOM` → the hexes of the etching cast *two turns earlier* (one Rises record per etching, or a fixed lane set per
cycle). Keep drain at 15 (10 tested: no effect). *Effect:* the act's top killer becomes a second memory layer ("the
old etching is drowning") instead of dice. Pool deaths fall, and the puzzle gets deeper rather than noisier.
**[DIRECTOR]** (balance and design).

**R10. Make the auras matter or cut them (the Act II and III proposals).** The Stilling shield of 600 HP against
60,600: either raise it to absorb one burst (about **3,500**, 2 rounds, on every Etching, so the player spends the
first guard hit breaking the pane, or Clears it if R4-A lands), or drop it. The Remainder lifesteal of 15% on a boss
whose hits are about 1,000 is negligible, and the brief says it is being replaced; see R7. **[DIRECTOR]**.

**R11. Show the Act II cycle counter.** *Spec:* `moe-the-glass-falls-quiet.effects[2]` (`increasecooldown`, SELF, 99
rounds) gets a small `staticAnimation`. Each cycle adds a stack, so a ring is added per cycle [AE §3.3]: a visible "how
close is the enrage". Art reuse. **[DIRECTOR]** art only.

**R12. Land the act endings in the dialog.** The killing blow is never animated [AE §0.11]. The opening of `d_act2`,
`d_act3` and `w_clear` should describe the final break ("The last line of light goes out…"), so the beat happens on
the dialog screen the player actually sees. Text only. **[DIRECTOR]**.

**Release triage (Friday).** R1 is required for the script to be true. R3 and R11 are art-only and safe. R2 and R5 are
small rule and number edits that need one 20-run sim loop. R4, R7, R8, R9 and R10 are design decisions; post-launch
is fine if they are not approved today.

**Clear-rate expectation [I]:** R1 alone lowers perfect play slightly (Act III gets its finale back). R2, R4-A and R7
raise it by giving a reader more tools. R5 and R9 reduce noise deaths. The net should move perfect play from 25%
toward the 50–70% target while real-elite play stays near 0–10%, because every added answer has to be *seen and
timed*.
