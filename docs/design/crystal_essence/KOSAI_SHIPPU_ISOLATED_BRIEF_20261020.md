# Crystal Essence — Kōsai Shippū isolated-generation brief

**Workstream:** CRYSTAL ESSENCE — JUTSU ICONS (BR-020)  
**State:** TARGET LOCK DIRECTOR APPROVED; GENERATION NOT LAUNCHED.  
**Lead:** Image Production · **Support:** Art Director.  
**Frozen design authority:** `docs/design/crystal_essence/JUTSU_TARGET_LOCKS.json`, target lock SHA-256 `2d374ea676b47415bc6d17246c7e7540e044aa08187a2c5edd262610e7c2f3d5`.  
**Approval:** director, 2026-10-20: “Approved, proceed” to the proposed family treatment and Kōsai Shippū target lock. This does **not** approve any generated image, nor the four other targets.

## Technical launch gate — CLEARED (official ZIP-first doctor/intake/lock-check)

After receiving the official, exact Git-verified `dist/producing-tnr-art.zip`, the Art Studio ran the real `jutsu_studio.py doctor` (**RUN_CAPABLE_CANONICAL**), one bounded original ZIP `intake` (**5/5 MANIFEST_VERIFIED**, CRC OK, no issues), and `lock-check` against that generated `source_index.json` (**exit 0**). Kōsai is **DIRECTION_APPROVED**, and the four other complete reservations remain direction **PENDING**. Exact sources/hashes/commands and the non-blocking type normalization issue: `docs/design/crystal_essence/SOURCE_INTAKE_VERIFIED_20261020.md`. The source verification gate is now **CLOSED** for Kōsai; this does not imply real WebP exports, family gallery approval or `CANONICAL_PREFLIGHT` PASS. No new live capture was performed.

Reproduction commands (already executed successfully using the frozen official package and actual source ZIP):

~~~sh
python3 skills/producing-tnr-art/scripts/jutsu_studio.py doctor
python3 skills/producing-tnr-art/scripts/jutsu_studio.py intake BR-020_Crystal_Essence.zip --out WORK/crystal_essence/intake
python3 skills/producing-tnr-art/scripts/jutsu_studio.py lock-check docs/design/crystal_essence/JUTSU_TARGET_LOCKS.json --source-index WORK/crystal_essence/intake/source_index.json
~~~

Actual `lock-check` returned exit 0: Kōsai Shippū `DIRECTION_APPROVED` with lock SHA-256 `2d374ea676b47415bc6d17246c7e7540e044aa08187a2c5edd262610e7c2f3d5`; four other records complete/direction PENDING. The original source manifest's `jutsu_type` is BLOODLINE but `source_index.type` remains null due to a CLI field-name mapping gap; independently verified from the original manifest and committed historical `jutsu.get` captures. The source ZIP and approved image-reference bytes are preserved unchanged.

## Approved single-target composition (P0 A–F)

**Bloodline:** Crystal Essence · A · `ssevlOGQ4JjPn2sHZtq0c`.  
**Jutsu:** Kōsai Shippū · D · `igPSz82fa_L2XPrtnMvnz` · `BLOODLINE`.  
**Evidence:** successful `jutsu.get`, capture index 1 in `harvests/inbox/tnr_results_1792216502874.json`, 2026-10-17; historical, not 2026-10-20 live proof. Source description: enhanced speed and damaging crystal-laced shockwaves.

**Technique:** Three massive, staggered high-speed crystalline shockwave **crescents**, advancing as the active attack. The crystal is physically embedded into the traveling impact fronts, NOT floating decorative gems. Silhouette and motion must be unmistakable before color.

**Perspective and movement:** Shallow lateral three-quarter/front-side camera. Three distinct curved bands surge **left to right**, with dominant near-right collision emphasis and inky dark negative channels between the bands. Use the original's three-flight arc identity but REMOVE its human actor: the arcs themselves become the entire hero subject.

**Secondary effect:** Very restrained sharp trailing glass splinters suggesting momentum/recoil. Do not allow sparks, explosions or warm bloom to replace the three readable primary crescents.

**Approved family treatment:** LUMINOUS SILICATE / WARM-CORE REFRACTION — mineral glass, crisp premium TNR pixel outlines and planar cel shadows, teal/jade/cyan facets, bright tight sun-gold/amber internal refraction, predominantly navy/black designed opaque background. Source observed cool crystal and golden light; family organization approved by director. Not frosted, snowy or ice-sapphire BBE.

**Geometry exclusions:** Do not depict Jade's upright splitting chrysalis; Prism's one straight refracted beam; Sphere's closed circular defensive shell; Cave's upper/lower inward-closing teeth. No swords, snowflakes, frosted shackles, magical glyphs, rings, floating diamonds, scenery, labels, UI or watermarks. **ANATOMY EXCEPTION: NONE** — no people, limbs, hands or face.

**Visual acceptance:** Generate EXACTLY ONE square icon in a fresh, single-jutsu isolated conversation; inspect actual returned pixels versus action/camera/family P0 and at 125px / 64px / 32px. If wrong target/composition twice, reject and restart in a new clean session; don't condition on rejected images. The director must approve that exact candidate. Do not process, package, show a family gallery, edit repo or contact live game in the isolated session.

**Individual image reference for new isolated conversation:** exact `images/igPSz82fa_L2XPrtnMvnz_Kosai_Shippu.png` from original ZIP, SHA-256 `111319fe33b495e4cc5d68de8a67f3d5bc9d52d8185d096283403585d33e6bbd`, **IDENTITY ONLY**. If a second *separately attached actual approved* BBE/BEE exemplar is available, it may be **STYLE/MATERIAL ONLY**. The original ZIP, contact sheet, rejected generations and bare URL are never generator attachments.

**Live-game requests/writes:** 0/0 · **Credentials:** none.
