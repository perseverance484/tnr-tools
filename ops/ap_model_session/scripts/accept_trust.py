# Usage: python3 ops/ap_model_session/scripts/accept_trust.py [folder]   (default: the repo root this kit is in)
import os, pty, time, select, re, sys
ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
pid, fd = pty.fork()
if pid == 0:
    os.chdir(ROOT)
    env = {k: os.environ[k] for k in ("PATH","HOME","HTTPS_PROXY","https_proxy","NO_PROXY","no_proxy","NODE_EXTRA_CA_CERTS","SSL_CERT_FILE") if k in os.environ}
    env.update(LANG="C.UTF-8", TERM="xterm-256color")
    os.execvpe("claude", ["claude", "--model", "haiku"], env)
buf = b""
def read(t):
    global buf
    end = time.time() + t
    while time.time() < end:
        r, _, _ = select.select([fd], [], [], 0.5)
        if r:
            try: buf += os.read(fd, 65536)
            except OSError: return
def screen():
    s = re.sub(rb"\x1b\[[0-9;?]*[a-zA-Z]|\x1b\][^\x07]*\x07", b"", buf).decode("utf-8", "replace")
    return s
read(12)
for step in range(10):
    s = screen()[-1200:]
    low = s.lower().replace(" ", "")
    print(f"==== step {step} ====\n{s[-500:]}")
    if any(w in low for w in ("selectloginmethod","apikey","anthropicconsole","claudeaccountwithsubscription","paste")):
        print("LOGIN PROMPT, stopping"); break
    if "trust" in low and ("proceed" in low or "folder" in low):
        print(">> trust dialog, pressing Down then Enter")
        os.write(fd, b"\x1b[B"); read(1.5); os.write(fd, b"\r"); read(8); buf_tail = screen()[-400:]; print(buf_tail); break
    if "?forshortcuts" in low or "tryedit" in low or ">try" in low:
        print("at prompt"); break
    buf = b""
    os.write(fd, b"\r"); read(6)
os.write(fd, b"/exit\r"); read(4)
try: os.kill(pid, 15)
except Exception: pass
