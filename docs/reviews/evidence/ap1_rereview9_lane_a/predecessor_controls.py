import io,json,os,time,sys
from unittest.mock import patch
from player import brain,relay
from player.tests import test_rereview5 as old
from player.tests.test_relay import token_of
mode=sys.argv[1] if len(sys.argv)>1 else 'pending'
old.BEFORE=('c412de4df43baf4f11fbd817efb0f7ae95c08226' if mode=='trusted' else '29797ba0f769152381e71710f812605be9e0bfea')
OLD=r'''
import io,json,os,time
from unittest.mock import patch
from player import brain,relay
from player.tests.support import Rig,user
from player.tests.test_relay import token_of
r=Rig(); r.world.absorb([user()._replace(at=r.t)]);r.world.save()
now=[time.time()];real=brain.Brain;write=relay.write
class Killed(Exception):pass
def saving(path,obj):
 write(path,obj)
 if path==r.dir+'/client.json' and obj.get('pending'):raise Killed
def nxt(token=None):
 out=io.StringIO();brain.next_batch(r.dir,token,out,lambda t:now.__setitem__(0,now[0]+max(t,0)));return out.getvalue().splitlines()
with patch.dict(os.environ,{'TNR_PLAYER_NO_DAEMON':'1','TNR_TRANSCRIPT':r.dir+'/none','TNR_PLAYER_FIGHTS':r.dir+'/fights'}),patch.object(time,'time',lambda:now[0]),patch.object(brain,'Brain',lambda live:real(live,clock=lambda:now[0])):
 token=token_of(nxt()[0])
 with patch.object(relay,'write',saving):
  try:nxt(token)
  except Killed:pass
 print(json.dumps({'live':r.dir,'now':now[0]}))
'''
if mode=='receipt':
 OLD=OLD.replace(" write(path,obj)\n if path==r.dir+'/client.json' and obj.get('pending'):raise Killed"," if path==r.dir+'/client.json' and obj.get('pending'):raise Killed\n write(path,obj)")
live,made=old.by_the_version_before(OLD)
now=[made['now']];real=brain.Brain
with patch.dict(os.environ,{'TNR_PLAYER_NO_DAEMON':'1','TNR_TRANSCRIPT':live+'/none','TNR_PLAYER_FIGHTS':live+'/fights'}),patch.object(time,'time',lambda:now[0]),patch.object(brain,'Brain',lambda live:real(live,clock=lambda:now[0])):
 def nxt(token=None):
  out=io.StringIO();brain.next_batch(live,token,out,lambda t:now.__setitem__(0,now[0]+max(t,0)));return out.getvalue().splitlines()
 out=io.StringIO();brain.stopped(live,[],out);print('listing before:',out.getvalue().strip())
 pending=relay.read(live+'/client.json').get('pending')
 print('pending wait:',pending['ready_at']-now[0] if pending else None)
 if mode=='expired':now[0]=pending['ready_at']+11
 started=now[0]
 if mode=='ack':brain.stopped(live,['all'],io.StringIO())
 if mode=='installed':real(live,clock=lambda:now[0])._save()
 lines=nxt(relay.read(live+'/client.json')['token'] if mode=='receipt' else token_of(nxt()[0]));calls=[json.loads(s)['call'] for s in lines if s.startswith('{') and 'call' in json.loads(s)]
 print('mode:',mode,'calls:',calls,'elapsed:',now[0]-started)
 print('saved ledger protocol:',relay.read(live+'/world.json')['budget'].get('protocol'))
 assert bool(calls)==(mode!='expired'), 'unexpected control result'
