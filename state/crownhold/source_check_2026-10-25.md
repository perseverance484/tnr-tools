# Crownhold source check (push/269, 2026-10-25)

Bundle `harvests/inbox/tnr_results_1792983091495.json`: 81/81 reads ok. Compared against the design package's
`sources/source_records.json` (claude/silent-bastion-authoring-69za5u@6271e1f).

- **All 76 kit jutsu ids are live.** 68 differ from the package's records, almost all cosmetically:
  - `statTypes: ["Highest"]` stored as `["None"]` (the server's own transform, as push/261 showed) on damage effects;
    buff/debuff tags (IDG, DDT and similar) no longer carry `statTypes`/`generalTypes`; Tempest Cleave's
    classifications normalised the same way; `OTHER_USER` target now `OPPONENT`. No combat change.
  - **15 renames** (ids unchanged, so kits and rules still bind): Tempo Fracture -> Dragging Hour, Hexweave -> Cursed
    Thread Weave, Cataclysm Detonation -> Explosive Tag Cataclysm, Worldbreaker Chorus -> Great Bell Toll, Apex Hunger
    -> Oni's Hunger, Compression Barrier -> Folding Screen Guard, Recoil Slam -> Backlash Palm, Nullifying Wave ->
    Dispelling Wave, Zephyr Lance -> Wind Spear, Arc Bolt -> Lightning Needle, Storm Breaker Volt -> Thunderclap
    Breaker, Static Jolt -> Numbing Spark, Ion Lance -> Raijin's Spear, Twin Shot -> Twin Kunai, Rapid Fire ->
    Shuriken Storm. Story text or rule notes that name a jutsu must use the new names.
  - **Two real mechanical changes:**
    - **S07 Rapid Fire -> Shuriken Storm** (`Nrxc8m9utE9qaD_gWpLgf`): damage 40 became pierce 70 + wound 30 for 3
      rounds. All four commanders equip it and name it in two rules each. It is now a much stronger filler; keep it or
      swap it (director).
    - **B28 Recoil Slam -> Backlash Palm**: its recoil now lasts 2 rounds (was 0).
- **Veilstep (B09)** is unchanged (Stealth 1 round, cooldown 5), so RUL-2026-10-16-007 holds as authored.
- **Arakane's weapons** are live: Solar Bow `ALqXVSL58QMfJ4DgoJ5Il` (BOW, 40 AP, range 5, cooldown 3, visible) and
  Crossbow `LbccOnzfsADLgTBPSHjKK` (BOW, 40 AP, range 4, cooldown 0, **hidden**). Whether an AI can use a hidden item is
  to be confirmed by the post-create read-back.
- **Names:** the three name reads returned counts only (561 AI, 1,683 jutsu, 865 items; not persisted). Against the
  repository snapshots there is no collision for the 20 AI usernames, The Last Directive, Extermination Order,
  Countermand or Crownbreaker; Forge's `dedupNames` repeats the check live at create time.
