# Old Ghost - prose pass proposal

Record read from `tnr_results_1788135094828`. 45 nodes, 29 dialog, three routes converging.
Nothing is written yet; this is for markup.

Mechanical sweep first, so it is off the table: **no em dashes**, and the pronoun rulings
already hold - the officer is `she` throughout g32-g35, Old Ghost is `he` everywhere else.
No empty descriptions, no placeholder text. The coworker's mechanical list is already clean,
so what follows is editorial.

---

## 1. g30 names three endings at once (the real problem)

g30 is where **all three routes converge** - `g16 -> g30`, `g24 -> g30`, `g31 -> g30`. Its text:

> Alone at the foot of the wall, with the two he left behind still in a lane on the other
> side of the slope.
>
> Three down in a dye works yard. He waited for the other two to commit before he moved
> once, which is how he has stayed in that Bingo Book.
>
> He is down at the verge with his business already concluded and nothing on him to show
> what it was.

Those are three different endings. "The foot of the wall" and "two left behind in a lane"
is the **stakeout** route. "Three down in a dye works yard" is the **contact** route. "Down
at the verge" is the **ask-around** route. On any single playthrough two of the three are
false, and the player just fought the one they can check.

### Option A - split g30 into three route-specific nodes (recommended)

Costs two extra nodes and no engine work; each battle node already points somewhere.
`g16 -> g30a`, `g24 -> g30b`, `g31 -> g30c`, and all three carry the same closing beat and
the same single choice out to g32.

**g30a** (ask-around route, east verge, caught him leaving)

> He is down at the verge with his business already concluded and nothing on him to show
> what it was.
>
> He was finished by noon. You spent the day walking, and he let you.
>
> You file it that night. Old Ghost. Bingo Book entry. Taken inside the village.

**g30b** (contact route, dye works, three down)

> Three down in a dye works yard, and the lights still on in a building with no reason to
> have them.
>
> He waited for the other two to commit before he moved once, which is how he has stayed in
> that Bingo Book.
>
> You file it that night. Old Ghost. Bingo Book entry. Taken inside the village.

**g30c** (stakeout route, foot of the wall, ran him down)

> Alone at the foot of the wall, with the two he left behind still in a lane on the other
> side of the slope.
>
> He ran out of village before he ran out of breath, and he never once looked back at them.
>
> You file it that night. Old Ghost. Bingo Book entry. Taken inside the village.

### Option B - make g30 route-neutral (one node, no new nodes)

Cheaper, and loses the specificity that makes the three routes feel different.

> It is over, and there is nothing on him to show what he was doing here.
>
> He moved once, at the moment he had to, which is how he has stayed in that Bingo Book as
> long as he has.
>
> You file it that night. Old Ghost. Bingo Book entry. Taken inside the village.

---

## 2. g35 closing line is repeated verbatim by its own exit choice

g35 ends with:

> "That is all you get. The entry stays open. It always does."

and the only choice out of g35 is labelled **"The entry stays open. It always does."** The
player reads the same sentence twice in a row, once as her line and once as their own.

Proposed choice text: **"Take the pay."** - which also matches g36's exit and lands the
same beat without the echo.

---

## 3. g33 and g34 share a sentence

- g33: "She signs it and does not close the entry."
- g34: "She signs it without another word and does not close the entry."

They are exclusive branches so no player sees both, but g34 is the *say nothing* branch and
would read better without borrowing g33's phrasing.

Proposed g34:

> The pen moves. She does not look up while it does, and the entry is still open when she
> sets it down.
>
> When you are at the door she says it to your back.
>
> "Many have reported the same. Myself included."

---

## 4. g15 pronoun tangle

> By dusk you have four addresses, three of them empty and the fourth a woman who has never
> heard the name. But the fourth one flinched.
>
> She flinched at the name, not at you.
>
> Whoever he saw today, he saw them here, and he has already finished.

Four pronoun referents in three lines - the woman, the player, Old Ghost, and whoever he
met. "Whoever he saw today, he saw them here" is the sentence that has to be read twice.

Proposed:

> By dusk you have four addresses. Three are empty. The fourth is a woman who has never
> heard the name, and who flinched when she heard it anyway.
>
> Not at you. At the name.
>
> Whoever he came to meet, he met them on this street, and he is already done.

---

## Not changing

- **g14** "You spend the afternoon walking in a circle somebody drew for you." Best line in
  the quest.
- **g8** "four descriptions of four different men, and the last one is you."
- **g_win** "Report filed. Entry open." Two sentences, correct weight.
- The three dead-end routes off g4 (walls, market, alleys). They cost the player a day and
  say so, which is the point.

---

## Open, not mine to settle

- The **Bingo Book ruling** on the board is still open and g2/g3/g30 all lean on it.
- **g30 silent portrait** was ruled per node in the art micro-rulings; Option A would need
  that ruling applied to three nodes instead of one.
