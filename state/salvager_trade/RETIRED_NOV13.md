# Retired trade records (Nov 13)

The four original trade quests in 542_ids_retired_nov13.json were switched from mission to event at about 18:40Z on Nov 13.
That switch bulk-assigns an event quest to every player active in the last 7 days who is in its rank range
(tnrsrc quests.ts ~984, upsertQuestEntries), and the attempts start with entry unpaid. The "Keep my salvage" branch
comes before the first battle, so an unpaid attempt there would hand out free salvage.

Fix: fresh copies made with quests.clone (no assignment), ids now in 542_ids.json. The originals stay hidden for good.
Hidden quests are filtered out of a player's quest list (questAssignment.ts ~889) and cannot be played by non-staff, so
the stray attempts stay invisible. Never unhide the originals.
