import { assertBloodrightAvailable } from "../src/bloodright/jobs.mjs";
import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { compileBloodright, prepareBloodright, scopeKey } from "../src/bloodright/compiler.mjs";
import { CONTRACT, bloodrightProblems } from "../src/bloodright/validate.mjs";
import { parseManifest, planOrder } from "../src/runner/manifest.mjs";
import { readIdmap } from "../src/storage/compat.mjs";
import { ForgeCore } from "../src/core/core.mjs";
import { composeForTest } from "./compose.mjs";
import { BloodrightGame } from "./bloodright.game.mjs";
const design = JSON.parse(readFileSync(new URL("../../docs/design/bloodright/examples/blood_enchanted_eyes_structural.json", import.meta.url)));
const BL = design.bloodline.id, HP = "HWq7986PPhl5emkAM3L4a", FOLDER = "kvxMu9ntHbNcD6FFHKGo3";
const clone = v => structuredClone(v);
function config() { return { version: 1, source: { path: "docs/design/bloodright/examples/blood_enchanted_eyes_structural.json", ref: "5963810895aae4e2deaa61b72424c203752f50c1" }, hiddenProbeId: HP, bindings: { folderId: FOLDER, nodes: { p2_t1: HP } }, nodes: Object.fromEntries(design.nodes.map(n => [n.id, { seichiSilverCost: 20, rounds: 99 }])) }; }
// 20/99 for all nodes is TEST DATA, not the pilot pricing decision.
function setup() {
  const game = new BloodrightGame();
  game.folders.set(FOLDER, { id: FOLDER, name: "Blood-Enchanted Eyes", image: "", description: null, order: 120, hidden: false });
  game.skills.set(HP, { id: HP, name: "Hungry Pulse", image: "https://example.test/keep.webp", description: "New skill description", target: "SELF", tier: 1, requiredSkillIds: [], costSkillPoints: 1, pathType: "BLOODRIGHT", bloodlineId: BL, seichiSilverCost: 20, hidden: true, skillType: "DEFAULT", folderId: FOLDER, effects: [] });
  const d = composeForTest({ game });
  d.github.text = async () => JSON.stringify(design);
  return d;
}
const compile = (d, cfg = config(), tree = design) => compileBloodright({ design: tree, config: cfg, skills: [...d.game.skills.values()], folders: [...d.game.folders.values()], idmap: readIdmap(d.storage) });
const mutations = d => d.game.calls.filter(c => /skillTree\.(create|update)/.test(c.path));

test("scoped contract keeps spread elements, exact pin and procedure kinds", () => {
  assert.equal(CONTRACT._meta.pin, "1ccdaf078a58101872675e459c8e755b495d4c83");
  for (const e of ["Fire", "Shadow", "Yin-Yang", "None"]) assert.ok(CONTRACT.elements.includes(e));
  assert.equal(CONTRACT.procedures["skillTree.create"].kind, "mutation");
  assert.equal(CONTRACT.procedures["skillTree.getAll"].mcp, true);
});

test("BEE compiler: 12 nodes, 106 legal allocations, one Advanced Art; Hungry Pulse is an edit", () => {
  const d = setup(), r = compile(d);
  assert.deepEqual(r.problems, []); assert.equal(r.allocations, 106); assert.equal(r.maxAdvanced, 1);
  assert.equal(r.manifest.items.length, 13);
  const hp = r.manifest.items.find(it => it.targetId === HP);
  assert.equal(hp.slot, "edit"); assert.equal(hp.data.image, "https://example.test/keep.webp");
  assert.equal(hp.data.effects[0].affectedTag, "lifesteal"); assert.equal(hp.data.effects[0].target, "INHERIT");
  assert.deepEqual(hp.data.effects[0].affectedElements, ["Shadow"]);
  assert.equal(hp.data.effects[0].power, 2); assert.equal(hp.data.effects[0].rounds, 99);
  assert.equal(JSON.stringify(compile(d)), JSON.stringify(r));
});

test("compiler refuses unresolved decisions, name collisions, bad bindings, cycles and unknown tags", () => {
  for (const mutate of [
    (c,t,d) => { c.nodes.p1_t1.rounds = null; },
    (c,t,d) => { c.nodes.p1_t1.seichiSilverCost = null; },
    (c,t,d) => { t.classification.qualifying_elements = []; },
    (c,t,d) => { t.nodes[0].parents = ["p1_t3"]; },
    (c,t,d) => { t.nodes[0].bonuses.notReal = 2; },
    (c,t,d) => { d.game.skills.get(HP).bloodlineId = "wrong"; },
    (c,t,d) => { c.bindings.nodes.p1_t1 = HP; },
    (c,t,d) => { d.game.skills.set("collision", { id: "collision", name: "Breaking Point", pathType: "SKILL" }); },
    (c,t,d) => { c.bindings.folderId = "missing"; },
  ]) { const d = setup(), c = config(), t = clone(design); mutate(c,t,d); const r = compile(d,c,t); assert.ok(r.problems.length); assert.equal(r.manifest,null); assert.equal(mutations(d).length,0); }
});

test("complete discovery follows pages of both path types and proves hidden visibility", async () => {
  const d = setup();
  for (let i=0;i<1002;i++) d.game.skills.set(`row${i}`, { id: `row${i}`, name: `Name ${i}`, tier: 1, pathType: "SKILL", hidden: false });
  const r = await prepareBloodright({ config: config(), ...d }); assert.deepEqual(r.problems, []);
  const calls = d.game.calls.filter(c => c.path === "skillTree.getAll");
  assert.deepEqual(calls.map(c => [c.input.pathType,c.input.cursor]), [["SKILL",0],["SKILL",1],["SKILL",2],["BLOODRIGHT",0],["SKILL",0],["SKILL",1],["SKILL",2],["BLOODRIGHT",0]]);
  assert.equal(mutations(d).length, 0);
  d.game.hiddenAccess = false;
  await assert.rejects(prepareBloodright({ config: config(), ...d }), /hidden-content access/);
});

test("paged inventory refuses repeated cursors, duplicated rows and failures on later pages", async () => {
  for (const mode of ["cursor", "row", "error"]) {
    const d = setup(); let count=0;
    d.client.batch = async () => { count++; return [mode === "error" && count === 2 ? { ok: false, error: { code: "SERVER" } } : { ok: true, data: { data: [{id: mode === "row" ? "same" : String(count),pathType:"SKILL"}], nextCursor: mode === "cursor" ? 0 : count } }]; };
    if (mode === "error") assert.equal((await d.reader.list("skillTree.getAll", {fresh:true})).ok,false);
    else await assert.rejects(d.reader.list("skillTree.getAll", {fresh:true}), /cursor|repeated/);
    assert.equal(await d.cache.get("skillTree.getAll",""),null);
  }
});

test("pilot verifies all 13 records; second compilation reuses IDs and sends no mutations", async () => {
  const d = setup(); const first = compile(d);
  d.runner.plan(first.manifest, {jobId:"bee"});
  const result = await d.runner.run("bee");
  assert.equal(result.outcome,"success",JSON.stringify(result));
  assert.equal(d.game.skills.size,12); assert.equal(d.game.folders.size,1);
  assert.equal(d.game.calls.filter(c=>c.path==="skillTree.create").length,11);
  assert.equal(d.game.skills.get(HP).image,"https://example.test/keep.webp");
  assert.ok([...d.game.skills.values()].every(s=>s.pathType==="BLOODRIGHT" && s.bloodlineId===BL && s.hidden));
  const second = compile(d); assert.deepEqual(second.problems,[]);
  assert.ok(second.preview.every(r=>r.operation==="reuse"));
  const before = mutations(d).length;
  d.runner.plan(second.manifest,{jobId:"bee2"});
  assert.equal((await d.runner.run("bee2")).outcome,"success");
  assert.equal(mutations(d).length,before);
});

test("new folder creates once, verifies without updateFolder, and children use its ID", async () => {
  const d=setup(), c=config(); d.game.folders.clear(); delete c.bindings.folderId; c.folder={name:"BEE staging"};
  const r=compile(d,c); assert.deepEqual(r.problems,[]);
  d.runner.plan(r.manifest,{jobId:"folder"}); assert.equal((await d.runner.run("folder")).outcome,"success");
  assert.equal(d.game.calls.filter(c=>c.path==="skillTree.createFolder").length,1);
  assert.equal(d.game.calls.filter(c=>c.path==="skillTree.updateFolder").length,0);
  assert.equal([...d.game.folders.values()][0].hidden,true);
});

test("stale preview pauses before the changed record is sent", async () => {
  const d=setup(), r=compile(d); d.game.folders.get(FOLDER).order=121;
  d.runner.plan(r.manifest,{jobId:"stale"}); const result=await d.runner.run("stale");
  assert.equal(result.pause.reason,"STALE_PREVIEW"); assert.equal(mutations(d).length,0);
});

test("permission refusal is distinct from session expiration and preserves READY", async () => {
  const d=setup(); d.game.roleAllowed=false; d.runner.plan(compile(d).manifest,{jobId:"role"});
  const result=await d.runner.run("role"); assert.equal(result.pause.reason,"PERMISSION"); assert.equal(d.auth.state,"ready");
});

test("crash after update reconciles landed data without sending update again", async () => {
  const d=setup(); d.game.crashPath="skillTree.update"; d.runner.plan(compile(d).manifest,{jobId:"crashupdate"});
  assert.equal((await d.runner.run("crashupdate")).state,"PAUSED");
  const first=d.game.calls.find(c=>c.path==="skillTree.update").input.id;
  const r=await d.runner.resume("crashupdate"); assert.equal(r.outcome,"success",JSON.stringify(r));
  assert.equal(d.game.calls.filter(c=>c.path==="skillTree.update" && c.input.id===first).length,1);
});

test("lost create response is orphaned, never double-created; explicit adoption resumes", async () => {
  const d=setup(); d.game.crashPath="skillTree.create"; d.runner.plan(compile(d).manifest,{jobId:"crashcreate"});
  await d.runner.run("crashcreate"); await d.runner.resume("crashcreate");
  const item=d.journal.get("crashcreate").items.find(i=>i.state==="ORPHANED"); assert.ok(item);
  assert.equal(d.game.skills.size,2); assert.equal(item.candidates.length,1);
  d.runner.adopt("crashcreate",item.idx,item.candidates[0].id);
  assert.equal((await d.runner.run("crashcreate")).outcome,"success"); assert.equal(d.game.skills.size,12);
});

test("failed prerequisites prevent children, and resume order ignores newly populated idmap", async () => {
  const d=setup(), r=compile(d), parsed=parseManifest(r.manifest), order=planOrder(parsed);
  const ids=Object.fromEntries(order.map((it,i)=>[it.srcId,`id${i}`]));
  assert.deepEqual(planOrder(parsed,ids).map(it=>it.srcId),order.map(it=>it.srcId));
  // Drift the existing folder on readback: its dependent skills must never be sent.
  const get=d.reader.get.bind(d.reader); let reads=0;
  d.reader.get=async(...args)=>{ const x=await get(...args); if(args[0]==="skillTree.getAllFolders" && ++reads>1) x.data.order=999; return x; };
  d.runner.plan(r.manifest,{jobId:"parent"}); const result=await d.runner.run("parent");
  assert.equal(result.pause.reason,"DEPENDENCY"); assert.equal(mutations(d).length,0);
});

test("frozen provenance and expected snapshots affect job identity", () => {
  const d=setup(), m=compile(d).manifest, hash=parseManifest(m).hash;
  const changed=clone(m); changed.bloodrightImport.source.ref="a".repeat(40); assert.notEqual(parseManifest(changed).hash,hash);
  const changedRow=clone(m); changedRow.items[0].expected.order++; assert.notEqual(parseManifest(changedRow).hash,hash);
});

test("Core selects package, blocks incomplete prices, persists compiled text and resumes without recompiling", async () => {
  const d=setup(), core=new ForgeCore({...d,version:"test",now:()=>0});
  const c=config(); c.nodes.p1_t1.rounds=null;
  await core.selectManifest({path:"push/bee.json",name:"bee",text:JSON.stringify({bloodright:c})});
  assert.ok(core.state.selected.problems.length); await core.startJob(); assert.equal(mutations(d).length,0);
  await core.selectManifest({path:"push/bee.json",name:"bee",text:JSON.stringify({bloodright:config()})});
  d.game.crashPath="skillTree.update"; await core.startJob();
  const job=d.journal.listJobs()[0]; assert.ok(job.manifestPath.startsWith("bloodright-job:"));
  d.runner.manifests.clear(); d.github.text=async()=>{throw new Error("must not recompile");};
  await core.resumeJob(job.jobId); assert.equal(d.journal.get(job.jobId).state,"DONE");
  assert.equal(d.game.skills.size,12);
});

test("extra live effect keys are meaningful: friendlyFire drift must not be called reuse", async () => {
  const d=setup(); d.runner.plan(compile(d).manifest,{jobId:"seed"}); await d.runner.run("seed");
  d.game.skills.get(HP).effects[0].friendlyFire="ENEMIES";
  const next=compile(d); assert.equal(next.preview.find(r=>r.targetId===HP).operation,"update");
  assert.ok(next.preview.find(r=>r.targetId===HP).changes.some(c=>c.key==="effects"));
});

test("folder create with lost response requires ownership confirmation and never sends an update", async () => {
  const d=setup(), c=config(); d.game.folders.clear(); delete c.bindings.folderId; c.folder={name:"BEE staging"};
  d.game.crashPath="skillTree.createFolder"; d.runner.plan(compile(d,c).manifest,{jobId:"foldercrash"});
  await d.runner.run("foldercrash"); await d.runner.resume("foldercrash");
  const item=d.journal.get("foldercrash").items[0]; assert.equal(item.state,"ORPHANED");
  d.runner.adopt("foldercrash",0,item.candidates[0].id);
  assert.equal((await d.runner.run("foldercrash")).outcome,"success");
  assert.equal(d.game.calls.filter(c=>c.path==="skillTree.createFolder").length,1);
  assert.equal(d.game.calls.filter(c=>c.path==="skillTree.updateFolder").length,0);
});

test("global uniqueness check is fresh at Start; a new collision is never overwritten", async () => {
  const d=setup(), compiled=compile(d);
  d.game.skills.set("late",{id:"late",name:"Breaking Point",tier:1,pathType:"SKILL",hidden:false});
  d.runner.plan(compiled.manifest,{jobId:"late"}); await d.runner.run("late");
  assert.equal(d.journal.get("late").items.find(i=>i.name==="Breaking Point").state,"FAILED");
  assert.equal(d.game.skills.get("late").pathType,"SKILL");
  assert.ok(!d.game.calls.some(c=>c.path==="skillTree.update" && c.input.id==="late"));
});

test("binding changes after preview block new creates", async () => {
  const d=setup(), m=compile(d).manifest;
  d.storage.setItem("tnr_bk_idmap_v1",JSON.stringify({[scopeKey(BL,"p1_t1")]:"someone-else"}));
  d.runner.plan(m,{jobId:"binding"}); const result=await d.runner.run("binding");
  assert.equal(result.pause.reason,"STALE_BINDINGS"); assert.equal(mutations(d).length,0);
});

test("pre-send validator refuses unsupported tags and strips no accidental keys", () => {
  const d=setup(), row=compile(d).manifest.items.find(it=>it.entity==="skillTree").data;
  for (const mutate of [r=>r.effects[0].affectedElement=["Shadow"],r=>r.effects[0].powerPerLevel=2,r=>r.effects[0].rounds=101,r=>r.effects[0].type="lifesteal",r=>r.effects[0].affectedElements=[],r=>r.pathType="SKILL"]) {
    const data=clone(row); mutate(data); assert.ok(bloodrightProblems("skillTree",data).length);
  }
});

test("missing frozen text refuses resume without re-reading the design or sending", async () => {
  const d=setup(), core=new ForgeCore({...d,version:"test",now:()=>0});
  await core.selectManifest({path:"push/bee.json",name:"bee",text:JSON.stringify({bloodright:config()})});
  d.game.crashPath="skillTree.update"; await core.startJob();
  const job=d.journal.listJobs()[0], before=mutations(d).length;
  d.runner.manifests.clear(); await d.repoCache.clear();
  const notes=[]; core.subscribe(n=>notes.push(n)); await core.resumeJob(job.jobId);
  assert.equal(mutations(d).length,before); assert.ok(notes.some(n=>/saved manifest unavailable/.test(n.text)));
});

test("Python factory/validator bridge and harvest understand compiled Bloodright records", async () => {
  const { execFileSync }=await import("node:child_process");
  const { mkdtempSync,writeFileSync,rmSync }=await import("node:fs");
  const { tmpdir }=await import("node:os");
  const { join }=await import("node:path");
  const { fileURLToPath }=await import("node:url");
  const root=fileURLToPath(new URL("../../",import.meta.url));
  const d=setup(), manifest=compile(d).manifest;
  const output=execFileSync("python3",["-c",`import sys,json;sys.path.insert(0,'skills/building-tnr-content/scripts');from bloodright_bridge import problems;from factory import Factory;m=json.load(sys.stdin);assert not problems(m);f=Factory(entities='skills/building-tnr-content/data/45d_DATA_entity_schemas.json',ctors='skills/building-tnr-content/data/45c_DATA_constructors.json',checks='skills/building-tnr-content/data/45g_DATA_checks.json');e=m['items'][1];f.entry(e['entity'],e['slot'],name=e['name'],srcId=e['srcId'],data=e['data']);f.manifest(m['items'],bloodright_import=m['bloodrightImport']);print('ok')`],{cwd:root,input:JSON.stringify(manifest),encoding:"utf8"});
  assert.match(output,/ok/);
  d.runner.plan(manifest,{jobId:"harvest"}); await d.runner.run("harvest");
  const core=new ForgeCore({...d,version:"test",now:()=>0}); let bundle;
  core.subscribe(n=>{if(n.type==="export")bundle=n.text;}); await core.exportJob("harvest");
  const dir=mkdtempSync(join(tmpdir(),"br-harvest-"));
  try {
    const compiled=join(dir,"compiled.json");writeFileSync(compiled,JSON.stringify(manifest));
    const validated=execFileSync("python3",["skills/building-tnr-content/scripts/validate.py",compiled,"--ctors","skills/building-tnr-content/data/45c_DATA_constructors.json","--strict"],{cwd:root,encoding:"utf8"});
    assert.match(validated,/0 errors/);
    const file=join(dir,"results.json");writeFileSync(file,bundle);
    const verified=execFileSync("python3",["skills/building-tnr-content/scripts/harvest.py","verify",file],{cwd:root,encoding:"utf8"});
    assert.match(verified,/13 ok, 0 fail, 0 unverified, 0 skipped  ->  verified/);
  } finally {rmSync(dir,{recursive:true,force:true});}
});

test("read-only reuse transition requires a bound Bloodright edit and the exact ID", () => {
  for (const entity of ["jutsu","skillTree","skillTreeFolder"]) for (const op of ["create","update"]) {
    const d=setup(); d.journal.open({jobId:"transition",items:[{entity,op,targetId:op==="update"?HP:null}]});
    for (const patch of [{}, {reused:true,phase:"update",entityId:HP}, {reused:true,phase:"verify",entityId:"wrong"}]) assert.throws(()=>d.journal.transition("transition",0,"CONFIRMED",patch));
    const go=()=>d.journal.transition("transition",0,"CONFIRMED",{reused:true,phase:"verify",entityId:HP});
    if(entity!=="jutsu" && op==="update") {go();assert.equal(d.journal.get("transition").items[0].sentAt,null);}
    else assert.throws(go);
  }
});

test("resume detects binding conflicts before journal synchronization can overwrite them", async () => {
  const d=setup(); d.game.crashPath="skillTree.update"; d.runner.plan(compile(d).manifest,{jobId:"resume-binding"}); await d.runner.run("resume-binding");
  const map=readIdmap(d.storage); map[scopeKey(BL,"folder")]="changed"; d.storage.setItem("tnr_bk_idmap_v1",JSON.stringify(map));
  const before=mutations(d).length;
  const result=await d.runner.resume("resume-binding"); assert.equal(result.pause.reason,"STALE_BINDINGS");
  assert.equal(mutations(d).length,before); assert.equal(readIdmap(d.storage)[scopeKey(BL,"folder")],"changed");
});

test("review R1: changed settings cannot open another import over an unresolved create", async () => {
  const d=setup(), c=config(); c.nodes.p4_t3.seichiSilverCost=21;
  const core=new ForgeCore({...d,version:"test",now:()=>0});
  await core.selectManifest({path:"push/changed.json",name:"changed",text:JSON.stringify({bloodright:c})});
  const changed=compile(d,c).manifest;
  d.runner.plan(compile(d).manifest,{jobId:"unresolved-A"});
  d.game.crashPath="skillTree.create"; await d.runner.run("unresolved-A"); await d.runner.resume("unresolved-A");
  assert.ok(d.journal.get("unresolved-A").items.some(i=>i.state==="ORPHANED"));
  const sent=mutations(d).length;
  await assert.rejects(prepareBloodright({config:c,...d}),/unresolved.*unresolved-A/i);
  assert.throws(()=>d.runner.plan(changed,{jobId:"blocked-B"}),/unresolved.*unresolved-A/i);
  await core.startJob();
  assert.equal(d.journal.listJobs().length,1); assert.equal(mutations(d).length,sent);
});

test("review R2: lost hidden visibility after create pauses immediately and resumes that placeholder", async () => {
  const d=setup(), original=d.game.handle.bind(d.game); let creates=0;
  d.game.handle=(path,input)=>{const r=original(path,input);if(path==="skillTree.create" && ++creates===2)d.game.hiddenAccess=false;return r;};
  d.runner.plan(compile(d).manifest,{jobId:"visibility"});
  const paused=await d.runner.run("visibility");
  assert.equal(paused.pause.reason,"VISIBILITY"); assert.equal(creates,2);
  assert.ok(!d.journal.get("visibility").items.some(i=>i.state==="FAILED"));
  assert.ok(d.journal.get("visibility").items.some(i=>i.state==="CONFIRMED" && i.phase==="update"));
  d.game.hiddenAccess=true;
  assert.equal((await d.runner.run("visibility")).outcome,"success");
  assert.equal(creates,11); assert.equal(d.game.skills.size,12);
});

test("review R2: missing Bloodright readback pauses before any later create", async () => {
  const d=setup(), original=d.game.handle.bind(d.game);let lost=false;
  d.game.handle=(path,input)=>{const r=original(path,input);if(path==="skillTree.update" && !lost){lost=true;d.game.hiddenAccess=false;}return r;};
  d.runner.plan(compile(d).manifest,{jobId:"verify-visibility"});
  const paused=await d.runner.run("verify-visibility");
  assert.equal(paused.pause.reason,"VISIBILITY");
  assert.equal(d.game.calls.filter(c=>c.path==="skillTree.create").length,1);
  assert.ok(d.journal.get("verify-visibility").items.some(i=>i.state==="CONFIRMED" && i.phase==="verify"));
  d.game.hiddenAccess=true;assert.equal((await d.runner.run("verify-visibility")).outcome,"success");
});

test("review R3: deletion between offset pages refuses the inventory instead of silently omitting a row", async () => {
  const d=setup();for(let i=0;i<600;i++){const key=`r${String(i).padStart(4,"0")}`;d.game.skills.set(key,{id:key,name:key,tier:1,pathType:"SKILL",hidden:false});}
  const original=d.game.handle.bind(d.game);let removed=false;
  d.game.handle=(path,input)=>{const r=original(path,input);if(path==="skillTree.getAll" && input.pathType==="SKILL" && input.cursor===0 && !removed){removed=true;d.game.skills.delete("r0000");}return r;};
  await assert.rejects(d.reader.list("skillTree.getAll",{fresh:true}),/inventory changed/i);
  assert.equal(await d.cache.get("skillTree.getAll",""),null);
});

test("review R4: design names with surrounding whitespace are refused", () => {
  for(const name of [" Breaking Point","Breaking Point ","\tBreaking Point\n"]){const d=setup(),tree=clone(design);tree.nodes[0].name=name;const r=compile(d,config(),tree);assert.equal(r.manifest,null);assert.ok(r.problems.some(p=>/whitespace|trim/i.test(p)));}
});

test("review raw-manifest note: Bloodright writes require provenance, preimages and name checks", () => {
  const m=compile(setup()).manifest;
  for(const change of [v=>delete v.bloodrightImport,v=>delete v.items[0].expected,v=>delete v.bloodrightImport.bindings[v.items[0].srcId],v=>v.dedupNames=false]){const broken=clone(m);change(broken);assert.throws(()=>parseManifest(broken),/Bloodright/);}
  assert.doesNotThrow(()=>parseManifest({capture:{before:[{proc:"skillTree.get",input:{id:HP},persist:"full"}]}}));
});

test("review R1: SENT, ORPHANED and CONFIRMED legacy jobs block only their bloodline", () => {
  for(const state of ["SENT","ORPHANED","CONFIRMED"]){
    const d=setup(),m=compile(d).manifest;d.runner.plan(m,{jobId:"legacy-pending"});
    assert.equal(d.journal.get("legacy-pending").bloodrightImport.bloodlineId,BL);
    d.journal.annotateJob("legacy-pending",{bloodrightImport:null});
    d.journal.transition("legacy-pending",1,"SENT",{phase:"create"});
    if(state!=="SENT")d.journal.transition("legacy-pending",1,state,state==="CONFIRMED"?{entityId:"pending-id",phase:"update"}:{});
    assert.throws(()=>assertBloodrightAvailable(d.journal,BL),/unresolved.*legacy-pending/i);
    assert.doesNotThrow(()=>assertBloodrightAvailable(d.journal,"another-bloodline"));
    d.journal.transition("legacy-pending",1,"FAILED",{error:"operator resolved test obligation"});
    assert.doesNotThrow(()=>assertBloodrightAvailable(d.journal,BL));
  }
});

test("review R1: an already planned second job cannot run or resume over a lost create", async () => {
  const d=setup(),c=config();c.nodes.p4_t3.seichiSilverCost=21;
  d.runner.plan(compile(d).manifest,{jobId:"queued-A"});d.runner.plan(compile(d,c).manifest,{jobId:"queued-B"});
  d.game.crashPath="skillTree.create";await d.runner.run("queued-A");const sent=mutations(d).length;
  assert.equal((await d.runner.run("queued-B")).pause.reason,"UNRESOLVED_IMPORT");
  assert.equal((await d.runner.resume("queued-B")).pause.reason,"UNRESOLVED_IMPORT");
  assert.equal(mutations(d).length,sent);
  assert.equal((await d.runner.resume("queued-A")).pause.reason,"ORPHANED");
});

test("review R2: a hidden folder lost after one-phase create pauses before any skill create", async () => {
  const d=setup(),c=config();d.game.folders.clear();delete c.bindings.folderId;c.folder={name:"BEE staging"};
  const original=d.game.handle.bind(d.game);
  d.game.handle=(path,input)=>{const r=original(path,input);if(path==="skillTree.createFolder")d.game.hiddenAccess=false;return r;};
  d.runner.plan(compile(d,c).manifest,{jobId:"folder-visibility"});
  assert.equal((await d.runner.run("folder-visibility")).pause.reason,"VISIBILITY");
  assert.equal(d.game.calls.filter(c=>c.path==="skillTree.create").length,0);
  assert.equal(d.journal.get("folder-visibility").items[0].state,"CONFIRMED");
  d.game.hiddenAccess=true;assert.equal((await d.runner.run("folder-visibility")).outcome,"success");
  assert.equal(d.game.calls.filter(c=>c.path==="skillTree.createFolder").length,1);
});
