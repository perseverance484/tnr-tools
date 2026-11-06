# The Mother of Echoes: jutsu text pass

**Status: DRAFT, pending director approval (2026-11-05).** Nothing here is live. The machine-readable copy is `push/mother_of_echoes_text.json` (not wired into `push/mother_of_echoes.gen.py` yet).

## Voice and the hint rule

- **Voice:** restrained and eerie; glass, light, stillness and the names in the glass. Sayo is precise and patient. No exclamation marks, no purple prose.
- **Hint, don't instruct (director, 2026-11-05).** Each description hints at the tell and the counter through the fiction, so an attentive player can work the fight out like a puzzle. No imperative how-to lines ("step off", "Cleanse it", "kill the Feeler") and no mechanics-speak ("breaks on her next turn").
- **Accurate clues.** Every clue points at the real mechanic in the push/476 records (spec `7fdaa5da`): for example "the floor goes still before it breaks" for the follow-the-player drain, "while something of the deep still lives" for Cradle, "her guard hangs open for a breath" for the Recasts' self-weakness, and "nothing can wash it off while her eyes are closed" for The Quiet's cleanse block.
- **1–3 sentences.** `battleDescription` (the combat-log line) is kept except where noted.

55 jutsu. Current text is from `push/476_mother_of_echoes_tune.json`.

## Act I: Sayo, Mother of Echoes (refraction and lancet)

### Glass Lancet

- **Current:** A needle of skyglass, thrown hard.
- **Proposed:** She lifts one finger, and a sliver of the wall comes for you. Every lancet she throws steadies the next, and nothing can wash that steadiness from her hand; only time lets it go.

### Lucid

- **Current:** With the Silence gone, Sayo hears herself again: her glass cuts deeper.
- **Proposed:** While her shadow stands beside her, she cannot hear herself think. Silence it, and Sayo hears every thought again, and her glass cuts deeper for it.

### Refraction

- **Current:** Refraction: lines of light from the walls; they shatter on her next turn.
- **Proposed:** "Three lines. Mind them." Light runs in from the walls and lies across the floor, very bright and very still. Light like that does not stay whole for long.

### Far Refraction

- **Current:** Refraction: lines of light from the walls; they shatter on her next turn.
- **Proposed:** "Three more." Light runs in from the far walls, laid across the floor where the first lines were not. It is just as bright, and just as brittle.

### Facet

- **Current:** Below 60%: her Refraction is drawn with its mirror image (both line sets); they shatter on her next turn.
- **Proposed:** Once her glass is badly cracked, every line she draws has a reflection, mirrored across the hall. The gaps between a line and its double are narrow, and they are all there is.

### Refraction Breaks

- **Current:** The marked lines shatter.
- **Proposed:** The lines of light shatter where they lie, and whoever stood on one is cut deep. For a moment the broken glass stays sharp underfoot: wounds taken there close slowly and open wider.

### Far Refraction Breaks

- **Current:** The marked lines shatter.
- **Proposed:** The far lines shatter where they lie. The shards stay sharp a moment longer than the light, and nothing standing in them mends well or bleeds little.

### Facet Breaks

- **Current:** The marked lines shatter.
- **Proposed:** The lines and their reflection shatter together. Where both images broke, the floor stays jagged for a moment, and nothing on it mends well.

### Lucid Refraction

- **Current:** Lucid: the lines shatter and are drawn again at once.
- **Proposed:** "I can see it clearly now." The lines shatter, and new ones are already lying where the light falls. She no longer needs to pause between one thought and the next.

### Your Likeness

- **Current:** Below 40%: she casts your impression from the glass for three rounds.
- **Proposed:** "Hold still. There. That is you." When she is badly hurt, she pours an impression of you out of the glass. It fights the way you fight, but an impression is thin, and it does not last.

### The Glass Remembers

- **Current:** Enrage: every surface of the hall answers at once.
- **Proposed:** The hall is patient, but not forever. Linger too long in her house and every pane turns toward you at once, and there is no floor left that is not glass.

## Act I: The Silence and the Feeler of the Deep (hush)

### The Hush

- **Current:** The Hush: stilled pools seep up through the floor; standing in one drains you and nothing heals you.
- **Proposed:** Where her shadow passes, sound stops and does not come back. The still pools it leaves stay a long time; whatever stands in them slowly empties, and no wound there will close.

### The Hush, Unbridled

- **Current:** The Hush: stilled pools seep up through the floor; standing in one drains you and nothing heals you.
- **Proposed:** Nothing holds the quiet back now. It pours up through the floor faster than it ever did, and the pools it leaves wound whatever stands in them. Clean floor grows scarce.
- **battleDescription, current:** Nothing holds the quiet back now. It pours up out of the floor.
- **battleDescription, proposed:** Nothing holds the quiet back now. It pours up out of the floor in still, dark pools.

### Stillness

- **Current:** The deep listens around the Silence: next turn, everything within 3 is crushed and stunned.
- **Proposed:** The floor around the Silence goes still, and everything near her begins to stop. Nothing close to her moves for long. The far side of the hall is still loud.

### Nothing Moves

- **Current:** Everything within 3 of the Silence is crushed and stunned.
- **Proposed:** For a moment nothing near the Silence moves, and nothing can. Those it holds are crushed, and for a few rounds after their wounds close slowly and open easily, until something clean washes the stillness off.

### The Listening

- **Current:** The Listening: a feeler of the deep rises and listens for movement.
- **Proposed:** Something under the floor turns toward the sound of you. A feeler of the deep rises and listens, and while any part of the deep still lives in the hall, it keeps hold of her.

### The Listening, Unbridled

- **Current:** The Listening: a feeler of the deep rises and listens for movement.
- **Proposed:** It no longer waits to hear you. The feelers rise one after another now, and as long as one of them lives, the deep keeps its hold on her.

### The Silence Turns

- **Current:** The floor under you goes still; it breaks next turn unless you move.
- **Proposed:** Her shadow turns toward the weight of you. The floor under your feet goes still before it breaks, and it takes a great deal from whatever is still standing on it.
- **battleDescription, current:** The floor under %target goes still. Something below has turned toward it.
- **battleDescription, proposed:** The floor under %target goes still. Something below has turned toward it.

### Cradle

- **Current:** While a feeler lives, the Silence holds Sayo: 90% less damage taken, and the hold cannot be cleared.
- **Proposed:** The deep closes around her like cupped hands, and blows slide off the glass. It holds her only while something of the deep still lives in the hall, and nothing can pry the hold loose but that.

### Grasp

- **Current:** The feeler takes hold of whatever is nearest: rooted, and drained.
- **Proposed:** The feeler closes around whatever is nearest, without a sound. What it holds cannot move for a moment and slowly empties, and the floor beneath a held thing does not wait for it.

## Your Likeness (summon)

### Your Own Strike

- **Current:** Your likeness strikes with your habits.
- **Proposed:** Your likeness strikes exactly the way you would, straight through the guard you trust. It has learned only your habits, and only for a little while.

## Act II: Sayo, Glasswright of the Stilling (etching)

### Etching: Rime

- **Current:** She etches a pattern into the glass. It will remember.
- **Proposed:** She traces the north of the hall into the glass. It rimes over, glows, and fades. The glass forgets nothing she draws.

### Etching: Ember

- **Current:** She etches a pattern into the glass. It will remember.
- **Proposed:** She traces the south of the hall into the glass. It glows like an ember, then fades from sight, but not from the glass.

### Etching: Seam

- **Current:** She etches a pattern into the glass. It will remember.
- **Proposed:** She traces a seam down the west wall. It glows, then sinks into the glass, which keeps it the way a scar keeps a cut.

### Etching: Heart

- **Current:** She etches a pattern into the glass. It will remember.
- **Proposed:** She traces the heart of the hall into the glass. It beats once, then fades. The glass keeps the rhythm long after the light is gone.

### Etching: Hail

- **Current:** She etches a pattern into the glass. It will remember.
- **Proposed:** She taps a scatter of points into the glass, like hail. Each one glows and fades, and each one is remembered, exactly where it fell.

### Recast: Rime

- **Current:** The glass remembers an etching and detonates it, unmarked. While she recasts, her guard is open (x3 damage taken).
- **Proposed:** The glass remembers the rime, and the north of the hall breaks with nothing to show where. Only someone who also remembers will be standing elsewhere. For a breath after the glass answers her, her own guard hangs open.

### Recast: Ember

- **Current:** The glass remembers an etching and detonates it, unmarked. While she recasts, her guard is open (x3 damage taken).
- **Proposed:** The glass remembers the ember, and the south of the hall breaks without a mark. The ember was shown once, and once is all it gets. While the glass answers, she is open to anyone who stayed whole.

### Recast: Seam

- **Current:** The glass remembers an etching and detonates it, unmarked. While she recasts, her guard is open (x3 damage taken).
- **Proposed:** The glass remembers the seam, and the west wall breaks, unmarked. The scar was always there for anyone who watched it sink in. Her guard stays open for a breath after the glass answers.

### Recast: Heart

- **Current:** The glass remembers an etching and detonates it, unmarked. While she recasts, her guard is open (x3 damage taken).
- **Proposed:** The glass remembers the heart, and the middle of the hall breaks, unmarked. The edges that never glowed are the only ones it does not remember. For a breath afterward her own guard hangs open.

### Recast: Hail

- **Current:** The glass remembers an etching and detonates it, unmarked. While she recasts, her guard is open (x3 damage taken).
- **Proposed:** The glass remembers every point of hail, and all of them break at once, unmarked. Between the points it remembers there is room to stand. In the moment the glass answers, she stands open.

### The Hush Rises

- **Current:** While she etches, the Silence seeps up through the floor: stilled pools that drain and block healing, more of them every cycle.
- **Proposed:** While she etches, the Silence seeps up through the floor in still patches that never close. More of them rise every time she draws, and whatever stands in one empties fast and cannot mend.

### The Glass Falls Quiet

- **Current:** The cycle ends; a Worn afterimage is raised in the lull.
- **Proposed:** "Again." She lowers her hand, and for a moment the hall rests. In the lull, someone worn steps out of the glass, and the next pattern is already waiting in her fingers.

### The Glass Turns

- **Current:** The floor under you goes still; it breaks next turn unless you move.
- **Proposed:** In the lull, the glass remembers the weight of you. The floor where you stand goes still before it breaks, and it takes a great deal from whatever has not moved.
- **battleDescription, current:** The glass under %target remembers the weight of you.
- **battleDescription, proposed:** The glass under %target remembers the weight of you.

### Raise the Gate Porter

- **Current:** Raises one of the Worn: the Gate Porter.
- **Proposed:** The gate porter steps out of the glass, still holding a door that is not there. He keeps his threshold close and clears it of anyone who stands too near, wherever the step back lands them.

### Raise Sister Hana

- **Current:** Raises one of the Worn: Sister Hana.
- **Proposed:** Sister Hana steps out of the glass, hands already busy with someone else's wounds. She mends Sayo as she mended everyone, and she will not stop on her own.

### Raise Cadet Tomo

- **Current:** Raises one of the Worn: Cadet Tomo.
- **Proposed:** Cadet Tomo steps out of the glass, rope in hand, waiting for an order. His line reaches a long way, and it does not care what floor it drags you across.

## Act II: the Worn (echoes)

### Doorward Sweep

- **Current:** The porter sweeps the threshold: damage and a shove.
- **Proposed:** "Gate's closed." The gate porter sweeps the threshold clear with a heavy blow, and whoever stood there is put a step outside, onto whatever floor was behind them.

### Worn Mending

- **Current:** Sister Hana tends Sayo, as she tended everyone.
- **Proposed:** "Hold still, it's nearly done." Sister Hana tends Sayo, closing her wounds a little at a time. She has done this for so long she no longer knows how to stop; someone will have to stop her.

### Cadet's Tether

- **Current:** Tomo throws a line and hauls: pulled 3 hexes.
- **Proposed:** "Line's secure!" Tomo throws his line and hauls, and you come in several steps with it. The rope does not look down at the floor it pulls you over.

## Act III: Sayo, Saint of Stillness (glassfall and hush)

### The Quiet

- **Current:** She channels: you take more damage and heal less, stacking; while she channels it cannot be cleansed.
- **Proposed:** She closes her eyes and the hall goes quiet, and you go quiet with it. Each time, a little more of you stops mending and a little more gives way, and while her eyes are closed nothing can wash it off.

### Shatterfall

- **Current:** A fan of cracks runs out from her; it falls on her next turn.
- **Proposed:** Cracks fan out from her feet across the glass. Glass that cracked like that will not hold anyone's weight for long, and no one standing in the fan has ever walked out of the fall.

### Shatterfall Gives Way

- **Current:** The fan falls.
- **Proposed:** The fan of cracks gives way, and the glass beneath it falls. Those who were standing in it do not come back up, and the broken edges stay sharp underfoot for a while after.

### Every Name in the Glass

- **Current:** Every stilled name rises to the floor; only where the three refused stays dry.
- **Proposed:** "Do you hear them? Every one of them stayed." Every stilled name rises to the floor at once, and the whole hall glows with them, except three places: where the three refused.

### The Names Flood In

- **Current:** The flood of names.
- **Proposed:** Every name in the glass floods the hall. They take everyone who stands among them; only the three who refused were never theirs, and the ground where they stood stays dry.

### No One Is Mended

- **Current:** For the whole of Every Name in the Glass, the Hush covers the floor: nothing mends.
- **Proposed:** "Nothing mends here. Nothing needs to." While the names rise, the quiet covers the whole floor, and for a long time no wound anywhere will close. What you carried in is all you will have.

### Hush Where They Refused

- **Current:** The Hush seeps into one of the three dry places.
- **Proposed:** The quiet finds one of the three dry places and seeps into it. That place is no longer dry; whoever waits there empties and cannot mend, and two places remain.

### The Held Breath

- **Current:** She breathes in. Next turn, everyone not standing where the three refused is drawn in and loses their breath.
- **Proposed:** She breathes in, and the air leaves the hall, except where the three refused. Something that large will have to be breathed out again, and everyone it reaches will go with it.

### Breathless Pull

- **Current:** The breath she took is spent: everyone off the dry tiles is drawn toward her and stunned.
- **Proposed:** The breath she took is spent. Everyone it reaches is drawn toward her and left breathless, unable to move from wherever the breath set them down. The three dry places keep their air.

### The Long Hush

- **Current:** Below 25%: she cannot fall for 6 rounds; the glass begins to fall.
- **Proposed:** "Not yet. You are almost a good impression." When she is nearly broken, the hush holds her up and she will not fall, but no hush lasts. Above, the ceiling begins to come down.

### Glassfall: First Pane

- **Current:** The marked third of the hall is crushed; the next third is marked.
- **Proposed:** A third of the ceiling comes down where the glass was marked, and the next pane cracks. The ceiling has three panes, and it falls one third at a time.

### Glassfall: Second Pane

- **Current:** The marked third of the hall is crushed; the next third is marked.
- **Proposed:** Another third of the ceiling comes down, and the next pane cracks. What was marked falls; what is newly marked will fall next.

### Glassfall: Last Pane

- **Current:** The marked third of the hall is crushed; the next third is marked.
- **Proposed:** The last third of the ceiling comes down, and the first pane cracks again. The fall goes round the hall the way a clock does.

### Glassfall: Opening Pane

- **Current:** The marked third of the hall is crushed; the next third is marked.
- **Proposed:** This time the second third comes down first, and the last pane cracks. The ceiling keeps its marks honest even when it does not keep its order.

### Glassfall: Heart Recast

- **Current:** The marked third of the hall is crushed; the next third is marked.
- **Proposed:** The ceiling comes down, and the glass remembers the heart once more. Whoever learned where the heart was drawn in the Stilling remembers it too.
