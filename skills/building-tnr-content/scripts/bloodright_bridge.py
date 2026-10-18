"""Use Forge's scoped Bloodright contract; never fall back to stale AllTags constructors."""
import json
from pathlib import Path
import subprocess


def problems(value):
    root = Path(__file__).resolve().parents[3]
    tool = root / "forge/tools/validate_bloodright.mjs"
    if not tool.is_file():
        return ["Bloodright validation requires a tnr-tools checkout with forge/tools/validate_bloodright.mjs and Node 24; no legacy-schema fallback"]
    try:
        run = subprocess.run(["node", str(tool)], input=json.dumps(value), text=True,
                             capture_output=True, timeout=30, check=True)
        result = json.loads(run.stdout)
        if not isinstance(result, list):
            raise ValueError("validator did not return a problem list")
        return result
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        return [f"Bloodright validator unavailable: {exc}"]


def package_problems(value):
    """Offline check of a bloodrightCollection package through Forge's own prepareCollection."""
    root = Path(__file__).resolve().parents[3]
    tool = root / "forge/tools/validate_bloodright_package.mjs"
    if not tool.is_file():
        return ["Bloodright package validation requires a tnr-tools checkout with forge/tools/validate_bloodright_package.mjs"]
    try:
        run = subprocess.run(["node", str(tool), str(root)], input=json.dumps(value), text=True,
                             capture_output=True, timeout=120, check=True)
        result = json.loads(run.stdout)
        if not isinstance(result, list):
            raise ValueError("validator did not return a problem list")
        return result
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        return [f"Bloodright package validator unavailable: {exc}"]
