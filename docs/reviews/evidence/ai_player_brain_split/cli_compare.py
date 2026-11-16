"""The command line of the old file and of the package, command for command, each in a live folder of its own.
Prints both transcripts side by side where they differ, after the relay's name, the paths and the times are
taken out."""
import json, os, re, subprocess, sys, tempfile, time
from player import config as C
from player.tests.test_rereview5 import the_package_at
BASE = sys.argv[1]
def session(root):
    live = tempfile.mkdtemp(prefix="player-cli-")
    env = {**os.environ, "PYTHONPATH": root, "TNR_PLAYER_LIVE": live, "TNR_PLAYER_NO_DAEMON": "1",
           "TNR_TRANSCRIPT": os.path.join(live, "none"), "TNR_PLAYER_FIGHTS": os.path.join(live, "fights")}
    out = []
    def run(*args, stdin=""):
        p = subprocess.run([sys.executable, "-W", "ignore", "-m", "player.brain", *args], cwd=root, env=env,
                           input=stdin, capture_output=True, text=True, timeout=120)
        out.append([list(args), p.returncode, p.stdout, p.stderr])
        return p
    run(); run("bogus"); run("status")
    run("set", "mode=guard", "paused=false")
    first = run("next").stdout
    token = re.search(r"next ([0-9a-f]+-\d+)", first).group(1)
    second = run("next", token).stdout
    token2 = re.search(r"next ([0-9a-f]+-\d+)", second.splitlines()[-1]).group(1)
    run("put", token2, "1", stdin=json.dumps({"userData.status": "AWAKE", "userData.curHealth": 10, "userData.maxHealth": 10}))
    run("put", token2, "99", stdin="{}"); run("put", "nobody-1", "1", stdin="{}")
    run("stopped"); run("stopped", "all"); run("stopped", "nobody-7")
    run("next", "0000aa-3")                                   # a relay nobody knows
    run("next", token)                                        # the same batch's line again
    third = run("next", token2).stdout
    run("status")
    home = subprocess.Popen([sys.executable, "-W", "ignore", "-m", "player.brain", "run"], cwd=root, env=env,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    time.sleep(1.5)
    found = subprocess.run(["pgrep", "-f", "player.brain run"], capture_output=True, text=True).stdout.split()
    again = run("run")                                        # a second resident: the lock is taken
    out.append([["(the resident is found by `pgrep -f \"player.brain run\"`, and is running)"], 0, str(str(home.pid) in found and home.poll() is None), ""])
    home.terminate(); home.wait(timeout=10)
    out.append([["(the resident ended on SIGTERM)"], 0, str(home.returncode), home.stderr.read()[-200:]])
    home.stdout.close(); home.stderr.close()
    files = sorted(os.listdir(live))
    def plain(text):
        text = text.replace(root, "<root>").replace(live, "<live>")
        text = re.sub(r"\b[0-9a-f]{6}-(\d+)\b", r"<relay>-\1", text)
        text = re.sub(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ", "<time>", text)
        text = re.sub(r"\b1[78]\d{8}(\.\d+)?\b", "<t>", text)
        text = re.sub(r'"(hold|eta|wait|since|at|age)": ?-?\d+(\.\d+)?', r'"\1": <n>', text)
        text = re.sub(r"update-[0-9a-f]{8}|unknown-[0-9a-f]{6}", "<id>", text)
        return text
    return [[a, code, plain(o), plain(e)] for a, code, o, e in out], files
old_root = the_package_at(BASE)
old, old_files = session(old_root)
new, new_files = session(C.ROOT)
same = 0
for (a, c1, o1, e1), (_, c2, o2, e2) in zip(old, new):
    if (c1, o1, e1) == (c2, o2, e2):
        same += 1
        print(f"same   {' '.join(a) or '(no command)':40s} exit {c1}; {len(o1.splitlines())} lines out, {len(e1.splitlines())} err")
    else:
        print(f"DIFFER {' '.join(a)}\n  old: exit {c1}\n{o1[:600]}\n{e1[:400]}\n  new: exit {c2}\n{o2[:600]}\n{e2[:400]}")
print(f"{same} of {len(old)} commands give the same exit code and the same words; live folder files: old {old_files} new {new_files}")
print("usage text on a bad command:", repr(new[1][3][:120]))
