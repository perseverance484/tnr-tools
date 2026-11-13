# Skyglass end-to-end run (job 591, v2) — dauntless, 2026-11-13 (UTC)

Contract: `state/prompt_skyglass_e2e_run.md` (v2). Staff test mode on hidden content, played by hand through the TNR
connector only, PvE loadouts (`w6SGSCzCfnyzAhqKebKzI` / `q94r_70pLKJjXfRTc6OBp`), no auto-combat, no content or
staff endpoints. Learned each fight from quest text, dialog and battle state. Run lock held as `player` 09:34–11:15.

## Go-live table

| Piece | Verdict | Why (one line) | Battle id(s) |
|---|---|---|---|
| The Whole Wreck (walk-through) | **ready** | Every dialog, branch and hand-over works; all six deep charts, the Closing Hold chart, Lantern and four shards arrived as described. | cQDfvaW4CWyyRR8VHJsW5 … 8uY8Wr-BvaWnvC44vXfP5 |
| Wreck deck 1–3, deck 5 wave 1 (inside walk-through) | **ready** | All won solo with readable kits (Seal Charge rupture, Chain Hook, Raijin's Spear, Chart Mark, Keelbind). | _D8OjY56xflavJZ9bpaZz, 220Sph5oGt9TbDOJUo0ye, kRcZsWoQc845pEABJY5GP, vqO5YecgwAyriFHxgN3UD |
| Core Horror (walk-through) | ready (party content) | Omen → Eruption one-shot me for 12,440 on marked ground; a lesson, not a bug. Tuned for three; salvager warns solo will lose. | V4aAiCCpVG1L8H-XPjYqa (loss R2) |
| Captain + Sealwright (walk-through) | ready (party content) | Clear "kill the healer" puzzle (Mending Seal heals 9,090 + 80% ward); solo is a chain-stun loss, as warned. | pDuzDo76aDbWKe-bgAXle (loss R5) |
| Driftline Captain (walk-through only) | **fix first** | Won solo, but it was a mutual kill: -60 AP stun 3r + bloodline seal locks every 60-AP jutsu, then Counter Stance reflected 972 and killed me with my own finishing blow. This is the 30–80 band's final boss. | ummLudyvcT46QNzZ55dNF |
| Crowned Captain (walk-through) | **fix first** | Won R17 only because from ~R9 the boss went fully passive ("stands and does nothing") for 8 rounds, even while in its final-stand enrage. Possible AI stall. | 8uY8Wr-BvaWnvC44vXfP5 |
| Salvager's thread: Wreck Sighted | **blocked** | "Must be in your allied village to start quest" from Hyorin (sector 177, my village). | — |
| Salvager's thread: At the Salvager's Fire | **blocked** | Same message, yet `quests.allianceBuilding` lists the Fire for Hyorin lvl 100. It's listed but you can't start it. | — |
| Trade: Deck Charts | **ready** | Entry 4 salvage, husk fight, choice of 4 charts (took Rotted Galley). | wN4_3vRHxgPaoRC3yXx0d |
| Trade: Hold Charts | **ready** | Entry 10, husk, choice of 5 (took Glass Nursery). | JvBX0j1TZOKExFgHvjmo2 |
| Trade: A Sealed Chart | blocked (my salvage) | "You need 20× Wreck Salvage in your inventory to enter." The gate works; the trade itself is untested. | — |
| Trade: The Lantern | **ready** | Entry 30, husk, Lantern given; 2nd start refused: "Quest limit for this period reached". The weekly limit holds. | X6Hy0SkgGQQ31TJDTMLi9 |
| Chart: The Spoiled Hold | blocked (no chart) | "You need 1× Chart of the Spoiled Hold, 2× Core Rot in your inventory to enter." | — |
| Chart: The Rotted Galley | **ready** | 3/3 won; trivially easy at lvl 100 (one-shots). Reward choice has no salvage. | h2X88T0rhzOQoQ8n_hXD1, -pSdDXbNTNJBoncJmC63L, dyDOa8BOAl8L5VVJiOfuv |
| Chart: The Glass Nursery | **ready** | 2/2 won; good omen design (Fanned Lines / Cracking Ring / Seal Cross) and strong text; Lingering Echoes passive apart from omens. | xfrtydYgUojFGMUwwG97n, kouPKk-B0XzGnrWdPvpGk |
| The Closing Hold (Hullbound Mender) | **ready** | 3/3 won; the best fight of the day. Planks, port/starboard splits and a hold that shrinks for good are all telegraphed and readable. Check the drop rate (3 rare drops in one run). | OkveNxs8fr_TR8HaCeAJk, I650N4hp2KU6QfhOJNK-V, 08O2jRzuMavIkactiKMvG |
| Driftline: Into the Driftline / Beachcombing / Tally / Split Hold / Broken Stern | blocked (by design) | "Quest is only available up to level 80" / "complete the prerequisite quest first". Needs a 30–80 tester. | — |
| Mother of Echoes (Practice) Act I | **ready** | Won R12, 0 omen damage; Refraction/Facet lines, Cradle-while-Feeler, Hush pools all readable. | cpyB1Zsjfd2NMImqu_TZQ |
| Mother of Echoes (Practice) Act II | **ready** | Won R9, ~0 damage taken; the etching → recast → "guard open" memory loop is excellent. | isTuDgApEvHsheUJx_B1X |
| Mother of Echoes (Practice) Act III | **fix first** | Won R17 (4,133 HP / 595 CP left). Fix: a raw `%target` placeholder in "Hold Still" text, and the Practice ends with a **real** reward choice (Crown's Hoard LEGENDARY / 5 Coffers / 3 Tokens). Left unclaimed. | 671wW9Pb_u9_4jZTEpSJ_ |

## For the director: the three things most worth fixing before tonight

1. **The Mother of Echoes (Practice) pays a real endgame reward choice.** It needs no shards and says "Try again
   whenever you like", but clearing it offers Crown's Hoard (LEGENDARY) / Skyglass Coffer ×5 (EPIC) / Skyglass
   Token ×3 (LEGENDARY). If it goes live like that, anyone can farm it. Either keep the Practice hidden or remove its
   reward. I left the choice unclaimed on the account.
2. **The Captain kit in the solo 30–80 band (Driftline Captain), and the Crowned Captain AI stall.** A -60 AP stun
   for 3 rounds plus a bloodline seal turns off every 60-AP jutsu (almost all of a PvE kit). Counter Stance (35%
   reflect) then lets the winning hit kill the player. I won by mutual kill at level 100, so a level 30–80 player
   will find it swingy or impossible. Separately, the Crowned Captain stopped acting for 8+ rounds after its summon
   expired, including during its final stand. Check that AI before release.
3. **The Salvager's thread can't be started from home.** Wreck Sighted and At the Salvager's Fire both return "Must be in
   your allied village to start quest" from the account's own village (Hyorin, sector 177), although the Fire is
   listed by the alliance building there. If they only start from Wake Island or sector 210, the quest text should
   say so. Right now a new player has no path into the event from the board.

Also: the `%target` text placeholder in Act III "Hold Still"; Rotted Galley's reward choice has no Wreck Salvage,
although the salvager says runs pay salvage; the Closing Hold gave Lantern + Sealed Treasury + Shard of the Keel in
one clear (check the drop chances).

## Time (UTC)

| Step | Start–end | Notes |
|---|---|---|
| Setup (sync, lock, wake, loadouts) | 09:33–09:35 | Local clone was stale/diverged; reset to origin/main (backup branch kept locally). |
| 1 The Whole Wreck | 09:35–10:12 | 10 fights (7 W, 3 L by design/solo); Crowned Captain fight ~30 min alone. |
| 3 Trades | 10:12–10:40 | Includes a TNR connector credential outage ~10:20–10:34 (every call: "A credential for this connector could not be obtained"). |
| 4 Charts | 10:41–10:47 | Rotted Galley 3/3, Glass Nursery 2/2. |
| 5 Closing Hold | 10:48–10:54 | 3/3. |
| 6 Driftline / 2 thread | 10:55–10:57 | All blocked (see table). |
| 7 Mother practice | 10:58–11:14 | 3 acts, first attempt, no retries. |
| Finish | 11:14–11:15 | Potion, ramen, PvP loadouts, 4,550 energy → intelligence (+549.9), asleep, lock released. |
| **Total** | **09:33–11:15 (1 h 42 m)** | |

## Rewards and costs

- **Handed over by the walk-through:** Tide Chart; 30 Wreck Salvage; Chart of the Captain's Watch, Quarantined Archive,
  Buried Cache, Drowned Foundry, The Last Heading, Reliquary Seal; Chart of the Closing Hold; the four Shards (Crown,
  Ledger, Tide, Keel); Lastlight Lantern; 100 energy on completion. Inventory now holds 4 Lanterns (1 old +
  walk-through + trade + Closing Hold drop).
- **Trades:** −44 Wreck Salvage (4 + 10 + 30) → Chart of the Rotted Galley, Chart of the Glass Nursery, Lastlight
  Lantern. Charts spent: Rotted Galley, Glass Nursery, Closing Hold.
- **Chart/boss rewards claimed** (choices a player could earn): Medicine Inro (Galley); Skyglass Token ×2 (Nursery);
  Closing Hold drops Lastlight Lantern + Sealed Treasury + Shard of the Keel, choice Skyglass Token ×2 + Skyglass
  Coffer ×2. **Not claimed:** Mother Practice choice (see fix 1). Director decides what to do with the kept rewards
  (player brief 5.3).
- **Ryo:** 9,617,425 → 9,685,562 (+68,137). Ramen 2× large.
- **Potions:** 13 Full Potions (92 → 79). Full Potion heals a flat ~2,525, not "to full", so going from 0 takes two.
- **Durability:** no worn item broken; Aetherion (Captain's Decree) 97 → 34, Kitsune pieces 100 → 94. No repairs.

## Findings (with evidence)

**Bugs / likely bugs**
- Mother Practice ends with a real reward choice (questId `YDmKO6fp2vBRnTf7fHWQZ`, `getPendingRewardChoices`: Crown's
  Hoard / Skyglass Coffer ×5 / Skyglass Token ×3). Unclaimed.
- Act III battle text: "Hold Still: … The glass either side of %target goes quiet." (battle 671wW9Pb_u9_4jZTEpSJ_, R7).
- Crowned Captain (and the Lingering Echoes in the Glass Nursery) "stands and does nothing" every turn for long
  stretches. The Crowned Captain did this from R9 to R17, final stand included (battle 8uY8Wr-BvaWnvC44vXfP5).
- Wreck Sighted / At the Salvager's Fire: "Must be in your allied village to start quest" from Hyorin 177, though
  the Fire appears in `quests.allianceBuilding` for Hyorin.
- Battle round timer: polling between actions sometimes moved the version on and cost a whole turn ("Battle state
  changed. Choose your action again."). Twice in the Mother practice, once in the first fight.

**Balance**
- Rotted Galley, Wreck decks 1–3/5a and Closing Hold adds are trivially easy for a level-100 Kitsune-geared player
  (Thunderbolt 5,447 one-shots a 5,050 chart enemy). Mender and Sayo use heavy damage reduction instead, so hits
  land at ~700–1,100 outside their openings.
- Mother practice is mechanically rich but not brutal for this account: I never dropped below 4,100 HP, and the real
  pressure was chakra (2,631 → 595 CP in Act III). Max-pool gear (+700 HP at battle start) tops HP back up each act,
  so "HP carries" barely bites for this gear.
- Captain-type stuns (Final Command, Command Absolute, Extermination Order) seal elemental 60-AP jutsu and add AP
  tax. A kit built on 60-AP jutsu is near-helpless for 2–3 rounds at a time. Fine for party content, harsh for the
  solo Driftline Captain.
- Counter Stance (35% reflect) punished my big hits: 2,013 reflected from a 5,753 Rebirth, and 972 from the
  finishing Thunderbolt that killed me.

**Confusion / text**
- The salvager's line "runs pay salvage" doesn't match the Rotted Galley choice (Galley Stores / Medicine Inro /
  Buried Cache).
- Every trade starts with a husk fight. It's fine flavour, but it adds friction to what is a shop action.
- The walk-through dialog `d_s7` "Move on" skips the Mender fight without saying it is the new boss; I missed it there
  and played the Closing Hold standalone instead.
- The 'three refused' safe hexes ((6,2), (5,5), (6,8)) are shown only by their absence from a full-board mark, which
  is hard to read without the battle view. In the browser, check that they visibly stand out.

## The Mother of Echoes (practice, first attempt, all three acts)

| Act | Result | Round | What mattered | Omens that read well |
|---|---|---|---|---|
| I — The Glasswright and the Deep | Win | R12 | Kill the Feeler first (Cradle −90% while it lives), then Sayo, then the Silence before Unbridled pools and a Feeler every round pile up. | Refraction / Facet lines a turn early; Stillness ring; Hush pools. |
| II — The Stilling | Win | R9 | Remember the etched zones (Rime north, Ember south, Seam west), stand in the middle band, burst during "Recast … her guard hangs open" (3–4× damage: StunJab 4,066, Tomb 3,225 + wound). | All etchings and recasts. Best mechanic of the run. |
| III — A Good Impression | Win | R17 | Stay off Black Refraction lines; basic Clear shattered "The Silence Holds Her" once (then on cooldown); go to a 'refused' hex for Every Name Remembered; No One Will Be Mended blocks self-lifesteal buffs. Finished at 13 HP on her, then Aetherion. | Lines, Hold Still (minds where you'd go), Names flood. |

No retries needed. Visuals ignored as instructed (clips still 1×).

## Notes on run conditions

- No player attacks; PvP loadouts unused until the finish. No premium currency, sales or deletes. No staff/content
  endpoints called. I read quest dialog options and objective text through the quest records (what the logbook
  shows), never manifests or design docs.
- Ready content jobs 548/549 had been queued since 2026-11-09 and were already ready before this run (not "became
  ready"), so I did not pause for them.
- Connector outage 10:20–10:34: calls refused with a credential error, then service resumed with no action from me.
