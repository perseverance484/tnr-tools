import io,json,os,subprocess,sys,time
from unittest.mock import patch
from player import brain,relay
from player.tests import test_rereview5 as old
from player.tests.test_rereview7 import OLD_RESIDENT
from player.tests.test_relay import token_of
old.BEFORE='29797ba0f769152381e71710f812605be9e0bfea'
root=old.the_package_before()
p=subprocess.Popen([sys.executable,'-W','ignore','-c',OLD_RESIDENT],cwd=root,env={**os.environ,'PYTHONPATH':root},stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
try:
 made=json.loads(p.stdout.readline());live=made['live']
 with patch.dict(os.environ,{'TNR_PLAYER_NO_DAEMON':'1','TNR_TRANSCRIPT':live+'/none','TNR_PLAYER_FIGHTS':live+'/fights'}):
  def nxt(token=None):
   out=io.StringIO();brain.next_batch(live,token,out);return out.getvalue().splitlines()
  lines=nxt(token_of(nxt()[0]));calls=[json.loads(s)['call'] for s in lines if s.startswith('{') and 'call' in json.loads(s)]
  print('old resident alive:',p.poll() is None,'calls without acknowledgement:',calls)
  print('saved ledger protocol:',relay.read(live+'/world.json')['budget'].get('protocol'))
  assert calls
finally:
 p.terminate();p.wait(timeout=5);p.stdout.close();p.stderr.close()
