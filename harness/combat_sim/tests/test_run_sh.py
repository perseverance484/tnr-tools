"""Launcher tests (review items 2 and 3): run.sh never installs, honours only the committed pin, and refuses an
export whose source differs from the pinned tree.

    python3 -m unittest harness/combat_sim/tests/test_run_sh.py

Needs a local game clone holding the pin (TNR_ENGINE_SRC, default /root/work/game); skipped without one. No network.
"""
import os
import shutil
import subprocess
import tempfile
import unittest

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUN = os.path.join(HERE, "run.sh")


def read(path, mode="r"):
    with open(path, mode) as f:
        return f.read()


def write(path, data, mode="w"):
    with open(path, mode) as f:
        f.write(data)


PIN = read(os.path.join(HERE, "ENGINE_PIN")).strip()
SRC = os.environ.get("TNR_ENGINE_SRC", "/root/work/game")


def have_clone():
    return subprocess.run(["git", "-C", SRC, "cat-file", "-e", f"{PIN}^{{commit}}"], capture_output=True).returncode == 0


@unittest.skipUnless(have_clone(), f"no game clone holding {PIN} at {SRC}")
class LauncherTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp(prefix="tnr_run_sh_test_")
        export = subprocess.Popen(["git", "-C", SRC, "archive", PIN, "app"], stdout=subprocess.PIPE)
        subprocess.run(["tar", "-x", "-C", cls.tmp], stdin=export.stdout, check=True)
        export.wait()
        cls.app = os.path.join(cls.tmp, "app")

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def run_sh(self, *args, **env):
        e = {k: v for k, v in os.environ.items() if not k.startswith("TNR_")}
        e.update({"TNR_ENGINE_SRC": SRC, "TNR_ENGINE_APP": self.app})
        e.update(env)
        return subprocess.run([RUN, *args], env=e, capture_output=True, text=True, timeout=120)

    def test_no_dependencies_exits_without_installing(self):
        self.assertFalse(os.path.exists(os.path.join(self.app, "node_modules")))
        r = self.run_sh("selftest.ts")
        self.assertEqual(r.returncode, 3, r.stderr)
        self.assertIn("never installs", r.stderr)
        self.assertFalse(os.path.exists(os.path.join(self.app, "node_modules")))
        self.assertFalse(any(n.startswith("tnr_combat_sim_") for n in os.listdir(self.app)))

    def test_conflicting_pin_override_refused(self):
        r = self.run_sh("selftest.ts", TNR_ENGINE_PIN="0" * 40)
        self.assertEqual(r.returncode, 2, r.stderr)
        self.assertIn("conflicts with the committed ENGINE_PIN", r.stderr)

    def test_matching_pin_override_accepted(self):
        r = self.run_sh("selftest.ts", TNR_ENGINE_PIN=PIN)
        self.assertEqual(r.returncode, 3, r.stderr)  # gets as far as the missing dependencies

    def test_changed_source_file_refused(self):
        path = os.path.join(self.app, "src/libs/combat/turn.ts")
        orig = read(path, "rb")
        try:
            write(path, b"\n// tampered\n", "ab")
            r = self.run_sh("selftest.ts")
            self.assertEqual(r.returncode, 2, r.stderr)
            self.assertIn("src/libs/combat/turn.ts", r.stderr + r.stdout)
        finally:
            write(path, orig, "wb")

    def test_extra_source_file_refused(self):
        path = os.path.join(self.app, "src/libs/combat/extra_patch.ts")
        try:
            write(path, "export {};\n")
            r = self.run_sh("selftest.ts")
            self.assertEqual(r.returncode, 2, r.stderr)
        finally:
            os.remove(path)

    def test_missing_source_file_refused(self):
        path = os.path.join(self.app, "src/libs/combat/turn.ts")
        orig = read(path, "rb")
        try:
            os.remove(path)
            r = self.run_sh("selftest.ts")
            self.assertEqual(r.returncode, 2, r.stderr)
        finally:
            write(path, orig, "wb")


if __name__ == "__main__":
    unittest.main()
