# TNR Jutsu Icon A/S/H — Prompt Desk Progress Tracker

**Status:** ACTIVE PROMPT DESK, initialized 2026-10-19 from director report. This is a PROMPT/TRACKING ledger only, **not** Bloodright art and **not** an Art Studio. It authorizes zero generation, QC, ZIP processing, game actions or publications.
**Population source:** Existing *public* A/S/H membership from historical director-approved 29-member census (`docs/design/bloodright/ICON_PRODUCTION_TRACKER.md` at `c85c1ea834e24315b5688f73a65c35479b8963e6`), **membership/rank only**. Bloodline IDs and ranks cross-checked against `docs/design/bloodright/trees/<slug>.json` on `tnr-tools main@4e674234d0539b7010c34025034330980a38b196`, whose tree legacy source is `7c1dfdd5e3ee163b90c22694dbb2de94ede08866`. This is a **historical planning roster**, not proof of current live kits. The Bloodright tracker's fixed three-emblem geometry/art status is NEVER inherited for these unique jutsu icons.
**Scope qualifier:** 29 *public* A/S/H bloodlines (19 A / 6 S / 4 H). The separate historical Bloodright census excludes hidden/deferred/excluded records. Do not silently add them here; director may explicitly expand membership.
**Startup counts:** 4 director-reported art-complete; 25 still to tackle (17 A / 4 S / 4 H); 1 of the 25 is a FULL RESTART (Houkyuken); 0 opening prompts authored by this new desk.
**Git-owned ledger:** `chatgpt/ash-jutsu-prompt-desk-20261019` at `docs/design/jutsu_icon_studio/TNR_ASH_JUTSU_PROMPT_PROGRESS.md` (ChatGPT sole writer; main unaffected unless separately merged).
**Bootstrap verification (2026-10-19):** `main@4e674234d0539b7010c34025034330980a38b196`; pinned census 29/29 members, 19 A / 6 S / 4 H; 29/29 tree metadata bloodline IDs, BR numbers and ranks individually matched. Name-label differences are known aliases only: Houkyuken/Hokyuken, BEE and BBE abbreviations.
**Desk state (2026-10-20, director milestone):** Director now reports **Bakuhatsu art complete**. The separate studio is independently evidenced at `chatgpt/bakuhatsu-jutsu-art-studio-20261019@68cff7db7d5cbac0db8e88e74f8dfe6a4b2ba5b4`, so its opening prompt moves `PROMPT_READY -> LAUNCHED`; the exact text pasted into that Studio is not independently proven. Its art state moves `NOT_STARTED -> DONE_DIRECTOR_REPORTED`. Prompts: **2 LAUNCHED**, **23 TO_DRAFT**, **4 NOT_REQUIRED**, **0 PROMPT_READY**. Art: **6 DONE_DIRECTOR_REPORTED**, **22 NOT_STARTED**, **1 ABANDONED_RESET**. Total public cohort **29 / 6 director-done / 23 remaining** (A 19/4/15; S 6/2/4; H 4/0/4). Pinned Bakuhatsu Studio documents **5/5 raw approvals**; local export QC, canonical preflight, accepted gallery, ZIP delivery, Git binary pin and live readback remain **NOT_RUN / NOT_BUILT / NOT_PERFORMED** at its checked head; no missing acceptance evidence is inferred from “complete.” Other completed-family caveats remain unchanged. No next target selected or prompt drafted; Crystal Essence is a suggestion only. This Prompt Desk made repository-only reads/writes, zero live-game requests/writes; credentials none.

## Status meaning and edits

- **Prompt status**: `NOT_REQUIRED` (already art-complete), `TO_DRAFT`, `PROMPT_READY` (copy-ready opener delivered), `LAUNCHED` (director confirms it was used), or `REVISION_NEEDED`. Do not mark LAUNCHED because a prompt was merely written.
- **Art status**: `DONE_DIRECTOR_REPORTED` (user asserts finished; **not** a blanket canonical gallery/preflight/upload claim), `NOT_STARTED`, `ABANDONED_RESET` (older art unusable), `STUDIO_ACTIVE`, `STUDIO_CLOSED` (requires a returned studio handoff). The Prompt Desk does not itself certify raw, export, gallery or game gates.
- **Prompt SHA/session:** When handing off an opener, append the exact new prompt file/commit (if Git-backed) and a new studio thread/branch ref **only after confirmed**. Never invent links/SHAs. Maintain one prompt and one art studio at a time unless director changes order.
- **Update discipline**: Only after director action or a verifiable returned Studio closeout. Keep provenance/gates separate from art-completion status. Update a row and the count totals together. This tracker has exactly one ChatGPT writer at a time; do not edit Fable branches.

## Campaign roster (exact historical IDs — verify on intake)

| Rank | Bloodline (historical source) | BR | Bloodline ID | Prompt | Art state | Note |
| :---: | --- | --- | --- | --- | --- | --- |
| A | [Aerathiel](../bloodright/trees/aerathiel.json) | BR-002 | `1C34syOOEKp6k3UKweYT6` | NOT_REQUIRED | DONE_DIRECTOR_REPORTED | Director says finished; 5 processed exports pinned. Exact-gallery acceptance remains PENDING; further gates separate. |
| A | [Arashima](../bloodright/trees/arashima.json) | BR-005 | `9F6Ruhuf82gSzpZcsUaPW` | TO_DRAFT | NOT_STARTED | — |
| A | [Bakuhatsu](../bloodright/trees/bakuhatsu.json) | BR-008 | `RNUcHSH2c00IhOLc2C9aJ` | LAUNCHED | DONE_DIRECTOR_REPORTED | Director 2026-10-20: “Bakuhatsu complete.” Opener [`prompts/BAKUHATSU_STUDIO_OPENER_20261019.md`](prompts/BAKUHATSU_STUDIO_OPENER_20261019.md) @ `7c6d269381ba080c7a63c8c19ef699ed7acd1f1d`; evidenced Studio `chatgpt/bakuhatsu-jutsu-art-studio-20261019@68cff7db7d5cbac0db8e88e74f8dfe6a4b2ba5b4`: 5/5 raws approved, CONCUSSIVE FRACTURE family treatment approved, canonical preflight NOT_RUN, final export/gallery NOT_BUILT, gallery acceptance unproven, ZIP user delivery not evidenced, Git binaries not pinned, no live upload/readback. No Studio terminal closeout handoff confirmed. |
| A | [Crystal Essence](../bloodright/trees/crystal_essence.json) | BR-020 | `ssevlOGQ4JjPn2sHZtq0c` | TO_DRAFT | NOT_STARTED | — |
| A | [Heavenly Sonata](../bloodright/trees/heavenly_sonata.json) | BR-032 | `clh4d6q6s000atb0h0qdqdh1z` | TO_DRAFT | NOT_STARTED | — |
| A | [Houkyuken (Hokyuken)](../bloodright/trees/houkyuken.json) | BR-033 | `ALoGrHuBY5Ml9bJG_DILe` | TO_DRAFT | ABANDONED_RESET | FULL RESET: director rejects all earlier generated art/direction. Do not salvage/use any generated images from old studio. Legacy originals may be used as IDENTITY ONLY. |
| A | [Hyouga Yui](../bloodright/trees/hyouga_yui.json) | BR-034 | `lPcN4q0dtX2muWT2KlXGg` | TO_DRAFT | NOT_STARTED | — |
| A | [Itojinsei](../bloodright/trees/itojinsei.json) | BR-036 | `j4_9ypNqYq8Ifbqf-9D2r` | TO_DRAFT | NOT_STARTED | — |
| A | [Kyuko-sei](../bloodright/trees/kyuko_sei.json) | BR-040 | `Y10fxyLR39IBJ3ICkAdEp` | TO_DRAFT | NOT_STARTED | — |
| A | [Oblivion Seal](../bloodright/trees/oblivion_seal.json) | BR-053 | `wasIGmDuczwD9PB89gML6` | TO_DRAFT | NOT_STARTED | — |
| A | [Shadow Weaver](../bloodright/trees/shadow_weaver.json) | BR-063 | `d0WYPbbsVx7Y_i0fddwxc` | TO_DRAFT | NOT_STARTED | — |
| A | [Shakunetsu Sakura](../bloodright/trees/shakunetsu_sakura.json) | BR-064 | `aa1lZukkHpz6ihmcxLaei` | TO_DRAFT | NOT_STARTED | — |
| A | [Shinrai Ou](../bloodright/trees/shinrai_ou.json) | BR-065 | `xO4Dycx7FFEqxwvAEXBxY` | TO_DRAFT | NOT_STARTED | — |
| A | [Shinseina Ki](../bloodright/trees/shinseina_ki.json) | BR-066 | `vA8I_7iBNgvkuKOpnG1yD` | LAUNCHED | DONE_DIRECTOR_REPORTED | Director 2026-10-19: “Shinseina Ki complete.” Opener [`prompts/SHINSEINA_KI_STUDIO_OPENER_20261019.md`](prompts/SHINSEINA_KI_STUDIO_OPENER_20261019.md) @ `ef6533f87f1d2e8075c3a6f88abdb881bf91157a`; separate studio branch `chatgpt/shinseina-ki-jutsu-art-studio-20261019@b527aa39e1af6f6c883effeb01534d2277b0bbb8`; 5/5 raw approvals, 5/5 canonical preflight PASS as recorded, gallery acceptance PENDING, Wood Warrior anatomy-exception reconciliation PENDING, ZIP user delivery not proven, binaries not Git-pinned, game upload/readback not proven. No verifiable final closeout handoff yet. |
| A | [Suragu](../bloodright/trees/suragu.json) | BR-074 | `Ksb6ogNqc5mp4l_hRgPuW` | TO_DRAFT | NOT_STARTED | — |
| A | [Taiyo Kami](../bloodright/trees/taiyo_kami.json) | BR-075 | `6C2t3jK35hvPoVocLiHEl` | TO_DRAFT | NOT_STARTED | — |
| A | [Teno Yuki](../bloodright/trees/teno_yuki.json) | BR-077 | `clh4d6qjs000gtb0hr357gjvv` | TO_DRAFT | NOT_STARTED | — |
| A | [Tenohira Musei](../bloodright/trees/tenohira_musei.json) | BR-078 | `18Byy1tMXkQETmB88JLl5` | TO_DRAFT | NOT_STARTED | — |
| A | [Vaporia](../bloodright/trees/vaporia.json) | BR-090 | `f7IgtcsLqomqmmBgAYS1O` | NOT_REQUIRED | DONE_DIRECTOR_REPORTED | Director says finished; 5 exports pinned. Historical exact final-gallery approval unproven. |
| S | [Blood-Enchanted Eyes (BEE)](../bloodright/trees/blood_enchanted_eyes.json) | BR-011 | `ovZIWu28ANn-Cij5TjT8S` | NOT_REQUIRED | DONE_DIRECTOR_REPORTED | Director says finished; 8 style WebPs indexed. Sanguine Plague v3 is PROVENANCE_PARTIAL. |
| S | [Blue Blade Eyes (BBE)](../bloodright/trees/blue_blade_eyes.json) | BR-015 | `clh4d6qo4000itb0hrx8t06wq` | NOT_REQUIRED | DONE_DIRECTOR_REPORTED | Director says finished; 8 style WebPs indexed. No live upload/readback inferred. |
| S | [Cosmic Ascendant](../bloodright/trees/cosmic_ascendant.json) | BR-018 | `osVXxtyW61gr-bx5v5ys2` | TO_DRAFT | NOT_STARTED | — |
| S | [Ethereal Monarch](../bloodright/trees/ethereal_monarch.json) | BR-023 | `IxhIoLEmznqdcnc_6MCN9` | TO_DRAFT | NOT_STARTED | — |
| S | [Eyes of the Forsaken King](../bloodright/trees/eyes_of_the_forsaken_king.json) | BR-027 | `r3nBY_Th4_ZAIUfhx1jdy` | TO_DRAFT | NOT_STARTED | — |
| S | [Shiroi Youso](../bloodright/trees/shiroi_youso.json) | BR-067 | `vv45N2En3p8VrNcU2acd8` | TO_DRAFT | NOT_STARTED | — |
| H | [Godstorm Eclipse](../bloodright/trees/godstorm_eclipse.json) | BR-029 | `szai-IgtB7PLubojIIlh-` | TO_DRAFT | NOT_STARTED | — |
| H | [Night Parade of A Thousand Demons](../bloodright/trees/night_parade_of_a_thousand_demons.json) | BR-051 | `r_99Xg8SIOYw2awCMSR7e` | TO_DRAFT | NOT_STARTED | — |
| H | [Sands of Time](../bloodright/trees/sands_of_time.json) | BR-059 | `yzbSbZ5rqRVIjiwN-farx` | TO_DRAFT | NOT_STARTED | — |
| H | [Tetsugan](../bloodright/trees/tetsugan.json) | BR-083 | `T-MyR4yQ1_aVbaJDLoI07` | TO_DRAFT | NOT_STARTED | — |

## Prepared openings (verified milestones)

| Date | Bloodline | Prompt | Art Studio | Evidence |
| --- | --- | --- | --- | --- |
| 2026-10-20 | Bakuhatsu (A, BR-008, `RNUcHSH2c00IhOLc2C9aJ`) | **LAUNCHED** (independent Studio evidence; exact pasted opener unverified) | **DONE_DIRECTOR_REPORTED** | Director reports art complete. Original prompt `prompts/BAKUHATSU_STUDIO_OPENER_20261019.md@7c6d269381ba080c7a63c8c19ef699ed7acd1f1d`; Studio `chatgpt/bakuhatsu-jutsu-art-studio-20261019@68cff7db7d5cbac0db8e88e74f8dfe6a4b2ba5b4`, five current exact raw approvals including Howitzer v3 (v1/v2 rejected). Last register: family export/QC/canonical preflight NOT_RUN, final deterministic gallery NOT_BUILT, ZIP user delivery NOT_BUILT, Git binaries and game readback NOT_PERFORMED. Art completion is not a claim those gates passed. |
| 2026-10-19 | Shinseina Ki (A, BR-066, `vA8I_7iBNgvkuKOpnG1yD`) | **LAUNCHED** (Studio evidenced; exact pasted prompt unverified) | **DONE_DIRECTOR_REPORTED** | Director 2026-10-19 reports completed art. Opening document `prompts/SHINSEINA_KI_STUDIO_OPENER_20261019.md` @ `ef6533f87f1d2e8075c3a6f88abdb881bf91157a`; Studio `chatgpt/shinseina-ki-jutsu-art-studio-20261019@b527aa39e1af6f6c883effeb01534d2277b0bbb8` with five original visual approvals, five current processed outputs and reported pinned canonical preflight PASS. Exact gallery family acceptance PENDING and Wood Warrior anatomy exception unresolved; final closeout/user delivery NOT VERIFIED. Historical kit `docs/design/bloodright/kits/shinseina_ki.json@7c1dfdd5e3ee163b90c22694dbb2de94ede08866`, not current-live proof. |

**Bakuhatsu observed Studio:** `chatgpt/bakuhatsu-jutsu-art-studio-20261019@68cff7db7d5cbac0db8e88e74f8dfe6a4b2ba5b4`, `docs/design/bakuhatsu/JUTSU_ICON_REGISTER.md` and `JUTSU_TARGET_LOCKS.json`. Historical source ZIP `BR-008_Bakuhatsu.zip` SHA-256 `7944d75ab09950d89fa927fec9fe5421d58eb29de36dd986e17c420ad2d18a24`; 5/5 source/lock and raw approvals. Howitzer Crash final is V3 MACH-SHEAR BOW SHOCK; V1/V2 failed and are ineligible references. Technical gates at checked head: `OUTPUT_LOCAL_QC: NOT_RUN`, `CANONICAL_PREFLIGHT: NOT_RUN`, `FAMILY_SHOWCASE_ACCEPTED: NOT_BUILT`, `ZIP_DELIVERED: NOT_BUILT`, `GIT_BINARY_PIN: NOT_PERFORMED`, `USER_UPLOAD_READBACK: NOT_PERFORMED`. Keep the director's completed-art report distinct from these missing gates; do not invent later Studio closeout evidence.

**Shinseina Ki observed Studio:** `chatgpt/shinseina-ki-jutsu-art-studio-20261019@b527aa39e1af6f6c883effeb01534d2277b0bbb8`, source intake and five per-target locks evidenced. `JUTSU_ICON_REGISTER.md` records 5/5 raw visual approvals, 5/5 local QC PASS and canonical `artpreflight --type JUTSU_ICON` PASS. A deterministic 3+2 WebP-source gallery has a technical audit VALID, but **exact director family-gallery acceptance remains PENDING**, as does the image-specific Wood Warrior anatomy exception. v1 archives are **BUILT_NOT_DELIVERED** in pinned evidence, binary ZIP/image bytes **NOT_GIT_PINNED**, no verified user upload/readback; do not treat the director's art-complete report as those gates passing. An actual final Studio closeout handoff is not yet in this desk's records.

**Next suggestion (not director-selected):** Crystal Essence, A-rank / BR-020 / `ssevlOGQ4JjPn2sHZtq0c`. Rank, name and ID are read from `docs/design/bloodright/trees/crystal_essence.json@main:02a288e966db27f427508734a6223e0e583b081a`; historical kit `docs/design/bloodright/kits/crystal_essence.json@7c1dfdd5e3ee163b90c22694dbb2de94ede08866` is comparison-only, not current-live evidence. Why next: crystalline material study offers contrast to Bakuhatsu's explosive fracture and Shinseina's wood; reserve distinct techniques and avoid copying BBE's ice silhouettes. **No Crystal Essence opener, ZIP intake or Studio has begun.**

## Milestone snapshot

| Rank | Total | Art done (director-reported) | Remain |
| --- | ---: | ---: | ---: |
| A | 19 | 4 | 15 |
| S | 6 | 2 | 4 |
| H | 4 | 0 | 4 |
| **TOTAL** | **29** | **6** | **23** |

**Explicit director reset:** Houkyuken/Hokyuken earlier art session was not salvageable; discard all old generated candidates, prior purported approvals and the previous visual direction. A fresh future ZIP-first Studio must start with legacy source originals (IDENTITY ONLY), independent pinned style/material examples, new technique/action silhouette reservations and a new director-approved lock. The earlier session is historical rejection evidence only, not a source of approved final jutsu artwork.

**Reference caveat:** BBE/BEE have 16 pinned style exemplar WebPs (BEE Sanguine Plague v3 `PROVENANCE_PARTIAL`); Vaporia/Aerathiel have ten Git-pinned *processed production exports* in `art/jutsu_icons/` but are not indexed as `style_refs` by default. Exact current source and any approval/reuse of reference pixels must be verified by the actual future Studio.

**Production gate caveat:** In particular, Aerathiel exact-gallery signoff remains PENDING. An independently reported clean preflight on pinned exports must not be silently promoted to a historical canonical gate without appropriate pinned/evidence reconciliation. No user live-game writes/readback have been verified in this campaign.

## Prompt Desk operating loop

1. Reverify current main and campaign roster changes; show a 1-line progress summary without rescanning every bloodline. The historical list is a candidate queue, not current-live census.
2. Director picks ONE target, or supplies its original-art ZIP name. Read **that target's** source-backed rank/ID and current `docs/workflows/BLOODLINE_JUTSU_ICON_STUDIO.md`, `docs/workflows/ISOLATED_ART_GENERATION.md`, and `docs/design/jutsu_icon_studio/START_PROMPT.md` on the latest main.
3. Produce one copy-ready **new persistent Art Studio opening prompt** that directs the Studio to attach the original-art ZIP, perform safe intake and exact jutsu/ID mapping, create a family treatment card and target silhouette ledger, and propose the first isolated-generation brief; explicitly **NO image generation in the startup turn**.
4. Log `PROMPT_READY` only when the copy-ready opener exists. Log `LAUNCHED` only when director confirms its actual Studio start. Subsequent Art Studio production is entirely in its own conversation(s), not this Prompt Desk.
5. When the Studio returns a verifiable closeout or the director says art is finished/abandoned, update progress; **never** merge artistic completion with canonical preflight, gallery approval, Git binary pin, upload or live publication.

**No fixed processing order:** Rank section is inventory, not imposed production priority. Director chooses the next bloodline. Once one is selected, do not prepare 24 other elaborate prompts in the same turn.