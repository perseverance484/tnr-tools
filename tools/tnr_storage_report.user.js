// ==UserScript==
// @name         TNR storage report (read-only)
// @namespace    tnr-tools-diagnostics
// @version      1.0.0
// @description  Shows what is using this site's browser storage (localStorage keys by size, IndexedDB databases, the browser's quota estimate). Reads only; never writes or deletes anything.
// @match        *://www.theninja-rpg.com/*
// @match        *://theninja-rpg.com/*
// @grant        none
// @run-at       document-idle
// ==/UserScript==
(async () => {
  const kb = (n) => (n / 1024).toFixed(1) + " KB";
  const rows = [];
  let lsTotal = 0;
  try {
    for (let i = 0; i < localStorage.length; i++) {
      const k = localStorage.key(i);
      const v = localStorage.getItem(k) || "";
      const bytes = (k.length + v.length) * 2; // UTF-16, as browsers count it
      lsTotal += bytes;
      rows.push([k, bytes]);
    }
  } catch (e) { rows.push(["(localStorage unreadable: " + e.message + ")", 0]); }
  rows.sort((a, b) => b[1] - a[1]);
  let est = "unavailable";
  try {
    if (navigator.storage && navigator.storage.estimate) {
      const e = await navigator.storage.estimate();
      est = `${kb(e.usage || 0)} used of ${kb(e.quota || 0)}`;
    }
  } catch (e) { est = "error: " + e.message; }
  let dbs = "unavailable";
  try { if (indexedDB.databases) dbs = (await indexedDB.databases()).map((d) => d.name).join(", ") || "(none)"; } catch (e) { dbs = "error: " + e.message; }
  const box = document.createElement("div");
  box.style.cssText = "position:fixed;z-index:2147483647;top:8px;left:8px;right:8px;max-height:70vh;overflow:auto;" +
    "background:#111;color:#eee;font:12px/1.4 monospace;padding:10px;border:2px solid #6cf;border-radius:6px";
  const close = document.createElement("button");
  close.textContent = "Close"; close.style.cssText = "float:right"; close.onclick = () => box.remove();
  const pre = document.createElement("pre");
  pre.style.cssText = "white-space:pre-wrap;margin:0";
  pre.textContent = [
    "TNR storage report (read-only)",
    "Browser estimate (IndexedDB + cache + localStorage): " + est,
    "localStorage total: " + kb(lsTotal) + " across " + rows.length + " keys (most browsers allow ~5,000 KB)",
    "IndexedDB databases: " + dbs,
    "",
    "Largest localStorage keys:",
    ...rows.slice(0, 15).map(([k, b]) => "  " + kb(b).padStart(10) + "  " + k),
  ].join("\n");
  box.append(close, pre);
  document.body.appendChild(box);
})();
