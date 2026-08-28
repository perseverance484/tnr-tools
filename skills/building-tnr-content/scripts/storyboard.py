#!/usr/bin/env python3
"""Render a mission sheet as an editable storyboard.

The storyboard is the editing surface: dauntless marks it up, hands it back, and the edits are
applied to the SHEET, not to the built manifest. Sheet stays the source of truth so nothing
drifts between what he read and what ships.

Node ids and the EDGES line are the wiring contract. Edit prose freely; if you change an id or
an edge, say so explicitly, because the graph is validated against them.
"""
import json, sys, re

BG = {"XAjOr4zBngvaztvPd0Ls0": "safehouse", "gXpaJL3VnawaQ5PGqSoAB": "market row",
      "p76eudOzH1KfbpLzhBgrJ": "doorway", "JAh1c6Ykf_nUfM5Xk67DW": "hall steps",
      "wyMQkpiugsLs8BQpDdTf2": "back alley"}
CH = {"pqihl43HYROpkIMX172-P": "Handler"}
AI = {"2ZF5jMvECgiNBgrr4icqk": "Faceless Shadow (55)",
      "rKWmoT0Ez1q4r8jEqprWP": "Faceless Stray (40)",
      "@ai:fsw_fc_blade": "Faceless Blade (50)", "@ai:fsw_um_stray": "Unmarked Stray (25)",
      "@ai:fsw_um_blade": "Unmarked Blade (30)", "@ai:fsw_um_shadow": "Unmarked Shadow (35)",
      "@ai:fsw_palefang": "Pale Fang (70)", "@ai:fsw_wintercrow": "Winter Crow (80)",
      "@ai:fsw_oldghost": "Old Ghost (85)"}


def prose(t):
    """Strip the markup so the text reads as script. <i> becomes plain italic-style lines."""
    t = t.replace("<br>", "\n").replace("<i>", "*").replace("</i>", "*")
    t = re.sub(r"\n{3,}", "\n\n", t)
    return "\n".join(l.strip() for l in t.split("\n")).strip()


def render(sheet):
    objs = sheet["objectives"]
    inbound = {}
    for o in objs:
        n = o.get("nextObjectiveId")
        tgts = [c["nextObjectiveId"] for c in n] if isinstance(n, list) else ([n] if n else [])
        if o.get("failObjectiveId"):
            tgts.append(o["failObjectiveId"])
        for t in tgts:
            inbound.setdefault(t, []).append(o["id"])

    L = [f"# {sheet['name']}", "",
         f"**{sheet['rank']} rank** &middot; {len(objs)} nodes &middot; "
         f"{sum(1 for o in objs if o['task'] == 'defeat_opponents')} battles &middot; "
         f"{sum(1 for o in objs if not o.get('nextObjectiveId'))} endings", "",
         "> Edit the prose freely. Node ids and the EDGES lines are the wiring, so flag any",
         "> change to those explicitly. Everything here comes from the sheet, which is the",
         "> source of truth; edits get applied there and the manifest is rebuilt from it.", "",
         "## Premise", "", sheet["description"], "",
         "## On success", "", sheet["successDescription"], "", "---", ""]

    for o in objs:
        task = o["task"]
        head = {"dialog": "DIALOG", "move_to_location": "TRAVEL",
                "defeat_opponents": "BATTLE"}.get(task, task.upper())
        bits = []
        if o.get("sceneBackground"):
            bglabel = BG.get(o["sceneBackground"], o["sceneBackground"])
            intent = sheet.get("bgIntent", {}).get(o["id"])
            bits.append(f"{intent} (stand-in: {bglabel})" if intent and intent != bglabel else bglabel)
        if o.get("sceneCharacters"):
            bits.append(", ".join(CH.get(c, c) for c in o["sceneCharacters"]))
        elif "sceneCharacters" in o:
            bits.append("no characters")
        setting = f"  <sub>{' &middot; '.join(bits)}</sub>" if bits else ""

        L.append(f"### `{o['id']}` &middot; {head}{setting}")
        if inbound.get(o["id"]):
            L.append(f"<sub>from: {', '.join('`'+x+'`' for x in inbound[o['id']])}</sub>")
        L.append("")

        if task == "defeat_opponents":
            for g in o.get("opponentAIs", []):
                who = ", ".join(AI.get(i, i) for i in g["ids"])
                L.append(f"**Enemy:** {g['number']} &times; {who}")
            L.append("")
        L += [prose(o["description"]), ""]

        if o.get("successDescription"):
            L += [f"**On success.** {prose(o['successDescription'])}", ""]
        if o.get("failDescription"):
            L += [f"**On failure.** {prose(o['failDescription'])}", ""]

        n = o.get("nextObjectiveId")
        if isinstance(n, list):
            for c in n:
                L.append(f"- **\u201c{c['text']}\u201d** &rarr; `{c['nextObjectiveId']}`")
            L.append("")
        elif n:
            L.append(f"EDGES: &rarr; `{n}`" + (f" &middot; on failure &rarr; `{o['failObjectiveId']}`"
                                               if o.get("failObjectiveId") else ""))
            L.append("")
        else:
            L += ["**ENDING.**", ""]
        L.append("---")
        L.append("")
    return "\n".join(L)


if __name__ == "__main__":
    sheet = json.load(open(sys.argv[1]))
    out = sys.argv[2]
    open(out, "w").write(render(sheet))
    print("wrote", out)
