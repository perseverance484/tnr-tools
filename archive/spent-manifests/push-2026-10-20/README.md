# Withdrawn 2026-10-20

`134_suragu_formula_scaling.json` was withdrawn before it was run (dauntless, 2026-10-20). It would
have added `generalTypes: ["Highest"]` (and set `statTypes` to `["None"]`) on Magma Slayer's and
Eruption Strike's main hits. The only basis was engine law 4 ("an empty generals list detonates the
damage formula"), a 2026-07 live observation that has not been re-verified in the game source, while
jutsu with the same gap have been live for months without reported damage spikes. As written it is
an unmeasured damage change, not a verified fix. Revisit only after the damage formula's handling of
missing `generalTypes` is read in the game source or measured in a fight capture.

## 144-145 replaced before they were run (2026-10-20)

`144_frost_warden_rank_fix.json` and `145_frost_warden_reequip.json` sent both Frost Warden steps
(unequip with the rank fix, then re-equip) as review-desk suggestions. dauntless chose instead to
run the unequip directly and send only the re-equip, with the rank fix, as a suggestion. They are
replaced by push/146 (direct unequip) and push/147 (suggestion). Never run.
