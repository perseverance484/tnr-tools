// ==UserScript==
// @name         TNR forge (loader)
// @namespace    tnr-tools-forge
// @version      0.1.0
// @description  Loads forge_bundle.js: the full-page TNR content builder (journal, cache-first reads, two-phase creates, reconciliation). Installs beside the old TNR Content Builder loader; both can stay.
// @match        *://www.theninja-rpg.com/forge*
// @match        *://theninja-rpg.com/forge*
// @grant        none
// @run-at       document-start
// @require      https://cdn.jsdelivr.net/gh/perseverance484/tnr-tools@builder-app/forge_bundle.js
// ==/UserScript==
// Open https://www.theninja-rpg.com/forge while logged in. The page is a same-origin 404 with no
// game providers; the bundle stops it at document-start and mounts the app in its place.
// The @require above points at the builder-app BRANCH (jsDelivr caches branch refs for ~12h).
// Once the branch is reviewed, replace it with a commit-pinned URL exactly as release_pin.yml
// does for builder_bundle.js; the workflow is paths-filtered to that file and does not cover
// this one yet.
