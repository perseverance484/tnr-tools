# Taiyo Kami handoff files (historical)

`taiyo_kami.json`, `taiyo_kami.svg` and `taiyo_kami_validation.json` are the original ChatGPT handoff reference, kept unchanged as evidence. They predate RUL-2026-10-03-005: they describe the potency scope per bloodline ("existing supported tags of every Taiyo Kami jutsu") and print the old raw-power Damage label.

The current reference is the generated projection `../trees/taiyo_kami.{json,md,svg,validation.json}`. Its node names, tiers, prerequisites and every modifier value are identical to these files; only the scope wording (all Scorch jutsu), the `%` display and the generated metadata follow the current rulings. `scripts/bloodright/tests/test_bloodright_tools.py` checks that the projection keeps the handoff values and that the tooling still reproduces the handoff audit.
