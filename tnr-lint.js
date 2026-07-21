/* tnr-lint.js v1.0 (2026-07-18)
 * Machine lint for TNR builder manifests. Embeds 13_LINT_rules.json (stack) as executable checks.
 * Self-contained: no fetches, no DOM. Usage:
 *   var res = TNRLint.run(manifest);            // {blocks:[...], warns:[...]}
 *   if (res.blocks.length && !manifest.skipPreflight) { log(TNRLint.report(res)); abort; }
 *   else log(TNRLint.report(res));
 * L14 (id provenance) is generation-side and intentionally not implemented here.
 */
(function (root) {
  'use strict';

  var DECOR = ['appearSfx','disappearSfx','appearAnimation','disappearAnimation','staticAnimation','staticAssetPath','description','powerPerLevel','calculation','direction','target','statTypes','generalTypes'];
  var CORE = { // effect type -> core allowed fields beyond {type,power,rounds}
    damage:['elements'], pierce:['elements'], wound:[],
    increasedamagegiven:[], decreasedamagetaken:[], increasedamagetaken:[],
    increasestat:[], absorb:[], reflect:[], shield:[],
    heal:['poolsAffected'], stun:['apReduction'], seal:[], moveprevent:[],
    drain:['poolsAffected'], decreasehealgiven:[], increasecooldown:[],
    clear:[], cleanse:[], debuffprevent:[], copy:[], lifesteal:[]
  };
  var FORMULA_TYPES = {damage:1, pierce:1, wound:1};
  var PCT_STACK_TYPES = {increasedamagegiven:1, decreasedamagetaken:1, increasedamagetaken:1};

  function isObj(x){ return x && typeof x === 'object' && !Array.isArray(x); }
  function walkEffects(data, cb){
    if (!isObj(data)) return;
    if (Array.isArray(data.effects)) data.effects.forEach(function(f,i){ if (isObj(f) && f.type) cb(f,i); });
  }
  function push(list, rule, entry, msg){ list.push({rule:rule, srcId:(entry&&entry.srcId)||'?', msg:msg}); }

  function run(manifest){
    var B=[], W=[];
    var items = (manifest && manifest.items) || [];
    var imgSizes = (manifest && manifest.imgSizes) || {};
    var createSrc = {};
    items.forEach(function(e){ if (e.slot==='create' && e.srcId) createSrc[e.srcId]=1; });

    // L02 refs resolved (manifest-wide, honoring same-manifest creates and imgSizes)
    var txt = JSON.stringify(manifest);
    var refRe = /@(jutsu|item|ai|scene|img):([A-Za-z0-9_.\-]+)/g, m;
    while ((m = refRe.exec(txt))){
      if (m[1]==='img'){ if (!(m[2] in imgSizes)) push(B,'L17',null,'@img:'+m[2]+' has no imgSizes byte entry'); }
      else if (!createSrc[m[2]]) push(B,'L02',null,'@'+m[1]+':'+m[2]+' does not resolve to a create in this manifest');
    }

    // injectjutsus wrapper detection for L13 exception
    var injectRefs = {};
    items.forEach(function(e){
      if (e.entity==='item') walkEffects(e.data, function(f){
        if (f.type==='injectjutsus') JSON.stringify(f).replace(/@jutsu:([A-Za-z0-9_\-]+)/g, function(_,s){ injectRefs[s]=1; return _; });
      });
    });

    items.forEach(function(e){
      var d = e.data || {};
      // L01
      if ((e.slot==='convert'||e.slot==='edit') && (!e.targetId || typeof e.targetId!=='string' || e.targetId.charAt(0)==='@'))
        push(B,'L01',e,'convert/edit without a literal targetId');
      // L03/L04/L11/L12: quest checks
      if (e.entity==='quest'){
        if (e.slot==='create' && d.consecutiveObjectives!==true) push(B,'L03',e,'quest create without consecutiveObjectives:true');
        ['startsAt','endsAt'].forEach(function(k){
          if (k in d && d[k] && !/^\d{4}-\d{1,2}-\d{1,2}$/.test(String(d[k]))) push(B,'L04',e,k+' must be plain YYYY-MM-DD');
        });
        var objs = d.content && d.content.objectives;
        if (Array.isArray(objs)){
          var ids={}, referenced={}, wins=[];
          objs.forEach(function(o){ ids[o.id]=1; });
          var edges={};
          objs.forEach(function(o){
            var tg=[];
            if (o.task==='dialog'){
              var nx=o.nextObjectiveId;
              if (Array.isArray(nx)) nx.forEach(function(c){ tg.push(c.nextObjectiveId); });
              else if (nx) tg.push(nx);
              var dtext=(o.description||'')+(Array.isArray(nx)?nx.map(function(c){return c.text||'';}).join(' '):'');
              if (/[\u2013\u2014]/.test(dtext)) push(B,'L11',e,'em/en dash in dialog node '+o.id);
            } else if (o.task==='start_battle'){
              if (!o.failObjectiveId) push(B,'L12',e,'battle '+o.id+' missing failObjectiveId');
              if (!o.opponentAIs || !o.opponentAIs.length) push(B,'L12',e,'battle '+o.id+' missing opponentAIs');
              tg.push(o.nextObjectiveId, o.failObjectiveId);
            } else if (o.nextObjectiveId) tg.push(o.nextObjectiveId);
            edges[o.id]=tg.filter(Boolean);
            tg.forEach(function(t){ if(t) referenced[t]=1; });
            if (o.task==='win_quest') wins.push(o.id);
          });
          objs.forEach(function(o){ edges[o.id].forEach(function(t){ if(!ids[t]) push(B,'L12',e,'edge '+o.id+' -> '+t+' unresolved'); }); });
          var starts = objs.filter(function(o){ return !referenced[o.id]; });
          if (starts.length!==1) push(B,'L12',e,'start-node count '+starts.length+' (expected 1)');
          if (starts.length===1){
            var seen={}, stack=[starts[0].id];
            while (stack.length){ var u=stack.pop(); if(seen[u])continue; seen[u]=1; (edges[u]||[]).forEach(function(t){stack.push(t);}); }
            wins.forEach(function(wn){ if(!seen[wn]) push(B,'L12',e,'win node '+wn+' unreachable'); });
          }
        }
      }
      // L05
      if (e.entity==='ai' && e.slot==='create'){
        ['rank','regeneration','preferredStat','preferredGeneral1','preferredGeneral2'].forEach(function(k){
          if (!(k in d)) push(B,'L05',e,'AI create missing '+k);
        });
      }
      // L13 hidden default on creates
      if (e.slot==='create' && 'entity' in e){
        var isWrapper = e.entity==='jutsu' && e.srcId && injectRefs[e.srcId];
        if (isWrapper){ if (d.hidden!==false) push(B,'L13',e,'injectjutsus wrapper jutsu must be hidden:false'); }
        else if (d.hidden!==true) push(B,'L13',e,'create without hidden:true');
      }
      // jutsu-level checks
      if (e.entity==='jutsu'){
        var cd = d.cooldown; if (cd!=null && cd<3) push(B,'L16',e,'cooldown '+cd+' below floor 3');
        var ep = d.actionCostPerc; if (ep!=null && ep>70) push(W,'L10',e,'EP '+ep+' above signature ceiling 70');
      }
      // per-effect checks
      var pctCount={};
      walkEffects(d, function(f){
        if (FORMULA_TYPES[f.type]){
          if (!Array.isArray(f.statTypes)||!f.statTypes.length||!Array.isArray(f.generalTypes)||!f.generalTypes.length)
            push(B,'L06',e,f.type+' effect missing statTypes/generalTypes');
        }
        if ('direction' in f && f.direction!=='offence') push(B,'L07',e,f.type+' direction "'+f.direction+'" (must be "offence")');
        if (f.type==='stun' && !('apReduction' in f)) push(W,'L15',e,'stun without apReduction (defaults to 10)');
        if (CORE.hasOwnProperty(f.type)){
          var allowed={type:1,power:1,rounds:1};
          DECOR.forEach(function(k){allowed[k]=1;});
          CORE[f.type].forEach(function(k){allowed[k]=1;});
          Object.keys(f).forEach(function(k){ if(!allowed[k]) push(B,'L09',e,f.type+' effect has illegal field "'+k+'"'); });
        } else push(W,'L09',e,'effect type "'+f.type+'" not in the exemplar bank (verify against 46/40x)');
        if (PCT_STACK_TYPES[f.type] && (f.calculation==='percentage'||!f.calculation))
          pctCount[f.type]=(pctCount[f.type]||0)+1;
        if (e.entity==='item'){
          if (f.type==='clear'||f.type==='copy') push(B,'L18',e,'item effect "'+f.type+'" excluded from the item union');
          if (f.type==='noncombatconsumereward' && d.target!=='SELF') push(B,'L18',e,'noncombatconsumereward requires item target SELF');
        }
      });
      Object.keys(pctCount).forEach(function(tp){
        if (pctCount[tp]>4){
          var prod=1; walkEffects(d,function(f){ if(f.type===tp && (f.calculation==='percentage'||!f.calculation)) prod*=(1+(f.power||0)/100); });
          push(W,'L08',e,pctCount[tp]+' '+tp+' rows: product multiplier x'+prod.toFixed(1));
        }
      });
    });
    return {blocks:B, warns:W};
  }

  function report(res){
    var out=[];
    res.blocks.forEach(function(b){ out.push('BLOCK ['+b.rule+'] '+b.srcId+': '+b.msg); });
    res.warns.forEach(function(w){ out.push('warn  ['+w.rule+'] '+w.srcId+': '+w.msg); });
    return out.length? out.join('\n') : 'lint clean';
  }

  root.TNRLint = {run:run, report:report, version:'1.0'};
})(typeof unsafeWindow!=='undefined'?unsafeWindow:(typeof window!=='undefined'?window:globalThis));
