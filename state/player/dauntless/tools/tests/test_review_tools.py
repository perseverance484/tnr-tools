"""The two review tools on the logs that stopped them in AP run 2 (2026-11-16).
Run: python3 tests/test_review_tools.py   (python, no live calls, no engine)

1. critique.py's command line looked for the other side of a fight among user ids only. An AI opponent has none, so
   on every fight against an AI it stopped with StopIteration. postmortem.py had the same line.
2. postmortem.py measures each turn's alternatives in the engine. Run 2 ran where there is no engine app: the engine
   bridge gives no answer there, the list of exchanges came back empty, and the review of both losses stopped on the
   first turn with IndexError. A turn the engine did not answer keeps its read and its numbers and has no regret,
   and the report says that it was not measured.
"""
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.path.dirname(HERE)
sys.path.insert(0, TOOLS)

import critique as K  # noqa: E402
import postmortem  # noqa: E402
from ingest import ME  # noqa: E402

AI, HIM = "aTGxSsvezuwZbqj2rPHQN", "user_2SAAMvwqsbjyS2Qd8A2pB0Gzn4W"
LOSS = "9j3DIjLVbD_9b1RmJ69UM"          # run 2, fight 6: lost to Shisui in round 13


def rows(*who):
    return [(1 + i // 2, u, "basicAttack", []) for i, u in enumerate(who)]


def test_the_other_side_of_a_log():
    assert K.opponent_of(rows(ME, HIM, ME, HIM), ME) == HIM
    assert K.opponent_of(rows(HIM, ME), ME) == HIM
    assert K.opponent_of(rows(ME, AI, ME, AI), ME) == AI                 # no player but me: the AI
    assert K.opponent_of(rows(AI, ME, HIM), ME) == HIM                   # a player is taken before anything else
    assert K.opponent_of(rows(ME, ME), ME) is None
    assert K.opponent_of(rows(ME, None, ME), ME) is None                 # a row with no actor is nobody
    print("ok: the other side of a log is the other player, or the AI when there is none")


def test_the_review_reads_a_fight_against_an_ai():
    """The command line, on a log as the connector returns it (newest first) with an AI on the other side."""
    log = {"*.battleRound": [2, 2, 1, 1],
           "*.userId": [AI, ME, AI, ME],
           "*.actionId": ["3v9c1SHlD2GLPF2HW1_Sc", "basicAttack", "mOA1hXNf4CcuwOhnnN7ZK", "basicAttack"],
           "*.appliedEffects.*.txt": [["dauntless takes 300.00 damage"], ["Arsenal Keeper takes 120.00 damage"],
                                      ["Arsenal Keeper will absorb up to 20% damage and convert it to Health for "
                                       "the next 2 rounds"], ["Arsenal Keeper takes 120.00 damage"]]}
    with tempfile.TemporaryDirectory() as d:
        path = os.path.join(d, "aiFight00_entries.json")
        json.dump(log, open(path, "w"))
        out = subprocess.run([sys.executable, os.path.join(TOOLS, "critique.py"), "--entries", path],
                             capture_output=True, text=True, timeout=120)
        assert out.returncode == 0, out.stderr[-600:]
        assert "replay review" in out.stdout, out.stdout[-300:]
        json.dump({k: v[1::2] for k, v in log.items()}, open(path, "w"))      # only my rows: nobody to review against
        out = subprocess.run([sys.executable, os.path.join(TOOLS, "critique.py"), "--entries", path],
                             capture_output=True, text=True, timeout=120)
        assert out.returncode != 0 and "nobody but me" in out.stderr and "Traceback" not in out.stderr, out.stderr[-300:]
    print("ok: the replay review reads a fight against an AI, and says so when nobody else acts in a log")


def test_a_turn_the_engine_did_not_answer_has_no_regret():
    ex, score = postmortem.swings([], 3)                                  # no engine app: no answer
    assert ex is postmortem.UNMEASURED and score == [None, None, None]
    ex, score = postmortem.swings([(3000, 2500, 2600)], 3)                # an answer for fewer bundles than asked
    assert ex is postmortem.UNMEASURED and score == [None, None, None]
    ex, score = postmortem.swings([(3000, 2500, 2600), None, (2800.4, 2000, 2100)], 3)
    assert ex is not postmortem.UNMEASURED and score == [500, None, 800]  # a bundle the engine rejects is None
    assert not ex[:0] and not postmortem.UNMEASURED                       # "ex and ex[0]" stays safe on both
    print("ok: a turn the engine did not answer has no regret; one it answered keeps a rejected bundle apart")


def test_the_turns_that_followed_mine():
    """What tune_real --depth plays each line against: his next turns as he played them, mine in between as I
    played them, up to his depth-th. Waits and plain moves are left out."""
    T = postmortem.turns_after
    first = [(1, ME, "a1", []), (1, HIM, "h1", []), (1, HIM, "wait", []), (2, ME, "move", []), (2, ME, "a2", []),
             (2, ME, "a2b", []), (2, HIM, "h2", []), (3, ME, "a3", []), (3, HIM, "h3", []), (4, ME, "a4", [])]
    assert T(first, 1, HIM, 1) == [{"who": "him", "actions": ["h1"]}]
    assert T(first, 1, HIM, 2) == [{"who": "him", "actions": ["h1"]}, {"who": "me", "actions": ["a2", "a2b"]},
                                   {"who": "him", "actions": ["h2"]}]
    assert [t["who"] for t in T(first, 1, HIM, 3)] == ["him", "me", "him", "me", "him"]
    assert T(first, 3, HIM, 3) == [{"who": "him", "actions": ["h3"]}, {"who": "me", "actions": ["a4"]}]   # it ended
    second = [(1, HIM, "h1", []), (1, ME, "a1", []), (2, HIM, "h2", []), (2, ME, "a2", []), (3, HIM, "h3", [])]
    assert T(second, 1, HIM, 2) == [{"who": "him", "actions": ["h2"]}, {"who": "me", "actions": ["a2"]},
                                    {"who": "him", "actions": ["h3"]}]                # he acts first in a round
    assert T(second, 2, HIM, 1) == [{"who": "him", "actions": ["h3"]}] and T(second, 9, HIM, 2) == []
    other = first[:2] + [(1, "aiSummon", "bite", [])] + first[2:]                     # a third actor is nobody's turn
    assert T(other, 1, HIM, 2) == T(first, 1, HIM, 2)
    print("ok: the turns that followed mine, his and mine in turn, up to his depth-th")


def test_where_things_stood_after_his_last_turn():
    S = postmortem.deep_swings
    ex = [(3000, 2500, 2600, [(3000, 2500), (2000, 2400), (1500, 900)]), None, (2800, 2000, 2100, [(2800, 2000)]),
          (2800, 2000, 2100, None), (2800, 2000, 2100, [])]
    assert S(ex, 5) == [600, None, 800, None, None]
    assert S(postmortem.UNMEASURED, 3) == [None, None, None]                          # no engine: nothing measured
    ex1, score = postmortem.swings(ex, 5)
    assert score == [500, None, 800, 800, 800]                                        # one exchange: as it was
    print("ok: the deeper figure is where things stood after his last scripted turn; one exchange is unchanged")


def test_a_loss_is_reviewed_where_there_is_no_engine():
    """Run 2's first loss, as it was reviewed in the cloud container: no engine app. It ends well, says what was
    not measured, and still writes the turns and the replay review."""
    with tempfile.TemporaryDirectory() as d:
        env = dict(os.environ, TNR_ENGINE_APP=os.path.join(d, "no-engine"), TNR_LEARN="0", TNR_POSTMORTEM_OUT=d)
        out = subprocess.run([sys.executable, os.path.join(TOOLS, "postmortem.py"), LOSS[:10]],
                             capture_output=True, text=True, timeout=300, env=env)
        assert out.returncode == 0, out.stderr[-800:]
        assert "the engine gave no answer" in out.stdout and "replay review" in out.stdout, out.stdout[-600:]
        kept = json.load(open(os.path.join(d, LOSS + ".json")))
        assert kept["engine"] is False and len(kept["turns"]) >= 10 and kept["errors"], (kept["engine"], len(kept["turns"]))
        assert all(t["regret"] is None and t["swing_played"] is None for t in kept["turns"])
        assert all(t["dmg_logged"] is not None and t["played"] for t in kept["turns"])
        assert not any("deep" in t for t in kept["turns"])                           # depth 1: the review as it was
        out = subprocess.run([sys.executable, os.path.join(TOOLS, "postmortem.py"), LOSS[:10]], capture_output=True,
                             text=True, timeout=300, env=dict(env, TNR_TUNE_DEPTH="3"))
        assert out.returncode == 0, out.stderr[-800:]
        deep = [t["deep"] for t in json.load(open(os.path.join(d, LOSS + ".json")))["turns"]]
        assert all(x["played"] is None and x["pick"] is None and x["best"] is None for x in deep), deep[:2]
        assert [x["his_turns"] for x in deep][:3] == [3, 3, 3] and deep[-1]["his_turns"] <= 2, deep[-2:]
    print(f"ok: {LOSS[:8]} is reviewed with no engine: {len(kept['turns'])} turns, {len(kept['errors'])} review "
          "errors, no regret claimed")


if __name__ == "__main__":
    test_the_other_side_of_a_log()
    test_the_review_reads_a_fight_against_an_ai()
    test_a_turn_the_engine_did_not_answer_has_no_regret()
    test_the_turns_that_followed_mine()
    test_where_things_stood_after_his_last_turn()
    test_a_loss_is_reviewed_where_there_is_no_engine()
