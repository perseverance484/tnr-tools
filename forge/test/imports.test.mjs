// The import-direction gate, and proof that it is not vacuous.
import { test } from "node:test";
import assert from "node:assert/strict";
import { mkdtempSync, mkdirSync, writeFileSync, rmSync, cpSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { execFileSync } from "node:child_process";
import { checkImports } from "../tools/check_imports.mjs";

const FORGE = join(dirname(fileURLToPath(import.meta.url)), "..");

test("no module imports against the required direction", () => {
  const { files, edges, violations } = checkImports();
  assert.ok(files > 0 && edges > 0, "the gate must actually scan a population");
  assert.deepEqual(violations, [], "import-direction violations:\n" + violations.join("\n"));
});

test("the gate reports the population it scanned, so zero is a measurement", () => {
  const { files, edges } = checkImports();
  assert.ok(files >= 30, `only ${files} modules scanned; the walker is probably missing a directory`);
  assert.ok(edges >= 30, `only ${edges} cross-layer imports scanned`);
});

test("the gate catches a violation when one exists", () => {
  // Copy src into a scratch tree, inject one prohibited edge in each direction, and run the gate
  // against it. A gate nobody has ever seen fail is not evidence.
  const root = mkdtempSync(join(tmpdir(), "forge-imports-"));
  try {
    mkdirSync(join(root, "tools"), { recursive: true });
    cpSync(join(FORGE, "src"), join(root, "src"), { recursive: true });
    cpSync(join(FORGE, "tools", "check_imports.mjs"), join(root, "tools", "check_imports.mjs"));
    writeFileSync(join(root, "src", "runner", "_leak.mjs"), 'import { h } from "../ui/dom.mjs";\nexport const leak = h;\n');
    writeFileSync(join(root, "src", "core", "_leak.mjs"), 'import { h } from "../ui/dom.mjs";\nexport const leak = h;\n');

    let failed = false, output = "";
    try {
      execFileSync(process.execPath, [join(root, "tools", "check_imports.mjs")], { encoding: "utf8", stdio: ["ignore", "pipe", "pipe"] });
    } catch (e) {
      failed = true;
      output = String(e.stdout || "") + String(e.stderr || "");
    }
    assert.ok(failed, "the gate must exit nonzero on a violation");
    assert.match(output, /runner\/_leak\.mjs \(execution\) imports/);
    assert.match(output, /core\/_leak\.mjs \(core\) imports/);
    assert.match(output, /2 violation\(s\)/);
  } finally {
    rmSync(root, { recursive: true, force: true });
  }
});

test("the userscript host lives under hosts/, not in the view", async () => {
  const mod = await import("../src/hosts/userscript/takeover.mjs");
  for (const name of ["arm", "disarm", "isArmed", "mountHost", "entryTakeover", "onEntryPath", "pageAuthRuntime"]) {
    assert.equal(typeof mod[name], "function", `${name} must survive the move`);
  }
});
