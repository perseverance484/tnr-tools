# Ghost Ship chest icons — cross-family geometry reset (2026-10-20)

**Status:** DIRECTOR RESTART / STOP-USE — all 6 previously accepted chest raws are visually invalidated and require regeneration.  
**Working role:** Art Director (lead), Image Production (support)  
**Authority:** Director's 2026-10-20 message: “Just noticed all the chests need to be regenerated. Their geometry is messed up, there's an extra metal band on the right side, looks like it was copied from the Sage's Stromgbox reference image's leather strap.”  
**Governing approved workstream brief:** `docs/handoffs/GHOST_SHIP_CHEST_ICONS_ART_REQUEST.md`; `RUL-2026-10-20-002`; `docs/workflows/ISOLATED_ART_GENERATION.md`  
**Limits:** Art Studio coordination only; **no generation in this thread**, no game requests/writes, no credentials, no game uploads/publishing.

## Rejection and provenance discipline

The director has **withdrawn visual acceptance** of ALL six previously approved chest images. Their original approval statements were authentic at the time, but their current operative state is **REVOKED — GEOMETRY INVALID**. The six original source bytes and earlier approval history are preserved as **rejected historical evidence**, not active generation references. Do not silently erase their hashes, rewrite the history as though never approved, or treat them as ready for production.

| # | Invalidated target | Conversation source | Raw SHA-256 | Current |
| --- | --- | --- | --- | --- |
| 01 | Common Hunter's Chest | `1000018925.png` | `b341d9e939d7a5cb182ac8576ab97777b36cfea607a3e4d6768052554ea3e4f3` | REVOKED |
| 02 | Common Gatherer's Chest | `1000018926.png` | `acb6f618cdbc3b5414a3bfbfaabc682b9e03403141fe0d8b7b8c0a4a5356381a` | REVOKED |
| 03 | Rare Hunter's Chest | `1000018929.png` | `bb2d7affc025c49e21111f8db8f4a0bbc15b3930f96193a2c13ec9430c21793c` | REVOKED |
| 04 | Rare Gatherer's Chest | `1000018930.png` | `d5e44dba4c5947067ee0da8cef1d7e326a1aafbec7d85c21e6eba76db33a31a4` | REVOKED |
| 05 | Epic Hunter's Chest | `1000018931.png` | `9cdded700f3027e2788ba040cc1995667afb322ef229476d51436728e02d0339` | REVOKED |
| 06 | Epic Gatherer's Chest | `1000018932.png` | `9ec335743a0898552f009e5906a28b043ef9e43472bd0fe6521101af7e65ebdc` | REVOKED |

Gates 07–12 were not visually approved. **Cancel** the prepared Legendary Hunter generation handoff until the corrected foundation has been accepted. The prior `EPIC_HUNTER`/`EPIC_GATHERER`/Rare/Common individually approved images must not be reintroduced as style, geometry, or same-family images in any new generation session.

## Visual evidence and diagnosis

Studied the actual six source images as a cross-family set, then enlarged the Epic Gatherer's upper-left and upper-right lid band regions. The repeated error is a **second parallel curved metal strap/strip immediately adjacent to a primary domed-lid hoop**, most conspicuous at the right side of the lid; at higher tiers the duplication can also be seen around the left hoop. Some steps previously requested “layered/stepped bands,” which risk reinforcing this *side-by-side duplicate topology* instead of applying armor **on top of** an existing sound structural hoop.

**Observed:** recurring unwanted band geometry in the already approved set, not just a small shading error.  
**User-suspected cause:** visual contamination copied from a Sage's Strongbox / “Stromgbox” reference strap. This attribution is **not independently source-verified** by the studio; the documented canonical reference is the Skyglass Reliquary (style/material only). Do not claim confirmed generator causality from the image alone.

This defect is fundamentally compositional/structural. Keying, resizing, alpha cleanup, silver-rarity polish, or manual production preflight cannot repair it without modifying the director-accepted subject itself. Regenerate rather than process the old files.

## Proposed hard geometry lock (director confirmation required before restart)

**Do not confuse tier ornament with structural band count.** Proposed intended chest assembly:

1. **ONE arching metal hoop per lid end**: one near camera-left end of the domed lid and **ONE** on camera-right end. Both are coherent physical bands following the single barrel-shaped curve and terminating in aligned corner fittings. **NO second thin metal arch immediately beside either main hoop**, especially not to the right of the right-hand hoop. **NO stray parallel strap copied from a style reference.**
2. **ONE family-specific central wrap only**: Hunter's **brown leather strap with a bone/fang clasp**, Gatherer's **coiled rope binding and tucked green sprig**. Center binding follows the same lid curvature; the single center binding must not morph into metal, split into a metal twin, or create an extra side hoop.
3. **Strong 3D continuity:** rear/side wood planking follows the dome; each side hoop visually connects to its own side/corner brace with believable anchors; no unsupported overlapping straps, phantom depth band, extra vertical rail on the right, disconnected floating plates, or a “ghost” arc behind the outer hoop.
4. **Tier changes applied to existing geometry rather than increasing hoop count:** Rare strengthens each **existing** end hoop with riveted *on-top-of-band* raised plate armor and cooler gunmetal. Epic refines those existing surfaces with silver edging, larger gem and illuminated family brand. Legendary uses filigree and a physically mounted lid shard group, **not** additional parallel metal hoops.
5. **Visual QC first:** inspect the top and near/far right sides at **full source resolution** and **125px**, alongside a mirrored check of the left; confirm proper band count/attachment BEFORE considering motif correctness or tier aesthetics.

The above **two-end-hoop** topology is a concrete studio proposal to remove the observed duplication; the director controls final geometry interpretation. Do not silently present a corrected geometry as approved until the director confirms this intended reading of “extra band.”

## Restart sequence

1. **STOP currently queued Legendary Hunter session.** Its brief is historically superseded until a rebuilt, director-approved Epic Hunter exists.
2. **Restart at Common Hunter**, in one **clean isolated generation conversation**: only the original Skyglass Reliquary source is eligible as a **style/material-only** reference. Explicitly exclude all rejected chest originals, Sage's Strongbox, galleries and previous candidates from prompt attachments. Require the approved domed silhouette, Hunter claws, central leather/fang wrap, small skyglass clasp, **and the hard geometry lock above**. First inspect structural topology before offering any candidate for director approval. The background must actually have native alpha or true solid-key coverage (not opaque black).
3. Only after director approves geometry-correct Common Hunter, regenerate Common Gatherer in another clean isolated conversation with the Reliquary + **corrected** Common Hunter, never the rejected old version. Keep two reference images maximum.
4. **Rebuild pairs sequentially** Rare Hunter, Rare Gatherer, Epic Hunter, Epic Gatherer, Legendary Hunter, Legendary Gatherer, Rusted Hunter, Rusted Gatherer, Ornate, Mystery. Each uses only the Reliquary and newly approved **geometry-correct** same-family predecessor where applicable, **never a now-rejected old chest**. Do not accelerate by batching away geometry gates.
5. The approved direction from the original brief (Hunter claws/leather/fang; Gatherer leaf/rope/sprig; tier ladder; Ornate aged gold; Mystery chains/lock/mist with no question mark) is **still approved as concept and palette**. **Only the previously approved rendered originals are invalidated.** The director's actual item rarity decision remains out of scope.
6. Each new corrected raw gets its own exact raw SHA and provenance, and must pass alpha/background QC, dark-composite edge QC, lossless `ICON` WebP, and `artpreflight.py --type ICON` prior to any packaging. **No production-ready exports exist.** Respect the original target delivery filenames for the eventual replacements; if any actual file has already been delivered under a production filename, use versioned suffixes rather than overwriting.

## Pending director clarification

**Confirm topology before initiating the new Common Hunter:** is the intended correction *exactly one curved metal hoop at each outer end of the lid* (plus the single center leather/rope binding), with the extra adjacent right-side thin band removed? A different intended end-band count/layout must be established here before a full 12-icon regeneration campaign.

**Next:** update the persistent studio register and supersede earlier isolated briefs, then issue ONE corrected Common Hunter isolated prompt **only after the intended topology is confirmed**. No artwork generation in the studio.
