// ==UserScript==
// @name         TNR forge (loader)
// @namespace    tnr-tools-forge
// @version      0.2.1
// @description  Loads forge_bundle.js: the full-page TNR content builder (journal, cache-first reads, two-phase creates, reconciliation). Installs beside the old TNR Content Builder loader; both can stay.
// @match        *://www.theninja-rpg.com/forge*
// @match        *://theninja-rpg.com/forge*
// @grant        none
// @run-at       document-start
// @updateURL    https://raw.githubusercontent.com/perseverance484/tnr-tools/main/forge_loader_user.js
// @downloadURL  https://raw.githubusercontent.com/perseverance484/tnr-tools/main/forge_loader_user.js
// @x-release-pending 0.3.0
// @require      https://cdn.jsdelivr.net/gh/perseverance484/tnr-tools@b9948729a4649f1cf7ecf500c3c40ed8ee9ad225/forge_bundle.js
// ==/UserScript==
// Open https://www.theninja-rpg.com/forge while logged in. The page is a same-origin 404 with no
// game providers; the bundle stops it at document-start and mounts the app in its place.
//
// RELEASE PIN. @require must always resolve to an IMMUTABLE bundle commit. Development branches
// keep the last released @version/@require and may carry @x-release-pending <package-version>.
// release_pin.yml is the only path that promotes a pending Forge release on main: it rewrites the
// @require to the merge commit that contains forge_bundle.js, syncs @version from forge/package.json,
// and removes the pending marker. @updateURL/@downloadURL may safely watch main because main never
// needs to expose a moving branch bundle in order to stage the next release.
