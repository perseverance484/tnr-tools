#!/usr/bin/env python3
"""Build deterministic, bounded skill ZIPs from tracked runtime files."""

from __future__ import annotations

import hashlib
import os
import subprocess
import sys
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

ROOT = Path(__file__).resolve().parents[2]
SKILLS = ROOT / "skills"
DIST = ROOT / "dist"
ZIP_TIME = (1980, 1, 1, 0, 0, 0)
MAX_ZIP_BYTES = 2 * 1024 * 1024
ARCHIVE_ONLY_DIRS = {("data", "rank_icons"), ("data", "frames")}


def tracked_files(skill: Path):
    prefix = skill.relative_to(ROOT).as_posix()
    output = subprocess.check_output(
        ["git", "ls-files", "-z", "--", prefix], cwd=ROOT
    ).decode()
    return [ROOT / path for path in output.split("\0") if path]


def packaged_files(skill: Path):
    for path in tracked_files(skill):
        rel = path.relative_to(skill)
        if rel.name.endswith("_raw.png") or rel.parts[:2] in ARCHIVE_ONLY_DIRS:
            continue
        yield path


def add_file(zf: ZipFile, root: Path, path: Path) -> None:
    info = ZipInfo(path.relative_to(root).as_posix(), ZIP_TIME)
    info.create_system = 3
    info.external_attr = (0o100755 if os.access(path, os.X_OK) else 0o100644) << 16
    info.compress_type = ZIP_DEFLATED
    zf.writestr(info, path.read_bytes(), compress_type=ZIP_DEFLATED, compresslevel=9)


def main() -> int:
    DIST.mkdir(exist_ok=True)
    oversized = []
    for skill in sorted(path for path in SKILLS.iterdir() if path.is_dir()):
        out = DIST / f"{skill.name}.zip"
        with ZipFile(out, "w", compression=ZIP_DEFLATED, compresslevel=9) as zf:
            for path in packaged_files(skill):
                add_file(zf, skill, path)
        size = out.stat().st_size
        digest = hashlib.sha256(out.read_bytes()).hexdigest()[:12]
        print(f"{out.relative_to(ROOT)}  {size} bytes  sha256:{digest}")
        if size > MAX_ZIP_BYTES:
            oversized.append((out.relative_to(ROOT), size))

    for path, size in oversized:
        print(f"{path} is {size} bytes; skill ZIPs must stay at or below 2 MiB", file=sys.stderr)
    return 1 if oversized else 0


if __name__ == "__main__":
    raise SystemExit(main())
