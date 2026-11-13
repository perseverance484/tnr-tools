# Skyglass end-to-end run: one agent plays the whole major update by hand, now

Job 591 (v2). Director 2026-11-13 09:23-09:35 UTC: "design a single run and assign our agent to play it end to end ...
It will need to use the PvE jutsu and item set and play intelligently." Then: "Do the run now", and: "we had the
mother of Echoes, some new charts, a new boss and a bunch of stuff planned for a major update ... I want to test all of
that additional content and have it go live as well."

So this run plays **all of the planned update while it is still hidden**, today, before tonight's release, and its
report decides what goes live. This brief is the run's contract. It sits under `state/prompt_playing_tnr.md` and
CLAUDE.md; where they are stricter, they win.

## 1. Mode

Everything below is hidden content, so this is **staff test mode** (player brief 5.3), played on the director's
account **dauntless**, by hand. Play it as a dedicated level-100 player meeting it for the first time: learn each
fight from what the game shows (quest text, dialog, battle state, inventory). Do not read this repository's design
docs, manifests, specs or generated data to solve a fight; the point is to find out what a player can work out. Do
not call content or staff endpoints (create, update, delete, hide); this run only plays.

## 2. Setup (once, before any fight)

1. Clone or pull `perseverance484/tnr-tools` (main). Read CLAUDE.md, `state/prompt_playing_tnr.md` sections 1, 4.5
   and 5, `state/player/dauntless/pvp_playbook.md` ("Loadouts by activity", "Kit") and
   `state/player/dauntless/combat_notes_live.md`.
2. Run lock: `node forge/tools/run_lock.mjs claim --holder player --job "591 Skyglass e2e run" --ttl 60 --wait`.
   If another holder has it, wait (retry every minute); never take it over. Heartbeat at least every 30 minutes
   (`node forge/tools/run_lock.mjs heartbeat --token <token>`); release at the end. If a content job becomes ready in
   `state/run_queue.json`, finish the current fight, then pause, release, and resume when it is done.
3. Only the TNR connector (`mcp__Tnr__*`). No browser. No chat or messages. About 12 calls a minute.
4. Loadouts: `jutsu.selectJutsuLoadout {id: "w6SGSCzCfnyzAhqKebKzI"}` (PvE, the set with the PvE-only jutsu) and
   `item.selectItemLoadout {id: "q94r_70pLKJjXfRTc6OBp"}` (PvE, the Kitsune set). Read both back.
5. Gear and pools: nothing worn may be broken (worn is fine); repair anything at 0. Full Potion straight after every
   fight out of an isolated run; ramen for chakra and stamina. Count potions, ryo and repairs used.

## 3. The route (in this order; record every step)

Ids are given so you can start each piece; how to play it you learn in game.

1. **The Whole Wreck** (`VcZuZmu4db0A6EF32WW3h`, hidden staff walk-through, not isolated). The salvager walks you
   through every Skyglass piece, hands you the real items (Tide Chart, Wreck Salvage, the deep charts, the Closing
   Hold chart, the Lantern, the four shards) and offers each boss as players would face it. **Take every fight it
   offers** rather than moving on. This is the spine of the run; steps 2-6 use what it gives you.
2. **The Salvager's thread**: Wreck Sighted (`_zp1l7Y9a_77pgonAdsYx`, visible), then **At the Salvager's Fire**
   (`lEg5pVXqA8lzJpIPrykNi`, hidden event). Judge whether a new player would understand the event from these alone.
3. **The Salvager's trades** (hidden mastery quests): Deck Charts `TdYCx3GME2s6L33GjnWHx`, Hold Charts
   `7pk21EmBrmL_EyHuPK2Xp`, A Sealed Chart `jUQYz9zyMdJIRdLbucYjm`, The Lantern `MSQJTdZEQK1JWjFiVtQVI`. Make each
   trade once with the salvage you hold. Check: the salvage is taken, the chart is given, the trade is your choice
   (not random), and the Lantern trade's weekly limit holds (try it a second time; it should refuse). If a trade
   cannot be started where you are, record exactly what the game says.
4. **The new charts** (hidden chart runs): The Spoiled Hold `iRMyb0WN_ip--EDbvAgLc`, The Rotted Galley
   `x7ByC_5ssbpibxTB60Ag1`, The Glass Nursery `F2eGqpysfQ02E6pXvKqJJ`. One win each, if you hold the chart.
5. **The new boss**: **The Closing Hold** (`pCFFWT8ZNDMfXCrvR-0hk`, hidden; the Hullbound Mender). Win it.
6. **The Driftline** (hidden): Into the Driftline `yZUKtA7Tsmax9LshlRV_v`, Beachcombing `coeU4MbjxOq0iydIfM3xA`,
   The Salvager's Tally `BlcnJq-OHkeWcl8pxNU6w`, and its charts The Split Hold `ktVUByCZUfREmWYsvPtzQ` and The Broken
   Stern `BDUY4nScGzYiZoHGkmkxP`. Play what you can start and hold the chart for.
7. **The Mother of Echoes (Practice)** (`YDmKO6fp2vBRnTf7fHWQZ`, hidden, isolated). All three acts. Health, chakra
   and stamina carry between acts with no refills; do not leave to heal. Learn her by playing: the omens (marked
   ground), the safe hexes, what each act punishes. She is meant to be brutal; a loss is a valid result. Record the
   round and the move that ended it, and retry up to twice with a changed plan. Most of her clips are still drawn at
   1x size while the resize is pending: ignore visuals, judge mechanics. Do not claim a reward choice from this quest.
8. **Not today**: the live Wrecks and page 2 open at 6 PM Central with the weekly release; a later session plays them.
   Do not start The Mother of Echoes (real, `IBPNwhAzlAJPXoeEnp8gW`) or the Watch Log Fourth Page.

If a step cannot be started (missing item, wrong place, prerequisite), record exactly what the game said and move to
the next step. Do not try to work around it.

## 4. How to play (by hand, every turn)

- **Always play it by hand.** Never auto-combat. Read the full battle state every turn, then choose.
- Each turn read: HP, chakra and stamina for every fighter; statuses and their rounds; marked or telegraphed hexes;
  your cooldowns and the enemy's; ranges; action points. Predict the enemy's next move from what you have seen it do.
- PvE priorities: stay alive (leave marked ground before it fires; heal before a big hit, not after), then remove the
  biggest threat, then damage. Cleanses and barriers against the move you know is coming. Spend cooldowns where they
  change the outcome.
- Keep a short notebook per enemy (opener, telegraph, punish) and use it the next time you meet it.
- **If attacked by a player** outside an isolated battle: fight back with the PvP loadouts
  (`soXekhNjk7qihu-Rsok-6` / `B-bCCtg-_fvcJSrvR1ts0`), then switch back to PvE and carry on.
- Never flee to dodge a hard fight. Retry a lost battle at most twice with a changed plan, then record and move on.

## 5. Stop and report instead of acting when

- something would spend premium currency or real money, sell or delete a rare item, or leave the clan or village;
- a response looks like an exploitable bug (report it, do not repeat it);
- the account is stuck (an isolated run it cannot leave, a battle that will not end);
- any rule in `state/prompt_playing_tnr.md` section 5 applies.

## 6. Finish

1. PvP loadouts back on, Full Potion, then (if in home sector 177 and not in battle) spend energy over 500 on
   intelligence and `home.toggleSleep` so the account is asleep. Release the lock.
2. Write `state/player/dauntless/sessions/<UTC date>_skyglass_e2e.md`, headed by a **go-live table**: one row per
   piece (Whole Wreck, Salvager's thread, each trade, each new chart, the Closing Hold, the Driftline pieces, the
   Mother of Echoes per act) with **ready / fix first / blocked**, one line why, and the battle id. Then:
   - **time** per step and in total (UTC);
   - **rewards and costs** (items handed over, drops, ryo, potions, durability);
   - **findings** with evidence: bugs, balance (too hard, too easy, unrewarding), confusion points, text issues;
   - **the Mother of Echoes**: per act, the round reached, what killed you or how you won, which omens read well;
   - **for the director**: the three things most worth fixing before tonight's release.
3. Commit "player: Skyglass e2e run (591)" and push to main. Mark job 591 done in `state/run_queue.json` with a
   one-line result.
