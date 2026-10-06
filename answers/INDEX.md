# answers/INDEX.md - the lookup layer

Two fetches answer any name/id lookup: this INDEX, then the entity file
(plus hot.json when its delta column below is non-zero). Rows are
`[id, name, hidden]`; `hidden: null` means the source did not carry the
flag. `generated` stamps are DERIVED from sources, so regeneration is
idempotent. Raw CDN caches ~5 min; fresher than that takes a capture.

Mission checks: `python3 scripts/tnr.py missions check --rank A`.
Without a checkout, fetch `answers/missions_A.md` and, for provenance/coverage,
`answers/missions_A.json` at the SAME exact commit. B/C/D/S views also exist.
Full-record observations override seed names/visibility; see `answers/records.json`
for per-record evidence, input hashes, exclusions and unresolved observations.

| entity | rows | source stamp | hot delta (newer, uncataloged) | fetch |
|---|---|---|---|---|
| jutsu | 1472 | seed catalog (pre-answers) | 19 | https://raw.githubusercontent.com/perseverance484/tnr-tools/main/answers/names_jutsu.json |
| item | 766 | seed catalog (pre-answers) | 0 | https://raw.githubusercontent.com/perseverance484/tnr-tools/main/answers/names_item.json |
| ai | 532 | seed catalog (pre-answers) | 0 | https://raw.githubusercontent.com/perseverance484/tnr-tools/main/answers/names_ai.json |
| asset | 407 | 2026-08-24 | 19 | https://raw.githubusercontent.com/perseverance484/tnr-tools/main/answers/names_asset.json |
| quest | 400 | seed catalog (pre-answers) | 10 | https://raw.githubusercontent.com/perseverance484/tnr-tools/main/answers/names_quest.json |

Hot shard (delta rows + capture stamps): https://raw.githubusercontent.com/perseverance484/tnr-tools/main/answers/hot.json

Other fetchable canon:
- Engine laws (full numbered text): https://raw.githubusercontent.com/perseverance484/tnr-tools/main/docs/ENGINE_LAWS.md
- Doctrine (single source): https://raw.githubusercontent.com/perseverance484/tnr-tools/main/docs/DOCTRINE.md

Skill zips (download, not fetch): /dist/ on the repo page.

A capture beats any file here (precedence). Retention: see
docs/COMPACTION_RUNBOOK.md - manual-only, seed is the audit floor.
