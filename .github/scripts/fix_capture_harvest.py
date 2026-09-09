#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

harvest = ROOT / "skills/building-tnr-content/scripts/harvest.py"
text = harvest.read_text()
old = '''    if not es:\n        if d.get("captures"):\n            print("capture-only bundle (0 write entries): nothing to verify")\n            return 0\n        print("no entries; is this a results bundle?")\n        return 1\n'''
new = '''    if not es:\n        captures = d.get("captures") or []\n        if captures:\n            if forge:\n                failed = [c for c in captures if not isinstance(c, dict) or c.get("ok") is not True]\n                outcome = d.get("outcome")\n                if outcome != "success" or failed:\n                    print(f"UNVERIFIED  capture-only forge bundle: outcome={outcome!r}, "\n                          f"{len(failed)} failed capture(s)")\n                    return 1\n            print("capture-only bundle (0 write entries): nothing to verify")\n            return 0\n        print("no entries; is this a results bundle?")\n        return 1\n'''
if text.count(old) != 1:
    raise SystemExit(f"harvest.py: expected one capture-only verify anchor, found {text.count(old)}")
harvest.write_text(text.replace(old, new, 1))

test = ROOT / "forge/test/harvest.test.mjs"
text = test.read_text().replace('version: "forge 0.2.0"', 'version: "forge 0.2.1"')
anchor = '''test("harvest.py verify passes a clean forge bundle, and only a clean one", async (t) => {\n'''
pos = text.index(anchor)
# Insert the capture-only regression before the existing clean-write verification test.
block = '''test("harvest.py verify agrees with forge on capture-only outcomes", async (t) => {\n  const bin = python();\n  if (!bin) return t.skip("no python3 on PATH");\n\n  async function make(fail) {\n    const game = new FakeGame();\n    if (fail) {\n      const handle = game.handle.bind(game);\n      game.handle = (path, input) => path === "jutsu.getAllNames"\n        ? { ok: false, error: { code: "NOT_FOUND", httpStatus: 404, message: "capture failed", path } }\n        : handle(path, input);\n    }\n    const storage = new MemoryStorage();\n    const d = composeForTest({ game, storage });\n    d.runner.plan({ items: [], capture: { after: [{ proc: "jutsu.getAllNames", input: {} }] } },\n      { jobId: fail ? "capture-bad" : "capture-good", manifestPath: "push/00_forge_readonly_smoke.json" });\n    const summary = await d.runner.run(fail ? "capture-bad" : "capture-good");\n    return { summary, ...(await exportOf(d, fail ? "capture-bad" : "capture-good")) };\n  }\n\n  const dir = mkdtempSync(join(tmpdir(), "forge-harvest-capture-"));\n  try {\n    const good = await make(false);\n    assert.equal(good.summary.outcome, "success");\n    const goodFile = join(dir, "good.json");\n    writeFileSync(goodFile, good.text);\n    const goodVerify = harvest(bin, "verify", goodFile);\n    assert.equal(goodVerify.code, 0, goodVerify.out);\n    assert.match(goodVerify.out, /capture-only bundle/);\n\n    const bad = await make(true);\n    assert.equal(bad.summary.outcome, "failed");\n    assert.equal(bad.bundle.captures[0].ok, false);\n    const badFile = join(dir, "bad.json");\n    writeFileSync(badFile, bad.text);\n    const badVerify = harvest(bin, "verify", badFile);\n    assert.equal(badVerify.code, 1, badVerify.out);\n    assert.match(badVerify.out, /UNVERIFIED\\s+capture-only forge bundle/);\n    assert.match(badVerify.out, /1 failed capture/);\n  } finally { rmSync(dir, { recursive: true, force: true }); }\n});\n\n'''
text = text[:pos] + block + text[pos:]
test.write_text(text)
print("capture-only harvest verification aligned with forge outcome")
