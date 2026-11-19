"""Stdlib tests for tools/pull_live.py: routing, filtered-call skipping, persisted outputs, unsafe paths."""
import json
import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "tools"))
import pull_live  # noqa: E402


def _line(kind, block, ts="2026-11-18T22:00:00Z"):
    role = "assistant" if kind == "tool_use" else "user"
    return json.dumps({"timestamp": ts, "message": {"role": role, "content": [block]}})


def _use(uid, endpoint, inp, **extra):
    return _line("tool_use", {"type": "tool_use", "id": uid, "name": "mcp__Tnr__callEndpoint",
                              "input": {"endpointName": endpoint, "input": inp, **extra}})


def _result(uid, text, is_error=False):
    return _line("tool_result", {"type": "tool_result", "tool_use_id": uid, "is_error": is_error,
                                 "content": [{"type": "text", "text": text}]})


class PullLiveTest(unittest.TestCase):
    def transcript(self, lines):
        d = tempfile.mkdtemp()
        p = os.path.join(d, "sess.jsonl")
        with open(p, "w") as f:
            f.write("\n".join(lines) + "\n")
        return p

    def test_routes_and_skips(self):
        p = self.transcript([
            _use("a", "profile.getAi", {"userId": "AI1"}), _result("a", json.dumps({"userId": "AI1", "level": 14})),
            _use("b", "jutsu.get", {"id": "J1"}, select=["name"]), _result("b", json.dumps({"name": "x"})),
            _use("c", "item.getUserItem", {"id": "U1"}), _result("c", json.dumps({"id": "U1", "item": {"id": "I1"}})),
            _use("d", "pets.getPet", {"petId": "P1"}), _result("d", json.dumps({"pet": {"id": "P1"}})),
            _use("e", "jutsu.get", {"id": "J2"}), _result("e", "not json"),
            _use("f", "jutsu.get", {"id": "J3"}), _result("f", json.dumps({"id": "J3"}), is_error=True),
            _use("g", "quests.get", {"id": "Q"}), _result("g", json.dumps({"id": "Q"})),
        ])
        out = pull_live.collect(p)
        self.assertEqual(sorted(out), ["ai/AI1.json", "items/I1.json", "pets/P1.json", "user_items/U1.json"])
        self.assertEqual(out["ai/AI1.json"]["data"]["level"], 14)
        self.assertEqual(out["ai/AI1.json"]["_source"]["readAt"], "2026-11-18T22:00:00Z")
        self.assertEqual(out["items/I1.json"]["_source"]["via"], "item.getUserItem.item")

    def test_later_answer_wins(self):
        p = self.transcript([
            _use("a", "jutsu.get", {"id": "J1"}), _result("a", json.dumps({"v": 1})),
            _use("b", "jutsu.get", {"id": "J1"}), _result("b", json.dumps({"v": 2})),
        ])
        self.assertEqual(pull_live.collect(p)["jutsu/J1.json"]["data"]["v"], 2)

    def test_persisted_output(self):
        p = self.transcript([])
        store = os.path.join(os.path.dirname(p), "sess", "tool-results")
        os.makedirs(store)
        with open(os.path.join(store, "big.json"), "w") as f:
            json.dump([{"type": "text", "text": json.dumps({"id": "AI9"})}], f)
        with open(p, "w") as f:
            f.write(_use("a", "profile.getAi", {"userId": "AI9"}) + "\n")
            f.write(_result("a", "Output too large. Full output saved to: /elsewhere/big.json") + "\n")
        self.assertEqual(pull_live.collect(p)["ai/AI9.json"]["data"]["id"], "AI9")

    def test_unsafe_path_refused(self):
        p = self.transcript([_use("a", "jutsu.get", {"id": "../x"}), _result("a", json.dumps({}))])
        with self.assertRaises(SystemExit):
            pull_live.collect(p)

    def test_nested_item_id_traversal_refused(self):
        # item.getUserItem's nested item record carries its own id; it must be checked like the call input
        p = self.transcript([_use("a", "item.getUserItem", {"id": "U1"}),
                             _result("a", json.dumps({"id": "U1", "item": {"id": "../../escaped"}}))])
        with self.assertRaises(SystemExit):
            pull_live.collect(p)

    def test_nested_item_traversal_writes_nothing(self):
        p = self.transcript([_use("a", "item.getUserItem", {"id": "U1"}),
                             _result("a", json.dumps({"id": "U1", "item": {"id": "../../escaped"}}))])
        base = tempfile.mkdtemp()
        out = os.path.join(base, "a", "b")
        os.makedirs(out)
        r = subprocess.run([sys.executable, os.path.join(HERE, "..", "tools", "pull_live.py"), p, out], capture_output=True)
        self.assertNotEqual(r.returncode, 0)
        self.assertFalse(os.path.exists(os.path.join(base, "escaped.json")))
        self.assertEqual(os.listdir(out), [])

    def test_non_string_and_partial_ids_refused(self):
        for bad in [{"id": 5}, {"id": "ok/../x"}, {"id": "J1\n"}, {}]:
            p = self.transcript([_use("a", "jutsu.get", bad), _result("a", json.dumps({}))])
            with self.assertRaises(SystemExit, msg=repr(bad)):
                pull_live.collect(p)

    def test_inside_refuses_escape(self):
        root = os.path.realpath(tempfile.mkdtemp())
        self.assertTrue(pull_live._inside(root, "jutsu/J1.json").startswith(root + os.sep))
        with self.assertRaises(SystemExit):
            pull_live._inside(root, "../escaped.json")

    def test_cli_writes_files(self):
        p = self.transcript([_use("a", "jutsu.get", {"id": "J1"}), _result("a", json.dumps({"id": "J1"}))])
        out = tempfile.mkdtemp()
        subprocess.run([sys.executable, os.path.join(HERE, "..", "tools", "pull_live.py"), p, out], check=True, capture_output=True)
        with open(os.path.join(out, "jutsu", "J1.json")) as f:
            self.assertEqual(json.load(f)["data"]["id"], "J1")


if __name__ == "__main__":
    unittest.main()
