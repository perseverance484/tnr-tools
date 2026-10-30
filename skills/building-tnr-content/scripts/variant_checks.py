"""Item variant, variant-token and new-tag placement checks for validate.py (RUL-2026-10-29-047).

Field sets, bounds and enums come from the generated contracts (45d itemVariant, 45g, 45e), extracted
from studie-tech/TheNinjaRPG@3314d122c93e036618483d18229a793ad7ad21fd. The rules no schema expresses
are read at that pin and cited per rule:

  routers/item.ts:1167-1275    upsertItemVariant {itemId, variant}: one mutation creates (no
                               variant.id) and replaces the whole record (with it); the create
                               answers no id. Refused before any write: requiredItemId on a cost
                               other than VARIANT_TOKEN, a required item without an unlockitemvariant
                               whose variantId is null or this variant's id (on a create the id does
                               not exist yet, so only null), MAX_ITEM_VARIANTS, a taken order
  drizzle/schema.ts:1736-1766  ItemVariant: name varchar(191), image varchar(512), cost int, unique
                               (itemId, order), no hidden column
  routers/item.ts:1458-1520    consumeVariantToken: the token's unlockitemvariant must carry no
                               variantId or this variant's; a variant with requiredItemId accepts only
                               that item. A variant is listed to every owner of its item from the
                               create on: there is no switch to hide it
  validators/combat.ts:1689-1840  SuperRefineItem: unlockitemvariant needs CONSUMABLE, target SELF,
                               method SINGLE, destroyOnUse and preventBattleUsage; increasejutsuslots
                               the same, at most MAX_EXTRA_JUTSU_SLOTS in total; activity bonuses only
                               on ARMOR/ACCESSORY/KEYSTONE/CRYSTAL items. SuperRefineJutsu,
                               PetSpeciesValidator and RaidDamageThresholdValidator refuse activity
                               bonuses; SuperRefinePassiveEffects refuses increasejutsuslots

Forge mirrors the variant rules in forge/src/runner/variants.mjs and lints.mjs ("VARIANT").
"""
import json
import re

from catalog_checks import _url

ID_LEN = 21
INT_MAX = 2147483647
NAME_MAX = 191      # ItemVariant.name varchar(191); the validator has no max
IMAGE_MAX = 512     # ItemVariant.image varchar(512)
TOKEN_ITEM = {"itemType": "CONSUMABLE", "target": "SELF", "method": "SINGLE",
              "destroyOnUse": True, "preventBattleUsage": True}
GEAR_TYPES = ("ARMOR", "ACCESSORY", "KEYSTONE", "CRYSTAL")
# what item.create's placeholder already holds (queries/item.ts insertItemForCreate: target "CHARACTER";
# schema.ts: method SINGLE, destroyOnUse/preventBattleUsage false; itemType is the create's own type,
# CONSUMABLE when omitted): a token create must state the rest, or the fetch-merged update keeps them
PLACEHOLDER_OK = ("itemType", "method")


def _id_or_ref(v, prefix):
    return isinstance(v, str) and (len(v) == ID_LEN or bool(re.match(r"^@%s:[A-Za-z0-9_\-]+$" % prefix, v)))


def check(entry, items, fields, checks, rep, where):
    data = entry.get("data") or {}
    create = entry.get("slot") == "create"
    if not fields:
        rep.err(where, "45d has no itemVariant entity: regenerate the contracts at the pin before building variants")
        return
    for k in data:
        if k == "id":
            rep.err(where, "id: the variant id is the entry's targetId; do not send it in data")
        elif k not in fields and k not in ("hidden", "itemId"):
            rep.err(where, f"unknown key '{k}' for itemVariant (the server drops it silently). Valid: itemId, {', '.join(sorted(fields))}")
    if "hidden" in data and data["hidden"] is not True:
        rep.err(where, "itemVariant has no hidden column: a create carries hidden:true (law 16b), stripped before the send")
    if not _id_or_ref(data.get("itemId"), "item"):
        rep.err(where, f"itemId: every variant entry names its base item (a {ID_LEN}-char id or an @item ref); "
                       "upsertItemVariant takes {itemId, variant} and the variant is read from that item's list")
    if create:
        for k in (checks.get("required_on_create") or {}).get("fields", {}).get("itemVariant", []):
            if k not in data:
                rep.err(where, f"itemVariant create missing required '{k}'")
    for k, allowed in ((checks.get("enums") or {}).get("fields", {}).get("itemVariant") or {}).items():
        v = data.get(k)
        if v is not None and v not in allowed:
            rep.err(where, f"{k}={v!r} not in {allowed}")
    name = data.get("name")
    if name is not None and not (isinstance(name, str) and name and name == name.strip() and len(name) <= NAME_MAX):
        rep.err(where, f"name: 1-{NAME_MAX} characters (the column), no leading or trailing whitespace (the validator trims)")
    img = data.get("image")
    if img is not None and not (isinstance(img, str) and (img.startswith("@img:") or (_url(img) and len(img) <= IMAGE_MAX))):
        rep.err(where, f"image: an @img ref or an http(s) URL of at most {IMAGE_MAX} characters")
    for k, lo, hi in (("cost", 0, INT_MAX), ("order", (fields.get("order") or {}).get("min", 1), (fields.get("order") or {}).get("max", 7))):
        v = data.get(k)
        if v is not None and not (isinstance(v, int) and not isinstance(v, bool) and lo <= v <= hi):
            rep.err(where, f"{k}: an integer {lo}..{hi}")
    for k in ("description", "battleDescription"):
        v = data.get(k)
        if k in data and not isinstance(v, str):
            rep.err(where, f"{k}: a string; omit the key to leave it empty (null is refused: z.string().optional())")
        elif isinstance(v, str) and "<" in v:
            rep.warn(where, f"{k} carries markup: sanitizeVariantText rewrites it, so the read-back may report drift")
    req = data.get("requiredItemId")
    if req is not None:
        if not _id_or_ref(req, "item"):
            rep.err(where, f"requiredItemId: a {ID_LEN}-char item id, an @item ref or null")
        if data.get("costType") not in (None, "VARIANT_TOKEN"):
            rep.err(where, "requiredItemId: only a VARIANT_TOKEN variant can require an unlock item")
    if "furnitureData" in data and data["furnitureData"] is not None and not isinstance(data["furnitureData"], dict):
        rep.err(where, "furnitureData: an object or null (furniture items only)")
    if not create:
        return
    if data.get("costType") != "VARIANT_TOKEN":
        rep.warn(where, f"costType {data.get('costType')}: a variant has no hidden switch, so owners of the item can buy it as soon as it exists")
    elif req is None:
        rep.warn(where, "no requiredItemId: any token whose unlockitemvariant has no variantId (every older Variant Token) unlocks it")
    if isinstance(req, str) and req.startswith("@item:"):
        tok = next((it for it in items if it.get("srcId") == req[6:]), None)
        if tok and tok.get("slot") == "create":
            fx = [f for f in (tok.get("data") or {}).get("effects") or [] if isinstance(f, dict) and f.get("type") == "unlockitemvariant"]
            if not any(f.get("variantId") is None for f in fx):
                rep.err(where, f"{req} needs an unlockitemvariant with variantId null when this variant is created "
                               "(the server accepts only null before the variant has an id); set the token's variantId in a later edit")
    key = (json.dumps(data.get("itemId")), data.get("order"))
    twins = [it for it in items if it is not entry and it.get("entity") == "itemVariant" and it.get("slot") == "create"
             and (json.dumps((it.get("data") or {}).get("itemId")), (it.get("data") or {}).get("order")) == key]
    if twins:
        rep.err(where, f"another variant create in this manifest uses order {data.get('order')} on the same item; (itemId, order) is unique")


def check_effects_placement(entry, consts, rep, where, ctors=None):
    """The tags 3314d122 added: where they may live (SuperRefineItem/Jutsu, PetSpeciesValidator)."""
    ent, data = entry.get("entity"), entry.get("data") or {}
    create = entry.get("slot") == "create"
    item_type = data.get("itemType", "CONSUMABLE" if create else None)  # Forge creates an untyped item CONSUMABLE
    effects = [f for f in data.get("effects") or [] if isinstance(f, dict)]
    activity = set(((consts or {}).get("activityBonusTypes") or {}).get("value") or [])
    cap = ((consts or {}).get("MAX_EXTRA_JUTSU_SLOTS") or {}).get("value")
    for i, f in enumerate(effects):
        t, w = f.get("type"), f"{where}.effects[{i}]"
        if t in activity and (ent in ("jutsu", "petSpecies", "quest") or (ent == "item" and item_type not in (None,) + GEAR_TYPES)):
            rep.err(w, f"{t}: activity bonuses require a bloodline, activated skill, worn gear (ARMOR/ACCESSORY/KEYSTONE/CRYSTAL) or imbuement")
        if t == "increasejutsuslots" and ent != "item":
            rep.err(w, "increasejutsuslots: jutsu slot grants are only supported on non-combat consumables")
        if t == "unlockitemvariant" and ent == "item":
            v = f.get("variantId")
            if v is not None and not _id_or_ref(v, "variant"):
                rep.err(w, f"variantId: null (any token variant without a required item), a {ID_LEN}-char variant id or an @variant ref")
    if ent != "item":
        return
    slots = [f for f in effects if f.get("type") == "increasejutsuslots"]
    for t, found in (("unlockitemvariant", any(f.get("type") == "unlockitemvariant" for f in effects)), ("increasejutsuslots", bool(slots))):
        if not found:
            continue
        for k, v in TOKEN_ITEM.items():
            if k in data and data[k] != v:
                rep.err(where, f"{t} requires {k} {v!r}, got {data[k]!r}")
            elif k not in data and create and k not in PLACEHOLDER_OK:
                rep.err(where, f"{t} requires {k} {v!r}; state it on the create")
    # an omitted power is the tag's prefault (45c), not 0
    dflt = ((((ctors or {}).get("unions") or {}).get("AllTags") or {}).get("increasejutsuslots") or {}).get("fields", {}).get("power", {}).get("default", 1)
    total = sum(f.get("power", dflt) for f in slots if isinstance(f.get("power", dflt), (int, float)))
    if slots and isinstance(cap, int) and total > cap:
        rep.err(where, f"increasejutsuslots: an item may grant at most {cap} extra jutsu slots ({total})")
