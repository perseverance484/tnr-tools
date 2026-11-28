import concurrent.futures, json, os, pathlib, re, subprocess, sys, tempfile

ROOT=pathlib.Path.cwd()
BASE=pathlib.Path(tempfile.mkdtemp(prefix='ap1-r11-reports-'))
ORIGINAL=BASE/'original'
for name in ('original','adapted','logs'):
    (BASE/name).mkdir()
def git_show(spec):
    return subprocess.check_output(['git','show',spec],text=True)
report=git_show('e7e4c0f6:docs/reviews/AI_PLAYER_AP1_REREVIEW9_REVIEW.md')
blocks=re.findall(r'```python\n(.*?)```',report,re.S)
(ORIGINAL/'first_delivery.py').write_text(blocks[0])
(ORIGINAL/'first_resident.py').write_text(blocks[1])
for name in ('known_limit','takeover_delivery','repeated_unreadable'):
    (ORIGINAL/f'{name}.py').write_text(git_show(f'f586a6b2:docs/reviews/evidence/ap1_rereview9_lane_a/{name}.py'))
print('Evidence folder:',BASE,flush=True)
if '--prepare-only' in sys.argv:
    raise SystemExit(0)
TARGET='e4a267cd1ab5ff85c3b2399bab713f2870da6ccb'
PREVIOUS='29797ba0f769152381e71710f812605be9e0bfea'
VERSIONS=[PREVIOUS,'c412de4df43baf4f11fbd817efb0f7ae95c08226','7cf7d73c5cb235801b66e4b4763cb63e1bc7b14e']
jobs=[]
def add(name,source,args=(),adapt=False):
    path=BASE/'adapted'/f'{name}.py'
    path.write_text(source)
    jobs.append((name,path,list(args),adapt))

first=(ORIGINAL/'first_delivery.py').read_text()
second=(ORIGINAL/'takeover_delivery.py').read_text()
resident=(ORIGINAL/'first_resident.py').read_text()
for mode in ('pending','receipt','ack','installed','expired','trusted'):
    add('unchanged_first_'+mode,first,[mode])
add('unchanged_second',second)
add('unchanged_resident',resident)
for version in VERSIONS:
    tag=version[:8]
    changed=first.replace(PREVIOUS,version).replace(" assert bool(calls)==(mode!='expired'), 'unexpected control result'",'')
    for mode in ('pending','receipt','ack','installed','expired'):
        add(f'first_{tag}_{mode}',changed,[mode],True)
    changed=second.replace(PREVIOUS,version)
    changed=changed.replace('            assert len(calls_of(lines))>0\n','').replace("            assert now[0]-made['now']<60\n",'').replace('            if takeover: assert len(held)==30\n','')
    add(f'second_{tag}',changed,adapt=True)
    changed=resident.replace(PREVIOUS,version).replace('  assert calls\n','')
    add(f'resident_{tag}',changed,adapt=True)
changed=first.replace("'c412de4df43baf4f11fbd817efb0f7ae95c08226' if mode=='trusted'",f"'{TARGET}' if mode=='trusted'")
add('current_trusted',changed,['trusted'],True)
replay=(ORIGINAL/'repeated_unreadable.py').read_text()
for mode in ('replay','different','no-word'):
    add('unchanged_h2_'+mode,replay,[mode])
    add('protocol_adapted_h2_'+mode,replay.replace("['budget']['protocol']==1","['budget']['protocol']==relay.PROTOCOL"),[mode],True)

def run(job):
    name,path,args,adapt=job
    p=subprocess.run([sys.executable,str(path),*args],cwd=ROOT,env={**os.environ,'PYTHONPATH':str(ROOT)},capture_output=True,text=True,timeout=150)
    (BASE/'logs'/f'{name}.log').write_text(p.stdout+p.stderr)
    result={'case':name,'exit':p.returncode,'adapted':adapt}
    print(json.dumps(result),flush=True)
    return result
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
    results=list(pool.map(run,jobs))
(BASE/'results.json').write_text(json.dumps(results,indent=2)+'\n')
