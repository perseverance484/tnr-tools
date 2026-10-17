# Copy-ready — Start a Bloodline Jutsu Icon Art Studio

**Attach one original bloodline jutsu-art ZIP** to a new TNR Tools project conversation. The short mobile prompt is sufficient; the expanded version below is available when a new thread needs more explicit guardrails. No extra reference screenshots, style ZIP or separate manifest are needed: the approved BBE/BEE style exemplars are pinned in the repository, and a ZIP without its own `manifest.json` only needs the roster (jutsu_id, name) pasted under the prompt.

**Ref:** the tooling and pinned exemplars live on `claude/bloodline-jutsu-icon-studio-3nmvc2` until it is integrated; afterwards use `main`. Replace the ref line below accordingly.

## Preferred short mobile prompt

~~~text
Repository: perseverance484/tnr-tools
Ref (main once integrated):
claude/bloodline-jutsu-icon-studio-3nmvc2
Task: BLOODLINE JUTSU ICON ART STUDIO, ZIP-FIRST.
Input: attached original bloodline jutsu-art ZIP.

Verify live refs; read required TNR bootstrap plus
docs/workflows/BLOODLINE_JUTSU_ICON_STUDIO.md (§8),
ISOLATED_ART_GENERATION.md and JUTSU_ICON_SHOWCASE.md
from their verified exact refs. Batch repo reads.
Run jutsu_studio.py intake on the ZIP (one call);
report exact names/IDs/N; open the actual originals.
Style: pinned exemplars via style_refs.py select
--target JUTSU_ICON, STYLE ONLY; attach real bytes or
say they were not attached.
Return one compact inventory, family treatment card,
one UNIQUE technique-first silhouette for every jutsu,
and the first proposed isolated-generation brief.
Actors only when necessary; full-bleed opaque is fine.
This is NOT Bloodright. NO generation in this initial
studio turn, no live game requests/writes.
~~~

## Expanded initialization prompt

~~~text
Repository: perseverance484/tnr-tools
Workflow Branch: chatgpt/bloodline-jutsu-studio-zip-first-20261017
(This workflow is not yet integrated into main; retrieve it from this branch at its verified exact head if absent on main.)
Session: BLOODLINE JUTSU ICON ART STUDIO — ZIP-FIRST
Input: attached bloodline original-art ZIP
Lead: ChatGPT Art Director | Support: Image Production

Bootstrap:
- Verify live main and relevant branch exact SHA.
- Read required repo state/authority and
  docs/workflows/BLOODLINE_JUTSU_ICON_STUDIO.md
  docs/workflows/ISOLATED_ART_GENERATION.md
  docs/workflows/JUTSU_ICON_SHOWCASE.md
  and current art skill/JUTSU_ICON spec.
- Batch repository reads. Run ONE
  `jutsu_studio.py intake <ZIP> --out work/intake`
  (add --roster if the ZIP has no manifest.json): safe
  inventory, hash/decoder check, exact ID/name mapping.
- Inspect actual extracted reference images; never
  assume the generator can see pixels inside a ZIP.
- Style: `style_refs.py select --target JUTSU_ICON`
  picks a pinned director-approved BBE/BEE exemplar,
  STYLE/MATERIAL ONLY. Attach its actual bytes; a URL
  is not an attached image. Its silhouette is reserved.

Direction:
- Establish bloodline-specific palette/material.
- Technique first; actors only if necessary.
- Reserve ONE distinctive primary silhouette per jutsu.
- Strong 125/64/32 readability; avoid lookalike effects.
- Opaque designed backgrounds are allowed.
- This is NOT the three-icon Bloodright reskin workflow.

FIRST REPLY ONLY:
- Compact N-row inventory (name, ID, image, status).
- One family treatment card and N-silhouette ledger.
- Exact missing/mismatched entries, if any.
- Recommend first single-jutsu isolated-generation target.
- Ask for director direction approval if not already given.

Production:
- Persistent Studio coordinates; ONE clean isolated
  generation session per unique jutsu, using 1–2
  individually attached, role-labeled references.
- On visual approval preserve exact raw bytes.
- Once N/N accepted, fill approved.json from
  approved_template.json and run ONE
  `jutsu_studio.py finalize approved.json --out work/final`
  (exports, real JUTSU_ICON preflight, adaptive showcase,
  closeout + upload ZIPs); then get family acceptance.
- Do not apply BBE's under-80000 cap to other families
  unless separately approved.
- Do not upload, edit or publish in the live game.
- Avoid redundant GitHub fetches or repository writes
  after every candidate; keep checkpoints durable.
- Report actual validation results, not inferred PASS.

Begin ZIP-FIRST STUDIO BOOTSTRAP. No image generation
in this initial Art Studio turn.
~~~
