# Preflight result at e6686d39 (old container, Nov 16)
- Run 1, 05:29:28Z: exit 1, trust dialog not accepted, 0 calls made. preflight_evidence/preflight_run1_stdout_trust_not_accepted.txt
- Trust accepted 05:31Z by driving interactive claude in a pty (Down, Enter on "Yes, I trust this folder"); stored for repo root /home/user/tnr-tools.
- Run 2, 05:31:51Z, `--form subagent --bare-env` from a bare env shell at /home/user/tnr-gate (detached checkout of e6686d39): EXIT 0. Hooks ran for every call; gate let through 3, stand-in given 3; hooks before brain next / before call / behind call = 5/3/3; ended "stopped after the check's calls". Nothing answered outside the stand-in. Evidence: preflight_evidence/tnr_preflight_tlh_o41q (two `latest` symlinks could not be copied to this share).
- A fresh container is a new machine: run it again there (LAUNCH.md step 2).
