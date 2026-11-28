"""Additional offline controls for AP2's owed rows and the session wait.

Client is the previous review's unchanged real next/put harness. All worlds are
temporary; no connector or real run-lock tool is used.
"""
import io
import json
import unittest
from player import brain, config as C, calls as K
from player.activities import equipment
from player.tests.support import Rig, res, user
from player.tests.test_rereview4 import Killed, dies_before_the_receipt
from player.tests.test_upkeep import stock, PANACEA, PILL, KUNAI
from overlap import Client, purchases

class Checks(unittest.TestCase):
    def test_both_spending_controls_need_a_later_successful_profile(self):
        for read_after in (False, True):
            with self.subTest(read_after=read_after):
                c=Client(pocket=400_000)
                try:
                    short=stock(**{PANACEA:(0,'ITEM_3',False,None),PILL:None})
                    a,first,_=c.start(short)
                    self.assertEqual(purchases(first),180_000)
                    aid=c.state()['held']['id']
                    b,_,_=c.next()
                    b,reads,_=c.next(b)
                    if not read_after:
                        c.feed(b,reads,short,c.me)
                    c.r.t+=1
                    self.assertEqual(c.next(a)[2],[brain.SUPERSEDED])
                    if read_after:
                        c.feed(b,reads,stock(),user(money=220_000,bank=900_000_000))
                    b,steps,_=c.next(b)
                    self.assertEqual(purchases(steps),0)
                    self.assertEqual(c.saved()['records']['spend']['out'],[[aid,180_000.0,True]])
                    # The next request's profile fails: the marked reservation must survive.
                    for i,s in enumerate(steps,1):
                        reply='Error: read unavailable' if s['call']=='profile.getUser' else json.dumps({'success':False})
                        self.assertEqual(brain.put(c.r.dir,b,i,reply),0)
                    c.r.t+=1
                    b,steps,_=c.next(b)
                    self.assertEqual(c.saved()['records']['spend']['out'],[[aid,180_000.0,True]])
                    self.assertEqual(purchases(steps),0)
                    self.assertIn('profile.getUser',[s['call'] for s in steps])
                    c.feed(b,steps,stock(),user(money=220_000,bank=900_000_000))
                    c.r.t+=1
                    _,steps,_=c.next(b)
                    spend=c.saved()['records']['spend']
                    self.assertEqual((spend['ryo'],spend['out'],purchases(steps)),(C.DAILY_CAP,[],0))
                finally:
                    c.stack.close()

    def test_equipment_control_receipt_and_failed_refresh_keep_the_obligation(self):
        c=Client(equipment_on=True)
        try:
            a,_,_=c.start(stock())
            aid=c.state()['held']['id']
            b,_,_=c.next()
            c.r.t+=31
            b,reads,_=c.next(b)
            self.assertEqual(c.next(a)[2],[brain.SUPERSEDED])
            changed=stock(**{KUNAI:(30,'NONE',False,None),'more':[('backup',equipment.BACKUP_THROWN[0],50,'THROWN',False,None)]})
            c.feed(b,reads,changed,c.me)
            with dies_before_the_receipt(c.r), self.assertRaises(Killed):
                c.next(b)
            self.assertEqual(c.saved()['inventory']['stale'],[[aid,None,True]])
            b,refresh,_=c.next(b)  # receipt re-delivery does not pay off the mark
            self.assertEqual(c.saved()['inventory']['stale'],[[aid,None,True]])
            for i,s in enumerate(refresh,1):
                data='Error: item read unavailable' if s['call']=='item.getUserItems' else json.dumps(c.me.data)
                self.assertEqual(brain.put(c.r.dir,b,i,data),0)
            c.r.t+=31
            b,refresh,_=c.next(b)
            self.assertEqual(c.saved()['inventory']['stale'],[[aid,None,True]])
            self.assertEqual([s['call'] for s in refresh],['item.getUserItems','profile.getUser'])
            c.feed(b,refresh,changed,c.me)
            c.r.t+=1
            c.next(b)
            self.assertFalse(c.saved()['inventory'].get('stale'))
            self.assertEqual(c.saved()['relay']['activity'],'pvp_hunt')
        finally:
            c.stack.close()

    def test_two_batch_rows_are_released_selectively_across_requests_and_restarts(self):
        # Seed two outstanding batches to test the shared module's per-batch rule.
        # Reads in a request must not discharge rows first marked by that request.
        r=Rig(mode='guard',upkeep=True)
        r.world['control']['activities'].update(restock=False,training=False,bank=False,repair=False)
        r.world.absorb([user()._replace(at=r.t)])
        r.world['budget'].update(batch='current',calls=[
            [r.t,'world','loose',bid,r.t,bid+'-1'] for bid in ('A','B')])
        r.world['records']['spend']['out']=[['A',100],['B',200]]
        r.world['inventory']['stale']=[['A',None],['B',None]]
        last='current'
        for i,(ended,expected) in enumerate((('A',[['A',100,True],['B',200]]),
                                             ('B',[['B',200,True]]),(None,[])),1):
            r.t+=1
            req={'id':f'R{i}','relay':'r','seq':i,'held':{'id':last,'token':f'r-{i}'},
                 'ended':[[ended,r.t,ended+'-1','back']] if ended else []}
            r.brain.handle([stock()._replace(at=r.t),user()._replace(at=r.t)],ask=req)
            self.assertEqual(r.world['records']['spend']['out'],expected)
            self.assertEqual(r.world['inventory'].get('stale',[]),[[x[0],None]+x[2:] for x in expected])
            last=req['id']
            r.new_brain()
            self.assertEqual(r.world['records']['spend']['out'],expected)

    def test_session_waits_through_bank_refusal_then_leaves_at_exact_limit(self):
        r=Rig(upkeep=True)
        r.world['control']['end_session']=True
        r.world['control']['activities'].update(training=False,equipment=False,restock=False)
        high=user(money=9_400_000,sector=C.CIRCUIT[0])
        out=r.tick(high)
        self.assertEqual(out['activity'],'bank')
        step=next(s for s in out['steps'] if s.get('call')=='bank.toBank')
        out=r.tick(res('bank.toBank',{'success':False,'message':'unavailable'},step['input']),high)
        self.assertEqual((out['activity'],r.calls(out)),('session',['profile.getUser']))
        self.assertGreaterEqual(out['hold'],30)
        self.assertIn('deposit is tried again later',out['note'])
        r.new_brain()
        out=r.tick(high)
        self.assertEqual((out['activity'],r.calls(out)),('session',['profile.getUser']))
        out=r.tick(user(money=C.POCKET_LIMIT,sector=C.CIRCUIT[0]))
        self.assertEqual((out['activity'],r.calls(out)[0]),('session','travel.startGlobalMove'))

if __name__=='__main__':
    unittest.main()
