#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
p = ROOT / "forge/test/runner.test.mjs"
text = p.read_text()
start = text.index('test("compatibility: pre-send validation over every manifest under push/, with its known findings", () => {')
end_marker = '''test("compatibility: every manifest committed under push/ still parses", () => {'''
second = text.index(end_marker, start)
# Find the end of the second top-level test. Its body ends immediately before the next test/section.
end = text.index('\n});', second) + len('\n});')
replacement = '''test("compatibility: staged manifests parse and pass Forge pre-send validation", () => {
  const v = new Validator(FIELDS, NESTED_KEYS);
  const dir = new URL("../../push/", import.meta.url);
  for (const f of readdirSync(dir).filter((name) => name.endsWith(".json")).sort()) {
    const m = parseManifest(readFileSync(new URL(f, dir), "utf8"));
    const problems = m.items.flatMap((it) => v.problems(it.entity, it.data, null, { preCreate: it.op === "create" }));
    assert.deepEqual(problems, [], `${f}: ${problems.join(" | ")}`);
  }
});'''
p.write_text(text[:start] + replacement + text[end:])
print("stale push compatibility tests collapsed to the current staging invariant")
