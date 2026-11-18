#!/usr/bin/env python3
"""Save live read-only connector answers from a Claude Code session transcript as sim input.

The TNR connector's answers already sit in the session transcript (tool_use + tool_result pairs),
so this needs no network and makes no live request. Only unfiltered answers are kept (a call with
`select`, `search` or `maxLength` returns a partial view and is skipped). Each saved file is
`{"_source": {"endpoint", "input", "readAt"}, "data": <answer>}`.

    python3 harness/combat_sim/tools/pull_live.py TRANSCRIPT.jsonl OUT_DIR [--list]

Where an answer was too large for the transcript, Claude Code stores it in
`<transcript dir>/<session id>/tool-results/<tool_use_id>.json`; that file is read instead.

Kept endpoints and where they land in OUT_DIR:
  profile.getAi            ai/<userId>.json
  ai.getAiProfile          profiles/<id>.json
  jutsu.get                jutsu/<id>.json
  item.getUserItem         user_items/<id>.json   (and items/<itemId>.json from its item record)
  item.get                 items/<id>.json
  bloodline.get            bloodlines/<id>.json
  pets.getPet              pets/<petId>.json      (pet, species passives, the pet's battle jutsu)
  combat.getBattleEntries  battles/<battleId>.entries.json
  misc.getDmgConfig        runtime/dmg_config.json
  misc.getSharedCooldowns  runtime/shared_cooldowns.json
Anything else is ignored. Later answers for the same key replace earlier ones.
"""
import json
import os
import re
import sys

ROUTES = {
    "profile.getAi": lambda i, d: f"ai/{i['userId']}.json",
    "ai.getAiProfile": lambda i, d: f"profiles/{i['id']}.json",
    "jutsu.get": lambda i, d: f"jutsu/{i['id']}.json",
    "item.getUserItem": lambda i, d: f"user_items/{i['id']}.json",
    "item.get": lambda i, d: f"items/{i['id']}.json",
    "bloodline.get": lambda i, d: f"bloodlines/{i['id']}.json",
    "pets.getPet": lambda i, d: f"pets/{i['petId']}.json",
    "combat.getBattleEntries": lambda i, d: f"battles/{i['battleId']}.entries.json",
    "misc.getDmgConfig": lambda i, d: "runtime/dmg_config.json",
    "misc.getSharedCooldowns": lambda i, d: "runtime/shared_cooldowns.json",
}
PERSISTED = re.compile(r"Full output saved to: (\S+\.json)")
SAFE_KEY = re.compile(r"^[A-Za-z0-9_\-]+$")


def _text(content):
    if isinstance(content, str):
        return content
    return "".join(x.get("text", "") for x in content or [] if isinstance(x, dict))


def _answer(text, transcript):
    m = PERSISTED.search(text)
    if m:
        path = m.group(1)
        base = os.path.join(os.path.dirname(os.path.abspath(transcript)),
                            os.path.splitext(os.path.basename(transcript))[0], "tool-results",
                            os.path.basename(path))
        for p in (path, base):
            if os.path.exists(p):
                with open(p) as f:
                    text = _text(json.load(f))
                break
        else:
            return None
    try:
        return json.loads(text)
    except ValueError:
        return None


def collect(transcript):
    uses, out = {}, {}
    with open(transcript) as f:
        for line in f:
            try:
                o = json.loads(line)
            except ValueError:
                continue
            msg = o.get("message") or {}
            content = msg.get("content")
            if not isinstance(content, list):
                continue
            for b in content:
                if b.get("type") == "tool_use" and b.get("name", "").endswith("callEndpoint"):
                    uses[b["id"]] = b.get("input") or {}
                elif b.get("type") == "tool_result" and b.get("tool_use_id") in uses and not b.get("is_error"):
                    call = uses[b["tool_use_id"]]
                    ep = call.get("endpointName")
                    if ep not in ROUTES or call.get("select") or call.get("search") or call.get("maxLength"):
                        continue
                    data = _answer(_text(b.get("content")), transcript)
                    if data is None:
                        continue
                    inp = call.get("input") or {}
                    rel = ROUTES[ep](inp, data)
                    if not all(SAFE_KEY.match(p.replace(".entries", "").replace(".json", "")) for p in rel.split("/")):
                        raise SystemExit(f"refusing unsafe output path {rel!r}")
                    src = {"endpoint": ep, "input": inp, "readAt": o.get("timestamp")}
                    out[rel] = {"_source": src, "data": data}
                    if ep == "item.getUserItem" and isinstance(data, dict) and isinstance(data.get("item"), dict):
                        out[f"items/{data['item']['id']}.json"] = {"_source": {**src, "via": "item.getUserItem.item"}, "data": data["item"]}
    return out


def main(argv):
    if len(argv) < 3:
        raise SystemExit(__doc__)
    found = collect(argv[1])
    if "--list" in argv:
        for k in sorted(found):
            print(k, found[k]["_source"]["readAt"])
        return 0
    for rel, doc in sorted(found.items()):
        path = os.path.join(argv[2], rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            json.dump(doc, f, indent=1, sort_keys=True)
            f.write("\n")
    print(f"wrote {len(found)} files to {argv[2]}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
