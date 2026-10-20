# Crystal Essence — Kōsai Shippū isolated-generation brief

**Workstream:** CRYSTAL ESSENCE — JUTSU ICONS (BR-020)  
**State:** TARGET LOCK DIRECTOR APPROVED; GENERATION NOT LAUNCHED.  
**Lead:** Image Production · **Support:** Art Director.  
**Frozen design authority:** `docs/design/crystal_essence/JUTSU_TARGET_LOCKS.json`, target lock SHA-256 `2d374ea676b47415bc6d17246c7e7540e044aa08187a2c5edd262610e7c2f3d5`.  
**Approval:** director, 2026-10-20: “Approved, proceed” to the proposed family treatment and Kōsai Shippū target lock. This does **not** approve any generated image, nor the four other targets.

## Technical launch gate — NOT YET CLOSED

The source ZIP has passed independent local inspection, and 5/5 jutsu IDs/names and source images match the committed historical capture. However the prescribed installed `producing-tnr-art` runtime and matching full repository checkout are **not present** in this isolated container; `jutsu_studio.py doctor`, `intake`, and `lock-check` remain **NOT_RUN**. The source is **not** canonically intake-certified, and production preflight has not run. A new generation session must wait until a compatible environment produces a successful canonical doctor/intake source index and confirms the first target's lock against that index (additional four target locks remain pending; missing future locks are expected, not currently approved). Do not fabricate a PASS or treat a manual manifest read as a canonical CLI result. No need to obtain new live captures: sources are committed and explicitly historical.

Required local commands in a matching checkout/installed skill:

~~~sh
python3 skills/producing-tnr-art/scripts/jutsu_studio.py doctor
python3 skills/producing-tnr-art/scripts/jutsu_studio.py intake BR-020_Crystal_Essence.zip --out WORK/crystal_essence/intake
python3 skills/producing-tnr-art/scripts/jutsu_studio.py lock-check docs/design/crystal_essence/JUTSU_TARGET_LOCKS.json --source-index WORK/crystal_essence/intake/source_index.json
~~~

The CLI may report `LOCK_INCOMPLETE` for the four not-yet-approved jutsu: verify **Kōsai Shippū specifically** is approved with its matching lock hash. Current ZIP manifest rows provide `jutsu_type`; the CLI source index currently extracts `type`, so additionally cross-check BLOODLINE type against committed `jutsu.get` captures instead of treating an absent source-index type as proof of a different jutsu type. Do not modify the original ZIP.

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
