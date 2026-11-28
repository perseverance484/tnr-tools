"""Actual brain next/put paths in temporary worlds; no game or lock-tool calls."""
import contextlib
import io
import json
import os
from unittest import mock
from player import brain, config as C, relay, calls as K
from player.activities import equipment, training
from player.tests.support import Rig, user
from player.tests.test_relay import token_of
from player.tests.test_upkeep import stock, PANACEA, PILL, KUNAI
from player.world import utc_day

class Client:
    def __init__(self, equipment_on=False, pocket=200_000):
        self.r = r = Rig(upkeep=True)
        r.world['control']['activities'].update(training=False, equipment=equipment_on)
        self.me = user(money=pocket, bank=900_000_000)
        r.world.absorb([self.me._replace(at=r.t)])
        r.world['records']['spend'] = {'day': utc_day(r.t), 'ryo': C.DAILY_CAP-180_000}
        r.world.save()
        real = brain.Brain
        self.stack = contextlib.ExitStack()
        self.stack.enter_context(mock.patch.object(brain, 'Brain', lambda live: real(live,clock=lambda:r.t,combat=r.combat,gates=r.brain.gates)))
        self.stack.enter_context(mock.patch.object(brain.time, 'time', lambda:r.t))
        self.stack.enter_context(mock.patch.dict(os.environ, {'TNR_PLAYER_NO_DAEMON':'1','TNR_TRANSCRIPT':os.path.join(r.dir,'absent'),'TNR_PLAYER_FIGHTS':os.path.join(r.dir,'fights')}))
    def next(self, token=None):
        out=io.StringIO()
        brain.next_batch(self.r.dir,token,out,lambda n:setattr(self.r,'t',self.r.t+n))
        lines=out.getvalue().splitlines()
        steps=[json.loads(x) for x in lines if x.startswith('{') and 'call' in json.loads(x)]
        return token_of(lines[-1]) if not lines[-1].startswith('STOP') else None,steps,lines
    def feed(self, token, steps, items, me):
        for i,s in enumerate(steps,1):
            data=items.data if s['call']=='item.getUserItems' else me.data if s['call']=='profile.getUser' else {'success':True}
            assert brain.put(self.r.dir,token,i,json.dumps(data))==0
    def saved(self):
        return relay.read(os.path.join(self.r.dir,'world.json'))
    def state(self):
        return relay.read(os.path.join(self.r.dir,'client.json'))
    def start(self, items):
        token,_,_=self.next()
        token,steps,_=self.next(token)
        assert [s['call'] for s in steps][:2]==['item.getUserItems','profile.getUser']
        self.feed(token,steps,items,self.me)
        return self.next(token)

def purchases(steps):
    return sum(s['input']['stack']*({PANACEA:55_000,PILL:1_000}[s['input']['itemId']]) for s in steps if s['call']=='item.buy')

def reservation(read_after=False):
    c=Client(pocket=400_000)
    try:
        short=stock(**{PANACEA:(0,'ITEM_3',False,None),PILL:None})
        a,steps,_=c.start(short)
        batch_a=c.state()['held']['id']
        first=purchases(steps)
        assert first==180_000
        b,_,_=c.next()
        b,reads,_=c.next(b)
        assert [s['call'] for s in reads]==['item.getUserItems','profile.getUser']
        if not read_after:
            c.feed(b,reads,short,c.me)  # B's reads finish before A spends its reserved money.
        before=c.saved()['records']['spend']
        c.r.t+=1
        # A executes its already-printed batch, spending 180,000, then returns.
        ended_at=c.r.t
        _,_,end=c.next(a)
        assert end==[brain.SUPERSEDED]
        if read_after:
            c.r.t+=1
            c.feed(b,reads,stock(),user(money=220_000,bank=900_000_000))
        c.r.t+=1
        _,new,_=c.next(b)
        after=c.saved()['records']['spend']
        return {'read_after_A':read_after,'first_admitted':first,'before':before,'after':after,
                'next_calls':[s['call'] for s in new],'next_admitted':purchases(new),
                'old_reservation_remaining':any(x[0]==batch_a for x in after.get('out',[])),
                'decisions':len(c.saved()['decisions'])}
    finally:
        c.stack.close()

def loose_selection(read_after=False):
    c=Client(equipment_on=True)
    try:
        a,steps,_=c.start(stock())
        assert [s['call'] for s in steps]==list(equipment.SELECTS)+['item.getUserItems','profile.getUser']
        batch_a=c.state()['held']['id']
        b,_,_=c.next()
        c.r.t+=31
        b,reads,_=c.next(b)
        assert [s['call'] for s in reads]==['item.getUserItems','profile.getUser']
        if read_after:
            c.r.t+=1
            assert c.next(a)[2]==[brain.SUPERSEDED]
        items=stock(**{KUNAI:(30,'NONE',False,None),'more':[('backup',equipment.BACKUP_THROWN[0],50,'THROWN',False,None)]}) if read_after else stock()
        c.feed(b,reads,items,c.me)
        _,out,_=c.next(b)
        saved=c.saved()
        feed=relay.read(os.path.join(c.r.combat.live,'equipped.json'))
        return {'read_after_A':read_after,
                'old_selection_still_loose':any(x[2:3]==['loose'] and x[3]==batch_a for x in saved['budget']['calls']),
                'stale':saved['inventory'].get('stale'),'activity':saved['relay']['activity'],
                'thrown_in_feed':feed['THROWN'],
                'calls':[s['call'] for s in out]}
    finally:
        c.stack.close()

def banking_off():
    cases=[]
    for activity in ('training','session','pvp_hunt'):
        r=Rig(upkeep=True)
        r.world['control']['activities'].update(bank=False)
        r.world.own('restock')['next']=r.t+900
        r.world.own('training')['next']=r.t+900
        r.world.own('equipment')['selected']=list(equipment.PVP1)
        r.world['control']['end_session']=activity=='session'
        out=r.tick(user(money=9_400_000,curEnergy=training.TRIP if activity=='training' else 0,
                        sector=C.HOME_SECTOR if activity=='pvp_hunt' else C.CIRCUIT[0]))
        cases.append({'activity':out['activity'],'calls':r.calls(out),'pocket':r.world.me['money'],
                      'gate':r.brain.gates.check(K.trip(C.HOME_SECTOR)[0],r.world,activity).kind})
    return cases

if __name__=='__main__':
    result={'reservation':[reservation(False),reservation(True)],
            'selection':[loose_selection(False),loose_selection(True)],'banking_off':banking_off()}
    bad,good=result['reservation']
    assert bad['first_admitted']==bad['next_admitted']==180_000 and bad['decisions']==0
    assert not bad['old_reservation_remaining'] and bad['after']['ryo']==49_820_000
    assert good['next_admitted']==0 and good['after']['ryo']==50_000_000
    bad,good=result['selection']
    assert bad['old_selection_still_loose'] and bad['stale'] is None and bad['activity']=='pvp_hunt'
    assert not good['old_selection_still_loose'] and good['thrown_in_feed']==equipment.BACKUP_THROWN[0]
    assert all(x['gate']=='allow' and 'travel.startGlobalMove' in x['calls'] for x in result['banking_off'])
    print(json.dumps(result,indent=2))
