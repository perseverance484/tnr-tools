# One Perfect Crop — hidden core-manifest override

**Date:** 2026-09-16  
**Status:** ACTIVE director ruling for the hidden core-manifest path  
**Scope:** One Perfect Crop only  
**Live-game authority:** dauntless only

## Ruling

The project may proceed now to a **hidden core manifest** even though the final art pack and content-admin values are unfinished.

For this core build:

1. **Missing art does not gate the manifest.** Where an art/image/scene field is intentionally not authored, the current builder/game create-path placeholder may stand. The core manifest must not add `@img` references, new asset entries, or fabricated scene ids merely to make the build look complete.
2. **Content-admin values remain deferred.** Ryo, XP, other currencies, Cabbage Seed rarity/type/economics, repeatability, and eligibility are not decided by this ruling.
3. **Do not invent deferred values.** The core manifest may rely on the current create-path defaults for unresolved quest-admin fields only as reversible hidden-state placeholders. Those defaults are not accepted balance/content.
4. **Do not create Cabbage Seed yet.** The item contract requires user-owned type/rarity/economic choices. The core manifest therefore contains no Cabbage Seed item entry and no Cabbage Seed reward grant. A later launch-final patch adds the item and final reward package after the admin task closes.
5. **Preserve all finished gameplay/content.** The frozen prose/graph, two dialog-gated `start_battle` encounters, hard-fail loss routes, Road Bandit AI/profile, Harvest Boar AI/profile, shared-jutsu ids, and one-enemy encounter contracts remain exact.
6. **Everything stays hidden.** This ruling authorizes repository implementation/review of the core manifest, not publishing. Any live execution remains a separate user-owned action after independent review.
7. **Launch finalization remains mandatory.** Before any publish/unhide decision, the deferred art/admin work must be completed or explicitly accepted as final, a launch-final patch must be independently reviewed, and hidden-state readback must be clean.

## Relationship to older sources

`state/plan_one_perfect_crop_finish.md` remains authoritative for the frozen story/encounter design, accepted art intent, and launch-final expectations.

Its older Phase C/D statement that unresolved admin/art must block **any** runnable manifest is superseded only for this new hidden core-manifest path. It still applies to launch-final readiness.

`state/one_perfect_crop_content_admin_open.md` remains the authoritative list of unresolved launch-final admin choices. None of those choices is resolved by this override.

The submitted `Farming level 15` requirement remains unresolved. It must not be silently translated to character level 15.

## Core-manifest consequence

The core manifest is intentionally a reversible hidden skeleton with complete gameplay and combat content but temporary visual/admin defaults. It is suitable for repository integration and independent review. It is not, by itself, approval to publish or a claim that the event's rewards, eligibility, repeatability, item definition, or final art are complete.
