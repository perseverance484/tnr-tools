"""Observe the prior review's unchanged cases without its old defect assertions."""
import json
import overlap

result = {
    'reservation': [overlap.reservation(False), overlap.reservation(True)],
    'selection': [overlap.loose_selection(False), overlap.loose_selection(True)],
    'banking_off': overlap.banking_off(),
}
assert all(r['next_admitted'] == 0 and r['old_reservation_remaining'] for r in result['reservation'])
assert all(r['stale'] and r['activity'] != 'pvp_hunt' for r in result['selection'])
assert all(r['gate'] == 'refuse' and 'travel.startGlobalMove' not in r['calls'] for r in result['banking_off'])
print(json.dumps(result, indent=2))
