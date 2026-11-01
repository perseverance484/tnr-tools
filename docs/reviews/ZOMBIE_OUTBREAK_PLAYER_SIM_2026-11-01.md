# Zombie Outbreak: simulated player runs (Vanquish the Horde + Zombie Outbreak sample fight)

**Date:** 2026-11-01. **Lane B review, review only:** no live record changed.
- **Records:** the push/401 recapture `harvests/inbox/tnr_results_1793568292560.json` (both quests, Patient Zero
  and his kit, the four zombie AIs with their items), the shared zombie AiProfile from
  `tnr_results_1793412740001`, and Patient Zero's rules as VERIFIED by push/336.
- **Engine:** upstream TheNinjaRPG `821fe9f00d4179fc6c4e68f9da574b2915e70d8c` (2026-11-01), read-only, run
  in-process with no database and no network.
- **Live requests:** 0.

## Method

The harness is in `zombie_outbreak_sim/harness/` and follows the `harness/ghost_ship_final` pattern.
- **Assembly:** battles are built with the engine's own `processUsersForBattle`, with `capUserStats` per rank.
- **Quest scaling:** reproduced as `initiateBattle` does it: target level set to the player's, then `scaleUserStats`.
- **Turn loop:** `alignBattle` → `performAIaction` → `alignBattle`, as in `combat.performAction`.
- **Both sides on the real AI selector:** zombies and Patient Zero run their live rule sets; the player runs a
  declared auto-combat policy.

**Player carriers** (declared inputs, not real accounts):
- **Stats:** the engine's own "player" budget for the level (`scaleUserStats`, even spread), at 100% or 60%
  (under-trained). Pools come from the level.
- **Rank:** GENIN up to 30, CHUNIN up to 50, JONIN above.
- **Kits:** two kits built from captured shared-pool jutsu.
  - *basic:* Heavy Cut, Sundering Blow, Warrior's Poise.
  - *strong:* Cataclysm Fist, Sundering Blow, Warrior's Poise, Light Barrier.
- **Not modelled:** armour, weapons, bloodline, pets and jutsu levels. Absolute win rates are therefore
  pessimistic for geared players. Comparisons between configurations hold.

**Runs:**
- Pyramid stages run in order. HP carries into the next wave, as `initiateBattle` starts a fight on current pools.
- A loss retries at full HP (the player is hospitalised), within the live retry budget: 3 / 3 / 2 / 2.
- Initiative and target rolls are seeded. Start tiles are fixed.

**How claims are marked:**
- [V-src]: engine source.
- [V-rec]: captured record.
- [V-sim]: observed in the harness.

## Findings

### B1. Zombie Claws deal permanent, stacking damage (BLOCKER)

- **The record:** the Zombie Claws item (`mMl6P4B7v6-_CyDo3HVG7`) carries a `damage` effect with **no `rounds`
  field** [V-rec].
- **The engine:** `damageUser` treats `rounds === undefined` as residual damage that never expires
  (`libs/combat/tags.ts` 1544; `isEffectActive`, `util.ts` 1311) [V-src].
- **The effect in battle:** every claw hit adds another damage effect to the target. All of them keep ticking for
  the rest of the fight, on each of the target's actions [V-sim, `harness/dot.test.ts`].
  - Level 40 duel: 1 → 2 → 3 → 4 stacked effects.
  - The player falls from 2,050 to 400 HP by round 5.
- **Zombie Outbreak sample fight** (`m_sW9`; staff turned on scale-to-player): the only enemy is the Zombie
  Villager, the one zombie that has the claws equipped [V-rec].
  - The player **loses at every level from 10 to 40, in every kit and band** (0/16 per level).
  - Level 60 is a coin-flip on training.
  - Level 100 wins only because the zombie's GENIN rank caps its stats.
  - Source: `results/zombieo_sample_as_live.json`.
  - The reset sends the player back for another try, so a sub-60 player loops the hospital and can never finish.
- **With the claws' damage made instant (`rounds: 0`):** every level wins with 46% to 100% HP left, in 3 to 14
  rounds (`results/zombieo_sample_claws_fixed.json`).
- **Fix:** set `rounds: 0` on the claws' damage effect.
  - The item is held by four zombies, and law 18 applies to items (RULINGS: the Zombie Claws break, 2026-10-26).
  - So: take the claws off all four, edit the item, put them back.

### B2. The pyramid's wave zombies never attack (BLOCKER for intent)

- **The setup:** Zombie Protector, Zombie Youngling and Elite Zombie Protector hold Zombie Claws with
  `equipped: "NONE"` [V-rec]. Their only attack rule is `use_specific_item` Zombie Claws.
- **The result:** the claws are unusable, so every wave zombie walks up, then ends its turn [V-sim].
  - Live waves 1 to 3 end at 100% player HP in every run.
  - Patient Zero's four boss-room Younglings never hit either.
- Equipping them as they stand is not an option: with B1 unfixed, wave 1 kills every player at every level
  (`results/live_claws_equipped.json`).

### M1. As live, the pyramid is one fight: Patient Zero

`results/grid_live_and_after403.json`, mode `live`. Patient Zero is unscaled (level 30, CHUNIN, stats ×3, pools ×2).

| Player level | First-try boss win (basic kit) | First-try boss win (strong kit) |
|---|---|---|
| 25 | 0% | 0% |
| 30 | 0% | 0% |
| 40 | 0% | 100% at full training, 0% at 60% |
| 60 | 100% | 100% |
| 100 | 100% | 100% |

- A cleared pyramid needs about level 60, or a strong kit at 40.
- Players at 25 to 40 reach him at full HP and lose both tries. The quest is permanently failed for them (M3).
- Patient Zero uses all six moves in rotation, including his three signature jutsu [V-sim]. That holds once
  push/402 restores his equip link.

### M2. push/403's scale-to-player on every fight makes it worse (do not run as built)

`results/after403_no_round_cap.json`, `results/grid_live_and_after403.json`, mode `after403`.

- **Scaled waves become slogs:** the zombies gain level-matched HP but still never attack (B2). At level 40 the
  waves take **27, 53 and 59 rounds**, about 140 rounds of hitting enemies that cannot hurt you. The engine has
  no round cap, so these end, but nobody will sit through them [V-src: a draw only when nobody is alive].
- **A scaled Patient Zero wins every first try at every level, 25 through 100.**
  - This holds at statsMultiplier 3, 2 and 1.5 (`results/boss_pz_mult_*.json`), so his stat multiplier is not
    the lever.
  - His ×2 pools and AI-tier kit damage against a solo player are what decide it.
- **Unscaled, lowering his multiplier helps the middle band only a little.** Level 40 first-try wins: 25% at ×3,
  38% at ×2, 75% at ×1.5. Levels 25 to 30 stay near 0.

### M3. One attempt, ever

- The pyramid has `maxAttempts: 1` and `questType: battlepyramid`. Attempts are enforced for that type and count
  at quest start [V-src: `QuestTypesWithMaxAttempts`, `drizzle/constants.ts` 1114; `quests.ts` 3242].
- Any `fail_quest` ends the event for that player permanently:
  - the intro's "No thanks!";
  - any "flee" choice;
  - running out of retries.
- With M1 that means most players at 25 to 40 lose the event on their first try at the boss.

### M4. Zombie Outbreak is a random, repeatable medical mission

- Medical quests ignore `maxAttempts` / `maxCompletes`. The mission hall picks a random medical quest by letter
  rank, capped at **9 medical missions a day** [V-src: `selectQuestForStartRandom`, `MEDICAL_MISSIONS_PER_DAY`].
- At medical rank NONE, Zombie Outbreak can be rolled by any player level 10+ and repeated.
- Each completion pays 150k ryo, 1,500 tokens, 1,500 prestige, 1,500 clan points and 4,500 medical exp.
- Silent Bloom, the model for these rewards, is gated at MASTER [V-rec].
- How often it rolls depends on how many D-rank medical quests are in the pool [not checked: needs the medical
  catalog].

## Recommendations (user-owned decisions marked)

1. **Fix the claws (B1):** unequip from all four zombies, set the damage effect's `rounds: 0`, re-equip.
   - Mechanical fix; one manifest.
   - Unblocks Zombie Outbreak for every level.
2. **Make the waves fight (B2): decision.**
   - Equipping the fixed claws on scaled waves is still too much. Wave 1 (3 zombies) kills most solo players
     below level 100 (`results/claws_fixed_equipped.json`).
   - With the waves unscaled (live wave 1 is already scaled), a strong-kit player at 40+ clears.
   - Options:
     - (a) equip the claws and keep waves 2 to 3 unscaled while cutting wave sizes (3/6/7 is heavy for a solo
       fight);
     - (b) equip them and unscale wave 1 too.
3. **Patient Zero: decision.**
   - Keep his fight unscaled.
   - Pick the target band. As built, he needs about level 60 (or 40 with a strong kit). A ×1.5 multiplier
     brings level 40 to roughly 75%.
   - Scaling him to the player fails at every level unless his pools or kit damage drop as well.
4. **push/403:** do not run it as built. Ship the scene character alone, with scaling left as live. It is held
   in `state/held/` until a decision.
5. **Retries / attempts: decision.** Consider `maxAttempts` above 1, or removing the intro "No thanks!" branch,
   so a misclick or one early loss does not lock a player out of the event.
6. **Zombie Outbreak gating: decision.** Raise the medical rank, or accept it as a repeatable random mission at
   its current payout.

## Limits

- **Plain carriers:** no gear, bloodline, pets or jutsu levels. Real players are stronger, so the level thresholds
  above are upper bounds.
- **Fixed start tiles and seeded rolls:** runs per configuration are repeat samples of a near-deterministic
  fight, not independent win rates.
- **Engine pin:** upstream main at the date above, not a verified deployed build.
- **Retry model:** a loss heals to full for the retry.
- **Patient Zero's equip link:** modelled as restored (post push/402). Until 402 runs he will not use his three
  signature jutsu in the live game.
