// Document takeover at document-start (spec section 2).
//
// Host path: any unmatched URL on the game origin, /forge by convention. From source at
// 345d18ac: next.config.mjs sets experimental.globalNotFound: true; proxy.ts's matcher comment
// states "URLs with no matching route render through global-not-found.tsx without the
// Clerk-dependent root layout", and the middleware body returns immediately for every
// pathname other than "/" (proxy.ts, `if (pathname !== "/") return;`). global-not-found.tsx
// is a bare <html><body> with one Link and no providers. So the host page has NO tRPC
// provider, NO Clerk hydration, NO game fetch on mount, and no React tree to co-exist with,
// while the session cookie is still first-party for /api/trpc. That is why /forge.
//
// The takeover stops the page load, empties the document, and mounts the app. The old
// builder's loader matches the whole origin at document-idle and would append its panel
// here too; its nodes are removed on arrival so both scripts can stay installed.

import { h, clear } from "./dom.mjs";

export const HOST_PATH = "/forge";
const OLD_BUILDER_CLASSES = ["k-fab", "k-pn"]; // builder_bundle.js root nodes

export function takeover(doc = document, win = window) {
  try { win.stop(); } catch { /* not fatal */ }
  const html = doc.documentElement || doc.appendChild(doc.createElement("html"));
  clear(html);
  const head = h("head", {}, h("meta", { charset: "utf-8" }), h("meta", { name: "viewport", content: "width=device-width, initial-scale=1, viewport-fit=cover" }), h("title", {}, "TNR forge"));
  const body = h("body", {});
  html.append(head, body);
  // keep the old builder's panel off this document
  const mo = new win.MutationObserver((muts) => {
    for (const m of muts) for (const n of m.addedNodes) {
      if (n && n.nodeType === 1 && OLD_BUILDER_CLASSES.some((c) => n.classList && n.classList.contains(c))) n.remove();
    }
  });
  mo.observe(body, { childList: true });
  return { html, head, body, observer: mo };
}

export function onHostPath(loc = location) { return loc.pathname === HOST_PATH || loc.pathname.startsWith(HOST_PATH + "/"); }
