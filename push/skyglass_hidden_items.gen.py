#!/usr/bin/env python3
"""Go-live item edits for the HIDDEN event records, sent early (push/368; director 2026-10-31).

    python3 push/skyglass_hidden_items.gen.py     # writes push/368_skyglass_hidden_items.json

The records in push/skyglass_update.gen.py PRE_GOLIVE_HIDDEN (the four Rare charts, the Lastlight Lantern, the Skyglass
Coffer, Sealed Treasury, Archive Chart Case, Medicine Inro, Sage's Strongbox, Elemental Tool Pouch, Unmarked Cargo) are
our own hidden creates, so players cannot open them (director: "Everything should have pushed hidden"). Their full
go-live edits (approved RUL-2026-10-31-074 text, tier, contents) go now; go-live push/339 keeps only the visible
pre-existing items and the runs. The edits never send `hidden`, so every record stays hidden. 329 refs are resolved
from 329's results bundle (literal ids, L01). Do not hand-edit the output.
"""
import importlib.util
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUNDLE_329 = os.path.join(ROOT, "harvests/inbox/tnr_results_1793424666625.json")
spec = importlib.util.spec_from_file_location("upd", os.path.join(ROOT, "push", "skyglass_update.gen.py"))
U = importlib.util.module_from_spec(spec)
spec.loader.exec_module(U)


def main():
    items = U.hidden_edits(BUNDLE_329)
    U.write(U.EARLY, "skyglass_hidden_items", (
        f"push/{U.EARLY}: the go-live edits to the {len(items)} hidden event records, sent early (director 2026-10-31): "
        "the four Rare charts, the Lastlight Lantern, the Skyglass Coffer, Sealed Treasury, Archive Chart Case, Medicine "
        "Inro, Sage's Strongbox, Elemental Tool Pouch and Unmarked Cargo, with the approved RUL-2026-10-31-074 text, tiers "
        "and contents. No hidden flag is sent, so every record stays hidden. Built from push/329's results bundle "
        + os.path.basename(BUNDLE_329) + " by push/skyglass_hidden_items.gen.py."), items)


if __name__ == "__main__":
    main()
