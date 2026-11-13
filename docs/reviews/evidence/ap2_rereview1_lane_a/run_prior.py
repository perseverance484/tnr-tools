"""Call the previous report's unchanged observation functions, without its defect assertions."""
import json
import prior

result = {
    'daily_cap': [prior.cap_case(n) for n in (170000, 180000)],
    'cash': [prior.cash_trip(0), prior.cash_trip(prior.training.TRIP), prior.cash_trip(0, True)],
    'lease': [prior.lease_delivery(crowded=False), prior.lease_delivery(), prior.lease_delivery(150),
              prior.lease_delivery(renew=True), prior.lease_delivery(start_before=60),
              prior.lease_delivery(restart='pending'), prior.lease_delivery(restart='receipt')],
    'equipment': prior.equipment_feed(),
}
print(json.dumps(result, indent=2))
