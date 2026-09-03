// One stylesheet, installed through CSSOM. Mobile first: Firefox Android, one column, big taps.
export const CSS = `
:root { color-scheme: dark; --bg:#0f1115; --panel:#171a21; --line:#2a2f3a; --ink:#e8eaf0; --mute:#9aa3b2; --ok:#5fbf8a; --warn:#d9a441; --bad:#e0655f; --acc:#7aa2ff; --sent:#b08cff; }
html, body { margin:0; padding:0; background:var(--bg); color:var(--ink); font: 15px/1.45 system-ui, -apple-system, "Segoe UI", Roboto, sans-serif; -webkit-text-size-adjust:100%; }
* { box-sizing:border-box; }
.f-app { min-height:100vh; display:flex; flex-direction:column; }
.f-top { position:sticky; top:0; z-index:10; background:var(--panel); border-bottom:1px solid var(--line); display:flex; align-items:center; gap:8px; padding:8px 10px; }
.f-title { font-weight:700; letter-spacing:.02em; }
.f-ver { color:var(--mute); font-size:12px; margin-left:auto; }
.f-nav { display:flex; gap:4px; overflow-x:auto; padding:6px 8px; background:var(--panel); border-bottom:1px solid var(--line); }
.f-nav button { flex:1 0 auto; min-height:40px; }
.f-nav button[aria-current="page"] { background:var(--acc); color:#0b0d12; }
.f-main { flex:1; padding:12px 10px 80px; max-width:760px; width:100%; margin:0 auto; }
h2 { font-size:17px; margin:14px 0 8px; } h3 { font-size:14px; color:var(--mute); margin:12px 0 6px; text-transform:uppercase; letter-spacing:.06em; }
button, .f-btn { font:inherit; min-height:44px; padding:8px 14px; border:1px solid var(--line); border-radius:8px; background:#222733; color:var(--ink); cursor:pointer; }
button:disabled { opacity:.45; cursor:default; }
button.f-primary { background:var(--acc); color:#0b0d12; border-color:transparent; font-weight:600; }
button.f-danger { border-color:var(--bad); color:var(--bad); }
input[type=text], input[type=password], input[type=search], textarea { font:inherit; width:100%; min-height:44px; padding:8px 10px; border:1px solid var(--line); border-radius:8px; background:#0b0d12; color:var(--ink); }
textarea { min-height:160px; font-family: ui-monospace, Menlo, monospace; font-size:12px; }
.f-card { background:var(--panel); border:1px solid var(--line); border-radius:10px; padding:10px 12px; margin:8px 0; }
.f-row { display:flex; align-items:center; gap:10px; padding:10px 0; border-bottom:1px solid var(--line); }
.f-row:last-child { border-bottom:0; }
.f-row.f-tap { cursor:pointer; } .f-row.f-tap:active { background:#1d2230; }
.f-grow { flex:1; min-width:0; } .f-mute { color:var(--mute); font-size:13px; } .f-mono { font-family: ui-monospace, Menlo, monospace; font-size:12px; word-break:break-all; }
.f-pill { display:inline-block; padding:2px 8px; border-radius:999px; font-size:12px; font-weight:600; border:1px solid var(--line); color:var(--mute); }
.f-pill.PLANNED { color:var(--mute); } .f-pill.SENT { color:var(--sent); border-color:var(--sent); } .f-pill.CONFIRMED { color:var(--acc); border-color:var(--acc); }
.f-pill.VERIFIED, .f-pill.DONE { color:var(--ok); border-color:var(--ok); } .f-pill.FAILED, .f-pill.ABORTED { color:var(--bad); border-color:var(--bad); }
.f-pill.ORPHANED, .f-pill.PAUSED { color:var(--warn); border-color:var(--warn); } .f-pill.SKIPPED { color:var(--mute); }
.f-banner { padding:10px 12px; border-radius:10px; margin:8px 0; border:1px solid; }
.f-banner.warn { border-color:var(--warn); background:#2a2312; } .f-banner.bad { border-color:var(--bad); background:#2a1515; } .f-banner.ok { border-color:var(--ok); background:#12261c; } .f-banner.info { border-color:var(--acc); background:#141b2e; }
.f-bar { height:6px; background:#0b0d12; border-radius:4px; overflow:hidden; margin:6px 0; } .f-bar > i { display:block; height:100%; background:var(--acc); }
.f-bar.warn > i { background:var(--warn); }
.f-actions { display:flex; gap:8px; flex-wrap:wrap; margin-top:8px; }
.f-kv { display:grid; grid-template-columns: auto 1fr; gap:4px 12px; font-size:13px; } .f-kv b { color:var(--mute); font-weight:500; }
.f-err { white-space:pre-wrap; font-family: ui-monospace, Menlo, monospace; font-size:12px; color:#ffb4b0; }
.f-toast { position:fixed; left:10px; right:10px; bottom:12px; z-index:20; }
details summary { cursor:pointer; color:var(--mute); }
`;
