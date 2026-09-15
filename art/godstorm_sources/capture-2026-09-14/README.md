# Godstorm source-art archive

Recovered 2026-09-15. Retrieval complete; production art acceptance remains separate.

## Proven transport

The ChatGPT execution container could not resolve GitHub or the image host, and the native web/download route did not admit the captured image URL. The authorized GitHub connector did work. A narrowly scoped job on `chatgpt/godstorm-art-recovery` read the existing pinned captures, downloaded their static image URLs on the GitHub runner, committed the unchanged image bytes here, and exported an Actions artifact. The connector downloaded that ZIP into the ChatGPT runtime. Local SHA-256 checks, ZIP integrity checks and full Pillow verification/decoding then passed for all 19 files. Actual images were visually opened, including Marrow vault 1 and Sovereign Echo; overview sheets for all 19 images were inspected. This is actual pixel access, not merely a list of URLs or truncated base64.

No additional network permission, PAT, game cookie or new Forge capture was required from the user for this execution. This does not enable unrestricted networking in the ChatGPT Python/container environment.

## Exact evidence

- Capture baseline: `6e09b15bb6f3d1c90ba416d14211b533f5b4a367`.
- Capture inputs: `harvests/inbox/tnr_results_1789401726302.json` and `harvests/inbox/tnr_results_1789402842027.json`, read from pinned Git objects.
- Collector/workflow source at successful run: `642a18becab86a191d8c5f85b4ecfc4f58a6ad76`.
- Original-image/index archive commit: `3f11dcd325df8d2fd27110999c39f4bab430b000`.
- Successful Actions run: `35015157511`; job `104536629588`.
- Artifact: `10415640675`, `godstorm-source-art`, ZIP size 1,919,041 bytes.
- Artifact SHA-256, independently matched after transfer: `57c331ab29d79bdde795e0b4fd08ac3eeeae9e656fa1b71295aeab0ca54295a1`.
- Individual hosted image bytes: 1,909,318 bytes total. Original image files remain under `originals/`; `index.json` records hashes, dimensions, formats, entity IDs, fields, exact URLs, capture pointers and timestamps.

| Category | References reviewed | Files recovered | Missing/default |
|---|---:|---:|---:|
| Retained primary AI avatars | 18 | 13 | Five default assignments, recorded and skipped |
| Retained quest listing images | 2 | 2 | Zero |
| Captured background candidates | 4 | 4 | Zero |
| Total | 24 | 19 | Five default avatar assignments |

The five default records are Umbral Reaver, Hollow Lantern, Starless Monk, Nightveil Sentinel and Warden of the First Dark. No replacement for them was generated or counted as an existing asset.

All 19 selected non-default URLs downloaded successfully. This is the bounded initial pack, not closure of the entire game's art catalog, additional scene candidates, jutsu/effect art or alternate-avatar paths.

## Raw-file observations, not acceptance

All 13 recovered enemy images are PNGs with actual transparency. They are 256 pixels high and vary from 177 to 239 pixels wide. They are already isolated source candidates, not opaque portrait paintings needing automatic background removal. Size, padding, silhouette and scene suitability still need the current production-art checks.

The three Marrow plates are WEBP files at 500 x 333. StormCourtyard is a JPEG at 1536 x 864, from the shared SkychainMonastery record. The two listing images are WEBP files at 1536 x 1536. No format conversion or resizing was applied to originals. Review sheets and the self-contained chat gallery are derived presentation files, not replacement game art.

These are the bytes served by captured URLs on September 15. The capture recorded the URLs on September 14; it did not pin image bytes then. The files are not proven original generation masters. Historical captured names remain in provenance even where the new release drops Tower branding.

## Repeat access

While the artifact exists, use GitHub's artifact download action with artifact ID `10415640675`; it returns an actual ZIP file that can be mounted in the chat runtime. Verify the ZIP digest and every indexed image hash before inspection. The artifact's recorded expiry is 2026-10-15; the committed originals/index do not depend on that temporary artifact remaining available.

After artifact expiry, export the committed archive at its exact SHA again; do not repeat live game reads merely to recover these same pixels. The collector refuses an existing output directory to avoid replacing archived evidence. A later source refresh must use a fresh evidence path and explicit approval. This is a bounded completed recovery job, not an ongoing monitor or automatically adopted general-purpose production exporter.

## Safety and verification limits

The job issued no game API request, no game mutation, no image upload and no publication. It reads only pinned approved capture data and limits image downloads and redirects to HTTPS file paths on the specified image hosts. It does not request or transmit player credentials. Main, the planning branch and Fable branches were not modified; scripts/workflow and recovered files are on this separate ChatGPT-owned branch.

The first two job attempts stopped during strict capture-identity checks before downloading anything. The collector was corrected to use `userId` in both the captured profile.getAi input and response. The successful third run completed extraction, download, archival commit and artifact export. No guard was disabled to proceed.

Successful retrieval and pixel decoding do not imply the full art preflight, reuse suitability, revised quest validation, balance pass or final operator acceptance has passed. Those remain separate work.
