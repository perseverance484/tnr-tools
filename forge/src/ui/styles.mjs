// One stylesheet, installed through CSSOM. Mobile first: Firefox Android, one column, big taps.
//
// SCOPING (this is a correctness rule, not a tidiness one). Forge now mounts on a live TNR
// application route, inside an overlay, with the game's own document still under it. A bare
// `html, body`, `*`, `button` or `h2` rule would restyle the carrier page - and would keep
// restyling it after Forge is closed, because an adopted stylesheet outlives the overlay node.
// So every selector below is scoped to .f-host / .f-app, the custom properties and color-scheme
// live on those two elements rather than :root, and the only rules that touch the document
// itself live in CSS_DOC, which is installed on the /forge entry splash and nowhere else.

const TOKENS = `color-scheme: dark; --bg:#0f1115; --panel:#171a21; --line:#2a2f3a; --ink:#e8eaf0; --mute:#9aa3b2; --ok:#5fbf8a; --warn:#d9a441; --bad:#e0655f; --acc:#7aa2ff; --sent:#b08cff;`;

/** Document-level reset. ONLY for the standalone /forge entry splash. Never on a carrier page. */
export const CSS_DOC = `
html, body { margin:0; padding:0; background:#0f1115; color:#e8eaf0; font: 15px/1.45 system-ui, -apple-system, "Segoe UI", Roboto, sans-serif; -webkit-text-size-adjust:100%; }
`;

export const CSS = `
.f-host { ${TOKENS} position:fixed; inset:0; z-index:2147483000; overflow:auto; -webkit-overflow-scrolling:touch; background:var(--bg); color:var(--ink); font: 15px/1.45 system-ui, -apple-system, "Segoe UI", Roboto, sans-serif; }
.f-app { ${TOKENS} min-height:100%; display:flex; flex-direction:column; background:var(--bg); color:var(--ink); font: 15px/1.45 system-ui, -apple-system, "Segoe UI", Roboto, sans-serif; text-align:left; }
.f-app, .f-app * { box-sizing:border-box; }
.f-app .f-top { position:sticky; top:0; z-index:10; background:var(--panel); border-bottom:1px solid var(--line); display:flex; align-items:center; gap:8px; padding:8px 10px; }
.f-app .f-title { font-weight:700; letter-spacing:.02em; }
.f-app .f-ver { color:var(--mute); font-size:12px; margin-left:auto; }
.f-app .f-exit { min-height:32px; padding:4px 10px; font-size:13px; }
.f-app .f-nav { display:flex; gap:4px; overflow-x:auto; padding:6px 8px; background:var(--panel); border-bottom:1px solid var(--line); }
.f-app .f-nav button { flex:1 0 auto; min-height:40px; }
.f-app .f-nav button[aria-current="page"] { background:var(--acc); color:#0b0d12; }
.f-app .f-main { flex:1; padding:12px 10px 80px; max-width:760px; width:100%; margin:0 auto; }
.f-app h2 { font-size:17px; margin:14px 0 8px; } .f-app h3 { font-size:14px; color:var(--mute); margin:12px 0 6px; text-transform:uppercase; letter-spacing:.06em; }
.f-app button, .f-app .f-btn { font:inherit; min-height:44px; padding:8px 14px; border:1px solid var(--line); border-radius:8px; background:#222733; color:var(--ink); cursor:pointer; }
.f-app button:disabled { opacity:.45; cursor:default; }
.f-app button.f-primary { background:var(--acc); color:#0b0d12; border-color:transparent; font-weight:600; }
.f-app button.f-danger { border-color:var(--bad); color:var(--bad); }
.f-app input[type=text], .f-app input[type=password], .f-app input[type=search], .f-app textarea { font:inherit; width:100%; min-height:44px; padding:8px 10px; border:1px solid var(--line); border-radius:8px; background:#0b0d12; color:var(--ink); }
.f-app textarea { min-height:160px; font-family: ui-monospace, Menlo, monospace; font-size:12px; }
.f-app .f-card { background:var(--panel); border:1px solid var(--line); border-radius:10px; padding:10px 12px; margin:8px 0; }
.f-app .f-row { display:flex; align-items:center; gap:10px; padding:10px 0; border-bottom:1px solid var(--line); }
.f-app .f-row:last-child { border-bottom:0; }
.f-app .f-row.f-tap { cursor:pointer; } .f-app .f-row.f-tap:active { background:#1d2230; }
.f-app .f-grow { flex:1; min-width:0; } .f-app .f-mute { color:var(--mute); font-size:13px; } .f-app .f-mono { font-family: ui-monospace, Menlo, monospace; font-size:12px; word-break:break-all; }
.f-app .f-pill { display:inline-block; padding:2px 8px; border-radius:999px; font-size:12px; font-weight:600; border:1px solid var(--line); color:var(--mute); }
.f-app .f-pill.PLANNED { color:var(--mute); } .f-app .f-pill.SENT { color:var(--sent); border-color:var(--sent); } .f-app .f-pill.CONFIRMED { color:var(--acc); border-color:var(--acc); }
.f-app .f-pill.VERIFIED, .f-app .f-pill.DONE { color:var(--ok); border-color:var(--ok); } .f-app .f-pill.FAILED, .f-app .f-pill.ABORTED { color:var(--bad); border-color:var(--bad); }
.f-app .f-pill.ORPHANED, .f-app .f-pill.PAUSED, .f-app .f-pill.INCOMPLETE { color:var(--warn); border-color:var(--warn); } .f-app .f-pill.SKIPPED { color:var(--mute); }
.f-app .f-authbar { padding:0 10px; max-width:760px; width:100%; margin:0 auto; }
.f-app .f-authbar:empty { display:none; }
.f-app .f-banner { padding:10px 12px; border-radius:10px; margin:8px 0; border:1px solid; }
.f-app .f-banner.warn { border-color:var(--warn); background:#2a2312; } .f-app .f-banner.bad { border-color:var(--bad); background:#2a1515; } .f-app .f-banner.ok { border-color:var(--ok); background:#12261c; } .f-app .f-banner.info { border-color:var(--acc); background:#141b2e; }
.f-app .f-bar { height:6px; background:#0b0d12; border-radius:4px; overflow:hidden; margin:6px 0; } .f-app .f-bar > i { display:block; height:100%; background:var(--acc); }
.f-app .f-bar.warn > i { background:var(--warn); }
.f-app .f-actions { display:flex; gap:8px; flex-wrap:wrap; margin-top:8px; }
.f-app .f-kv { display:grid; grid-template-columns: auto 1fr; gap:4px 12px; font-size:13px; } .f-app .f-kv b { color:var(--mute); font-weight:500; }
.f-app .f-err { white-space:pre-wrap; font-family: ui-monospace, Menlo, monospace; font-size:12px; color:#ffb4b0; }
.f-app .f-toast { position:fixed; left:10px; right:10px; bottom:12px; z-index:2147483001; }
.f-app details summary { cursor:pointer; color:var(--mute); }
.f-boot .f-mute { color:var(--mute); font-size:13px; }
.f-boot p { margin:8px 0; max-width:52ch; }
.f-boot { ${TOKENS} padding:16px; background:var(--bg); color:var(--ink); min-height:100vh; font: 15px/1.45 system-ui, -apple-system, "Segoe UI", Roboto, sans-serif; }
`;
