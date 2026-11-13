# Skyglass end-to-end run: one agent plays the whole weekend release by hand

Job 591. Director 2026-11-13 09:23 UTC: "design a single run and assign our agent to play it end to end ... It will need
to use the PvE jutsu and item set and play intelligently." This brief is the contract for that run. It sits under
`state/prompt_playing_tnr.md` (the player brief) and CLAUDE.md; where they are stricter, they win.

## 1. What the run is for

Play this weekend's Skyglass release the way a dedicated level-100 player would, start to finish, on the director's
account **dauntless**, and report what a player meets: what works, what breaks, what confuses, how long it takes,
and what it pays. It replaces the director clicking through the release himself.

Two modes, kept apart (player brief section 5.3):

- **Player mode** for everything players can see this weekend (sections 3.1-3.6). Use only what the account sees in
  game: quest text, dialog, battle state, inventory, the Discord-style in-game thread. Do not read this repository's
  design docs, manifests, specs or generated data while playing, and do not use content endpoints. A player would not
  know them.
- **Staff test mode** for the hidden Mother of Echoes practice quest (section 3.7). Hidden content is staff testing,
  not play. Still played by hand.

## 2. Setup (once, before any fight)

1. Clone or pull `perseverance484/tnr-tools` (main). Read CLAUDE.md, `state/prompt_playing_tnr.md` sections 1, 4.5
   and 5, `state/player/dauntless/pvp_playbook.md` "Loadouts by activity" and "Kit", and
   `state/player/dauntless/combat_notes_live.md`.
2. Run lock: `node forge/tools/run_lock.mjs claim --holder player --job "591 Skyglass e2e run" --ttl 60 --wait`.
   Heartbeat it at least every 30 minutes (`node forge/tools/run_lock.mjs heartbeat --token <token>`), and release
   it at the end. If another holder has it, wait; never take it over. If a content job becomes ready in
   `state/run_queue.json`, finish the current fight, then pause and release (player brief 4.5).
3. Use only the TNR connector (`mcp__Tnr__*`). No browser. No chat or messages. Pace at about 12 calls a minute.
4. Loadouts: `jutsu.selectJutsuLoadout {id: "w6SGSCzCfnyzAhqKebKzI"}` (PvE, the set with the PvE-only jutsu) and
   `item.selectItemLoadout {id: "q94r_70pLKJjXfRTc6OBp"}` (PvE, the Kitsune set). Read both back.
5. Gear and pools: no worn piece may be broken (worn is fine). Repair anything at 0 durability. HP full: a Full
   Potion (`item.consume`, user item `ZlMNc0o96Y_aIai3E8Q-U` or the current stack) straight after every fight; ramen
   for chakra and stamina. Note how many potions and how much ryo the run uses.

## 3. The route (in this order; record each step)

The release opens Friday 6 PM Central (Saturday 00:00 UTC): the scheduled release reopens both Wrecks and page 2
opens. Check both are live before starting; if not, stop and report.

1. **Wreck Sighted** (event quest `_zp1l7Y9a_77pgonAdsYx`, visible). If not done, play it through. If done, read it
   as a new player would and note whether it explains the event (director's onboarding goal).
2. **The Watch Log: The Rotted Heading** (page 2, `V-i3ZcAqPu0hB3G9IEzGo`, open Sat-Mon). Start it. Its five
   challenges are wins on chart runs. Work out from the page and the game alone which charts you need and how to get
   them.
3. **Faded Skyglass Wreck** (dungeon `j4QEUtjbK_lbOYUPVoidk`, level 30): one full clear, all floors, solo (with 2
   pets if the account has them). Daily limit: one clear per day.
4. **Skyglass Wreck** (dungeon `RHqzYdY4EAQA9HwsBKWDS`, level 80): one full clear, all 5 floors, solo. Record every
   drop.
5. **Chart runs**: win each page 2 chart you can open with what you hold or can make by steeping (the page says, for
   example, The Rotted Heading comes from steeping The Last Heading with 3 Core Rot). Do not buy charts or Core Rot
   with premium currency. If a chart cannot be reached this weekend, record what is missing and how many Wreck clears
   or trades it would take.
6. **Claim** each completed page 2 challenge and record the rewards. Open any reward boxes a player would open.
7. **Staff test: The Mother of Echoes (Practice)** (`YDmKO6fp2vBRnTf7fHWQZ`, hidden). Play all three acts by hand,
   PvE loadouts. Health, chakra and stamina carry between acts with no refills: do not leave to heal. Learn her by
   playing: the omens (marked ground), where the safe hexes are, what each act punishes. She is meant to be brutal;
   a loss is a valid result. Record the round and the move that ended it. Her animations are mid-resize (most clips
   still at 1x, Stillness at 2.5x): ignore visuals, judge mechanics. Rewards: note them; the director decides what
   to do with them (player brief 5.3). Do not claim a reward choice from this quest.

Skip anything still hidden other than step 7 (the Salvager's trades and the new charts are not out this weekend).

## 4. How to play (by hand, every turn)

- **Always play it by hand.** Never auto-combat. Read the full battle state each turn, then choose.
- Each turn read: HP, chakra and stamina for every fighter; statuses and their rounds; marked or telegraphed hexes;
  your cooldowns and the enemy's; ranges; action points. Decide what the enemy is about to do from what you have seen
  it do.
- PvE priorities: stay alive (leave marked ground before it fires; heal before a big hit, not after), then remove the
  biggest threat, then damage. Use cleanses and barriers against the move you know is coming. Spend cooldowns where
  they change the outcome, not on the first turn by habit.
- Keep a short notebook per enemy as you learn it (what it opens with, its telegraph, its punish), and use it the next
  time you meet that enemy.
- **If attacked by a player** at any point outside an isolated battle: fight back with the PvP loadouts
  (`soXekhNjk7qihu-Rsok-6` / `B-bCCtg-_fvcJSrvR1ts0`), then switch back to PvE and carry on.
- Never flee to dodge a hard fight. Retry a lost battle at most twice (`quests.retryBattle` where the game offers it),
  changing the plan each time, then move on and record it.

## 5. Stop and report instead of acting when

- something would spend premium currency or real money, sell or delete a rare item, or leave the clan or village;
- a game response looks like a bug that could be exploited (report it, do not repeat it);
- the account is stuck (an isolated Battle Pyramid it cannot leave, a battle that will not end);
- any rule in `state/prompt_playing_tnr.md` section 5 applies.

## 6. Finish

1. PvP loadouts back on, Full Potion, then (if in home sector 177 and not in battle) spend energy over 500 on
   intelligence training and `home.toggleSleep` so the account is asleep. Release the lock.
2. Write `state/player/dauntless/sessions/<UTC date>_skyglass_e2e.md`:
   - **Result per step** (done / blocked and why), with battle ids;
   - **Time** per step and in total (UTC start and end);
   - **Rewards and costs**: drops, page rewards, ryo, potions, durability;
   - **Findings**, each with evidence (battle id or the response): bugs, balance (too hard, too easy, unrewarding),
     confusion points (what a player could not tell), text issues;
   - **The Mother of Echoes**: per act, the round reached, what killed you or how you won, and which omens read well
     or badly in mechanics;
   - **For the director**: the three things most worth fixing before next Friday.
3. Commit with message "player: Skyglass e2e run (591)" and push to main. Update job 591 in `state/run_queue.json`
   to done with a one-line result.
