// ==UserScript==
// @name         TNR forge (loader)
// @namespace    tnr-tools-forge
// @version      0.2.0
// @description  Loads forge_bundle.js: the full-page TNR content builder (journal, cache-first reads, two-phase creates, reconciliation). Installs beside the old TNR Content Builder loader; both can stay.
// @match        *://www.theninja-rpg.com/forge*
// @match        *://theninja-rpg.com/forge*
// @grant        none
// @run-at       document-start
// @require      https://cdn.jsdelivr.net/gh/perseverance484/tnr-tools@bbb3a19d24bcf0b51a94cfb53a57f3f27b22d37c/forge_bundle.js
// ==/UserScript==
// Open https://www.theninja-rpg.com/forge while logged in. The page is a same-origin 404 with no
// game providers; the bundle stops it at document-start and mounts the app in its place.
//
// RELEASE PIN. @version must equal forge/package.json, and the @require must resolve to an
// IMMUTABLE commit, so that installed bytes can only ever be the reviewed ones. Until this branch
// merges it points at the branch instead, which jsDelivr caches for about 12h and which any later
// push silently changes - so the @x-unpinned-until-release line above marks it explicitly. That
// line is the whole point: forge/tools/check_release_pin.mjs (run as part of `npm test`) FAILS if
// the @require is not commit-pinned and the marker is absent, so a release can never float on a
// branch quietly. release_pin.yml rewrites the @require to the commit URL, syncs @version from
// forge/package.json and deletes the marker on every push to main that changes forge_bundle.js;
// installing that workflow change is a dauntless action (the PAT cannot push .github/workflows/).
