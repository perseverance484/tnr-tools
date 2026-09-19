# Forge Presentation Studio — design contract

**Revision:** 1, 2026-09-19. **Status:** complete design proposal for director acceptance; not an implementation or release approval.

**Owner:** ChatGPT, Content Designer; UI/UX Reviewer, Art Director and Engineering Auditor lenses.

**Branch/base:** `chatgpt/forge-presentation-studio-design`, based on `main@eefefd1afd67111a90c332951a8dd9f83cb99cbd`.

**Governing plan:** [Presentation Studio upgrade plan at 99f1aa8a6fe7cc7361aa613cdcad258bafb9c83e](https://github.com/perseverance484/tnr-tools/blob/99f1aa8a6fe7cc7361aa613cdcad258bafb9c83e/docs/plans/FORGE_PRESENTATION_STUDIO_UPGRADE_PLAN.md). Later bootstrap-only commits on that branch do not change this pin.

**Reference:** [Godstorm evidence and layout binding](FORGE_PRESENTATION_STUDIO_GODSTORM_REFERENCE.md).

## 1. Purpose, authority and scope

An operator selects committed evidence, checks a readable dossier, makes a small set of editorial choices, and exports a faithful explanation of the content. Facts, named art and editorial writing remain separately inspectable throughout.

The user request and governing plan already require complete coverage, exact named art, current evidence, anchored summaries, deterministic rendering and zero live requests/writes. This document elaborates those requirements. Proposed geometry, copy, navigation and visual treatment need director acceptance before P2/P3 integration. It does not change game content, rewards, doctrine or the Forge Next Phase 1 contract.

`docs/00_INDEX.md` governs disagreements; `docs/DOCTRINE.md` owns doctrine. Fable owns implementation. P0 is the size prerequisite; P1 supplies dossier/spec/registry/lint and the executable golden fixture; P2 supplies the renderer; P3 supplies Forge integration. This contract implements none of them. No completed Presentation Studio fixture or renderer exists on the inspected main tree: the companion reference verifies its expected inputs and outcomes without claiming P1 acceptance.

## 2. Information architecture and ownership

| Object | Owns | Must not become |
| --- | --- | --- |
| Evidence package / source lock | Explicit repository commits, capture identities, selected record versions, hashes and their scope | A moving `main` alias or a claim of present live state |
| Dossier | Derived structure, graph order, roster, rewards, dialogue source passages, current record fields and provenance | Editable copies of game facts |
| Asset registry | Entity + field + source-record binding to exact bytes or an explicitly approved derivative | A filename search or general image gallery |
| Presentation spec | Template, anchored prose, permitted grouping, approved asset choice and display options | A second rewards/roster/content database |
| Build | Validated composition of one dossier/spec/asset revision; artifact and provenance sidecar | New canon, a live run, or publication approval |

The P3 destination is one **Presentation Studio** workspace. Its five sections are **Sources**, **Content**, **Art**, **Preview**, **Export**. Show a compact section selector on phones and an optional rail on wider screens. Do not add five global Forge tabs. Its eventual entry point is a presentation action for a subject/evidence package; P3 must decide placement within the reviewed Forge navigation.

Sources shows package selection and lock. Content shows Structure, Story, Roster, Rewards and Content status. Art shows required entity images and optional scene illustrations. Preview shows the actual template and checks. Export shows the validated build and delivery actions. Source details are available from every fact or asset without losing the operator's place.

## 3. Mobile operator journey

| Step | What the operator sees and does | Required result |
| --- | --- | --- |
| 1. Choose | Select subject and a committed evidence package by name, capture dates and revision | Selection does not contact the game or run a capture |
| 2. Lock | Review component names, dates, completeness and any conflicting records; tap **Use these sources** | Resolve every ref to a full commit and record the selection; show **Snapshot, not a live check** |
| 3. Inspect | Read derived counts, encounter cadence, complete roster, rewards and hidden/unknown status | Missing evidence is listed before layout editing; zero is distinguished from unknown |
| 4. Compose | Choose Event poster or Staff brief; edit short summaries beside their source passages | All hard facts stay locked; changes affect only the presentation spec |
| 5. Resolve art | Tap **Resolve assets** once; inspect named rows and coverage counts | Repository-bound bytes are found and verified without a device file picker |
| 6. Preview/check | Read the composition; tap an issue to jump to its field or entity | One revision-specific check result covers both semantics and layout |
| 7. Export | Tap **Prepare export**, then **Save PNG**, **Share** if supported, or **Save package** | Export uses the checked revision; success means bytes were prepared or handed off, not that someone received them |

Keep the selected subject, source revision, local draft save status and issue count visible in a compact header. Use one primary action at a time. Back/section navigation preserves the spec and position. Local drafts are recoverable by source/spec revision; browser storage failure must say **Draft not saved** and offer an explicit draft export. Do not claim a local draft is committed to the repository.

The proposed mobile acceptance floor is a 360 CSS-pixel portrait viewport: one main column, ordinary text at least 16 CSS pixels, touch targets at least 44 × 44 CSS pixels, no page-wide horizontal scrolling, no hover-only details, no required dragging. Ordering uses Move up/Move down or explicit selectors. Full names wrap. The keyboard and sticky actions must not cover the focused field, issue text or last row. At increased text size, cards grow rather than clipping.

Changing evidence creates a new source lock. Show the changed records and invalidate affected summaries, art, checks and exports. Preserve the old draft as a separately labeled revision. A late resolve/build response for revision A must never populate revision B. Changing only a title still invalidates layout checks and artifact hashes. Returning to a saved build must recheck local bytes against its hashes.

## 4. Derived versus editable

| Content | Ownership / editor behavior |
| --- | --- |
| Canonical names, entity IDs, memberships, battle/objective counts, reachable rewards, visibility, source URLs | Derived, read-only; **View source** action. No editable number or name field |
| Encounter order, predecessors, terminals and reward timing | Derived from the selected graph; do not infer from array order, filenames or image count |
| Event composition and floor/role annotations | Explicit spec references to existing subject/objective/AI IDs, validated against evidence; no inferred grouping from scene art |
| Headline/subtitle | Editable editorial text; canonical subject names remain visible separately. Embedded factual claims must use dossier bindings rather than retyped values |
| Story summary | Editable plain text with current quest-qualified anchors and an editorial review state |
| Roster ordering | Template-controlled grouping, then encounter order; staff sorting is a view choice. Membership and canonical labels stay derived |
| Exact image selection | Choose only eligible registry entries bound to that entity/field. No arbitrary upload or manual override for required art |
| Section options | Optional explanatory captions and nonessential decoration only. Required structure, story, complete roster and reward sections cannot be removed to bypass failures |
| Status and provenance | Derived; hidden/unpublished cannot be edited into available/published |

Generic templates may later support an explicitly labeled sample, but both v1 templates require `coverage: all`. Search, collapse and filtering never change export membership. A required roster remains complete even when the viewport only shows part of it.

## 5. Semantic hierarchy

The event is the parent; its explicitly selected quest/pyramid components are the top-level locations. Floors/stages belong inside those components. Encounters belong to the graph. Enemies belong to complete, named role groups. Scene images illustrate these subjects through separately validated bindings.

| Concept | Meaning | Godstorm treatment |
| --- | --- | --- |
| Event | Presentation subject with explicit component membership | Godstorm |
| Location/component | Semantic quest/pyramid subject | Marrow Vaults; Stormcourt, exactly two |
| Floor | Explicit grouping of graph nodes, validated for cadence and coverage | Five per component; display local ordinal while retaining source IDs |
| Enemy role | Annotation over a referenced AI and its encounters | Recurring / Ascendant; Keeper; final keeper may also have a Boss badge |
| Listing image | Image field of the selected quest record | One exact square image identifies each component |
| Scene/background | Illustration referenced by a content scene | Upper Court, Binding Dais Active, Binding Dais Released are optional scene captions |

Adding a background never adds a location, changes the location-art denominator, or changes the roster. An arbitrary caption cannot promote an asset into a component. Any future extra location requires explicit semantic subject membership and validation; for the Godstorm fixture it fails the two-location invariant.

In the poster, read order is **event → component structure → story → complete roster → full-clear rewards**. In the operator workspace and staff brief, **evidence problems and content status precede that content**. Visual prominence never changes evidence precedence.

## 6. Event-poster anatomy

The first poster is a complete event overview, including all enemies and the concluding story beats. It is not a spoiler-free launch announcement. A future spoiler-limited template needs its own explicit contract.

| Zone, top to bottom | Required content | Layout rule |
| --- | --- | --- |
| Identity | Event name; short editorial subtitle if used | Text rendered deterministically; no title baked into generated art |
| Structure strip | Component count, total battles, distinct AIs, keeper encounters | Use labeled measures; keep distinct AI count separate from battle count |
| Component 1 | Exact listing image + canonical name; cadence; story; recurring roster; ordered keeper roster; full-clear rewards | One coherent chapter, all nine Godstorm portraits, no representative subset |
| Component 2 | Same anatomy and relative emphasis | Same column widths, tile sizes and reward labeling |
| Footer | Snapshot date/range and short build ID | Readable compact provenance; complete hashes stay in sidecar |

Proposed reference geometry: responsive one-column HTML; a 1080-pixel-wide PNG master with content-driven height, 48-pixel outer margins and 24-pixel gutters. At a 360-pixel fit-to-width preview, required copy is at least 16 CSS pixels, corresponding to at least 48 pixels in that export. Body copy stays on opaque, calm panels. Do not put required text over detailed artwork.

Each component opens with an uncropped square listing image and name, followed by a compact cadence sentence and a 1–2 sentence story. Use a two-column roster grid at the phone width, with portrait cells about 140 CSS pixels wide and full names below. Four recurring/ascendant entries occupy two rows; five keepers occupy three rows in encounter order. The last keeper may span both columns with the same portrait scale. It is still one roster entry, not an extra nineteenth character.

A long poster is acceptable; shrinking names until eighteen portraits fit a short canvas is not. Also offer component pages using the same bindings: each repeats the event/subject name, source/build ID and page number. All required sections and entities must exist across the complete page set. The UI must label a single page as partial, and the complete package contains every page. Canvas or memory limits trigger page splitting at component boundaries, never silent cropping.

Visual proposal: use Forge's established dark neutrals for the editor and restrained neutral panels for the artifact. Let the exact artwork supply the event's color. Use weight, spacing, rules and clear labels for hierarchy; reserve status colors for status. Avoid whole-poster textures, lighting filters, ornamental frames that crop silhouettes, and tiny embossed labels. This treatment is a proposal, not a new game-art house style.

## 7. Staff-brief anatomy

| Order | Section | Required content |
| --- | --- | --- |
| 1 | Decision/status header | Subject, snapshot scope, content visibility, validation result, unresolved decisions, artifact revision |
| 2 | Event summary | Exact two-component structure, cadence, anchored story summaries |
| 3 | Structure and encounters | Per-component counts; local floor → objective-group mapping; ordered keeper names; path to final reward |
| 4 | Complete roster and art | All distinct AI names and IDs, role, component, exact thumbnail, asset class, source date and binding |
| 5 | Rewards | Current full-clear rows with the exact reward-bearing objective; explicit zero intermediate cash-outs/items where proven |
| 6 | Evidence and editorial review | Capture/source table, summary anchors, freshness differences, asset exceptions, unresolved conflicts and omissions |
| 7 | Delivery record | Build/spec/dossier identifiers, lint result, export inventory and explicit next human-owned decision |

The brief is a structured document, not a poster with smaller text. On mobile, roster/evidence tables become labeled cards with the same fields. For wider preview or print they may use tables. Keep one entity row/card intact across page breaks, repeat column headers and identify every page. Technical IDs are available here and in source details; they do not crowd the player-facing poster.

An incomplete brief can be inspected as a draft. A separate **Save issue report** action may export diagnostics labeled **INCOMPLETE — NOT A VALIDATED PRESENTATION**, with missing fields explicit and no normal final-artifact claim. It cannot turn fatal lint failures into a completed staff brief.

## 8. Exact-art contract

Named AIs, quests/locations, items, jutsu and other canonical game entities use their exact source raster or an explicitly approved derivative. Never send the complete poster, names or canonical raster layers through a generative renderer. Never use another AI's portrait, a default avatar, a similar silhouette, a scene character, or an ascendant/non-ascendant variant as a fallback.

The binding is **entity ID + source field + selected record revision + exact URL/asset identity + immutable file revision + byte hash**. A hash proves bytes, not which entity they depict; the record-to-image join must also pass. Filename, dimensions and byte count alone do not establish identity. Rendering must consume the exact bytes that were checked, including after a cache hit or a late asynchronous result.

| Registry status | Admission rule | Presentation treatment |
| --- | --- | --- |
| `exact-current` | Exact saved source pixels bound to the selected current record field, with recorded byte hash and acquisition provenance | Eligible; label **Exact source** in Art. “Current” is relative to the selected evidence, not a new live verification |
| `approved-derivative` | Explicit approval identifies entity, source hash, derivative hash, transformation and use; no generative redraw | Eligible with visible warning **Approved derivative** and disclosure in staff brief/sidecar |
| `historical-only` | Superseded image/assignment, rejected subject use, unrelated archive candidate, or old reference without a valid current binding | Excluded from active selection/counts; inspect only in an explicitly historical evidence view |
| `missing` | Required eligible bytes, binding, hash or approval unavailable | Block final export; show entity and reason. A placeholder is diagnostic, never a ready portrait |

Asset class, evidence freshness and resolution failures are separate fields. For example, a registry can expect an exact-current image while local resolution reports **Hash mismatch**; readiness is false. Historical storage paths do not make unchanged source pixels historical-only if they are independently rebound to a current selected field. Conversely, successful recovery does not grant visual acceptance for a new use.

Preserve the full source image, aspect and alpha. Default placement uses contain/letterboxing, no silhouette cropping, mirroring, recolor, smoothing, glow, filters, background removal or AI enhancement. Thirteen recovered Godstorm portraits are small non-square PNGs; do not stretch them to square to imitate the game's avatar box or reprocess them into the newer five portraits' format. A square layout cell may contain the unchanged image on a separate neutral surface.

Exactness applies to the immutable embedded source and deterministic display transform. Scaling a preview does not create a new source asset. Record scale/placement; use nearest-neighbor for pixel-art sampling, integer enlargement where possible, and a 1:1 inspection view. If a composition needs actual trimming, repadding or another pixel-changing edit, that is a separately approved derivative with its own hash. A rejected crop cannot be rescued by generative fill.

Game-upload processing and byte ceilings remain owned by `skills/producing-tnr-art/` and its art spec. A presentation export is a separate derivative, not a new upload. Do not automatically run source art through chroma/QC export processing simply to place it in a presentation.

Optional generated decoration is **off in this proposal**, pending the director's policy decision. If later allowed, it must be isolated, opt-in, declared in metadata and semantically anonymous; it cannot depict a named entity/location, supply text, fill a missing slot or count toward coverage.

## 9. Narrative summaries

Use 1–2 sentences per component, normally 30–55 words: entry/premise, the meaningful development, and the outcome. This is a writing target; wrapping must not truncate a complete thought. Preserve who was confined, who maintains the binding, what changes, and the direction of travel when the selected dialogue establishes them. Do not import names, titles, mythology or causal claims from planning prose.

Each summary stores references qualified by **quest ID + objective ID + text field + selected source revision/content hash**. IDs alone are insufficient: two quests may reuse an ID, and an old/new version may keep the same ID while changing its text. Display the exact selected source passages beside the editor as safe text, with early/middle/outcome groups. A summary anchor must resolve to a reachable current dialogue/objective passage relevant to the claim. Existence-only validation is necessary but does not prove a faithful paraphrase.

Require narrative review after the text or any anchored passage changes. Lint blocks absent/foreign/stale anchors and invalid source types; it warns on sparse coverage. The human review checks meaning against all current dialogue and may reject a summary whose anchors exist but do not support it. There is no automatic LLM story-writing step in P1. Store the reviewed summary hash and source hashes; never retain a green editorial state across a source-text change.

Hard-fact claims inside prose still resolve through dossier bindings; accepting free text is not an escape hatch for stale rewards or counts. Historical Tower/Dawnless wording is excluded from current Godstorm copy, including subtitles, captions, alt text and export filenames. Historic source names remain visible only as clearly marked provenance. The companion reference supplies two proposed summaries and exact anchors.

## 10. Evidence freshness and provenance

Show three independent truths: **Evidence** (selected snapshot and coverage), **Art** (four registry classes plus resolution), and **Content** (hidden/published/unknown as captured). A successful Forge job or green presentation check is never a publishing claim.

Sources must resolve per entity and field from an explicit manifest of evidence. A later AI-profile/rules record does not replace an avatar capture merely because both mention the same AI. Do not merge arbitrary fields from different versions into an apparently whole current record. Use an explicit overlay only with matching identity, scoped provenance and a supersession decision. Required incomplete or unresolved sources block the affected current claim.

| Evidence state | Meaning / action |
| --- | --- |
| Selected snapshot verified | Required captures and bindings validate within the chosen evidence package; display capture times and scope |
| Mixed dates | Different entities/fields were captured at different times; show oldest/newest and per-field dates, warn, and retain scoped authority |
| New repository evidence available | Compare relevant records before adoption; never silently switch a saved build's lock |
| Known stale | A selected field/anchor is superseded by relevant admitted evidence; block current output until rebuilt; old artifact remains an explicitly historical snapshot |
| Incomplete / conflict / unknown | Explain what is missing or disagrees, identify candidate sources, and block unsupported claims |

Elapsed time alone is not proof of staleness or freshness. Do not invent a universal expiry interval. In zero-live mode, **Check for newer evidence** means repository evidence only. Never report **Checked live today** or silently fetch an image CDN to settle freshness.

The staff brief/source drawer shows full repository commits; source paths and SHA-256s; capture procedure, identity, snapshot key and capture time; fact field/objective; asset URL and acquisition date; approved-derivative decision if any; dossier/spec/template/renderer revision; and lint/editorial state. The poster footer uses a small snapshot date/range plus build ID. Hidden status is always visible in the operator workspace and staff brief/sidecar; it need not occupy normal poster copy, but no artifact may assert availability contradicted by the evidence.

Metadata exports are an explicit presentation projection. Do not include whole profile bodies, journals, idmaps, local-only captures, credentials or unrelated records merely because they were present in a source bundle. Cite the source file and pointer instead.

## 11. Failure and recovery contract

| Failure | Required visible behavior | Recovery / gate |
| --- | --- | --- |
| Required record absent or unverified | Name subject, record and affected section; show unknown instead of zero | Choose adequate committed evidence; final export blocked |
| Mixed/partial run | Inspect each relevant capture's identity, full persistence, success and scope; never inherit the job's global color | Admit independently proven captures with disclosure, or block. Do not mark every capture verified because the job is DONE |
| Conflicting values/versions | Show both source pointers and differing values | Apply repository precedence or obtain a genuine director ruling; no “use newest file” default |
| Roster 17/18, duplicate ID or substituted portrait | Show the missing/extra identity and group | Complete exact set equality before export; equal counts alone do not pass |
| Missing/default/historical image | Named diagnostic placeholder, excluded from ready count | Resolve exact bytes/approved derivative; no generative fallback |
| Hash, decode or identity mismatch | **Asset refused**, with the affected entity; verified-ready state removed | Resolve the pinned file; no same-size/manual override |
| Stale same-ID dialogue | Show the changed passage and stale summary | Re-anchor and review; no inherited green check |
| Historical reward contamination | Name source and affected reward row | Rebuild from reachable selected current nodes; no warning-only final export |
| Scene promoted to location | Identify the invalid semantic binding | Remove/correct it; Godstorm top-level set remains exactly two |
| Layout overflow or missing glyph/image/font | Mark the exact page/tile | Reflow or split at defined boundaries; do not shrink below the reading floor or emit a partial success |
| Revision changed while resolving/rendering | Discard obsolete result without installing its bytes or readiness | Prepare/check the current revision |
| Save/share unavailable, canceled or failed | Retain generated bytes; distinguish cancellation from delivery | Offer Save PNG/package or open the prepared image; do not regenerate or lose the draft |

Lint results are attached to a build revision. Fatal issues disable final artifact actions and explain why next to those actions. Warnings remain visible and travel in the sidecar. A warning is never a device for overriding a missing required fact or asset.

## 12. Android export and sharing

Proposed P2 delivery is deterministic HTML/CSS preview plus PNG; an SVG intermediate/export is optional and must embed the exact rasters. PDF may follow. Use actual text in HTML/SVG and a deterministic rasterizer for PNG. No external fonts or images may be required to open the saved package. Escape content as text; preserve the existing safe DOM/CSSOM boundary in Forge integration.

Prepare the bytes before presenting a separate Share tap. Feature-detect file sharing for the prepared files; do not assume Firefox Android exposes it. If unavailable, offer Save PNG and Save package. The operator chooses recipients in their device share sheet; nothing is sent automatically. Show page count, dimensions and byte size before saving. A canceled share keeps the output ready. Avoid promising a download location or receipt the browser cannot verify.

Use meaningful filenames such as `godstorm-event-poster-<build-id>.png` and numbered component pages, with a matching `.provenance.json`. **Save package** contains the artifact(s), self-contained preview, spec/dossier projections and provenance sidecar. Individual image sharing remains useful; its footer must retain snapshot/build identity if the sidecar is not shared. No manual hunt for eighteen source files is part of the operator flow.

The sidecar records source commits/hashes/pointers, selected assets and transforms, dossier/spec/template/renderer hashes or revisions, artifact hashes, page inventory and lint/editorial results. Keep build time separate from capture time. Byte identity is required for embedded sources and logical content; byte-stable PNGs depend on a pinned renderer/font/encoder environment and must not be claimed across arbitrary browsers.

The proposed default treats binaries as generated deliverables while retaining the source spec/bindings. Whether final binaries are also committed remains a director decision. Download/export and sharing do not publish game content or change hidden status.

## 13. Godstorm reference layout

Use the companion reference's verified record selection and exact art bindings. Top strip: **2 pyramids · 50 battles · 18 enemies · 10 keeper fights**. Every number is a dossier binding, not a string owned by the template.

First chapter: **Marrow Vaults**, its exact listing image, **25 battles across 5 floors**, the anchored blurb, four recurring portraits, five ordered keeper portraits, and **Full clear: 125,000 ryo · 25 tokens · 10 prestige**. Second chapter: **Stormcourt**, the corresponding listing image, cadence and blurb, four ascendant portraits, five ordered keepers, and **Full clear: 250,000 ryo · 150 tokens · 60 prestige**.

Both chapters explain **4 normal fights → 1 keeper, repeated for five floors**. Normal opponents rotate; this sentence does not promise a fixed repeated identity order. For Stormcourt, label the normal-opponent group **Ascendants**. The final keeper remains within the five, even with a boss badge. No chest icon, item ribbon, intermediate reward row, third location, Tower title or Dawnless chapter appears.

The staff brief includes objective counts, all identity/source mappings, exact reward-bearing dialogue IDs, hidden status and mixed-date evidence. Optional scene detail may show the three new Stormcourt backgrounds with scene captions; it never replaces the two listing images or becomes a location row.

## 14. Acceptance and independent review

| Gate | Required proof |
| --- | --- |
| P1 evidence | Explicit pinned sources; correct reachable graph/rewards; exact distinct roster; per-claim provenance; no planning-file promotion |
| P1 adversarial | Old cash-out/chest data, same-ID changed dialogue, missing/duplicate keeper, swapped and same-size wrong images, cross-quest anchors, absent required captures and scene/location leakage all refused |
| P1 art | 18 roster and 2 listing-image bindings resolve; exact source bytes and identity joins pass; rejected StormCourtyard and stale default assignments excluded |
| P2 fidelity | Exact names, summaries, complete roster and current rewards; source hashes unchanged; all text/images loaded; no clipping, invented art or unlabelled omissions |
| P2 reproducibility | Identical lock/spec/assets yield identical logical content and documented transform metadata; fixed-environment output checks as claimed |
| P3 mobile | Test actual Android browser save/share fallback, cancellation, large-output splitting, keyboard/back behavior and draft recovery; record unsupported/unverified capabilities |
| Bundle containment | P0 measured raw/gzip improvement and ratchet; no safety loss; P1 repo-side by default; heavy renderer outside the core unless independently justified and reviewed |

No live smoke is implied by these gates. For a later frozen Fable P0/P1 handoff, independently verify branch, base, merge-base and head; review that exact SHA against the pinned plan and accepted contract; reproduce surviving findings on a ChatGPT review branch. Do not edit Fable's branch or claim renderer/UI acceptance from a P1-only handoff.

## 15. Director decisions and present limits

None blocks completing this design draft or P0/P1. Before P2/P3 integration, settle the product name, optional generated-decoration policy, binary commit policy, template priorities if changed, and scheduling relative to Forge Next. Accept or adjust the proposed mobile geometry, full-story overview treatment and example blurbs as part of design acceptance. Proposed defaults are Presentation Studio; Event poster + Staff brief; decoration off; generated binaries; unchanged Forge Next scope.

The factual reference uses selected committed snapshots, not a fresh live check. Thirteen older portraits have explicit capture/acquisition dates. Android behavior and renderer layout remain acceptance targets, not tested implementation claims. The baseline session parity guard crashes on `checks: null`; the dedicated repair verifier succeeds. The companion document records the exact checks and limits.
