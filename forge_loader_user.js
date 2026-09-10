// ==UserScript==
// @name         TNR forge (loader)
// @namespace    tnr-tools-forge
// @version      0.3.0
// @description  Loads forge_bundle.js: the full-page TNR content builder (journal, cache-first reads, two-phase creates, reconciliation). Installs beside the old TNR Content Builder loader; both can stay.
// @match        *://www.theninja-rpg.com/*
// @match        *://theninja-rpg.com/*
// @grant        none
// @run-at       document-start
// @updateURL    https://raw.githubusercontent.com/perseverance484/tnr-tools/main/forge_loader_user.js
// @downloadURL  https://raw.githubusercontent.com/perseverance484/tnr-tools/main/forge_loader_user.js
// @x-release-pending 0.4.0
// @require      https://cdn.jsdelivr.net/gh/perseverance484/tnr-tools@58323b0af0eeafc3204cfbd5c31cb068a3cf5a88/forge_bundle.js
// ==/UserScript==
// Open https://www.theninja-rpg.com/forge while logged in. That entry is unchanged, but since
// 0.4.0 it is a doorway, not the host: /forge is a same-origin 404 that renders through
// global-not-found.tsx with NO ClerkProvider and NO tRPC provider, so a Clerk session cannot
// live there and every protectedProcedure answered UNAUTHORIZED. The bundle now stops that page,
// arms this tab, and hands off to a normal game route, where it mounts as an overlay on top of
// the running app with the provider tree left intact underneath.
//
// @match therefore covers the whole game origin, exactly as the old builder loader does: the
// carrier route is not fixed in advance (the app may redirect a signed-in operator elsewhere),
// so activation is decided by a per-tab sessionStorage marker rather than by a URL. On any game
// page in a tab that has NOT been armed through /forge, the bundle does nothing at all - it
// returns before touching the document, issuing a request or installing a style.
//
// RELEASE PIN. @require must always resolve to an IMMUTABLE bundle commit. Development branches
// keep the last released @version/@require and may carry @x-release-pending <package-version>.
// release_pin.yml is the only path that promotes a pending Forge release on main: it rewrites the
// @require to the merge commit that contains forge_bundle.js, syncs @version from forge/package.json,
// and removes the pending marker. @updateURL/@downloadURL may safely watch main because main never
// needs to expose a moving branch bundle in order to stage the next release.
