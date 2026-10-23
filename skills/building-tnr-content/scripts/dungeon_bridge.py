"""Use Forge's scoped dungeon contract (forge/src/dungeon/); 45d has no dungeon schema to fall back on."""
import json
from pathlib import Path
import subprocess


def problems(entry):
    root = Path(__file__).resolve().parents[3]
    tool = root / "forge/tools/validate_dungeon.mjs"
    if not tool.is_file():
        return ["dungeon validation requires a tnr-tools checkout with forge/tools/validate_dungeon.mjs and Node 24"]
    try:
        run = subprocess.run(["node", str(tool)], input=json.dumps(entry), text=True,
                             capture_output=True, timeout=30, check=True)
        result = json.loads(run.stdout)
        if not isinstance(result, list):
            raise ValueError("validator did not return a problem list")
        return result
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        return [f"dungeon validator unavailable: {exc}"]
