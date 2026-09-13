# Fable / Astra implementation brief — TNR Guide Studio MVP

## Status
Design/product direction is locked for implementation planning at `docs/design/GUIDE_STUDIO_PRODUCT_SPEC.md` v1.1. Do not begin by changing TheNinjaRPG or Forge.

## Objective
Build a standalone, mobile-first Guide Studio that lets a player:

**visit link → select bloodline → enter author name → choose build jutsu → explain how the build works → preview → submit**

The app must produce an Aerathiel/Night Parade-series guide without requiring players to locate/upload official game art, type mechanics, or author the general bloodline explanation from scratch.

## Product correction from director review
The original skeleton was too bare and the strategy form felt too generic. Implement the following as required behavior:

1. **Complete automatic bloodline foundation.** Selecting a bloodline automatically supplies:
   - two concise general-description/introduction paragraphs;
   - hero art;
   - Bloodline Overview copy + overview art/infographic;
   - the complete core bloodline kit;
   - any required special-mechanic module, such as Night Parade summons.
   A template is not publishable to players if this foundation is incomplete.

2. **Core kit is independent of player loadout.** The full bloodline kit always renders regardless of what the author selects for their build. Player selection creates a separate build/loadout layer; it never determines which bloodline jutsu exist in the guide.

3. **`HOW I USE IT` is acceptance-critical.** Every selected build jutsu has an obvious inline, autosaved `HOW I USE IT` text area. Do not hide this behind a separate generic strategy form. If a selected jutsu is already present in the core kit, prefer a compact build-reference card with the player's note rather than duplicating a giant mechanic card; repeating the full card is acceptable for MVP if simpler.

4. **Strategy authoring must feel like guide writing, not a survey.** Use template-driven strategy chapters rather than bland hard-coded categories. Default chapter family:
   - Build Philosophy
   - The Core Loop
   - Opening Moves
   - Defense & Recovery
   - Pressure Windows
   - Key Synergies
   - Adaptation & Matchups
   - Mistakes to Avoid
   Templates may rename/reorder/hide chapters to fit the bloodline. Final rendering should read as guide subsections, not answered questions. Blank optional chapters do not render.

5. **Kinjutsu: Black Thorn Rose mechanic correction.** Do not classify it as damage. Its Guide Studio display must represent:
   - self `DAMAGE TAKEN` reduction;
   - enemy `HEALING REDUCTION`.
   Add a regression fixture/test proving no damage-dealt classification is rendered for this jutsu. Effect normalization must retain target semantics generally so self mitigation cannot be flattened into offensive damage.

## Governing product spec
`docs/design/GUIDE_STUDIO_PRODUCT_SPEC.md` on the ChatGPT design branch.

Aerathiel is the presentation reference. Night Parade is the special-mechanic exemplar.

## Architecture constraints
- Hosted outside TheNinjaRPG domain.
- Cloudflare is intended deployment target; operator handles account/DNS/deployment credentials.
- No TNR login or session integration.
- No game mutations.
- Ordinary public authoring makes zero TNR API calls.
- Build/refresh tooling may create a static catalog from existing public read-only `jutsu.getAll` and `bloodline.getAll`.
- Static catalog/template versions are pinned in each submission.
- Official images are automatic from catalog/template.
- Player image upload is only for optional combat highlights.
- Submission endpoint validates server-side and delivers intake to a Discord webhook kept only as a Worker secret.

## Suggested Cloudflare MVP
- Pages: frontend + static catalogs/templates.
- Worker or Pages Function: `/api/submit`.
- R2: submission JSON + optional highlights.
- Turnstile: submission abuse control.
- Secret: Discord guide-intake webhook.

## Required screens
1. Template selector showing only complete/published bloodline templates.
2. About / author name.
3. Build-loadout picker with a clear `Full bloodline kit included automatically` state, searchable jutsu catalog, automatic image/mechanics, reorder, and inline per-jutsu `HOW I USE IT`.
4. Guide-chapter strategy authoring using template-driven `strategyBlocks`.
5. Optional combat highlights.
6. Real guide preview containing the automatic foundation plus player-authored build layer.
7. Submission checklist + receipt.

## Required renderer behavior
- General bloodline description, hero, overview, complete core kit, and required special modules render from the selected template before player-authored build content.
- Core-kit membership comes from the template, not from selected loadout IDs.
- Selected external/support jutsu render with official mechanics plus `HOW I USE IT`.
- Selected core-kit jutsu may use a compact reference + `HOW I USE IT` to avoid unnecessary mechanic duplication.
- Same component renderer powers preview and publication.
- Mechanics never come from player-entered values.
- Blank optional strategy chapters do not render.
- Text is always escaped/sanitized as text, not trusted HTML.

## Required player-facing behavior
- Mobile-first at 360px.
- Local autosave and restore, including per-jutsu usage notes.
- No freeform page design.
- Loadout screen copy should make the ownership split obvious: **Your full bloodline kit is already included. Choose the jutsu that define your build.**
- `HOW I USE IT` must be reachable directly from each selected jutsu without a modal-only workflow.
- Strategy inputs should look and read like composing chapters of the finished guide.

## Initial templates
- Aerathiel.
- Night Parade of a Thousand Demons.

Neither template should be exposed publicly until its locked introduction, overview, complete core kit, required special modules, and official assets are present.

## Catalog proof
Pinned TNR source `studie-tech/TheNinjaRPG@36c5873b7b6ee5fd3af717008d7c51b0f185b756` exposes:
- `jutsu.getAll` as a public paginated full-record query with `limit <= 1000`;
- `bloodline.getAll` as a public paginated full-record query with `limit <= 500`.

The deployed browser must consume generated static snapshots, not call these endpoints itself.

Catalog normalization must preserve target semantics in addition to effect type. Do not infer player-facing tags from effect names alone when target/direction changes meaning.

## Testing expectations
At minimum:
- renderer/effect-normalization fixtures;
- template completeness/schema validation tests;
- complete core-kit always renders even with an empty or unrelated selected loadout;
- player loadout cannot remove/alter core-kit membership;
- inline `HOW I USE IT` entry, persistence, preview, and submission;
- Kinjutsu: Black Thorn Rose fixture: self `DAMAGE TAKEN` reduction + enemy `HEALING REDUCTION`, and no damage-dealt classification;
- autosave recovery;
- jutsu search/add/remove/reorder;
- unknown/stale IDs rejected on submit;
- blank optional strategy chapters omitted;
- text escaping/XSS tests;
- image type/size/count checks;
- responsive/mobile interaction smoke;
- submit Worker unit/integration test with Discord transport mocked;
- no TNR mutation routes/imports;
- no TNR credential/session handling.

## Live statement
Implementation and tests require no live game writes and no live credentials. Any catalog refresh is public read-only and should be separately identifiable from application runtime.

## Handoff
Return exact base/head SHAs, full test commands/results, deployment assumptions, generated catalog provenance, template completeness status for Aerathiel and Night Parade, and any browser/Cloudflare behavior that remains unverified.
