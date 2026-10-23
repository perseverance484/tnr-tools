# Jutsu upgrade batch 1: text (DRAFT)

- **Director, 2026-10-23:** batch 1 approved (`PRIORITY_TARGETS_2026-10-23.md`): the ten most-used NORMAL jutsu not yet
  upgraded get a premium icon and new text, in the voice used for the event jutsu.
- **Voice:** premium tier (`WRITING_STYLE.md`, "Premium tier"): the **description** is a short overview (2 sentences) that
  still names every effect a player will notice; the **battle line** is the jutsu in full bloom (4 sentences), told as the
  story would show it, not as combat mechanics. American English, plain color words.
- **Placeholders:** `%target` only on jutsu aimed at an enemy (`OPPONENT`). Ground and area jutsu (Titanoboa, Clone,
  Body Flicker, Terra Shift, Crescent Strike) describe the area and never assume anyone is in it; the self buff
  (Chakra Overflow) never uses `%target`. No `%jutsu`, no gendered placeholders.
- **Source:** live records from the public `jutsu.getAll` read, 2026-10-23 (`harvests/inbox/tnr_results_1792732003454.json`);
  each is re-confirmed against the push/224 capture before the ticket is built.
- **Status:** DRAFT. Final prose is the director's (CLAUDE.md section 10). No training warnings: every one of the ten still
  gains power per level.

## 1. Chakra Overflow (`e2eC-x4UXc5m6QexNbx8w`)

*Live:* self, 40 AP, cooldown 7: damage given +25% twice (stacked), 2 rounds.
*Old:* description fine but mechanical; battle line runs to five sentences that list "ninjutsu, genjutsu" and say the
name.

**Description:** The user forces their chakra past its natural limit until it spills from their body in a blazing aura.
For a short time, every attack they make strikes with overwhelming force.

**Battle line:** %user draws a slow breath and tears open the gates of their chakra, and power floods out faster than any
body should hold. A blazing aura of white and gold boils around them, spilling over like a river breaking its banks.
Every strike %user throws carries the weight of that flood, landing with a force that shakes the air. For a few precious
moments, %user stands at the edge between control and ruin, and chooses power.

## 2. Summoning: Titanoboa (`ZeqpsECJ882inNKUu0t3d`)

*Live:* empty ground, range 3, 70 AP, cooldown 11: summon 4 rounds.

**Description:** The user offers their blood to the earth and calls forth the Titanoboa, a serpent vast enough to swallow
a gatehouse. The great snake fights at their side for several rounds.

**Battle line:** %user drags a kunai across their palm and slams the bloodied hand to the ground, and a summoning seal burns
outward through the dirt. The earth heaves and splits as coil after coil of emerald scale rises from below, each one
thicker than a tree. At last the Titanoboa lifts its great head above the battlefield, golden eyes narrowing and fangs
bared. It answers to %user alone, and it is hungry.

## 3. Crimson Vein (`GGms9iTcZq_gICEuZYF2Q`)

*Live:* target, range 5, 40 AP, cooldown 7: target takes +20% damage, user lifesteal 25%, 2 rounds.

**Description:** Threads of crimson chakra burrow into the target and open their body to every blow. The same threads carry
stolen life back to the user for a short time.

**Battle line:** %user flicks their fingers, and threads of crimson chakra lash out like living veins to burrow beneath
%target's skin. They spread in a branching web of blood-red light, laying %target open so every strike that follows bites
deeper. Along each thread a pulse of stolen life flows back to %user, mending them with every wound they deal. Bound vein
to vein, %target can only feel their strength drain toward their enemy.

## 4. Abyssal Wraith (`57JrAbfLuAliey0TgH2uM`)

*Live:* target, range 4, 60 AP, cooldown 5: genjutsu damage.
*Old:* battle line repeats itself ("mental strain", "torment", "compromised mental state") and claims extra "calculated
strikes" the jutsu does not make.

**Description:** The user tears open a window onto the abyss and lets a wraith pour out into the target's mind. Its touch
wounds the mind as surely as any blade wounds flesh.

**Battle line:** %user's eyes go dark, and in %target's sight the ground beneath them cracks open onto a bottomless abyss.
From that black pit a wraith claws its way upward, hollow-eyed and shrieking, trailing ghostfire as it rises. It plunges
straight through %target, and the cold of the grave tears through their mind like a blade. When the vision breaks, the
wound it left remains.

## 5. Clone Technique (`clh4d6phm0000tb0h7wo71p2z`)

*Live:* empty ground, range 2, 60 AP, cooldown 7: clone at full strength, 2 rounds.

**Description:** The user splits their chakra in two and steps out of themselves as a perfect copy. The clone shares their
full strength and fights on its own for a short while.

**Battle line:** %user forms a single hand seal, and their chakra splits down the middle with a sharp crack of smoke. From
the drifting cloud a second %user steps forward, identical down to the last scar and the glint in their eye. The clone
moves without a word, as strong and as deadly as the original. For a short while the enemy faces two of %user, and
neither one is a trick.

## 6. Faint Shadow (`GnuyzNIf-Mdu41dnQv5dH`)

*Live:* target, range 4, 60 AP, cooldown 5: genjutsu damage; user damage given +15%, 2 rounds.

**Description:** Faint whispers rise from every shadow around the target, battering their mind with dread. Their fear
emboldens the user, whose attacks hit harder for a short time.

**Battle line:** %user lets their shadow stretch and thin, and soon every shadow around %target begins to whisper. The
voices come from everywhere and nowhere, faint at first, then crowding close until %target cannot tell them from their
own thoughts. The dread cuts at their mind like a cold blade, and every flinch only feeds %user's resolve. For a short
time, %user strikes with the confidence of one who knows their enemy is already afraid.

## 7. Body Flicker (`y39RtS7NN7TdqOgyT52gr`)

*Live:* empty ground, range 5, area circle at the landing point, 60 AP, cooldown 5: move, ninjutsu damage in the area.
*Old:* battle line says "the enemies around them", which is dead text when nobody is there.

**Description:** The user vanishes in a flicker of speed and reappears at a chosen spot on the field. Their arrival bursts
outward in a ring of chakra that strikes the ground around them.

**Battle line:** %user vanishes in a swirl of leaves, so fast that the eye catches only the afterimage left behind. A
heartbeat later they reappear across the field, landing in a crouch as the leaves settle. The force of their arrival
bursts outward in a ring of chakra, slamming into everything caught around the landing point. By the time the dust
clears, %user is already looking for the next opening.

## 8. Terra Shift (`CLlN7iJPGCGRIDbJTo4P5`)

*Live:* empty ground, range 5, area circle, 60 AP, cooldown 7: earth damage in the area, move; user takes 15% less
damage, 2 rounds.
*Old:* battle line is six sentences and places the protection underground, not after the user resurfaces.

**Description:** The user sinks into the earth and bursts out at a new position, hurling stone across the ground around
them. A crust of rock clings to their body afterward, blunting incoming blows for a short time.

**Battle line:** %user presses their chakra into the ground and sinks beneath it as easily as stepping into water, leaving
only a ripple of soil behind. The earth carries them unseen across the battlefield, then erupts as they burst out in a
spray of shattered stone. The shockwave tears outward through the surrounding ground, battering everything caught in the
blast. As the dust settles, a crust of living rock clings to %user's skin, turning aside the blows that follow.

## 9. Crescent Strike (`sER45bYNHRP6GDk7Zl2Ez`)

*Live:* empty ground, range 5, area circle, 60 AP, cooldown 5: move, bukijutsu damage in the area.
*Old:* battle line says "the enemies around them".

**Description:** The user darts to a chosen spot and sweeps their blade in a wide arc shaped like the crescent moon. The
cut tears through everything around the landing point.

**Battle line:** %user disappears in a flash of steel and reappears with their blade already drawn, moonlight running
along its edge. In a single turning motion they sweep it through a wide silver arc, a perfect crescent hanging in the air
for a heartbeat. The cut tears through everything caught within its reach before the blade returns to its sheath. Only
the fading crescent in the air shows where the strike passed.

## 10. Rotting Bite (`69LbdTR46ecbDsKoP0Lsy`)

*Live:* target, range 4, 60 AP, cooldown 5: damage; user lifesteal 20%, 2 rounds.
*Old:* battle line names the mechanic ("activating lifesteal").

**Description:** The user sinks phantom fangs into the target, and rot creeps outward from the bite. The decay feeds the
user, letting them heal from a share of the damage they deal for a short time.

**Battle line:** %user lunges, and a set of phantom fangs flashes out of the dark to sink deep into %target. Where they bite,
a creeping rot spreads beneath the skin in blackening veins of sickly green. The decay feeds on %target's strength and
pours it back into %user, who grows stronger with every wound they open. For a short time, each strike %user lands draws
life from the rot.
