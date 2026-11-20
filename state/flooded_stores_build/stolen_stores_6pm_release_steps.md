# Stolen Stores release, Friday 2026-11-20 at 6 PM Central (00:00 UTC Saturday)

The director's go for this sitting: 15:15Z "Sounds good for release. Build everything needed hidden", 15:39Z "1. Ok,
set it up on the scheduled task that's already planned. 2. We'll publish it with the rest", 16:16Z "5. They will be
part of tonight's release" (Isonade style C animations). Every step below is on hidden records built and read back
today. Nothing here creates, deletes or edits anything not listed.

Repo: perseverance484/tnr-tools, branch claude/project-thread-hlg3nc (head 6012696b or later). Connector: Tnr.

## Timing and order

The main chat set this up (relay 16:36Z): a kickoff at 23:20Z (5:20 PM CT) starts this thread on this file. Steps 1
to 3 run from then (reads, regeneration, hidden prep). Every player-visible write (steps 4 to 9) waits for 00:00Z
and each gets its read-back before the next.

"Weekly Skyglass release check" (trig_015Z6waXLdEXKM3JUJCJKT5C, 00:00Z) now waits up to about 45 minutes for an
unhidden Watch Log page, and skips any Wreck already reopened with the right expiry and hidden false. So step 9 can be
done here or left to it.

1. **Pre-checks.** `node forge/tools/run_lock.mjs status`: the lock is free (the Isonade animation thread also needs
   it tonight; take turns). dauntless is not in a fight or quest (`profile.getUser` battleId null). Sleep it again
   with `home.toggleSleep` after anything that wakes it.
2. **Fresh reads, then regenerate** (each generator refuses if the live record moved in a way it doesn't expect):
   - Deck Charts trade `zYhkIQeVGNUMljwev3-ud` and the Fire `lEg5pVXqA8lzJpIPrykNi`: `quests.get` each in full and
     compare to the copies inside `push/673_stolen_stores_golive_master.json` (phases 300 and 520). If either differs
     anywhere but the fields 673 sets, stop and report; don't run.
   - Then `python3 push/stolen_stores_golive.gen.py` and `git diff --exit-code push/673_stolen_stores_golive_master.json`
     (expect no change).
3. **Isonade style C animations, ONLY if the director approves packs A to C (rev d, e, f; they replace rev b)** (the main chat says either way). If approved:
   the animation thread's hidden uploads and wiring, with law 18 (remove, save, add back, count equipped) on any
   jutsu an AI equips, before 673, so 673's asset unhides land on the final list; or that thread confirms its assets
   need no unhide from 673. If not approved: skip; 673 ships the current 9 animations.
   Window agreed with the animation thread (session_01GL8iyjKuCXzCd1WzPQu76i) at 17:40Z: 22:15 to 23:10Z under the
   run lock, only if the director approves packs A to C in words first. No approval by about 22:00Z means the
   thread skips the window and tells me; 673 then ships the current 9. It writes new hidden strips, Isonade jutsu art fields,
   a law 18 re-equip on the Isonade AI, read-backs, its own unhides and one test battle, then releases the lock and
   messages back with the final asset ids per jutsu and whether any of 673's 9 assets (xKgBB, izjz7, BexP4, isRdj,
   vLnK4, 5vyAK, PKF3L, Xba6L, quxGk) should stay hidden. If it says some should, drop those from 673 phase 100,
   regenerate and re-check before step 5. At 23:20Z check that its done message arrived and the lock is free; if not,
   wait for it rather than start.
4. **Shore crew spawns on (00:00Z, before 673).** From the Roaming crew thread (relay 16:44Z). For each of the 4
   spawns `N142XR4hbrfHaIEE7Z-BL`, `v329QMIIE8NCr5ScXwQrj`, `1hQvqkHGhNw-XhBRQxREv`, `W8WZoQ1q7T8-5nnosdDPm`: read the
   placement in full, `overworldAi.upsertPlacement` with that record changed only at `isActive: true`, read it back.
   All 4 active before Short Rations unhides (673 phase 200): once Short Rations is live the spawns can't be switched
   off or changed while the quest uses them. Short Rations kept id `Gqbnq2LVtIVBlLYlAnam1`, so 643, 673 and both
   pages need no change. The Galley Mate's Flooded Stores chart drop goes live with 673's chart item unhide.
5. **Run 673** under the lock:
   ```
   node forge/tools/run_lock.mjs claim --holder claude --job "push/673" --wait
   node forge/tools/mcp_run.mjs run push/673_stolen_stores_golive_master.json --token <token> --state /mnt/project-files/tnr/forge_state/673 --transcript auto
   node forge/tools/run_lock.mjs release --token <token>
   ```
   20 items: 9 Isonade assets, chart item, The Flooded Stores, Short Rations, Deck Charts pick, both Watch Log pages,
   new Wreck Sighted copies on, last weekend's off, the Fire's topics. Expect "Finished: all 20 items written and
   verified". Commit the bundle from harvests/inbox and set 673 done in state/run_queue.json.
6. **Salvager pool.** `overworldAi.getPlacementsForAi` for the Salvager, compare to
   `push/639_salvager_pool_upsert.json` (only the pool may differ), then `overworldAi.upsertPlacement` with that file's
   `input`, then read it back. Pool sums to 100 or less.
7. **Sector 210 map.** `worldMap.publishSectorMap {"id": "RJl-uOXFYoHlxcgkptJF3"}`. This replaces the live sector map.
8. **Short Rations switch** (the director 16:35Z: "Switch Short Rations"). The shore-crew thread
   (cmsg_01HemWcQ2jhMimRupeBNzcGRP1ktJt8h1SP18BCWCQ6qe6) hands over the crew placements and the rebuilt Short Rations.
   673 sends Short Rations `Gqbnq2LVtIVBlLYlAnam1` only `{hidden: false}`, so it cannot overwrite the rebuilt quest
   as long as the id stays the same. Both Watch Log pages and the Salvager pool point at that id. Keep the tin icon
   (`...0tzd8oDeiVIzM4ZECEIcLXcweuU7CfBRq2T3S1iWhVAz8Glb`) on it. Done by steps 4 to 6.
9. **Wrecks.** Reopen both to 00:00 UTC Tuesday as the release-check routine does, or leave it to that routine.

## Read-backs (all must hold)

- 9 Isonade assets, Chart of the Flooded Stores, The Flooded Stores, Short Rations: hidden false.
- Chart item, run and Short Rations show the director's new icons; both pages show theirs.
- The Watch Log: Stolen Stores `AgGR962c3XNo6Pr0up2qT`: hidden false, level 81 to 100, starts 2026-11-21, ends
  2026-11-24, challenge 1 counts a Quartermaster's Mate or the Galley Mate, challenge 2 pays the Chart of the Flooded
  Stores.
- The Watch Log: Stolen Stores (Shallows) `qOhvkP3aPCPH88wI7-IZW`: hidden false, level 30 to 80, same window,
  challenge 1 counts a Looting Deckhand or a Foraging Deckhand, challenge 3 pays the Chart of the Flooded Stores.
- No other Watch Log page is unhidden: The Rotted Heading `V-i3ZcAqPu0hB3G9IEzGo`, the 81+ staff test
  `SuHxe9zqUvVlEqxEQp8Dd` and Her Invitation `I_cEOGSfFuahaJlR3FnWC` read hidden at 16:40Z today; check The Rotted
  Heading (Shallows) and "The Watch Log: First Page - copy" too.
- Deck Charts trade: 5 picks, the Flooded Stores chart among them.
- Wreck Sighted: Stolen Stores copies `VRibCq0gip_otYBbWEX4J` and `tYNgqctjx_5KIKbbOyApH` hidden false; last weekend's
  `IZgCt17ReC_0vtUG-GNRl` and `-UjsbiBbaSyPtZ4zAH10A` hidden true.
- Fire `lEg5pVXqA8lzJpIPrykNi`: "What's eating the stores?" carries the story v2 line (hook for a tail).
- 4 shore crew spawns isActive true. Salvager pool includes Short Rations; sector 210 shows the published map.
- Both Wrecks open until 00:00 UTC Tuesday.

## Stays hidden on purpose

Isonade's Old Hull, the AI-only jutsu, Isonade Test, the 81+ staff test page, the grant test quest.

## Known leftovers (not tonight's problem)

`push/flooded_stores_run.gen.py` and `push/wreck_sighted_stolen_stores.gen.py`'s copy text still hold the story v1
run strings (the live records hold v2 from push/674). Regenerating either from scratch would put v1 back.

## After the run

Release the lock and tell the main chat: the Roaming crew thread then does one check fight on dauntless at full HP
and puts the account to sleep.
