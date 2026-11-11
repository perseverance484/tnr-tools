#!/usr/bin/env python3
"""Entry point the relay runs: pilot.py, or the last copy that passed tests/test_pilot.py if pilot.py fails to load
or crashes (2026-11-11: a half-finished edit to pilot.py stopped the live pilot mid-hunt)."""
import os
import runpy
import sys
import traceback

HERE = os.path.dirname(os.path.abspath(__file__))
GOOD = os.path.join(HERE, "pilot_good.py")
sys.path.insert(0, HERE)
sys.argv[0] = os.path.join(HERE, "pilot.py")
try:
    runpy.run_path(os.path.join(HERE, "pilot.py"), run_name="__main__")
except SystemExit:
    raise
except BaseException:  # noqa: BLE001
    if not os.path.exists(GOOD):
        raise
    sys.stderr.write("pilot.py failed, running the last good copy:\n" + traceback.format_exc(limit=2))
    runpy.run_path(GOOD, run_name="__main__")
