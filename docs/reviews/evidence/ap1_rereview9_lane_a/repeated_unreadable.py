import io,json,os,sys,tempfile,time
from types import SimpleNamespace
from unittest.mock import patch
from player import brain,relay
from player.tests.test_relay import token_of
from player.tests.test_rereview4 import dies_before_the_receipt,Killed
from player.tests.test_rereview6 import calls_of

mode=sys.argv[1] if len(sys.argv)>1 else 'replay'
live=tempfile.mkdtemp(prefix='ap1-repeated-unreadable-')
now=[time.time()]; real=brain.Brain
def truncate(text=''):
    with open(live+'/world.json','w') as f: f.write(text)
    os.utime(live+'/world.json',(now[0],now[0]))
def say(*names):
    out=io.StringIO(); brain.stopped(live,list(names),out); return json.loads(out.getvalue())
def nxt(token=None):
    out=io.StringIO()
    brain.next_batch(live,token,out,lambda t:now.__setitem__(0,now[0]+max(t,0)))
    return out.getvalue().splitlines()
with patch.dict(os.environ,{'TNR_PLAYER_NO_DAEMON':'1','TNR_TRANSCRIPT':live+'/none','TNR_PLAYER_FIGHTS':live+'/fights'}),patch.object(time,'time',lambda:now[0]),patch.object(brain,'Brain',lambda live:real(live,clock=lambda:now[0])):
    truncate()
    first=say('all'); word=relay.read(live+'/client.json')['ended']
    token=token_of(nxt()[0])
    with dies_before_the_receipt(SimpleNamespace(dir=live)):
        try: nxt(token)
        except Killed: pass
    assert relay.read(live+'/client.json')['ended']==word
    assert relay.read(live+'/world.json')['budget']['protocol']==1
    now[0]+=120
    truncate('{' if mode=='different' else '')  # second unreadable ledger, after the first takeover was durably saved
    if mode=='no-word':
        state=relay.read(live+'/client.json'); state['ended']=[]
        relay.write(live+'/client.json',state)
    second=say()
    started=now[0]; lines=nxt(token)
    w=relay.read(live+'/world.json')
    loose=[c for c in w['budget']['calls'] if c[1]=='update' and c[2:3]==['loose']]
    result={'mode':mode,'first_word':first,'second_listing':second,'new_word':False,'same_id':first['stopped']==second['still_held'],'remaining_loose_update_rows':len(loose),'calls':calls_of(lines),'elapsed':now[0]-started}
    print(json.dumps(result))
    if mode=='replay':
        assert first['stopped']==second['still_held']
        assert not loose
        assert calls_of(lines)
    else:
        assert len(loose)==30
        assert not calls_of(lines)
