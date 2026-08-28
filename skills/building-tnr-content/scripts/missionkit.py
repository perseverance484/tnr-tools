"""Shared builders so every mission is wired the same way as Old Ghost."""
import json
PINS={p["name"]:p for p in json.load(open("34b_DATA_pins.json"))["pins"]}
SAFE="XAjOr4zBngvaztvPd0Ls0"; MKT="gXpaJL3VnawaQ5PGqSoAB"
DOOR="p76eudOzH1KfbpLzhBgrJ"; HALL="JAh1c6Ykf_nUfM5Xk67DW"; ALLEY="wyMQkpiugsLs8BQpDdTf2"
H="pqihl43HYROpkIMX172-P"

def c(t,n): return {"text":t,"nextObjectiveId":n}

def d(i,desc,nxt=None,bg=None,ch=None):
    o={"id":i,"task":"dialog","description":desc}
    if nxt: o["nextObjectiveId"]=nxt
    if bg: o["sceneBackground"]=bg
    if ch is not None: o["sceneCharacters"]=ch
    return o

def go(i,desc,nxt,bg):
    """Travel. Instant. Only where the player just goes somewhere."""
    return {"id":i,"task":"move_to_location","description":desc,"sectorType":"user_village",
            "locationType":"specific","nextObjectiveId":nxt,"sceneBackground":bg}

def act(i,verb,desc,nxt,bg):
    """An Action. Timed, self-resolving, and the player must hold the tile.

    Never use where the fiction has the player moving under pressure or reacting to somebody
    else. An Action is a decision to stand still and do the thing properly.
    """
    p=PINS[verb]
    return {"id":i,"task":"collect_item","description":desc,
            "collect_time_minutes":p["collect_time_minutes"],"item_name":verb,
            "delete_on_complete":True,"hideLocation":False,"sectorType":"user_village",
            "locationType":"specific","nextObjectiveId":nxt,"sceneBackground":bg}

def bt(i,desc,failto,nxt,ais,bg,notice="Target down."):
    return {"id":i,"task":"defeat_opponents","description":desc,"failObjectiveId":failto,
            "completionOutcome":"Win","sectorType":"user_village","locationType":"specific",
            "opponentAIs":ais,"nextObjectiveId":nxt,"sceneBackground":bg,
            "successDescription":notice}

def end(i,desc,to,text,bg=None,ch=None):
    """A closing DIALOG. It must carry an option: the builder's q.fill flow validator
    rejects any dialog with none. `to` is the quest's win_quest node."""
    o={"id":i,"task":"dialog","description":desc,
       "nextObjectiveId":[{"text":text,"nextObjectiveId":to}]}
    if bg: o["sceneBackground"]=bg
    if ch is not None: o["sceneCharacters"]=ch
    return o

def win(i,desc):
    """The quest terminal. win_quest is one of the few tasks allowed to carry no next,
    and it is what actually marks the quest complete. Live Witness Detail ends this way."""
    return {"id":i,"task":"win_quest","description":desc,
            "successDescription":"Mission complete.",
            "sceneBackground":"","sceneCharacters":[]}

def write(path,rank,srcid,name,desc,succ,objs,bg=HALL):
    json.dump({"rank":rank,"srcId":srcid,"name":name,"description":desc,
               "successDescription":succ,"sceneBackground":bg,"sceneCharacters":[],
               "objectives":objs}, open(path,"w"), indent=1, ensure_ascii=False)
