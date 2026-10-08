# Forge Bloodright importer — approved implementation brief

User approved execution on 2026-10-08. Lane A implementation owned by ChatGPT on
`chatgpt/forge-bloodright-import`, based on `5963810895aae4e2deaa61b72424c203752f50c1`.

Implement the approved six-stage plan: scoped source contract and skill/folder recipes;
complete inventory and explicit scoped bindings; deterministic design compiler; preview
and journal/recovery integration; socket-free regression/build gates; BEE pilot package.

The game source pin is `1ccdaf078a58101872675e459c8e755b495d4c83`.
The existing legacy contract pin stays unchanged. Source evidence is recorded in
`docs/reviews/BLOODRIGHT_IMPORT_SOURCE_AUDIT.md`.

Canonical pilot design: `docs/design/bloodright/examples/blood_enchanted_eyes_structural.json`
at the tools base SHA above (12 nodes, four chains, five BP). Preserve Hungry Pulse
`HWq7986PPhl5emkAM3L4a`, its existing image, and its explicit screenshot values (20 Silver,
99 rounds). Those values are not authorization to price every other node. Unspecified
prices/durations block compilation. New content is hidden. Existing folder is explicitly
bound; names alone never authorize overwrites. Preview is frozen into job identity and
persisted for reload. Parents must verify before children run; ambiguous writes are never
blindly retried. Existing session machinery and server content-role checks remain authoritative.

No live writes, publication, automatic deletions/refunds, game-engine changes, balance
invention, or replacement artwork. The user launches the resulting Forge import after
review and filling any outstanding content decisions. Finish with reproducible build and
exact-SHA handoff; independent review remains a separate step.
