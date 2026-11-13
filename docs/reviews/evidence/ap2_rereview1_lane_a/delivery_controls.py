"""Additional H1 controls: replacement relays and the resident serve path, offline."""
import io
import unittest
from player import brain, relay
from player.tests.test_ap2_review import H1TheLeaseAtDelivery
from player.tests.test_relay import token_of
from player.tests.test_rereview4 import Killed
from player.tests.test_rereview6 import calls_of

class Delivery(unittest.TestCase):
    def harness(self):
        h=H1TheLeaseAtDelivery()
        self.addCleanup(h.doCleanups)
        return h

    def replacement(self, expired):
        h=self.harness()
        h.start(before=600)
        h.dies_in_the_wait=True
        with self.assertRaises(Killed):
            h.next(h.token)
        pending=h.client()['pending']
        expected=[s['call'] for s in pending['steps'] if 'call' in s]
        new=token_of(h.next()[0])
        h.r.t=h.cutoff+1 if expired else pending['ready_at']
        lines=h.next(new)
        self.assertEqual(calls_of(lines),[] if expired else expected)
        self.assertEqual(h.next(h.token),[brain.SUPERSEDED])
        self.assertEqual(h.handled,2 if expired else 1)

    def test_replacement_inside_lease_gets_the_pending_batch(self):
        self.replacement(False)

    def test_replacement_after_cutoff_gets_no_calls(self):
        self.replacement(True)

    def test_resident_answer_lapses_while_client_waits(self):
        h=self.harness()
        h.start(before=75)
        resident=brain.Brain(h.r.dir)
        lock=brain._lock(h.r.dir)
        self.assertIsNotNone(lock)
        self.addCleanup(lock.close)
        answered=[]
        def sleep(n):
            for path in relay.pending_requests(h.r.dir):
                brain.serve(resident,h.r.dir,path)
                answered.append(1)
            h.r.t+=n+(150 if n>=1 else 0)
        out=io.StringIO()
        brain.next_batch(h.r.dir,h.token,out,sleep)
        self.assertEqual(answered,[1])
        self.assertGreater(h.r.t,h.expires)
        self.assertEqual(calls_of(out.getvalue().splitlines()),[])
        self.assertIsNone(h.client()['pending'])
        self.assertEqual(len(h.client()['unprinted']),1)

if __name__=='__main__':
    unittest.main(defaultTest='Delivery')
