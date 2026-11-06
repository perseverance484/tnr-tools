#!/usr/bin/env python3
"""Write exports/moe_fx_final.json: the final tuning job's assets (push/mother_of_echoes.gen.py FX4), with type and
frame count read from the files themselves (QA S11: written by a script, never by hand).

    python3 art/mother_of_echoes_fx/build_final_meta.py
"""
import importlib.util
import json
import os

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
_s = importlib.util.spec_from_file_location("moe", os.path.join(ROOT, "push", "mother_of_echoes.gen.py"))
M = importlib.util.module_from_spec(_s)
_s.loader.exec_module(M)


def main():
    rows = []
    for k, (f, _name) in sorted(M.FX4.items()):
        p = os.path.join(ROOT, M.FXDIR, f)
        if not os.path.exists(p):
            raise SystemExit(f"FX4 {k}: {f} missing")
        im = Image.open(p)
        static = f.startswith("tile_")
        rows.append({"file": M.FXDIR + f, "type": "STATIC" if static else "ANIMATION",
                     "frames": 1 if static else im.height // im.width, "speed": None if static else 50,
                     "bytes": os.path.getsize(p)})
    with open(os.path.join(ROOT, M.FX4_META), "w") as fh:
        json.dump({"source": "art/mother_of_echoes_fx/build_final_meta.py (from push/mother_of_echoes.gen.py FX4)",
                   "assets": rows}, fh, indent=1)
        fh.write("\n")
    print(len(rows), "assets")


if __name__ == "__main__":
    main()
