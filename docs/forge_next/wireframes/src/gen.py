#!/usr/bin/env python3
"""Forge Next wireframe generator (planning artifact only; not production UI).

specs.json: {title, intro, screens:[{id, title, purpose, flow, notes[], default_theme,
  mobile:[blocks], desktop:{columns, regions:[{name, span, blocks}]}}]}
themes.json: {name: {label, blurb, tokens:{bg,paper,raised,line,ink,mute,acc,read,mut,pub,warn,sent,ok,bad,gold}}}

Block kinds: brand, bar, nav (items, active, bottom), rail (items, active), opmode (mode, counts, note),
banner (tone, head, body, actions), card (title, pill, risk, blocks), row (title, sub, pills, actions),
list (rows), lanes (items:[{label, sub, accent}]), tiles (items:[{label, value, tone}]), action (label,
variant, hint), kv (pairs), tabs (items, active), form (fields:[[label, value, cls]]), preview (label, body),
diff (rows:[[field, old, new]]), progress (pct, label), text (text), quick (items:[{label, sub, variant}]),
seg (cells:[STATE..], label), sheet (title, lines[], action{label,variant,state}, cancel), story (nodes:[{kind,title,sub,pills}]), lamps (head, items:[{glyph,label,value,tone,actions}]).
Every page is self-contained HTML (inline CSS, one tiny theme-switch script), no external resources.
"""
import html
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "out")


def esc(s):
    return html.escape(str(s), quote=True)


def acts(items):
    return "".join(f'<span class="act">{esc(a)}</span>' for a in items or [])


def pills(items):
    return "".join(f'<span class="pill {esc(p)}">{esc(p)}</span>' for p in items or [])


def block(b):
    k = b.get("kind", "text")
    risk = b.get("risk", "")
    cls = f"blk {k}" + (f" risk-{risk}" if risk else "")
    if k == "brand":
        return f'<div class="{cls}"><span class="wordmark">TNR <b>FORGE</b></span><span class="tag">{esc(b.get("tag","content operations"))}</span>{acts(b.get("actions"))}</div>'
    if k == "bar":
        chips = "".join(f'<span class="chip">{esc(c)}</span>' for c in b.get("chips", []))
        return f'<div class="{cls}"><span class="ttl">{esc(b.get("title",""))}</span><span class="sub">{esc(b.get("sub",""))}</span>{chips}</div>'
    if k == "nav":
        items = "".join(f'<span class="ni{" on" if i == b.get("active") else ""}">{esc(i)}</span>' for i in b.get("items", []))
        return f'<div class="{cls}{" bottom" if b.get("bottom") else ""}">{items}</div>'
    if k == "rail":
        items = "".join(f'<span class="ri{" on" if i == b.get("active") else ""}">{esc(i)}</span>' for i in b.get("items", []))
        return f'<div class="{cls}"><div class="wordmark">TNR <b>FORGE</b></div>{items}</div>'
    if k == "opmode":
        mode = b.get("mode", "READ ONLY")
        counts = "".join(f'<span class="cnt"><b>{esc(v)}</b>{esc(kk)}</span>' for kk, v in b.get("counts", []))
        note = f'<div class="note">{esc(b["note"])}</div>' if b.get("note") else ""
        return f'<div class="{cls} mode-{esc(mode.lower().replace(" ", "-"))}"><span class="mode">{esc(mode)}</span><span class="counts">{counts}</span>{note}</div>'
    if k == "banner":
        return f'<div class="{cls} tone-{esc(b.get("tone","info"))}"><b>{esc(b.get("head",""))}</b> {esc(b.get("body",""))}{acts(b.get("actions"))}</div>'
    if k == "card":
        inner = "".join(block(x) for x in b.get("blocks", []))
        p = b.get("pill", "")
        pill = f'<span class="pill {esc(p)}">{esc(p)}</span>' if p else ""
        return f'<div class="{cls}"><div class="ch">{esc(b.get("title",""))}{pill}<span class="chs">{esc(b.get("sub",""))}</span></div>{inner}</div>'
    if k == "row":
        return f'<div class="{cls}"><div class="rmain"><div class="rt">{esc(b.get("title",""))}{pills(b.get("pills"))}</div><div class="rs">{esc(b.get("sub",""))}</div></div>{acts(b.get("actions"))}</div>'
    if k == "list":
        return f'<div class="{cls}">' + "".join(block(dict(x, kind="row")) for x in b.get("rows", [])) + "</div>"
    if k == "lanes":
        items = "".join(f'<div class="lane" style="--lane:{esc(i.get("accent","#888"))}"><div class="ln">{esc(i.get("label",""))}</div><div class="ls">{esc(i.get("sub",""))}</div>{("<div class=lc>" + esc(i["count"]) + "</div>") if i.get("count") else ""}</div>' for i in b.get("items", []))
        return f'<div class="{cls}">{items}</div>'
    if k == "tiles":
        items = "".join(f'<div class="tile tone-{esc(i.get("tone","info"))}"><div class="tl">{esc(i.get("label",""))}</div><div class="tv">{esc(i.get("value",""))}</div><div class="ts">{esc(i.get("sub",""))}</div></div>' for i in b.get("items", []))
        return f'<div class="{cls}">{items}</div>'
    if k == "quick":
        items = "".join(f'<div class="qa {esc(i.get("variant","read"))}"><div class="ql">{esc(i.get("label",""))}</div><div class="qs">{esc(i.get("sub",""))}</div></div>' for i in b.get("items", []))
        return f'<div class="{cls}">{items}</div>'
    if k == "action":
        hint = f'<span class="hint">{esc(b["hint"])}</span>' if b.get("hint") else ""
        return f'<div class="{cls}"><span class="btn {esc(b.get("variant",""))}">{esc(b.get("label",""))}</span>{hint}</div>'
    if k == "kv":
        return f'<div class="{cls}">' + "".join(f"<b>{esc(kk)}</b><span>{esc(vv)}</span>" for kk, vv in b.get("pairs", [])) + "</div>"
    if k == "tabs":
        return f'<div class="{cls}">' + "".join(f'<span class="tab{" on" if i == b.get("active") else ""}">{esc(i)}</span>' for i in b.get("items", [])) + "</div>"
    if k == "form":
        return f'<div class="{cls}">' + "".join(f'<label><span class="lb">{esc(f[0])}</span><span class="in {esc(f[2]) if len(f) > 2 else ""}">{esc(f[1])}</span></label>' for f in b.get("fields", [])) + "</div>"
    if k == "preview":
        return f'<div class="{cls}"><div class="pv">{esc(b.get("label","preview"))}</div><div class="pvb">{esc(b.get("body",""))}</div></div>'
    if k == "diff":
        rows = "".join(f'<div class="dr"><span class="dk">{esc(r[0])}</span><span class="dold">{esc(r[1])}</span><span class="dnew">{esc(r[2])}</span></div>' for r in b.get("rows", []))
        return f'<div class="{cls}"><div class="dh"><span>field</span><span>live value when read</span><span>proposed</span></div>{rows}</div>'
    if k == "seg":
        cells = "".join(f'<i class="sc {esc(c)}" title="{esc(c)}"></i>' for c in b.get("cells", []))
        return f'<div class="{cls}"><div class="segt">{cells}</div><span class="ps">{esc(b.get("label",""))}</span></div>'
    if k == "sheet":
        lines = "".join(f'<div class="shl">{esc(l)}</div>' for l in b.get("lines", []))
        a = b.get("action", {})
        return f'<div class="{cls} tone-{esc(a.get("variant","mutation"))}"><div class="sht">{esc(b.get("title",""))}</div>{lines}<div class="sha"><span class="btn {esc(a.get("variant","mutation"))} {esc(a.get("state",""))}">{esc(a.get("label","Confirm"))}</span><span class="spacer"></span><span class="btn ghost">{esc(b.get("cancel","Cancel"))}</span></div></div>'
    if k == "story":
        nodes = "".join(f'<div class="sn kind-{esc(n.get("kind","dialog"))}"><div class="snk">{esc(n.get("kind",""))}</div><div class="snt">{esc(n.get("title",""))}</div><div class="sns">{esc(n.get("sub",""))}</div>{pills(n.get("pills"))}</div>' for n in b.get("nodes", []))
        return f'<div class="{cls}">{nodes}</div>'
    if k == "lamps":
        items = "".join(f'<div class="lamp tone-{esc(i.get("tone","info"))}"><span class="lg">{esc(i.get("glyph","·"))}</span><span class="ll">{esc(i.get("label",""))}</span><span class="lv">{esc(i.get("value",""))}</span>{acts(i.get("actions"))}</div>' for i in b.get("items", []))
        head = f'<div class="lh">{esc(b["head"])}</div>' if b.get("head") else ""
        return f'<div class="{cls}">{head}{items}</div>'
    if k == "progress":
        return f'<div class="{cls}"><div class="pb"><i style="width:{int(b.get("pct", 40))}%"></i></div><span class="ps">{esc(b.get("label",""))}</span></div>'
    return f'<div class="{cls}">{esc(b.get("text",""))}</div>'


CSS = r"""
:root{--bg:#0d1017;--paper:#151a24;--raised:#1c2230;--line:#2c3446;--ink:#f1ede4;--mute:#9aa3b2;--acc:#4f7cff;--read:#3fbf8a;--mut:#e0862a;--pub:#c8322f;--warn:#e0a83a;--sent:#b48cff;--ok:#3fbf8a;--bad:#e0655f;--gold:#d8a94a;--radius:10px;--font:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
[data-theme="wire"]{--bg:#f4f5f7;--paper:#ffffff;--raised:#eef0f4;--line:#d7dae0;--ink:#1a1d24;--mute:#6b7280;--acc:#2f5bea;--read:#1f8f5f;--mut:#d97706;--pub:#b91c1c;--warn:#b45309;--sent:#7c3aed;--ok:#15803d;--bad:#b91c1c;--gold:#a16207}
body{margin:0;background:var(--bg);color:var(--ink);font:14px/1.4 var(--font);padding-block:16px;padding-inline:16px}
a{color:var(--acc)}
h1{font-size:18px;margin:0 0 4px}h2{font-size:12px;margin:18px 0 6px;color:var(--mute);text-transform:uppercase;letter-spacing:.08em}
.meta{color:var(--mute);margin-bottom:12px;max-width:90ch}
.frames{display:flex;gap:24px;flex-wrap:wrap;align-items:flex-start}
.phone{width:390px;min-height:844px;background:var(--bg);border:8px solid #000;border-radius:36px;box-shadow:0 12px 40px rgba(0,0,0,.45);overflow:hidden;position:relative;flex:0 0 auto}
.phone .screen{padding:10px 12px 96px;min-height:826px}
.desk{width:min(1280px,100%);min-height:760px;background:var(--bg);border:6px solid #000;border-radius:14px;box-shadow:0 12px 40px rgba(0,0,0,.45);overflow:hidden;flex:1 1 900px}
.desk .screen{display:grid;gap:14px;padding:14px;min-height:740px}
.region{border:1px dashed var(--line);border-radius:var(--radius);padding:10px;min-width:0}
.region .rn{font-size:10px;color:var(--mute);text-transform:uppercase;letter-spacing:.1em;margin-bottom:6px}
.blk{margin:6px 0}
.brand{display:flex;align-items:center;gap:10px;padding:8px 10px;border-radius:var(--radius);background:var(--paper);border:1px solid var(--line)}
.wordmark{font-weight:800;letter-spacing:.06em;color:var(--ink)}.wordmark b{color:var(--gold)}
.brand .tag{color:var(--mute);font-size:11px;text-transform:uppercase;letter-spacing:.1em;margin-right:auto}
.bar{display:flex;align-items:center;gap:8px;padding:8px 10px;border-radius:var(--radius);background:var(--paper);border:1px solid var(--line)}
.bar .ttl{font-weight:700}.bar .sub{color:var(--mute);font-size:12px;margin-left:auto}
.chip{font-size:11px;padding:2px 8px;border-radius:4px;border:1px solid var(--line);background:var(--raised);color:var(--ink)}
.nav{display:flex;gap:4px;justify-content:space-around;padding:8px;border-radius:var(--radius);background:var(--paper);border:1px solid var(--line)}
.phone .nav.bottom{position:absolute;left:0;right:0;bottom:0;border-radius:0;padding:10px 6px 18px;border-width:1px 0 0}
.ni{flex:1;text-align:center;padding:8px 4px;border-radius:8px;font-size:12px;min-height:44px;display:flex;align-items:center;justify-content:center;color:var(--mute)}.ni.on{color:var(--acc);font-weight:700;border-top:3px solid var(--acc);border-radius:0}
.rail{display:flex;flex-direction:column;gap:4px}.rail .wordmark{padding:8px 6px 12px;font-size:16px}
.ri{padding:10px 10px;border-radius:6px;color:var(--mute);border-left:3px solid transparent}.ri.on{background:var(--raised);color:var(--ink);border-left-color:var(--mut);font-weight:600}
.opmode{display:flex;align-items:center;gap:12px;flex-wrap:wrap;padding:10px 12px;border-radius:6px;border:2px solid var(--line);background:var(--paper)}
.opmode .mode{font-weight:800;letter-spacing:.12em;font-size:13px;padding:6px 10px;border-radius:4px;background:var(--raised);color:var(--ink)}
.opmode .counts{display:flex;gap:12px;flex-wrap:wrap;color:var(--mute);font-size:12px}.opmode .cnt b{color:var(--ink);font-size:15px;margin-right:4px}
.opmode .note{flex-basis:100%;font-size:12px;color:var(--mute)}
.opmode.mode-read-only{border-color:var(--read)}.opmode.mode-read-only .mode{background:var(--read);color:#06130c}
.opmode.mode-live-write .mode{color:#fff}
.opmode.mode-live-write{border-color:var(--mut)}.opmode.mode-live-write .mode{background:var(--mut);color:#1a0d00}
.opmode.mode-publish{border-color:var(--pub);box-shadow:0 0 0 3px color-mix(in srgb,var(--pub) 30%,transparent)}.opmode.mode-publish .mode{background:var(--pub);color:#fff}
.opmode.mode-recovery{border-color:var(--warn)}.opmode.mode-recovery .mode{background:var(--warn);color:#1a1000}
.banner{padding:10px 12px;border-radius:var(--radius);border:1px solid var(--line);background:var(--paper)}
.banner.tone-ok{border-color:var(--ok)}.banner.tone-warn{border-color:var(--warn)}.banner.tone-bad{border-color:var(--bad)}.banner.tone-pub{border-color:var(--pub);border-width:2px}.banner.tone-info{border-color:var(--acc)}
.act{display:inline-flex;align-items:center;margin-left:8px;padding:6px 10px;border-radius:6px;background:var(--raised);border:1px solid var(--line);font-size:12px;min-height:36px;white-space:nowrap;color:var(--ink)}
.card{border:1px solid var(--line);border-radius:var(--radius);padding:10px;background:var(--paper);box-shadow:0 2px 0 rgba(0,0,0,.25)}
.card .ch{font-weight:700;display:flex;align-items:center;gap:8px;margin-bottom:4px}.card .chs{margin-left:auto;font-weight:400;color:var(--mute);font-size:12px}
.row{display:flex;align-items:center;gap:10px;padding:10px 0;border-bottom:1px solid var(--line);min-height:44px}.row:last-child{border-bottom:0}
.rmain{flex:1;min-width:0}.rt{font-weight:600}.rs{color:var(--mute);font-size:12px}
.lanes{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:10px}
.lane{position:relative;min-height:110px;border-radius:var(--radius);padding:12px;border:1px solid var(--line);background:linear-gradient(160deg,color-mix(in srgb,var(--lane) 38%,var(--paper)),var(--paper) 70%);box-shadow:inset 0 0 0 1px color-mix(in srgb,var(--lane) 35%,transparent)}
.lane .ln{font-weight:800;letter-spacing:.04em;text-transform:uppercase;font-size:13px}.lane .ls{color:var(--mute);font-size:12px;margin-top:4px}.lane .lc{display:inline-block;margin-top:8px;font-size:11px;padding:2px 8px;border-radius:4px;background:var(--raised);border:1px solid var(--line);color:var(--ink)}
.tiles{display:grid;grid-template-columns:repeat(auto-fill,minmax(120px,1fr));gap:8px}
.tile{border:1px solid var(--line);border-radius:8px;padding:8px 10px;background:var(--raised)}.tile .tl{font-size:11px;color:var(--mute);text-transform:uppercase;letter-spacing:.06em}.tile .tv{font-weight:700;font-size:15px;margin:2px 0}.tile .ts{font-size:11px;color:var(--mute)}
.tile.tone-ok .tv{color:var(--ok)}.tile.tone-warn .tv{color:var(--warn)}.tile.tone-bad .tv{color:var(--bad)}.tile.tone-info .tv{color:var(--acc)}
.quick{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:8px}
.qa{border-radius:8px;padding:10px 12px;border:1px solid var(--line);background:var(--raised);border-left:4px solid var(--acc)}.qa.read{border-left-color:var(--read)}.qa.mutation{border-left-color:var(--mut)}.qa.publish{border-left-color:var(--pub)}.qa.recovery{border-left-color:var(--warn)}
.qa .ql{font-weight:700}.qa .qs{font-size:12px;color:var(--mute)}
.action{display:flex;align-items:center;gap:10px;flex-wrap:wrap}
.btn{display:inline-flex;align-items:center;justify-content:center;min-height:48px;padding:10px 18px;border-radius:6px;border:1px solid var(--line);background:var(--raised);color:var(--ink);font-weight:700;letter-spacing:.02em;box-shadow:3px 3px 0 rgba(0,0,0,.35)}
.btn.primary{background:var(--acc);color:#fff;border-color:transparent}.btn.read{background:var(--read);color:#06130c;border-color:transparent}.btn.mutation{background:var(--mut);color:#fff;border:2px solid #5a0d13;border-radius:0;box-shadow:5px 5px 0 #5a0d13}.btn.publish{background:var(--pub);color:#1b1200;border:2px solid #1b1200;border-radius:0;box-shadow:5px 5px 0 #1b1200}.btn.recovery{background:transparent;color:var(--warn);border:2px solid var(--warn);border-radius:0;box-shadow:none}.btn.recovery::before{content:"↻ "}.btn.ghost{background:transparent;box-shadow:none}.btn.danger{color:var(--bad);border-color:var(--bad);background:transparent}.btn.disabled{opacity:.45;box-shadow:none}
.hint{color:var(--mute);font-size:12px}
.pill{display:inline-flex;align-items:center;gap:4px;margin-left:6px;padding:2px 8px;border-radius:4px;font-size:11px;font-weight:700;border:1px solid var(--line);color:var(--mute);vertical-align:middle;letter-spacing:.04em}
.pill::before{content:"";width:7px;height:7px;border-radius:2px;background:currentColor;display:inline-block}
.pill.SENT{color:var(--sent);border-color:var(--sent)}.pill.SENT::before{border-radius:50%}
.pill.CONFIRMED{color:var(--acc);border-color:var(--acc)}
.pill.VERIFIED,.pill.DONE,.pill.PUBLISHED,.pill.LIVE,.pill.ok{color:var(--ok);border-color:var(--ok)}
.pill.FAILED,.pill.bad{color:var(--bad);border-color:var(--bad)}.pill.FAILED::before{transform:rotate(45deg)}
.pill.ORPHANED,.pill.PAUSED,.pill.INCOMPLETE,.pill.warn,.pill.NEEDS-DECISION{color:var(--warn);border-color:var(--warn)}.pill.ORPHANED::before{clip-path:polygon(50% 0,100% 100%,0 100%)}
.pill.HIDDEN,.pill.DRAFT,.pill.PLANNED,.pill.SKIPPED{color:var(--mute);border-color:var(--mute)}
.pill.READ,.pill.READ-ONLY{color:var(--read);border-color:var(--read)}.pill.MUTATION,.pill.LIVE-WRITE{color:var(--mut);border-color:var(--mut)}.pill.PUBLISH{color:var(--pub);border-color:var(--pub)}.pill.RECOVERY{color:var(--warn);border-color:var(--warn)}.pill.FULL{color:var(--gold);border-color:var(--gold)}.pill.ADMIN{color:var(--gold);border-color:var(--gold)}
.kv{display:grid;grid-template-columns:auto 1fr;gap:4px 12px;font-size:13px}.kv b{color:var(--mute);font-weight:500}
.tabs{display:flex;gap:6px;overflow-x:auto}.tab{padding:8px 12px;border-radius:4px;border:1px solid var(--line);font-size:12px;min-height:36px;display:inline-flex;align-items:center;white-space:nowrap;color:var(--mute)}.tab.on{background:var(--ink);color:var(--bg);font-weight:700}
.form label{display:block;margin:8px 0}.form .lb{display:block;font-size:12px;color:var(--mute);margin-bottom:3px}.form .in{display:block;min-height:44px;border:1px solid var(--line);border-radius:6px;padding:10px;background:var(--raised)}.form .in.ro{opacity:.6}.form .in.area{min-height:90px}
.preview .pv{font-size:10px;color:var(--mute);text-transform:uppercase;letter-spacing:.1em}.preview .pvb{border:2px dashed var(--line);border-radius:var(--radius);padding:14px;min-height:120px;background:repeating-linear-gradient(45deg,var(--paper),var(--paper) 10px,var(--raised) 10px,var(--raised) 20px);color:var(--mute)}
.diff{font-size:12px}.diff .dh,.diff .dr{display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;padding:6px 0;border-bottom:1px solid var(--line)}.diff .dh{color:var(--mute);text-transform:uppercase;font-size:10px;letter-spacing:.08em}.dold{color:var(--mute);text-decoration:line-through}.dnew{color:var(--ok);font-weight:600}
.progress .pb{height:8px;background:var(--raised);border-radius:6px;overflow:hidden}.progress .pb>i{display:block;height:100%;background:linear-gradient(90deg,var(--acc),color-mix(in srgb,var(--acc) 60%,#fff))}
.progress.tone-warn .pb>i{background:var(--warn)}
.progress.tone-bad .pb>i{background:repeating-linear-gradient(45deg,var(--bad),var(--bad) 4px,transparent 4px,transparent 8px);outline:1px solid var(--bad);outline-offset:-1px}
.progress.tone-bad .ps,.progress.tone-warn .ps{color:var(--ink)}.progress .ps{font-size:12px;color:var(--mute)}
.seg .segt{display:flex;gap:2px;height:14px;border:1px solid var(--line);border-radius:4px;padding:1px;background:var(--raised)}.seg .sc{flex:1;display:block;border-radius:2px;background:transparent}
.seg .sc.VERIFIED{background:var(--ok)}.seg .sc.CONFIRMED{background:var(--acc)}.seg .sc.SENT{background:repeating-linear-gradient(45deg,var(--sent),var(--sent) 3px,transparent 3px,transparent 6px)}.seg .sc.FAILED{background:var(--bad)}.seg .sc.SKIPPED{background:var(--line)}.seg .sc.ORPHANED{background:var(--ink)}.seg .sc.RUNNING{background:linear-gradient(90deg,var(--acc),#fff)}.seg .sc.PLANNED{background:transparent;outline:1px dashed var(--line);outline-offset:-1px}
.sheet{border:2px solid var(--line);border-radius:12px;padding:14px;background:var(--raised);box-shadow:0 18px 40px rgba(0,0,0,.6)}.sheet.tone-mutation{border-color:var(--mut)}.sheet.tone-publish{border-color:var(--pub);box-shadow:0 0 0 3px color-mix(in srgb,var(--pub) 30%,transparent),0 18px 40px rgba(0,0,0,.6)}.sheet.tone-recovery{border-color:var(--warn)}
.sheet .sht{font-weight:800;font-size:16px;margin-bottom:6px}.sheet .shl{font-size:13px;margin:4px 0;padding-left:10px;border-left:2px solid var(--line)}.sheet .sha{display:flex;align-items:center;gap:10px;margin-top:12px}.sheet .spacer{flex:1}
.story{display:flex;flex-direction:column;gap:0}.sn{border:1px solid var(--line);border-radius:8px;padding:8px 10px;background:var(--raised);position:relative;margin-bottom:14px}.sn::after{content:"";position:absolute;left:18px;bottom:-14px;width:2px;height:14px;background:var(--line)}.sn:last-child::after{display:none}.sn .snk{font-size:10px;text-transform:uppercase;letter-spacing:.1em;color:var(--mute)}.sn .snt{font-weight:700}.sn .sns{font-size:12px;color:var(--mute)}.sn.kind-battle{border-left:4px solid var(--mut)}.sn.kind-decision{border-left:4px solid var(--warn)}.sn.kind-win{border-left:4px solid var(--ok)}.sn.kind-dialog{border-left:4px solid var(--acc)}
.lamps{border:1px solid var(--line);border-radius:var(--radius);background:var(--paper);padding:6px 10px}.lamps .lh{font-weight:700;margin:4px 0 6px}.lamp{display:flex;align-items:center;gap:10px;padding:8px 0;border-bottom:1px solid var(--line);min-height:44px;flex-wrap:wrap}.lamp .act{margin-left:32px}.lamp:last-child{border-bottom:0}.lamp .lg{width:22px;text-align:center;font-weight:900}.lamp .ll{font-weight:600;flex:0 0 118px}.lamp .lv{flex:1 1 140px;color:var(--mute);font-size:13px}.lamp.tone-ok .lg{color:var(--ok)}.lamp.tone-warn .lg{color:var(--warn)}.lamp.tone-bad .lg{color:var(--bad)}.lamp.tone-info .lg{color:var(--acc)}.lamp.tone-mute .lg{color:var(--mute)}
.risk-read{border-left:4px solid var(--read)}.risk-mutation{border-left:4px solid var(--mut)}.risk-publish{border-left:4px solid var(--pub)}.risk-recovery{border-left:4px solid var(--warn)}
.text{color:var(--mute);font-size:13px}
.themebar{display:flex;gap:8px;align-items:center;margin:8px 0 14px;flex-wrap:wrap}.themebar button{min-height:36px;padding:6px 12px;border-radius:6px;border:1px solid var(--line);background:var(--paper);color:var(--ink);font:inherit}
.legend{display:flex;gap:12px;flex-wrap:wrap;font-size:12px;color:var(--mute);margin:8px 0}.legend span{display:inline-flex;align-items:center;gap:6px}.legend i{display:inline-block;width:14px;height:14px;border-radius:3px}
.idx a{display:block;padding:10px;border:1px solid var(--line);border-radius:10px;background:var(--paper);margin:6px 0;color:var(--ink);text-decoration:none}
@media (max-width:900px){.desk{display:none}.phone{margin:0 auto}}
"""


def theme_css(name, t):
    vars_ = ";".join(f"--{k}:{v}" for k, v in t.get("tokens", {}).items())
    return f'[data-theme="{name}"]{{{vars_}}}' if vars_ else ""


def page(spec, themes, index_href="index.html"):
    mob = "".join(block(b) for b in spec.get("mobile", []))
    regions = spec.get("desktop", {}).get("regions", [])
    cols = spec.get("desktop", {}).get("columns", "200px minmax(360px,2fr) minmax(260px,1fr)")
    desk = "".join(f'<div class="region" style="grid-column:{esc(r.get("span","auto"))}"><div class="rn">{esc(r["name"])}</div>{"".join(block(b) for b in r.get("blocks", []))}</div>' for r in regions)
    tcss = "\n".join(theme_css(n, t) for n, t in themes.items())
    tbtns = "".join(f'<button data-set="{esc(n)}">{esc(t.get("label", n))}</button>' for n, t in themes.items())
    notes = "".join(f"<li>{esc(n)}</li>" for n in spec.get("notes", []))
    pend = "".join(f"<li>{esc(n)}</li>" for n in spec.get("pending", []))
    pend = f'<h2>Open director decisions this screen depends on</h2><ul class="meta">{pend}</ul>' if pend else ""
    cites = "".join(f"<li>{esc(n)}</li>" for n in spec.get("cites", []))
    cites = f'<h2>Evidence</h2><ul class="meta">{cites}</ul>' if cites else ""
    return f"""<!DOCTYPE html><html lang="en" data-theme="{esc(spec.get("default_theme","forge"))}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(spec["title"])} · Forge Next wireframe</title><style>{CSS}\n{tcss}</style></head><body>
<a href="{esc(index_href)}">← wireframe index</a> <span class="hint">· planning wireframe (not production UI); labels marked PENDING are open director decisions</span>
<h1>{esc(spec["title"])} <span style="color:var(--mute);font-weight:400;font-size:13px">({esc(spec["id"])})</span></h1>
<div class="meta">{esc(spec.get("purpose",""))}</div>
<div class="themebar"><span class="hint">theme:</span>{tbtns}</div>
<div class="legend"><span><i style="background:var(--read)"></i>read / research</span><span><i style="background:var(--mut)"></i>live write</span><span><i style="background:var(--pub)"></i>publish</span><span><i style="background:var(--warn)"></i>recovery / attention</span><span><i style="background:var(--sent)"></i>SENT (ambiguous)</span><span><i style="background:var(--gold)"></i>admin / brand</span></div>
<div class="frames">
<div class="phone"><div class="screen">{mob}</div></div>
<div class="desk"><div class="screen" style="grid-template-columns:{esc(cols)}">{desk}</div></div>
</div>
<h2>Flow and notes</h2><div class="meta">{esc(spec.get("flow",""))}</div><ul class="meta">{notes}</ul>{pend}{cites}
<script>document.querySelectorAll('.themebar button').forEach(b=>b.addEventListener('click',()=>{{document.documentElement.setAttribute('data-theme',b.dataset.set)}}));</script>
</body></html>"""


def index(specs, themes, title, intro):
    links = "".join(f'<a href="{esc(s["id"])}.html"><b>{esc(s["title"])}</b> <span class="hint">{esc(s.get("purpose",""))}</span></a>' for s in specs)
    tcss = "\n".join(theme_css(n, t) for n, t in themes.items())
    tiles = ""
    for n, t in themes.items():
        toks = t.get("tokens", {})
        sw = "".join(f'<span title="{esc(k)}" style="display:inline-block;width:26px;height:26px;border-radius:5px;background:{esc(v)};border:1px solid #0006;margin:1px"></span>' for k, v in toks.items())
        tiles += f'<div class="card" data-theme="{esc(n)}" style="background:var(--paper);color:var(--ink);flex:1 1 320px"><div class="ch">{esc(t.get("label", n))}</div><div class="text">{esc(t.get("blurb",""))}</div><div style="margin:8px 0">{sw}</div><div class="opmode mode-live-write"><span class="mode">LIVE WRITE</span><span class="counts"><span class="cnt"><b>3</b>creates</span><span class="cnt"><b>2</b>updates</span></span></div><div class="action"><span class="btn read">Run captures</span><span class="btn mutation">Start job</span><span class="btn publish">Publish</span></div><div><span class="pill SENT">SENT</span><span class="pill CONFIRMED">CONFIRMED</span><span class="pill VERIFIED">VERIFIED</span><span class="pill ORPHANED">ORPHANED</span><span class="pill HIDDEN">HIDDEN</span></div></div>'
    return f"""<!DOCTYPE html><html lang="en" data-theme="forge"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)}</title><style>{CSS}\n{tcss}</style></head><body>
<h1>{esc(title)}</h1><div class="meta">{esc(intro)}</div>
<h2>Screens</h2><div class="idx">{links}</div>
<h2>Theme tokens (style tiles)</h2><div class="frames" style="gap:12px">{tiles}</div>
</body></html>"""


def main():
    specs = json.load(open(os.path.join(HERE, "specs.json")))
    themes = json.load(open(os.path.join(HERE, "themes.json")))
    os.makedirs(OUT, exist_ok=True)
    for s in specs["screens"]:
        with open(os.path.join(OUT, s["id"] + ".html"), "w") as f:
            f.write(page(s, themes))
    with open(os.path.join(OUT, "index.html"), "w") as f:
        f.write(index(specs["screens"], themes, specs.get("title", "Forge Next wireframes"), specs.get("intro", "")))
    print("wrote", len(specs["screens"]) + 1, "files to", OUT)


if __name__ == "__main__":
    main()
