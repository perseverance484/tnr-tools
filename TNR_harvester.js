/* TNR Harvester v1.0 (hosted body; loaded via @require loader)
 * Full-site read harvest via tRPC replay. Supersedes TNR Pulse (its collectors are included).
 * Contracts per 49_DATA_read_contracts.json + repo verification 2026-08-06.
 * Pace: >=1.15s/call (60/60s limiter). Resumable: completed collectors checkpoint to localStorage.
 * Each collector downloads its own JSON on completion. Run parked; do not navigate.
 * Excluded by design: private conversations, IP-bearing reads.
 */
(function () {
  "use strict";
  if (window.top !== window.self) return;
  if (window.__tnrHarvesterLoaded) return;
  window.__tnrHarvesterLoaded = true;

  var PACE_MS = 1150;
  var BACKOFF_MS = 20000;
  var MAX_RETRY = 3;
  var LS_KEY = "tnrHarvest_v1";
  var VOID_INPUT = { json: null, meta: { values: ["undefined"] } };

  var state = {
    running: false,
    stop: false,
    calls: 0,
    results: {}, // id -> payload (memory, for re-download)
    done: {}, // id -> {t, count} (persisted)
  };

  try {
    var saved = JSON.parse(localStorage.getItem(LS_KEY) || "{}");
    if (saved && saved.done) state.done = saved.done;
  } catch (e) { /* fresh */ }

  function persist() {
    try {
      localStorage.setItem(LS_KEY, JSON.stringify({ done: state.done }));
    } catch (e) { /* ignore quota */ }
  }

  function sleep(ms) {
    return new Promise(function (r) { setTimeout(r, ms); });
  }

  function buildUrl(proc, input) {
    var wrapped = { 0: input === undefined ? VOID_INPUT : { json: input } };
    return (
      "/api/trpc/" + proc + "?batch=1&input=" +
      encodeURIComponent(JSON.stringify(wrapped))
    );
  }

  async function call(proc, input) {
    var attempt = 0;
    for (;;) {
      attempt += 1;
      if (state.stop) throw new Error("stopped");
      var res;
      try {
        res = await fetch(buildUrl(proc, input), {
          method: "GET",
          credentials: "same-origin",
          headers: { accept: "application/json" },
        });
      } catch (e) {
        if (attempt >= MAX_RETRY) throw new Error(proc + ": network: " + e.message);
        await sleep(BACKOFF_MS);
        continue;
      }
      state.calls += 1;
      if (res.status === 429) {
        if (attempt >= MAX_RETRY) throw new Error(proc + ": rate limited");
        setStatus("429 on " + proc + ", backoff " + BACKOFF_MS / 1000 + "s");
        await sleep(BACKOFF_MS);
        continue;
      }
      var body;
      try {
        body = await res.json();
      } catch (e) {
        throw new Error(proc + ": bad JSON (http " + res.status + ")");
      }
      var item = Array.isArray(body) ? body[0] : body;
      if (item && item.error) {
        var msg = "";
        try {
          msg = item.error.json.message || JSON.stringify(item.error.json);
        } catch (e2) {
          msg = JSON.stringify(item.error).slice(0, 200);
        }
        if (msg.indexOf("TOO_MANY") >= 0 && attempt < MAX_RETRY) {
          await sleep(BACKOFF_MS);
          continue;
        }
        throw new Error(proc + ": " + msg.slice(0, 200));
      }
      if (item && item.result && item.result.data) {
        var d = item.result.data;
        return Object.prototype.hasOwnProperty.call(d, "json") ? d.json : d;
      }
      throw new Error(proc + ": unexpected shape (http " + res.status + ")");
    }
  }

  // Generic offset pager for {data, nextCursor} endpoints.
  async function paged(proc, baseInput, opts) {
    opts = opts || {};
    var rows = [];
    var cursor = null;
    var page = 0;
    var pageCap = opts.pageCap || 1000;
    for (;;) {
      if (state.stop) break;
      if (page >= pageCap) break;
      var input = {};
      for (var k in baseInput) input[k] = baseInput[k];
      input.cursor = cursor;
      var r = await call(proc, input);
      var batch = (r && (r.data || r.listings || r.threads)) || [];
      for (var i = 0; i < batch.length; i++) {
        rows.push(opts.map ? opts.map(batch[i]) : batch[i]);
      }
      page += 1;
      if (opts.progress) opts.progress(page, rows.length);
      if (!r || r.nextCursor === null || r.nextCursor === undefined) break;
      cursor = r.nextCursor;
      await sleep(PACE_MS);
    }
    return rows;
  }

  function stripUser(u) {
    var o = {};
    for (var k in u) {
      if (k === "avatar" || k === "avatar3d" || k === "avatarLight" ||
          k === "effects" || k === "lastIp") continue;
      o[k] = u[k];
    }
    if (u.village && u.village.name) o.villageName = u.village.name;
    delete o.village;
    return o;
  }

  /* ---------------- Collectors ---------------- */

  function pr(id) {
    return function (page, n) {
      setStatus(id + ": page " + page + ", " + n + " rows");
    };
  }

  var COLLECTORS = [
    // CONTENT
    { id: "jutsu", set: "content", label: "Jutsu catalog", run: async function () {
      return { rows: await paged("jutsu.getAll", { limit: 200 }, { progress: pr("jutsu") }) };
    } },
    { id: "items", set: "content", label: "Item catalog", run: async function () {
      return { rows: await paged("item.getAll", { limit: 200 }, { progress: pr("items") }) };
    } },
    { id: "quests", set: "content", label: "Quest catalog", run: async function () {
      return { rows: await paged("quests.getAll", { limit: 100 }, { progress: pr("quests") }) };
    } },
    { id: "ais", set: "content", label: "AI roster", run: async function () {
      return { rows: await paged("profile.getPublicUsers",
        { limit: 100, isAi: true, orderBy: "Strongest" },
        { progress: pr("ais"), map: stripUser }) };
    } },
    { id: "badges", set: "content", label: "Badges", run: async function () {
      return { rows: await paged("badge.getAll", { limit: 500 }, { progress: pr("badges") }) };
    } },
    { id: "bloodlines", set: "content", label: "Bloodlines", run: async function () {
      return { rows: await paged("bloodline.getAll", { limit: 200 }, { progress: pr("bloodlines") }) };
    } },
    { id: "skilltrees", set: "content", label: "Skill trees", run: async function () {
      return { rows: await paged("skillTree.getAll", { limit: 200 }, { progress: pr("skilltrees") }) };
    } },
    { id: "assets", set: "content", label: "Game assets", run: async function () {
      return { rows: await paged("gameAsset.getAll", { limit: 200 }, { progress: pr("assets") }) };
    } },
    // TELEMETRY (the pulse set)
    { id: "telemetry", set: "pulse", label: "Game telemetry", run: async function () {
      var seq = [
        ["online", "profile.countOnlineUsers", undefined],
        ["battleLengths", "data.getBattleLengthStatistics", { minCount: 1 }],
        ["queueLengths", "data.getQueueLengthStatistics", { minCount: 1 }],
        ["rankedDistribution", "data.getRankedRankDistributionStatistics", { minCount: 1 }],
        ["rankedLoadouts", "data.getRankedLoadoutStatistics", { minCount: 1, limit: 100 }],
        ["jutsuBalance_openWorld", "data.getJutsuBalanceStatistics", { battleTypes: ["COMBAT"], minCount: 3 }],
        ["jutsuBalance_ranked", "data.getJutsuBalanceStatistics", { battleTypes: ["RANKED_PVP", "RANKED_SPARRING"], minCount: 3 }],
        ["aiBalance", "data.getAiBalanceStatistics", { minCount: 3 }],
        ["rankedSeason", "pvpRank.getCurrentSeason", undefined],
        ["rankedTopPlayers", "pvpRank.getCurrentTopPlayers", undefined],
        ["activeWars", "war.getActiveWars", undefined],
      ];
      var t = {};
      for (var i = 0; i < seq.length; i++) {
        if (state.stop) break;
        setStatus("telemetry: " + seq[i][1] + " (" + (i + 1) + "/" + seq.length + ")");
        try {
          t[seq[i][0]] = await call(seq[i][1], seq[i][2]);
        } catch (e) {
          t[seq[i][0]] = { error: String(e.message || e) };
        }
        await sleep(PACE_MS);
      }
      return t;
    } },
    // POPULATION
    { id: "census", set: "pulse", label: "Player census", run: async function () {
      var cap = intVal(censusCapInput, 300);
      return { rows: await paged("profile.getPublicUsers",
        { limit: 100, isAi: false, orderBy: "Strongest" },
        { progress: pr("census"), map: stripUser, pageCap: cap }) };
    } },
    // ECONOMY
    { id: "auction", set: "economy", label: "Auction listings", run: async function () {
      return { rows: await paged("auction.getAuctionListings",
        { limit: 100, status: "ACTIVE" }, { progress: pr("auction"), pageCap: 30 }) };
    } },
    { id: "ryoOffers", set: "economy", label: "Black market ryo offers", run: async function () {
      return { rows: await paged("blackmarket.getRyoOffers",
        { limit: 100, activeToggle: true }, { progress: pr("ryoOffers"), pageCap: 20 }) };
    } },
    { id: "ryoGraph", set: "economy", label: "Ryo trade graph", run: async function () {
      return await call("blackmarket.getGraph", undefined);
    } },
    // WORLD
    { id: "villages", set: "world", label: "Villages", run: async function () {
      return { rows: await call("village.getAll", undefined) };
    } },
    { id: "alliances", set: "world", label: "Alliances", run: async function () {
      return await call("village.getAlliances", undefined);
    } },
    { id: "clans", set: "world", label: "Clan names", run: async function () {
      return { rows: await call("clan.getAllNames", undefined) };
    } },
    // SENTIMENT
    { id: "polls", set: "sentiment", label: "Polls", run: async function () {
      return { rows: await paged("poll.getPolls",
        { limit: 100, includeInactive: true }, { progress: pr("polls"), pageCap: 10 }) };
    } },
    { id: "forum", set: "sentiment", label: "Forum (capped)", run: async function () {
      var threadCap = intVal(threadCapInput, 20);
      var commentPages = intVal(commentPagesInput, 1);
      var boards = await call("forum.getAll", undefined);
      await sleep(PACE_MS);
      var out = { boards: boards, threads: [] };
      if (!Array.isArray(boards)) return out;
      for (var b = 0; b < boards.length; b++) {
        if (state.stop) break;
        var board = boards[b];
        var threads = [];
        try {
          threads = await paged("forum.getThreads",
            { boardId: board.id, limit: Math.min(threadCap, 100) },
            { pageCap: Math.ceil(threadCap / 100) || 1 });
        } catch (e) {
          out.threads.push({ boardId: board.id, error: String(e.message || e) });
          continue;
        }
        threads = threads.slice(0, threadCap);
        await sleep(PACE_MS);
        for (var t = 0; t < threads.length; t++) {
          if (state.stop) break;
          var th = threads[t];
          var thId = th.id || th.threadId;
          var entry = { boardId: board.id, boardName: board.name, thread: th, comments: [] };
          if (thId) {
            for (var p = 0; p < commentPages; p++) {
              if (state.stop) break;
              try {
                var r = await call("comments.getForumComments",
                  { thread_id: thId, cursor: p === 0 ? null : p, limit: 100 });
                var rows = (r && (r.comments || r.data)) || [];
                for (var c = 0; c < rows.length; c++) entry.comments.push(rows[c]);
                if (rows.length < 100) { await sleep(PACE_MS); break; }
              } catch (e) {
                entry.commentError = String(e.message || e);
                break;
              }
              await sleep(PACE_MS);
            }
          }
          out.threads.push(entry);
          setStatus("forum: " + board.name + " " + (t + 1) + "/" + threads.length);
        }
      }
      return out;
    } },
  ];

  var SETS = ["content", "pulse", "economy", "world", "sentiment"];

  /* ---------------- Runner ---------------- */

  function countOf(payload) {
    if (payload && Array.isArray(payload.rows)) return payload.rows.length;
    if (payload && Array.isArray(payload.threads)) return payload.threads.length;
    return 1;
  }

  function dl(name, obj) {
    var blob = new Blob([JSON.stringify(obj, null, 1)], { type: "application/json" });
    var url = URL.createObjectURL(blob);
    var a = document.createElement("a");
    a.href = url;
    a.download = name;
    document.body.appendChild(a);
    a.click();
    setTimeout(function () {
      URL.revokeObjectURL(url);
      if (a.parentNode) a.parentNode.removeChild(a);
    }, 2000);
  }

  function stamp() {
    return new Date().toISOString().replace(/[:]/g, "").slice(0, 13);
  }

  function finalize(col, payload) {
    var wrapped = {
      tool: "tnr-harvester",
      v: 1,
      collector: col.id,
      t: new Date().toISOString(),
      origin: location.origin,
      count: countOf(payload),
      payload: payload,
    };
    state.results[col.id] = wrapped;
    state.done[col.id] = { t: wrapped.t, count: wrapped.count };
    persist();
    if (autoDl.checked) dl("tnr_h1_" + col.id + "_" + stamp() + ".json", wrapped);
    updateRow(col.id, "done " + wrapped.count);
  }

  async function runSelected(force) {
    if (state.running) return;
    state.running = true;
    state.stop = false;
    state.calls = 0;
    setButtons(false);
    var started = Date.now();
    var ran = 0;
    try {
      for (var i = 0; i < COLLECTORS.length; i++) {
        if (state.stop) break;
        var col = COLLECTORS[i];
        if (!rowChecks[col.id].checked) continue;
        if (!force && state.done[col.id]) {
          updateRow(col.id, "skip (done " + state.done[col.id].count + ")");
          continue;
        }
        updateRow(col.id, "running...");
        try {
          var payload = await col.run();
          if (state.stop) { updateRow(col.id, "stopped"); break; }
          finalize(col, payload);
          ran += 1;
        } catch (e) {
          if (String(e.message) === "stopped") { updateRow(col.id, "stopped"); break; }
          updateRow(col.id, "ERR " + String(e.message || e).slice(0, 80));
        }
        await sleep(PACE_MS);
      }
      var mins = ((Date.now() - started) / 60000).toFixed(1);
      setStatus((state.stop ? "Stopped. " : "Done. ") + ran + " collectors, " +
        state.calls + " calls, " + mins + " min");
    } finally {
      state.running = false;
      state.stop = false;
      setButtons(true);
    }
  }

  /* ---------------- UI ---------------- */

  function el(tag, styles, text) {
    var e = document.createElement(tag);
    if (styles) for (var k in styles) e.style[k] = styles[k];
    if (text !== undefined) e.textContent = text;
    return e;
  }

  var panel = el("div", {
    position: "fixed", right: "8px", bottom: "8px", zIndex: "999999",
    background: "#111827", color: "#e5e7eb", border: "1px solid #4b5563",
    borderRadius: "8px", padding: "8px", font: "11px/1.4 monospace",
    width: "290px", maxHeight: "80vh", overflowY: "auto",
    boxShadow: "0 2px 10px rgba(0,0,0,0.6)",
  });

  panel.appendChild(el("div", { fontWeight: "bold", marginBottom: "2px" }, "TNR Harvester v1.0"));
  panel.appendChild(el("div", { color: "#9ca3af", marginBottom: "6px" },
    "Stay parked while it runs. Files download per collector."));

  var btnBar = el("div", { display: "flex", flexWrap: "wrap", gap: "3px", marginBottom: "6px" });
  panel.appendChild(btnBar);
  var actionButtons = [];
  function mkBtn(label, fn, keep, bg) {
    var b = el("button", {
      background: bg || "#2563eb", color: "#fff", border: "none",
      borderRadius: "4px", padding: "4px 6px", font: "11px monospace", cursor: "pointer",
    }, label);
    b.addEventListener("click", fn);
    if (!keep) actionButtons.push(b);
    btnBar.appendChild(b);
    return b;
  }

  function selectSet(setName) {
    for (var i = 0; i < COLLECTORS.length; i++) {
      var c = COLLECTORS[i];
      rowChecks[c.id].checked = setName === "all" ? true : c.set === setName;
    }
  }

  mkBtn("All", function () { selectSet("all"); });
  mkBtn("Content", function () { selectSet("content"); });
  mkBtn("Pulse", function () { selectSet("pulse"); });
  mkBtn("Econ", function () { selectSet("economy"); });
  mkBtn("World", function () { selectSet("world"); });
  mkBtn("Sentim", function () { selectSet("sentiment"); });

  var runBar = el("div", { display: "flex", flexWrap: "wrap", gap: "3px", marginBottom: "6px" });
  panel.appendChild(runBar);
  function mkRun(label, fn, keep, bg) {
    var b = el("button", {
      background: bg || "#16a34a", color: "#fff", border: "none",
      borderRadius: "4px", padding: "4px 6px", font: "11px monospace", cursor: "pointer",
    }, label);
    b.addEventListener("click", fn);
    if (!keep) actionButtons.push(b);
    runBar.appendChild(b);
    return b;
  }
  mkRun("Start", function () { runSelected(false); });
  mkRun("Force re-run", function () { runSelected(true); });
  mkRun("Stop", function () { state.stop = true; setStatus("Stopping..."); }, true, "#b91c1c");
  mkRun("Reset ckpt", function () {
    state.done = {}; persist();
    for (var i = 0; i < COLLECTORS.length; i++) updateRow(COLLECTORS[i].id, "");
    setStatus("Checkpoints cleared.");
  }, true, "#6b7280");
  mkRun("X", function () { if (panel.parentNode) panel.parentNode.removeChild(panel); }, true, "#6b7280");

  var optRow = el("div", { marginBottom: "6px", color: "#9ca3af" });
  function mkNum(label, val, width) {
    optRow.appendChild(el("span", {}, label));
    var inp = el("input", {
      width: width || "42px", background: "#1f2937", color: "#e5e7eb",
      border: "1px solid #4b5563", borderRadius: "3px", marginRight: "6px",
    });
    inp.type = "number"; inp.min = "1"; inp.value = String(val);
    optRow.appendChild(inp);
    return inp;
  }
  var censusCapInput = mkNum("census pgs:", 300);
  var threadCapInput = mkNum("thr/board:", 20);
  var commentPagesInput = mkNum("cmt pgs:", 1);
  var autoDl = el("input");
  autoDl.type = "checkbox"; autoDl.checked = true;
  optRow.appendChild(autoDl);
  optRow.appendChild(el("span", {}, " auto-DL"));
  panel.appendChild(optRow);

  function intVal(inp, dflt) {
    var v = parseInt(inp.value, 10);
    return v > 0 ? v : dflt;
  }

  var list = el("div", { borderTop: "1px solid #374151", paddingTop: "4px" });
  panel.appendChild(list);
  var rowChecks = {};
  var rowStatus = {};
  COLLECTORS.forEach(function (c) {
    var row = el("div", { display: "flex", alignItems: "center", gap: "4px", marginBottom: "2px" });
    var cb = el("input");
    cb.type = "checkbox"; cb.checked = true;
    rowChecks[c.id] = cb;
    row.appendChild(cb);
    row.appendChild(el("span", { minWidth: "108px" }, c.label));
    var st = el("span", { color: "#9ca3af", flex: "1" },
      state.done[c.id] ? "done " + state.done[c.id].count : "");
    rowStatus[c.id] = st;
    row.appendChild(st);
    var dlb = el("button", {
      background: "#374151", color: "#e5e7eb", border: "none",
      borderRadius: "3px", padding: "1px 5px", font: "10px monospace", cursor: "pointer",
    }, "DL");
    dlb.addEventListener("click", function () {
      if (state.results[c.id]) {
        dl("tnr_h1_" + c.id + "_" + stamp() + ".json", state.results[c.id]);
      } else {
        setStatus(c.id + ": no data in this session (re-run to download).");
      }
    });
    row.appendChild(dlb);
    list.appendChild(row);
  });

  function updateRow(id, msg) {
    if (rowStatus[id]) rowStatus[id].textContent = msg;
  }

  var status = el("div", {
    marginTop: "6px", minHeight: "14px", wordBreak: "break-word",
    borderTop: "1px solid #374151", paddingTop: "4px",
  }, "Ready. " + (Object.keys(state.done).length ? Object.keys(state.done).length + " collectors checkpointed." : ""));
  panel.appendChild(status);
  function setStatus(msg) { status.textContent = msg; }

  function setButtons(on) {
    for (var i = 0; i < actionButtons.length; i++) {
      actionButtons[i].disabled = !on;
      actionButtons[i].style.opacity = on ? "1" : "0.5";
    }
  }

  function attach() {
    if (document.body) document.body.appendChild(panel);
    else setTimeout(attach, 500);
  }
  attach();
})();
