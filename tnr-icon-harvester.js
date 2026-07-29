// TNR Icon Harvester (hosted logic) v1.0
// Loaded via @require from the tnr-tools repo. Grants and @connect live in the loader.
// API footprint: exactly ONE tRPC call (jutsu.getAllNames). All image pulls hit the
// utfs/uploadthing CDN, sequential, throttled, with exponential backoff. The TNR
// rolling cumulative limiter is never touched beyond that single call.

(function () {
  'use strict';
  if (window.top !== window.self) return;
  if (window.__tnrIconHarvester) return;
  window.__tnrIconHarvester = true;

  var DEFAULT_DELAY_MS = 450;      // gap between CDN fetches
  var BATCH_SIZE = 100;            // icons per zip
  var SAMPLE_TARGET = 200;         // approx icons in sample mode
  var LEDGER_KEY = 'ihv_done_urls_v1';

  var state = {
    running: false,
    paused: false,
    entries: [],        // unique [{url, id, name, dupIds:[]}]
    idx: 0,
    batch: [],          // [{fname, buf, meta}]
    batchNo: 0,
    ok: 0, skipped: 0, failed: 0,
    failures: [],
    doneSet: {}
  };

  // ---------- persisted ledger ----------
  function loadLedger() {
    try {
      var raw = (typeof GM_getValue === 'function') ? GM_getValue(LEDGER_KEY, '[]') : '[]';
      var arr = JSON.parse(raw);
      var m = {};
      for (var i = 0; i < arr.length; i++) m[arr[i]] = 1;
      return m;
    } catch (e) { return {}; }
  }
  function saveLedger() {
    if (typeof GM_setValue !== 'function') return;
    GM_setValue(LEDGER_KEY, JSON.stringify(Object.keys(state.doneSet)));
  }

  // ---------- UI (createElement + CSSOM only) ----------
  function el(tag, styles, text) {
    var n = document.createElement(tag);
    if (styles) for (var k in styles) n.style[k] = styles[k];
    if (text) n.textContent = text;
    return n;
  }
  var panel = el('div', {
    position: 'fixed', right: '8px', bottom: '8px', zIndex: '99999',
    background: '#111827', color: '#e5e7eb', padding: '10px',
    borderRadius: '10px', font: '12px sans-serif', width: '230px',
    boxShadow: '0 2px 10px rgba(0,0,0,.6)'
  });
  var title = el('div', { fontWeight: 'bold', marginBottom: '6px' }, 'TNR Icon Harvester v1.0');
  var status = el('div', { whiteSpace: 'pre-line', marginBottom: '6px' }, 'idle');
  var rowOpts = el('div', { marginBottom: '6px' });
  var delayLbl = el('label', { display: 'block', marginBottom: '4px' }, 'Delay ms: ');
  var delayIn = el('input', { width: '60px' });
  delayIn.type = 'number'; delayIn.min = '250'; delayIn.value = String(DEFAULT_DELAY_MS);
  delayLbl.appendChild(delayIn);
  var sampleLbl = el('label', { display: 'block' }, 'Sample mode (~' + SAMPLE_TARGET + '): ');
  var sampleCk = el('input', {});
  sampleCk.type = 'checkbox';
  sampleLbl.appendChild(sampleCk);
  rowOpts.appendChild(delayLbl); rowOpts.appendChild(sampleLbl);

  function btn(label) {
    var b = el('button', {
      margin: '2px', padding: '4px 8px', border: '0', borderRadius: '6px',
      background: '#374151', color: '#e5e7eb', cursor: 'pointer'
    }, label);
    return b;
  }
  var bStart = btn('Harvest'), bPause = btn('Pause'), bResume = btn('Resume'), bReset = btn('Reset progress');
  var rowBtns = el('div', {});
  rowBtns.appendChild(bStart); rowBtns.appendChild(bPause); rowBtns.appendChild(bResume); rowBtns.appendChild(bReset);
  panel.appendChild(title); panel.appendChild(status); panel.appendChild(rowOpts); panel.appendChild(rowBtns);
  document.body.appendChild(panel);

  function say(t) { status.textContent = t; }

  // ---------- source list: the single API call ----------
  function fetchAllNames() {
    var input = encodeURIComponent(JSON.stringify({ 0: { json: null, meta: { values: ['undefined'], v: 1 } } }));
    var url = '/api/trpc/jutsu.getAllNames?batch=1&input=' + input;
    return fetch(url, { credentials: 'same-origin' })
      .then(function (r) { return r.json(); })
      .then(function (j) {
        var block = Array.isArray(j) ? j[0] : j;
        return block.result.data.json;
      });
  }

  function buildEntries(list) {
    var byUrl = {};
    var order = [];
    var skippedDefault = 0;
    for (var i = 0; i < list.length; i++) {
      var it = list[i];
      var u = it.image || '';
      if (!u) { skippedDefault++; continue; }
      if (u.indexOf('default.webp') !== -1) { skippedDefault++; continue; }
      if (byUrl[u]) { byUrl[u].dupIds.push(it.id); continue; }
      byUrl[u] = { url: u, id: it.id, name: it.name, dupIds: [] };
      order.push(byUrl[u]);
    }
    order.sort(function (a, b) { return a.name < b.name ? -1 : 1; });
    if (sampleCk.checked && order.length > SAMPLE_TARGET) {
      var step = Math.ceil(order.length / SAMPLE_TARGET);
      var sampled = [];
      for (var s = 0; s < order.length; s += step) sampled.push(order[s]);
      order = sampled;
    }
    return { entries: order, skippedDefault: skippedDefault, total: list.length };
  }

  // ---------- CDN fetch with backoff ----------
  function gmGet(url, tryNo) {
    return new Promise(function (resolve, reject) {
      GM_xmlhttpRequest({
        method: 'GET', url: url, responseType: 'arraybuffer', timeout: 30000,
        onload: function (r) {
          if (r.status >= 200 && r.status < 300 && r.response && r.response.byteLength > 0) resolve(r.response);
          else reject(new Error('status ' + r.status));
        },
        onerror: function () { reject(new Error('network')); },
        ontimeout: function () { reject(new Error('timeout')); }
      });
    }).catch(function (err) {
      if (tryNo >= 3) throw err;
      var wait = Math.pow(2, tryNo) * 2000 + Math.random() * 500;
      return sleep(wait).then(function () { return gmGet(url, tryNo + 1); });
    });
  }
  function sleep(ms) { return new Promise(function (res) { setTimeout(res, ms); }); }

  function sniffExt(buf) {
    var b = new Uint8Array(buf.slice(0, 16));
    if (b[0] === 0x89 && b[1] === 0x50) return '.png';
    if (b[0] === 0xFF && b[1] === 0xD8) return '.jpg';
    if (b[0] === 0x47 && b[1] === 0x49 && b[2] === 0x46) return '.gif';
    if (b[0] === 0x52 && b[1] === 0x49 && b[2] === 0x46 && b[3] === 0x46 &&
        b[8] === 0x57 && b[9] === 0x45 && b[10] === 0x42 && b[11] === 0x50) return '.webp';
    if (b[4] === 0x66 && b[5] === 0x74 && b[6] === 0x79 && b[7] === 0x70) return '.avif';
    return '.png';
  }

  // ---------- zip + download ----------
  function flushBatch(final) {
    if (state.batch.length === 0) return Promise.resolve();
    state.batchNo++;
    var no = (state.batchNo < 10 ? '0' : '') + state.batchNo;
    var zip = new JSZip();
    var manifest = [];
    for (var i = 0; i < state.batch.length; i++) {
      var it = state.batch[i];
      zip.file(it.fname, it.buf);
      manifest.push(it.meta);
    }
    zip.file('manifest.json', JSON.stringify(manifest, null, 1));
    if (final && state.failures.length) zip.file('failures.json', JSON.stringify(state.failures, null, 1));
    state.batch = [];
    return zip.generateAsync({ type: 'blob', compression: 'STORE' }).then(function (blob) {
      var a = document.createElement('a');
      var u = URL.createObjectURL(blob);
      a.href = u; a.download = 'tnr_icons_b' + no + '.zip';
      document.body.appendChild(a); a.click();
      setTimeout(function () { URL.revokeObjectURL(u); a.remove(); }, 4000);
      saveLedger();
      return sleep(1200);
    });
  }

  // ---------- main loop ----------
  function loop() {
    if (!state.running) return;
    if (state.paused) { setTimeout(loop, 500); return; }
    if (state.idx >= state.entries.length) {
      state.running = false;
      flushBatch(true).then(function () {
        say('DONE. ok ' + state.ok + ', already had ' + state.skipped + ', failed ' + state.failed +
            '\nzips: ' + state.batchNo + '. Upload them to Claude.');
      });
      return;
    }
    var e = state.entries[state.idx];
    state.idx++;
    if (state.doneSet[e.url]) {
      state.skipped++;
      setTimeout(loop, 15);
      return;
    }
    gmGet(e.url, 0).then(function (buf) {
      var ext = sniffExt(buf);
      var fname = e.id + ext;
      state.batch.push({ fname: fname, buf: buf, meta: { file: fname, id: e.id, name: e.name, url: e.url, bytes: buf.byteLength, dup_ids: e.dupIds } });
      state.doneSet[e.url] = 1;
      state.ok++;
      say('pulling ' + state.idx + '/' + state.entries.length + '\nok ' + state.ok + ' fail ' + state.failed + ' zip#' + (state.batchNo + 1));
      var next = (state.batch.length >= BATCH_SIZE) ? flushBatch(false) : Promise.resolve();
      return next;
    }).catch(function (err) {
      state.failed++;
      state.failures.push({ id: e.id, name: e.name, url: e.url, error: String(err && err.message || err) });
    }).then(function () {
      var d = Math.max(250, parseInt(delayIn.value, 10) || DEFAULT_DELAY_MS);
      setTimeout(loop, d);
    });
  }

  bStart.addEventListener('click', function () {
    if (state.running) return;
    say('fetching jutsu.getAllNames (single API call)...');
    state.doneSet = loadLedger();
    fetchAllNames().then(function (list) {
      var built = buildEntries(list);
      state.entries = built.entries;
      state.idx = 0; state.ok = 0; state.skipped = 0; state.failed = 0;
      state.failures = []; state.batch = []; state.batchNo = 0;
      state.running = true; state.paused = false;
      say('catalog ' + built.total + ', unique art ' + built.entries.length +
          ', no-art/default ' + built.skippedDefault + '\nstarting...');
      loop();
    }).catch(function (err) {
      say('getAllNames failed: ' + String(err && err.message || err));
    });
  });
  bPause.addEventListener('click', function () { if (state.running) { state.paused = true; say('paused at ' + state.idx + '/' + state.entries.length); } });
  bResume.addEventListener('click', function () { if (state.running && state.paused) { state.paused = false; say('resuming'); } });
  bReset.addEventListener('click', function () {
    state.doneSet = {};
    if (typeof GM_deleteValue === 'function') GM_deleteValue(LEDGER_KEY);
    say('progress ledger cleared');
  });
})();
