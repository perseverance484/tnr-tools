import json,os,pathlib,re,signal,subprocess,sys,tempfile,time
from player import brain,config as C
from player.tests.test_rereview5 import the_package_at

def residents(live):
    found=[]
    for d in pathlib.Path('/proc').iterdir():
        if not d.name.isdecimal(): continue
        try:
            cmd=(d/'cmdline').read_bytes().split(b'\0')
            env=(d/'environ').read_bytes().split(b'\0')
            if b'player.brain' in cmd and b'run' in cmd and ('TNR_PLAYER_LIVE='+live).encode() in env:
                found.append(int(d.name))
        except (OSError,PermissionError): pass
    return found

def session(root,label):
    live=tempfile.mkdtemp(prefix='brain-split-autospawn-')
    env={**os.environ,'PYTHONPATH':root,'TNR_PLAYER_LIVE':live,'TNR_TRANSCRIPT':live+'/none','TNR_PLAYER_FIGHTS':live+'/fights'}
    env.pop('TNR_PLAYER_NO_DAEMON',None)
    command=[sys.executable,'-m','player.brain']
    def run(*args):
        return subprocess.run(command+list(args),cwd=root,env=env,capture_output=True,text=True,timeout=25)
    def token(p):
        assert p.returncode==0 and not p.stderr,(p.returncode,p.stderr)
        return re.search(r'next ([0-9a-f]+-\d+)',p.stdout.splitlines()[-1]).group(1)
    owned=[]
    try:
        first=token(run('next'))
        assert not residents(live)
        second=token(run('next',first)) # actual CLI -> _await -> Popen(-m player.brain run)
        until=time.monotonic()+10
        while time.monotonic()<until:
            owned=residents(live)
            if owned:
                lock=brain._lock(live)
                if lock is None: break
                lock.close()
            time.sleep(.05)
        assert len(owned)==1,owned
        lock=brain._lock(live)
        assert lock is None,'resident has not taken brain.lock'
        assert run('run').returncode==1
        third=token(run('next',second))
        assert residents(live)==owned
        status=json.loads(run('status').stdout)
        assert status is not None
        os.kill(owned[0],signal.SIGTERM)
        until=time.monotonic()+10
        while time.monotonic()<until:
            lock=brain._lock(live)
            if lock is not None:
                lock.close(); break
            time.sleep(.05)
        else: raise AssertionError('SIGTERM did not release brain.lock')
        print(json.dumps({'version':label,'auto_started':1,'second_resident_exit':1,'same_resident_served_next':True,'token_advanced':second!=third,'sigterm_released_lock':True}),flush=True)
    finally:
        for pid in residents(live):
            try: os.kill(pid,signal.SIGTERM)
            except ProcessLookupError: pass

session(the_package_at('e4a267cd1ab5ff85c3b2399bab713f2870da6ccb'),'base')
session(C.ROOT,'split')
