"""Offline Lane A observations for AP2 at 988c56cc; no connector or real run-lock tool.

Run from the repository root with PYTHONPATH=. All state is temporary. The assertions
confirm the reported observations on the frozen target, including passing controls;
they are not assertions of the desired corrected behavior.
"""
import contextlib
import io
import json
import os
from unittest import mock

from player import brain, calls as K, config as C, relay, runlock
from player.activities import equipment, training
from player.tests.support import Rig, user, res
from player.tests.test_upkeep import stock, PANACEA, PILL, queue, jutsu, T, KUNAI
from player.tests.test_runlock import on_the_accounts_folder
from player.tests.test_relay import token_of
from player.tests.test_rereview4 import Killed, dies_before_the_receipt
from player.world import utc_day

def calls(out):
    return [s for s in out['steps'] if 'call' in s]

def cap_case(left):
    r = Rig(upkeep=True)
    r.world['control']['activities'] = {'training': False, 'equipment': False}
    me = user(money=200_000, bank=900_000_000)
    r.tick(me)
    r.world['records']['spend'] = {'day': utc_day(r.t), 'ryo': C.DAILY_CAP-left}
    out = r.tick(stock(**{PANACEA: (0, 'ITEM_3', False, None), PILL: None}), me)
    buys = [s for s in calls(out) if s['call'] == 'item.buy']
    total = sum(s['meta']['ryo'] for s in buys)
    return {'remaining': left, 'admitted_ryo': total, 'buys': [s['input'] for s in buys],
            'decisions': len(r.world['decisions'])}

def cash_trip(energy, ending=False):
    r = Rig(upkeep=True)
    r.world.own('restock')['next'] = r.t + 900
    r.world.own('equipment')['selected'] = list(equipment.PVP1)
    r.world['control']['end_session'] = ending
    # Energy crosses the trip threshold while the queue fill completes.
    road = {'money': 150_000, 'bank': 900_000_000, 'curEnergy': min(energy, training.TRIP - 1)}
    if not ending:
        r.tick(user(**road))
        out = r.tick(queue(), jutsu({T[0]: 3}), user(**road))
        assert calls(out)[0]['call'] == 'bank.toPocket', out
        drawn = {**road, 'money': C.TRAINING_DRAW, 'bank': 890_150_000}
        out = r.tick(res('bank.toPocket', {'success': True}, calls(out)[0]['input']), user(**drawn))
        assert calls(out)[0]['call'] == 'jutsu.startTraining', out
        replies = [res(s['call'], {'success': True}, s['input']) for s in calls(out) if s['call'] == 'jutsu.startTraining']
        out = r.tick(*replies, user(**{**drawn, 'money': 9_400_000, 'curEnergy': energy}))
    else:
        out = r.tick(user(money=9_400_000, curEnergy=energy))
    return {'energy': energy, 'ending': ending, 'pocket': r.world.me['money'],
            'activity': out['activity'], 'calls': [s['call'] for s in calls(out)],
            'bank_available': r.brain.reg.activities['bank'].available(r.world)}

def lease_delivery(oversleep=0, crowded=True, renew=False, restart=None, start_before=65):
    r = Rig()
    r.world.absorb([user()._replace(at=r.t)])
    tool = on_the_accounts_folder(r)
    r.brain.lock.hold()
    expires = r.brain.lock.state['expires']
    r.t = expires - start_before
    tool.broken = None if renew else 'offline renewal'
    if crowded:
        r.world['budget']['calls'] = [[r.t, 'world'] for _ in range(C.WORLD_CAP)]
    r.world.save()
    real, handled = brain.Brain, []
    def make(live):
        b = real(live, clock=lambda: r.t, combat=r.combat, gates=r.brain.gates)
        b.lock = runlock.RunLock(b.world, tool=tool, rehearsal=False)
        handle = b.handle
        def counted(*args, **kwargs):
            handled.append(1)
            return handle(*args, **kwargs)
        b.handle = counted
        return b
    waits, interrupted = [], False
    def sleep(n):
        nonlocal interrupted
        waits.append(n)
        if restart == 'pending' and n >= 1 and not interrupted:
            interrupted = True
            raise Killed
        r.t += n + (oversleep if n >= 1 else 0)
    def nxt(token=None):
        out = io.StringIO()
        brain.next_batch(r.dir, token, out, sleep)
        return out.getvalue().splitlines()
    with contextlib.ExitStack() as stack:
        stack.enter_context(mock.patch.object(brain, 'Brain', make))
        stack.enter_context(mock.patch.object(brain.time, 'time', lambda: r.t))
        stack.enter_context(mock.patch.dict(os.environ, {'TNR_PLAYER_NO_DAEMON': '1',
            'TNR_TRANSCRIPT': os.path.join(r.dir, 'absent'), 'TNR_PLAYER_FIGHTS': os.path.join(r.dir, 'fights')}))
        token = token_of(nxt()[0])
        if restart == 'receipt':
            try:
                with dies_before_the_receipt(r):
                    nxt(token)
            except Killed:
                pass
            else:
                raise AssertionError('receipt interruption did not run')
            r.t = expires + 70
            lines = nxt(token)
        elif restart == 'pending':
            try:
                nxt(token)
            except Killed:
                pass
            else:
                raise AssertionError('pending interruption did not run')
            state = relay.read(os.path.join(r.dir, 'client.json'))
            r.t = state['pending']['ready_at'] + 5
            lines = nxt(token)
        else:
            lines = nxt(token)
    sent = [json.loads(line)['call'] for line in lines if line.startswith('{') and 'call' in json.loads(line)]
    confirmed = relay.read(os.path.join(r.dir, 'world.json'))['records']['run_lock'].get('expires', 0)
    return {'oversleep': oversleep, 'crowded': crowded, 'renew': renew, 'restart': restart, 'waits': waits,
            'printed_vs_expiry': round(r.t-expires, 2), 'calls': sent,
            'before_confirmed_cutoff': r.t < confirmed-runlock.STOP_MARGIN,
            'handle_calls': len(handled),
            'tool_calls': [a[0] for a in tool.asked]}

def equipment_feed():
    r = Rig(upkeep=True)
    r.world['control']['activities']['training'] = False
    me = user(money=100_000)
    r.tick(me)
    prior = stock()
    # Simulate switching between loadouts with different thrown weapons. This does
    # not assert the current contents of any live account's loadout.
    out = r.tick(prior, me)
    assert [s['call'] for s in calls(out)][:2] == list(equipment.SELECTS), out
    sent = [s['call'] for s in calls(out)]
    out = r.tick(*[res(s['call'], {'success': True}, s['input']) for s in calls(out) if s['call'] in equipment.SELECTS], me)
    before = json.load(open(os.path.join(r.combat.live, 'equipped.json')))
    # Control: a later item read of the now-selected PvP 1 loadout refreshes the feed.
    r.tick(stock(**{KUNAI: (30, 'NONE', False, None),
                   'more': [('backup', equipment.BACKUP_THROWN[0], 50, 'THROWN', False, None)]}), me)
    after = json.load(open(os.path.join(r.combat.live, 'equipped.json')))
    return {'selection_batch': sent, 'after_selection_activity': out['activity'],
            'before_item_read': before['THROWN'], 'after_item_read': after['THROWN']}

if __name__ == '__main__':
    result = {'daily_cap': [cap_case(n) for n in (170_000, 180_000)],
              'cash': [cash_trip(0), cash_trip(training.TRIP), cash_trip(0, True)],
              'lease': [lease_delivery(crowded=False), lease_delivery(), lease_delivery(150),
                        lease_delivery(renew=True), lease_delivery(start_before=60),
                        lease_delivery(restart='pending'), lease_delivery(restart='receipt')],
              'equipment': equipment_feed()}
    assert result['daily_cap'][0]['admitted_ryo'] > result['daily_cap'][0]['remaining']
    assert result['daily_cap'][0]['decisions'] == 0
    assert result['daily_cap'][1]['admitted_ryo'] == result['daily_cap'][1]['remaining']
    assert [x['activity'] for x in result['cash']] == ['bank', 'training', 'session']
    assert all(x['bank_available'] for x in result['cash'][1:])
    for i in (0, 1, 2, 5, 6):
        assert result['lease'][i]['calls'] and not result['lease'][i]['before_confirmed_cutoff']
    assert result['lease'][3]['calls'] and result['lease'][3]['before_confirmed_cutoff']
    assert not result['lease'][4]['calls']
    assert result['lease'][6]['handle_calls'] == 1
    assert result['equipment']['before_item_read'] != result['equipment']['after_item_read']
    assert 'item.getUserItems' not in result['equipment']['selection_batch']
    print(json.dumps(result, indent=2))
