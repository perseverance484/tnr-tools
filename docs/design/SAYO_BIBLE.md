# Sayo: character and visual bible

**Status: DRAFT, pending director approval.** Written 2026-11-05 from the director's brief: "Let's look into defining
Sayo, her chakra nature, her moves, and what the animations for the effects should look like. Then we can have a more
premium visual register simply by having consistency and depth to draw on." Design writing only. Live-game requests: 0.
No records, strips or manifests were changed.

**What this file owns, and what it does not.** It is the reference an animator, prompt writer or text writer builds Sayo
from: who she is, what her chakra looks like, and how each of her moves should read on the board. It cites its owners
rather than restating them, and it loses to them where they disagree (`docs/00_INDEX.md` precedence):

| Topic | Canonical owner (this file cites it) |
|---|---|
| Canon: Sayo, the Stilling, the Silence, the Worn | `docs/design/SKYGLASS_STORY_BIBLE.md` (final chapter); RUL-2026-11-01-094, RUL-2026-11-03-111, RUL-2026-11-05-117/-118 |
| Danger grammar (heavy, control, linger, safe) | `docs/design/SKYGLASS_BOSS_ANIMATIONS.md` (readability rules) |
| What the engine can draw | `docs/design/COMBAT_ANIMATION_ENGINE.md` (cited **[AE §n]**) |
| Slot list, wiring, act materials as built | `docs/design/MOTHER_OF_ECHOES_ART.md`; `push/mother_of_echoes.gen.py` (`FAMILY`, `BOSS_ACT`, `TG3`, `MOSAIC`, `SFX_BY_NAME`) |
| What each move does | spec `harness/skyglass_wreck_sim/mother_of_echoes_spec.json` at `fable/mother-of-echoes-sim@700a0d6b` (pass 6 final; the live build pins `780907a7`) |
| Player-facing move text | `docs/design/MOTHER_OF_ECHOES_JUTSU_TEXT.md` (approved) |
| The fight as played | `docs/design/MOTHER_OF_ECHOES_FIGHT_SCRIPT.md` |
| House style, tech ceiling | `docs/design/ghost_ship_art_bible/ART_BIBLE.md` |

Lines marked **[proposed]** are new texture this bible offers for approval. Everything else is drawn from the owners
above or from the approved art (`art/mother_of_echoes/exports/avatar_moe_sayo_v2`, `_sayo_stilling`, `_saint`,
`_silence`; `art/skyglass_variant_skins/raw/ME40_raw_icon-variant-heartglass_approved.png` and
`variant_the_remainder.png`; the art3 build `art/mother_of_echoes_fx/build_fx_a3.py`).

---

## 1. Who she is

**Sayo, the Glasswright.** She found the root crystal under Crownhold and grew it. Every piece of skyglass in the event
(the ship's Core, the Command Crown, the Lastlight Lantern, every shard) is a splinter of her Mother Glass. She is the
Skyglass Project: the officers commanded it, but she made it. The first afterimage was hers too: she brought back a
medic in a sealing jar, the First Impression. When she introduces herself, she gives one name and one deed: "Sayo. I
grew the glass."

**The Stilling.** Crownhold was besieged, and the ring of enemy camps drew tight around the mountain. On the last night
of the siege she drew the whole army of Crownhold into the Mother Glass: soldiers, officers, the ship's crew and the
Crowned Captain. Crownhold stopped answering, and most dates in the Archivist's register are that one night. Every
afterimage since is one she casts from an impression fixed at that instant. That is why the siege order never ends.
There was no outside sealing and no shogunate. Everything that holds still in this event, Sayo stilled.

**Motive.** She does not think of it as killing. She thinks of it as keeping. "I never lost them. I kept them." A
craftsman's love, pushed until it has no limit: nothing she has made may break, end or leave, so she stopped everything
before it could. **[proposed]** The fear under the fondness is loss, which is why the Silence found her so easily: it
offered her a world in which nothing is ever lost again, because nothing ever moves again.

**Voice.** Precise, patient and fond. She never shouts and never uses an exclamation mark. Short sentences, soft
imperatives: "Hold still." "Turn." "Again." She speaks of people as work: impressions, faces, likenesses, lines. Her
wit is dry and clinical ("How interesting."). Glass, light, stillness and the names in the glass are her vocabulary; no
technology words, ever (story bible, Voice).

**How she sees the player.** As the finest material she has found in a generation. She measured them all along: the
charts, the Lantern, the Night Watch roster in a hand they did not know, and Crownhold itself. She needed someone to
break the Command Crown, the one will that contested hers ("Some nights it does not answer me at once."). The four
shards, each with her thumbprint pressed in while the glass was soft, are her invitation. The player has been "cutting
them out of my glass, one by one", which she finds interesting rather than wrong. She studies the player the way she
studied the others: "You read patterns well. Let us see how well you remember them."

**What she wants.** To still the player and keep them. "Hold still. You will make for a good impression." *Impression*
carries both meanings: what a strong chakra leaves when it is pressed into soft glass, and what the player has made on
her.

**The Silence.** An ancient stillness asleep in the deep mountain. The Mother Glass's roots reached it and woke it. It
hungers for stillness and cannot act without an instrument, so it rides in her shadow, which does not move when she
does. She is not holding it back so much as succumbing to it. It never speaks. Over the fight:
- **Act I:** her shadow stays where it was when she turns, then stands up off the floor and fights beside her as the
  Silence. While it stands beside her she cannot hear herself think: kill it, and she is Lucid, sharper and faster.
- **Act III:** it folds itself small, slides back across the floor into her shadow, and she becomes its vessel. Her
  lips stop moving when she speaks.

**The Worn.** The Gate Porter, Sister Hana and Cadet Tomo are the three who refused. On the night of the Stilling the
porter would not open his door, the sister would not stop tending the wounded, and the cadet ran. The glass could only
keep them worn thin. Their names have no word beside them in the register. They exist only within reach of her glass
(RUL-2026-11-05-118): the player meets them only in her fight, still doing the one thing they refused to stop doing.
The three dry places on the floor in Act III are where they refused. She raises them in the lull of Act II as
something between servants and trophies. **[proposed]** She is gentle with them, as with anything broken that she
still owns.

**One woman, three faces** (RUL-2026-11-03-111: her forms transform her body, not her outfit).

| Act | Name | The face it shows | Look (approved avatar) | The fight's lesson |
|---|---|---|---|---|
| I: The Glasswright and the Deep | Sayo, Mother of Echoes | The **artist and host**: light, reflection, invitation. She paints the player's death a turn ahead and lets them see it. | Floating, hair drifting as if underwater, light veins under the skin. The Heartglass fan open behind her as a halo: framed cyan panes in gunmetal ribs with spiked finials, faces in the panes, the heart crystal at the crown, black tassels with cyan beads. Near-black coat; faceted pale-cyan glass climbing the hems. Eyes open. | Read the floor. |
| II: The Stilling | Sayo, Glasswright of the Stilling | The **scribe**: cold, focused, remembering. She stops warning. | Half her body turned to glass, etched with straight pale-gold lines like a castle floor plan. The fan breaking (cracked panes). Eyes closed, face half glass, hair tied back hard. The etching lattice behind her. | Remember what she showed you. |
| III: A Good Impression | Sayo, Saint of Stillness | The **vessel**: the Silence wearing the glass she made of herself. Serene, ended. | Entirely glass, the Silence's black filling her from inside; cyan light only in cracks. Black tears. A halo of frozen diamond shards where the fan was. Lifted on bone-white feelers; a black smoke silhouette behind her. Eyes closed, hands open, the lancet gone. | The hall is hers. Survive the room. |

The finale line belongs to the player: "The Mother Glass cracks from the root to the crown. For the first time since the
siege, Crownhold makes a sound. You are not stilled." The killing blow is never animated [AE §0.11], so the last beat
lands in the dialog, not on the canvas.

---

## 2. Her chakra nature: held light

### 2.1 What it is in the world

Skyglass holds chakra the way paper holds ink (story bible, Canon). **[proposed]** Sayo's chakra is the reason that is
true. Most chakra flows; hers *settles*. Wherever it comes to rest, it holds, and skyglass grows there, facet by facet,
the way frost finds a windowpane. That is the Glasswright's whole art, and it has five verbs:

| Verb | In the world | How it looks |
|---|---|---|
| **Grow** | Her resting chakra accretes into crystal. The Mother Glass, the Core, the crown and the shards all grew this way. | Facets that appear edge first and fill inward, in straight-sided steps, never a smooth swell. Growth is always from an edge or a line, never from a glowing point. |
| **Etch** | She scores a line into the glass with the lancet, and the glass keeps the line as a promise. An etching is a memory she means to use. | A bright scribe point travels and leaves a straight groove behind it. The groove glows white-gold, fades from sight, and stays in the glass. Lines meet at right angles and junctions, like a floor plan. |
| **Refract** | Light in her hall is chakra made visible. She bends it at facets and lays it where she wants it. | Straight lines of light that run in from the walls, lie still on the floor, and split at a facet into a line and its reflection. Light that *lies down*: it is not a beam and it does not flicker. |
| **Remember** | Glass keeps what was pressed into it: a voice, a habit, a face, a pattern. She can make it give them back. Every afterimage, every Recast, The Glass Remembers. | The thing that was there returns exactly: the same lattice in the same place, a face in a pane, a likeness of the player. A return always replays the original shape before it acts. |
| **Still** | Her signature and her sin. She can make motion stop: dust in the air, a breath, a heartbeat, an army. The Stilling was this verb done to everyone at once. | **The held frame:** for an instant before her glass breaks, everything stops. Dust motes hang. Hair stops drifting. Then it breaks all at once. |

An **impression** is literal: a strong chakra pressed into skyglass while the glass is soft, the way her thumb was
pressed into the shards. The Stilling was every chakra in Crownhold pressed into the Mother Glass at once.

### 2.2 How it looks and behaves

- **Light that bends and holds.** Her light lies where it falls, steady, very bright and very still. It has hard edges
  and travels in straight lines. It brightens to white at a facet edge and splits at an angle. It never pulses like a
  flame or crackles like lightning.
- **Memory in glass.** What her glass remembers comes back as the same shape it had, in white or gold, before it acts.
  Faces in panes have their eyes open and do not blink.
- **Stillness as the signature.** Every Sayo payoff has the held frame: anticipation, then **a hold** (2 frames, 100
  ms, in which nothing moves and one cold glint crosses), then the break. Frozen dust motes (2x2 clusters, pale) are her
  particle of rest; they appear in her lulls, her auras and her stillness moves, and they never drift.
- **Glass, never energy.** Her chakra is always on, in or as crystal. A thrown lancet is a sliver of the wall; a
  refraction is light inside glass laid on the floor; a payoff is glass breaking. No floating orbs, no energy beams, no
  magic circles.

### 2.3 Her sounds

**[proposed]** In the world: glass **rings**, like a struck temple bowl, clear and sustained, with a high edge. When she
stills something, the ring **stops dead** mid-tone: her signature is the cut-off, not the strike. Breaking glass is a
dry, bright crack followed by a fall of small pieces. The Mother Glass rings once under the throne when the crown breaks.

In the game: existing in-game SFX only, one per cast (director 2026-11-05; `SFX_BY_NAME`). The mapping in section 4
says which existing sound stands in for which in-world sound. Wind = light running in or a mark arriving; Lightning =
light shattering; Sword Clash = the glass answering a Recast; Earth = glass falling or giving way; Sword = the lancet;
Smoke = the hush and every summon; Punch = a body blow; Heal = mending. A future custom set should start with the
struck-glass ring and the cut-off.

### 2.4 The Silence's chakra: absence

The Silence has no chakra of its own. It is what is left when chakra stops.

| | Sayo (held light) | The Silence (absence) |
|---|---|---|
| Substance | Crystal, light, reflection | Ink: flat, matte black that reflects nothing. A hole cut out of the picture. |
| Motion | Lines travel, facets grow, then the held frame | **Seep** up from below, **spread** outward, **close** inward, **pull** toward it. Slow and one-way. |
| Signature | The hold before the break | **The cut:** things vanish without debris. Sound stops and does not come back. A ring closes and nothing is inside. |
| Edges | Hard, bright, white at the facet | Soft and absolute, outlined only by a thin violet (control) or teal (Remainder) rim so it reads on dark boards. |
| Particles | Prismatic glints, white four-point stars, cyan chips | None that shine. Frozen pale dust beside it; bone-white feelers like roots. |
| What it does to the player | Cuts, breaks, marks | Hushes: drains, stops healing, roots, stuns, draws breath out. |
| Sound | The ring, cut off | **[proposed]** Nothing: the absence of the room's sound, then a low drawn breath. In game: Smoke. |

**How they mix (the Remainder).** A broken afterimage returns to the glass thinner, and the Silence drinks the
**remainder**. Glass that has drunk it is the Remainder: obsidian-black skyglass with smoke moving *inside* the crystal,
thorned and hooked where Heartglass was framed and straight, its light squeezed into the cracks as teal-cyan veins,
bound with bone-white cord. Corruption inverts her light: in Act I light sits *on* the facets and edges (outside in);
in Act III it comes only from *inside* the cracks (inside out). And the smoke is the one thing that moves in her
stillness: corrupted, even her hold is not quite still.

---

## 3. The move families as visual grammar

The six families are the generator's `FAMILY` table (`push/mother_of_echoes.gen.py`, mirrored by the family icons
ME21-ME26). Each family has one shape and one motion; the act sets the material; the danger grammar sets the colour of
the warning (`SKYGLASS_BOSS_ANIMATIONS.md` rule 1: shape carries the meaning, colour confirms it).

**The constants, every act:** heavy is a faceted ring on the floor with an **ember outer rim and an ember edge on every
heavy shard** (the director kept it in all three acts: in the fiction, glass about to break glows at its edge like a
bead at the lamp; it is heat in glass, never fire). Control is a ring of violet links round a closed glass eye. Linger is
bile seeping through crazed glass. Safe is a cut-glass cyan diamond with a white four-point star. Etch is a white-gold
lattice. Danger reads first; the material second.

**The beat every payoff follows:** anticipation (the rim heats, 2-3 frames) → **hold** (1-2 frames, nothing moves) →
impact (one white frame in Act I/II, one teal-white frame in Act III) → follow-through (shards, 4-6 frames) → settle
(scorch or pool, 2-3 frames). 9-15 frames at 50 ms (0.45-0.75 s).

### 3.1 Lancet: the hand

- **In fiction:** a sliver of the wall comes for you when she lifts one finger. Each one steadies the next.
- **Shape:** one long thin needle, point first; one impact star.
- **Motion verbs:** *flick, pierce, steady.*
- **Timing:** fast and dry: 3 frames of flight, 2 held frames of the white star, then chips fall. The quickest thing she
  does.
- **Material:** Glass Lancet and The Glass Remembers are each **one record held by every form** (Lancet: all three Sayos;
  The Glass Remembers: all four bosses), and a record has one look. So the Lancet is drawn in **neutral Mother Glass**
  (clear pale cyan, white star, no act markers), and The Glass Remembers in the corrupted wave (director 2026-11-05: the
  glass remembering what it holds). Per-act lancets would need split records, which is a director decision.
- **Grammar:** not a mark. A hit with no telegraph: the fight's clock.
- **Signature beat:** the held star.
- **Lucid** (the family's buff): the Act I aura changes state. She hears herself: the orbiting facets align, their
  prismatic glints stop, and their edges turn white.

### 3.2 Refraction: lines of light

- **In fiction:** light runs in from the walls and lies across the floor, very bright and very still; it does not stay
  whole for long. Below 60% every line has its reflection.
- **Shape:** straight rows across the hall from a wall (the spec's lines are rows 1, 4 and 7, nine hexes each, running in
  from the left, right and left walls; Facet adds the mirror rows). Long, thin, parallel; the gaps between are the
  safety.
- **Motion verbs:** *travel, lie still, split, shatter along.*
- **Timing:** the mark arrives as a run from the wall end (proposed wave, 3 bands); it lies still for the player's whole
  turn; the break runs the same way, wall end first.
- **Material:** Act I Heartglass only (the family's casters are Act I Sayo).
- **Grammar:** heavy mark (tg_heavy, Act I) → heavy payoff → a 1-round linger pool where the glass stays sharp.
- **Signature beat:** the split. At the impact frame the line cracks *along its length* and the two halves part like a
  pane splitting on a score, with prismatic glints thrown off the facets, before the shards stand up.
- **Every Name in the Glass / The Names Flood In** (Act III members of the family) are refraction turned inside out:
  every pane in the hall lit at once except three places. Their payoff is faces, not lines: a glass mask rises, holds,
  opens its eyes, and bursts.

### 3.3 Etching: carving in sequence

- **In fiction:** she traces a region of the hall into the glass; it glows, fades from sight, and the glass remembers.
  Later the glass breaks there with nothing to show where, in the order she drew.
- **Shape:** a lattice of straight scored lines that meet their neighbours exactly, so a region reads as one etched
  sheet. Right angles and junctions: a castle floor plan (as on her Act II coat).
- **Motion verbs:** *score, glow, sink, remember, answer.*
- **Timing:** the etch is slow and deliberate (a scribe spark cuts the lattice out, the cut flares gold); the Recast is
  the fastest heavy hit in the fight, because the player was meant to have moved already.
- **Material:** Act II, the turn: Heartglass panes, gold scoring, and the Remainder's black cracks and smoke creeping in.
- **Grammar:** a new family, *etch* (white-gold lattice: remember this). Its payoff is a heavy hit without a mark, then a
  linger pool. The guard-open ring on Sayo afterwards is her one window.
- **Signature beat:** the replay. The Recast's first frames redraw the exact lattice in white-gold, then glass blades rise
  along it, then black cracks race up the blades and they shatter. The mark comes due.
- **The Glass Turns** (the family's follow mark): the glass remembers the weight of you. A heavy ring under the player in
  Act II material.

### 3.4 Glassfall: falling planes

- **In fiction:** the ceiling comes down a third at a time, like a clock; the floor fan gives way under her cracks.
- **Shape:** large flat planes, point first; a shadow on the floor that grows before the pane arrives. Shatterfall is a
  fan of cracks from her feet.
- **Motion verbs:** *crack, fall, give way, sweep round.*
- **Timing:** heavy and late. The longest anticipation in the fight (the shadow grows for 3-4 frames), a hard impact,
  then the burst. Waves sweep across the field so the fall reads as one ceiling, not many small events.
- **Material:** Act III, the Remainder: thorned black panes with teal veins, ember rim on impact.
- **Grammar:** heavy marks and heavy payoffs, each with a 3-round linger pool. The next third is marked by the same cast
  that drops the current one, so the board always shows where the clock goes next.
- **Signature beat:** the wave. Shatterfall Gives Way rolling out from the Saint by rank is the reference for the whole
  fight (the director loved it).

### 3.5 Hush: absence spreading

- **In fiction:** where her shadow passes, sound stops and does not come back. The still pools empty whatever stands in
  them; the deep closes around her like cupped hands; she breathes in, and the air leaves the hall.
- **Shape:** closed rings and flat pools; never shards. Things close *inward*.
- **Motion verbs:** *seep, spread, close, still, draw in, empty.*
- **Timing:** slow in, sudden stop. Pools well up over several frames; a stun ring closes and then *nothing moves* (the
  frozen-dust frame); a pull draws everything to one point and stops dead.
- **Material:** the Silence's: ink, violet edge for control, teal vein for the Remainder, bone-white for feelers. Act II
  hushes are the Silence seeping into her glass; Act III hushes are hers, from inside.
- **Grammar:** linger (pools: drain, no healing), control (violet links: stun, root, pull), and the Silence's heavy
  marks (The Silence Turns). The safe stars in The Held Breath are the only light in the move.
- **Signature beat:** the cut. The ring closes, the dust stops in the air, and the sound stops with it.

### 3.6 Echoes: the kept

- **In fiction:** she pours impressions out of the glass: the player's likeness, and the three who refused.
- **Shape:** the summon itself (the avatar), framed by its entrance; never a second figure drawn in the clip.
- **Motion verbs:** *pour, rise, wear thin, repeat.*
- **Timing:** the entrance (15 frames) cracks the floor glass open around the avatar's feet and lets the summon climb out.
  Their strikes are quick and human, each in the one gesture they kept.
- **Material:** Your Likeness in silvered Heartglass (Act I); the Worn in ash and grey-brown cloth with Act II cracks,
  each keeping one small accent from their avatar (the Porter's lantern amber, Hana's rose, Tomo's cyan-violet frays).
  Never ember, violet or bile on a Worn strike: those colours are warnings.
- **Grammar:** summons and their hits. The pushes and pulls they cause are redirection, drawn on the target's old hex
  [AE: the fighter walks, the clip does not follow].
- **Signature beat:** the rise. Feelers climb out with bone cords; the Worn come up in ash.

### 3.7 Follow marks, auras and intros

- **Follow marks** (The Silence Turns, The Glass Turns): a heavy ring placed *under the player*, in the caster's act
  material. The floor goes still before it breaks: the loop's dust holds, and the ember rim heats.
- **Boss auras** (spec 700a0d6b proposes a real buff per boss: Act I Sayo reflect, the Silence absorb, Act II shield,
  the Saint lifesteal; strips `anim_moe_aura_*_a3`, held in `FX3_UNWIRED`): a loop round the AI portrait on the 0.8 s
  beat, portrait-clear, in the boss's material. The aura is the boss's identity at a glance: Act I Heartglass facets
  orbiting with prismatic glints; the Silence's ink tendrils with teal veins; Act II a gold etch ring with black cracks
  creeping in; the Saint's thorned black shards and shadow tendrils with lit veins. When the buffs land, wire these
  strips, not the library strips the sim spec carries as placeholders.
- **Act-start flourishes** (`anim_moe_flourish_*_a3`, the aura buff's appear, once): each is the act's *turn* in one
  beat. Act I Sayo: the Heartglass fan opens behind her into a halo, pane by pane. The Silence: her shadow peels up off
  the floor into a standing ink hood. Act II: the fan cracks and the lattice draws itself behind her. The Saint: the ink
  folds small and slides into her, and the halo of frozen shards rings out round her head.
- **Dialog portraits:** Sayo only, her act forms (`scene_moe_sayo_a3`, `_sayo_stilling_a3`, `_saint_a3`).

---

## 4. Per-move animation specs

How to read the table:
- **Slot type:** *mark* = ground mark (tile under fighters, loop and appear; on screen for the rest of the cast round and
  all of the next [AE §0.6]). *payoff* = the hit's appear. *wave* = mosaic: the hit's appear is blanked and one
  zero-impact `visual` per band carries the strip, led by `band x 3` blank frames (150 ms per band). *pool* = linger
  ground effect. *loop* = static loop on a fighter. *summon* = summon entrance (plays 1x).
- **Material:** I = Heartglass, II = the turn, III = the Remainder (section 5); a jutsu's material is its holders' act
  (`BOSS_ACT`; the Silence and its feeler are III).
- **Sound:** the in-world sound, then the existing SFX that carries it (`SFX_BY_NAME`; one per cast).
- **Strip status (art3 audit, this pass):** **meets** = matches this bible; **tune** = right idea, fails a 50 px or
  material check, fix in the builder; **redo** = the wrong shape or motion for its family; **rewire** = the right strip
  exists, the slot points at the wrong one; **missing** = no art today.

### 4.1 Act I: Sayo, Mother of Echoes (Heartglass)

| Move | Family | Slot | Mark (cast) | Impact | After | Mosaic / wave / slice | Sound | 50 px notes | Strip status |
|---|---|---|---|---|---|---|---|---|---|
| Refraction, Far Refraction | Refraction | mark (tg_heavy I) | Heartglass ring with ember rim on each row hex; white ring slams down and contracts; loop: mirror glints at the ring ends | (none; 1-round mark) | still visible under the break next turn | **[proposed]** appear as a 3-band wave by distance from the row's wall (light running in) | light running in: Wind | the tile must read as a *row*, so the ring art stays inside the hex and the field joins seamlessly | tile, loop, appear I **meet**; the run-in wave is new |
| Facet | Refraction | mark (tg_heavy I) | both row sets at once: the line and its reflection | | | same wave, both walls | Wind | the gaps are one hex wide; nothing may spill into a gap hex | **meets** |
| Refraction Breaks, Far Refraction Breaks, Facet Breaks | Refraction | payoff + pool (tg_linger I-II) | | anticipation: rim heats; **hold**; white frame; the row **splits lengthwise** and the halves part; Heartglass panes stand up, prismatic glints | sharp-glass pool for 1 round (bile through crazed glass) | **wave, 3 bands from the wall end**, two strip variants (light running left-to-right and right-to-left). Rows are horizontal in the spec, so one orientation serves every line | glass shattering along a score: Lightning | one horizontal crack 2-3 px thick, outlined; the split must read before the shards | `anim_moe_refraction_a3` **redo**: a radial burst, not a line that splits, and not a wave |
| Lucid Refraction | Refraction | payoff + new mark | the new rows land under the burst | as Breaks | the next rows are already lying | as Breaks; the new mark's appear must stay readable under the burst's settle frames | Lightning | the burst must end clear of the hex centre by its last 3 frames so the new ring shows | uses the Breaks strip (**redo** with it) |
| Glass Lancet | Lancet | payoff on target | | needle 3 frames, **held white star 2 frames**, chips fall | (buff on her: +7% damage, 9 rounds; invisible today) | none | a thrown sliver: Sword | thick outlined needle; the star is the read | `anim_moe_lancet_v2` **meets** as the neutral Mother Glass lancet. **[proposed]** a small stacking "steadying" loop on Sayo (positive-power tag, so visible) would show the fight's clock; a UX decision for the director |
| Lucid | Lancet | loop on Sayo | | | the aura's lucid state: facets align, glints stop, edges white | none | the ring, sustained: Lightning | must not draw a second orbit beside the Act I aura | `anim_moe_lucid_aura_v1` **redo**: a second facet orbit that duplicates `aura_sayo1_a3`; make it the aura's lucid state instead |
| Your Likeness | Echoes | summon | the floor glass cracks open in silvered cyan round the summon's feet | the likeness climbs out | | none | Smoke | frames the avatar; no second figure | `anim_moe_rise_likeness_a3` **meets** |
| Your Own Strike (the likeness) | Echoes | payoff on target | | the player's own strike in silvered mirror glass: a slash that reflects (white edge leading, cyan trailing) | | none | Punch | one clean arc 3 px thick | `anim_moe_echo_strike_v1` **redo**: one silver crescent shared by three different actors |
| The Glass Remembers (enrage; every boss) | Lancet | wave | | every pane answers: the corrupted burst rolls across the hall | scorch | **wave, 4 column bands** | glass giving way: Earth | | `anim_moe_enrage_w0..3_a3` **meets** (director 2026-11-05: one record, one corrupted look) |
| Act I aura (reflect, proposed buff) | aura | loop on Sayo | | | Heartglass facets orbit, prismatic 2x2 glints, white on the beat | none | | portrait-clear, aimed high | `anim_moe_aura_sayo1_a3` **meets** (unwired) |
| Act I flourish | intro | aura appear | | the fan opens into a halo, pane by pane, the heart crystal last | settles into the aura | none | | | `anim_moe_flourish_sayo1_a3` **redo**: a generic ring and falling teeth; the four flourishes share one template |

### 4.2 Act I: the Silence and the Feeler (the Remainder)

| Move | Family | Slot | Mark (cast) | Impact | After | Mosaic / wave / slice | Sound | 50 px notes | Strip status |
|---|---|---|---|---|---|---|---|---|---|
| The Hush, The Hush, Unbridled | Hush | pool (tg_linger III) | dark pools well up through crazed black glass, teal-lit crack web | | 8 rounds: drain, no healing | none | sound stopping: Smoke | must stay distinct from the bright Act I-II pool | `tile_moe_linger_dark_a3` **meets** |
| Stillness | Hush | mark (tg_control) | obsidian links with violet lit edges round an ink ground, a closed glass eye, radius 3 round the Silence | | | none | Wind | the ring of links is the read | `tile_moe_control_dark_a3` **meets**; `anim_moe_control_glint_v1` **tune** (1-2 px glints vanish at 50 px) |
| Nothing Moves | Hush | payoff on hit fighters | | a solid ink ring closes from the rim with a crisp violet edge; **the dust stops in the air** | stun | none | the cut: Smoke | | `anim_moe_still_dark_v2` **meets** |
| The Listening, The Listening, Unbridled | Hush | summon | | the floor opens in ink, bone cords climb, the feeler rises | | none | Smoke | frames the avatar | `anim_moe_rise_feeler_a3` **tune**: it carries Heartglass cyan; a feeler is Remainder material (ink, teal vein, bone) |
| The Silence Turns | Hush (follow mark) | mark (tg_heavy III) under the player | thorned black ring with teal veins and the ember rim | (drain next action if still there) | | none | Wind | | heavy III **meets** |
| Cradle (the Feeler) | Hush | loop on Sayo | | | pale feelers braid round her portrait over a violet ink hold | none | Smoke | trimmed clear of the HP bars | `anim_moe_cradle_v2` **meets** |
| Grasp (the Feeler) | Hush | payoff on target | | bone feelers close round the target over an ink pool | rooted, drained | none | Punch | | `anim_moe_grasp_v1` **meets** |
| Silence aura (absorb, proposed) | aura | loop | | | ink tendrils with teal veins | none | | | `anim_moe_aura_silence_a3` **meets** (unwired) |
| Silence flourish | intro | aura appear | | her shadow peels up off the floor and stands | | none | | | `anim_moe_flourish_silence_a3` **redo** (shared template) |

### 4.3 Act II: Sayo, Glasswright of the Stilling (the turn)

| Move | Family | Slot | Mark (cast) | Impact | After | Mosaic / wave / slice | Sound | 50 px notes | Strip status |
|---|---|---|---|---|---|---|---|---|---|
| Etching: Rime, Ember, Seam, Heart, Hail | Etching | mark (tg_etch) | a white scribe spark cuts the lattice out; the cut flares gold; lattice loop with scribe sparks on the 0.8 s beat | | fades; the glass keeps it | the lattice joins across hexes into one sheet | the score: Wind | sparse solid 2x2 score chips, never a 1 px dither | tile v3, glint, appear **meet** |
| Recast: Rime, Ember, Seam, Heart, Hail | Etching | payoff + pool + loop on her | none (unmarked) | the same lattice flashes white-gold, Heartglass blades rise along it, black cracks race up, they shatter | 3-round pool; guard-open ring on Sayo | **[proposed]** a wave in her drawing order. The Recasts are GROUND COORDINATES casts at the live pin (`780907a7`, checked), so the reason `push/mother_of_echoes.gen.py` and the ART doc give for not banding them ("CHARACTER casts") is stale. Banding needs a gen change and the sim's fixed-seed check | the glass answering: Sword Clash | | `anim_moe_recast_a3` **meets** |
| Guard open (the Recast weakness on SELF) | Etching | loop on Sayo | | | a cracked ring of etched gold glass, plates push out and flare white on the beat | none | | | `anim_moe_guard_open_v2` **meets**; optional: one black crack for Act II |
| The Hush Rises | Hush | pool | the Silence seeps up through her floor | | 10 rounds | none | Smoke | | **rewire**: `TG3` gives Act II the bright Act I pool, but this is the Silence seeping in (its own name); use the dark pool, or a II pool with black smoke in the bile |
| The Glass Falls Quiet | Hush | loop on Sayo (fleeprevent) + visual | | | dust curtains beside her, frozen, for the 2-round lull | none | the room exhaling: Smoke | | `anim_moe_lull_v3` **meets**. The visual's appear is `anim_moe_control_appear_v1` (violet links): **rewire**, violet means lock and the lull is the one rest beat. Use no appear, or a dust settle |
| The Glass Turns | Etching (follow mark) | mark (tg_heavy II) under the player | Heartglass ring with gold scoring, black crack and smoke creeping in, ember rim | | | none | Wind | | `tile_moe_heavy_ii_a3` and `anim_moe_heavy_glint_ii_a3` **tune**: at 50 px the Act II tile is indistinguishable from Act I (no gold, the smoke is 1 px). Add two gold scored lines and a 2 px black crack |
| Raise the Gate Porter, Sister Hana, Cadet Tomo | Echoes | summon | | grey-brown ash wells up from cracking glass; the Worn climbs out | | none | Smoke | frames the avatar | `anim_moe_rise_worn_a3` **meets** |
| Doorward Sweep (the Porter) | Echoes | payoff + shove | | a low, heavy sweep of the threshold in ash, one amber lantern spark | the target is put a step outside | none | Punch | | strike: `anim_moe_echo_strike_v1` **redo** (shared crescent); shove `anim_moe_shove_v1` **meets** |
| Worn Mending (Sister Hana) | Echoes | payoff on Sayo | | ash-grey hands' worth of light closing a wound, rose accent | | none | Heal | | `anim_moe_mend_v1` **tune**: gold motes collide with the etch's gold ("remember this"); recolour to ash and rose |
| Cadet's Tether (Tomo) | Echoes | payoff + pull | | a rope line snaps taut and hauls | the target comes in several steps | none | Punch | | strike **redo** (shared crescent; draw the rope); pull `anim_moe_pull_v1` **meets** |
| Act II aura (shield, proposed) | aura | loop | | | gold etch ring with the Remainder's black cracks creeping in | none | | | `anim_moe_aura_sayo2_a3` **meets** (unwired) |
| Act II flourish | intro | aura appear | | the fan cracks and the lattice draws itself behind her | | none | | | `anim_moe_flourish_sayo2_a3` **redo** (shared template) |

### 4.4 Act III: Sayo, Saint of Stillness (the Remainder)

| Move | Family | Slot | Mark (cast) | Impact | After | Mosaic / wave / slice | Sound | 50 px notes | Strip status |
|---|---|---|---|---|---|---|---|---|---|
| The Quiet | Hush | payoff on target | | ink lids close over the target like an eye shutting, one teal vein, a frozen mote; the sound cuts | stacking damage taken and healing cut, uncleansable while she channels | none | Smoke | solid 2-3 px clusters | `anim_moe_quiet_v1` **redo**: a 1 px dotted ring (fails the 50 px rule) in no act's material |
| Shatterfall | Glassfall | mark (tg_heavy III), fan from her feet | thorned black rings with teal veins and the ember rim | | | none | Wind | | heavy III **meets** |
| Shatterfall Gives Way | Glassfall | wave | | the fan gives way: thorned black shards and a void bloom, teal-white impact, ember edge | 3-round pool (dark) | **wave, 5 rank bands out from the Saint** | glass giving way: Earth | | `anim_moe_shatterfall_w0..4_a3` **meets**: the reference for the whole set |
| Every Name in the Glass | Refraction | mark (tg_heavy III) + safe (tg_safe) | every hex marked except three cyan stars where the three refused | | | none | Wind | the three stars must be the most inviting thing on the board | heavy III and safe **meet** |
| The Names Flood In | Refraction | wave | | a glass mask rises, holds, its eyes snap open as ember cracks split it, it bursts | 3-round pool | **wave, 4 bands out from the field centre** | Earth | the director's own keyframes (ME28b), drawn for 50 px | `anim_moe_flood_w0..3_a3` **meets** |
| No One Is Mended | Hush | pool, whole floor, 20 rounds | the quiet covers the whole floor | | no healing anywhere | none | Smoke | **[proposed]** a whole-floor bile field can drown the marks laid over it; consider a lower-contrast ink film with frozen motes | dark pool **meets** the grammar; the low-contrast film is a proposal |
| The Held Breath | Hush | mark (tg_control) + safe | links everywhere except the three stars | | | none | Wind | | control dark and safe **meet** |
| Breathless Pull | Hush | payoff + pull | | breath drawn in from the rim and away upward, a violet lock at the feet | pulled toward her, stunned | none | Wind | | `anim_moe_breath_draw_v1` **tune**: 1-2 px motes haze at 50 px; use 2x2 outlined clusters |
| Hush Where They Refused | Hush | pool on one star | the quiet seeps into one dry place | | 3 rounds | none | Smoke | | dark pool **meets** |
| The Long Hush | Glassfall | mark (tg_heavy III, the first third) + final stand on her | | | she cannot fall for 6 rounds | none | Wind | | mark **meets**; the final stand has **no art (missing)**. **[proposed]** her aura goes fully still: every tendril and mote stops, one teal vein beats |
| Glassfall: First, Second, Last, Opening Pane; Heart Recast | Glassfall | wave + next third marked | the next third's heavy III ring lands in the same cast | a thorned black pane falls point first over its growing shadow, teal-white impact, ember rim, burst | 3-round pool | **wave, 3 column bands**. **[proposed]** a slice: one great pane cut into column pieces, so the third reads as one ceiling falling | Earth | the pane is 7 px wide today; 9-11 px would read better | `anim_moe_glassfall_w0..2_a3` **meets** (the pane width is an optional tune) |
| Saint aura (lifesteal, proposed) | aura | loop | | | thorned black shards and shadow tendrils with lit veins | none | | | `anim_moe_aura_saint_a3` **tune**: at 50 px its shards read as white-outlined isosceles triangles, a hazard-sign glyph. Make them hooked, asymmetric thorns |
| Saint flourish | intro | aura appear | | the ink folds small and slides into her; the halo of frozen shards rings out | | none | | | `anim_moe_flourish_saint_a3` **redo** (shared template; the same triangle glyphs) |

### 4.5 Shared marks (every act)

| Mark | Files | Status |
|---|---|---|
| Heavy, per act | `tile_moe_heavy_{i,ii,iii}_a3`, `anim_moe_heavy_glint_{i,ii,iii}_a3`, `anim_moe_heavy_appear_{i,ii,iii}_a3` | I and III tiles **meet**; II tile and loop **tune** (above). `anim_moe_heavy_appear_iii_a3` **tune**: it slams down the same white ring as Act I; Act III should arrive dark, with the ring's light coming from teal veins |
| Control | `tile_moe_control_dark_a3`, `anim_moe_control_glint_v1`, `anim_moe_control_appear_v1` | tile and appear **meet**; glint **tune** |
| Linger | `tile_moe_linger_v1` (I-II), `tile_moe_linger_dark_a3` (III), `anim_moe_linger_glint_v1`, `anim_moe_linger_appear_v1` | **meet** |
| Safe | `tile_moe_safe_v1`, `anim_moe_safe_glint_v1`, `anim_moe_safe_appear_v1` | **meet** |
| Etch | `tile_moe_etch_v3`, `anim_moe_etch_glint_v1`, `anim_moe_etch_appear_v1` | **meet** |

**Engine notes the specs above rely on** [AE]: everything the AI does between two player clicks lands in one snapshot,
unsequenced (§0.1, §2.3); appears overdraw 2-3x (§0.4), so payoffs use hard alpha and light fills; a clip is a square
2.5 hex-heights wide and cannot reach past one hex ring (§5.5), so anything larger is a per-hex mosaic or slice (§4.2);
`decrease*` tags on fighters are invisible (§0.5); ground marks carry no disappear clip (§5.3); a slice or wave is one
asset per band, and pieces start within a texture load of each other, not frame-locked (§4.2).

---

## 5. Visual register rules

### 5.1 Palette per act

> **Revision (director 2026-11-05: no sickly green; colours per enemy).** No bile, acid or toxic green anywhere in this
> fight: lingering ground and pools take the colour of the enemy that made them and read as danger through material
> and value contrast (frozen, stilled, shattered, blackened, ember-edged), never through a hazard colour. Cyan is
> reserved for safe hexes: in danger art, Heartglass cyan appears only as thin facet lines and glints, never as a fill.
> **Exception (director 2026-11-05):** the Refraction family's Heartglass cyan (the line's arrival and break) keeps its
> cyan fill; it is the fight's quality bar. Everywhere else in danger art the rule above holds.
> Etch gold stays distinct from ember (gold is the scored line, ember only the heavy rim and shard edge). The tables
> below and the grammar constants carry the revision; sections outside 5 are unchanged and still mention bile pools
> (read them through this revision).

Measured from the approved variants and the art3 builder (`build_fx_a3.py` `PAL`, `build_fx.py` constants).

**Act I: Heartglass (light).**

| Role | Hex |
|---|---|
| Deep (the void behind a pane) | `#10101a` |
| Pane seam / frame shadow | `#232231` |
| Gunmetal frame | `#3e3c54` |
| Steel finial | `#5b6786` |
| Glass body | `#49a4c8` |
| Glass lit face | `#5bc6e7` |
| Facet line / glint | `#9ad0e3` |
| Hot edge | `#c8f7fc` |
| Impact white | `#fffffa` |
| Prismatic glints (impact frames only, 2x2, at most 3 per frame) | `#ffaaaa` `#aaffd2` `#beb4ff` |
| The fan's tassel (avatar and icons only; **never in FX**, where violet means control) | `#2a2849` `#574b8b` `#7062ca` |

**Act II: the Stilling (the turn).** Heartglass body, lit face and hot edge as Act I, plus:

| Role | Hex |
|---|---|
| Etch groove, dark | `#3a2c1e` |
| Etch dim | `#967640` |
| Etch gold (the scored line) | `#deb868` |
| Etch hot | `#ffeec4` |
| Deep | `#0e1016` |
| The Remainder's crack (creeping in) | `#080a0f` |
| Smoke in the glass | `#27323c` |

**Act III: the Remainder (corrupted).**

| Role | Hex |
|---|---|
| Deep / outline | `#080a0f` |
| Obsidian body | `#12171e` |
| Obsidian lit face / smoke | `#27323c` |
| Frame (dark teal) | `#142a33` |
| Vein, dim (the variant) | `#2f5c6a` |
| Vein, lit (the variant) | `#92b6bf` |
| Vein, bright (art3, for dark boards) | `#60d6ec` |
| Vein hot / impact | `#c8faff` |
| Void bloom | `#10081e` |
| Bone cord / feeler | `#ebeceb`, shade `#aaacb0`, dark `#2c2e36` |
| Steel | `#6b7681` |

**The Silence:** ink `#0e0c12`; violet edge (control) `#2c1e48` `#604296` `#805cc4` `#b08ce8`; bone as Act III; frozen dust
`#ced2de`.

**The Worn:** ash `#3a3438` `#807670` `#bab2a8`, each with one small accent kept from their avatar (the Porter's lantern
amber, Hana's rose, Tomo's cyan-violet frays).

**Grammar constants (every act; `SKYGLASS_BOSS_ANIMATIONS.md` owns the event-wide set; this fight's revision, director
2026-11-05):** ember `#5c1e12` `#d63a1a` `#ffce54` (heavy only); score outline `#18100a`; safe cyan `#98d6e8` `#cef4fc`
(safe only); violet (control only, as the Silence's table); **no bile in this fight.**

**Lingering ground, by owner (replaces the bile pool):**

| Owner / act | The floor after the ability | Hex |
|---|---|---|
| Sayo, Act I (Heartglass) | crazed white glass: hairline facet cracks in white and white-gold, gunmetal grout, prismatic 2x2 glints at crack junctions (few) | ground `#d8dde6`, crack `#3e3c54`, lit crack `#fffffa` / `#ffeec4`, glint `#ffaaaa` `#beb4ff` |
| Sayo, Act II (the turn) | shattered etched glass: dim gold scores broken, black cracks across them, smoke stains | ground `#0e1016`, smoke `#27323c`, score `#967640`, crack `#080a0f`, lit edge `#9ad0e3` |
| Sayo, Act III (the Remainder) | blackened obsidian, teal cracks frozen mid-run, bone flecks | ground `#12171e`, crack `#142a33` / `#60d6ec`, bone `#ebeceb` |
| The Silence (Hush, An Absence) | matte ink that reflects nothing, frost lying in it, teal only in veins | ink `#0e0c12`, frost `#27323c` / `#465462`, frozen dust `#ced2de`, vein `#2f5c6a` / `#60d6ec` |
| The Worn | ash only (they never leave ground) | ash table above |

Two bones are in use: `build_fx.py` `#e4dece` (warm) and `build_fx_a3.py` `#ebeceb` (the Remainder's cord). New work
uses `#ebeceb`.

### 5.2 Light direction

- **Act I and II:** one cold key light from the upper left. Facets show a lit face (left) and a shade face (right); the
  white highlight runs along the top-left edge. On heavy shards the right face carries the ember edge.
- **Act III:** no outside light. Light comes only from inside the veins. A 1 px teal rim on the upper-left edge keeps
  the black glass legible on dark boards.
- **The Silence:** unlit. Only its rim (violet for control, teal for the Remainder) and its bone feelers show.

### 5.3 Edge treatment

- Hard alpha; a 1 px dark outline round every cluster (score `#18100a` on light material, deep on dark material); a
  1 px clear frame margin [AE §3.4].
- **Act I:** straight, clean edges; white top-left highlight; gunmetal frame bars with spiked finials where panes meet.
- **Act II:** the same straight edges, with gold scored lines *inside* the pane and black hairline cracks starting from
  the edges.
- **Act III:** jagged and hooked; outline plus the teal rim.

### 5.4 Shard shapes

- **Act I:** kite and lozenge facets, and the fan's trapezoid panes (wider at the top), framed. Glints are four-point
  stars (the house emblem's star).
- **Act II:** the same panes, scored with right-angled lattice lines like a floor plan, breaking *along* the scores.
- **Act III:** hooked thorns and curved barbs (the Remainder's barbed limbs), asymmetric, smoke inside.
- **Never** isosceles triangles with a dot or outline at 50 px: they read as teeth or a warning glyph.

### 5.5 Particle vocabulary

| Act | Allowed particles |
|---|---|
| I | prismatic 2x2 glints; white four-point stars; white-gold facet chips (cyan chips only on safe art); frozen dust |
| II | gold scribe sparks; white-gold lattice flashes; black crack ticks; first smoke wisps; ash (the Worn) |
| III | black flecks; smoke curls inside glass; teal vein sparks; bone motes; frozen dust |
| Silence | frozen dust; frost flakes on its ground (matte, never glossy) |
| Heavy (all acts) | ember chips off the rim and shard edges, falling, never rising like flame |

Every particle is a solid 2-3 px cluster with an outline. A 1 px particle is haze after the 50 px rendition and the
linear stretch.

### 5.6 What she never looks like

- **Sci-fi:** no holograms, scanlines, hex grids, glitch, neon bloom, energy beams, lasers, circuitry, panels or screens
  (`ART_BIBLE.md` §2).
- **Generic magic:** no magic circles, runes, written glyphs, sparkle confetti, hearts, swirling auras or coloured fog.
- **Fire:** no flame tongues, fireballs or rising embers. The ember on heavy is glass at breaking heat on an edge, not
  fire.
- **Lightning:** no bolts or crackle, even though the Lightning SFX stands in for shattering light.
- **Ghosts:** no translucent bodies, wisps with faces, skulls or wailing spirits. Faces appear only *in panes* or as the
  glass mask, eyes open.
- **The colour of warnings on a non-warning:** no ember, violet, bile or safe cyan on a summon strike, a heal or a rest
  beat.
- **Soft painting:** no airbrush gradients, glow halos or soft alpha.

**Sayo's house-style exceptions (hers alone):** glass on her body and hems, the fan halo, tassels, floating and the
waived eye-level clause (ME01 note; RUL-2026-11-03-111). The art bible's "no gold" rule is waived only for the Act II
etch gold (the tg_etch family, still pending the director's confirmation, `MOTHER_OF_ECHOES_ART.md` open question 5).
None of these exceptions carries over to any other character.

### 5.7 Consistency checks before shipping

Run all of these on the delivered 50 px rendition, stretched linearly to the clip size, on the light (snow) and dark
battle stills with three fighters standing in the field (`docs/design/mother_of_echoes_fx/preview.py`):

1. **One-second read** (`SKYGLASS_BOSS_ANIMATIONS.md` rule 6): a stranger says "get out" or "get here" within a second.
2. **Shape before colour:** the strip reads correctly in greyscale.
3. **Family:** the shape and motion verb match section 3 (lines split, etches replay, panes fall, hushes close inward,
   echoes rise).
4. **Act material:** palette only from the act's table (5.1); a shared record uses its agreed neutral or corrupted look.
5. **Grammar colours:** ember only on heavy, violet only on control, no bile anywhere (lingering ground in its owner's material, table 5.1), safe cyan only on safe, etch
   gold only on etch.
6. **The beat:** anticipation, hold, impact frame, follow-through, settle; 9-15 frames at 50 ms; the hold is present on
   every Sayo payoff.
7. **Clusters:** no 1 px detail; every cluster outlined; hard alpha; 1 px clear margin.
8. **Overdraw:** the appear still reads when stacked 2-3x [AE §0.4].
9. **Portrait-clear:** loops stay clear of fighter portraits and HP bars; auras stay clear of the AI portrait centre.
10. **Field seams:** a tile repeated over 20 hexes forms one surface with no hex seams; loops share the 0.8 s beat.
11. **Distinct from neighbours:** heavy I vs II vs III, light pool vs dark pool, and the act's aura vs any buff loop on
    the same boss are distinguishable at a glance.
12. **Never list:** nothing from 5.6.
13. **Engine rules:** no disappear clip on a ground mark [AE §5.3]; no art on a tag that goes negative when cast [AE
    §5.1]; at most 80 frames; strip under the byte ceiling; a fresh filename for every revision (law 32).

---

## 6. Strips that do not meet this bible (summary)

| Strip | Verdict | Why |
|---|---|---|
| `anim_moe_refraction_a3` | redo | a radial burst; Refraction's payoff should split along the line and run from the wall as a 3-band wave |
| `anim_moe_flourish_{sayo1,silence,sayo2,saint}_a3` | redo | one ring-and-teeth template recoloured four ways; each act's turn is missing (fan opens, shadow stands, fan cracks, ink folds in). Unwired, so cheap to replace |
| `anim_moe_lucid_aura_v1` | redo | a second facet orbit that duplicates the Act I aura; make it the aura's lucid state |
| `anim_moe_quiet_v1` | redo | 1 px dotted ring, no act material; should be ink lids closing |
| `anim_moe_echo_strike_v1` | redo | one crescent for three actors; split into the likeness's mirror slash, the Porter's sweep and Tomo's rope |
| `tile_moe_heavy_ii_a3`, `anim_moe_heavy_glint_ii_a3` | tune | indistinguishable from Act I at 50 px; add gold scoring and a 2 px black crack |
| `anim_moe_heavy_appear_iii_a3` | tune | arrives as Act I's white ring; should arrive dark with teal veins |
| `anim_moe_aura_saint_a3` | tune | shards read as warning triangles; use hooked thorns |
| `anim_moe_rise_feeler_a3` | tune | Heartglass cyan on a Remainder summon |
| `anim_moe_mend_v1` | tune | gold motes collide with the etch gold; recolour to ash and rose |
| `anim_moe_breath_draw_v1`, `anim_moe_control_glint_v1` | tune | 1-2 px particles haze at 50 px |
| The Hush Rises pool (`TG3`, Act II) | rewire | gets the bright pool; it is the Silence seeping in |
| The Glass Falls Quiet visual appear (`anim_moe_control_appear_v1`) | rewire | violet lock links on the fight's one rest beat |
| The Long Hush final stand | missing | no art for the Saint refusing to fall |

Everything else in section 4 meets the bible. The Shatterfall Gives Way wave is the quality bar for the rest.

**Landed alongside this draft (art4, `97641d00`, not audited here):** `build_fx_a4.py` draws one 30-frame signature
entrance per form (Act I fan opening with a prismatic burst, the Silence's shadow standing up off the floor, Act II gold
etch ring under creeping black cracks, Act III thorns and bone tendrils) with a reveal hold. Those entrances match the
flourish brief in section 3.7 and **supersede the art3 flourish redo** above once they pass section 5.7.
`build_fx_mosaic.py` prototypes slicing one composition across hexes, starting with the Refraction line: that is the
route for the Refraction Breaks redo (section 4.1).

## 7. Open decisions (director)

1. Approve this bible (Sayo's chakra as held light, the held frame as her signature, the Silence as absence).
2. The **[proposed]** texture in sections 1-2: her fear of loss, her sounds (the ring and the cut-off), her gentleness
   with the Worn.
3. Glass Lancet: keep one neutral look, or split the record per act (a build change).
4. A visible stack loop for the Lancet ramp (the fight's clock), and the Long Hush final-stand loop.
5. The Recast wave in drawing order (the Recasts are ground casts at the live pin; the generator's comment saying
   otherwise is stale).
6. The etch gold as a house-style exception (open question 5 in `MOTHER_OF_ECHOES_ART.md`).
