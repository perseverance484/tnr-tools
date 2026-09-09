#!/usr/bin/env python3
"""Pin changed userscript bundles to the commit that shipped them."""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TARGETS = (
    ("builder_bundle.js", "builder_loader_user.js", None),
    ("forge_bundle.js", "forge_loader_user.js", "forge/package.json"),
)


def pin(bundle: str, loader: str, version_file: str | None, sha: str) -> None:
    path = ROOT / loader
    text = path.read_text()
    url = f"https://cdn.jsdelivr.net/gh/perseverance484/tnr-tools@{sha}/{bundle}"
    text, count = re.subn(
        rf"(// @require\s+)\S*{re.escape(bundle)}\S*",
        lambda match: match.group(1) + url,
        text,
    )
    if count != 1:
        raise RuntimeError(f"expected one @require for {bundle} in {loader}, found {count}")

    text = re.sub(r"^// @x-unpinned-until-release.*\n", "", text, flags=re.M)
    if version_file:
        version = json.loads((ROOT / version_file).read_text())["version"]
        text, count = re.subn(
            r"(// @version\s+)\S+",
            lambda match: match.group(1) + version,
            text,
            count=1,
        )
        if count != 1:
            raise RuntimeError(f"missing @version in {loader}")

    path.write_text(text)
    print(f"pinned {loader} -> {url}")


def main() -> int:
    sha = os.environ.get("GITHUB_SHA")
    if not sha:
        print("GITHUB_SHA is required", file=sys.stderr)
        return 2

    changed = set(sys.stdin.read().splitlines())
    pinned = 0
    for bundle, loader, version_file in TARGETS:
        if bundle in changed:
            pin(bundle, loader, version_file, sha)
            pinned += 1

    if not pinned:
        print("no changed bundle to pin", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
