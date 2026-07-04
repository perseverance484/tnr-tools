/* TNR Quality Control (QC) v1.3 - unattended AI battle testing.
   Fetches a testspec (policies + assertions) and runs fight campaigns against a quest-gated AI,
   judging boss behavior live and exporting one verdict file per campaign.
   PvE only. Dry-run ON by default. */
(function () {
  'use strict';
  if (window.__tnrQC) return;
  window.__tnrQC = true;

  var API = location.origin + '/api/trpc/';
  var S = {
    running: false, dryRun: true, spec: null, names: null, idByName: null,
    battleId: null, lastVersion: -1, acting: false, timer: null,
    fight: null, fights: [], events: [], phaseIdx: 0, fightNum: 0, maxFights: 10,
    pollMs: 1500, actDelay: 800, errStreak: 0
  };

  /* ---------- tRPC ---------- */
  function tq(proc, input) {
    var u = API + proc + '?batch=1&input=' + encodeURIComponent(JSON.stringify({ 0: { json: input } }));
    return fetch(u, { credentials: 'include' })
      .then(function (r) {
        if (!r.ok) throw new Error(proc + ' HTTP ' + r.status);
        return r.json();
      })
      .then(function (j) {
        try { return j[0].result.data.json; }
        catch (e) { throw new Error(proc + ' bad shape: ' + JSON.stringify(j).slice(0, 180)); }
      });
  }
  function tm(proc, input) {
    return fetch(API + proc + '?batch=1', {
      method: 'POST', credentials: 'include',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ 0: { json: input } })
    }).then(function (r) { return r.json(); })
      .then(function (j) { return j[0].result.data.json; });
  }

  function loadNames() {
    if (S.idByName) return Promise.resolve();
    return tq('jutsu.getAllNames', {}).then(function (list) {
      S.idByName = {}; S.names = {};
      (list || []).forEach(function (n) {
        if (n && n.name) { S.idByName[n.name.trim().toLowerCase()] = n.id; S.names[n.id] = n.name; }
      });
    });
  }
  function jid(nameOrId) {
    if (!nameOrId) return null;
    var k = String(nameOrId).trim().toLowerCase();
    return (S.idByName && S.idByName[k]) || nameOrId;
  }

  /* ---------- state helpers ---------- */
  function me(b) { var m = null; b.usersState.forEach(function (u) { if (u.iAmHere) m = u; }); return m; }
  function aiFoe(b, my) {
    var f = null;
    b.usersState.forEach(function (u) {
      if (u.isAi && u.curHealth > 0 && !u.fledBattle && !u.leftBattle) f = u;
    });
    return f;
  }
  function dist(a, b) { return Math.max(Math.abs(a.longitude - b.longitude), Math.abs(a.latitude - b.latitude)); }
  function fxOn(b, uid) { return (b.usersEffects || []).filter(function (e) { return e.targetId === uid; }); }
  function fxPower(b, uid, type) {
    var p = 0; fxOn(b, uid).forEach(function (e) { if (e.type === type) p += Math.abs(e.power || 0); }); return p;
  }
  function ready(b, my, id) {
    var ok = false;
    (my.jutsus || []).forEach(function (j) {
      if (j.jutsuId === id && j.equipped && (b.round - j.lastUsedRound) >= j.originalCooldown) ok = true;
    });
    return ok;
  }

  /* ---------- policy interpreter (same vocabulary as pilot v1) ---------- */
  function condOk(c, ctx) {
    var b = ctx.b, my = ctx.my, foe = ctx.foe;
    switch (c.cond) {
      case 'always': return true;
      case 'round_lte': return b.round <= c.value;
      case 'round_gte': return b.round >= c.value;
      case 'distance_lte': return foe && dist(my, foe) <= c.value;
      case 'distance_gte': return foe && dist(my, foe) >= c.value;
      case 'ap_gte': return my.actionPoints >= c.value;
      case 'my_hp_pct_lte': return (my.curHealth / my.maxHealth) * 100 <= c.value;
      case 'enemy_hp_pct_lte': return foe && (foe.curHealth / foe.maxHealth) * 100 <= c.value;
      case 'self_has_effect': return fxPower(b, my.userId, c.type) >= (c.threshold || 1);
      case 'self_lacks_effect': return fxPower(b, my.userId, c.type) < (c.threshold || 1);
      case 'enemy_has_effect': return foe && fxPower(b, foe.userId, c.type) >= (c.threshold || 1);
      case 'enemy_lacks_effect': return foe && fxPower(b, foe.userId, c.type) < (c.threshold || 1);
      case 'jutsu_ready': return ready(b, my, jid(c.jutsu));
      default: return false;
    }
  }
  function step(my, foe, away, b) {
    var best = null, bestD = away ? -1 : 1e9;
    for (var dx = -1; dx <= 1; dx++) for (var dy = -1; dy <= 1; dy++) {
      if (!dx && !dy) continue;
      var x = my.longitude + dx, y = my.latitude + dy;
      if (x < 0 || y < 0 || x >= b.width || y >= b.height) continue;
      if (b.usersState.some(function (u) { return u.curHealth > 0 && u.longitude === x && u.latitude === y; })) continue;
      var dd = Math.max(Math.abs(x - foe.longitude), Math.abs(y - foe.latitude));
      if ((away && dd > bestD) || (!away && dd < bestD)) { bestD = dd; best = { longitude: x, latitude: y }; }
    }
    return best;
  }
  function decide(ctx, rules) {
    for (var i = 0; i < rules.length; i++) {
      var r = rules[i], ok = true;
      (r.when || []).forEach(function (c) { if (!condOk(c, ctx)) ok = false; });
      if (!ok) continue;
      var a = r.do || {};
      if (a.type === 'cast') {
        var id = jid(a.jutsu);
        if (!ready(ctx.b, ctx.my, id)) continue;
        var t = a.target === 'self' ? ctx.my : ctx.foe;
        if (!t) continue;
        return { name: r.name, actionId: id, longitude: t.longitude, latitude: t.latitude };
      }
      if (a.type === 'basic') {
        var t2 = a.target === 'self' ? ctx.my : ctx.foe;
        if (!t2) continue;
        return { name: r.name, actionId: a.id, longitude: t2.longitude, latitude: t2.latitude };
      }
      if (a.type === 'move_to_distance') {
        if (!ctx.foe) continue;
        var cur = dist(ctx.my, ctx.foe);
        if (cur === a.value) continue;
        var s = step(ctx.my, ctx.foe, cur < a.value, ctx.b);
        if (!s) continue;
        return { name: r.name, actionId: 'move', longitude: s.longitude, latitude: s.latitude };
      }
      if (a.type === 'end_turn')
        return { name: r.name, actionId: 'wait', longitude: ctx.my.longitude, latitude: ctx.my.latitude, endsTurn: true };
    }
    return { actionId: 'wait', longitude: ctx.my.longitude, latitude: ctx.my.latitude, endsTurn: true, name: 'fallthrough' };
  }

  /* ---------- fight recording + onboard judge ---------- */
  function newFight(phase) {
    return { phase: phase.name, startedAt: new Date().toISOString(), turns: [], hits: [],
             bossCasts: {}, assertions: {}, result: null, rounds: 0 };
  }
  function snap(b, my, foe) {
    return { round: b.round, v: b.version,
      my: { hp: Math.round(my.curHealth), ap: my.actionPoints, x: my.longitude, y: my.latitude },
      foe: foe ? { hp: Math.round(foe.curHealth), x: foe.longitude, y: foe.latitude, d: dist(my, foe) } : null,
      myFx: fxOn(b, my.userId).map(function (e) { return e.type + ':' + e.power; }),
      foeFx: foe ? fxOn(b, foe.userId).map(function (e) { return e.type + ':' + e.power; }) : [] };
  }
  function judgeBossTurn(preState, entries, f) {
    var casts = [];
    (entries || []).forEach(function (le) {
      var d = le.description || '';
      var name = d.indexOf(':') > 0 ? d.split(':')[0].trim() : '';
      if (name && name !== 'End Turn' && name !== 'Move') casts.push(name);
      (le.appliedEffects || []).forEach(function (ae) {
        var m = /^(.*?) takes ([\d,.]+) (damage|afterburn damage)/.exec(ae.txt || '');
        if (m) f.hits.push({ round: le.battleRound, action: name, victim: m[1],
                             dmg: parseFloat(m[2].replace(/,/g, '')), kind: m[3] });
      });
    });
    casts.forEach(function (c) { f.bossCasts[c] = (f.bossCasts[c] || 0) + 1; });
    (S.spec.assertions || []).forEach(function (a) {
      var applicable = true;
      (a.when || []).forEach(function (c) {
        var v;
        if (c.check === 'foe_shield_gte') v = preState.myShield >= c.value;
        else if (c.check === 'distance_gte') v = preState.d >= c.value;
        else if (c.check === 'my_effect_gte') v = (preState.myFxSum[c.type] || 0) >= c.value;
        else v = false;
        if (!v) applicable = false;
      });
      if (!applicable) return;
      var rec = f.assertions[a.name] || { pass: 0, fail: 0 };
      var hit = casts.some(function (c) { return (a.expectCastAnyOf || []).indexOf(c) >= 0; });
      if (hit) rec.pass++; else rec.fail++;
      f.assertions[a.name] = rec;
    });
  }
  function preStateFor(b, my, foe) {
    var sums = {};
    fxOn(b, my.userId).forEach(function (e) { sums[e.type] = (sums[e.type] || 0) + Math.abs(e.power || 0); });
    return { d: foe ? dist(my, foe) : 99, myShield: sums.shield || 0, myFxSum: sums };
  }

  function finishFight(won) {
    var f = S.fight; if (!f) return;
    f.result = won ? 'win' : 'loss';
    var kit = S.spec.bossKit || [];
    f.deadJutsu = kit.filter(function (k) { return !f.bossCasts[k]; });
    var bossTotal = 0; f.hits.forEach(function (h) { if (h.victim !== S.spec.bossName) bossTotal += h.dmg; });
    f.bossDmgPerRound = f.rounds ? Math.round(bossTotal / f.rounds) : 0;
    f.ttk = f.rounds;
    var band = S.spec.ttkBand || [8, 12];
    f.flags = [];
    if (f.deadJutsu.length) f.flags.push('DEAD_JUTSU: ' + f.deadJutsu.join(', '));
    if (won && (f.ttk < band[0] || f.ttk > band[1])) f.flags.push('TTK_OUT_OF_BAND: ' + f.ttk);
    if (f.bossDmgPerRound < (S.spec.bossMinDmgPerRound || 0)) f.flags.push('BOSS_TOO_SOFT: ' + f.bossDmgPerRound);
    S.fights.push(f); S.fight = null;
    status('fight ' + S.fightNum + ' ' + f.result + ' r' + f.ttk);
  }

  /* ---------- campaign loop ---------- */
  function phase() { var ps = S.spec.phases || []; return ps[S.phaseIdx % ps.length]; }
  function startNextFight() {
    if (S.fightNum >= S.maxFights) { stop(); status('campaign done: ' + S.fights.length + ' fights'); return; }
    S.fightNum++;
    var sp = S.spec;
    tm('hospital.npcHeal', { villageId: sp.villageId }).catch(function () {})
      .then(function () { return tq('profile.getUser', {}); })
      .then(function (u) {
        var sector = u && u.userData && u.userData.sector;
        return tm('quests.startQuest', { questId: sp.questId, userSector: sector });
      })
      .then(function () { return tm('quests.checkRewards', { questId: sp.questId, nextObjectiveId: sp.battleObjectiveId }); })
      .then(function () {
        S.fight = newFight(phase()); S.phaseIdx++;
        S.battleId = null; S.lastVersion = -1;
        status('fight ' + S.fightNum + ' started (' + S.fight.phase + ')');
      })
      .catch(function (e) { status('START ERROR: ' + (e && e.message || e)); S.errStreak++; if (S.errStreak > 3) { stop(); status('stopped after repeated start errors'); } });
  }

  function tick() {
    if (!S.running || S.acting) return;
    if (!S.fight) {
      if (S.dryRun) { dryAttach(); return; }
      S.acting = true; startNextFight(); setTimeout(function () { S.acting = false; }, 2500); return;
    }
    var getBid = S.battleId ? Promise.resolve(S.battleId)
      : tq('profile.getUser', {}).then(function (u) { return u && u.userData && u.userData.battleId; });
    getBid.then(function (bid) {
      if (!bid) { finishFight(true); return; }
      S.battleId = bid;
      return tq('combat.getBattle', { battleId: bid }).then(function (res) {
        if (!S.sawBattleShape) {
          S.sawBattleShape = true;
          status('getBattle shape: ' + (res ? Object.keys(res).join(',').slice(0, 120) : 'null'));
        }
        var b = res && res.battle; if (!b) { status('no .battle in payload'); S.battleId = null; return; }
        var my = me(b);
        if (!my) {
          if (!S.saidNoMe) { S.saidNoMe = true;
            status('no iAmHere; users: ' + b.usersState.map(function (u) { return u.username + (u.isAi ? '(ai)' : '') + (u.iAmHere ? '(me)' : ''); }).join(', ').slice(0, 140)); }
          var humans = b.usersState.filter(function (u) { return !u.isAi; });
          if (humans.length === 1) my = humans[0]; else { S.battleId = null; return; }
        }
        var foe = aiFoe(b, my);
        if (!foe) { finishFight(true); S.battleId = null; return; }
        if (my.curHealth <= 0) { finishFight(false); S.battleId = null; return; }
        S.fight.rounds = b.round;
        if (b.version === S.lastVersion) return;
        if (S.dryRun) { S.lastVersion = b.version; dryObserve(b, my, foe); return; }
        if (b.activeUserId !== my.userId) {
          S.lastVersion = b.version;
          if (S.waitTicks === undefined) S.waitTicks = 0;
          if (++S.waitTicks % 8 === 1) {
            var act = b.usersState.filter(function (u) { return u.userId === b.activeUserId; })[0];
            status('waiting r' + b.round + ': active=' + (act ? act.username : b.activeUserId).toString().slice(0, 30));
          }
          return;
        }
        S.waitTicks = 0;
        var ctx = { b: b, my: my, foe: foe };
        var pre = preStateFor(b, my, foe);
        var d = decide(ctx, phaseRules());
        S.fight.turns.push({ snap: snap(b, my, foe), chose: d.name, action: S.names && S.names[d.actionId] || d.actionId });
        if (S.dryRun) { S.lastVersion = b.version; status('DRY r' + b.round + ' ' + d.name); return; }
        S.acting = true;
        tm('combat.performAction', { battleId: b.id, userId: my.userId, actionId: d.actionId,
          longitude: d.longitude, latitude: d.latitude, version: b.version })
          .then(function (out) {
            S.errStreak = 0;
            judgeBossTurn(pre, out && out.logEntries, S.fight);
            S.lastVersion = -1;
          })
          .catch(function (e) { S.errStreak++; if (S.errStreak > 5) stop(); })
          .then(function () { setTimeout(function () { S.acting = false; }, S.actDelay); });
      });
    }).catch(function () {});
  }
  var seenEntries = {};
  function dryAttach() {
    tq('profile.getUser', {}).then(function (u) {
      var bid = u && u.userData && u.userData.battleId;
      if (!bid) { status('DRY: start a battle manually'); return; }
      S.battleId = bid; S.fight = newFight({ name: 'dry_observe' });
      status('DRY: observing battle');
    }).catch(function (e) { status('DRY attach error: ' + e); });
  }
  function dryObserve(b, my, foe) {
    S.fight.rounds = b.round;
    S.fight.turns.push({ snap: snap(b, my, foe), chose: 'observe', action: null });
    tq('combat.getBattleEntries', { battleId: b.id, refreshKey: 1, checkBattle: false, limit: 1000 })
      .then(function (list) {
        if (!S.sawEntriesShape) { S.sawEntriesShape = true; status('entries type: ' + (Array.isArray(list) ? 'array ' + list.length : typeof list)); }
        var fresh = [];
        (Array.isArray(list) ? list : []).forEach(function (le) {
          var key = le.id || (le.createdAt + '|' + (le.description || '').slice(0, 40));
          if (seenEntries[key]) return;
          seenEntries[key] = 1; fresh.push(le);
        });
        if (fresh.length) judgeBossTurn(preStateFor(b, my, foe), fresh, S.fight);
      }).catch(function (e) { status('tick error: ' + (e && e.message || e)); });
  }
  function phaseRules() {
    var p = phase();
    if (S.fight) { for (var i = 0; i < (S.spec.phases || []).length; i++) if (S.spec.phases[i].name === S.fight.phase) return S.spec.phases[i].rules; }
    return p ? p.rules : [];
  }
  function start() { if (S.running) return; S.running = true; S.timer = setInterval(tick, S.pollMs); status('QC running'); }
  function stop() { S.running = false; if (S.timer) clearInterval(S.timer); status('stopped'); }

  /* ---------- UI ---------- */
  var panel, statusEl;
  function el(tag, css, txt) {
    var e = document.createElement(tag);
    if (css) Object.keys(css).forEach(function (k) { e.style[k] = css[k]; });
    if (txt) e.textContent = txt; return e;
  }
  function status(t) {
    if (statusEl) statusEl.textContent = 'QC: ' + t;
    S.events.push({ t: new Date().toISOString(), msg: String(t) });
    if (S.events.length > 800) S.events.shift();
  }
  function btn(label, fn) {
    var b = el('button', { margin: '2px', padding: '4px 8px', fontSize: '11px', background: '#1a1028', color: '#eee', border: '1px solid #5a4a7a', borderRadius: '4px' }, label);
    b.addEventListener('click', fn); return b;
  }
  function buildUI() {
    panel = el('div', { position: 'fixed', bottom: '8px', left: '8px', zIndex: 99999,
      background: 'rgba(12,8,20,0.94)', color: '#eee', padding: '6px', borderRadius: '8px',
      fontFamily: 'monospace', fontSize: '11px', maxWidth: '260px' });
    statusEl = el('div', { marginBottom: '4px' }, 'QC: idle');
    panel.appendChild(statusEl);
    var row = el('div', {});
    row.appendChild(btn('Spec', function () {
      fetch(window.TNR_QC_SPEC_URL || 'https://raw.githubusercontent.com/perseverance484/tnr-tools/main/testspec_endless_night.json?v=1')
        .then(function (r) { return r.json(); })
        .then(function (s) { S.spec = s; S.maxFights = s.maxFights || 10; status('spec ' + s.name + ' (' + (s.phases || []).length + ' phases)'); })
        .catch(function () { status('spec fetch failed'); });
    }));
    row.appendChild(btn('Start', function () {
      if (!S.spec) { status('load spec first'); return; }
      loadNames().then(start);
    }));
    row.appendChild(btn('Stop', stop));
    row.appendChild(btn('Dry:ON', function () { S.dryRun = !S.dryRun; this.textContent = S.dryRun ? 'Dry:ON' : 'Dry:OFF'; }));
    row.appendChild(btn('Verdict', function () {
      var out = { spec: S.spec && S.spec.name, generatedAt: new Date().toISOString(),
        fights: S.fights, partialFight: S.fight, events: S.events, summary: summarize() };
      var blob = new Blob([JSON.stringify(out, null, 1)], { type: 'application/json' });
      var a = el('a', {}); a.href = URL.createObjectURL(blob);
      a.download = 'tnr-qc-verdict-' + Date.now() + '.json';
      document.body.appendChild(a); a.click(); a.remove();
    }));
    panel.appendChild(row);
    document.body.appendChild(panel);
  }
  function summarize() {
    var s = { fights: S.fights.length, wins: 0, ttks: [], flags: [], assertions: {} };
    S.fights.forEach(function (f) {
      if (f.result === 'win') { s.wins++; s.ttks.push(f.ttk); }
      (f.flags || []).forEach(function (fl) { s.flags.push(f.phase + ': ' + fl); });
      Object.keys(f.assertions || {}).forEach(function (k) {
        var a = s.assertions[k] || { pass: 0, fail: 0 };
        a.pass += f.assertions[k].pass; a.fail += f.assertions[k].fail;
        s.assertions[k] = a;
      });
    });
    return s;
  }
  if (document.body) buildUI(); else document.addEventListener('DOMContentLoaded', buildUI);
})();
