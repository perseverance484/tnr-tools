# The Tenth Name - you are the tenth name

Ruled: C, mixed with A. Ten names, nine of them unfindable, and the tenth is yours.

My objection to C on its own was that it puts the officer under suspicion and breaks her for
every other quest in the set. Mixing A fixes that, on one condition: **the officer is not the
desk.** She hands you the page *because* your number is on it. That is the whole reason she
gives you the mission instead of filing it, and it makes her the most trustworthy person in
the set rather than the least.

---

## The premise

The page lists ten service numbers. Nine are struck through. The tenth is yours, with a date
eight months out.

You go looking for the nine. **You cannot find any of them.** Not bodies, not desertion
notices, not graves. A transfer that was never received. A discharge signed by an office that
has no record of signing it. A name three people remember and no ledger does. They were not
killed. They were **closed** - each one written out through a different department, in
ordinary paperwork, by nine different clerks who each did one small correct thing.

## What you are proving, and why it does not work

The turn is the answer to "innocent of what."

Somewhere upstream, a leak was found. The desk handling it did not look for who leaked. It
listed everyone who **could have** - everyone with the access - and began closing them, one at
a time, in the order the list is written. Nine are done. The date beside your number is when
they reach you.

So the nine had nothing in common except access. And that is the bleak part: **they were
innocent too.** Proving you did not do it clears you of a charge nobody ever made. There is no
tribunal, no accusation, no file with your name on a crime. There is a list, and a schedule.

That is the anime turn: the player spends the whole mission assembling a defence, and walks
into act 4 realising there was never a court.

## Why the nine cannot be found - the mechanic, three flavours

Each investigated name gives one fact, and the facts escalate:

1. **The transfer.** Sent to a village that never received her. Both ledgers are correct. The
   gap is between them, which is nobody's department.
2. **The discharge.** Signed, stamped, filed. The signing office says the seal is theirs and
   the signature is not, and produces a register showing they were closed that week.
3. **The debt.** Died over eleven ryo, everyone agrees, nobody witnessed. His debt was settled
   a week later by someone who left no name - the only *generous* thing on the list, and the
   one that tells you it is being managed, not committed.

Three facts, three offices, and every one of those offices reports to the same desk.

---

## Node outline - 20 nodes, two dead ends

**Act 1 - the page (4)**

1. `t1` A dead courier nobody has claimed. In the coat, folded twice, a page of ten service
   numbers. Nine struck through.
2. `t2` The officer reads down the page. She stops at the tenth. *"That is yours."*
3. `t3` She does not file it. She gives it to you, which is not procedure, and says so.
   *"You have eight months and I have a desk I cannot ask questions of. Go and find out what
   happened to the nine."*
4. `t4` Choice of where to start. Three of the nine are close enough to walk to.

**Act 2 - the nine (8, two dead ends)**

5. `t5` **The transfer.** The records window, and the gap between two correct ledgers.
6. `t6` [dead end] **The barracks.** Four people remember serving with the second name. None
   of them remember when he left, and one of them is sure he is still here.
7. `t7` **The discharge.** The signing office, the seal that is theirs, the signature that is
   not.
8. `t8` [dead end] **The grave.** There is a stone with the fifth name on it. There is nothing
   under it. The groundsman has done this before and does not want to talk about it.
9. `t9` **The debt.** The moneylender's back room, and the settled account with no name on it.
10. `t10` [collect] The ninth name is three weeks old, the freshest of them. You go through
    what he left behind before somebody else does.
11. `t11` [fight] Two arrive for the same box. Their kit is ours. Their marks are ours.
12. `t12` One of them is carrying the same page. Yours is not the only copy, and on his, the
    tenth line is already struck through.

**Act 3 - the pattern (4)**

13. `t13` Nine closures, nine departments, nine reasons, no two alike. Coincidence does not
    vary that carefully.
14. `t14` Every one of those offices reports to the same desk. The list was never stolen. It
    was **issued.**
15. `t15` You find what the nine had in common, and it is the worst possible answer: access.
    Same clearance, same window, same three months. Not one of them is accused of anything.
16. `t16` **There is no charge.** Nobody is looking for who leaked. Somebody is closing
    everyone who could have, in the order written, and you are tenth because you are tenth.

**Act 4 - eight months (4)**

17. `t17` [travel] Back to the officer with a defence you no longer have anywhere to file.
18. `t18` She has the same realisation one beat behind you and does not soften it.
    *"I can protect you from an accusation. There is not one."*
19. `t19` **The choice.**
    - **Take yourself off the list.** There is one way: give the desk a better candidate. You
      have three months of access records and you know exactly whose name fits. She will not
      stop you and she will not look at you afterwards.
    - **Take the page public.** Nine closures become nine questions somebody upstairs has to
      answer. The desk survives it - desks do - but the schedule stops while it does. You are
      now the visible one, which is its own eight months.
    - **Do nothing and keep working.** The date holds. You have eight months, and the quest
      ends with you knowing exactly how many.
20. `t_win` One closing beat per choice, three lines. The page goes in your coat, not a
    drawer.

Two fights, two dead ends that sting, three escalating investigation scenes, one pattern, one
turn where the defence evaporates, and three endings that are all costs.

---

## Risks worth naming

- **The antagonist is the village's own administration.** That is the point, and it is also a
  set-level tone call that is not mine to make. If the content admin wants the rot located
  outside the village, the desk can be a foreign hand *inside* an office, which weakens the
  turn but keeps the shape.
- **The player's service number.** Quest text addresses "you" throughout, so no per-player
  data is needed - the page simply reads as the player's. Nothing engine-side required.
- **Ending 1 is dark.** Naming somebody else to save yourself is the strongest ending and the
  one most likely to need a look before it ships.

## Needed from you

1. **Does the desk stay inside the village**, or is it a foreign hand working through our
   offices?
2. **Ending 1** - does it stay as written?
3. `push/35` stays held and gets discarded when this is written.
