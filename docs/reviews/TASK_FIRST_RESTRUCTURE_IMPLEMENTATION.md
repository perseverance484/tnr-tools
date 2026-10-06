# Task-first repository restructuring

Status: implemented on `chatgpt/task-first-restructure`; independent review required
before integration. Base: `2b6cefd8ce2f1ab4d16bb8a0db8f9e38921cdf0a`.
The user approved the architectural review's five-phase plan in this task.
ChatGPT is the implementation author; this report is not independent approval.

## Result

`python3 scripts/tnr.py missions check --rank A` now performs a deterministic,
read-only inspection of repository captures. At the implementation baseline it
resolves 14 A-rank missions, including all four Forsworn missions from the October 6
capture with five objectives each. It reports the incomplete population and 20
unresolved quest IDs whose rank cannot be established. Missing records are never
reported as deleted or invented from mission construction profiles.

Initialization no longer edits the shared digest or runs unrelated guards by
default. The short ChatGPT entry point plus mission packet is below 5.6 KB,
compared with the audited 103,699-byte broad reading route. Three local warm
queries measured 0.122–0.131 seconds before final documentation edits. These are
local command timings, not a promise about ChatGPT or GitHub response latency.

## Implementation against the approved plan

1. **Initialization:** read-only session opening, explicit optional guards,
   intelligible legacy parity errors, explicit NOT APPLICABLE for Forge's absent
   legacy inventory, and repaired archived-manifest reference.
2. **Queries:** one capture adapter, generated record index and A/B/C/D/S mission
   views, hash-based invalidation, in-memory fallback, ID selection, ambiguous
   harvest selection refusal, and existing-name/visibility refreshes. Raw captures
   and the stronger pinned jutsu-art census workflow are preserved.
3. **Context:** thin `scripts/tnr.py` entry point, an inspection pack rendered by
   the existing pack builder, short agent/bootstrap instructions, and scoped
   workstream initialization. No new database, service or orchestration framework.
4. **Enforcement:** repository consistency CI, reference/mirror checks, task-state
   validation, projection parity, generated-answer parity, and regression tests.
   Incoming push CI derives current answers because operator capture commits
   precede bot writeback; PR CI requires submitted generated artifacts to match.
   The answers workflow runs query regressions before publishing derived files.
5. **History:** small navigation digest, verbatim preservation of the September 20
   digest, dated historical workflow archive, installed workflow ownership, and a
   retained release-pin compatibility mirror. The unsafe assumption that name
   catalogs preserve complete capture history was removed from retention guidance.

## Sources and generated outputs

- Canonical capture adapter: `skills/building-tnr-content/scripts/record_index.py`.
- Producer: `.github/scripts/build_answers.py`; inputs are seed catalogs and inbox
  evidence. `answers/records.json` hashes the adapter and every inbox JSON.
- The record adapter admits only supported exact-record Forge procedures with
  DONE/success envelopes, successful full persistence, matching input/record IDs,
  record names and timezone-qualified timestamps. Invalid newer full evidence
  and conflicting equal-time evidence remain unresolved. Summary/legacy formats
  are counted as exclusions. No complete-population claim is inferred.
- This checks committed capture envelope/shape, not server authenticity or the
  originating manifest's execution identity. The jutsu-art workflow retains its
  stronger manifest and census checks; no extraction/source contract was adopted.
- Read-only context and queries do not write state or generated answers. Cache
  validity is based on source hashes; CI independently rebuilds output byte for byte.
- Names retain the seed/hot compatibility shape. Eligible full-record observations
  override seed fields; per-record provenance is in records.json. Seed dates are
  not rebranded as fresh live observations.
- Generated outputs: answer files/views, mission task pack/TOC, workstream Markdown,
  mounted instructions, global state projections, and the content skill ZIP.
- Root runtime configs, Forge/browser bundles, game manifests and art bytes are
  unchanged. The installed release workflow is unchanged; its retained mirror
  was made byte-identical by removing a compatibility comment.

## Validation

- `python3 scripts/tnr.py verify`: all repository consistency checks pass, including
  66 Python regression tests (43 existing jutsu-art tests plus 23 task/query/gate
  tests), workstream selftests/validation, routing, answers, state projections,
  doctrine, packs, and lawmap.
- From skill `data/`: `python3 ../scripts/selfcheck.py --generated .`: 0 errors;
  factory 20/20, validator consumes 16/16 check blocks, three runner-contract cases.
- From `forge/`: `node --test test/harvest.test.mjs test/release_loader.test.mjs`:
  17 tests pass, including existing legacy and Forge capture/readback behavior.
- Workflow YAML parses; Python modules compile; `git diff --check` passes.
- Packaging: deterministic skill ZIPs are regenerated after staging tracked inputs;
  root distribution contracts remain byte-identical to canonical sources.
- Retained pre-existing limitations: five law-classification warnings and the
  jutsu census's unresolved two-row universe discrepancy. These remain visible.
- Full Forge and Guide Studio suites were not rerun: their runtime implementations
  were unchanged. Focused integration tests cover the changed harvest interface.

## Rollout and review

Review this exact branch tip independently before integration under
`docs/DEVELOPMENT_WORKFLOW.md`. The capture adapter's conservative eligibility,
unknown-population reporting, generated-index currentness, and CI/bot-writeback
interaction deserve particular review attention.

After integration, replace the already-pasted ChatGPT Project Instructions with
`docs/agents/PROJECT_INSTRUCTIONS.md`. Repository edits cannot update that external
Project setting. Reinstall the generated content skill when using a packaged
installation. Checkout users and exact-commit readers use the repository directly.

Live-game requests: 0. Live-game writes: 0. No game credentials used. No browser,
installed mobile-session, or end-to-end ChatGPT-thread latency claim is made.
No history rewrite, runtime release, application deployment or live operation is
part of this change.
