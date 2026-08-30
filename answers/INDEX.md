# answers/INDEX.md - the lookup layer

generated: 2026-08-30 04:54Z. Raw CDN caches ~5 min; a lookup that must be fresher takes a capture.
Rows are `[id, name, hidden]`; `hidden: null` means the source did not carry the flag.

| entity | rows | source | source stamp | fetch |
|---|---|---|---|---|
| jutsu | 1472 | `harvests/seed/40_INDEX_jutsu.json` | seed catalog (pre-answers) | https://raw.githubusercontent.com/perseverance484/tnr-tools/main/answers/names_jutsu.json |
| item | 766 | `harvests/seed/41_INDEX_item.json` | seed catalog (pre-answers) | https://raw.githubusercontent.com/perseverance484/tnr-tools/main/answers/names_item.json |
| ai | 532 | `harvests/seed/42_INDEX_ai.json` | seed catalog (pre-answers) | https://raw.githubusercontent.com/perseverance484/tnr-tools/main/answers/names_ai.json |
| asset | 407 | `harvests/seed/43_INDEX_asset.json` | 2026-08-24 | https://raw.githubusercontent.com/perseverance484/tnr-tools/main/answers/names_asset.json |
| quest | 400 | `harvests/seed/47_INDEX_quest.json` | seed catalog (pre-answers) | https://raw.githubusercontent.com/perseverance484/tnr-tools/main/answers/names_quest.json |

Other fetchable canon:
- Engine laws (full numbered text): https://raw.githubusercontent.com/perseverance484/tnr-tools/main/docs/ENGINE_LAWS.md
- Rollout plan: https://raw.githubusercontent.com/perseverance484/tnr-tools/main/docs/ROLLOUT_PLAN.md

Skill zips (download, not fetch): /dist/ on the repo page.

A capture beats any file here (precedence). Hidden content of the current
wave may predate the newest committed harvest; absence is not proof.
