// ==UserScript==
// @name         TNR Crafting Recipe Census (read-only)
// @namespace    tnr-tools-crafting-census
// @version      1.0.1
// @description  On-page Run / Stop / Download panel for the read-only crafting recipe census. Inactive unless the tab is armed by opening a game page with #craft-census.
// @match        *://www.theninja-rpg.com/*
// @match        *://theninja-rpg.com/*
// @grant        none
// @run-at       document-idle
// @require      https://cdn.jsdelivr.net/gh/perseverance484/tnr-tools@42a1db0fbf22c61ced73eab6047436d637fc7940/harness/crafting_recipe_census/crafting_recipe_census.console.js
// ==/UserScript==
// Phone-friendly wrapper around crafting_recipe_census.console.js. The census itself is the
// @require above, pinned to an immutable commit: GET-only to item.getAll and
// item.getItemWithCraftingRequirements, credentials omitted, throttled, resumable. This file adds
// only a panel; it issues no request of its own.
//
// Arming: open https://www.theninja-rpg.com/#craft-census. That sets a per-tab sessionStorage
// marker, so the panel survives the game's own redirects in that tab. On every other page and
// tab this script returns before touching the document. "Close" on the panel disarms the tab.
//
// The panel re-attaches itself if the game's React hydration clears <body> (the failure Forge
// 0.4.0 hit), by checking once a second that it is still in the document.
(function () {
  "use strict";
  const ARM_HASH = "#craft-census";
  const ARM_KEY = "tnr_crafting_census_armed";
  const w = window;
  try {
    if (w.location.hash === ARM_HASH) w.sessionStorage.setItem(ARM_KEY, "1");
    if (w.sessionStorage.getItem(ARM_KEY) !== "1") return;
  } catch (_e) {
    return;
  }
  // The @require may land on the sandbox global or on the page window, depending on the manager.
  const findCensus = () => {
    try {
      if (typeof TNRCraftCensus !== "undefined" && TNRCraftCensus) return TNRCraftCensus;
    } catch (_e) { /* not declared in this scope */ }
    return w.TNRCraftCensus || (typeof globalThis !== "undefined" && globalThis.TNRCraftCensus) || null;
  };
  const doc = w.document;

  const panel = doc.createElement("div");
  panel.id = "tnr-craft-census-panel";
  panel.setAttribute(
    "style",
    "position:fixed;left:8px;right:8px;bottom:8px;z-index:2147483647;background:#111;color:#eee;" +
      "font:13px/1.35 system-ui,sans-serif;border:1px solid #555;border-radius:8px;padding:8px;" +
      "box-shadow:0 2px 12px rgba(0,0,0,.5);max-height:45vh;overflow:auto",
  );
  const title = doc.createElement("div");
  title.textContent = "Crafting Recipe Census (read-only)";
  title.setAttribute("style", "font-weight:600;margin-bottom:6px");
  const bar = doc.createElement("div");
  bar.setAttribute("style", "display:flex;flex-wrap:wrap;gap:6px;margin-bottom:6px");
  const out = doc.createElement("pre");
  out.setAttribute("style", "margin:0;white-space:pre-wrap;word-break:break-word;font:12px/1.3 monospace");
  const logView = doc.createElement("pre");
  logView.setAttribute(
    "style",
    "margin:6px 0 0;white-space:pre-wrap;word-break:break-word;font:11px/1.3 monospace;color:#9c9",
  );
  panel.append(title, bar, out, logView);

  // A message (error, saved file) stays on screen until the next button press.
  let message = "";
  const show = (text) => {
    message = text;
    out.textContent = text;
  };
  const fmt = (s) => {
    if (!s || s.status === "not_started") return "Not started. Tap Run.";
    const pass = (m) =>
      Object.entries(m)
        .map(([k, v]) => `${k}: ${v.rows} rows / ${v.pages} pages${v.done ? " (done)" : ""}`)
        .join("\n  ");
    const halt = s.lastHalt ? `\nlast halt: ${s.lastHalt.reason} - ${s.lastHalt.detail}` : "";
    return (
      `status: ${s.status}   phase: ${s.phase}   requests: ${s.requests}\n` +
      `list:\n  ${pass(s.main)}\ndetails: ${s.details}\nconfirm:\n  ${pass(s.confirm)}${halt}`
    );
  };
  const refresh = async () => {
    const census = findCensus();
    if (!census) {
      out.textContent = "Census script failed to load (@require). Reinstall the userscript.";
      return;
    }
    title.textContent = `Crafting Recipe Census (read-only) ${census.RUNTIME || census.VERSION || ""}`;
    try {
      const status = fmt(await census.status());
      out.textContent = message ? `${message}\n\n${status}` : status;
    } catch (e) {
      out.textContent = `status error: ${e && e.message ? e.message : e}`;
    }
    if (census.logs) logView.textContent = census.logs().slice(-12).join("\n");
  };

  const button = (label, fn) => {
    const b = doc.createElement("button");
    b.type = "button";
    b.textContent = label;
    b.setAttribute(
      "style",
      "flex:1 1 auto;min-width:70px;padding:10px 8px;font:600 14px system-ui,sans-serif;" +
        "background:#2b2b2b;color:#fff;border:1px solid #666;border-radius:6px",
    );
    b.addEventListener("click", async () => {
      message = "";
      try {
        const census = findCensus();
        if (!census && label !== "Close") throw new Error("census script not loaded");
        await fn(census);
      } catch (e) {
        show(`${label} error: ${e && e.message ? e.message : e}`);
      }
      await refresh();
    });
    bar.append(b);
  };

  let runPromise = null;
  button("Run", async (census) => {
    if (runPromise) return show("Already running.");
    show("Starting...");
    runPromise = Promise.resolve()
      .then(() => census.run())
      .then(
        () => show(""),
        (e) => show(`Run error: ${e && e.message ? e.message : e}`),
      )
      .finally(() => {
        runPromise = null;
        refresh();
      });
  });
  button("Stop", async (census) => census.stop());
  button("Download", async (census) => {
    const name = await census.download();
    show(`Saved ${name}\nMove it to harvests/inbox/ in the repo.`);
  });
  button("Reset", async (census) => {
    if (runPromise) throw new Error("tap Stop and wait for the run to halt first");
    if (!w.confirm("Discard the saved census state and start over?")) return;
    await census.reset();
  });
  button("Close", async () => {
    w.sessionStorage.removeItem(ARM_KEY);
    clearInterval(timer);
    panel.remove();
  });

  const attach = () => {
    if (!panel.isConnected && doc.body) doc.body.append(panel);
  };
  const timer = setInterval(() => {
    attach();
    refresh();
  }, 1000);
  attach();
  refresh();
})();
