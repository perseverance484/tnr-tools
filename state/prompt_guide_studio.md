# Fable implementation brief — TNR Guide Studio MVP

## Status
Design/product direction is locked for implementation planning. Do not begin by changing TheNinjaRPG or Forge.

## Objective
Build a standalone, mobile-first Guide Studio that lets a player:

**visit link → select bloodline → enter author name → choose loadout → write strategy → preview → submit**

The app must produce Aerathiel-series guide data without requiring players to locate/upload official game art or type mechanics.

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
1. Template selector.
2. About / author name.
3. Loadout picker with search, automatic image/mechanics, reorder, per-jutsu `How I use it`.
4. Guided strategy prompts.
5. Optional combat highlights.
6. Real guide preview.
7. Submission checklist + receipt.

## Required player-facing behavior
- Mobile-first at 360px.
- Local autosave and restore.
- No freeform page design.
- Same component renderer powers preview and publication.
- Mechanics never come from player-entered values.
- Blank optional strategy prompts do not render.
- Text is always escaped/sanitized as text, not trusted HTML.

## Initial templates
- Aerathiel.
- Night Parade of a Thousand Demons.

## Catalog proof
Pinned TNR source `studie-tech/TheNinjaRPG@36c5873b7b6ee5fd3af717008d7c51b0f185b756` exposes:
- `jutsu.getAll` as a public paginated full-record query with `limit <= 1000`;
- `bloodline.getAll` as a public paginated full-record query with `limit <= 500`.

The deployed browser must consume generated static snapshots, not call these endpoints itself.

## Testing expectations
At minimum:
- renderer/effect-normalization fixtures;
- schema validation tests;
- autosave recovery;
- jutsu search/add/remove/reorder;
- unknown/stale IDs rejected on submit;
- text escaping/XSS tests;
- image type/size/count checks;
- responsive/mobile interaction smoke;
- submit Worker unit/integration test with Discord transport mocked;
- no TNR mutation routes/imports;
- no TNR credential/session handling.

## Live statement
Implementation and tests require no live game writes and no live credentials. Any catalog refresh is public read-only and should be separately identifiable from application runtime.

## Handoff
Return exact base/head SHAs, full test commands/results, deployment assumptions, generated catalog provenance, and any browser/Cloudflare behavior that remains unverified.
