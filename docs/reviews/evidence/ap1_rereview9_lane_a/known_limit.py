import io,json,os,time
from unittest.mock import patch
from player import brain,relay,calls as K
from player.tests.test_relay import token_of
from player.tests.test_rereview5 import by_the_version_before
from player.tests.test_rereview2 import most_in_a_minute
OLD=r'''
import io,json,os,time
from unittest.mock import patch
from player import brain,relay
from player.tests.support import Rig,user
from player.tests.test_relay import token_of
r=Rig();r.world.absorb([user()._replace(at=r.t)]);r.world.save()
now=[r.t];real=brain.Brain
def nxt(token=None):
 out=io.StringIO();brain.next_batch(r.dir,token,out,lambda t:now.__setitem__(0,now[0]+max(t,0)));return out.getvalue().splitlines()
with patch.dict(os.environ,{'TNR_PLAYER_NO_DAEMON':'1','TNR_TRANSCRIPT':r.dir+'/none','TNR_PLAYER_FIGHTS':r.dir+'/fights'}),patch.object(time,'time',lambda:now[0]),patch.object(brain,'Brain',lambda live:real(live,clock=lambda:now[0])):
 a=token_of(nxt(token_of(nxt()[0]))[-1])
 b=token_of(nxt(token_of(nxt()[0]))[-1])
 relay.write(r.dir+'/control.json',{'version':1,'paused':True})
 b=token_of(nxt(b)[-1])
 now[0]+=1000
 nxt(b)
 print(json.dumps({'live':r.dir,'now':now[0],'holder':a,'ledger':relay.read(r.dir+'/world.json')['budget']['calls']}))
'''
def scenario(mode):
 print("CASE:",mode)
 live,made=by_the_version_before(OLD);assert made['ledger']==[]
 print('old package expired all ledger entries; A never returned:',made['holder'])
 now=[made['now']];real=brain.Brain
 relay.write(live+'/control.json',{'version':2,'paused':False})
 def nxt(token=None):
  out=io.StringIO();brain.next_batch(live,token,out,lambda t:now.__setitem__(0,now[0]+max(t,0)));return out.getvalue().splitlines()
 with patch.dict(os.environ,{'TNR_PLAYER_NO_DAEMON':'1','TNR_TRANSCRIPT':live+'/none','TNR_PLAYER_FIGHTS':live+'/fights'}),patch.object(time,'time',lambda:now[0]),patch.object(brain,'Brain',lambda live:real(live,clock=lambda:now[0])):
  last_old_call=now[0]-.1
  if mode!='no acknowledgment':
   out=io.StringIO();brain.stopped(live,['all'],out);print('stopped all:',out.getvalue().strip())
  if mode=='acknowledgment plus 60 seconds':now[0]+=60
  lines=nxt(token_of(nxt()[0]));calls=[json.loads(s)['call'] for s in lines if s.startswith('{') and 'call' in json.loads(s)]
  print('new calls issued:',len(calls),'new calls; saved loose:',[c for c in relay.read(live+'/world.json')['budget']['calls'] if c[2:3]==['loose']])
  for lane,n in [('recovery',15),('world',10)]:
   clock=[now[0]];budget=real(live,clock=lambda:clock[0]).budget
   made_times=[last_old_call]*4+[clock[0]]*len(calls) # A makes its last four calls just before the boundary.
   for _ in range(n):
    steps,_=budget.pace([K.user(),K.user()],lane)
    for s in steps:
     if 'wait' in s:clock[0]+=s['wait']
     else:made_times.append(clock[0]);clock[0]+=.01
   print(lane,most_in_a_minute(made_times))

for mode in ("no acknowledgment", "acknowledgment only", "acknowledgment plus 60 seconds"):
 scenario(mode)
