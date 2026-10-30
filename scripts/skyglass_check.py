#!/usr/bin/env python3
"""skyglass_check.py - gate Skyglass manifests against the design of record (RUL-2026-10-28-028 item 3).

    python3 scripts/skyglass_check.py                    # every Skyglass manifest in push/
    python3 scripts/skyglass_check.py push/319_skyglass_update.json [more.json ...]
    python3 scripts/skyglass_check.py --json             # machine-readable findings

Deterministic, stdlib only, socket-free: it reads repository files and nothing else. Exit 0 when there is no
ERROR (warnings allowed), 1 on any ERROR, 2 on a usage problem or an unreadable manifest.

Checks (convention and data: docs/workflows/SKYGLASS_CHECK.md; design data: state/skyglass_design/design_data.json):
  design      the design data still matches its prose sources and every id is still where it says it is
  picks       completion picks (rewardMode, rewardPickCount, the option cards) match loot tables section 4a;
              retired records are only hidden
  win-only    battle objectives carry no reward except the profession flags; no profession flag anywhere has an
              empty id list (empty = the whole pool)
  chest-text  every weighted-cache item's description follows the RUL-2026-10-28-030 format: a coloured line
              per tier (rate and items), 'Always:' for fixed rewards, a roll line only when the count varies
  voice       player-facing text uses none of the story bible's "Never use" words, nor "seven-bladed"
  chart-tier  chart rarity matches its tier (RUL-2026-10-28-028 item 4)
  prof-chest  profession chest rarity and hunt/gather flags (RUL-2026-10-28-023); hunt profession drops limited
              to the area's chests
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import re
import sys
from collections import Counter
from decimal import ROUND_HALF_UP, Decimal

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
DESIGN = "state/skyglass_design/design_data.json"
LOOT = "docs/design/SKYGLASS_LOOT_TABLES.md"
BIBLE = "docs/design/SKYGLASS_STORY_BIBLE.md"
RULINGS = "docs/RULINGS.md"
NAMES = "answers/names_item.json"

# Source-verified: studie-tech/theninjarpg@2af4b32066c39e2868efae5dba6b339278701dca
# app/src/validators/rewards.ts:162-202 (MASTERY_EXPERIENCE_FIELDS, REWARD_CHOICE_AMOUNT_FIELDS,
# REWARD_CHOICE_CONTENT_FIELDS) and app/src/libs/rewardChoice.ts buildRewardChoiceCards: every positive amount field is
# one card, every id of every reward_items entry is one card (with that entry's quantity), every jutsu / bloodline /
# sage mode / badge / title id is one card, and every reward package with a reward is one card.
AMOUNT_FIELDS = (
    "reward_ninjutsu_experience", "reward_genjutsu_experience", "reward_taijutsu_experience",
    "reward_bukijutsu_experience", "reward_bloodline_experience", "reward_sage_stat_experience",
    "reward_money", "reward_seichi_silver", "reward_clanpoints", "reward_anbupoints", "reward_exp",
    "reward_pet_experience", "reward_tokens", "reward_prestige", "reward_reputation", "reward_skillpoints",
    "reward_medical_experience", "reward_hunting_experience", "reward_crafting_experience",
    "reward_gathering_experience", "reward_sage_mastery_experience", "reward_war_damage", "reward_war_healing",
)
CONTENT_FIELDS = {"reward_jutsus": "jutsu", "reward_bloodlines": "bloodline", "reward_sage_modes": "sage_mode",
                  "reward_badges": "badge", "reward_titles": "title"}
BATTLE_TASKS = {"start_battle", "defeat_opponents"}
PROFESSION_FLAGS = {"reward_hunter_items": "reward_hunter_items_ids",
                    "reward_gathering_items": "reward_gathering_items_ids"}
BATTLE_ALLOWED = set(PROFESSION_FLAGS) | set(PROFESSION_FLAGS.values())
TEXT_KEYS = {"name", "description", "successDescription", "failDescription", "drawDescription", "fleeDescription",
             "battleDescription", "text", "displayName"}
TIER_WORDS = ("Common", "Uncommon", "Rare", "Epic", "Legendary", "Mythic")
SKYGLASS_FILE = re.compile(r"skyglass|crownhold", re.I)


class Finding:
    def __init__(self, level, check, file, where, field, msg):
        self.level, self.check, self.file, self.where, self.field, self.msg = level, check, file, where, field, msg

    def as_dict(self):
        return {"level": self.level, "check": self.check, "file": self.file, "where": self.where,
                "field": self.field, "message": self.msg}

    def __str__(self):
        loc = " :: ".join(x for x in (self.file, self.where, self.field) if x)
        return f"{self.level:5} [{self.check}] {loc} :: {self.msg}"


def _read(root, rel):
    with open(os.path.join(root, rel), encoding="utf-8") as fh:
        return fh.read()


def _section(text, heading_prefix):
    """Lines of the markdown section whose heading starts with heading_prefix, up to the next heading of that level."""
    lines = text.splitlines()
    level = heading_prefix.split(" ")[0]
    out, inside = [], False
    for ln in lines:
        if ln.startswith(heading_prefix):
            inside = True
            continue
        if inside and ln.startswith(level + " "):
            break
        if inside:
            out.append(ln)
    return out if inside else None


def _strip_refs(text):
    """A section 4a cell without its trailing ruling references, e.g. ' (RUL-2026-10-28-018)'."""
    return re.sub(r"\s*\(RUL-[\d-]+(?:[,;/ ]+RUL-[\d-]+)*\)\s*$", "", text.strip())


def _canon(options):
    """Options in a comparable form: package components unordered, quantity 1 made explicit on items."""
    def one(o):
        if "package" in o:
            return {"package": sorted((one(c) for c in o["package"]), key=lambda x: json.dumps(x, sort_keys=True))}
        o = dict(o)
        if "item" in o:
            o.setdefault("quantity", 1)
        return o
    return sorted((one(o) for o in options), key=lambda x: json.dumps(x, sort_keys=True))


def _cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def pct_text(basis_points):
    """Canonical percentage for a cache weight in basis points (10000 = 100%): whole percent, rounded half up
    (RUL-2026-10-28-030)."""
    return str((Decimal(basis_points) / Decimal(100)).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


# RUL-2026-10-28-030 / loot tables section 0: one coloured line per tier.
TIER_COLOURS = {"Common": "#9ca3af", "Rare": "#3b82f6", "Epic": "#a855f7", "Legendary": "#f59e0b"}
TIER_LINE = re.compile(r'\s*<span\s+style\s*=\s*"\s*color\s*:\s*(?P<colour>#[0-9a-fA-F]{6})\s*;?\s*"\s*>\s*<b>\s*'
                       r'(?P<tier>[A-Za-z]+)\s+(?P<pct>\d+(?:\.\d+)?)%\s*</b>\s*</span>\s*·\s*(?P<items>.*?)\s*$')


def desc_lines(desc):
    """(raw, plain) per rendered line: split on <br>, tags stripped and whitespace collapsed for plain."""
    out = []
    for raw in re.split(r"<br\s*/?>", desc, flags=re.I):
        plain = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", raw)).strip()
        if raw.strip():
            out.append((raw.strip(), plain))
    return out


def item_text(name, qty):
    return f"{name} ×{qty}" if qty > 1 else name


def always_entries(plain):
    """The entries of an 'Always:' line, each in canonical form ('150,000 ryo', 'Name', 'Name ×n'): the label is
    dropped and the rest is split on ' · ', ', ', ' + ', ' and ' or ' or '."""
    body = re.sub(r"^\s*Always:\s*", "", plain, flags=re.I).strip().rstrip(".")
    out = []
    for part in re.split(r"\s*·\s*|,\s+|\s+\+\s+|\s+and\s+|\s+or\s+", body):
        part = re.sub(r"\s*[×x]\s*(\d+)$", r" ×\1", part.strip())
        if part:
            out.append(part)
    return out


def norm_items(text):
    """A tier line's item list as plain text: tags dropped, ', and more' read as ' and more'."""
    plain = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", text)).strip()
    return re.sub(r",?\s+and more$", " and more", plain)


def tier_items_text(entries, names):
    """The expected item list of a tier: entries joined with ' or ' (items of one bundle with ' + '), the first three
    then 'and more' past three; None when an item has no known name."""
    parts = []
    for e in entries:
        bundle = []
        for it in e.get("items") or []:
            nm = names.get(it.get("itemId"))
            if not nm:
                return None
            bundle.append(item_text(nm, int(it.get("quantity") or 1)))
        if bundle:
            parts.append(" + ".join(bundle))
    if len(parts) > 3:
        return " or ".join(parts[:3]) + " and more"
    return " or ".join(parts)


class Design:
    def __init__(self, root):
        self.root = root
        self.findings = []
        self.data = json.loads(_read(root, DESIGN))
        self.items = self.data["items"]
        self.ids = {}            # key -> id or None (pending)
        for key, rec in self.items.items():
            self.ids[key] = self._resolve(key, rec)
        self.by_id = {v: k for k, v in self.ids.items() if v}
        self.names = {}          # id -> display name, for chest-text fixed rewards
        self._load_names()
        self.runs = self._runs()
        self.banned = self._banned()
        self._verify_docs()

    def err(self, where, field, msg, level="ERROR"):
        self.findings.append(Finding(level, "design", DESIGN, where, field, msg))

    def _resolve(self, key, rec):
        if rec.get("id_from"):
            src = rec["id_from"]
            try:
                return json.loads(_read(self.root, src["file"])).get(src["key"]) or None
            except (OSError, ValueError) as e:
                self.err(f"items.{key}", "id_from", f"cannot read {src['file']}: {e}")
                return None
        rid = rec.get("id")
        if rid:
            self._verify_literal(f"items.{key}", rid, rec.get("source"))
        return rid

    def _verify_literal(self, where, rid, sources):
        if not sources:
            self.err(where, "source", f"id {rid} names no source file; ids must come from an existing state file")
            return
        for src in [sources] if isinstance(sources, str) else sources:
            try:
                if rid in _read(self.root, src):
                    return
            except OSError:
                pass
        self.err(where, "id", f"id {rid} not found in {sources}; the design data is stale")

    def _load_names(self):
        for key, rec in self.items.items():
            if self.ids.get(key) and rec.get("name"):
                self.names[self.ids[key]] = rec["name"]
        try:
            for row in json.loads(_read(self.root, NAMES)).get("rows", []):
                if isinstance(row, list) and len(row) >= 2:
                    self.names.setdefault(row[0], row[1])
        except (OSError, ValueError):
            pass

    def _runs(self):
        runs = {}
        for r in self.data["picks"]["runs"]:
            q = r["quest"]
            if q.get("id"):
                self._verify_literal(f"picks.{r['run']}", q["id"], q.get("source"))
            runs[r["run"]] = r
        for r in runs.values():
            if "options_from" in r:
                r["_inherited"] = True
                base = runs.get(r["options_from"])
                if base is None:
                    self.err(f"picks.{r['run']}", "options_from", f"unknown run {r['options_from']}")
                    r["options"] = []
                else:
                    r["options"] = base["options"]
            for opt in r["options"]:
                for key in self._option_keys(opt):
                    if key not in self.items:
                        self.err(f"picks.{r['run']}", "options", f"unknown item key {key}")
        for ret in self.data.get("retired", []):
            for f in ("quest_id", "item_id"):
                if ret.get(f):
                    self._verify_literal(f"retired.{ret['name']}", ret[f], ret.get("source"))
        return runs

    @staticmethod
    def _option_keys(opt):
        if "package" in opt:
            return [k for c in opt["package"] for k in Design._option_keys(c)]
        return [opt[k] for k in ("item", "jutsu", "badge") if k in opt]

    def _banned(self):
        voice = self.data["voice"]
        marker = voice["doc_marker"]
        line = next((ln for ln in _read(self.root, BIBLE).splitlines() if ln.startswith(marker)), None)
        words = []
        if line is None:
            self.err("voice", "doc_marker", f"the story bible has no line starting {marker!r}")
        else:
            body = line[len(marker):].strip().rstrip(".")
            words = [w.strip() for w in body.split(",") if w.strip()]
        pats = [(w, re.compile(r"\b" + re.escape(w) + r"\b", re.I)) for w in words]
        pats += [(p["phrase"], re.compile(p["pattern"], re.I)) for p in voice.get("extra_banned_phrases", [])]
        return pats

    def _verify_docs(self):
        loot = _read(self.root, LOOT)
        picks = self.data["picks"]
        sec = _section(loot, picks["doc_section"])
        if sec is None:
            self.err("picks", "doc_section", f"{LOOT} has no heading starting {picks['doc_section']!r}")
            sec = []
        if picks["doc_rule"] not in "\n".join(sec):
            self.err("picks", "doc_rule", f"{LOOT} section 4a no longer states {picks['doc_rule']!r}")
        table, header_pick = {}, None
        for ln in sec:
            c = _cells(ln) if ln.strip().startswith("|") else None
            if not c or len(c) < 2 or set(c[0]) <= set("-:"):
                continue
            if c[0] == "Run":
                m = re.search(r"pick (\d+)", c[1])
                header_pick = int(m.group(1)) if m else None
            else:
                table[c[0]] = c[1]
        if header_pick is None:
            self.err("picks", "doc_section", "section 4a's table header no longer states the default '(pick N)'")
        self._bind_values(loot, table, header_pick)
        data_rows = {}
        for r in picks["runs"]:
            data_rows.setdefault(r["doc_row"], set()).add(r["doc_options"])
        for row, cell in table.items():
            if row not in data_rows:
                self.err("picks", "doc_row", f"section 4a row {row!r} has no entry in the design data")
            elif data_rows[row] != {cell}:
                self.err(f"picks.{row}", "doc_options",
                         f"section 4a now reads {cell!r}; re-derive the options and update doc_options")
        for row in data_rows:
            if row not in table:
                self.err(f"picks.{row}", "doc_row", f"no section 4a row {row!r}; the doc and the data diverged")
        sec0 = "\n".join(_section(loot, "## 0.") or [])
        for tier, colour in TIER_COLOURS.items():
            if f'<span style="color:{colour}"><b>{tier} ' not in sec0:
                self.err("chest-text", "TIER_COLOURS",
                         f"loot tables section 0 no longer shows {tier} in {colour}; update TIER_COLOURS to match")
        rulings = _read(self.root, RULINGS)
        for t in self.data["chart_tiers"]["tiers"]:
            if t["doc_row"] not in rulings:
                self.err(f"chart_tiers.{t['tier']}", "doc_row", f"{RULINGS} no longer has the row {t['doc_row']!r}")
            for key in t["charts"]:
                if key not in self.items:
                    self.err(f"chart_tiers.{t['tier']}", "charts", f"unknown item key {key}")
        pc = self.data["profession_chests"]
        sec4b = "\n".join(_section(loot, "## 4b.") or [])
        for a in pc["areas"]:
            if a["doc_row"] not in sec4b:
                self.err("profession_chests.areas", "doc_row", f"section 4b no longer has {a['doc_row']!r}")
            for run in a["runs"]:
                if run not in self.runs:
                    self.err("profession_chests.areas", "runs", f"unknown run {run!r}")

    def _bind_values(self, loot, table, header_pick):
        """Re-derive every run's pick count and options from the section 4a cell itself and fail when the machine
        values disagree, so the data cannot keep the doc's prose while carrying other numbers."""
        picks = self.data["picks"]
        aliases = picks.get("doc_aliases", {})
        for key, a in aliases.items():
            if not isinstance(a, dict):
                continue
            if "money" in a and not (isinstance(a.get("evidence"), str) and a["evidence"].strip()
                                     and isinstance(a.get("evidence_file"), str) and a["evidence_file"].strip()):
                # A money alias sets an amount, so it must always cite the ruling that sets it.
                self.err(f"picks.doc_aliases.{key}", "evidence",
                         "a money alias needs a non-empty evidence sentence and evidence_file")
                continue
            if not a.get("evidence"):
                continue
            if a["evidence"] not in _read(self.root, a["evidence_file"]):
                self.err(f"picks.doc_aliases.{key}", "evidence", f"{a['evidence_file']} no longer states {a['evidence']!r}")
            if "money" in a:
                # The alias amount must equal the amount its ruling sentence states, not just cite the sentence.
                amounts = [int(x.replace(",", "")) for x in re.findall(r"([\d,]+) ryo", a["evidence"])]
                if not amounts:
                    self.err(f"picks.doc_aliases.{key}", "evidence", "the evidence sentence states no ryo amount")
                elif a["money"] != amounts[0]:
                    self.err(f"picks.doc_aliases.{key}", "money",
                             f"the alias says {a['money']} ryo; its ruling sentence says {amounts[0]} ryo")
        by_name = {rec["name"]: k for k, rec in self.items.items() if rec.get("name")}
        for r in picks["runs"]:
            cell = table.get(r["doc_row"])
            if cell is None:
                continue
            where = f"picks.{r['run']}"
            m = re.match(r"\*\*pick (\d+)\*\* from their rare's options", cell)
            if m:
                want_pick = int(m.group(1))
                if not r.get("_inherited"):
                    self.err(where, "options", "section 4a gives this run its rare's options; use options_from")
                for ev in r.get("doc_evidence", []):
                    if ev not in loot:
                        self.err(where, "doc_evidence", f"{LOOT} no longer states {ev!r}")
                if not r.get("doc_evidence"):
                    self.err(where, "doc_evidence", "an inherited run needs doc_evidence tying it to its rare run")
                else:
                    self._bind_inheritance(where, r)
            else:
                want_pick = header_pick
                try:
                    want = [self._parse_option(t, aliases, by_name) for t in re.split(r"\s+/\s+", _strip_refs(cell))]
                except ValueError as e:
                    self.err(where, "doc_options", str(e))
                    want = None
                if r.get("_inherited"):
                    self.err(where, "options_from", "section 4a lists this run's own options; options_from is wrong")
                elif want is not None and _canon(want) != _canon(r["options"]):
                    self.err(where, "options",
                             f"the data's options {_canon(r['options'])} disagree with section 4a's {_canon(want)}")
            if want_pick is not None and r.get("pickCount") != want_pick:
                self.err(where, "pickCount", f"the data says pick {r.get('pickCount')}; section 4a says pick {want_pick}")

    def _bind_inheritance(self, where, r):
        """Derive the inherited run from section 5's two evidence lines and require options_from to equal it:
        "- **<run>** (tainted <chart>)" names the chart, and "| <chart> | <source> | **<rare run>**" names the run
        that chart opens."""
        ev = r.get("doc_evidence", [])
        m0 = re.match(r"- \*\*(.+?)\*\* \(tainted (.+?)\)", ev[0]) if ev else None
        m1 = re.match(r"\| (.+?) \| .+? \| \*\*(.+?)\*\*", ev[1]) if len(ev) > 1 else None
        if not (m0 and m1):
            self.err(where, "doc_evidence", "inheritance evidence must be the run's '(tainted <chart>)' line and that chart's row")
            return
        if m0.group(1) != r["run"]:
            self.err(where, "doc_evidence", f"the tainted line names {m0.group(1)!r}, not this run")
        norm = lambda n: re.sub(r"^The ", "", n.strip())  # the doc writes "Last Heading" and "The Last Heading"
        if norm(m1.group(1)) != norm(m0.group(2)):
            self.err(where, "doc_evidence", f"the chart row is for {m1.group(1)!r}, not the tainted chart {m0.group(2)!r}")
        if norm(m1.group(2)) != norm(r.get("options_from", "")):
            self.err(where, "options_from",
                     f"section 5 ties this run to {m1.group(2)!r}; options_from says {r.get('options_from')!r}")

    def _parse_option(self, text, aliases, by_name):
        text = re.sub(r"\s*\(one package card\)$", "", text.strip())
        if " + " in text:
            return {"package": [self._parse_option(t, aliases, by_name) for t in text.split(" + ")]}
        m = re.fullmatch(r"([\d,]+) ryo", text)
        if m:
            return {"money": int(m.group(1).replace(",", ""))}
        m = re.fullmatch(r"(.+?)(?: ×(\d+))?", text)
        name, qty = m.group(1), int(m.group(2) or 1)
        target = aliases.get(name, by_name.get(name))
        if isinstance(target, dict):
            target = target.get("key") or {k: v for k, v in target.items() if k == "money"}
            if isinstance(target, dict):
                return dict(target)
        if not target or target not in self.items:
            raise ValueError(f"section 4a option {text!r} names nothing in items or doc_aliases")
        kind = self.items[target]["kind"]
        return {"item": target, "quantity": qty} if kind == "item" else {kind: target}

    # --- lookups used by the checks
    def run_for_quest(self, it):
        tid, name = it.get("targetId"), (it.get("data") or {}).get("name")
        for r in self.runs.values():
            if tid and r["quest"].get("id") == tid:
                return r
        if name:
            for r in self.runs.values():
                if name in r["quest"].get("names", []) and not (tid and r["quest"].get("id")):
                    return r
        return None

    def chart_keys(self):
        out = {}
        for t in self.data["chart_tiers"]["tiers"]:
            for key in t["charts"]:
                out[key] = t
        return out

    def chest_rules(self):
        return {self.ids[c["key"]]: c for c in self.data["profession_chests"]["chests"] if self.ids.get(c["key"])}

    def area_tiers(self, run_name):
        for a in self.data["profession_chests"]["areas"]:
            if run_name in a["runs"]:
                return set(a["tiers"])
        return None

    def known_ids(self):
        ids = set(self.by_id)
        ids |= {r["quest"]["id"] for r in self.runs.values() if r["quest"].get("id")}
        for ret in self.data.get("retired", []):
            ids |= {ret.get("quest_id"), ret.get("item_id")} - {None}
        return ids

    def known_names(self):
        names = {rec["name"] for rec in self.items.values() if rec.get("name")}
        for r in self.runs.values():
            names |= set(r["quest"].get("names", []))
        return names


# ---------------------------------------------------------------- cards
def _num(v):
    try:
        f = float(v)
    except (TypeError, ValueError):
        return 0
    return int(f) if f == int(f) else f


def reward_cards(reward):
    """The pickable cards of a choose-mode reward, normalised for comparison (see AMOUNT_FIELDS provenance). Direct
    cards are guaranteed, so a direct item card carries no drop chance. A package card is granted whole, so it carries
    its complete payload (package_payload)."""
    cards = []
    if not isinstance(reward, dict):
        return cards, []
    unresolved = []
    for f in AMOUNT_FIELDS:
        amt = int(_num(reward.get(f) or 0))
        if amt > 0:
            cards.append(("money", amt) if f == "reward_money" else (f, amt))
    for entry in reward.get("reward_items") or []:
        q = max(1, int(_num(entry.get("quantity") or 1)))
        for cid in dict.fromkeys(entry.get("ids") or []):
            cards.append(("item", cid, q))
    for f, kind in CONTENT_FIELDS.items():
        for cid in dict.fromkeys(reward.get(f) or []):
            cards.append((kind, cid))
    for pack in reward.get("reward_packages") or []:
        if isinstance(pack, dict) and isinstance(pack.get("rewards"), dict):
            payload = package_payload(pack["rewards"])
            if payload:
                cards.append(("package", payload))
        else:
            unresolved.append(pack)
    return cards, unresolved


STRUCTURAL_NONE = (None, "", "NONE", "None")


def package_payload(rewards):
    """Everything a package grants when picked, as a sorted tuple: scalar amounts, every item id with its quantity AND
    drop chance (`number`, 100 = guaranteed), content ids, structural outcomes (rank, village, mastery promotion,
    hunter/gathering drops with their id lists), nested packages, and any other reward_* field that carries a value."""
    out = []
    handled = set(AMOUNT_FIELDS) | set(CONTENT_FIELDS) | {"reward_items", "reward_packages"} \
        | set(PROFESSION_FLAGS) | set(PROFESSION_FLAGS.values())
    for f in AMOUNT_FIELDS:
        amt = _num(rewards.get(f) or 0)
        if amt > 0:
            out.append(("money", amt) if f == "reward_money" else (f, amt))
    for entry in rewards.get("reward_items") or []:
        q = max(1, int(_num(entry.get("quantity") or 1)))
        n = _num(entry.get("number", 100))
        for cid in dict.fromkeys(entry.get("ids") or []):
            out.append(("item", cid, q, n))
    for f, kind in CONTENT_FIELDS.items():
        for cid in dict.fromkeys(rewards.get(f) or []):
            out.append((kind, cid))
    for flag, ids in PROFESSION_FLAGS.items():
        if rewards.get(flag) is True:
            out.append((flag, tuple(sorted(rewards.get(ids) or []))))
    for pack in rewards.get("reward_packages") or []:
        inner = package_payload(pack.get("rewards") or {}) if isinstance(pack, dict) else ()
        out.append(("package", inner) if inner else ("package_ref", json.dumps(pack, sort_keys=True)))
    for k in sorted(rewards):
        if k.startswith("reward_") and k not in handled and rewards[k] not in STRUCTURAL_NONE and _carries(rewards[k]):
            out.append((k, json.dumps(rewards[k], sort_keys=True)))
    return tuple(sorted(out, key=str))


def option_card(design, opt):
    """(card, pending_names): the normalised card for one design option, or None with the pending names. A package
    option's items are guaranteed (drop chance 100), as the design states them."""
    if "package" in opt:
        comps, pend = [], []
        for c in opt["package"]:
            card, p = option_card(design, c)
            pend += p
            if card:
                comps.append(card + (100,) if card[0] == "item" else card)
        return (None, pend) if pend else (("package", tuple(sorted(comps, key=str))), [])
    if "money" in opt:
        return ("money", int(opt["money"])), []
    for kind in ("item", "jutsu", "badge"):
        if kind in opt:
            key = opt[kind]
            rid = design.ids.get(key)
            name = design.items.get(key, {}).get("name") or key
            if not rid:
                return None, [name]
            return ((kind, rid, int(opt.get("quantity", 1))) if kind == "item" else (kind, rid)), []
    return None, ["?"]


def describe_card(design, card):
    if card[0] == "money":
        return f"{card[1]:,} ryo"
    if card[0] == "package":
        return "package[" + " + ".join(describe_card(design, c) for c in card[1]) + "]"
    if card[0] in ("item",):
        nm = design.names.get(card[1], card[1])
        text = f"{nm} ×{card[2]}" if card[2] != 1 else nm
        return text + (f" ({card[3]}% chance)" if len(card) > 3 and card[3] != 100 else "")
    if card[0] in CONTENT_FIELDS.values():
        return f"{card[0]} {design.names.get(card[1], card[1])}"
    if isinstance(card[1], (int, float)):
        return f"{card[0]} {card[1]:,}"
    return f"{card[0]} {card[1]}"


def card_ids(card):
    if card[0] == "package":
        return {i for c in card[1] for i in card_ids(c)}
    if card[0] == "item" or card[0] in CONTENT_FIELDS.values():
        return {card[1]}
    return set()


# ---------------------------------------------------------------- checks
class Checker:
    def __init__(self, design):
        self.d = design
        self.findings = []

    def add(self, level, check, file, where, field, msg):
        self.findings.append(Finding(level, check, file, where, field, msg))

    @staticmethod
    def where(i, it):
        tag = it.get("targetId") or it.get("srcId") or ""
        return f"items[{i}] {it.get('entity')}/{it.get('slot')} {tag} '{it.get('name', '')}'".replace("  ", " ")

    def run(self, path, manifest, skyglass):
        items = manifest.get("items") or []
        for i, it in enumerate(items):
            if not isinstance(it, dict):
                continue
            w = self.where(i, it)
            self.check_empty_profession_lists(path, w, it)
            if not skyglass:
                continue
            ent = it.get("entity")
            if ent == "quest":
                self.check_picks(path, w, it)
                self.check_battle_rewards(path, w, it)
                self.check_area_chests(path, w, it)
            if ent == "item":
                self.check_retired(path, w, it, "item_id")
                self.check_chest_text(path, w, it, items)
                self.check_chart_tier(path, w, it)
                self.check_prof_chest(path, w, it)
            self.check_voice(path, w, it)

    # 1. picks
    def check_picks(self, f, w, it):
        data = it.get("data") or {}
        if self.check_retired(f, w, it, "quest_id"):
            return
        run = self.d.run_for_quest(it)
        content = data.get("content")
        if run is None:
            if isinstance(content, dict) and content.get("rewardMode") == "choose":
                self.add("WARN", "picks", f, w, "data.content.rewardMode",
                         "choose-mode quest not in the section 4a table (state/skyglass_design/design_data.json)")
            return
        if not isinstance(content, dict):
            return  # the edit does not touch the quest body
        label = f"[{run['run']}]"
        if content.get("rewardMode") != "choose":
            self.add("ERROR", "picks", f, w, "data.content.rewardMode",
                     f"{label} is {content.get('rewardMode')!r}; section 4a needs 'choose'")
        pc = content.get("rewardPickCount", 1)
        if pc != run["pickCount"]:
            self.add("ERROR", "picks", f, w, "data.content.rewardPickCount",
                     f"{label} is {pc}; section 4a needs {run['pickCount']}")
        actual, unresolved = reward_cards(content.get("reward"))
        for pack in unresolved:
            self.add("WARN", "picks", f, w, "data.content.reward.reward_packages",
                     f"{label} package {pack!r} carries no rewards snapshot; cannot compare it")
        expected, pending = Counter(), []
        for opt in run["options"]:
            card, pend = option_card(self.d, opt)
            if card is None:
                pending.append(" + ".join(pend))
            else:
                expected[card] += 1
        got = Counter(actual)
        missing = expected - got
        extra = got - expected
        known = self.d.known_ids()
        budget = len(pending)
        for card, n in sorted(missing.items(), key=str):
            for _ in range(n):
                self.add("ERROR", "picks", f, w, "data.content.reward",
                         f"{label} missing option: {describe_card(self.d, card)}")
        for card, n in sorted(extra.items(), key=str):
            for _ in range(n):
                unknown = card_ids(card) - known
                if unknown and budget > 0:
                    budget -= 1
                    self.add("WARN", "picks", f, w, "data.content.reward",
                             f"{label} card {describe_card(self.d, card)} may be a pending option; unverified")
                else:
                    self.add("ERROR", "picks", f, w, "data.content.reward",
                             f"{label} option not in section 4a: {describe_card(self.d, card)}")
        for name in pending:
            self.add("WARN", "picks", f, w, "data.content.reward",
                     f"{label} pending: {name} has no id yet (not created); option not verifiable")

    def check_retired(self, f, w, it, id_field):
        """A retired record may only be hidden: the whole payload must be exactly {"hidden": true} on an edit.
        Returns True when the item targets a retired record."""
        for ret in self.d.data.get("retired", []):
            if not (it.get("targetId") and it["targetId"] == ret.get(id_field)):
                continue
            data = it.get("data")
            why = f"{ret['name']} is retired ({ret['ruling']}); an edit may only hide it"
            if it.get("slot") != "edit":
                self.add("ERROR", "picks", f, w, "slot", f"{why}, but this is a '{it.get('slot')}'")
            if not isinstance(data, dict) or data.get("hidden") is not True:
                self.add("ERROR", "picks", f, w, "data.hidden", why)
            extra = sorted(set(data) - {"hidden"}) if isinstance(data, dict) else []
            if extra:
                cards, _ = reward_cards(((data.get("content") or {}).get("reward")))
                offer = (" (still offers " + " / ".join(describe_card(self.d, c) for c in cards) + ")") if cards else ""
                self.add("ERROR", "picks", f, w, "data",
                         f"{why}; the payload also sends {', '.join(extra)}{offer}")
            return True
        return False

    # 2. win-only rewards
    def check_battle_rewards(self, f, w, it):
        content = (it.get("data") or {}).get("content")
        objs = content.get("objectives") if isinstance(content, dict) else None
        for j, o in enumerate(objs or []):
            if not isinstance(o, dict) or o.get("task") not in BATTLE_TASKS:
                continue
            for k, v in o.items():
                if not k.startswith("reward_") or k in BATTLE_ALLOWED:
                    continue
                if _carries(v):
                    self.add("ERROR", "win-only", f, w, f"data.content.objectives[{j}].{k} ({o.get('id')})",
                             f"battle objective pays {k}={v!r}; rewards pay at a win ending (RUL-2026-10-28-022)")

    def check_empty_profession_lists(self, f, w, it):
        for path, d in _walk(it.get("data"), "data"):
            for flag, ids in PROFESSION_FLAGS.items():
                if d.get(flag) is True and not d.get(ids):
                    self.add("ERROR", "win-only", f, w, f"{path}.{ids}",
                             f"{flag} is true with an empty id list, which rolls the whole pool (RUL-2026-10-28-023)")

    # 3. chest descriptions
    def check_chest_text(self, f, w, it, all_items):
        data = it.get("data") or {}
        effects = data.get("effects")
        if not isinstance(effects, list):
            return
        caches = [e for e in effects if isinstance(e, dict) and e.get("type") == "noncombatconsumereward"
                  and e.get("rewardMode") == "weightedCache" and isinstance(e.get("weightedCache"), dict)]
        if not caches:
            return
        desc = data.get("description")
        if not isinstance(desc, str) or not desc.strip():
            self.add("ERROR", "chest-text", f, w, "data.description",
                     "the effects set a weighted cache but the edit sends no description; the live text cannot be "
                     "shown to match the weights (loot tables section 0)")
            return
        names = dict(self.d.names)
        for other in all_items:
            od = (other or {}).get("data") or {}
            if other.get("entity") == "item" and other.get("targetId") and od.get("name"):
                names[other["targetId"]] = od["name"]
        lines = desc_lines(desc)
        self._always_line(f, w, lines, effects, names)
        for e in caches:
            self._cache_text(f, w, lines, e["weightedCache"], names)

    def _always_line(self, f, w, lines, effects, names):
        fld = "data.description"
        parts, unknown = [], 0
        for e in effects:
            if not isinstance(e, dict) or e.get("type") != "noncombatconsumereward" or e.get("rewardMode") == "weightedCache":
                continue
            money = int(float(e.get("reward_money") or 0))
            if money > 0:
                parts.append(f"{money:,} ryo")
            exp = int(float(e.get("reward_exp") or 0))
            if exp > 0:
                parts.append(f"{exp:,} exp")
            for entry in e.get("reward_items") or []:
                q = max(1, int(entry.get("quantity") or 1))
                for iid in entry.get("ids") or []:
                    nm = names.get(iid)
                    if not nm:
                        unknown += 1
                        self.add("WARN", "chest-text", f, w, fld,
                                 f"fixed reward item {iid}{' ×' + str(q) if q > 1 else ''}: no known name to check against")
                    else:
                        parts.append(item_text(nm, q))
        always = [plain for raw, plain in lines if re.match(r"\s*<b>\s*Always:\s*</b>", raw, re.I)]
        if not parts and not unknown:
            for a in always:
                self.add("ERROR", "chest-text", f, w, fld, f"'{a}' but the item has no fixed reward")
            return
        if not always:
            self.add("ERROR", "chest-text", f, w, fld,
                     "fixed reward not stated: needs '<b>Always:</b> " + (" · ".join(parts) or "…")
                     + "' (RUL-2026-10-28-030)")
            return
        if len(always) > 1:
            self.add("ERROR", "chest-text", f, w, fld, "more than one 'Always:' line")
        stated = Counter(always_entries(always[0]))
        want = Counter(parts)
        for p in sorted((want - stated).elements()):
            self.add("ERROR", "chest-text", f, w, fld, f"'Always:' line '{always[0]}' does not state '{p}'")
        budget = unknown
        for p in sorted((stated - want).elements()):
            if budget > 0 and not re.search(r"\d ?(ryo|exp)$", p):
                budget -= 1
                self.add("WARN", "chest-text", f, w, fld, f"'Always:' entry '{p}' may be the unnamed fixed item; unverified")
            else:
                self.add("ERROR", "chest-text", f, w, fld,
                         f"'Always:' line states '{p}', which the item does not grant on every opening")

    def _cache_text(self, f, w, lines, cache, names):
        fld = "data.description"
        totals, order, entries = {}, [], {}
        for t in cache.get("tiers") or []:
            p = int(t.get("probability") or 0)
            if p <= 0:
                continue
            name = (t.get("name") or "").strip()
            if name not in totals:
                order.append(name)
            totals[name] = totals.get(name, 0) + p
            entries.setdefault(name, []).extend(t.get("entries") or [])
        stated = {}
        for raw, plain in lines:
            m = TIER_LINE.match(raw)
            if m:
                stated.setdefault(m.group("tier"), []).append((m.group("colour").lower(), m.group("pct"), m.group("items")))
                continue
            m = re.search(r"\b(" + "|".join(TIER_WORDS) + r")\s+\d+(?:\.\d+)?\s*%", plain, re.I)
            if m:
                self.add("ERROR", "chest-text", f, w, fld,
                         f"'{plain}' states a tier rate outside the coloured tier-line format (RUL-2026-10-28-030)")
        for name in order:
            want = pct_text(totals[name])
            colour = TIER_COLOURS.get(name)
            got = stated.pop(name, [])
            if colour is None:
                self.add("ERROR", "chest-text", f, w, fld, f"tier '{name}' has no colour in the RUL-2026-10-28-030 format")
            if not got:
                self.add("ERROR", "chest-text", f, w, fld,
                         f"no tier line for '{name}': needs '<span style=\"color:{colour or '?'}\"><b>{name} {want}%</b></span> · …'")
                continue
            if len(got) > 1:
                self.add("ERROR", "chest-text", f, w, fld, f"tier '{name}' has {len(got)} lines; same-named tiers share one")
            c, pct, items = got[0]
            if colour and c != colour:
                self.add("ERROR", "chest-text", f, w, fld, f"tier '{name}' is coloured {c}; the format uses {colour}")
            if pct != want:
                self.add("ERROR", "chest-text", f, w, fld, f"tier '{name}' stated {pct}% but the cache weight is {want}%")
            expect = tier_items_text(entries[name], names)
            if expect is None:
                self.add("WARN", "chest-text", f, w, fld, f"tier '{name}' lists an item with no known name; items not checked")
            elif norm_items(items) != expect:
                self.add("ERROR", "chest-text", f, w, fld,
                         f"tier '{name}' lists '{norm_items(items)}' but the cache gives '{expect}'")
        for name in stated:
            self.add("ERROR", "chest-text", f, w, fld, f"tier line for '{name}' but the cache has no such tier")
        rolls = [r for r in cache.get("rolls") or [] if int(r.get("probability") or 0) > 0]
        counts = sorted({int(r["count"]) for r in rolls})
        roll_lines = [plain for _, plain in lines if re.search(r"\brolls?\b", plain, re.I)
                      and not re.match(r"\s*Each roll:?\s*$", plain, re.I)]
        if not rolls:
            self.add("ERROR", "chest-text", f, w, "data.effects.weightedCache.rolls", "the cache has no active roll")
        elif len(counts) > 1:
            want = f"{counts[0]}–{counts[-1]} rolls"
            if not any(re.search(rf"(?<!\d){counts[0]}\s*[–-]\s*{counts[-1]}\s+rolls\b", p) for p in roll_lines):
                self.add("ERROR", "chest-text", f, w, fld, f"the roll count varies; needs a roll line '{want}'")
        else:
            for p in roll_lines:
                self.add("WARN", "chest-text", f, w, fld,
                         f"'{p}': the roll count is fixed ({counts[0]}) and the item card already shows it")

    # 4. voice
    def check_voice(self, f, w, it):
        data = it.get("data")
        if it.get("entity") in ("ai", "aiProfile"):
            texts = [("data.username", (data or {}).get("username"))]
        elif it.get("entity") == "asset":
            return
        else:
            texts = [(p, v) for p, v in _texts(data, "data")]
        for path, text in texts:
            if not isinstance(text, str):
                continue
            for word, pat in self.d.banned:
                m = pat.search(text)
                if m:
                    lo = max(0, m.start() - 30)
                    self.add("ERROR", "voice", f, w, path,
                             f"banned word '{word}' (story bible, Voice): ...{text[lo:m.end() + 30]}...")

    # 5. chart tier
    def check_chart_tier(self, f, w, it):
        data = it.get("data") or {}
        for key, tier in self.d.chart_keys().items():
            rid, name = self.d.ids.get(key), self.d.items[key].get("name")
            hit = (rid and it.get("targetId") == rid) or (it.get("slot") == "create" and name and data.get("name") == name)
            if not hit:
                continue
            if "rarity" in data:
                if data["rarity"] != tier["rarity"]:
                    self.add("ERROR", "chart-tier", f, w, "data.rarity",
                             f"{name or key} is {data['rarity']}; {tier['tier']} are {tier['rarity']} (RUL-2026-10-28-028)")
            elif it.get("slot") == "create":
                self.add("ERROR", "chart-tier", f, w, "data.rarity",
                         f"{name or key} is created without a rarity; {tier['tier']} are {tier['rarity']}")

    # 6. profession chests
    def check_prof_chest(self, f, w, it):
        rule = self.d.chest_rules().get(it.get("targetId"))
        if not rule:
            return
        data = it.get("data") or {}
        name = self.d.items[rule["key"]]["name"]
        if "rarity" in data and data["rarity"] != rule["rarity"]:
            self.add("ERROR", "prof-chest", f, w, "data.rarity",
                     f"{name} is {data['rarity']}; section 4b sets {rule['rarity']}")
        want = {"canBeHunted": rule["profession"] == "hunter", "canBeGathered": rule["profession"] == "gatherer"}
        for flag, val in want.items():
            if flag in data and bool(data[flag]) != val:
                self.add("ERROR", "prof-chest", f, w, f"data.{flag}", f"{name} needs {flag}={str(val).lower()}")
        if "rarity" not in data or not any(k in data for k in want):
            self.add("WARN", "prof-chest", f, w, "data",
                     f"{name} edited without " + ("rarity" if "rarity" not in data else "its hunt/gather flag"))

    def check_area_chests(self, f, w, it):
        run = self.d.run_for_quest(it)
        if run is None:
            return
        tiers = self.d.area_tiers(run["run"])
        rules = self.d.chest_rules()
        prof = {"reward_hunter_items_ids": "hunter", "reward_gathering_items_ids": "gatherer"}
        for path, d in _walk(it.get("data"), "data"):
            for flag, ids_key in PROFESSION_FLAGS.items():
                if d.get(flag) is not True:
                    continue
                for cid in d.get(ids_key) or []:
                    r = rules.get(cid)
                    if r is None or r["profession"] != prof[ids_key]:
                        self.add("ERROR", "prof-chest", f, w, f"{path}.{ids_key}",
                                 f"[{run['run']}] {cid} is not a {prof[ids_key]} profession chest (section 4b)")
                    elif tiers is not None and r["tier"] not in tiers:
                        self.add("ERROR", "prof-chest", f, w, f"{path}.{ids_key}",
                                 f"[{run['run']}] {self.d.items[r['key']]['name']} is outside the area's tier "
                                 f"({' + '.join(sorted(tiers))})")


def _carries(v):
    if v is None or v is False:
        return False
    if isinstance(v, (int, float)):
        return v != 0
    if isinstance(v, str):
        return v not in ("", "NONE", "None")
    if isinstance(v, (list, dict)):
        return len(v) > 0
    return True


def _walk(o, path):
    if isinstance(o, dict):
        yield path, o
        for k, v in o.items():
            yield from _walk(v, f"{path}.{k}")
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from _walk(v, f"{path}[{i}]")


def _texts(o, path):
    if isinstance(o, dict):
        for k, v in o.items():
            if k in TEXT_KEYS and isinstance(v, str):
                yield f"{path}.{k}", v
            elif isinstance(v, (dict, list)):
                yield from _texts(v, f"{path}.{k}")
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from _texts(v, f"{path}[{i}]")


def is_skyglass(rel, manifest, design):
    if SKYGLASS_FILE.search(os.path.basename(rel)):
        return True
    ids, names = design.known_ids(), design.known_names()
    for it in manifest.get("items") or []:
        if not isinstance(it, dict):
            continue
        if it.get("targetId") in ids or ((it.get("data") or {}).get("name") in names and it.get("slot") == "create"):
            return True
    return False


def check(root, paths=None):
    """Run every check. paths None = every write manifest in push/. Returns (findings, scanned, io_errors)."""
    design = Design(root)
    checker = Checker(design)
    explicit = paths is not None
    if paths is None:
        paths = sorted(glob.glob(os.path.join(root, "push", "*.json")))
    scanned, io_errors = [], []
    for p in paths:
        rel = os.path.relpath(os.path.abspath(p), root)
        try:
            with open(p, encoding="utf-8") as fh:
                m = json.load(fh)
        except (OSError, ValueError) as e:
            io_errors.append(f"{rel}: {e}")
            continue
        if not isinstance(m, dict) or not m.get("items"):
            continue  # captures and reads carry no write items
        sky = explicit or is_skyglass(rel, m, design)
        scanned.append((rel, sky))
        checker.run(rel, m, sky)
    return design.findings + checker.findings, scanned, io_errors


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("manifests", nargs="*", help="manifests to check (default: every Skyglass manifest in push/)")
    ap.add_argument("--json", action="store_true", help="print findings as JSON")
    ap.add_argument("--root", default=ROOT, help=argparse.SUPPRESS)
    a = ap.parse_args(argv)
    findings, scanned, io_errors = check(a.root, a.manifests or None)
    errors = sum(1 for x in findings if x.level == "ERROR")
    warns = len(findings) - errors
    if a.json:
        print(json.dumps({"scanned": [{"file": f, "skyglass": s} for f, s in scanned], "io_errors": io_errors,
                          "errors": errors, "warnings": warns, "findings": [x.as_dict() for x in findings]}, indent=1))
    else:
        for x in findings:
            print(x)
        for e in io_errors:
            print(f"ERROR [io] {e}")
        sky = [f for f, s in scanned if s]
        print(f"skyglass_check: {len(sky)} Skyglass manifest(s) fully checked ({', '.join(sky) or 'none'}); "
              f"{len(scanned) - len(sky)} other write manifest(s) checked for empty profession lists; "
              f"{errors} error(s), {warns} warning(s)")
    if io_errors:
        return 2
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
