// TNR content builder bundle v4.23 - loaded via @require by the tiny VM loader.
// v4.23: (1) NULL GUARD FIX. wsNorm stripped every null in WS_OMIT_NULL, including fields the
//        server accepts as null (.nullable()/.nullish()). Nine quest fields were affected, so
//        clearing requiredVillage, prerequisiteQuestId, huntingRank et al was IMPOSSIBLE through
//        the builder: the null vanished and fetch-merge preserved the old value. The exempt list
//        is now read from 45g_DATA_checks.json `null_strip_exempt`, which is generated as the
//        name-safe subset (nullable on EVERY entity declaring the field), so `image` - .nullish()
//        on quest, required elsewhere - stays stripped. Law 72.
//        (2) 45g is the shared check config; the container validator reads the same file.
//        (3) Preflight gains laws 77 (runtime-only tags) and 78 (companion requirements),
//            reaching parity with 70_TOOL_validate.py.
//        (4) The results bundle carries `checks`, the preflight inventory, so
//            `validate.py --parity` can diff the two sides against something real.
// v4.18: node factory (short-form objectives) + write-shape normalizer (booleans, null-optionals, enum strings) applied to every mutation body.
// v4.21: capture-only manifests (empty `items` with a `capture` block) parse and build; capture entries shape-checked for `proc` at parse time.
// v4.22: capture.before was nested inside the `if(dedupNames)` block and never ran unless dedup was on; hoisted to build-body level. Capture phase errors now surface in the bundle instead of being swallowed.
// v4.19 changes (three lint bugs; no data was at fault):
//   1. L09 LCORE was a hand-maintained per-tag field whitelist that omitted every field 46 grants
//      through composition (IncludeStats / PowerAttributes). It rejected `elements` on
//      increasedamagegiven / increasedamagetaken / wound, `allowBloodlineDamageIncrease` on
//      damage / pierce, `health` on shield, `poolsAffected` on absorb - all legal, all present on
//      live records. LCORE is now generated from 46_DATA_tag_schemas composition. The 23-tag set is
//      unchanged so lint scope does not widen. `decreasehealgiven` corrected to `decreaseheal`
//      (the old key is not a real tag and never matched anything).
//   2. L07 hardcoded direction === 'offence'. redirection.direction is enum [push,pull] default
//      'pull'. Now checked against each tag's own enum (LDIR, from 46).
//   3. L06 demoted error -> warning. The generalTypes gap is a real engine law, but the server
//      accepts these records, so it must warn rather than block.
// v4.19 changes (bloodline entity + data-driven phase order):
//   1. NEW ENTITY "bloodline": create (null body, id in message) -> bloodline.get -> merge -> bloodline.update.
//      BloodlineValidator is a whole-record 11-field payload with NO id/createdAt/updatedAt, so the
//      merged record is whitelisted to those 11 fields before the write (extra keys are not sent).
//      Server strips rounds/friendlyFire from every effect on write (45 v3); harmless to send.
//   2. PHASE ORDER is now data-driven. PHR gains bloodline:-2 and an entry may carry a numeric
//      "phase" to override its default. The seven hardcoded push loops are replaced by one
//      phase-sorted stable pass, which reproduces the exact v4.15 order for any existing manifest.
//      Rationale: jutsu referencing @item (requiredBloodlineItemId) need items BEFORE jutsu, while
//      items referencing @jutsu (injectjutsus) need the opposite; a per-entry override serves both.
//   3. @bloodline: added to the ref whitelist and the unresolved-ref guard. NOTE resolveRefs was
//      already prefix-agnostic (RFX=/^@\w+:(.+)$/), so the prefix is documentary; the whitelist is
//      what buys ordering validation in preflight.
//   4. Preflight blBad(): required fields, rank/statClassification/difficulty enums, regenIncrease
//      bounds, effect-tag check.
// v4.15 changes (13_LINT_rules.json integration - the session-law lint, roadmap Level 1):
//   1. LINT PASS in preflight: enforces the 2026-07 engine laws that v4.14's schema preflight missed:
//      L01 explicit targetId on convert/edit; L03 consecutiveObjectives:true on quest creates;
//      L04 plain YYYY-MM-DD quest dates; L05 AI-create rank/regeneration/preferred block;
//      L06 statTypes+generalTypes on damage/pierce/wound; L07 direction literal "offence";
//      L08 warn + product printout on >4 same-type percentage rows (multiplicative guard);
//      L09 effect field-set subset vs the exemplar bank; L10 EP>70 warn; L11 em/en-dash ban in
//      dialog text; L12b win_quest reachability (BFS; edges/starts already in v4.14 qBad);
//      L13 hidden:true on creates (injectjutsus wrapper jutsu excepted: must be hidden:false);
//      L15 stun apReduction warn; L16 cooldown floor 3; L17 @img byte-ledger check;
//      L18 item union (clear/copy excluded; noncombatconsumereward target SELF).
//      Ref resolution (L02) stays with v4.14's idmap-aware refBad. "skipPreflight": true bypasses
//      lint too (Brandon-authorized only). Warns never block; they print in row detail.
//   2. Results bundle version stamp fixed (was stale 'v4.13').
// v4.14 changes (62_PLAN Phase 7; schemas sourced from 46_DATA_tag_schemas + 45b_DATA_enums):
//   1. JUTSU EDIT LIMITER FIX: convert/edit now uses a per-id jutsu.get merge base instead of loading
//      the full two-pass catalog, so small edit manifests no longer stall on rate-limit retries.
//   2. DEDUP VIA getAllNames: the opt-in "dedupNames" pass now uses the single-call name-list endpoints
//      (jutsu/item/gameAsset/profile.getAllAiNames) instead of paged full getAll, and GAINS QUEST
//      dedup via quests.getAllNames.
//   3. PREFLIGHT: reward_village_membership validated against the village enum (current + legacy names);
//      public-quest sceneCharacters rule (hidden:false requires main sceneCharacters or per-objective);
//      SOURCE CROSS-FIELD RULES from the server's SuperRefines: jutsu-forbidden tags (rollbloodline,
//      removebloodline, noncombatconsumereward), item cost/consumable/target-SELF constraint sets,
//      EMPTY_GROUND requirements (barrier/clone/summon/move), damage+move needs AOE, target SELF needs
//      range 0, wound/vamp require damage|pierce on the same action, barrier needs staticAssetPath,
//      powerPerLevel=0 rules, clone rounds>0. All presence-gated: a check only fires when the fields
//      involved are present in the payload (partial converts stay safe).
// --- v4.13 notes below remain accurate ---
// v4.13 changes (UPGRADE_ANALYSIS Tier 1 + 2.3):
//   1. QUEST EDIT FETCH-MERGE: quest slot!=create now GETs quests.get {id} and merges your partial data
//      over the live record (Howling rule automated). Send only what changes; arrays still replace whole.
//   2. @quest:/@item: CROSS-REFS: the resolver was already prefix-generic; preflight now VALIDATES every
//      @jutsu/@ai/@scene/@item/@quest ref (must be an earlier-phase srcId, an earlier same-phase quest,
//      or an existing idmap key) and a runtime guard blocks any entry whose refs failed to resolve, so
//      garbage strings can never be saved. Quest->quest forward refs work in one run (manifest order).
//   3. RESULTS BUNDLE: every build auto-downloads tnr_results_<ts>.json: per-entry {name,srcId,entity,
//      slot,state,detail,id,pushed(final merged payload)}, plus the full idmap. Hand this file back for
//      verification and registry updates.
//   4. LIVE NAME DEDUP (opt-in): top-level "dedupNames": true fetches live name lists for jutsu/item/
//      asset/ai creates and reds collisions BEFORE pushing (quest dedup pending a confirmed list
//      endpoint). Off by default to respect the rolling rate budget.
//   5. AI WRITE-SHAPE SANITIZER: fetched raw jutsus join rows -> string id array; items rows ->
//      {ids,number}. The 400 landmine class is deleted; explicit manifest values pass through.
//   6. MANIFEST FILE PICKER: "📄 Load" button loads a manifest JSON from the device (kills the paste cap).
//   7. FIELD SANITIZERS: empty-string image keys stripped pre-push (DB 500 guard); preflight type-checks
//      reward_rank/reward_village_membership (string) and reward_gathering_items/hunter_items (boolean)
//      on quest rewards and objectives.
//   8. EQUIP REMINDER: jutsu convert success rows carry a re-equip warning (silent link severance guard).
//   9. IDMAP EXPORT/IMPORT: "🗺 Map" downloads the idmap; "⤒ Map" imports/merges one (device-loss recovery).
// --- v4.12 notes below remain accurate ---
// v4.12 changes (all three roadmap items from 10_TECH 1.1a, plus preflight):
//   1. json.success read per entry: every mutation response is parsed; HTTP 200 with success:false now
//      shows RED with the server's message (name collisions, flow-invalid, validation errors).
//   2. Error text widened 300 -> 1200 chars so multi-field quest validation errors show at once.
//   3. Fetch-merge on CREATE for jutsu, item, and quest: after create, the builder GETs the fresh record
//      (jutsu.get / item.get / quests.get, all {id}, source-confirmed) and merges your data over its
//      defaults, like convert and the asset path. Partial create payloads no longer NaN-fail; complete
//      payloads still recommended. Item edit (slot!=create) also fetch-merges over the live record.
//   4. Preflight validation before any push, against the source-confirmed write schema
//      (45_DATA_field_schemas.json): required fields, enum values, effect tag literals, AI rule literals,
//      quest task vocabulary + flow graph (one start node, edges resolve, battle nodes have
//      failObjectiveId + opponentAIs, daily 3-7, raid rules). Failing rows go red with named fields and
//      the build aborts. Escape hatch: top-level "skipPreflight": true in the manifest.
// One manifest, mixed entities: jutsu, quest, asset (gameAsset), item, ai, aiProfile.
// Entry: {name, entity, slot:"create"|"convert"|"update", srcId?, targetId?, data}.
//   Cross-refs: any string value "@jutsu:<srcId>" or "@ai:<srcId>" resolves at run-time to the id that
//               entry produced (from the persisted idmap, keyed by srcId). Lets one ordered manifest do
//               the whole pyramid: jutsu create -> ai create (kits + rules pull @jutsu:) -> quest (@ai:).
//   Build order: jutsu-create, jutsu-convert, asset, item, ai, aiProfile, quest.
//   Images: a field value "@img:<filename>" pulls a URL the builder uploads itself. Tap the panel's
//           "Imgs" button and select the files once; on build each referenced file is uploaded to
//           uploadthing (POST /api/uploadthing?actionType=upload&slug=imageUploader, then PUT to the
//           signed ingest url) and its https://<app>.ufs.sh/f/<key> url is cached in the idmap under the
//           filename and written into the field (jutsu.image, ai avatar, quest sceneBackground, etc.).
//           Cached urls are reused on re-run; picked files live for the session only.
//   jutsu: create+fill, or convert-by-id. Convert FETCH-MERGES like the asset path: it loads the full
//          jutsu catalog once per run (jutsu.getAll, two passes - default + hidden:true so hidden AI
//          jutsu are included - mapped by id), merges your partial `data` over the live record, strips
//          the read-only `bloodline` join, preserves createdAt, then updates. So a partial convert
//          ({targetId, data:{description:"..."}}) is safe; full-record data still works.
//   quest: create (null) then update (auto flatten + referentialEqualities meta), or update-by-id.
//   asset: gameAsset.create (null) -> get the new row (falls back to a default row if get misses)
//          -> merge your data fields -> gameAsset.update. You supply the image URL (uploaded by hand).
//   item:  item.create ({type}) then item.update ({id,data}+Date meta, mirrors jutsu).
//          You supply the full item fields incl image URL. slot create=new, otherwise update targetId.
//   ai:    profile.create (null, slot create) -> profile.getAi(userId) -> merge your `data` fields over
//          the full live record (auto userId/id/isAi:true/isSummon:false) -> profile.updateAi (dynamic
//          Date meta). Armor is a manual editor step, not a payload field. If `data.rules` is present it
//          also pushes behavior (ai.updateAiProfile via the record's aiProfileId); rules+includeDefaultRules
//          are stripped from the AI record before saving. slot create=new user, else update targetId.
//   aiProfile: behavior-only push. targetId = ai userId (or @ai:<srcId>) -> getAi -> aiProfileId ->
//          ai.updateAiProfile with {rules, includeDefaultRules}. Use to (re)push rules to an existing AI.
// --- v4.19 (2026-08-26) ---------------------------------------------------
//  1. CAPTURE BLOCK. A manifest may carry:
//       "capture": { "before": [ {proc, input?, select?} ], "after": [ ... ] }
//     `before` runs ahead of the build (live records to merge against, current
//     name lists); `after` runs once the build finishes (verification, refreshed
//     lists). Results land in the results bundle under `captures`, each stamped
//     with the exact input it was called with and, for list procedures, an
//     explicit note that absence from a filtered call proves nothing. `select`
//     trims returned rows to named fields so a 1,490-row name list does not
//     bloat the bundle. Captures go through getRL, so they respect the limiter.
//     This retires the separate monitor-capture step for anything predictable.
//  2. READ-BACK. After a successful write, each entry is re-fetched and the
//     server's copy stored as `live` alongside `pushed`. Server-side
//     normalisation is otherwise invisible: scaleUserStats rewrites every AI
//     stat from level, so `pushed` never shows what the record actually holds.
//     Opt out with top-level "readBack": false.
(()=>{'use strict';if(window.__tnrBK)return;window.__tnrBK=1;
const MT={values:{"data.createdAt":["Date"],"data.updatedAt":["Date"]},v:1},now=()=>new Date().toISOString();
const THR=2000,sleep=m=>new Promise(r=>setTimeout(r,m));

// --- v4.20 generated config -----------------------------------------------
// 45c (constructors) and 32b (shared pool) are GENERATED from the TNR source by
// schema_extract.py. Hosting them beside this bundle means the browser preflight
// and the container-side validator read the SAME artifact, so the two cannot
// drift and both track source. Falls back to hand rules if the fetch fails; the
// panel title says which config is live.
const CFGBASE='https://raw.githubusercontent.com/perseverance484/tnr-tools/main/';
const CFGV='?v=1';
const CFG={ctors:null,pool:null,checks:null,nullOK:{},state:'loading'};
const loadCfg=async()=>{const grab=async n=>{try{const r=await fetch(CFGBASE+n+CFGV,{cache:'no-cache'});
  if(!r.ok)return null;return await r.json()}catch(e){return null}};
 const [c,p,k]=await Promise.all([grab('45c_DATA_constructors.json'),grab('32b_DATA_pool.json'),grab('45g_DATA_checks.json')]);
 CFG.ctors=c;CFG.pool=(p&&p.records)||null;CFG.checks=k;
 // law 72: a null is legal wherever the zod chain is .nullable()/.nullish().
 // Stripping those made the field impossible to CLEAR. The list is generated,
 // name-safe, and falls back to stripping everything if 45g is unreachable.
 CFG.nullOK={};if(k&&k.null_strip_exempt&&Array.isArray(k.null_strip_exempt.values))
  for(const f of k.null_strip_exempt.values)CFG.nullOK[f]=1;
 CFG.state=(c&&p&&k)?'generated':(c||p||k)?'partial':'fallback';
 CFG.byId={};if(CFG.pool)for(const k in CFG.pool){const r=Object.assign({code:k},CFG.pool[k]);CFG.pool[k]=r;CFG.byId[r.id]=r}
 return CFG};
// validate one tagged object against a generated constructor
const ctorBad=(obj,union,path)=>{const e=[];if(!CFG.ctors||!CFG.ctors.unions||!CFG.ctors.unions[union])return e;
 const members=CFG.ctors.unions[union];const key=obj&&obj.type;
 if(!key){e.push(path+': missing discriminant "type"');return e}
 const spec=members[key];
 if(!spec){e.push(path+': "'+key+'" is not a member of '+union);return e}
 for(const f in obj){const r=spec.fields[f];
  if(!r){e.push(path+'.'+f+': unknown field on '+key);continue}
  const v=obj[f];
  if(r.enum){const vals=Array.isArray(v)?v:[v];for(const one of vals)
   if(r.enum.indexOf(one)<0)e.push(path+'.'+f+'="'+one+'" not in enum')}
  if(typeof v==='number'){if(r.min!=null&&v<r.min)e.push(path+'.'+f+'='+v+' below min '+r.min);
   if(r.max!=null&&v>r.max)e.push(path+'.'+f+'='+v+' above max '+r.max)}}
 return e};
// pool codes -> ids, and distance gates derived from range+1
const POOLCODE=/^[A-Z]{1,2}\d{2}$/;
const resolvePool=d=>{if(!CFG.pool||!d)return 0;let n=0;
 if(Array.isArray(d.jutsus))d.jutsus=d.jutsus.map(j=>{if(typeof j==='string'&&POOLCODE.test(j)&&CFG.pool[j]){n++;return CFG.pool[j].id}return j});
 for(const r of (d.rules||[])){const a=r&&r.action;if(!a)continue;
  if(typeof a.jutsu==='string'&&POOLCODE.test(a.jutsu)&&CFG.pool[a.jutsu]){const rec=CFG.pool[a.jutsu];
   a.jutsuId=rec.id;delete a.jutsu;n++;
   if(rec.gate)for(const c of (r.conditions||[]))if(c&&c.type==='distance_lower_than'&&c.value==null)c.value=rec.gate}}
 return n};
const isLim=(s,t)=>s===429||/too fast|too many|rate limit|slow down|infraction/i.test(t||'');


// --- v4.18 node factory: author semantics, builder expands the payload ---
// A manifest may give a quest objective in short form:
//   {task,id,text,next,scene:{bg,chars},at:[sector,lon,lat],resetTo,fail,opponents:[ids],n}
// nodeExpand() fills every field the validator wants, using schema-derived defaults.
// Long-form objectives (with a 'description' key) pass through untouched.
const NF_REWARDS={"reward_hunter_items": false, "reward_hunter_items_ids": [], "reward_gathering_items": false, "reward_gathering_items_ids": [], "reward_seichi_silver": 0, "reward_money": 0, "reward_clanpoints": 0, "reward_anbupoints": 0, "reward_exp": 0, "reward_tokens": 0, "reward_prestige": 0, "reward_reputation": 0, "reward_skillpoints": 0, "reward_rank": "NONE", "reward_jutsus": [], "reward_bloodlines": [], "reward_badges": [], "reward_medical_experience": 0, "reward_hunting_experience": 0, "reward_crafting_experience": 0, "reward_gathering_experience": 0, "reward_war_damage": 0, "reward_war_healing": 0, "reward_items": [], "reward_village_membership": "NONE"};
const NF_BASE=(id,task,desc)=>Object.assign({},NF_REWARDS,{
  id:id,task:task,description:desc||'',successDescription:'',
  sceneBackground:'',sceneCharacters:[],attackers:[],image:''
});
const NF_LOC=at=>({sector:at[0],longitude:at[1],latitude:at[2],locationType:'specific',sectorType:'specific',sectorList:[]});
const nodeExpand=o=>{
  if(!o||typeof o!=='object')return o;
  if('description' in o&&!('text' in o))return o;            // already long form
  const t=o.task,n=NF_BASE(o.id,t,o.text);
  if(o.scene){n.sceneBackground=o.scene.bg||'';n.sceneCharacters=o.scene.chars||[]}
  if(o.rewards)Object.assign(n,o.rewards);
  if(t==='dialog'){
    n.nextObjectiveId=(o.next||[]).map(c=>Array.isArray(c)?{text:c[0],nextObjectiveId:c[1]}:c);
  }else if(t==='win_quest'||t==='fail_quest'){
    /* terminal: no nextObjectiveId key at all */
  }else if(t==='reset_quest'){
    if(o.resetTo)n.resetObjectiveId=o.resetTo;
  }else{
    if(o.next)n.nextObjectiveId=o.next;
  }
  if(o.at)Object.assign(n,NF_LOC(o.at));
  if(t==='collect_item'){n.collectItemIds=o.items||[];n.item_name=o.itemName||'Unknown';n.completed=0;n.hideLocation=!!o.hideLocation}
  if(t==='defeat_opponents'||t==='start_battle'){
    n.opponentAIs=(o.opponents||[]).map(x=>typeof x==='string'?{ids:[x],number:1,quantity:1}:x);
    if(o.fail)n.failObjectiveId=o.fail;
    n.opponent_scaled_to_user=!!o.scaled;n.completionOutcome=o.outcome||'Win';
    n.failDescription=o.failText||'You failed to defeat the opponent';
    n.fleeDescription=o.fleeText||'You fled from the opponent';
    n.drawDescription=o.drawText||'The battle ended in a draw';
    n.scaleGains=(o.scaleGains===undefined)?1:o.scaleGains;n.keepOriginalPools=!!o.keepPools;
  }
  if(o.n!==undefined)n.value=o.n;
  return n;
};
const questExpandContent=c=>{
  if(!c||!Array.isArray(c.objectives))return c;
  const out=Object.assign({},c);
  out.objectives=c.objectives.map(nodeExpand);
  return out;
};

// --- v4.18 write-shape normalizer: derived from validators via tnr_schema_extract.py ---
// Read records (harvests) are not write shapes. Three classes of drift break pushes:
//   1 booleans serialized/rebuilt as 0/1        2 optional fields sent as null (must be absent)
//   3 enum-string fields sent as 0/null         -> normalize every payload before it goes out.
const WS_BOOL=["attackers_scaled_to_user", "collected", "consecutiveObjectives", "delete_on_complete", "done", "hidden", "keepOriginalPools", "opponent_scaled_to_user", "recentlyDied", "reward_gathering_items", "reward_hunter_items", "singleBattle"];
const WS_OMIT_NULL=["failObjectiveId", "gatheringRank", "huntingRank", "id", "image", "latitude", "longitude", "maxLevel", "medicalRank", "nextObjectiveId", "prerequisiteQuestId", "questRank", "raidBossCurrentHealth", "raidBossMaxHealth", "requiredBloodlineId", "requiredLevel", "requiredVillage", "resetObjectiveId", "retryDelay", "sector", "selectedNextObjectiveId", "timestamp"];
const WS_ENUM_STR=["completionOutcome", "gatheringRank", "huntingRank", "locationType", "medicalRank", "questRank", "questType", "retryDelay", "reward_rank", "tagType", "task"];
const wsNorm=(v)=>{
  if(Array.isArray(v))return v.map(wsNorm);
  if(v&&typeof v==='object'){
    const o={};
    for(const k in v){
      let x=v[k];
      // absent != null (law 72) - but ONLY where the server rejects null.
      // CFG.nullOK is the generated exemption; without 45g we strip as before.
      if(x===null&&!CFG.nullOK[k]&&WS_OMIT_NULL.indexOf(k)>=0)continue;
      if(WS_BOOL.indexOf(k)>=0&&typeof x!=='boolean'){x=!!x&&x!==0}   // never coerce bools to 0
      // let the server default the enum - EXCEPT where null is the legitimate
      // way to clear a nullable enum (huntingRank, gatheringRank, medicalRank).
      // Without this the null guard above is undone one line later.
      if(WS_ENUM_STR.indexOf(k)>=0&&(x===null||x===0||x==='')&&!(x===null&&CFG.nullOK[k]))continue;
      o[k]=wsNorm(x);
    }
    return o;
  }
  return v;
};

const post=async(p,b)=>{b=wsNorm(b);const r=await fetch('/api/trpc/'+p+'?batch=1',{method:'POST',headers:{'content-type':'application/json'},credentials:'same-origin',body:JSON.stringify(b)});let t='';try{t=await r.text()}catch(e){}return{ok:r.ok,status:r.status,text:t}};
const postRL=async(p,b,wf)=>{let tr=0;while(1){const r=await post(p,b);if(isLim(r.status,r.text)){tr++;if(tr>8)return r;const w=Math.min(60000,5000*Math.pow(2,tr-1));wf&&wf(w,tr);await sleep(w);continue}return r}};
const rid=t=>(t.match(/"message":"([^"]+)"/)||[])[1],rerr=t=>{const m=t.match(/"message":"((?:[^"\\]|\\.)*)"/);return(m?m[1]:(t||'no body')).slice(0,1200)};
const getQ=async(p,inp)=>{const u='/api/trpc/'+p+'?batch=1&input='+encodeURIComponent(JSON.stringify({"0":{json:inp}}));const r=await fetch(u,{credentials:'same-origin'});let t='';try{t=await r.text()}catch(e){}return{ok:r.ok,status:r.status,text:t}};
const getRL=async(p,inp,wf)=>{let tr=0;while(1){const r=await getQ(p,inp);if(isLim(r.status,r.text)){tr++;if(tr>8)return r;const w=Math.min(60000,5000*Math.pow(2,tr-1));wf&&wf(w,tr);await sleep(w);continue}return r}};
const gjson=t=>{try{return JSON.parse(t)[0].result.data.json}catch(e){return null}};

// --- v4.19 capture engine -------------------------------------------------
// A manifest may carry a `capture` block. `before` runs ahead of the build
// (live records to merge against), `after` runs once the build finishes
// (verification, refreshed name lists). Every result is stamped with the exact
// input it was called with, because a filtered call's silence is not evidence
// of absence: a type-filtered gameAsset.getAllNames cannot see STATIC records
// no matter how many exist.
const capTrim=(d,sel)=>{if(!sel||!sel.length||!Array.isArray(d))return d;
 return d.map(r=>{if(!r||typeof r!=='object')return r;const o={};for(const k of sel)if(k in r)o[k]=r[k];return o})};
const runCapture=async(list,phase,wf,say)=>{const out=[];if(!Array.isArray(list)||!list.length)return out;
 for(let i=0;i<list.length;i++){const c=list[i]||{};const proc=c.proc||c.procedure;
  if(!proc){out.push({phase,proc:null,error:'entry has no proc'});continue}
  say&&say('capture '+phase+' '+(i+1)+'/'+list.length+': '+proc);
  let rec={phase,proc,input:(c.input===undefined?null:c.input),select:c.select||null,at:now()};
  try{const r=await getRL(proc,c.input||{},wf);rec.status=r.status;
   const d=gjson(r.text);
   rec.rows=Array.isArray(d)?d.length:(d&&typeof d==='object'?1:0);
   rec.data=capTrim(d,c.select);
   if(d===null)rec.error='no json payload (procedure name wrong, or not a query?)';
  }catch(e){rec.error=String((e&&e.message)||e)}
  // the load-bearing part: say plainly what a LIST call could not see. Only
  // list procedures can mislead by omission; a record fetch either found it or
  // did not.
  const isList=/getAll|\.list$|Names$/i.test(proc);
  if(!isList)rec.scope='record fetch';
  else if(rec.input&&typeof rec.input==='object'&&Object.keys(rec.input).length)
   rec.scope='FILTERED LIST: '+JSON.stringify(rec.input)+'. Absence from this result is NOT evidence a record does not exist; re-call with the type or filter you actually need.';
  else rec.scope='unfiltered list';
  out.push(rec);await sleep(THR)}
 return out};
// re-read a record after writing it, so the bundle carries what the SERVER holds
// rather than only what we sent. Server-side normalisation (scaleUserStats
// rewrites every AI stat from level) is invisible without this.
const LIVEGET={jutsu:'jutsu.get',item:'item.get',quest:'quests.get',asset:'gameAsset.get',bloodline:'bloodline.get'};
const readBack=async(r,wf)=>{try{const id=r.outId||r.targetId;if(!id)return null;
 if(r.entity==='ai'||r.entity==='aiProfile'){const F=await pgetAi(id,wf);return F||null}
 const proc=LIVEGET[r.entity];if(!proc)return null;return await sget(proc,id,wf)}catch(e){return null}};
const chk=r=>{if(!r.ok)return{ok:false,msg:'HTTP '+r.status+' '+rerr(r.text)};const j=gjson(r.text);if(j&&typeof j==='object'&&j.success===false)return{ok:false,msg:String(j.message||'success:false').slice(0,1200)};return{ok:true,msg:(j&&j.message)||''}};
const sget=async(proc,id,wf)=>{const r=await getRL(proc,{id},wf);const o=gjson(r.text);return(o&&o.id)?o:null};
// --- jutsu ---
const mk=wf=>postRL('jutsu.create',{"0":{json:null,meta:{values:["undefined"],v:1}}},wf);
const up=(id,d,wf)=>{const ca=d.createdAt||now();return postRL('jutsu.update',{"0":{json:{id,data:Object.assign({},d,{id,createdAt:ca,updatedAt:now()})},meta:MT}},wf)};
let jcat=null;const JLIM=100;// full-catalog cache for convert fetch-merge (loaded once per run)
const pageAll=async(extra,wf,map)=>{let cur=null,n=0;while(n<2000){n++;const r=await getRL('jutsu.getAll',Object.assign({cursor:cur,limit:JLIM,direction:'forward'},extra),wf);const p=gjson(r.text);if(!p||!p.data)break;for(const j of p.data)map[j.id]=j;if(p.nextCursor==null)break;cur=p.nextCursor;await sleep(THR)}return map};
const loadJutsu=async wf=>{const map={};await pageAll({},wf,map);await pageAll({hidden:true},wf,map);return map};
const ensureJcat=async wf=>{if(!jcat)jcat=await loadJutsu(wf);return jcat};
// --- item (mirrors jutsu; item.create takes {type}, NOT null) ---
const mki=(t,wf)=>postRL('item.create',{"0":{json:{type:t||"CONSUMABLE"}}},wf);
const upi=(id,d,wf)=>{const ca=d.createdAt||now();return postRL('item.update',{"0":{json:{id,data:Object.assign({},d,{id,createdAt:ca,updatedAt:now()})},meta:MT}},wf)};
// --- bloodline: create takes a null body; BloodlineValidator is an 11-field whole record (no id/createdAt/updatedAt) ---
const BLF=["name","image","description","rank","regenIncrease","statClassification","villageId","hidden","difficulty","traits","effects"];
const blcreate=wf=>postRL('bloodline.create',{"0":{json:null,meta:{values:["undefined"],v:1}}},wf);
const blupdate=(id,d,wf)=>{const data={};for(let i=0;i<BLF.length;i++){const k=BLF[i];if(d[k]!==undefined)data[k]=d[k]}return postRL('bloodline.update',{"0":{json:{id,data}}},wf)};
// --- ai (profile) : create -> getAi -> fetch-merge -> updateAi ; behavior via ai.updateAiProfile ---
const pcreate=wf=>postRL('profile.create',{"0":{json:null,meta:{values:["undefined"],v:1}}},wf);
const pgetAi=async(uid,wf)=>{const r=await getRL('profile.getAi',{userId:uid},wf);return gjson(r.text)};
const AIDATE=["data.joinedVillageAt","data.createdAt","data.updatedAt","data.questFinishAt","data.regenAt","data.immunityUntil","data.robImmunityUntil","data.bracketImmunityLiftedUntil","data.warParticipantUntil"];
const pupdateAi=(uid,data,wf)=>{const vals={};for(const p of AIDATE){if(data[p.slice(5)])vals[p]=["Date"]}return postRL('profile.updateAi',{"0":{json:{id:uid,data},meta:{values:vals,v:1}}},wf)};
const aiProfPush=(apid,rules,inc,wf)=>postRL('ai.updateAiProfile',{"0":{json:{id:apid,rules:rules||[],includeDefaultRules:inc!==false}}},wf);
const toggleAi=(uid,wf)=>postRL('ai.toggleAiProfile',{"0":{json:{aiId:uid}}},wf);
// --- image upload (uploadthing): presign -> HEAD -> PUT -> ufs.sh url ---
const UTID='ui0arpl8sm';// fallback app id for the final f/ url host
const utUpload=async(file,wf)=>{const meta={name:file.name,size:file.size,type:file.type||'application/octet-stream',lastModified:file.lastModified||Date.now()};let pr,tr=0,pt='';while(1){pr=await fetch('/api/uploadthing?actionType=upload&slug=imageUploader',{method:'POST',headers:{'content-type':'application/json'},credentials:'same-origin',body:JSON.stringify({files:[meta]})});pt='';try{pt=await pr.text()}catch(e){}if(isLim(pr.status,pt)){tr++;if(tr>8)break;const w=Math.min(60000,5000*Math.pow(2,tr-1));wf&&wf(w,tr);await sleep(w);continue}break}if(!pr.ok)throw new Error('presign '+pr.status+' '+pt.slice(0,140));let arr;try{arr=JSON.parse(pt)}catch(e){throw new Error('presign parse '+pt.slice(0,140))}const en=Array.isArray(arr)?arr[0]:arr;if(!en||!en.url||!en.key)throw new Error('presign no url/key');try{await fetch(en.url,{method:'HEAD'})}catch(e){}const fd=new FormData();fd.append('file',file,file.name);const pu=await fetch(en.url,{method:'PUT',body:fd});if(!pu.ok)throw new Error('put '+pu.status);let id=UTID;try{id=new URL(en.url).searchParams.get('x-ut-identifier')||UTID}catch(e){}return'https://'+id+'.ufs.sh/f/'+en.key};
const IMGRE=/^@img:(.+)$/;
const collectImgs=(o,set)=>{if(Array.isArray(o))o.forEach(x=>collectImgs(x,set));else if(o&&typeof o==='object'){for(const k in o)collectImgs(o[k],set)}else if(typeof o==='string'){const m=o.match(IMGRE);if(m)set.add(m[1])}};
// --- quest ---
const qcreate=wf=>postRL('quests.create',{"0":{json:null,meta:{values:["undefined"],v:1}}},wf);
const QRE={"data.sceneCharacters":["data.content.sceneCharacters"],"data.reward_jutsus":["data.content.reward.reward_jutsus"],"data.reward_badges":["data.content.reward.reward_badges"],"data.reward_items":["data.content.reward.reward_items"],"data.reward_hunter_items_ids":["data.content.reward.reward_hunter_items_ids"],"data.reward_gathering_items_ids":["data.content.reward.reward_gathering_items_ids"],"data.reward_bloodlines":["data.content.reward.reward_bloodlines"]};
const qupdate=(id,data,wf)=>{const d=JSON.parse(JSON.stringify(data));if(d.content)d.content=questExpandContent(d.content);d.id=id;d.createdAt=d.createdAt||now();d.updatedAt=now();const c=d.content||(d.content={});const rw=c.reward||(c.reward={});for(const k in rw)d[k]=rw[k];d.sceneBackground=(c.sceneBackground!==undefined)?c.sceneBackground:(d.sceneBackground||'');d.sceneCharacters=c.sceneCharacters||d.sceneCharacters||[];const meta={values:{"data.createdAt":["Date"],"data.updatedAt":["Date"]},referentialEqualities:QRE,v:1};return postRL('quests.update',{"0":{json:{id,data:d},meta}},wf)};
// --- asset (gameAsset) ---
const acreate=wf=>postRL('gameAsset.create',{"0":{json:null,meta:{values:["undefined"],v:1}}},wf);
const aget=async(id,wf)=>{let g=await getRL('gameAsset.get',{id},wf);let o=gjson(g.text);if(o&&o.id)return o;g=await getRL('gameAsset.get',id,wf);o=gjson(g.text);return(o&&o.id)?o:null};
const aupdate=(id,data,wf)=>postRL('gameAsset.update',{"0":{json:{id,data},meta:MT}},wf);
const DWEBP='https://uploadthing.b-cdn.net/f/630cf6e7-c152-4dea-a3ff-821de76d7f5a_default.webp';
const ADEF={type:"STATIC",image:DWEBP,url:DWEBP,frames:1,speed:1,hidden:true,folder:"",licenseDetails:"TNR",onInitialBattleField:false};
const cuid=()=>{try{return(window.Clerk&&Clerk.user&&Clerk.user.id)||''}catch(e){return''}};
const adefault=id=>{const o=Object.assign({id,name:'Placeholder',createdAt:now(),updatedAt:now()},ADEF);const u=cuid();if(u)o.createdByUserId=u;return o};
const MK='tnr_bk_idmap_v1',lm=()=>{try{return JSON.parse(localStorage.getItem(MK)||'{}')}catch(e){return{}}},sm=m=>{try{localStorage.setItem(MK,JSON.stringify(m))}catch(e){}};
let idmap=lm(),filemap={},imgsz={},rows=[],skipPF=false,dedupNames=false,$i,$l,$b,$s,$g,$r,$fi,$mf,$mi;
const dl=(n,s)=>{const b=new Blob([s],{type:'application/json'});const u=URL.createObjectURL(b);const a=document.createElement('a');a.href=u;a.download=n;document.body.appendChild(a);a.click();setTimeout(()=>{URL.revokeObjectURL(u);a.remove()},1500)};
// resolve @type:key tokens (e.g. @jutsu:water_lash, @ai:kaisei) to produced ids from idmap; returns a resolved copy
const RFX=/^@\w+:(.+)$/;
const resolveRefs=o=>{if(Array.isArray(o))return o.map(resolveRefs);if(o&&typeof o==='object'){const n={};for(const k in o)n[k]=resolveRefs(o[k]);return n}if(typeof o==='string'){const m=o.match(RFX);if(m&&idmap[m[1]])return idmap[m[1]]}return o};
const bdg=r=>r.entity==='bloodline'?('bloodline '+(r.slot==='create'?(idmap[r.key]?'reuse':'new'):'edit')):r.entity==='quest'?('quest '+(r.slot==='create'?'new':'edit')):r.entity==='asset'?('asset '+(r.slot==='create'?(idmap[r.key]?'reuse':'new'):'edit')):r.entity==='item'?('item '+(r.slot==='create'?(idmap[r.key]?'reuse':'new'):'edit')):r.entity==='ai'?('ai '+(r.slot==='create'?(idmap[r.key]?'reuse':'new'):'edit')+(r.data&&r.data.rules?'+rules':'')):r.entity==='aiProfile'?'ai-rules':(r.slot==='convert'?'convert':(idmap[r.key]?'reuse':'create'));
const prog=()=>{const d=rows.filter(r=>r.state==='ok').length,e=rows.filter(r=>r.state==='error').length;$b.style.width=Math.round(d/(rows.length||1)*100)+'%';$r.style.display=e?'':'none'};
const draw=()=>{$l.textContent='';for(const r of rows){const el=document.createElement('div');el.className='k-rw s-'+r.state;el.innerHTML='<i class="k-dt"></i><b class="k-nm"></b><u class="k-bg"></u><s class="k-st"></s>';el.querySelector('.k-nm').textContent=r.name;el.querySelector('.k-bg').textContent=bdg(r);el.querySelector('.k-st').textContent=r.detail||r.state;el.onclick=()=>{if(r.detail&&r.detail.length>26)alert(r.name+'\n\n'+r.detail)};r.el=el;$l.appendChild(el)}prog()};
const sr=(r,st,dt)=>{r.state=st;if(dt!==undefined)r.detail=dt;if(r.el){r.el.className='k-rw s-'+st;r.el.querySelector('.k-bg').textContent=bdg(r);r.el.querySelector('.k-st').textContent=r.detail||st}prog()};
let MANIFEST=null;
const parse=()=>{let m;try{m=JSON.parse($i.value)}catch(e){$s.textContent='❌ JSON: '+e.message;rows=[];$l.textContent='';$b.style.width='0%';return 0}const a=m.jutsu||m.items||[];const _cap=(m.capture&&[].concat(m.capture.before||[],m.capture.after||[]))||[];const _capbad=_cap.filter(c=>!c||typeof c!=='object'||!(c.proc||c.procedure));if(_capbad.length){$s.textContent='❌ capture: '+_capbad.length+" entr"+(_capbad.length>1?'ies':'y')+" missing 'proc'";rows=[];$l.textContent='';return 0}if(!a.length&&!_cap.length){$s.textContent='❌ no items';rows=[];$l.textContent='';return 0}if(!a.length){MANIFEST=m;imgsz=m.imgSizes||{};skipPF=!!m.skipPreflight;dedupNames=!!m.dedupNames;rows=[];$l.textContent='';$b.style.width='0%';$s.textContent='capture-only · '+_cap.length+' read'+(_cap.length>1?'s':'')+' · zero mutations';draw();return 1}MANIFEST=m;imgsz=m.imgSizes||{};skipPF=!!m.skipPreflight;dedupNames=!!m.dedupNames;rows=a.map(j=>({key:j.srcId,name:j.name,slot:j.slot,entity:j.entity||'jutsu',targetId:j.targetId,data:j.data,phase:(typeof j.phase==='number'?j.phase:undefined),state:'pending',detail:''}));const jc=rows.filter(r=>r.entity==='jutsu'&&r.slot==='create').length,jv=rows.filter(r=>r.entity==='jutsu'&&r.slot==='convert').length,as=rows.filter(r=>r.entity==='asset').length,it=rows.filter(r=>r.entity==='item').length,ai=rows.filter(r=>r.entity==='ai').length,ap=rows.filter(r=>r.entity==='aiProfile').length,q=rows.filter(r=>r.entity==='quest').length,bl=rows.filter(r=>r.entity==='bloodline').length;$s.textContent=rows.length+' entries · '+bl+' bloodline · '+jc+' jutsu-new · '+jv+' jutsu-edit · '+it+' item · '+as+' asset · '+ai+' ai · '+ap+' ai-rules · '+q+' quest';draw();return 1};
// --- preflight (v4.12): source-confirmed schema, mirrors 45_DATA_field_schemas.json ---
const EN={rank:["D","C","B","A","S","H"],urank:["STUDENT","GENIN","CHUNIN","JONIN","ELITE JONIN","ELDER","NONE"],wpn:["NONE","STAFF","AXE","FIST_WEAPON","SHURIKEN","SICKLE","DAGGER","SWORD","POLEARM","FLAIL","CHAIN","FAN","BOW","HAMMER"],jtype:["NORMAL","SPECIAL","BLOODLINE","FORBIDDEN","LOYALTY","CLAN","EVENT","AI"],stat:["Highest","Ninjutsu","Genjutsu","Taijutsu","Bukijutsu"],meth:["SINGLE","ALL","AOE_CIRCLE_SPAWN","AOE_LINE_SHOOT","AOE_WALL_SHOOT","AOE_LARGE_WALL_SHOOT","AOE_CIRCLE_SHOOT","AOE_SPIRAL_SHOOT"],tgt:["SELF","OTHER_USER","OPPONENT","ALLY","CHARACTER","GROUND","EMPTY_GROUND"],busage:["PVE","PVP","BOTH"],itype:["WEAPON","CONSUMABLE","ARMOR","ACCESSORY","MATERIAL","KEYSTONE","CRYSTAL","OTHER"],irar:["COMMON","RARE","EPIC","LEGENDARY"],islot:["HEAD","CHEST","LEGS","FEET","HAND","THROWN","ITEM","WAIST","KEYSTONE","NONE"],qtype:["starter","tier","daily","mission","errand","crime","exam","event","story","anbu","medical","hunting","gathering","battlepyramid","pvp","achievement","war","raid"],qdelay:["daily","weekly","monthly","none"],atype:["STATIC","ANIMATION","SCENE_BACKGROUND","SCENE_CHARACTER","SFX","MUSIC"],el:["Fire","Water","Wind","Earth","Lightning","Ice","Crystal","Dust","Shadow","Wood","Scorch","Storm","Magnet","Yin-Yang","Lava","Explosion","Light","Boil","Metal","Sand","None"]};
const TAGS="absorb afterburn barrier buffprevent cleanse cleanseprevent clear clearprevent clone copy damage debuffprevent decreasecooldown decreasedamagegiven decreasedamagetaken decreaseheal decreasemaxpools decreasepoolcost decreasestat drain elementalseal finalstand flee fleeprevent heal healprevent immunity increasecooldown increasedamagegiven increasedamagetaken increaseheal increasemaxpools increasepoolcost increaserange increasestat injectjutsus lifesteal marriageslotincrease mirror move moveprevent noncombatconsumereward noncombatgainskill noncombatincreasereskins onehitkill onehitkillprevent pierce poison recoil redirection reflect removebloodline repair rob robprevent rollbloodline seal sealprevent shield stealth stun stunprevent summon summonprevent timecompression timedilation unknown unlockitemvariant vamp visual weakness wound".split(" ");
const TASKS="pvp_kills arena_kills minutes_passed days_as_kage errands_total a_missions_total b_missions_total c_missions_total d_missions_total a_crimes_total b_crimes_total c_crimes_total d_crimes_total minutes_training stats_trained days_in_village jutsus_mastered user_level reputation_points random_encounter_wins spars_won medical_experience medical_experience_gained crafting_experience crafting_experience_gained hunting_experience hunting_experience_gained gathering_experience gathering_experience_gained move_to_location win_encounter_at_location collect_item deliver_item defeat_opponents fail_quest win_quest new_quest start_battle open_raid exclusive_raid reset_quest dialog".split(" ");
const CONDS="health_below specific_round round_greater_than round_lower_than distance_higher_than distance_lower_than does_not_have_summon has_effect target_has_effect".split(" ");
const ACTS="move_towards_opponent end_turn use_specific_jutsu use_specific_item use_random_jutsu use_random_item use_highest_power_action use_highest_power_jutsu use_highest_power_item use_combo_action".split(" ");
const AITGT="SELF CLOSEST_OPPONENT RANDOM_OPPONENT CLOSEST_ALLY RANDOM_ALLY BARRIER_BETWEEN BARRIER_BLOCKING_CLOSEST_OPPONENT EMPTY_GROUND_CLOSEST_TO_OPPONENT EMPTY_GROUND_CLOSEST_TO_SELF".split(" ");
const JENUM={jutsuWeapon:"wpn",jutsuType:"jtype",jutsuRank:"rank",requiredRank:"urank",method:"meth",target:"tgt",statClassification:"stat",battleUsageType:"busage"};
const IENUM={method:"meth",target:"tgt",itemType:"itype",weaponType:"wpn",rarity:"irar",slot:"islot",battleUsageType:"busage"};
const QENUM={questType:"qtype",questRank:"rank",retryDelay:"qdelay"};
const isRef=v=>typeof v==="string"&&/^@\w+:/.test(v);
const enumBad=(d,map)=>{const e=[];for(const f in map){const v=d[f];if(v==null||v===""||isRef(v))continue;if(EN[map[f]].indexOf(v)<0)e.push(f+"="+v)}return e};
const bnd=(d,f,lo,hi,e)=>{const v=d[f];if(typeof v==="number"&&(v<lo||v>hi))e.push(f+"="+v+" (allowed "+lo+"-"+hi+")")};
const fxBad=d=>{const e=[];(d.effects||[]).forEach((x,i)=>{if(x&&x.type&&TAGS.indexOf(x.type)<0)e.push("effects["+i+"].type="+x.type)});return e};
const fxRules=(d,entity)=>{const e=[],fx=d.effects;if(!Array.isArray(fx))return e;const has=t=>fx.some(x=>x&&x.type===t);const get=t=>fx.filter(x=>x&&x.type===t);
if(entity==="jutsu"){["rollbloodline","removebloodline","noncombatconsumereward"].forEach(t=>{if(has(t))e.push(t+" is forbidden on jutsu")})}
if(has("barrier"))get("barrier").forEach(x=>{if("staticAssetPath"in x&&!x.staticAssetPath)e.push("barrier needs staticAssetPath")});
if(has("wound")&&!has("damage")&&!has("pierce"))e.push("wound requires damage or pierce on the same action");
if(has("vamp")&&!has("damage")&&!has("pierce"))e.push("vamp requires damage or pierce on the same action");
["rollbloodline","removebloodline","noncombatconsumereward"].forEach(t=>get(t).forEach(x=>{if(x.powerPerLevel)e.push(t+" requires powerPerLevel 0")}));
get("clone").forEach(x=>{if(x.rounds===0)e.push("clone rounds must be >= 2")});
const tgt=d.target,rng=d.range,mth=d.method;
if(tgt==="SELF"&&typeof rng==="number"&&rng>0)e.push("target SELF requires range 0");
if(tgt!==undefined&&tgt!=="EMPTY_GROUND"&&!isRef(tgt)){["barrier","clone","summon","move"].forEach(t=>{if(has(t))e.push(t+" requires target EMPTY_GROUND")})}
if(has("damage")&&has("move")&&typeof mth==="string"&&!isRef(mth)&&mth.indexOf("AOE")<0)e.push("damage+move combo requires an AOE method");
if(entity==="item"){const c=d.cost,rc=d.repsCost,sc=d.seichiSilverCost;if(c!==undefined&&rc!==undefined&&sc!==undefined&&!(c>0||rc>0||sc>0))e.push("item needs cost, repsCost, or seichiSilverCost > 0");
if(d.itemType==="CONSUMABLE"&&d.destroyOnUse===false)e.push("CONSUMABLE requires destroyOnUse true");
const req=(t,rules)=>{if(!has(t))return;if(d.itemType!==undefined&&d.itemType!=="CONSUMABLE")e.push(t+" requires itemType CONSUMABLE");if(tgt!==undefined&&tgt!=="SELF")e.push(t+" requires target SELF");if(mth!==undefined&&mth!=="SINGLE")e.push(t+" requires method SINGLE");if(rules&&rules.destroy&&d.destroyOnUse===false)e.push(t+" requires destroyOnUse true");if(rules&&rules.pbu&&d.preventBattleUsage===false)e.push(t+" requires preventBattleUsage true")};
req("noncombatconsumereward");req("rollbloodline");req("removebloodline");req("unlockitemvariant",{destroy:1,pbu:1})}
return e};
const rulesBad=rl=>{const e=[];(rl||[]).forEach((ru,i)=>{if(!ru)return;const a=ru.action;if(a&&a.type&&ACTS.indexOf(a.type)<0)e.push("rule"+i+".action="+a.type);if(a&&a.target&&AITGT.indexOf(a.target)<0)e.push("rule"+i+".target="+a.target);(ru.conditions||[]).forEach((c,j)=>{if(c&&c.type&&CONDS.indexOf(c.type)<0)e.push("rule"+i+".cond"+j+"="+c.type);if(c&&c.target&&AITGT.indexOf(c.target)<0)e.push("rule"+i+".cond"+j+".target="+c.target)})});return e};
const jBnd=d=>{const e=[];bnd(d,"actionCostPerc",10,100,e);bnd(d,"range",0,5,e);bnd(d,"cooldown",0,300,e);bnd(d,"requiredLevel",1,100,e);return e};
const iBnd=d=>{const e=[];bnd(d,"actionCostPerc",1,100,e);bnd(d,"stackSize",1,999,e);bnd(d,"maxImbueNumber",1,3,e);bnd(d,"maxDurability",1,100,e);bnd(d,"range",0,10,e);bnd(d,"maxEquips",0,10,e);bnd(d,"cooldown",0,300,e);return e};
const qBad=d=>{const e=enumBad(d,QENUM);if(d.successDescription==="")e.push("successDescription empty");const obs=(d.content&&d.content.objectives)||[];if(!obs.length){e.push("no objectives");return e}
const ids={};obs.forEach(o=>{if(o&&o.id)ids[o.id]=1});const inc={};const edge=t=>{if(t)inc[t]=1};
for(const o of obs){if(!o)continue;const n=o.nextObjectiveId;if(typeof n==="string")edge(n);else if(Array.isArray(n))n.forEach(c=>c&&edge(c.nextObjectiveId));edge(o.failObjectiveId)}
for(const t in inc)if(!ids[t])e.push("edge to unknown id "+t);
const st=obs.filter(o=>o&&o.id&&!inc[o.id]);if(st.length!==1)e.push("start nodes="+st.length+(st.length?" ["+st.map(o=>o.id).join(",")+"]":""));
for(const o of obs){if(!o)continue;if(!o.id){e.push("objective missing id");continue}
if(o.task&&TASKS.indexOf(o.task)<0)e.push(o.id+": task="+o.task);
if((o.task==="start_battle"||o.task==="defeat_opponents")&&!o.failObjectiveId)e.push(o.id+": no failObjectiveId");
if((o.task==="start_battle"||o.task==="open_raid"||o.task==="exclusive_raid")&&!(o.opponentAIs&&o.opponentAIs.length))e.push(o.id+": empty opponentAIs")}
if(d.questType==="daily"&&(obs.length<3||obs.length>7))e.push("daily needs 3-7 objectives, has "+obs.length);
if(d.questType==="raid"){if(obs.length!==1)e.push("raid needs exactly 1 objective");if(!(d.raidBossMaxHealth>0))e.push("raidBossMaxHealth required >0");if(d.raidBossCurrentHealth==null)e.push("raidBossCurrentHealth required")}
return e};
const blBad=d=>{const e=[];["name","image","description","rank","regenIncrease","statClassification","villageId","effects"].forEach(k=>{if(d[k]===undefined)e.push("missing "+k)});
if(d.rank!=null&&!isRef(d.rank)&&EN.rank.indexOf(d.rank)<0)e.push("rank="+d.rank);
if(d.statClassification!=null&&!isRef(d.statClassification)&&EN.stat.indexOf(d.statClassification)<0)e.push("statClassification="+d.statClassification);
if(d.difficulty!=null&&["Easy","Medium","Hard","Expert"].indexOf(d.difficulty)<0)e.push("difficulty="+d.difficulty);
if(typeof d.traits==="string"&&d.traits.length>256)e.push("traits >256 chars");
bnd(d,"regenIncrease",0,100,e);return e.concat(fxBad(d))};
const aBad=d=>{const e=[];if(d.type&&EN.atype.indexOf(d.type)<0)e.push("type="+d.type);if(d.folder&&!/^[a-zA-Z0-9]*$/.test(d.folder))e.push("folder not alphanumeric");if(d.licenseDetails==="")e.push("licenseDetails empty");return e};
const aiBad=d=>{const e=[];if(d.primaryElement&&!isRef(d.primaryElement)&&EN.el.indexOf(d.primaryElement)<0)e.push("primaryElement="+d.primaryElement);if(d.secondaryElement&&!isRef(d.secondaryElement)&&EN.el.indexOf(d.secondaryElement)<0)e.push("secondaryElement="+d.secondaryElement);return[].concat(e,d.rules?rulesBad(d.rules):[],d.effects?fxBad(d):[])};
const PHR={bloodline:-2,jutsu:0,asset:2,item:3,ai:4,aiProfile:5,quest:6};const phr=r=>(typeof r.phase==='number')?r.phase:(r.entity==='jutsu'?(r.slot==='create'?0:1):(PHR[r.entity]!==undefined?PHR[r.entity]:9));
const collectRefs=(o,out)=>{if(Array.isArray(o))o.forEach(x=>collectRefs(x,out));else if(o&&typeof o==='object'){for(const k in o)collectRefs(o[k],out)}else if(typeof o==='string'){const m=o.match(/^@(jutsu|ai|scene|item|quest|bloodline):(.+)$/);if(m)out.push({pfx:m[1],key:m[2]})}};
const refBad=(r,L)=>{const e=[],refs=[];collectRefs(r.data,refs);if(typeof r.targetId==='string')collectRefs(r.targetId,refs);const my=phr(r),myIx=L.indexOf(r);for(const f of refs){if(idmap[f.key])continue;const src=L.find(x=>x.key===f.key);if(!src){e.push('@'+f.pfx+':'+f.key+' unknown (no srcId, not in idmap)');continue}const sp=phr(src);if(sp>my||(sp===my&&L.indexOf(src)>=myIx))e.push('@'+f.pfx+':'+f.key+' resolves after this entry (ordering)')}return e};
const VILL=["NONE","SHIROHANA","TSUKIMORI","HYORIN","AKASUMI","AKIKAZE","SHINE","GLACIER","SHROUD","CURRENT"];
const rwChk=(o,tag,e)=>{if(!o)return;if(typeof o.reward_village_membership==='string'&&o.reward_village_membership!==''&&!isRef(o.reward_village_membership)&&VILL.indexOf(o.reward_village_membership)<0)e.push(tag+' reward_village_membership='+o.reward_village_membership+' (village enum)');if(o.reward_village_membership==='')e.push(tag+' reward_village_membership empty string (use NONE)');if(o.reward_rank!=null&&typeof o.reward_rank!=='string')e.push(tag+' reward_rank not string');if(o.reward_village_membership!=null&&typeof o.reward_village_membership!=='string')e.push(tag+' reward_village_membership not string');if(o.reward_gathering_items!=null&&typeof o.reward_gathering_items!=='boolean')e.push(tag+' reward_gathering_items not boolean');if(o.reward_hunter_items!=null&&typeof o.reward_hunter_items!=='boolean')e.push(tag+' reward_hunter_items not boolean')};

// --- v4.15 lint (13_LINT_rules.json embedded; see stack file for the law references) ---
const LDECOR={appearSfx:1,disappearSfx:1,appearAnimation:1,disappearAnimation:1,staticAnimation:1,staticAssetPath:1,description:1,powerPerLevel:1,calculation:1,direction:1,target:1,statTypes:1,generalTypes:1,friendlyFire:1};
const LDIR={"redirection":["push","pull"],"increasestat":["offence","defence","both"],"decreasestat":["offence","defence","both"]};
const LCORE={damage:{allowBloodlineDamageDecrease:1,allowBloodlineDamageIncrease:1,dmgModifier:1,elements:1,residualModifier:1,timeTracker:1},pierce:{allowBloodlineDamageDecrease:1,allowBloodlineDamageIncrease:1,dmgModifier:1,elements:1,residualModifier:1,timeTracker:1},wound:{elements:1,timeTracker:1},increasedamagegiven:{elements:1,timeTracker:1},decreasedamagetaken:{elements:1,timeTracker:1},increasedamagetaken:{elements:1,timeTracker:1},increasestat:{elements:1,timeTracker:1},decreasestat:{elements:1,timeTracker:1},absorb:{elements:1,poolsAffected:1,timeTracker:1},reflect:{elements:1,timeTracker:1},shield:{health:1,timeTracker:1},heal:{poolsAffected:1,timeTracker:1},stun:{apReduction:1,timeTracker:1},seal:{timeTracker:1},moveprevent:{timeTracker:1},drain:{poolsAffected:1,timeTracker:1},decreaseheal:{timeTracker:1},increasecooldown:{actionsAffected:1,timeTracker:1},clear:{timeTracker:1},cleanse:{timeTracker:1},debuffprevent:{timeTracker:1},copy:{timeTracker:1},lifesteal:{elements:1,timeTracker:1}};
const LFORM={damage:1,pierce:1,wound:1},LPCT={increasedamagegiven:1,decreasedamagetaken:1,increasedamagetaken:1};
const lintRun=L=>{const B=[],W=[];const inj={};
for(const r of L){if(r.entity==='item')((r.data||{}).effects||[]).forEach(f=>{if(f&&f.type==='injectjutsus')JSON.stringify(f).replace(/@jutsu:([A-Za-z0-9_\-]+)/g,(_,s)=>{inj[s]=1;return _})})}
for(const r of L){const d=r.data||{},E=m=>B.push({r,m}),N=m=>W.push({r,m});
if((r.slot==='convert'||r.slot==='edit')&&(!r.targetId||typeof r.targetId!=='string'||r.targetId.charAt(0)==='@'))E('L01 convert/edit without literal targetId');
if(r.entity==='quest'){
 if(r.slot==='create'&&d.consecutiveObjectives!==true)E('L03 quest create needs consecutiveObjectives:true');
 for(const k of['startsAt','endsAt'])if(k in d&&d[k]&&!/^\d{4}-\d{1,2}-\d{1,2}$/.test(String(d[k])))E('L04 '+k+' must be plain YYYY-MM-DD');
 const obs=(d.content&&d.content.objectives)||[];if(obs.length){const ids={},edges={},inc={},wins=[];
  for(const o of obs){if(!o||!o.id)continue;ids[o.id]=1;const tg=[];const n=o.nextObjectiveId;
   if(typeof n==='string')tg.push(n);else if(Array.isArray(n))n.forEach(c=>c&&tg.push(c.nextObjectiveId));
   if(o.failObjectiveId)tg.push(o.failObjectiveId);edges[o.id]=tg.filter(Boolean);tg.forEach(x=>{if(x)inc[x]=1});
   if(o.task==='win_quest')wins.push(o.id);
   const dt=(o.description||'')+(Array.isArray(n)?n.map(c=>(c&&c.text)||'').join(' '):'');
   if(/[\u2013\u2014]/.test(dt))E('L11 em/en dash in dialog node '+o.id)}
  const first=obs.find(o=>o&&o.id);
  if(first){const seen={},sk=[first.id];while(sk.length){const u=sk.pop();if(seen[u])continue;seen[u]=1;(edges[u]||[]).forEach(x=>sk.push(x))}
   wins.forEach(w0=>{if(!seen[w0])E('L12b win node '+w0+' unreachable from the first objective')});
   for(const o of obs)if(o&&o.id&&!seen[o.id]&&o.id!==first.id)N('L12b orphan node '+o.id+' (unreachable)')}}}
if(r.entity==='ai'&&r.slot==='create')for(const k of['rank','regeneration','preferredStat','preferredGeneral1','preferredGeneral2'])if(!(k in d))E('L05 AI create missing '+k);
if(r.slot==='create'){const wrap=r.entity==='jutsu'&&r.key&&inj[r.key];
 if(wrap){if(d.hidden!==false)E('L13 injectjutsus wrapper must be hidden:false')}
 else if(d.hidden!==true)E('L13 create without hidden:true')}
if(r.entity==='jutsu'){if(d.cooldown!=null&&d.cooldown<3)E('L16 cooldown '+d.cooldown+' below floor 3');
 if(d.actionCostPerc!=null&&d.actionCostPerc>70)N('L10 EP '+d.actionCostPerc+' above signature ceiling 70')}
const pc={};
for(const f of(Array.isArray(d.effects)?d.effects:[])){if(!f||!f.type)continue;
 if(LFORM[f.type]&&(!Array.isArray(f.statTypes)||!f.statTypes.length||!Array.isArray(f.generalTypes)||!f.generalTypes.length))N('L06 '+f.type+' missing statTypes/generalTypes (generalTypes gap can explode damage)');
 if('direction'in f){const _ok=LDIR[f.type]||['offence','defence'];if(_ok.indexOf(f.direction)<0)E('L07 '+f.type+' direction "'+f.direction+'" (allowed: '+_ok.join('/')+')')}
 if(f.type==='stun'&&!('apReduction'in f))N('L15 stun without apReduction (defaults 10)');
 if(LCORE[f.type]){for(const k in f)if(k!=='type'&&k!=='power'&&k!=='rounds'&&!LDECOR[k]&&!LCORE[f.type][k])E('L09 '+f.type+' illegal field "'+k+'"')}
 if(LPCT[f.type]&&(f.calculation==='percentage'||!f.calculation))pc[f.type]=(pc[f.type]||0)+1;
 if(r.entity==='item'){if(f.type==='clear'||f.type==='copy')E('L18 item effect "'+f.type+'" excluded from item union');
  if(f.type==='noncombatconsumereward'&&d.target!=='SELF')E('L18 noncombatconsumereward requires item target SELF')}}
for(const tp in pc)if(pc[tp]>4){let p=1;for(const f of d.effects)if(f&&f.type===tp&&(f.calculation==='percentage'||!f.calculation))p*=(1+(f.power||0)/100);
 N('L08 '+pc[tp]+' '+tp+' rows: product x'+p.toFixed(1))}}
return{B,W}};

// laws 77/78: cross-field refines no schema expresses, so ctorBad cannot see
// them. A shape-valid effect array still 400s on these.
const RUNTIME_ONLY=()=>((CFG.checks&&CFG.checks.runtime_only_tags&&CFG.checks.runtime_only_tags.values)||['activatesagemode']);
const COMPANION=()=>((CFG.checks&&CFG.checks.companion_required&&CFG.checks.companion_required.values)||{consume:['damage','pierce'],vamp:['damage','pierce'],wound:['damage','pierce']});
const ENTONLY=()=>((CFG.checks&&CFG.checks.entity_only_tags&&CFG.checks.entity_only_tags.values)||{rollsagemode:'item',rollbloodline:'item',removebloodline:'item'});
const ZEROPPL=()=>((CFG.checks&&CFG.checks.zero_power_per_level&&CFG.checks.zero_power_per_level.values)||['rollsagemode','rollbloodline','removebloodline','noncombatconsumereward']);
const fxLaws=(d,ent)=>{const e=[];const fx=Array.isArray(d.effects)?d.effects:[];if(!fx.length)return e;
 const types=fx.map(f=>f&&f.type);const ro=RUNTIME_ONLY(),co=COMPANION(),eo=ENTONLY(),zp=ZEROPPL();
 for(const f of fx){if(!f||!f.type)continue;const t=f.type;
  if(ro.indexOf(t)>=0)e.push('law 77: "'+t+'" is runtime-only; the engine injects it in battle and every authored record carrying it is rejected');
  if(co[t]&&!co[t].some(x=>types.indexOf(x)>=0))e.push('law 78: "'+t+'" requires one of '+co[t].join('/')+' on the same action');
  if(eo[t]&&ent!==eo[t])e.push('law 78: "'+t+'" is '+eo[t]+'-only, not legal on '+ent);
  if(zp.indexOf(t)>=0&&f.powerPerLevel)e.push('law 78: powerPerLevel must be 0 for "'+t+'"');}
 return e};
// the inventory the container validator diffs against (--parity)
// 'nullable' and 'null_strip_exempt' are law 72 at two precisions: the
// container has entity context and uses the full nullability map, this side
// walks a context-free body and uses the name-safe subset. Both sides list
// both so the parity diff does not report a mismatch that is not one.
const BUILDER_CHECKS=['booleans','build_order','cap_100','null_strip_exempt','companion_required','date_fields','entity_only_tags','enums','formula_tags','hidden_on_create','nullable','required_on_create','runtime_only_tags','tag_power_max','terminal_actions','zero_power_per_level'];

const preflight=L=>{let bad=0;for(const r of L){const d=r.data||{};let e=[];
if(r.entity==="jutsu")e=[].concat(enumBad(d,JENUM),fxBad(d),jBnd(d),fxRules(d,"jutsu"));
else if(r.entity==="item")e=[].concat(enumBad(d,IENUM),fxBad(d),iBnd(d),fxRules(d,"item"));
else if(r.entity==="quest")e=qBad(d);
else if(r.entity==="asset")e=aBad(d);
else if(r.entity==="ai")e=aiBad(d);
else if(r.entity==="aiProfile")e=rulesBad(d.rules);
else if(r.entity==="bloodline")e=blBad(d);
if(CFG.ctors&&(r.entity==="ai"||r.entity==="aiProfile")&&Array.isArray(d.rules)){
 d.rules.forEach((ru,i)=>{if(!ru||typeof ru!=='object')return;
  if(!Array.isArray(ru.conditions))e.push('rules['+i+']: conditions must be an array (AiRule is {conditions:[],action:{}})');
  else ru.conditions.forEach((c,j)=>{e=e.concat(ctorBad(c,'ZodAllAiConditions','rules['+i+'].conditions['+j+']'))});
  if(ru.action)e=e.concat(ctorBad(ru.action,'ZodAllAiActions','rules['+i+'].action'));});}
if(CFG.ctors&&Array.isArray(d.effects))d.effects.forEach((fx,i)=>{e=e.concat(ctorBad(fx,'AllTags','effects['+i+']'))});
e=e.concat(fxLaws(d,r.entity));
if(r.entity==="quest"){rwChk(d.content&&d.content.reward,"reward",e);const _obs=(d.content&&d.content.objectives)||[];_obs.forEach(o=>o&&rwChk(o,o.id||"obj",e));if(d.hidden===false&&d.content){const mainSC=Array.isArray(d.content.sceneCharacters)&&d.content.sceneCharacters.length>0;const allSC=_obs.length>0&&_obs.every(o=>o&&Array.isArray(o.sceneCharacters)&&o.sceneCharacters.length>0);if(!mainSC&&!allSC)e.push("public quest (hidden:false) needs main sceneCharacters or sceneCharacters on every objective")}}
e=e.concat(refBad(r,L));
if(e.length){bad++;sr(r,"error","preflight: "+e.join("; ").slice(0,1200))}}
return bad};
const one=async r=>{const wf=(w,tr)=>sr(r,'running','⏳ limited '+(w/1000|0)+'s·try'+tr);
r.data=resolveRefs(r.data);if(r.targetId)r.targetId=resolveRefs(r.targetId);
if(r.data&&r.data.image==='')delete r.data.image;
const _un=(JSON.stringify(r.data)||'').match(/@(jutsu|ai|scene|item|quest|bloodline):[^"]{1,60}/);if(_un){sr(r,'error','unresolved ref '+_un[0]);return}
if(r.entity==='quest'){if(r.slot==='create'){sr(r,'running','creating quest…');let id=idmap[r.key];if(!id){const c=await qcreate(wf),kc=chk(c);id=rid(c.text);if(!kc.ok||!id){sr(r,'error','q.create '+(kc.ok?'no id in response':kc.msg));return}idmap[r.key]=id;sm(idmap);await sleep(THR)}sr(r,'running','merging defaults…');const live=await sget('quests.get',id,wf);let qd=r.data;if(live){delete live.expiresAt;qd=Object.assign({},live,r.data)}await sleep(THR);sr(r,'running','filling quest…');r.pushed=qd;r.outId=id;const u=await qupdate(id,qd,wf),ku=chk(u);ku.ok?sr(r,'ok','→ '+id+(live?'':' ⚠no defaults merged')):sr(r,'error','q.fill '+ku.msg)}else{sr(r,'running','merging live…');const live=await sget('quests.get',r.targetId,wf);let qd=r.data;if(live){delete live.expiresAt;qd=Object.assign({},live,r.data)}await sleep(THR);sr(r,'running','updating quest…');r.pushed=qd;r.outId=r.targetId;const u=await qupdate(r.targetId,qd,wf),ku=chk(u);ku.ok?sr(r,'ok','→ '+r.targetId+(live?'':' ⚠no live record')):sr(r,'error','q '+ku.msg)}return}
if(r.entity==='bloodline'){let id=r.targetId;if(r.slot==='create'){sr(r,'running','creating bloodline…');id=idmap[r.key];if(!id){const c=await blcreate(wf),kc=chk(c);id=rid(c.text);if(!kc.ok||!id){sr(r,'error','bl.create '+(kc.ok?'no id in response':kc.msg));return}idmap[r.key]=id;sm(idmap);await sleep(THR)}}else sr(r,'running','updating bloodline…');if(!id){sr(r,'error','bloodline needs targetId or slot create');return}sr(r,'running','merging live…');const live=await sget('bloodline.get',id,wf);let d=r.data;if(live)d=Object.assign({},live,r.data);await sleep(THR);r.pushed=d;r.outId=id;const u=await blupdate(id,d,wf),ku=chk(u);ku.ok?sr(r,'ok','→ '+id+(r.data&&r.data.rank?' rank '+r.data.rank:'')+(live?'':' ⚠no defaults merged')):sr(r,'error','bl.fill '+ku.msg);return}
if(r.entity==='asset'){let id=r.targetId;if(r.slot==='create'){sr(r,'running','creating asset…');id=idmap[r.key];if(!id){const c=await acreate(wf),kc=chk(c);id=rid(c.text);if(!kc.ok||!id){sr(r,'error','a.create '+(kc.ok?'no id in response':kc.msg));return}idmap[r.key]=id;sm(idmap)}}else sr(r,'running','updating asset…');let F=await aget(id,wf);if(!F)F=adefault(id);const data=Object.assign({},F,r.data,{id});r.pushed=data;r.outId=id;const u=await aupdate(id,data,wf),ku=chk(u);ku.ok?sr(r,'ok','→ '+id+' '+(data.type||'')):sr(r,'error','a.fill '+ku.msg);return}
if(r.entity==='item'){let id=r.targetId;if(r.slot==='create'){sr(r,'running','creating item…');id=idmap[r.key];if(!id){const c=await mki(r.data&&r.data.itemType,wf),kc=chk(c);id=rid(c.text);if(!kc.ok||!id){sr(r,'error','i.create '+(kc.ok?'no id in response':kc.msg));return}idmap[r.key]=id;sm(idmap);await sleep(THR)}}else sr(r,'running','updating item…');const live=await sget('item.get',id,wf);let d=r.data;if(live)d=Object.assign({},live,r.data);await sleep(THR);r.pushed=d;r.outId=id;const u=await upi(id,d,wf),ku=chk(u);ku.ok?sr(r,'ok','→ '+id+(r.data&&r.data.rarity?' '+r.data.rarity:'')+(live?'':' ⚠no defaults merged')):sr(r,'error','i.fill '+ku.msg);return}
if(r.entity==='ai'){let uid=r.targetId;if(r.slot==='create'){sr(r,'running','creating AI…');uid=idmap[r.key];if(!uid){const c=await pcreate(wf),kc=chk(c);uid=rid(c.text);if(!kc.ok||!uid){sr(r,'error','ai.create '+(kc.ok?'no id in response':kc.msg));return}idmap[r.key]=uid;sm(idmap);await sleep(THR)}}if(!uid){sr(r,'error','ai needs targetId or slot create');return}sr(r,'running','loading record…');const F=await pgetAi(uid,wf);if(!F){sr(r,'error','getAi failed '+uid);return}const af=Object.assign({},r.data);const rules=af.rules,inc=af.includeDefaultRules;delete af.rules;delete af.includeDefaultRules;const data=Object.assign({},F,af,{userId:uid,id:uid,isAi:true,isSummon:false});
if(Array.isArray(data.jutsus))data.jutsus=data.jutsus.map(j=>typeof j==='string'?j:(j&&(j.jutsuId||j.id))).filter(Boolean);
if(Array.isArray(data.items))data.items=data.items.map(t=>typeof t==='string'?{ids:[t],number:1}:(t&&t.ids?t:(t?{ids:[t.itemId||t.id].filter(Boolean),number:(t.number!=null?t.number:(t.quantity!=null?t.quantity:1))}:null))).filter(x=>x&&x.ids&&x.ids.length);
r.pushed=data;r.outId=uid;data.updatedAt=now();data.createdAt=data.createdAt||now();await sleep(THR);sr(r,'running','saving AI…');const u=await pupdateAi(uid,data,wf),ku=chk(u);if(!ku.ok){sr(r,'error','updateAi '+ku.msg);return}if(rules){let apid=F.aiProfileId;if(!apid){await sleep(THR);sr(r,'running','creating profile…');const tg=await toggleAi(uid,wf),kt=chk(tg);if(!kt.ok){sr(r,'error','→ '+uid+' toggle '+kt.msg);return}await sleep(THR);const F2=await pgetAi(uid,wf);apid=F2&&F2.aiProfileId}if(!apid){sr(r,'error','→ '+uid+' saved, no aiProfileId after toggle');return}await sleep(THR);sr(r,'running','pushing rules…');const rp=await aiProfPush(apid,rules,inc,wf),kr=chk(rp);kr.ok?sr(r,'ok','→ '+uid+' · rules '+rules.length):sr(r,'error','→ '+uid+' rules '+kr.msg);return}sr(r,'ok','→ '+uid);return}
if(r.entity==='aiProfile'){const uid=r.targetId;if(!uid){sr(r,'error','aiProfile needs targetId (ai userId or @ai:key)');return}sr(r,'running','resolving profile…');const F=await pgetAi(uid,wf);let apid=F&&F.aiProfileId;if(!apid){await sleep(THR);const tg=await toggleAi(uid,wf),kt=chk(tg);if(!kt.ok){sr(r,'error','toggle '+kt.msg);return}await sleep(THR);const F2=await pgetAi(uid,wf);apid=F2&&F2.aiProfileId}if(!apid){sr(r,'error','no aiProfileId for '+uid+' after toggle');return}await sleep(THR);sr(r,'running','pushing rules…');const rp=await aiProfPush(apid,r.data&&r.data.rules,r.data&&r.data.includeDefaultRules,wf),kr=chk(rp);kr.ok?sr(r,'ok','→ '+apid+' · rules '+((r.data&&r.data.rules||[]).length)):sr(r,'error','aiProfile '+kr.msg);return}
if(r.slot==='create'){sr(r,'running','creating…');let id=idmap[r.key];if(!id){const c=await mk(wf),kc=chk(c);id=rid(c.text);if(!kc.ok||!id){sr(r,'error','create '+(kc.ok?'no id in response':kc.msg));return}idmap[r.key]=id;sm(idmap);await sleep(THR)}sr(r,'running','merging defaults…');const live=await sget('jutsu.get',id,wf);let d=r.data;if(live){d=Object.assign({},live,r.data);delete d.bloodline}await sleep(THR);sr(r,'running','filling…');r.pushed=d;r.outId=id;const u=await up(id,d,wf),ku=chk(u);ku.ok?sr(r,'ok','→ '+id+(live?'':' ⚠no defaults merged')):sr(r,'error','fill '+ku.msg)}else{sr(r,'running','loading record…');const live=await sget('jutsu.get',r.targetId,wf);let d;if(live){d=JSON.parse(JSON.stringify(Object.assign({},live,r.data)));d.id=r.targetId;delete d.bloodline}else{d=JSON.parse(JSON.stringify(r.data));d.id=r.targetId}for(const e of d.effects||[])if(e.type==='injectjutsus')e.jutsuIds=(e.jutsuIds||[]).map(s=>idmap[s]||s);sr(r,'running','converting…');r.pushed=d;r.outId=r.targetId;const u=await up(r.targetId,d,wf),ku=chk(u);const j=(d.effects||[]).find(e=>e.type==='injectjutsus')||{};const nl=live?'':' ⚠no live record';ku.ok?sr(r,'ok','→ '+r.targetId+(j.jutsuIds?' · inj '+j.jutsuIds.length:'')+nl+' ⚠re-equip if AI-equipped'):sr(r,'error',ku.msg)}};
const build=async sub=>{const L=sub||rows;if(!sub)jcat=null;$g.disabled=$r.disabled=1;if(!skipPF){const pb=preflight(L);if(pb){$s.textContent='❌ preflight: '+pb+' entr'+(pb>1?'ies':'y')+' invalid, tap red rows. "skipPreflight":true bypasses.';$g.disabled=$r.disabled=0;return}
const lt=lintRun(L);for(const w of lt.W)sr(w.r,'pending',((w.r.detail?w.r.detail+' · ':'')+'⚠ '+w.m).slice(0,300));
if(lt.B.length){for(const b of lt.B)sr(b.r,'error','lint: '+b.m);$s.textContent='❌ lint: '+lt.B.length+' block'+(lt.B.length>1?'s':'')+' (13_LINT). Fix or "skipPreflight":true.';$g.disabled=$r.disabled=0;return}
const need=[];JSON.stringify(L).replace(/@img:([A-Za-z0-9_.\-]+)/g,(_,f)=>{if(!(f in imgsz))need.push(f);return _});
if(need.length){for(const r of L)sr(r,'pending',r.detail);$s.textContent='❌ lint L17: @img without imgSizes byte entry: '+need.slice(0,4).join(', ')+(need.length>4?' +'+(need.length-4):'');$g.disabled=$r.disabled=0;return}}const uwf=(w,tr)=>{$s.textContent='⏳ upload limited '+((w/1000)|0)+'s try'+tr};
window.__tnrCapBefore=[];
{const cb=(MANIFEST&&MANIFEST.capture&&MANIFEST.capture.before)||null;
 if(cb&&cb.length){try{window.__tnrCapBefore=await runCapture(cb,'before',null,t=>{$s.textContent=t})}catch(e){window.__tnrCapBefore=[{phase:'before',proc:null,error:'capture phase threw: '+String((e&&e.message)||e)}]}}}
if(dedupNames&&!sub){const creates=L.filter(r=>r.slot==='create'&&!idmap[r.key]);const byEnt={};for(const r of creates){(byEnt[r.entity]=byEnt[r.entity]||[]).push(r)}
const nameList=async proc=>{const s=new Set();const r0=await getRL(proc,null,uwf);const p=gjson(r0.text);(Array.isArray(p)?p:(p&&p.data)||[]).forEach(x=>{const v=x&&(x.name||x.username);if(v)s.add(String(v).trim().toLowerCase())});return s};
if(CFG.state==='loading'){$s.textContent='loading generated config…';await loadCfg()}
{let nres=0;for(const r of rows)if(r.entity==='ai'||r.entity==='aiProfile')nres+=resolvePool(r.data);
 if(nres)$s.textContent='resolved '+nres+' pool code(s) to ids and gates';
 // a leftover pool code would be pushed as a literal string and SILENTLY STRIPPED
 // server-side (law 17), leaving the AI with no kit and a green row. Block instead.
 const stuck=[];for(const r of rows){const d=r.data||{};
  for(const j of (d.jutsus||[]))if(typeof j==='string'&&POOLCODE.test(j))stuck.push(r.name+': '+j);
  for(const ru of (d.rules||[]))if(ru&&ru.action&&typeof ru.action.jutsu==='string')stuck.push(r.name+': '+ru.action.jutsu);}
 if(stuck.length){$s.textContent='❌ unresolved pool code(s), config is '+CFG.state+': '+stuck.slice(0,4).join(', ');
  $g.disabled=$r.disabled=0;return}}
let dwarn=0;const NPROC={jutsu:'jutsu.getAllNames',item:'item.getAllNames',asset:'gameAsset.getAllNames',ai:'profile.getAllAiNames',quest:'quests.getAllNames'};for(const ent in byEnt){if(ent==='aiProfile'||!NPROC[ent])continue;$s.textContent='dedup: live '+ent+' names…';let s=new Set();try{s=await nameList(NPROC[ent])}catch(e){}
if(!s.size){for(const r of byEnt[ent])if(r.state==='pending')sr(r,'pending','⚠dedup skipped (fetch failed)');continue}
for(const r of byEnt[ent]){const nm=(r.data&&(r.data.name||r.data.username))||'';if(nm&&s.has(String(nm).trim().toLowerCase())){dwarn++;sr(r,'error','LIVE NAME COLLISION: '+nm)}}}
if(dwarn){$s.textContent='❌ dedup: '+dwarn+' live name collision(s), rename before pushing';$g.disabled=$r.disabled=0;return}}const imgset=new Set();for(const r of L)collectImgs(r.data,imgset);const bySize={};for(const k in filemap){const _f=filemap[k];if(!bySize[_f.size])bySize[_f.size]=_f}const pick=n=>filemap[n]||(imgsz[n]?bySize[imgsz[n]]:null)||null;const needimg=[...imgset].filter(n=>!idmap[n]);if(needimg.length){const miss=needimg.filter(n=>!pick(n));if(miss.length){$s.textContent='❌ pick these first (🖼 Imgs): '+miss.join(', ');$g.disabled=$r.disabled=0;return}for(let i=0;i<needimg.length;i++){const n=needimg[i];$s.textContent='uploading '+(i+1)+'/'+needimg.length+': '+n;try{const url=await utUpload(pick(n),uwf);idmap[n]=url;sm(idmap)}catch(e){$s.textContent='❌ upload '+n+': '+((e&&e.message)||e);$g.disabled=$r.disabled=0;return}await sleep(THR)}}const PLBL={bloodline:'bloodlines',asset:'assets',item:'items',ai:'AIs',aiProfile:'AI rules',quest:'quests'};const ord=L.map((r,i)=>({r,i,p:phr(r)})).sort((a,b)=>(a.p-b.p)||(a.i-b.i));let curp=null;for(let i=0;i<ord.length;i++){const r=ord[i].r;if(ord[i].p!==curp){curp=ord[i].p;$s.textContent=(r.entity==='jutsu'?(r.slot==='create'?'jutsu creates':'jutsu edits'):(PLBL[r.entity]||r.entity))+'…'}await one(r);await sleep(THR)}const e=rows.filter(r=>r.state==='error').length;$s.textContent=e?('⚠ '+e+' error(s), tap a red row or Retry failed'):('✅ all '+rows.length+' done');
const CAPA=(MANIFEST&&MANIFEST.capture&&MANIFEST.capture.after)||null;
let capsAfter=[];const capSay=t=>{$s.textContent=t};
if(CAPA&&CAPA.length){try{capsAfter=await runCapture(CAPA,'after',null,capSay)}catch(_e){}}
const wantLive=!(MANIFEST&&MANIFEST.readBack===false);
if(wantLive){for(let i=0;i<rows.length;i++){const r=rows[i];if(r.state!=='ok')continue;
 $s.textContent='reading back '+(i+1)+'/'+rows.length+': '+r.name;
 r.live=await readBack(r,null);await sleep(THR)}}
try{const bundle={builder:'v4.23',at:now(),checks:BUILDER_CHECKS,cfg:CFG.state,entries:rows.map(r=>({name:r.name,srcId:r.key||null,entity:r.entity,slot:r.slot,state:r.state,detail:r.detail||'',id:r.outId||idmap[r.key]||r.targetId||null,pushed:r.pushed||null,live:r.live||null})),captures:(window.__tnrCapBefore||[]).concat(capsAfter),idmap};dl('tnr_results_'+Date.now()+'.json',JSON.stringify(bundle,null,1))}catch(_e){}
$g.disabled=$r.disabled=0;ac()};
const lt=()=>rows.map(r=>(r.state==='ok'?'ok  ':r.state==='error'?'ERR ':'-   ')+r.name+'  '+(r.detail||r.state)).join('\n')+'\n\nID MAP:\n'+JSON.stringify(idmap,null,1);
const cp=()=>{const t=document.createElement('textarea');t.value=lt();t.style.cssText='position:fixed;left:-9999px';document.body.appendChild(t);t.focus();t.select();let o=0;try{o=document.execCommand('copy')}catch(e){}if(!o)try{navigator.clipboard&&navigator.clipboard.writeText(t.value)}catch(e){}t.remove()};
const ac=()=>{try{navigator.clipboard&&navigator.clipboard.writeText(lt())}catch(e){}};

// --- v4.20 doctor: live checks the container cannot do --------------------
const doctor=async(say)=>{const out=[];
 if(CFG.state==='loading'){say('loading config…');await loadCfg()}
 out.push('config: '+CFG.state+(CFG.ctors?(' · '+Object.keys(CFG.ctors.unions||{}).length+' unions'):'')+(CFG.pool?(' · '+Object.keys(CFG.pool).length+' pool records'):''));
 const NP={jutsu:'jutsu.getAllNames',item:'item.getAllNames',asset:'gameAsset.getAllNames',ai:'profile.getAllAiNames',quest:'quests.getAllNames'};
 for(const ent in NP){say('doctor: '+ent+' names…');
  let rowsN=null;try{const r=await getRL(NP[ent],ent==='asset'?{folderPrefix:true}:{},null);rowsN=gjson(r.text)}catch(e){}
  if(!Array.isArray(rowsN)){out.push(ent+': name list unavailable');await sleep(THR);continue}
  const seen={},dupes=[],shells=[];
  for(const x of rowsN){const nm=String(x.name||x.username||'').trim();
   if(!nm){shells.push(x.id);continue}
   const k=nm.toLowerCase();if(seen[k])dupes.push(nm);else seen[k]=1;
   if(/^New Jutsu - |^New /i.test(nm))shells.push(nm)}
  out.push(ent+': '+rowsN.length+' records'+(dupes.length?(' · '+dupes.length+' DUPLICATE name(s): '+dupes.slice(0,4).join(', ')):'')+(shells.length?(' · '+shells.length+' blank shell(s)'):''));
  await sleep(THR)}
 // manifest targets that no longer resolve
 if(MANIFEST&&Array.isArray(MANIFEST.items)){const tg=MANIFEST.items.filter(x=>x.targetId&&!/^@/.test(x.targetId));
  if(tg.length){say('doctor: checking '+tg.length+' target id(s)…');let gone=0;
   for(const x of tg){const p={jutsu:'jutsu.get',item:'item.get',quest:'quests.get',asset:'gameAsset.get'}[x.entity];
    if(!p)continue;const live=await sget(p,x.targetId,null);if(!live)gone++;await sleep(THR)}
   out.push('manifest targets: '+tg.length+' checked, '+gone+' no longer resolve')}}
 return out};
const CSS='.k-fab{position:fixed;bottom:12px;left:12px;z-index:2147483000;background:#1f7c3b;color:#fff;border:0;border-radius:10px;padding:11px 16px;font:600 14px system-ui;box-shadow:0 4px 16px #0008}.k-pn{position:fixed;left:8px;right:8px;bottom:8px;z-index:2147483000;display:none;flex-direction:column;max-height:88vh;background:#16171b;color:#e8e8ea;border:1px solid #3a3b44;border-radius:14px;box-shadow:0 12px 44px #000a;font:13px system-ui;overflow:hidden}.k-hd{display:flex;align-items:center;gap:8px;padding:11px 12px;background:#202128;border-bottom:1px solid #34353d}.k-ti{flex:1;font-weight:700;font-size:15px}.k-ic{background:#34353d;color:#e8e8ea;border:0;border-radius:8px;padding:7px 12px;font-size:15px}.k-bw{height:4px;background:#2a2b32}.k-bar{height:100%;width:0;background:#2ec26a}.k-bd{padding:11px 12px;overflow:auto;overscroll-behavior:contain}.k-in{width:100%;box-sizing:border-box;height:13vh;min-height:64px;background:#0e0f12;color:#cde6ff;border:1px solid #34353d;border-radius:8px;padding:8px;font:12px monospace}.k-st2{margin:9px 2px;font-size:12px;min-height:16px}.k-ls{display:flex;flex-direction:column;gap:5px}.k-rw{display:flex;align-items:center;gap:8px;padding:9px 10px;background:#1b1c22;border:1px solid #2a2b33;border-radius:8px}.k-dt{width:9px;height:9px;border-radius:50%;background:#6b6c74;flex:none}.k-nm{flex:1;font:600 12px system-ui;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.k-bg{font-size:10px;padding:2px 8px;border-radius:999px;background:#33343d;flex:none;font-style:normal}.k-st{font-size:11px;opacity:.85;max-width:42%;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;flex:none;text-decoration:none}.s-running .k-dt{background:#e6b800}.s-ok .k-dt{background:#2ec26a}.s-error .k-dt{background:#ec5b5b}.s-error{border-color:#5a2a2a}.k-ft{display:flex;gap:8px;padding:10px 12px;background:#1b1c22;border-top:1px solid #34353d;flex-wrap:wrap}.k-bt{flex:1;min-width:92px;border:0;border-radius:9px;padding:12px;font:600 13px system-ui;color:#fff}.k-go{background:#1f7c3b}.k-rt{background:#8a5a00;display:none}.k-cp{background:#2b4d70}.k-rs{background:#5a2a2a}.k-im{background:#5a3a7a}.k-dc{background:#2b6f6f}';
const H=document.createElement('div');H.id='tnr-bk-host';const R=H.attachShadow({mode:'open'});
R.innerHTML='<style>'+CSS+'</style><button class="k-fab">▶ Build</button><div class="k-pn"><div class="k-hd"><span class="k-ti">Content builder v4.22</span><button class="k-ic k-min">▾</button></div><div class="k-bw"><div class="k-bar"></div></div><div class="k-bd"><textarea class="k-in" placeholder="paste a manifest or 📄 Load a JSON file"></textarea><div class="k-st2">paste a manifest to preview</div><div class="k-ls"></div></div><div class="k-ft"><button class="k-bt k-go">▶ Build</button><button class="k-bt k-lm">📄 Load</button><button class="k-bt k-im">🖼 Imgs</button><button class="k-bt k-rt">↻ Retry failed</button><button class="k-bt k-dc">🩺 Doctor</button><button class="k-bt k-cp">⧉ Copy</button><button class="k-bt k-me">🗺 Map</button><button class="k-bt k-mi">⤒ Map</button><button class="k-bt k-rs">⌫ Reset</button><input class="k-fi" type="file" multiple hidden><input class="k-mf" type="file" accept=".json,application/json" hidden><input class="k-mi2" type="file" accept=".json,application/json" hidden></div></div>';
document.body.appendChild(H);const q=s=>R.querySelector(s),pn=q('.k-pn'),fb=q('.k-fab');
loadCfg().then(()=>{try{q('.k-ti').textContent='Content builder v4.22 · cfg '+CFG.state}catch(e){}});
$i=q('.k-in');$l=q('.k-ls');$b=q('.k-bar');$s=q('.k-st2');$g=q('.k-go');$r=q('.k-rt');
const sh=v=>{pn.style.display=v?'flex':'none';fb.style.display=v?'none':'block'};
fb.onclick=()=>sh(1);q('.k-min').onclick=()=>sh(0);$i.addEventListener('input',parse);
$g.onclick=()=>{if(parse())build()};$r.onclick=()=>build(rows.filter(r=>r.state==='error'));
q('.k-dc').onclick=async()=>{const b=q('.k-dc');b.disabled=1;try{const lines=await doctor(t=>{$s.textContent=t});$s.textContent='🩺 doctor done';alert('DOCTOR\n\n'+lines.join('\n\n'))}catch(e){$s.textContent='doctor: '+((e&&e.message)||e)}b.disabled=0};
q('.k-cp').onclick=()=>{cp();$s.textContent='📋 copied'};
q('.k-rs').onclick=()=>{if(confirm('Clear remembered ids? Next build creates fresh records.')){idmap={};sm(idmap);jcat=null;draw();$s.textContent='memory cleared'}};
$mf=q('.k-mf');q('.k-lm').onclick=()=>$mf.click();$mf.addEventListener('change',()=>{const f=$mf.files[0];if(!f)return;const rd=new FileReader();rd.onload=()=>{$i.value=String(rd.result||'');parse();$s.textContent=(($s.textContent||'')+' · loaded '+f.name).slice(0,120)};rd.readAsText(f)});
q('.k-me').onclick=()=>{dl('tnr_idmap_'+Date.now()+'.json',JSON.stringify(idmap,null,1));$s.textContent='🗺 idmap exported ('+Object.keys(idmap).length+' keys)'};
$mi=q('.k-mi2');q('.k-mi').onclick=()=>$mi.click();$mi.addEventListener('change',()=>{const f=$mi.files[0];if(!f)return;const rd=new FileReader();rd.onload=()=>{try{const m=JSON.parse(String(rd.result||'{}'));const n=Object.keys(m).length;if(confirm('Merge '+n+' idmap key(s) into memory?')){Object.assign(idmap,m);sm(idmap);$s.textContent='⤒ merged '+n+' key(s), idmap now '+Object.keys(idmap).length}}catch(e){$s.textContent='❌ idmap import: '+e.message}};rd.readAsText(f)});
$fi=q('.k-fi');q('.k-im').onclick=()=>$fi.click();$fi.addEventListener('change',()=>{for(const f of $fi.files)filemap[f.name]=f;$s.textContent=Object.keys(filemap).length+' image(s) loaded: '+Object.keys(filemap).join(', ').slice(0,70)});
new MutationObserver(()=>{if(!document.getElementById('tnr-bk-host'))document.body.appendChild(H)}).observe(document.body,{childList:1});
})();
