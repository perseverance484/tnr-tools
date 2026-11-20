# Stolen Stores release, Friday 2026-11-20 at 6 PM Central (00:00 UTC Saturday)

The director's go for this sitting: 15:15Z "Sounds good for release. Build everything needed hidden", 15:39Z "1. Ok,
set it up on the scheduled task that's already planned. 2. We'll publish it with the rest", 16:16Z "5. They will be
part of tonight's release" (Isonade style C animations). Every step below is on hidden records built and read back
today. Nothing here creates, deletes or edits anything not listed.

Repo: perseverance484/tnr-tools, branch claude/project-thread-hlg3nc (head 6012696b or later). Connector: Tnr.

## Order

The existing routine "Weekly Skyglass release check" (trig_015Z6waXLdEXKM3JUJCJKT5C, 00:00 UTC Saturday) only
reopens the two Wrecks, and its step 1 stops unless a Watch Log page is already unhidden with startsAt today. So the
steps below run first, then that routine's Wreck reopen. Its prompt also says never to publish or edit a page; that
line has to change for tonight, or these steps run as their own routine just before it.

1. **Pre-checks.** `node forge/tools/run_lock.mjs status`: the lock is free (the Isonade animation thread also needs
   it tonight; take turns). dauntless is not in a fight or quest (`profile.getUser` battleId null). Sleep it again
   with `home.toggleSleep` after anything that wakes it.
2. **Fresh reads, then regenerate** (each generator refuses if the live record moved in a way it doesn't expect):
   - Deck Charts trade `zYhkIQeVGNUMljwev3-ud` and the Fire `lEg5pVXqA8lzJpIPrykNi`: `quests.get` each in full and
     compare to the copies inside `push/673_stolen_stores_golive_master.json` (phases 300 and 520). If either differs
     anywhere but the fields 673 sets, stop and report; don't run.
   - Then `python3 push/stolen_stores_golive.gen.py` and `git diff --exit-code push/673_stolen_stores_golive_master.json`
     (expect no change).
3. **Isonade style C animations.** Whatever the animation thread hands over (re-equip under law 18 if a jutsu an AI
   equips changes). Do it before 673 so 673's asset unhides land on the final asset list, or have that thread confirm
   its assets need no unhide from 673.
4. **Run 673** under the lock:
   ```
   node forge/tools/run_lock.mjs claim --holder claude --job "push/673" --wait
   node forge/tools/mcp_run.mjs run push/673_stolen_stores_golive_master.json --token <token> --state /mnt/project-files/tnr/forge_state/673 --transcript auto
   node forge/tools/run_lock.mjs release --token <token>
   ```
   20 items: 9 Isonade assets, chart item, The Flooded Stores, Short Rations, Deck Charts pick, both Watch Log pages,
   new Wreck Sighted copies on, last weekend's off, the Fire's topics. Expect "Finished: all 20 items written and
   verified". Commit the bundle from harvests/inbox and set 673 done in state/run_queue.json.
5. **Salvager pool.** `overworldAi.getPlacementsForAi` for the Salvager, compare to
   `push/639_salvager_pool_upsert.json` (only the pool may differ), then `overworldAi.upsertPlacement` with that file's
   `input`, then read it back. Pool sums to 100 or less.
6. **Sector 210 map.** `worldMap.publishSectorMap {"id": "RJl-uOXFYoHlxcgkptJF3"}`. This replaces the live sector map.
7. **Short Rations switch** (the director 16:35Z: "Switch Short Rations"). The shore-crew thread
   (cmsg_01HemWcQ2jhMimRupeBNzcGRP1ktJt8h1SP18BCWCQ6qe6) hands over the crew placements and the rebuilt Short Rations.
   673 sends Short Rations `Gqbnq2LVtIVBlLYlAnam1` only `{hidden: false}`, so it cannot overwrite the rebuilt quest
   as long as the id stays the same. Both Watch Log pages and the Salvager pool point at that id. Keep the tin icon
   (`...0tzd8oDeiVIzM4ZECEIcLXcweuU7CfBRq2T3S1iWhVAz8Glb`) on it.
8. **Wrecks.** The routine's own steps 1 to 5 (reopen both Wrecks to 00:00 UTC Tuesday).

## Read-backs (all must hold)

- 9 Isonade assets, Chart of the Flooded Stores, The Flooded Stores, Short Rations: hidden false.
- Chart item, run and Short Rations show the director's new icons; both pages show theirs.
- The Watch Log: Stolen Stores `AgGR962c3XNo6Pr0up2qT`: hidden false, level 81 to 100, starts 2026-11-21, ends
  2026-11-24, challenge 2 pays the Chart of the Flooded Stores.
- The Watch Log: Stolen Stores (Shallows) `qOhvkP3aPCPH88wI7-IZW`: hidden false, level 30 to 80, same window,
  challenge 3 pays the Chart of the Flooded Stores.
- No other Watch Log page is unhidden: The Rotted Heading `V-i3ZcAqPu0hB3G9IEzGo`, the 81+ staff test
  `SuHxe9zqUvVlEqxEQp8Dd` and Her Invitation `I_cEOGSfFuahaJlR3FnWC` read hidden at 16:40Z today; check The Rotted
  Heading (Shallows) and "The Watch Log: First Page - copy" too.
- Deck Charts trade: 5 picks, the Flooded Stores chart among them.
- Wreck Sighted: Stolen Stores copies `VRibCq0gip_otYBbWEX4J` and `tYNgqctjx_5KIKbbOyApH` hidden false; last weekend's
  `IZgCt17ReC_0vtUG-GNRl` and `-UjsbiBbaSyPtZ4zAH10A` hidden true.
- Fire `lEg5pVXqA8lzJpIPrykNi`: "What's eating the stores?" carries the story v2 line (hook for a tail).
- Salvager pool includes Short Rations; sector 210 shows the published map.
- Both Wrecks open until 00:00 UTC Tuesday.

## Stays hidden on purpose

Isonade's Old Hull, the AI-only jutsu, Isonade Test, the 81+ staff test page, the grant test quest.

## Known leftovers (not tonight's problem)

`push/flooded_stores_run.gen.py` and `push/wreck_sighted_stolen_stores.gen.py`'s copy text still hold the story v1
run strings (the live records hold v2 from push/674). Regenerating either from scratch would put v1 back.
