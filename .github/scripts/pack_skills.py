#!/usr/bin/env python3
"""Build deterministic skill ZIPs."""

from __future__ import annotations

import hashlib
import os
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

ROOT = Path(__file__).resolve().parents[2]
SKILLS = ROOT / "skills"
DIST = ROOT / "dist"
ZIP_TIME = (1980, 1, 1, 0, 0, 0)


def add_file(zf: ZipFile, root: Path, path: Path) -> None:
    info = ZipInfo(path.relative_to(root).as_posix(), ZIP_TIME)
    info.create_system = 3
    mode = 0o100755 if os.access(path, os.X_OK) else 0o100644
    info.external_attr = mode << 16
    info.compress_type = ZIP_DEFLATED
    zf.writestr(info, path.read_bytes(), compress_type=ZIP_DEFLATED, compresslevel=9)


def main() -> int:
    DIST.mkdir(exist_ok=True)
    for skill in sorted(p for p in SKILLS.iterdir() if p.is_dir()):
        out = DIST / f"{skill.name}.zip"
        with ZipFile(out, "w", compression=ZIP_DEFLATED, compresslevel=9) as zf:
            for path in sorted(p for p in skill.rglob("*") if p.is_file()):
                add_file(zf, skill, path)
        digest = hashlib.sha256(out.read_bytes()).hexdigest()[:12]
        print(f"{out.relative_to(ROOT)}  {out.stat().st_size} bytes  sha256:{digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
