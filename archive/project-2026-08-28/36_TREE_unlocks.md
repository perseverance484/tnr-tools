> **STALE - archived 2026-08-28 (rollout Stage 1).** shipped Ashen campaign; archive only.
> Do not build from this file.

# 38c_TREE_unlocks.md: how content reveals [2026-07-27]

## The engine rule
A quest carries exactly one prerequisite. The server field is `prerequisiteQuestId`, typed `string|null` in the write validator, not an array, so the unlock graph is a tree: one parent per quest, any number of children, and every child of a parent reveals the moment that parent completes. There is no way to express 'opens after both A and B' with prerequisites alone.

## The three ways to express a second condition
1. Serialize. Hang the record off the later of the two beats and let the chain carry the rest, since a linear spine makes every earlier beat a transitive requirement. This is what the campaign does everywhere.
2. Use an orthogonal gate field. `huntingRank`, `gatheringRank`, `requiredLevel`, `requiredRank`, `requiredVillage`, and `requiredBloodlineId` all stack on top of the prerequisite. The profession lanes are exactly this: parent is the Muster, and the rank field is the second gate.
3. Check possession in a node. A `deliver_item` objective can demand an item without consuming it. The campaign uses this only for the sworn patrol legs and their Oaths.

## The reveal points
The Muster reveals nine records at once: the Forge Column board, the Outer Districts, the Long Patrol, the Wards, the Rounds, and the four profession records. Each chapter reveals its own kiln plus the next board or chapter. The Compact reveals three, the Veiled Table reveals three. Everything else is a single child.

## The tree

From the live campaign hub:
  - The Concord Board (one time)
    - The Concord Muster (one time)
      - Ashen Gather: Cinderbloom (none, D RANK only)
      - Ashen Hunt: Kiln Drakes (Kilnhide) (none, D RANK only)
      - The Ashrend Roosts: The Long Climb (daily, D RANK only)
      - The Board: The Forge Column (one time)
        - The Ryokin (one time)
          - The Board: The Kiln Column (one time)
            - The Red Itokage (one time)
              - The Archive Furnace (daily)
                - The Archive Crucible (daily)
              - The Cipher Vault (one time)
              - The Shirakotsu (one time)
                - The Boneyard Furnace (daily)
                  - The Boneyard Crucible (daily)
                  - The Ossuary Vigil (one time)
                - The Hagane (one time)
                  - The Pit Furnace (daily)
                    - The Pit Crucible (daily)
                  - The Quiet Nemori (one time)
                    - The Board: The Heats (one time)
                      - The Compact (one time)
                        - The Clan Grounds (daily)
                        - The Quartermaster's Requisition (one time)
                        - The Reckoning (one time)
                          - The Veiled Table (one time)
                            - The Board: The Deep Doors (one time)
                              - The Ash Settlement (weekly)
                                - The Glassfire (weekly)
                            - The Deep Works (daily)
                            - The Table's Requisition (one time)
                    - The Rootway Furnace (daily)
                      - The Rootway Crucible (daily)
          - The First Fitting (one time)
          - The Vault Furnace (daily)
            - The Vault Crucible (daily)
              - The Undervaults (one time)
      - The Cinder Fields: The Deep Rows (daily, D RANK only)
      - The Long Patrol (daily)
        - The Ashfall Sweep (daily)
      - The Outer Districts (daily)
      - The Outer Wards (one time)
        - The Founder's Stair (one time)
      - The Quartermaster's Rounds (one time)


## Final tree after the simplification build (2026-07-27)

- The Concord Board
  - The Concord Muster
    - The Board: The Forge Column
      - The Ryokin
        - The Board: The Kiln Column
          - The Red Itokage
            - The Shirakotsu
              - The Hagane
                - The Quiet Nemori
                  - The Board: The Heats
                    - The Compact
                      - The Second Fitting
                        - The Reckoning
                          - The Veiled Table
                            - The Third Fitting
                              - The Board: The Deep Doors
                                - The Ash Settlement [WEEKLY]
                                  - The Glassfire [WEEKLY]
                            - The Deep Works [DAILY]
                      - The Clan Crucibles [DAILY]
          - The Clan Furnaces [DAILY]
      - The Outer Districts [DAILY]
    - Ashen Gather: Cinderbloom [PROFESSION]
    - Ashen Hunt: Kiln Drakes (Kilnhide) [PROFESSION]
    - The Ashrend Roosts: The Long Climb [PROFESSION]
    - The Cinder Fields: The Deep Rows [PROFESSION]
