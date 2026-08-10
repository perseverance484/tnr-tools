/* TNR Harvester v1.2 (hosted body; loaded via @require loader)
 * v1.2: + battlelogs collector; restores the v1.1 additions: history set (content change
 * log, war kill stats, raid leaderboards, meta windows), deep set (AI full kits),
 * craftables + bank flow in economy, item/BL/skilltree balance stats in pulse.
 * Deep is excluded from the All preset (slow); run it on demand.
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
    // PULSE addition (restored v1.1)
    { id: "balanceStats", set: "pulse", label: "Item/BL/skilltree balance", run: async function () {
      var seq = [
        ["itemBalance", "data.getItemBalanceStatistics", { minCount: 3 }],
        ["bloodlineBalance", "data.getBloodlineBalanceStatistics", { minCount: 3 }],
        ["skillTreeBalance", "data.getSkillTreeBalanceStatistics", { minCount: 3 }],
      ];
      var t = {};
      for (var i = 0; i < seq.length; i++) {
        if (state.stop) break;
        setStatus("balanceStats: " + seq[i][1] + " (" + (i + 1) + "/" + seq.length + ")");
        try {
          t[seq[i][0]] = await call(seq[i][1], seq[i][2]);
        } catch (e) {
          t[seq[i][0]] = { error: String(e.message || e) };
        }
        await sleep(PACE_MS);
      }
      return t;
    } },
    // ECONOMY additions (restored v1.1)
    { id: "craftables", set: "economy", label: "Craftable items (one call)", run: async function () {
      var r = await call("occupation.getCraftableItems", undefined);
      return Array.isArray(r) ? { rows: r } : r;
    } },
    { id: "bankFlow", set: "economy", label: "Bank transfer graph", run: async function () {
      // Input shape reconstructed: void first (blackmarket.getGraph pattern), {days:90} fallback.
      try {
        var g = await call("bank.getGraph", undefined);
        return Array.isArray(g) ? { rows: g } : { graph: g };
      } catch (e) {
        await sleep(PACE_MS);
        var g2 = await call("bank.getGraph", { days: 90 });
        return { graph: g2, input: { days: 90 },
          note: "void input rejected: " + String(e.message || e).slice(0, 120) };
      }
    } },
    // HISTORY set (restored v1.1)
    { id: "contentChanges", set: "history", label: "Content change log", run: async function () {
      // LOG_TYPES (45b) minus user/userjutsu/battleAction: player logs excluded by design.
      // Cap: 100/page x 30 pages = 3000 recent entries per logtype.
      var types = ["ai", "badge", "bloodline", "clan", "item", "jutsu", "poll", "war"];
      var out = {};
      for (var i = 0; i < types.length; i++) {
        if (state.stop) break;
        setStatus("contentChanges: " + types[i] + " (" + (i + 1) + "/" + types.length + ")");
        try {
          out[types[i]] = await paged("logs.getContentChanges",
            { logtype: types[i], limit: 100 },
            { pageCap: 30, progress: pr("log:" + types[i]) });
        } catch (e) {
          out[types[i]] = { error: String(e.message || e) };
        }
        await sleep(PACE_MS);
      }
      return out;
    } },
    { id: "warStats", set: "history", label: "War kill stats (<=25 wars)", run: async function () {
      var villages = [];
      if (state.results.villages && state.results.villages.payload &&
          Array.isArray(state.results.villages.payload.rows)) {
        villages = state.results.villages.payload.rows;
      } else {
        villages = (await call("village.getAll", undefined)) || [];
        await sleep(PACE_MS);
      }
      var seenWar = {};
      var wars = [];
      for (var v = 0; v < villages.length; v++) {
        if (state.stop) break;
        setStatus("warStats: village " + (v + 1) + "/" + villages.length);
        try {
          var ended = await call("war.getEndedWars", { villageId: villages[v].id });
          if (Array.isArray(ended)) {
            for (var w = 0; w < ended.length; w++) {
              if (ended[w] && ended[w].id && !seenWar[ended[w].id]) {
                seenWar[ended[w].id] = true;
                wars.push(ended[w]);
              }
            }
          }
        } catch (e) {
          wars.push({ villageId: villages[v].id, error: String(e.message || e) });
        }
        await sleep(PACE_MS);
      }
      wars = wars.slice(0, 25);
      var out = [];
      for (var k = 0; k < wars.length; k++) {
        if (state.stop) break;
        if (!wars[k].id) { out.push(wars[k]); continue; }
        setStatus("warStats: kills " + (k + 1) + "/" + wars.length);
        try {
          var stats = await call("war.getWarKillStats", { warId: wars[k].id });
          out.push({ war: wars[k], kills: stats });
        } catch (e) {
          out.push({ war: wars[k], error: String(e.message || e) });
        }
        await sleep(PACE_MS);
      }
      return { rows: out };
    } },
    { id: "raidBoard", set: "history", label: "Raid leaderboards", run: async function () {
      var out = { completed: null, boards: [] };
      try {
        out.completed = await call("raids.getCompletedRaids", undefined);
      } catch (e) {
        out.completed = { error: String(e.message || e) };
      }
      await sleep(PACE_MS);
      var quests = [];
      if (state.results.quests && state.results.quests.payload &&
          Array.isArray(state.results.quests.payload.rows)) {
        quests = state.results.quests.payload.rows;
      } else {
        try {
          quests = await paged("quests.getAll", { limit: 100 },
            { pageCap: 30, progress: pr("raidBoard:quests") });
        } catch (e) { quests = []; }
      }
      var raids = [];
      for (var i = 0; i < quests.length; i++) {
        if (quests[i] && quests[i].questType === "raid") raids.push(quests[i]);
      }
      for (var r = 0; r < raids.length; r++) {
        if (state.stop) break;
        setStatus("raidBoard: " + (r + 1) + "/" + raids.length + " " + raids[r].name);
        try {
          var lb = await call("raids.getRaidLeaderboard", { questId: raids[r].id });
          out.boards.push({ questId: raids[r].id, name: raids[r].name, leaderboard: lb });
        } catch (e) {
          out.boards.push({ questId: raids[r].id, name: raids[r].name,
            error: String(e.message || e) });
        }
        await sleep(PACE_MS);
      }
      return out;
    } },
    { id: "metaWindows", set: "history", label: "Meta windows (top-20 jutsu)", run: async function () {
      // Seed: open-world jutsu balance -> top 20 by summed count; then
      // data.getStatistics per jutsu over last 30d and the 30d before.
      var top = [];
      try {
        var stats = await call("data.getJutsuBalanceStatistics",
          { battleTypes: ["COMBAT"], minCount: 3 });
        var byId = {};
        if (Array.isArray(stats)) {
          for (var i = 0; i < stats.length; i++) {
            var row = stats[i];
            if (!row || !row.jutsuId) continue;
            if (!byId[row.jutsuId]) {
              byId[row.jutsuId] = { jutsuId: row.jutsuId, name: row.name, count: 0 };
            }
            byId[row.jutsuId].count += row.count || 0;
          }
        }
        for (var k in byId) top.push(byId[k]);
        top.sort(function (a, b) { return b.count - a.count; });
        top = top.slice(0, 20);
      } catch (e) {
        return { error: "seed failed: " + String(e.message || e) };
      }
      await sleep(PACE_MS);
      var d30 = 30 * 86400000;
      var now = Date.now();
      var winA = { startDate: new Date(now - d30).toISOString(),
                   endDate: new Date(now).toISOString() };
      var winB = { startDate: new Date(now - 2 * d30).toISOString(),
                   endDate: new Date(now - d30).toISOString() };
      var out = [];
      for (var j = 0; j < top.length; j++) {
        if (state.stop) break;
        setStatus("metaWindows: " + (j + 1) + "/" + top.length + " " + top[j].name);
        var entry = { jutsuId: top[j].jutsuId, name: top[j].name,
                      openWorldCount: top[j].count };
        try {
          entry.last30 = await call("data.getStatistics",
            { id: top[j].jutsuId, type: "jutsu", battleType: "COMBAT",
              startDate: winA.startDate, endDate: winA.endDate });
        } catch (e) { entry.last30 = { error: String(e.message || e) }; }
        await sleep(PACE_MS);
        if (state.stop) { out.push(entry); break; }
        try {
          entry.prior30 = await call("data.getStatistics",
            { id: top[j].jutsuId, type: "jutsu", battleType: "COMBAT",
              startDate: winB.startDate, endDate: winB.endDate });
        } catch (e) { entry.prior30 = { error: String(e.message || e) }; }
        await sleep(PACE_MS);
        out.push(entry);
      }
      return { rows: out, windows: { last30: winA, prior30: winB } };
    } },
    // DEEP set (restored v1.1, verbatim from the v1.1 build session)
    { id: "aiDeep", set: "deep", label: "AI full kits (slow ~12min)", run: async function () {
      var list = [];
      if (state.results.ais) list = state.results.ais.payload.rows || [];
      else {
        list = await paged("profile.getPublicUsers",
          { limit: 100, isAi: true, orderBy: "Strongest" }, { map: stripUser, progress: pr("aiDeep:list") });
      }
      var out = [];
      for (var i = 0; i < list.length; i++) {
        if (state.stop) break;
        setStatus("aiDeep: " + (i + 1) + "/" + list.length);
        try {
          var ai = await call("profile.getAi", { userId: list[i].userId });
          if (ai) {
            delete ai.avatar; delete ai.avatar3d; delete ai.avatarLight;
            out.push(ai);
          }
        } catch (e) { out.push({ userId: list[i].userId, error: String(e.message || e) }); }
        await sleep(PACE_MS);
      }
      return { rows: out };
    } },
    // HISTORY set (v1.2)
    { id: "battlelogs", set: "history", label: "Battle logs (bulk, 7d window)", run: async function () {
      // combat.getBattleHistory {secondsBack} -> [historyRow]; attackedId = ATTACKER userId (capture-verified).
      // combat.getBattleEntries {battleId, refreshKey:0, checkBattle:false, limit:1000} -> full log.
      // Seen-set tnr_bl_seen shared with the standalone battlelogs bundle. Pulls ALL battle types.
      var SEEN_KEY = "tnr_bl_seen";
      var seen;
      try { seen = new Set(JSON.parse(localStorage.getItem(SEEN_KEY) || "[]")); }
      catch (e) { seen = new Set(); }
      var windows = [31536000, 2592000, 604800, 86400, 10800];
      var hist = null, used = 0;
      for (var w = 0; w < windows.length; w++) {
        try {
          var res = await call("combat.getBattleHistory", { secondsBack: windows[w] });
          if (Array.isArray(res)) { hist = res; used = windows[w]; break; }
        } catch (e) {
          if (String(e.message).indexOf("stopped") >= 0) throw e;
          setStatus("battlelogs: window " + windows[w] + "s failed, stepping down");
        }
        await sleep(PACE_MS);
      }
      if (!hist) throw new Error("battlelogs: history unavailable at all windows");
      var oldest = null;
      for (var h = 0; h < hist.length; h++) {
        if (!oldest || hist[h].createdAt < oldest) oldest = hist[h].createdAt;
      }
      var todo = [];
      for (var i = 0; i < hist.length; i++) {
        if (!seen.has(hist[i].battleId)) todo.push(hist[i]);
      }
      setStatus("battlelogs: " + todo.length + " new of " + hist.length +
        " rows, window " + used + "s, oldest " + (oldest || "?"));
      var out = [];
      for (var j = 0; j < todo.length; j++) {
        if (state.stop) break;
        var row = todo[j];
        await sleep(PACE_MS);
        try {
          var entries = await call("combat.getBattleEntries",
            { battleId: row.battleId, refreshKey: 0, checkBattle: false, limit: 1000 });
          out.push({ meta: row, entries: Array.isArray(entries) ? entries : [] });
          seen.add(row.battleId);
          var arr = Array.from(seen);
          if (arr.length > 4000) arr = arr.slice(arr.length - 4000);
          localStorage.setItem(SEEN_KEY, JSON.stringify(arr));
          setStatus("battlelogs: " + (j + 1) + "/" + todo.length + " " + row.battleId);
        } catch (e) {
          if (String(e.message).indexOf("stopped") >= 0) break;
          out.push({ meta: row, error: String(e.message || e) });
        }
      }
      return { rows: out, windowSeconds: used, seenSkipped: hist.length - todo.length };
    } },
  ];

  var SETS = ["content", "pulse", "economy", "world", "sentiment", "history", "deep"];

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

  panel.appendChild(el("div", { fontWeight: "bold", marginBottom: "2px" }, "TNR Harvester v1.2"));
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
      rowChecks[c.id].checked = setName === "all" ? c.set !== "deep" : c.set === setName;
    }
  }

  mkBtn("All", function () { selectSet("all"); });
  mkBtn("Content", function () { selectSet("content"); });
  mkBtn("Pulse", function () { selectSet("pulse"); });
  mkBtn("Econ", function () { selectSet("economy"); });
  mkBtn("World", function () { selectSet("world"); });
  mkBtn("Sentim", function () { selectSet("sentiment"); });
  mkBtn("Hist", function () { selectSet("history"); });
  mkBtn("Deep", function () { selectSet("deep"); });

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
