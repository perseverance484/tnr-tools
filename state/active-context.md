# Active context - mounted session 1 (2026-08-29)

Git-native from here: THIS file in the repo is the open-here runbook; the classic
bundle/unpack ritual is retired. Container opens with: dauntless pastes the
tnr-container PAT, clone, read state/, work the board.

Landed this session (mounted Claude): builder v4.26 then v4.27 at root (new ⇩ Repo
loader: lists .json/.zip in a repo dir via contents API, loads through the same paths
as 📄 Load), pushpack.py -> scripts/, smoketest_pack.zip + 6_verify_and_fix.json ->
push/ (file 6 ON HOLD until Terr clears), clerk prompt + Terr addendum -> state/.
regen_schemas.yml NOT landed: tnr-container PAT lacks the Workflows permission and
GitHub rejects workflow-file pushes without it. Fix either way: add "Workflows: RW"
to the tnr-container PAT (Settings > Developer settings > Fine-grained tokens), or
add the file via web UI; a copy was handed back in-session.

dauntless gates, in order:
1. VM refresh once. Panel gate: 'Content builder v4.27 · cfg generated'.
2. If ⇪ Sync shows off: tap it, paste the tnr-sync PAT, confirm ON.
3. ⇩ Repo -> dir 'push' -> smoketest_pack.zip -> ▶ Build. Capture-only, zero
   mutations. Expect a harvests/inbox/ commit in the status line. That commit is the
   first zero-touch results round trip.
4. Say the word; container pulls and harvest.py's the inbox bundle -> Law 29
   transcription carve-out closed.

Then: warehouse clerk portrait (state/prompt_report_clerk.txt), run 6_verify_and_fix
via ⇩ Repo when Terr clears, land + first-run the regen workflow (workflow_dispatch;
read the log, extract CLI may need a flag). Fork of studie-tech/TheNinjaRPG:
already exists on the account, off the board.

Unchanged by the mount: real-name ban, hidden-first shipping, dauntless-only game pushes.
