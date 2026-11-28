import io, json, os, subprocess, sys, tempfile, time
from unittest.mock import patch
from player import brain, relay
from player.tests.test_relay import token_of
from player.tests.test_rereview6 import calls_of

ROOT = os.getcwd()
OLD = '29797ba0f769152381e71710f812605be9e0bfea'
package = tempfile.mkdtemp(prefix='ap1-base-package-')
subprocess.run(['git', 'archive', OLD, 'player'], stdout=open(package+'/player.tar', 'wb'), check=True)
subprocess.run(['tar', '-xf', package+'/player.tar', '-C', package], check=True)
for name in ('state', 'data', 'docs', 'scripts', 'harness', '.claude'):
    os.symlink(ROOT+'/'+name, package+'/'+name)

program = r'''
import io, json, os, sys, time
from unittest.mock import patch
from player import brain, relay
from player.tests.support import Rig, user
from player.tests.test_relay import token_of
r=Rig(); r.world.absorb([user()._replace(at=r.t)]); r.world.save()
now=[r.t]; real=brain.Brain; write=relay.write
def nxt(token=None):
    out=io.StringIO()
    brain.next_batch(r.dir,token,out,lambda t:now.__setitem__(0,now[0]+max(t,0)))
    return out.getvalue().splitlines()
class Death(Exception): pass
def die(path,obj):
    if path==r.dir+'/client.json' and obj.get('pending'):
        if sys.argv[1]=='pending': write(path,obj)
        raise Death()
    write(path,obj)
with patch.dict(os.environ,{'TNR_PLAYER_NO_DAEMON':'1','TNR_TRANSCRIPT':r.dir+'/none','TNR_PLAYER_FIGHTS':r.dir+'/fights'}),patch.object(time,'time',lambda:now[0]),patch.object(brain,'Brain',lambda live:real(live,clock=lambda:now[0])):
    token=token_of(nxt()[0])
    with patch.object(relay,'write',die):
        try: nxt(token)
        except Death: pass
    print(json.dumps({'live':r.dir,'now':now[0],'token':token}))
'''

for mode in ('pending', 'receipt'):
    for takeover in (False, True):
        p=subprocess.run([sys.executable,'-c',program,mode],cwd=package,env={**os.environ,'PYTHONPATH':package},capture_output=True,text=True,check=True)
        made=json.loads(p.stdout.splitlines()[-1]); live=made['live']; now=[made['now']]; real=brain.Brain
        def nxt(token=None):
            out=io.StringIO()
            brain.next_batch(live,token,out,lambda t:now.__setitem__(0,now[0]+max(t,0)))
            return out.getvalue().splitlines()
        with patch.dict(os.environ,{'TNR_PLAYER_NO_DAEMON':'1','TNR_TRANSCRIPT':live+'/none','TNR_PLAYER_FIGHTS':live+'/fights'}),patch.object(time,'time',lambda:now[0]),patch.object(brain,'Brain',lambda live:real(live,clock=lambda:now[0])):
            if takeover: real(live,clock=lambda:now[0]).world.save()
            if mode=='pending': token=token_of(nxt()[0])  # fresh relay, old actors already ended
            else: token=made['token']                   # retry the interrupted caller with current code
            lines=nxt(token)
            w=relay.read(live+'/world.json'); held=[c for c in w['budget']['calls'] if c[1]=='update']
            result={'mode':mode,'takeover_saved_first':takeover,'calls':calls_of(lines),'elapsed':now[0]-made['now'],'update_rows':len(held),'ledger_protocol':w['budget'].get('protocol'),'acknowledgements':relay.read(live+'/client.json')['ended']}
            print(json.dumps(result))
            assert len(calls_of(lines))>0
            assert now[0]-made['now']<60
            if takeover: assert len(held)==30
