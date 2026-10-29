"""Badge and title checks for validate.py.

Field sets and bounds come from the generated contracts (45d badge/title, 45c TitleEffectSchema;
required-on-create keys are Forge's, see REQUIRED_ON_CREATE), extracted from
studie-tech/TheNinjaRPG@2af4b32066c39e2868efae5dba6b339278701dca. The rules no schema expresses are
read at that pin and cited per rule:

  drizzle/schema.ts:4710-4757        neither Badge nor Title has a `hidden` column; Badge.image is
                                     varchar(191) and Badge.description varchar(500), while
                                     BadgeValidator allows 512 characters
  routers/badge.ts:124-138           create inserts "New Badge - <id>" with the default avatar image
                                     and an empty description; only the update sets the record
  routers/title.ts:93-110            create inserts "New Title - <id>", unarchived, with no effects
  server/utils/titleRewards.ts:9-37  quest and item saves refuse reward_titles naming an archived
                                     title (quests.ts:877, item.ts:682)

Forge mirrors the same rules in forge/src/runner/catalog.mjs and lints.mjs.
"""
import math
import re
from urllib.parse import urlsplit

ID_LEN = 21
BADGE_IMAGE_MAX = 191
BADGE_DESCRIPTION_MAX = 500
# Forge's REQUIRED (catalog.mjs), not 45g: 45g lists every validator key without a schema default,
# but the title create row already holds description "" and effects [] (drizzle/schema.ts:4713-4716)
# and the update is fetch-merged over it. `archived` is required so the choice is always stated.
REQUIRED_ON_CREATE = {"badge": ("name", "image", "description"), "title": ("name", "archived")}


def _url(v):
    """BadgeValidator's z.url() (zod 4.6.7) parses after a trim; http(s) without whitespace only."""
    try:
        u = urlsplit(v)
        return bool(re.match(r"^https?://\S+$", v)) and bool(u.hostname)
    except ValueError:
        return False


def check(entry, items, fields, checks, check_member, ctors, rep, where):
    ent = entry.get("entity")
    data = entry.get("data") or {}
    create = entry.get("slot") == "create"
    if not fields:
        rep.err(where, f"45d has no {ent} entity: regenerate the contracts at the pin before building {ent}s")
        return
    for k in data:
        if k not in fields and k != "hidden":
            rep.err(where, f"unknown key '{k}' for {ent} (the server drops it silently). Valid: {', '.join(sorted(fields))}")
    if "hidden" in data and data["hidden"] is not True:
        rep.err(where, f"{ent} has no hidden column: a create carries hidden:true (law 16b), stripped before the send")
    if create:
        for k in REQUIRED_ON_CREATE.get(ent, ()):
            if k not in data:
                rep.err(where, f"{k} is required on a {ent} create (the placeholder's value would stay)")
    for k in ("name", "description"):
        v, spec = data.get(k), fields.get(k) or {}
        if v is None:
            continue
        if not isinstance(v, str):
            rep.err(where, f"{k} must be a string")
            continue
        if k == "name" and v != v.strip():
            rep.err(where, "name has leading or trailing whitespace; the validator trims it, so the read-back would drift")
        n = len(v.strip()) if k == "name" else len(v)
        if spec.get("min") and n < spec["min"]:
            rep.err(where, f"{k} is empty")
        cap = spec.get("max")
        if ent == "badge" and k == "description":
            cap = min(cap or BADGE_DESCRIPTION_MAX, BADGE_DESCRIPTION_MAX)
        if cap and n > cap:
            rep.err(where, f"{k} is {n} characters; the {'Badge column' if cap == BADGE_DESCRIPTION_MAX else 'limit'} holds {cap}")
    if ent == "badge" and "image" in data:
        v = data["image"]
        if not isinstance(v, str) or not (v.startswith("@img:") or _url(v)):
            rep.err(where, "image must be an @img ref or an absolute URL (BadgeValidator: z.url())")
        elif not v.startswith("@img:") and len(v) > BADGE_IMAGE_MAX:
            rep.err(where, f"image URL is {len(v)} characters; the Badge column holds {BADGE_IMAGE_MAX}")
    if ent == "title":
        _check_title(entry, data, items, fields, check_member, ctors, rep, where)


def _check_title(entry, data, items, fields, check_member, ctors, rep, where):
    if "archived" in data and not isinstance(data["archived"], bool):
        rep.err(where, "archived must be a boolean")
    effects = data.get("effects")
    if effects is not None:
        cap = (fields.get("effects") or {}).get("max")
        if not isinstance(effects, list):
            rep.err(where, "effects must be a list")
            effects = []
        elif cap is not None and len(effects) > cap:
            rep.err(where, f"{len(effects)} effects; a title holds at most {cap}")
        for i, e in enumerate(effects):
            w = f"{where}.effects[{i}]"
            if not isinstance(e, dict):
                rep.err(w, "effect must be an object")
                continue
            check_member(e, "TitleEffectSchema", ctors, w, rep)
            p = e.get("power")
            if not isinstance(p, (int, float)) or isinstance(p, bool):
                rep.err(w, "power must be a number")
            elif not math.isfinite(p) or p < 0:
                rep.err(w, f"power must be finite and >= 0 (TitleEffectSchema), got {p}")
            if e.get("type") == "increasemastery" and not (isinstance(e.get("masteryTypes"), list) and e["masteryTypes"]):
                rep.err(w, "increasemastery needs at least one masteryTypes entry")
    if data.get("archived") is True:
        ref = "@title:" + entry["srcId"] if entry.get("slot") == "create" and entry.get("srcId") else entry.get("targetId")
        for other in items:
            if ref and re.search(r'"reward_titles":\s*\[[^\]]*"%s"' % re.escape(str(ref)), _dump(other.get("data"))):
                rep.err(where, f"TITLE {ref} is archived in this manifest; the server refuses a save rewarding it "
                               f"({other.get('entity')}:{other.get('name')})")
    elif entry.get("slot") == "create" and data.get("archived") is False:
        rep.note(where, "archived:false: the title is listed in title.getAllNames and can be rewarded at once. "
                        "Titles have no hidden column; nothing grants it until a published reward names it")


def _dump(v):
    import json
    return json.dumps(v or {})
