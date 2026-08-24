/* TNR Deleter v1.1 (hosted body; loaded via @require loader)
 * Batch content deletion with per-record gates. Never runs on load; DRY RUN default.
 * Entities: quest, jutsu, ai, aiProfile, item. Pre-checks: ai -> getAiRelations must
 * return zero questsUsingAi; jutsu -> getJutsuRelations must be empty; others ->
 * existence check only. POST tRPC mutation {id}. Checkpointed per entity+id in
 * localStorage (tnr_del_v1); rerun skips done ids. 1500ms pace, backoff on 429. */
(function () {
  "use strict";
  if (window.top !== window.self) return;
  if (window.__tnrDeleterLoaded) return;
  window.__tnrDeleterLoaded = true;
  var PACE = 1500, KEY = "tnr_del_v1";
  var state = { run: false, done: JSON.parse(localStorage.getItem(KEY) || "{}") };
  function save() { localStorage.setItem(KEY, JSON.stringify(state.done)); }
  function sleep(ms) { return new Promise(function (r) { setTimeout(r, ms); }); }
  function el(tag, css, text) {
    var e = document.createElement(tag);
    if (css) for (var k in css) e.style[k] = css[k];
    if (text !== undefined) e.textContent = text;
    return e;
  }
  function gurl(proc, input) {
    return location.origin + "/api/trpc/" + proc + "?batch=1&input=" +
      encodeURIComponent(JSON.stringify({ "0": input === undefined ? { json: null, meta: { values: ["undefined"] } } : { json: input } }));
  }
  async function gcall(proc, input) {
    var res = await fetch(gurl(proc, input), { credentials: "include" });
    if (res.status === 429) throw new Error("429");
    var j = await res.json();
    var e0 = j && j[0];
    if (e0 && e0.error) throw new Error((e0.error.json && e0.error.json.message) || "error");
    return e0 && e0.result && e0.result.data ? e0.result.data.json : null;
  }
  async function pcall(proc, input) {
    var res = await fetch(location.origin + "/api/trpc/" + proc + "?batch=1", {
      method: "POST", credentials: "include",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ "0": { json: input } })
    });
    if (res.status === 429) throw new Error("429");
    var j = await res.json();
    var e0 = j && j[0];
    if (e0 && e0.error) throw new Error((e0.error.json && e0.error.json.message) || "delete rejected");
    var d = e0 && e0.result && e0.result.data ? e0.result.data.json : null;
    if (d && d.success === false) throw new Error(d.message || "success=false");
    return d;
  }
  function emptyRelations(obj) {
    if (!obj) return true;
    for (var k in obj) {
      var v = obj[k];
      if (Array.isArray(v) && v.length) return false;
      if (v && typeof v === "object" && !emptyRelations(v)) return false;
    }
    return true;
  }
  var GATES = {
    quest: { pre: function (id) { return gcall("quests.get", { id: id }); }, del: "quests.delete", key: "id" },
    asset: { pre: function (id) { return gcall("asset.get", { id: id }); }, del: "asset.delete", key: "id" },
    jutsu: { pre: async function (id) {
        var rel = await gcall("jutsu.getJutsuRelations", { jutsuId: id });
        if (!emptyRelations(rel)) throw new Error("BLOCKED: relations not empty " + JSON.stringify(rel).slice(0, 120));
        return true;
      }, del: "jutsu.delete", key: "id" },
    ai: { pre: async function (id) {
        var rel = await gcall("ai.getAiRelations", { aiId: id });
        var qs = rel && rel.questsUsingAi;
        if (qs && qs.length) throw new Error("BLOCKED: used by " + qs.map(function (q) { return q.name; }).join(", ").slice(0, 100));
        return true;
      }, del: "profile.delete", key: "id" },
    aiProfile: { pre: function (id) { return gcall("ai.getAiProfile", { id: id }); }, del: "ai.deleteAiProfile", key: "id" },
    item: { pre: function (id) { return gcall("item.get", { id: id }); }, del: "item.delete", key: "id" }
  };
  var panel = el("div", { position: "fixed", right: "8px", bottom: "8px", zIndex: 99999, background: "#131722",
    color: "#eee", font: "12px monospace", padding: "8px", border: "1px solid #444", borderRadius: "8px",
    width: "300px", maxHeight: "70vh", overflow: "auto" });
  panel.appendChild(el("div", { fontWeight: "bold", marginBottom: "4px" }, "TNR Deleter v1.1"));
  var sel = document.createElement("select");
  ["quest", "jutsu", "ai", "aiProfile", "item"].forEach(function (t) {
    var o = document.createElement("option"); o.value = t; o.textContent = t; sel.appendChild(o);
  });
  sel.style.width = "100%"; panel.appendChild(sel);
  var ta = document.createElement("textarea");
  ta.rows = 6; ta.style.width = "100%"; ta.style.marginTop = "4px";
  ta.placeholder = "one id per line"; panel.appendChild(ta);
  var dryWrap = el("label", { display: "block", margin: "4px 0" });
  var dry = document.createElement("input"); dry.type = "checkbox"; dry.checked = true;
  dryWrap.appendChild(dry); dryWrap.appendChild(document.createTextNode(" DRY RUN (gate checks only)"));
  panel.appendChild(dryWrap);
  var btn = el("button", { width: "49%" }, "Start");
  var stop = el("button", { width: "49%", marginLeft: "2%" }, "Stop");
  var reset = el("button", { width: "100%", marginTop: "4px" }, "Reset checkpoint");
  var status = el("div", { margin: "4px 0", color: "#d9a441" }, "idle");
  var log = el("div", { whiteSpace: "pre-wrap", fontSize: "11px" });
  panel.appendChild(btn); panel.appendChild(stop); panel.appendChild(reset);
  panel.appendChild(status); panel.appendChild(log);
  document.body.appendChild(panel);
  function put(line, color) {
    var d = el("div", color ? { color: color } : null, line);
    log.insertBefore(d, log.firstChild);
  }
  stop.addEventListener("click", function () { state.run = false; status.textContent = "stopping"; });
  reset.addEventListener("click", function () { state.done = {}; save(); put("checkpoint cleared"); });
  btn.addEventListener("click", async function () {
    if (state.run) return;
    state.run = true;
    var t = sel.value, g = GATES[t];
    var ids = ta.value.split(/\s+/).map(function (s) { return s.trim(); }).filter(Boolean);
    var ok = 0, skip = 0, fail = 0;
    for (var i = 0; i < ids.length; i++) {
      if (!state.run) break;
      var id = ids[i], mark = t + ":" + id;
      status.textContent = (i + 1) + "/" + ids.length + " ok " + ok + " skip " + skip + " fail " + fail;
      if (state.done[mark]) { skip++; continue; }
      try {
        await g.pre(id);
        if (!dry.checked) {
          await sleep(400);
          var input = {}; input[g.key] = id;
          await pcall(g.del, input);
          state.done[mark] = 1; save();
          put("DELETED " + id, "#46b89a"); ok++;
        } else { put("gate OK " + id, "#46b89a"); ok++; }
      } catch (e) {
        var msg = String(e.message || e);
        if (msg === "429") { put("429, backing off 20s", "#d9a441"); await sleep(20000); i--; continue; }
        put("SKIP " + id + " " + msg, "#d94f4f"); fail++;
      }
      await sleep(PACE);
    }
    state.run = false;
    status.textContent = "done: ok " + ok + " skip " + skip + " fail " + fail;
  });
})();
