#!/usr/bin/env python3
"""Build deterministic skill ZIPs from tracked files."""

from __future__ import annotations

import hashlib
import os
import subprocess
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

ROOT = Path(__file__).resolve().parents[2]
SKILLS = ROOT / "skills"
DIST = ROOT / "dist"
ZIP_TIME = (1980, 1, 1, 0, 0, 0)


def tracked_files(skill: Path):
    prefix = skill.relative_to(ROOT).as_posix()
    output = subprocess.check_output(
        ["git", "ls-files", "-z", "--", prefix], cwd=ROOT
    ).decode()
    return [ROOT / path for path in output.split("\0") if path]


def add_file(zf: ZipFile, root: Path, path: Path) -> None:
    info = ZipInfo(path.relative_to(root).as_posix(), ZIP_TIME)
    info.create_system = 3
    info.external_attr = (0o100755 if os.access(path, os.X_OK) else 0o100644) << 16
    info.compress_type = ZIP_DEFLATED
    zf.writestr(info, path.read_bytes(), compress_type=ZIP_DEFLATED, compresslevel=9)


def main() -> int:
    DIST.mkdir(exist_ok=True)
    for skill in sorted(path for path in SKILLS.iterdir() if path.is_dir()):
        out = DIST / f"{skill.name}.zip"
        with ZipFile(out, "w", compression=ZIP_DEFLATED, compresslevel=9) as zf:
            for path in tracked_files(skill):
                add_file(zf, skill, path)
        digest = hashlib.sha256(out.read_bytes()).hexdigest()[:12]
        print(f"{out.relative_to(ROOT)}  {out.stat().st_size} bytes  sha256:{digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
