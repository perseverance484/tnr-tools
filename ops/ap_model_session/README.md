# AP model run kit
Launch procedure (LAUNCH.md) and the stop, deadline and heartbeat scripts for live AP model runs on dauntless.
Paths in LAUNCH.md are relative to the repo root. Scripts write their logs and pid next to the kit (ops/ap_model_session/), or to $AP_KIT if set.
n_fight_stop.sh <repo_root> <start_epoch> [n=10] sets end_session=true at the Nth fight_end after launch (one_fight_stop.sh is n=1).
