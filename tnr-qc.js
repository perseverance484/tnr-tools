/* TNR Quality Control (QC) v2.6 - unattended AI battle testing.
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
    pollMs: 1500, actDelay: 1200, backoff: 0, errStreak: 0, usedBasics: {}, hexParity: 1, badTiles: {}, loopVersion: -9, loopCount: 0
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
      .then(function (j) {
        try { return j[0].result.data.json; }
        catch (e) {
          var msg = '';
          try { msg = j[0].error.json.message; } catch (e2) { msg = JSON.stringify(j).slice(0, 140); }
          throw new Error(proc + ': ' + msg);
        }
      });
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
  function axial(x, y) {
    var par = S.hexParity; // 1 = odd columns shifted, 0 = even columns shifted (odd-q, flat-top)
    var r = y - (x - (par ? (x & 1) : -(x & 1))) / 2;
    return { q: x, r: r };
  }
  function dist(a, b) {
    var A = axial(a.longitude, a.latitude), B = axial(b.longitude, b.latitude);
    var dq = A.q - B.q, dr = A.r - B.r;
    return (Math.abs(dq) + Math.abs(dr) + Math.abs(dq + dr)) / 2;
  }
  function fxOn(b, uid) { return (b.usersEffects || []).filter(function (e) { return e.targetId === uid; }); }
  function fxPower(b, uid, type) {
    var p = 0; fxOn(b, uid).forEach(function (e) { if (e.type === type) p += Math.abs(e.power || 0); }); return p;
  }
  function basicReady(b, my, id) {
    if (id === 'move' || id === 'wait') return true;
    var ok = true;
    (my.basicActions || []).forEach(function (a) {
      if (a.id === id && a.lastUsedRound >= b.round) ok = false;
    });
    var k = id + '|' + b.round;
    if (S.usedBasics[k]) ok = false;
    return ok;
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
    var cands = [];
    for (var dx = -1; dx <= 1; dx++) for (var dy = -1; dy <= 1; dy++) {
      if (!dx && !dy) continue;
      var x = my.longitude + dx, y = my.latitude + dy;
      if (x < 0 || y < 0 || x >= b.width || y >= b.height) continue;
      if (dist({ longitude: x, latitude: y }, my) !== 1) continue; // true hex neighbors only
      if (S.badTiles[x + ',' + y]) continue;
      if (b.usersState.some(function (u) { return u.curHealth > 0 && u.longitude === x && u.latitude === y; })) continue;
      cands.push({ longitude: x, latitude: y, d: dist({ longitude: x, latitude: y }, foe) });
    }
    if (!cands.length) return null;
    cands.sort(function (p, q) { return away ? q.d - p.d : p.d - q.d; });
    return cands[0];
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
        if (!basicReady(ctx.b, ctx.my, a.id)) continue;
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
    // record casts + evaluate assertions from the spec against the pre-turn state
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
    var kitNames = S.spec.bossKit || [];
    casts = casts.filter(function (c) { return kitNames.some(function (k) { return c === k || k.indexOf(c) === 0; }); });
    f.castRounds = f.castRounds || {};
    casts.forEach(function (c) {
      f.bossCasts[c] = (f.bossCasts[c] || 0) + 1;
      (f.castRounds[c] = f.castRounds[c] || []).push(preState.round);
    });
    (S.spec.assertions || []).forEach(function (a) {
      var applicable = true;
      (a.when || []).forEach(function (c) {
        var v;
        if (c.check === 'foe_shield_gte') v = preState.myShield >= c.value;
        else if (c.check === 'distance_gte') v = preState.d >= c.value;
        else if (c.check === 'round_gte') v = preState.round >= c.value;
        else if (c.check === 'my_effect_gte') v = (preState.myFxSum[c.type] || 0) >= c.value;
        else v = false;
        if (!v) applicable = false;
      });
      if (!applicable) return;
      // skip if every expected jutsu is on cooldown from a prior cast
      var cds = S.spec.bossCooldowns || {};
      var anyAvailable = (a.expectCastAnyOf || []).some(function (j) {
        var cd = cds[j]; var rounds = (f.castRounds && f.castRounds[j]) || [];
        if (!cd || !rounds.length) return true;
        return (preState.round - rounds[rounds.length - 1]) >= cd;
      });
      if (!anyAvailable) return;
      var rec = f.assertions[a.name] || { pass: 0, fail: 0 };
      var hit = casts.some(function (c) { return (a.expectCastAnyOf || []).indexOf(c) >= 0; });
      if (hit) rec.pass++; else rec.fail++;
      f.assertions[a.name] = rec;
    });
  }
  function preStateFor(b, my, foe) {
    var sums = {};
    fxOn(b, my.userId).forEach(function (e) { sums[e.type] = (sums[e.type] || 0) + Math.abs(e.power || 0); });
    return { d: foe ? dist(my, foe) : 99, round: b.round, myShield: sums.shield || 0, myFxSum: sums };
  }

  function finishFight(won) {
    var f = S.fight; if (!f) return;
    f.result = won ? 'win' : 'loss';
    // flags
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
    S.prevBattleId = S.battleId || S.prevBattleId;
    S.fights.push(f); S.fight = null;
    status('fight ' + S.fightNum + ' ' + f.result + ' r' + f.ttk);
  }

  function tmChecked(proc, input) {
    return tm(proc, input).then(function (j) {
      if (j && j.success === false) throw new Error(proc + ' refused: ' + String(j.message || '').slice(0, 120));
      return j;
    });
  }
  /* ---------- campaign loop ---------- */
  function phase() { var ps = S.spec.phases || []; return ps[S.phaseIdx % ps.length]; }
  function startNextFight() {
    if (S.fightNum >= S.maxFights) { stop(); status('campaign done: ' + S.fights.length + ' fights'); campaignDone(); return; }
    S.fightNum++;
    S.starting = true;
    var sp = S.spec;
    tm('hospital.npcHeal', { villageId: sp.villageId }).catch(function () {})
      .then(function () { return tq('profile.getUser', {}); })
      .then(function (u) {
        S.prevBattleId = (u && u.userData && u.userData.battleId) || S.prevBattleId || null;
        S.mySector = u && u.userData && u.userData.sector;
        // finalize any lingering terminal node from the previous run (ignore refusals)
        var fin = Promise.resolve();
        (sp.finishObjectiveIds || []).forEach(function (oid) {
          fin = fin.then(function () {
            return tm('quests.checkRewards', { questId: sp.questId, nextObjectiveId: oid }).catch(function () {});
          });
        });
        return fin;
      })
      .then(function () {
        return tmChecked('quests.startQuest', { questId: sp.questId, userSector: S.mySector })
          .catch(function (e) {
            if ((e && e.message || '').indexOf('already on this quest') >= 0) {
              status('quest already active, resuming');
              return null;
            }
            throw e;
          });
      })
      .then(function () { return tmChecked('quests.checkRewards', { questId: sp.questId, nextObjectiveId: sp.battleObjectiveId }); })
      .then(function () {
        S.fight = newFight(phase()); S.phaseIdx++; S.usedBasics = {}; S.saidKit = false;
        S.battleId = null; S.lastVersion = -1; S.sawBattleThisFight = false;
        S.errStreak = 0;
        status('fight ' + S.fightNum + ' started (' + S.fight.phase + ')');
      })
      .catch(function (e) {
        S.fightNum--; // this attempt did not consume a fight slot
        status('START ERROR: ' + (e && e.message || e).toString().slice(0, 130));
        S.errStreak++;
        if (S.errStreak > 6) { stop(); status('stopped after repeated start errors'); }
      })
      .then(function () { setTimeout(function () { S.starting = false; S.acting = false; }, 5000); });
  }

  function tick() {
    var now = Date.now();
    if (S.lastTickAt && now - S.lastTickAt > 10000) status('tab was throttled ' + Math.round((now - S.lastTickAt) / 1000) + 's - keep QC foreground');
    S.lastTickAt = now;
    if (!S.running || S.acting) return;
    if (!S.fight) {
      if (S.dryRun) { dryAttach(); return; }
      S.acting = true; startNextFight(); return;
    }
    var getBid = S.battleId ? Promise.resolve(S.battleId)
      : tq('profile.getUser', {}).then(function (u) { return u && u.userData && u.userData.battleId; });
    getBid.then(function (bid) {
      if (!bid) {
        if (!S.sawBattleThisFight) {
          S.noBidTicks = (S.noBidTicks || 0) + 1;
          if (S.noBidTicks % 5 === 1) status('waiting for battle to spawn (' + S.noBidTicks + ')');
          if (S.noBidTicks > 20) { status('fight never materialized; aborting'); S.fight = null; S.noBidTicks = 0; }
          return;
        }
        var won = true;
        if (S.fight && S.fight.lastMyHpPct !== undefined && S.fight.lastFoeHpPct !== undefined)
          won = S.fight.lastFoeHpPct <= S.fight.lastMyHpPct;
        finishFight(won); return;
      }
      S.noBidTicks = 0;
      if (!S.sawBattleThisFight && S.prevBattleId && bid === S.prevBattleId) {
        S.noBidTicks = (S.noBidTicks || 0) + 1;
        if (S.noBidTicks % 5 === 1) status('waiting for new battle (stale id)');
        if (S.noBidTicks > 20) { status('fight never materialized; aborting'); S.fight = null; S.noBidTicks = 0; }
        return;
      }
      S.battleId = bid;
      var pend = S.pendingBattle; S.pendingBattle = null;
      return (pend ? Promise.resolve({ battle: pend }) : tq('combat.getBattle', { battleId: bid })).then(function (res) {
        if (!S.sawBattleShape) {
          S.sawBattleShape = true;
          status('getBattle shape: ' + (res ? Object.keys(res).join(',').slice(0, 120) : 'null'));
        }
        var b = res && res.battle; if (!b) { status('no .battle in payload'); S.battleId = null; return; }
        S.sawBattleThisFight = true;
        var my = me(b);
        if (!my) {
          if (!S.saidNoMe) { S.saidNoMe = true;
            status('no iAmHere; users: ' + b.usersState.map(function (u) { return u.username + (u.isAi ? '(ai)' : '') + (u.iAmHere ? '(me)' : ''); }).join(', ').slice(0, 140)); }
          // fallback: the sole non-AI combatant is me
          var humans = b.usersState.filter(function (u) { return !u.isAi; });
          if (humans.length === 1) my = humans[0]; else { S.battleId = null; return; }
        }
        var foe = aiFoe(b, my);
        if (!foe) { finishFight(true); S.battleId = null; return; }
        if (my.curHealth <= 0) { finishFight(false); S.battleId = null; return; }
        S.fight.rounds = b.round;
        S.fight.lastMyHpPct = Math.round(100 * my.curHealth / my.maxHealth);
        S.fight.lastFoeHpPct = Math.round(100 * foe.curHealth / foe.maxHealth);
        progress('F' + S.fightNum + '/' + S.maxFights + ' ' + (S.fight.phase || '') + ' r' + b.round +
          ' | boss ' + Math.round(100 * foe.curHealth / foe.maxHealth) + '% me ' +
          Math.round(100 * my.curHealth / my.maxHealth) + '% | v' + b.version);
        if (b.version === S.lastVersion) return;
        if (S.dryRun) { S.lastVersion = b.version; dryObserve(b, my, foe); return; }
        if (b.activeUserId !== my.userId) {
          S.lastVersion = b.version;
          var act = b.usersState.filter(function (u) { return u.userId === b.activeUserId; })[0];
          if (act && act.isAi && !S.dryRun) {
            // nudge: an actionId-less performAction makes the server execute the AI turn
            S.acting = true;
            var pre2 = preStateFor(b, my, foe);
            tm('combat.performAction', { battleId: b.id, userId: my.userId, version: b.version })
              .then(function (out) {
                judgeBossTurn(pre2, out && out.logEntries, S.fight);
                if (out && out.battleUpdate && out.battleUpdate.usersState) S.pendingBattle = out.battleUpdate;
                S.lastVersion = -1;
              })
              .catch(function (e) {
                var m = (e && e.message || e).toString();
                if (m.indexOf('too fast') >= 0) { S.backoff = Math.min((S.backoff || S.actDelay) * 2, 20000); }
                else status('nudge error: ' + m.slice(0, 100));
              })
              .then(function () { var d3 = S.backoff || S.actDelay; S.backoff = 0; setTimeout(function () { S.acting = false; tick(); }, d3); });
            return;
          }
          if (S.waitTicks === undefined) S.waitTicks = 0;
          if (++S.waitTicks % 8 === 1) {
            status('waiting r' + b.round + ': active=' + (act ? act.username : b.activeUserId).toString().slice(0, 30));
          }
          return;
        }
        S.waitTicks = 0;
        if (b.version === S.loopVersion) { S.loopCount++; } else { S.loopVersion = b.version; S.loopCount = 0; S.badTiles = {}; }
        if (!S.saidKit) {
          S.saidKit = true;
          var eq = (my.jutsus || []).filter(function (j) { return j.equipped; }).length;
          var missing = [];
          (phaseRules() || []).forEach(function (r) {
            if (r.do && r.do.type === 'cast') {
              var rid = jid(r.do.jutsu);
              if (rid === r.do.jutsu && !(S.idByName && S.idByName[String(r.do.jutsu).trim().toLowerCase()])) missing.push(r.do.jutsu);
            }
          });
          status('my jutsus equipped: ' + eq + (missing.length ? ' | unresolved names: ' + missing.join(', ').slice(0, 90) : ''));
        }
        var ctx = { b: b, my: my, foe: foe };
        var pre = preStateFor(b, my, foe);
        var d = decide(ctx, phaseRules());
        var cap = (S.spec && S.spec.maxRounds) || 0;
        if (cap && b.round > cap) {
          d = { name: 'datacap flee', actionId: 'flee', longitude: my.longitude, latitude: my.latitude };
          if (!basicReady(b, my, 'flee')) d = { name: 'datacap wait', actionId: 'wait', longitude: my.longitude, latitude: my.latitude };
        }
        if (S.loopCount >= 6) {
          status('loop breaker r' + b.round + ' after ' + d.name);
          if (d.actionId === 'move') { S.hexParity = S.hexParity ? 0 : 1; status('hex parity flipped'); }
          d = { name: 'loopbreak', actionId: 'wait', longitude: my.longitude, latitude: my.latitude };
          S.loopCount = 0;
        }
        S.fight.turns.push({ snap: snap(b, my, foe), chose: d.name, action: S.names && S.names[d.actionId] || d.actionId });
        status('r' + b.round + ' ' + d.name + ' -> ' + (S.names && S.names[d.actionId] || d.actionId));
        if (S.dryRun) { S.lastVersion = b.version; status('DRY r' + b.round + ' ' + d.name); return; }
        S.acting = true;
        tm('combat.performAction', { battleId: b.id, userId: my.userId, actionId: d.actionId,
          longitude: d.longitude, latitude: d.latitude, version: b.version })
          .then(function (out) {
            var newV = out && out.battleUpdate && out.battleUpdate.version;
            if (out && out.result === false) {
              status('action rejected: ' + String(out.message || '(no message)').slice(0, 100));
              if (d.actionId === 'move') S.badTiles[d.longitude + ',' + d.latitude] = 1;
            } else if (newV !== undefined && newV === b.version) {
              status('action no-op v' + b.version + ' (' + (S.names && S.names[d.actionId] || d.actionId) + ')');
              if (d.actionId === 'move') { S.badTiles[d.longitude + ',' + d.latitude] = 1; S.loopCount++; }
            } else { S.errStreak = 0; }
            S.usedBasics[d.actionId + '|' + b.round] = 1;
            judgeBossTurn(pre, out && out.logEntries, S.fight);
            S.lastVersion = -1;
            if (out && out.battleUpdate && out.battleUpdate.usersState) S.pendingBattle = out.battleUpdate;
          })
          .catch(function (e) {
            var m = (e && e.message || e).toString();
            if (m.indexOf('too fast') >= 0 || m.indexOf('acting too fast') >= 0) {
              S.backoff = Math.min((S.backoff || S.actDelay) * 2, 20000);
              status('rate limited, backing off ' + Math.round(S.backoff / 1000) + 's');
              S.lastVersion = -1; // retry this turn after backoff
            } else { S.errStreak++; status('action error: ' + m.slice(0, 110)); if (S.errStreak > 5) stop(); }
          })
          .then(function () { var d2 = S.backoff || S.actDelay; S.backoff = 0; setTimeout(function () { S.acting = false; tick(); }, d2); });
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
  function exportVerdict() {
    var out = { spec: S.spec && S.spec.name, generatedAt: new Date().toISOString(),
      fights: S.fights, partialFight: S.fight, events: S.events, summary: summarize() };
    var blob = new Blob([JSON.stringify(out, null, 1)], { type: 'application/json' });
    var a = el('a', {}); a.href = URL.createObjectURL(blob);
    a.download = 'tnr-qc-verdict-' + Date.now() + '.json';
    document.body.appendChild(a); a.click(); a.remove();
  }
  function campaignDone() {
    document.title = '[QC DONE] ' + document.title.replace('[QC DONE] ', '');
    if (panel) panel.style.border = '2px solid #6f6';
    progress('CAMPAIGN DONE: ' + S.fights.length + ' fights - verdict downloaded');
    exportVerdict();
  }
  function start() { if (S.running) return; S.running = true; S.timer = setInterval(tick, S.pollMs); status('QC running'); }
  function stop() { S.running = false; if (S.timer) clearInterval(S.timer); status('stopped'); }

  /* ---------- UI ---------- */
  var panel, statusEl, progressEl;
  function progress(t) { if (progressEl) progressEl.textContent = t; }
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
    statusEl = el('div', { marginBottom: '2px' }, 'QC: idle');
    panel.appendChild(statusEl);
    progressEl = el('div', { marginBottom: '4px', color: '#9d8fc9' }, '-');
    panel.appendChild(progressEl);
    var ta = el('textarea', { width: '240px', height: '48px', fontSize: '10px', background: '#110a1c', color: '#ccc', border: '1px solid #3a2a5a' });
    ta.setAttribute('placeholder', 'paste testspec JSON here (overrides URL)');
    panel.appendChild(ta);
    var row = el('div', {});
    row.appendChild(btn('Load', function () {
      try {
        S.spec = JSON.parse(ta.value);
        S.maxFights = S.spec.maxFights || 10;
        status('spec ' + S.spec.name + ' (' + (S.spec.phases || []).length + ' phases) [pasted]');
      } catch (e) { status('bad spec JSON'); }
    }));
    row.appendChild(btn('Spec', function () {
      fetch(window.TNR_QC_SPEC_URL || 'https://raw.githubusercontent.com/perseverance484/tnr-tools/main/qc/testspec_endless_night.json?v=1')
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
    row.appendChild(btn('Verdict', exportVerdict));
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
