# Withdrawn 2026-10-20

`134_suragu_formula_scaling.json` was withdrawn before it was run (dauntless, 2026-10-20). It would
have added `generalTypes: ["Highest"]` (and set `statTypes` to `["None"]`) on Magma Slayer's and
Eruption Strike's main hits. The only basis was engine law 4 ("an empty generals list detonates the
damage formula"), a 2026-07 live observation that has not been re-verified in the game source, while
jutsu with the same gap have been live for months without reported damage spikes. As written it is
an unmeasured damage change, not a verified fix. Revisit only after the damage formula's handling of
missing `generalTypes` is read in the game source or measured in a fight capture.
