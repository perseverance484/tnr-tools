/* TNR Capture v1.0  (hosted bundle, loaded via document-start @require loader)
   Hooks fetch + XHR, logs every matching request/response, persists across reloads,
   one-tap download of the whole log as JSON. Mobile-safe: createElement + shadow DOM,
   no innerHTML. Default filter "/api/" captures all tRPC traffic; clear it to grab all. */
(function () {
  if (window.__tnrCap) return;
  window.__tnrCap = true;

  var KEY = 'tnr_capture_log_v1';
  var FKEY = 'tnr_capture_filter_v1';
  var REC = true;
  var FILTER = '';
  try { FILTER = localStorage.getItem(FKEY); } catch (e) {}
  if (FILTER === null || FILTER === undefined) FILTER = '/api/';

  var LOG = [];
  try { LOG = JSON.parse(localStorage.getItem(KEY) || '[]') || []; } catch (e) { LOG = []; }
  var SEQ = LOG.length ? (LOG[LOG.length - 1].n || LOG.length) : 0;

  function trpcProc(url) {
    var i = url.indexOf('/api/trpc/');
    if (i < 0) return '';
    var rest = url.slice(i + 10);
    var q = rest.indexOf('?');
    if (q >= 0) rest = rest.slice(0, q);
    return decodeURIComponent(rest);
  }
  function want(url) { return REC && url && url.indexOf(FILTER) >= 0; }

  function persist() {
    try { localStorage.setItem(KEY, JSON.stringify(LOG)); return; }
    catch (e) {
      while (LOG.length > 10) {
        LOG.splice(0, Math.max(20, Math.floor(LOG.length * 0.2)));
        try { localStorage.setItem(KEY, JSON.stringify(LOG)); return; } catch (e2) {}
      }
    }
  }
  function record(rec) {
    rec.n = ++SEQ;
    LOG.push(rec);
    persist();
    uiAdd(rec);
    uiCount();
  }

  /* ---- fetch hook ---- */
  var oFetch = window.fetch;
  if (oFetch) {
    window.fetch = function (input, init) {
      var url = '', method = 'GET', reqBody = '';
      try {
        url = (typeof input === 'string') ? input : (input && input.url) || '';
        method = (init && init.method) || (input && typeof input === 'object' && input.method) || 'GET';
        var b = init && init.body;
        if (typeof b === 'string') reqBody = b;
        else if (b) reqBody = '[' + ((b.constructor && b.constructor.name) || 'body') + ']';
      } catch (e) {}
      var t0 = Date.now();
      var p = oFetch.apply(this, arguments);
      try {
        if (want(url)) {
          p.then(function (res) {
            try {
              var ct = '';
              try { ct = res.headers.get('content-type') || ''; } catch (e) {}
              var st = res.status;
              if (/json|text|javascript|xml|html/.test(ct) || ct === '') {
                res.clone().text().then(function (txt) {
                  record({ t: t0, ms: Date.now() - t0, method: method, status: st, ct: ct, proc: trpcProc(url), url: url, req: reqBody, res: txt });
                }, function () {
                  record({ t: t0, ms: Date.now() - t0, method: method, status: st, ct: ct, proc: trpcProc(url), url: url, req: reqBody, res: '[read error]' });
                });
              } else {
                record({ t: t0, ms: Date.now() - t0, method: method, status: st, ct: ct, proc: trpcProc(url), url: url, req: reqBody, res: '[binary ' + ct + ']' });
              }
            } catch (e) {}
          }, function () {});
        }
      } catch (e) {}
      return p;
    };
  }

  /* ---- XHR hook ---- */
  try {
    var oOpen = XMLHttpRequest.prototype.open;
    var oSend = XMLHttpRequest.prototype.send;
    XMLHttpRequest.prototype.open = function (m, u) {
      try { this.__cap = { m: m, u: u, t: Date.now() }; } catch (e) {}
      return oOpen.apply(this, arguments);
    };
    XMLHttpRequest.prototype.send = function (body) {
      try {
        var c = this.__cap;
        if (c && want(c.u)) {
          var self = this;
          c.req = (typeof body === 'string') ? body : (body ? '[body]' : '');
          this.addEventListener('loadend', function () {
            try {
              var txt = '';
              try { txt = self.responseText; } catch (e) { txt = '[binary]'; }
              var ct = '';
              try { ct = self.getResponseHeader('content-type') || ''; } catch (e) {}
              record({ t: c.t, ms: Date.now() - c.t, method: c.m, status: self.status, ct: ct, proc: trpcProc(c.u), url: c.u, req: c.req, res: txt });
            } catch (e) {}
          });
        }
      } catch (e) {}
      return oSend.apply(this, arguments);
    };
  } catch (e) {}

  /* ---- UI ---- */
  var host, root, panel, listEl, countEl, statusEl, dotEl, badgeCount;

  var CSS =
    '.badge{font:bold 12px system-ui,Arial,sans-serif;background:#111;color:#0f0;border:1px solid #0a0;border-radius:6px;padding:5px 9px;cursor:pointer;display:flex;align-items:center;gap:6px;box-shadow:0 2px 8px rgba(0,0,0,.5)}' +
    '.dot{width:8px;height:8px;border-radius:50%;background:#0f0;flex:0 0 auto}' +
    '.dot.off{background:#888}' +
    '.panel{display:none;width:300px;max-width:88vw;max-height:70vh;background:#0d0d0d;color:#eee;border:1px solid #333;border-radius:8px;margin-top:6px;font:12px system-ui,Arial,sans-serif;overflow:hidden;flex-direction:column;box-shadow:0 4px 16px rgba(0,0,0,.6)}' +
    '.panel.open{display:flex}' +
    '.hd{display:flex;align-items:center;justify-content:space-between;padding:8px;border-bottom:1px solid #222;font-weight:bold}' +
    '.hd b{color:#0f0}' +
    '.x{background:#1a1a1a;color:#ccc;border:1px solid #444;border-radius:4px;padding:2px 8px;cursor:pointer}' +
    '.row{display:flex;gap:6px;padding:8px;border-bottom:1px solid #1a1a1a;align-items:center}' +
    '.row input{flex:1;min-width:0;background:#000;color:#0f0;border:1px solid #333;border-radius:4px;padding:6px;font:12px monospace}' +
    'button.b{flex:1;background:#1a1a1a;color:#eee;border:1px solid #444;border-radius:4px;padding:7px 6px;font:12px system-ui;cursor:pointer}' +
    'button.b:active{background:#333}' +
    '.dl{background:#063b2b;border-color:#0a6;color:#cff}' +
    '.clr{background:#3b0606;border-color:#a33;color:#fcc}' +
    '.st{padding:6px 8px;color:#9af;border-bottom:1px solid #1a1a1a}' +
    '.list{overflow:auto;flex:1 1 auto;font:11px monospace;-webkit-overflow-scrolling:touch}' +
    '.it{padding:4px 8px;border-bottom:1px solid #151515;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}' +
    '.it .m{color:#88f}.it .s2{color:#0f0}.it .s4{color:#fa0}.it .s5{color:#f55}.it .s0{color:#888}';

  function el(tag, cls, txt) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (txt != null) n.textContent = txt;
    return n;
  }

  function uiBuild() {
    if (host || !document.body) return;
    host = el('div');
    host.id = 'tnr-cap-host';
    host.style.position = 'fixed';
    host.style.zIndex = '2147483647';
    host.style.bottom = '12px';
    host.style.right = '12px';
    host.style.display = 'flex';
    host.style.flexDirection = 'column';
    host.style.alignItems = 'flex-end';
    document.body.appendChild(host);
    root = host.attachShadow({ mode: 'open' });
    var style = document.createElement('style');
    style.textContent = CSS;
    root.appendChild(style);

    var badge = el('div', 'badge');
    dotEl = el('div', 'dot');
    badge.appendChild(dotEl);
    var bt = el('span', null, 'CAP');
    badge.appendChild(bt);
    badgeCount = el('span', null, String(LOG.length));
    badge.appendChild(badgeCount);
    badge.addEventListener('click', function () { panel.classList.toggle('open'); });
    root.appendChild(badge);

    panel = el('div', 'panel');

    var hd = el('div', 'hd');
    var title = el('b', null, 'TNR Capture');
    hd.appendChild(title);
    var close = el('button', 'x', 'hide');
    close.addEventListener('click', function () { panel.classList.remove('open'); });
    hd.appendChild(close);
    panel.appendChild(hd);

    var frow = el('div', 'row');
    var lbl = el('span', null, 'url contains');
    lbl.style.color = '#888';
    frow.appendChild(lbl);
    var fin = el('input');
    fin.value = FILTER;
    fin.placeholder = 'leave blank = all';
    fin.addEventListener('change', function () {
      FILTER = fin.value;
      try { localStorage.setItem(FKEY, FILTER); } catch (e) {}
      uiStatus();
    });
    frow.appendChild(fin);
    panel.appendChild(frow);

    var brow = el('div', 'row');
    var dl = el('button', 'b dl', 'Download');
    dl.addEventListener('click', doDownload);
    brow.appendChild(dl);
    var pauseBtn = el('button', 'b', 'Pause');
    pauseBtn.addEventListener('click', function () {
      REC = !REC;
      pauseBtn.textContent = REC ? 'Pause' : 'Resume';
      dotEl.className = REC ? 'dot' : 'dot off';
      uiStatus();
    });
    brow.appendChild(pauseBtn);
    var clr = el('button', 'b clr', 'Clear');
    clr.addEventListener('click', function () {
      LOG.length = 0; SEQ = 0; persist();
      while (listEl.firstChild) listEl.removeChild(listEl.firstChild);
      uiCount(); uiStatus();
    });
    brow.appendChild(clr);
    panel.appendChild(brow);

    statusEl = el('div', 'st');
    panel.appendChild(statusEl);

    listEl = el('div', 'list');
    panel.appendChild(listEl);

    root.appendChild(panel);

    // seed list with most recent entries
    var seed = LOG.slice(-15);
    for (var i = 0; i < seed.length; i++) uiAdd(seed[i]);
    uiCount();
    uiStatus();
  }

  function statusClass(st) {
    var s = String(st || 0)[0];
    return s === '2' ? 's2' : s === '4' ? 's4' : s === '5' ? 's5' : 's0';
  }

  function uiAdd(rec) {
    if (!listEl) return;
    var it = el('div', 'it');
    var m = el('span', 'm', rec.method + ' ');
    it.appendChild(m);
    var label = rec.proc || rec.url.replace(/^https?:\/\/[^/]+/, '');
    it.appendChild(document.createTextNode('#' + rec.n + ' ' + label + ' '));
    var s = el('span', statusClass(rec.status), '(' + rec.status + ')');
    it.appendChild(s);
    listEl.insertBefore(it, listEl.firstChild);
    while (listEl.childNodes.length > 15) listEl.removeChild(listEl.lastChild);
  }

  function uiCount() {
    if (countEl) countEl.textContent = String(LOG.length);
    if (badgeCount) badgeCount.textContent = String(LOG.length);
  }

  function uiStatus() {
    if (!statusEl) return;
    statusEl.textContent = (REC ? 'Recording' : 'Paused') + '  |  ' + LOG.length +
      ' calls  |  filter: ' + (FILTER ? '"' + FILTER + '"' : 'ALL');
  }

  function doDownload() {
    try {
      var data = JSON.stringify(LOG, null, 1);
      var blob = new Blob([data], { type: 'application/json' });
      var url = URL.createObjectURL(blob);
      var a = el('a');
      a.href = url;
      a.download = 'tnr-capture-' + new Date().toISOString().replace(/[:.]/g, '-') + '.json';
      document.body.appendChild(a);
      a.click();
      setTimeout(function () {
        try { document.body.removeChild(a); } catch (e) {}
        URL.revokeObjectURL(url);
      }, 1500);
    } catch (e) {}
  }

  var iv = setInterval(function () {
    if (document.body) { uiBuild(); if (host) clearInterval(iv); }
  }, 400);
})();
