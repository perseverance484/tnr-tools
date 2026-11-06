# Skyglass event: story audit against the Mother of Echoes reveal

**Status:** DECIDED 2026-11-05 (RUL-2026-11-05-117): every recommendation is approved, and the edits are applied in the generators and built as push/483–485. D2: the three who refused are the Worn. D3: Replicant Zero is renamed The First Impression. D4 is pending with main. D5 is done. The text below is the original review, kept as written. *Original status:* REVIEW ONLY (Lane B design text, 2026-11-05). Nothing in this file is applied. Every proposed line needs
the director's approval before a generator or manifest changes (CLAUDE.md §10). Zero live requests were made; no live
record was read or written. Base: `origin/main` at `6289a3e1`.

**The director's question:** "Let's analyze all pre-existing event dialog. Do we need to make any adjustments to make
the story flow well?"

**Short answer:** yes, but the changes are small. The event already tells a coherent story about the ship, the crew
and the Crowned Captain. What it lacks is any setup for the person the finale reveals. Before the Mother of Echoes, no
line names Sayo, a Glasswright, the Stilling or a siege. One live line also contradicts the reveal directly: Crownhold's
aftermath says the officers were "released at last". Ten one-line touches fix most of it (§5).

---

## 1. Method and sources

**What "live" means here.** No live capture of the Skyglass records exists for every surface, so live state is
reconstructed from the run records. Every `harvests/inbox/tnr_results_*.json` whose `journal.manifestPath` names a
Skyglass, Crownhold, Ghost Ship or Mother of Echoes manifest was read. For each record, the text kept is the text of
the **latest manifest that ran with a per-entry `verdict: match`**. Entries that errored, such as the Archive in 339,
fall back to the earlier matching send (382, then 385). Scripts are in the session scratchpad, not the repository.
Where a generator's current text differs from what ran, §2 says so.

**Sources used.**
- Canon and rulings:
  - `docs/RULINGS.md`: RUL-2026-11-01-093, -094 (Sayo, the Stilling, the Mother Glass), RUL-2026-11-03-111 (the
    Silence in her shadow), RUL-2026-10-29-057, RUL-2026-10-31-072/-074, RUL-2026-10-24-024 (old chests are relics),
    RUL-2026-10-23-003 (Ghost Ship quests retired), RUL-2026-10-29-041 (titles deferred).
  - `docs/design/SKYGLASS_STORY_BIBLE.md`.
  - `docs/design/ghost_ship_art_bible/ART_BIBLE.md` §1.
- Design text: `docs/design/SKYGLASS_TEXT.md`, `docs/design/MOTHER_OF_ECHOES_JUTSU_TEXT.md` (approved 2026-11-05),
  `docs/design/SKYGLASS_BOSS_FIGHTS.md`.
- Generators:
  - `push/mother_of_echoes.gen.py` (`Q_DESC`, `INTRO`, `DIALOG_OVERRIDES`, `F_LOST`).
  - `push/mother_of_echoes_text.json`.
  - `push/skyglass_uber_economy.gen.py` (`SHARDS`, `INVITE`, `TOKENS`).
  - `push/crownhold.gen.py`, which overrides `state/crownhold/package/state/silent_bastion_authoring/design/script.json`.
  - `state/skyglass_hunts/hunts.py` (Archive, Foundry, Watch).
  - `push/skyglass_update.gen.py`, `push/skyglass_items.gen.py`.
- Manifests that ran, read from `push/` and `archive/spent-manifests/`:
  - Ghost Ship: 90, 93, 94.
  - Hunts and Wreck: 260, 263, 265, 266, 268, 271, 272, 274.
  - Skyglass build: 319, 329, 339, 341, 342, 343, 344, 346, 348, 349, 354–358, 360, 361, 362–366, 368–371, 373, 374,
    381, 382, 383–385, 395, 400.
  - Uber economy: 417, 420.
  - Mother of Echoes: 440, 461–464, 466, 468, 469, 476, 481.
- Run records: every `harvests/inbox/tnr_results_*.json` with those manifest paths. The Mother of Echoes chain
  includes `tnr_results_1793719388089.json` (464), `1793846634826.json` (466), `1793925607180.json` (476) and
  `1793927673884.json` (481).
- Out of scope, because they are hidden or retired:
  - The two old Ghost Ship quests (90/93/94; hidden, RUL-2026-10-23-003). They still say "impression conduit" and
    "maintenance chamber", but players cannot see them.
  - The Skyglass Reliquary item, a relic by RUL-2026-10-24-024.

**Not found:** event announcement copy. No announcement or news-post text exists in the repository. The Skyglass
titles are deferred (RUL-2026-10-29-041), so none is live.

---

## 2. Live versus generator: where they differ

| Surface | Live now | Generator / approved doc | Consequence |
|---|---|---|---|
| **The Mother of Echoes** (main quest, hidden) | The 464 text: one opening dialog, "A woman in a glasswright's apron stands before it with her back to you. 'You came. Good. I was beginning to think I had measured you wrong.'" The old `d_act3` reads "The Silence has stopped holding back, and so has she." | `INTRO` (`d_intro1`, `d_intro2`), then the `DIALOG_OVERRIDES` `d_open` (shadow stands up) and `d_act3` (shadow folds back). The approved reveal. | **The reveal is live only on the Practice quest (481).** Go-live **477** must carry it to the main quest. Check it in 477's readback. |
| Mother of Echoes jutsu (55) | The 476 text (ran 2026-11-06 00:40Z) | `MOTHER_OF_ECHOES_JUTSU_TEXT.md`, approved later (commit 1b1b84f3); the generator now applies it | The approved hint-voice text is not live yet. It rides the next job. |
| Shards, Heartglass, The Remainder | 417 / 468 | Same as `skyglass_uber_economy.gen.py` | Match |
| Crownhold, hunts, chart runs, Haul, items | 385 / 383 / 384 / 420 / 368–371 / 395 | `crownhold.gen.py`, `hunts.py`, `SKYGLASS_TEXT.md` | Match on every line quoted below |
| Story bible | — | `SKYGLASS_STORY_BIBLE.md` has **no Sayo chapter**. RUL-094 names the bible as the canonical destination for "a new final chapter". The bible still says breaking the crown "frees every echo it holds", and its one-breath summary ends on "the man who never let any of them go". | Internal only, but every future text pass reads the bible first (recommendation 12) |
| Art bible §1 | — | "The Skyglass Project was a **secret shogunate programme**…" | Internal only. No player text says "shogun" (checked). Recommendation 12. |

---

## 3. The story as the player meets it

The order follows the chart chain (playthrough review: commons → Buried Cache → Foundry → Archive → Reliquary Seal; the
Watch → the Last Heading; Epic runs → Lantern → Crownhold; four shards → the Mother of Echoes). The Haul runs alongside
from page drops.

1. **Wreck Sighted** (348/385): a black ship that hung over the coast for decades has come down. Its crew are "still
   standing their watch". A salvager hands over a chart.
2. **The Skyglass Wreck** (dungeon, 362/366): the war-ship lies broken, "its Skyglass Core cracked and still burning".
   "Inside, the Core holds every deck the way it was … No one is relieved." The Captain makes his last stand in the
   battle log only.
3. **Low Tide Run / Night Watch** (354): the crew loop through their duties: a Deck Warden counting seal charges, the
   Arsenal Keeper logging stores that floated away. The Night Watch roster has "a new name: yours" in fresh ink, and a
   second line "in a hand you do not know". *(This is the best existing hint that someone is measuring the player,
   though it is not tied to anyone.)*
4. **The Buried Cache** (339/385): the crew were people. "For when we come home."
5. **The Drowned Foundry** (385): the Core grows skyglass that mends the hull, forever. The Arsenal Keeper's ledger
   reads "crew not relieved". The Foundry Warden says "The last pour is not finished."
6. **The Quarantined Archive** (385): the Sealwright's buried reports. The impressions are fraying ("men coming back as
   less each time"), and every request for rest is answered from **Crownhold** under the crown's seal: "Refused. None is
   relieved." The run ends on the name *Crownhold*.
7. **The Captain's Watch** (385): the Captain is someone else's echo. "The ship died once. The crown disagreed." "I wear
   his mask. He never trusted me with the rest."
8. **The Sealed Reliquary** (355): the echoes the Core could not hold. The Sealwright: "I sealed him in here for a
   reason. Then I sealed myself in after him."
9. **The Fall** (355): the night the ship came down, replayed. The Captain held "the heading straight into the shore,
   as he did that night".
10. **Rotted Reliquary / Burning Heading** (355): the rot's versions. The Captain helps you off the ship: "This time
    someone walks off."
11. **The Haul** (358): the crew's sealed stores and ledgers. The Sealwright's echo seals rooms.
12. **Crownhold** (Lantern; 420):
    - The fortress "that built the Skyglass Project and gave its crew their last order" has been silent "a generation".
    - The officers are impressions repeating their duties.
    - The "Skyglass Research Division" register lists researchers, smiths and officers, "each with a date and the word
      RECALLED".
    - Replicant Zero: "I was the first one *they* brought back. My body died in that jar. I did not."
    - The Honor Guard dates every true order "before the Silence".
    - The Crowned Captain: "Every officer you passed believes he is still serving. **I gave them that** … I built this
      command so it would outlast us."
    - Aftermath: the crown breaks, and "the officers … fade, **released at last**. Far away on the shore, the Skyglass
      wreck goes quiet: **its crew were his echoes too**." The directive is carved behind the throne, and the mission
      line is blank.
13. **The shards** (417, on drop):
    - Each is "a splinter of the Mother Glass". This is the first time the player sees the term.
    - Each carries "**Her** invitation", with no referent.
14. **The Mother of Echoes** (generator text, live on Practice only):
    - The shards "were an invitation".
    - Under Crownhold there is a hall of glass holding the faces of the Deck Warden, the Captain and the guards, eyes
      open.
    - She says: "Every one of them held still for me … The ship, the castle, all of it. I never lost them. I kept them
      … And you have been cutting them out of my glass, one by one."
    - Her shadow stands up (the Silence).
    - Act names: The Glasswright and the Deep; The Stilling; A Good Impression.
    - Ending: "For the first time since **the siege**, Crownhold makes a sound."

**Who did what, as the text stands before the finale:**
- The Skyglass Project at Crownhold grew skyglass and "recalled" the dead.
- The Crowned Captain gave the order and holds every echo through his crown.
- The Core rebuilds the crew.
- Crownhold "went silent" a generation ago, cause unstated.

**After the finale:** Sayo stilled them all and keeps them in the glass.

The two accounts can live together, because he commanded and she held. But only Crownhold's aftermath contradicts her
outright, and nothing points to her before the shards.

---

## 4. Findings

### 4.1 Contradictions with the reveal

| # | Where (live) | Text | Conflict |
|---|---|---|---|
| C1 | Crownhold `d.aftermath` (420; `push/crownhold.gen.py` l.359) | "the officers who still stood lower their blades and fade, released at last. Far away on the shore, the Skyglass wreck goes quiet: its crew were his echoes too." | Sayo: "I never lost them. I kept them." The faces are still in her glass. The narrator states as fact a release the finale takes back. "His echoes" also gives him the casting, which RUL-094 §3 gives to her. |
| C2 | Crownhold `d5.n.boss.clean` / `.alert` | "Every officer you passed believes he is still serving. I gave them that … I built this command so it would outlast us." | He claims to be the source. This is fine as his belief, since the bible makes him "certain", but nothing hints at the second will that RUL-094 §4 says contested hers. |
| C3 | Crownhold `d3.n.f2`, `d3.n.boss.clean` / `.alert` | Register "each with a date and the word RECALLED"; Replicant Zero "the first one they brought back" | The recall-over-years account. RUL-094 §3 fixes every afterimage at the instant of the Stilling, on one night. Reconcilable with small wording (R5, R6). |
| C4 | Crownhold `d4.n.f3` and the order puzzle | "Since the Silence fell over this mountain…"; "dated before/after the Silence" | "The Silence" names a *time* here (the bible's old usage). In the finale it is an *entity*. This is not wrong, and can be good foreshadowing if the line reads as something that arrived (R8). The puzzle text needs no change. |
| C5 | Shard of the Tide (417) | "washed out of the echoes the Core could not hold" | It drops from the Sealed and Rotted Reliquary **and** from The Fall and the Burning Heading. The story line fits only the first two. |

No player-facing text has a shogunate, a sealing of Crownhold by outsiders, or anyone else blamed for the stilling.
`shogun` returns no player text (checked); it appears only in the art bible.

### 4.2 Missing setup

| Gap | Evidence | Fix |
|---|---|---|
| **Sayo / the Glasswright** never appears before the finale | No live text before 417 contains `Sayo`, `Glasswright` or `Mother Glass` (checked over quests, items, jutsu). The new intro never names her in dialog either; the first name in dialog is `d_act2` ("Sayo wipes…"). The old 464 opening had "a glasswright's apron"; the new one dropped it. | R3, R4, R5 |
| **The siege** | The only mention before the finale is the Captain's "outlast any siege" (Watch). RUL-094's "last night of the siege" and `w_clear`'s "since the siege" have no setup. | R7 |
| **Stilling / holding still** | Already seeded, by accident: the Binder ("Hold still to be sealed"), the Oath of Stillness jutsu, and Sayo's "Hold still" in Act III and Refraction. | Keep. R6 sharpens it. |
| **The Mother Glass under Crownhold** | Crownhold says nothing about anything beneath it; the shard drop is the first hint. | R2 (the glass rings under the throne room) |
| **"The three who refused"** (the safe tiles, RUL-094 §5; jutsu text 440/466) | No surface says who they were. | Director decision D2 |
| **A second will contesting the crown** | Nothing hints at it. | R9 |
| **The ship was called home** (RUL-094 §4) | The Fall has the Captain steering into the shore, but nothing says why. | R10 |

### 4.3 Names in the reveal

- **The Deck Warden:** exists (Low Tide, Night Watch, Foundry, Fall, Cache, Wreck; AI `Deck Warden`).
- **The Captain:** exists (Wreck, Watch, Fall, Burning Heading).
- **"The guards you cut down":** generic, and that works (Honor Guard, Skyglass Sentinel, Trophy Warden, Stores Ward).
- **The Crowned Captain is not named in the hall.** He is the face the player broke most recently, since the Crown
  shard is a 100% Crownhold drop. Optional R11.
- **The Worn witnesses** (Cadet Tomo, Sister Hana, the Gate Porter) are new in the finale. As stilled Crownhold
  people they need no setup.

### 4.4 Voice and vocabulary (Edo fantasy, no technology words)

The story bible's banned list (system, network, lattice, interface, protocol, terminal, personnel, maintenance,
conduit, lift, reactor, data, scan, unit) was also checked for lab, relay, capacitor, prototype, research, division,
reconstruction, operation, interference, device, incident, manual, subject and containment.

| Live text | Where | Note |
|---|---|---|
| "The Skyglass **Research Division** is an archive hall"; "Above the **research division**" | Crownhold `d3.n.f1`, `d4.n.f1` | The most modern-sounding phrase in the event. R13a. |
| "Read the **suppressed incident reports**" (choice) | Archive `d_entry` (`hunts.py` l.31) | R13b |
| "as if from a **manual** worn thin with use" | Crownhold `d5.n.f3` | R13c |
| "**Replicant** Zero" (AI name, plaque, five objectives) | Crownhold; AI 272 | Sci-fi word. It is canon in the bible and on a live AI. D3. |
| Skyglass Katana: "the Captain's most faithful **reconstruction** … resist **interference**" | item (339) | Director-supplied text (RUL ~l.884/917). D4. |
| Skyglass Serum: "the Ghost Ship's longest chakra **operations**" | item (90, still live; Coffer drop) | Director-supplied. D4. |
| Unbroken Command: "their **reconstructed** form"; Core Rupture: "destroying the casting **device**" | jutsu (90) | The retheme text was accepted final (RUL-2026-10-12-008). D4. |
| Calibration Duelist, Prototype Lancer Unit, Unstable Echo Subject … | 272 AI names | **Not live:** 319 renamed all 18 to Crown Duelist, Crown Lancer, Crown Echo and the rest. Only Replicant Zero kept its name. |

**Not story, but player-visible:**
- **Echo of Erupting Ground** (342): its `description` is a designer note: "Shared pool record A3. Balance values
  pending sign-off. (Skyglass copy: damage hits enemies only.)"
- The Broadside, Command Absolute and Crownfall descriptions also read as notes: "Crowned Captain signature (Omen: Last
  Light, Binding) … +10 AP per action".
- Worth a text pass where enemy jutsu can be inspected.

---

## 5. Recommended adjustments (ranked by impact)

Each one is a proposal in the event's voice. **Approve** means the director accepts the line. The generator named
then changes, and a later push carries it.

**Timing (playthrough F05):** a re-send of a live run forces players who are mid-run to abandon. Apply chart-run,
hunt and Crownhold edits while the event is closed.

### R1. Ship the reveal to the main quest (process; highest impact)

- **Where:** go-live 477 (`push/mother_of_echoes.gen.py --step golive`).
- **Current live** (464, `d_open`): "Under Crownhold the Mother Glass is singing. A woman in a glasswright's apron
  stands before it with her back to you. 'You came. Good. I was beginning to think I had measured you wrong.'"
- **Required:**
  - `INTRO` (`d_intro1`, `d_intro2`) and `DIALOG_OVERRIDES` (`d_open`, `d_act3`) reach the main quest.
  - The approved jutsu text pass reaches all 55 jutsu.
- **Check:** the 477 readback shows `d_intro1` → `d_intro2` → `d_open` on The Mother of Echoes.
- **Why:** the approved reveal is live only on the Practice quest (481).

### R2. Crownhold aftermath: let the victory stand, but not the release

- **Where:** Crownhold `d.aftermath` (`push/crownhold.gen.py` l.359).
- **Current:** "The signal bells stop. Down every stair you climbed, the officers who still stood lower their blades
  and fade, released at last. Far away on the shore, the Skyglass wreck goes quiet: its crew were his echoes too."
- **Proposed:** "The signal bells stop. Down every stair you climbed, the officers who still stood lower their blades
  and fade. It looks like release. Far away on the shore, the Skyglass wreck goes quiet: its crew answered to his
  crown too.<br><br>Far beneath the throne room, glass rings once, like a struck bell, and is still."
- **Why:**
  - Removes the one statement the finale contradicts (C1). "Answered to his crown" keeps him the commander without
    making him the caster.
  - The ringing glass plants the Mother Glass under Crownhold at the exact moment the Shard of the Crown drops.

### R3. Name her in the reveal

- **Where:** Mother of Echoes `d_intro2` (`push/mother_of_echoes.gen.py` `INTRO`). Practice inherits it.
- **Current:** "… \"The ship, the castle, all of it. I never lost them. I kept them.\"<br><br>\"And you have been
  cutting them out of my glass, one by one. How interesting.\""
- **Proposed:** "… \"The ship, the castle, all of it. I never lost them. I kept them.\" She inclines her head, as if
  you had asked. \"Sayo. I grew the glass.\"<br><br>\"And you have been cutting them out of my glass, one by one. How
  interesting.\""
- **Why:**
  - Her name and role are otherwise first given in combat (the AI name) and then in `d_act2`.
  - The old opening's "glasswright's apron" was the only place the role was spoken.
  - Six words reveal who she is without exposition.

### R4. Seed the Glasswright in the Archive

- **Where:** The Quarantined Archive `d_records` (`state/skyglass_hunts/hunts.py`).
- **Current (end):** "… sent down from a fortress called Crownhold: 'Refused. None is relieved.'"
- **Proposed (append):** "<br><br>The last report is addressed to no officer, only to 'the Glasswright', and it was
  never sent. It asks one thing: who are they holding still for?"
- **Why:**
  - The Archive is the event's revelation room and the natural place for a second name.
  - It plants the role and the "holding still" motif three runs before Crownhold, without saying who she is.

### R5. Replicant Zero was brought back by someone

- **Where:** Crownhold `d3.n.boss.clean` and `d3.n.boss.alert`.
- **Current (both):** "I was the first one they brought back"
- **Proposed (both):** "I was the first one the Glasswright brought back"
- **Why:** puts the maker inside Crownhold (C3), so the finale's "she kept them" lands as a payoff, not a retcon.

### R6. The register: one night

- **Where:** Crownhold `d3.n.f2`.
- **Current:** "The register it carried lists names (Skyglass researchers, smiths, officers), each with a date and the
  word RECALLED."
- **Proposed:** "The register it carried lists names (Skyglass researchers, smiths, officers), each with a date and the
  word RECALLED. Most of the dates are the same night."
- **Why:**
  - Reconciles the recall account with the Stilling (C3).
  - Readers who notice will connect it to "the siege" (R7) and to the finale.
- **Optional, D2:** "Three names have no word beside them at all." This would seed "the three who refused".

### R7. Set up the siege

- **Where:** Crownhold `d4.n.f1` (`push/crownhold.gen.py` l.310).
- **Current:** "Above the research division, Crownhold becomes a war headquarters. Maps of borders that no longer
  exist cover the walls of High Command."
- **Proposed:** "Above the glass hall, Crownhold becomes a war headquarters. Maps of borders that no longer exist
  cover the walls of High Command, and on every one the same ring of enemy camps is drawn tight around this mountain."
- **Why:**
  - `w_clear` ("since the siege") and RUL-094 ("the last night of the siege") need a siege the player has seen.
  - "Glass hall" also replaces "research division" (R13a).

### R8. The Silence came up out of the mountain

- **Where:** Crownhold `d4.n.f3`.
- **Current:** "Since the Silence fell over this mountain, no true order has been issued from these halls,"
- **Proposed:** "Since the Silence came up out of the mountain, no true order has been issued from these halls,"
- **Why:**
  - Turns the old time-word into a hint of the entity (C4). RUL-094 §1 says the Silence woke "deep in the mountain".
  - The order puzzle's "dated before/after the Silence" still works unchanged.

### R9. A crack in the Crowned Captain's certainty

- **Where:** Crownhold `d5.n.boss.clean` and `d5.n.boss.alert`, after "…so it would outlast us." and "…to outlast us
  all." respectively.
- **Proposed (insert):** "He touches the crown, as if to quiet it. \"Some nights it does not answer me at once.\""
- **Why:**
  - RUL-094 §4 makes his afterimage the one will contesting hers. This is the only hint of that contest.
  - He stays certain (bible, Voice); the crown is what hesitates.

### R10. The ship was called home

- **Where:** The Fall `w_press` (chart-runs generator from `SKYGLASS_TEXT.md` §2.4; live 420).
- **Current:** "The Captain lets go of the wheel for the first time. \"Then it is done,\" he says, as the deck tips.
  \"It was done a long time ago.\""
- **Proposed:** "The Captain lets go of the wheel for the first time. \"Then it is done,\" he says, as the deck tips.
  \"We were called home. I only held the heading.\""
- **Why:**
  - RUL-094 §4: she called the ship home.
  - Ties to the Lantern ("points home") and the Wayfinder's "Still no home port".
  - This replaces a closing line listed in `SKYGLASS_TEXT.md` §6.2. Keep both sentences if the director prefers.

### R11. Shards: fix the Tide line, add one maker's mark

- **Where:** `push/skyglass_uber_economy.gen.py` `SHARDS` (live 417).
- **Shard of the Tide:**
  - Current: "A splinter of the Mother Glass, washed out of the echoes the Core could not hold."
  - Proposed: "A splinter of the Mother Glass, left behind by what the Core cannot let go: the reliquary's echoes, and
    the night of the fall."
- **All four,** append to the story line: " A small thumbprint is pressed into it, made while the glass was soft."
- **Why:**
  - Fixes C5, since the shard drops from both run families.
  - The thumbprint makes "Her invitation" point at a person, which pays off in `d_intro2`'s "Lovely, aren't they?"

### R12. Bring the internal canon up to date

- **`SKYGLASS_STORY_BIBLE.md`:** add RUL-094's final chapter (Sayo, the Mother Glass, the Stilling, the Silence in her
  shadow, the siege, the shards as her invitation).
  - Amend "Breaking the Command Crown frees every echo it holds" to "breaks the crown's hold. The echoes return to the
    Mother Glass, thinner (RUL-094 §3)".
  - Amend the one-breath summary's last line.
  - Add lab, relay, capacitor, research, division and reconstruction to the banned list.
- **Art bible §1:** "a secret shogunate programme" → "a secret programme of Crownhold's shinobi command". This matches
  the story bible and the director's no-shogunate framing.
- **Why:** every future text or art pass starts from these two files (story bible: "Where a surface disagrees with
  this file, the surface is rewritten"). The bible currently disagrees with the finale.

### R13. Vocabulary touch-ups (Claude-authored lines only)

- **a.** Crownhold `d3.n.f1`: "The Skyglass Research Division is an archive hall:" → "The Skyglass Project's glass
  hall is an archive:". For `d4.n.f1`, see R7.
- **b.** Archive `d_entry` choice: "Read the suppressed incident reports" → "Read the buried reports".
- **c.** Crownhold `d5.n.f3`: "as if from a manual worn thin with use" → "as if from a drill scroll worn thin with use".
- **d.** Echo of Erupting Ground `description` → "Calls the ground under the target up in a column of rock. An echo of
  the Stonebound's old technique; it strikes only enemies." This is a non-story fix (§4.4).

### R14. Optional: name both masks in the hall

- **Where:** Mother of Echoes `d_intro1`.
- **Current:** "The Deck Warden. The Captain. The guards you cut down."
- **Proposed:** "The Deck Warden. The Captain, twice: once bareheaded, once crowned. The guards you cut down."
- **Why:** puts the Crowned Captain, the last face the player broke, in her glass, and pays off the "I wear his mask"
  thread.

**Existing lines to keep:** these already serve the reveal.
- The Night Watch roster's "new name: yours" in fresh ink, and the second line "in a hand you do not know".
- The Binder: "Impressions never cast a shadow under the skyglass lantern … Hold still to be sealed". This pairs with
  her shadow that does not move.
- The Crown's Will: "Another echo come home."
- The Crownbreaker badge: "The throne is empty. The order still stands."
- The Remainder: "What the Silence did not finish drinking."

---

## 6. Decisions for the director

| # | Decision | Options and consequence |
|---|---|---|
| D1 | Approve R2–R11 and R13 (or a subset) | Each is one line in a named generator. R2, R5–R9 and R13 edit the live Crownhold quest. R4 and R13b edit the live Archive. R10 edits the live Fall. R11 edits four live shards. Each needs a push run outside event hours. R3 and R14 ride go-live 477 at no extra cost. |
| D2 | **Who are "the three who refused"?** | (a) Leave them mythic: the safe tiles explain themselves in the fight. (b) Seed them with R6's optional line ("Three names have no word beside them at all."), which keeps them unnamed. (c) Name them, for example as three Crownhold officers. That is new canon and needs a ruling. |
| D3 | **Replicant Zero's name** | Keep it (canon in the bible, a live AI, five objectives and a plaque), or rename it in the Edo voice (for example "The First Return"). A rename touches the AI username, the Crownhold text and the bible. |
| D4 | **Director-owned item and jutsu text** with technology words: the Skyglass Katana ("reconstruction", "interference"), the Skyglass Serum ("chakra operations"), Unbroken Command ("reconstructed form") and Core Rupture ("casting device") | These texts are director-supplied or accepted-final (RUL ~l.884/917, RUL-2026-10-12-008), so no rewrite is drafted here. Say if you want one. |
| D5 | Whether the story bible and art bible updates in R12 may be written by Claude from RUL-094/-111 | They are doc-only and change no records. |

---

## 7. Boundaries

- Review only. No generator, manifest or canon doc changed. This file is the only addition.
- Zero live-game requests; no credentials; no records read live or written.
- Live state is reconstructed from run records as described in §1, not from a fresh capture. A fresh read-only capture
  before any edit push is advisable for Crownhold and the Archive, which were last re-sent by 420 and 385.
- Not checked: battle-log lines of the Wreck's crew jutsu beyond the story-bearing set in §4.4, the Haul's hazard
  lines (story-neutral), and the profession chest contents.
