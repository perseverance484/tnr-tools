import io,json,os,pathlib,subprocess,sys,time
from unittest.mock import patch
from player import brain,relay
from player.world import World,takeovers
from player.tests.test_rereview5 import by_the_version_at
from player.tests.test_rereview9 import OLD_PROGRAM
from player.tests.test_relay import token_of
from player.tests.test_rereview6 import calls_of

mode=sys.argv[1] if len(sys.argv)>1 else 'window'
live,made=by_the_version_at('7cf7d73c5cb235801b66e4b4763cb63e1bc7b14e',OLD_PROGRAM,'pending')
path=pathlib.Path(live)/'world.json'
raw=path.read_bytes(); stamp=path.stat().st_mtime_ns
now=[made['now']+120]; real=brain.Brain; write=World._write
observed={'mode':mode}
def say(*names):
    out=io.StringIO(); brain.stopped(live,list(names),out); return json.loads(out.getvalue())
def nxt(token=None):
    out=io.StringIO(); brain.next_batch(live,token,out,lambda t:now.__setitem__(0,now[0]+max(0,t)))
    return out.getvalue().splitlines()
with patch.dict(os.environ,{'TNR_PLAYER_NO_DAEMON':'1','TNR_TRANSCRIPT':live+'/none','TNR_PLAYER_FIGHTS':live+'/fights'}),patch.object(time,'time',lambda:now[0]),patch.object(brain,'Brain',lambda live:real(live,clock=lambda:now[0])):
    home=real(live,clock=lambda:now[0])
    observed['first_hold']=home.budget.loose()[0][1]
    if mode=='before': observed['word']=say('all')
    def interleave(p,obj):
        if p==str(path) and mode=='window' and not observed.get('word'):
            observed['count_when_word_said']=takeovers(live)
            probe=brain._lock(live)
            observed['resident_has_brain_lock']=probe is None
            if probe is not None: probe.close()
            child="import sys,time; from player import brain; time.time=lambda:float(sys.argv[2]); brain.stopped(sys.argv[1],['all'])"
            said=subprocess.run([sys.executable,'-c',child,live,str(now[0])],cwd=os.getcwd(),env={**os.environ,'PYTHONPATH':os.getcwd()},capture_output=True,text=True,timeout=5,check=True)
            observed['word']=json.loads(said.stdout)
        write(p,obj)
    if mode=='failed':
        def fail_world(p,obj):
            if p==str(path): raise OSError('injected world save failure')
            write(p,obj)
        with patch.object(World,'_write',staticmethod(fail_world)):
            home._save()
        observed['count_when_word_said']=takeovers(live)
        observed['word']=say('all')
        home._save()  # the same brain recovers and saves the original hold, without recounting
    else:
        with patch.object(World,'_write',staticmethod(interleave)):
            observed['resident_exit']=brain.run(live,forever=False)
    if mode=='after': observed['word']=say('all')
    observed['saved_hold']=[c[3] for c in relay.read(str(path))['budget']['calls'] if c[1]=='update'][0]
    observed['count_after_save']=takeovers(live)
    now[0]+=120
    path.write_bytes(raw); os.utime(path,ns=(stamp,stamp))
    observed['later_listing']=say()
    started=now[0]
    lines=nxt(token_of(nxt()[0]))
    observed['calls']=calls_of(lines); observed['elapsed']=now[0]-started
    observed['loose_update']=sum(1 for c in relay.read(str(path))['budget']['calls'] if c[1]=='update' and c[2:3]==['loose'])
    observed['final_count']=takeovers(live)
    print(json.dumps(observed))
    assert observed['count_after_save']==1
    assert observed['final_count']==2
    if mode in ('window','failed'):
        if mode=='window': assert observed['resident_has_brain_lock']
        assert observed['word']['stopped']==observed['later_listing']['still_held']
        assert observed['calls'] and observed['elapsed']<60
        assert not observed['loose_update']
    else:
        assert observed['word']['stopped']!=observed['later_listing']['still_held']
        assert not observed['calls']
        assert observed['loose_update']==30
