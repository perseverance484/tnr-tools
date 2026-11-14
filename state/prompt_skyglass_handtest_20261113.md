# Skyglass hand tests before tonight's release (Fri 2026-11-13)

You are the TNR player agent on dauntless. Play by hand under the published rules and
`state/prompt_playing_tnr.md`. Read first: `state/player/dauntless/sessions/2026-11-13_skyglass_e2e.md`
(this morning's run) and `state/results/596_597_captain_stunprevent_and_core_rot_grant.md`.

Rules for this session:
- Take the run lock before you play and hold it with heartbeats: `node forge/tools/run_lock.mjs claim --holder player
  --job "skyglass hand tests 2026-11-13" --ttl 60`. Release it when you stop.
- Gameplay only. No content writes, no `item.adjustUserItem`, nothing from the never-list (payments, purchases,
  account deletion, other players, moderation, deletes).
- Do NOT claim the Mother of Echoes practice reward (questId `YDmKO6fp2vBRnTf7fHWQZ`). Leave it pending.
- Fight every battle by hand with the PvE jutsu and item set. Record battle ids.
- Everything is still hidden; the release is 6 PM CT. Stop by 5:15 PM CT whatever is left.

Start state (19:00 UTC): 48 Wreck Salvage, 1 Core Rot, 4 Lastlight Lanterns, 2 Charts of the Closing Hold.
The four Salvager's Trade quests are now Wake Island **event** quests (changed 18:32-18:54 UTC).

## Tests, in order

1. **Grant quest → Core Rot.** Start and finish `Salvage Swap Test: Grant` (x5-kg5W6sHoyXM8yJk-M4, hidden, mastery).
   Expect: 1 Core Rot (now 2). Record the start path and what it paid.
2. **Hold trade → Chart of the Spoiled Hold.** Start `The Salvager's Trade: Hold Charts` (7pk21EmBrmL_EyHuPK2Xp) at
   Wake Island. Entry 10 salvage, beat the husk, pick **Chart of the Spoiled Hold**. Record where it starts from,
   any "allied village" or location error word for word, salvage before/after.
3. **The Spoiled Hold** (iRMyb0WN_ip--EDbvAgLc): entry = the chart + 2 Core Rot. Play it through. At the rot wall,
   take **"burn the rot out"** (one more fight, 1 Core Rot back). Record: every fight (won/lost, rounds), the
   Core Rot refund, the chance drops and the reward pick offered (do pick, note what you took), clear time.
4. **Sealed trade** (`The Salvager's Trade: A Sealed Chart`, jUQYz9zyMdJIRdLbucYjm): entry 20 salvage, husk, pick a
   chart. Then try to start it a second time and record the refusal text (weekly limit check).
5. **Crowned Captain after the stun fix.** Spend 1 Lastlight Lantern on **Crownhold** (fqqpkcp_L4oOsC6yyodlk) and
   play it to the Captain. **Use Stunning Jab (or any stun) on him at least twice**, including once below 30% HP.
   Expect: the stun does not land ("stun prevented" or no stun), and he keeps casting omens, eruptions, Crownfall
   and Command Absolute instead of "stands and does nothing" for turns at a time. Record his turns from your stun
   onward, and the full battle id.
6. **Wreck Sighted / At the Salvager's Fire start path.** This morning both said "Must be in your allied village to
   start quest" from Hyorin 177. Try each from: your village's Administration Building, then Wake Island. Record which
   place works and the exact error elsewhere. Do not finish them if they would grant real rewards you did not have.

## Report

Write `state/player/dauntless/sessions/2026-11-13_skyglass_handtest.md`: a table (test, result: ready / fix first /
blocked, evidence ids), then the details per test, inventory before/after (salvage, Core Rot, Lanterns, charts),
and any bug word for word. Commit it to main with a short message and push. Then tell the director the table.
