// ==UserScript==
// @name         TNR forge (loader)
// @namespace    tnr-tools-forge
// @version      0.4.0
// @description  Loads forge_bundle.js: the full-page TNR content builder (journal, cache-first reads, two-phase creates, reconciliation). Installs beside the old TNR Content Builder loader; both can stay.
// @match        *://www.theninja-rpg.com/*
// @match        *://theninja-rpg.com/*
// @grant        none
// @run-at       document-start
// @updateURL    https://raw.githubusercontent.com/perseverance484/tnr-tools/main/forge_loader_user.js
// @downloadURL  https://raw.githubusercontent.com/perseverance484/tnr-tools/main/forge_loader_user.js
// @x-release-pending 0.4.1
// @require      https://cdn.jsdelivr.net/gh/perseverance484/tnr-tools@ce603def204f585d23837121b86cfdd9fd4c308c/forge_bundle.js
// ==/UserScript==
// Open https://www.theninja-rpg.com/forge while logged in. That entry is unchanged, but since
// 0.4.0 it is a doorway, not the host: /forge is a same-origin 404 that renders through
// global-not-found.tsx with NO ClerkProvider and NO tRPC provider, so a Clerk session cannot
// live there and every protectedProcedure answered UNAUTHORIZED. The bundle now stops that page,
// arms this tab, and hands off to a normal game route, where it mounts as an overlay on top of
// the running app with the provider tree left intact underneath. Since 0.4.1 the overlay is
// appended only once the game has hydrated the document (React owns <body> there): an overlay
// appended earlier was claimed by hydration and cleared with the rest of body when React fell
// back to a client render, which is why 0.4.0 showed the splash and then the plain game.
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
