#!/usr/bin/env python3
"""generation_preflight.py - deterministic art generation contract renderer.

Repository-ready is not generation-ready. A fresh art session can hold the
spec, the reference index, every hash and every URL and still reach the image
generator without one selected reference pixel ever having been rendered into
its visual context. The Road Bandit failure was exactly that. This tool makes
the boundary explicit: it renders, deterministically, everything the repository
CAN prove about one generation, and initialises everything it CANNOT prove as
unverified.

    python3 generation_preflight.py prepare --repo-root . \
        --target SCENE_CHARACTER --register NINJA --frame full \
        --subject "generic Road Bandit; lone adult male roadside shinobi ambusher; anonymous and unbranded" \
        --repo-ref <EXACT_40_HEX_SHA>            [--json] [--out packet.json]
    python3 generation_preflight.py check packet.json --repo-root .
    python3 generation_preflight.py --selftest

WHAT THIS IS
  A contract renderer. It reuses the canonical implementations and copies no
  wording of its own:
    - shotlist.render_prompt      the prompt scaffold, [STYLE] expanded verbatim
    - style_refs.verify / select  reference-pack provenance and selection
    - 25x_DATA_art_spec.json      the sole owner of house style and targets
    - style_refs.json             reference metadata, hashes and provenance

WHAT THIS IS NOT
  It generates nothing, invents no prompt wording, is not a second style
  authority and does not duplicate a scaffold or a house-style clause. It
  cannot see a ChatGPT conversation or the image tool, so it cannot know
  whether the selected pixels were rendered, which reference mode applies, or
  whether the generation context is clean. Those runtime fields are emitted
  as false / UNDECLARED and only the current session may change them, by
  stating what it actually did.

FAIL CLOSED
  No packet is emitted unless the reference pack verifies (bytes, dimensions,
  format AND capture provenance), the target/register/frame exist, every
  selected reference exists and hash-matches the index, no selected reference
  is excluded/deprecated, the subject is supplied, the repo ref is an exact
  40-hex commit id, and the canonical prompt renders with no token left over.

Stdlib only, deterministic, socket-free. The generation-contract hash is a
SHA-256 over the canonical JSON serialisation named in CANONICAL_JSON.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import shotlist  # noqa: E402
import style_refs  # noqa: E402

SCHEMA = "tnr.generation_preflight"
VERSION = 1
CONTRACT_SCHEMA = "tnr.generation_contract"

CANONICAL_JSON = (
    "json.dumps(obj, sort_keys=True, separators=(',', ':'), ensure_ascii=False)"
    ".encode('utf-8'), hashed with SHA-256"
)

SKILL_ROOT = HERE.parent
DEFAULT_SPEC_NAME = "25x_DATA_art_spec.json"
WORKSTREAMS_DIR = "state/workstreams"

# The three ways a session may stand relative to the selected references.
# Definitions are one line each on purpose: the workflow documents own the
# procedure; this packet only needs the terms to be unambiguous.
REFERENCE_MODES = {
    "ATTACHED": (
        "the selected individual reference images are actual rendered image "
        "attachments / input images in the current generation conversation"
    ),
    "ASSISTANT_GROUNDED": (
        "the assistant actually visually inspected the selected pixels, but the "
        "generation surface cannot receive them as image inputs; the canonical "
        "text contract is used, grounded by that inspection, with no claim of "
        "reference-image conditioning"
    ),
    "NOT_HYDRATED": (
        "only metadata, paths, URLs or unrendered bytes/base64 are available; "
        "image generation is forbidden until hydration occurs"
    ),
}

# Every field a session must prove for itself. Initialised closed.
RUNTIME_STATE_UNVERIFIED = {
    "visual_reference_pixels_inspected": False,
    "reference_mode": "UNDECLARED",
    "clean_asset_context_confirmed": False,
    "generation_allowed": False,
}

RUNTIME_NOTE = (
    "This helper proves what contract was rendered and which reference bytes were "
    "selected. It cannot observe the ChatGPT conversation or the image-generation "
    "tool, so it cannot know whether those pixels were rendered into the session's "
    "visual context, which reference mode applies, or whether the generation "
    "context is clean of other asset classes. It therefore cannot flip any "
    "runtime_state field. Only the current session can, and it must say what it "
    "actually did. A path, a URL, a hash or unrendered base64 never satisfies "
    "visual_reference_pixels_inspected."
)

SHA_LENGTH = 40
SHA_ALPHABET = set("0123456789abcdef")


class PreflightError(Exception):
    """The packet could not be rendered fail-closed. Carries every reason."""

    def __init__(self, headline: str, errors: list[str]):
        super().__init__(headline)
        self.headline = headline
        self.errors = list(errors)


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------


def canonical_bytes(obj) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def sha256_bytes(blob: bytes) -> str:
    return hashlib.sha256(blob).hexdigest()


def bad_sha(value) -> str | None:
    if not isinstance(value, str):
        return "repo ref must be a string"
    if len(value) != SHA_LENGTH:
        return f"repo ref must be an exact {SHA_LENGTH}-hex commit id, got {len(value)} characters"
    if not set(value) <= SHA_ALPHABET:
        return "repo ref must be lowercase hexadecimal (a branch name such as 'main' floats and is refused)"
    return None


def rel_or_str(repo_root: Path, path: Path) -> str:
    try:
        return path.resolve().relative_to(repo_root.resolve()).as_posix()
    except ValueError:
        return str(path)


def default_spec_path() -> Path:
    packaged = SKILL_ROOT / "data" / DEFAULT_SPEC_NAME
    if packaged.exists():
        return packaged
    import os

    return Path(os.environ.get("TNR_ART_SPEC", DEFAULT_SPEC_NAME))


def load_json(path: Path, what: str) -> dict:
    try:
        with path.open(encoding="utf-8") as handle:
            return json.load(handle)
    except FileNotFoundError:
        raise PreflightError(f"{what} not found", [f"{what} not found: {path}"])
    except json.JSONDecodeError as exc:
        raise PreflightError(f"{what} is not valid JSON", [f"{what} is not valid JSON: {path}: {exc}"])


def load_roadmap_task(repo_root: Path, workstream: str, task_id: str) -> tuple[str, dict]:
    """Read one task from a committed workstream roadmap, as plain JSON.

    Only `open_decisions` and `session_gates` are consumed. The roadmap is
    coordination state and this helper never validates or rewrites it; the
    workstream tool owns that.
    """
    rel = f"{WORKSTREAMS_DIR}/{workstream}/roadmap.json"
    data = load_json(repo_root / rel, f"workstream roadmap {rel}")
    for task in data.get("tasks") or []:
        if isinstance(task, dict) and task.get("id") == task_id:
            return rel, task
    raise PreflightError(
        "workstream task not found",
        [f"{rel} carries no task {task_id!r}; the direction review cannot be surfaced from it"],
    )


# --------------------------------------------------------------------------
# packet construction
# --------------------------------------------------------------------------


def build_packet(
    spec: dict,
    spec_rel: str,
    spec_sha: str,
    index: dict,
    index_rel: str,
    index_sha: str,
    repo_root: Path,
    target: str,
    register: str | None,
    frame: str | None,
    subject: str,
    repo_ref: str,
    tags=None,
    keys=None,
    limit=None,
    roadmap: tuple[str, dict] | None = None,
    approved=style_refs.APPROVED_CAPTURE,
) -> dict:
    errors: list[str] = []

    # 1. The pack must prove itself before anything is selected from it.
    pack_errors = style_refs.verify(index, repo_root, approved=approved)
    if pack_errors:
        raise PreflightError(
            "reference pack verification failed; no packet is emitted", pack_errors
        )

    # 2. Inputs the repository can check.
    reason = bad_sha(repo_ref)
    if reason:
        errors.append(reason)

    targets = spec.get("targets") or {}
    scaffolds = (spec.get("prompt_scaffolds") or {}).get("scaffolds") or {}
    if target not in targets:
        errors.append(f"target {target!r} is not in the art spec; known: {', '.join(sorted(targets))}")
    if target not in scaffolds:
        errors.append(f"target {target!r} has no prompt scaffold in the art spec")
    if target not in style_refs.TARGETS:
        errors.append(
            f"the v1 reference pack carries no references for target {target!r} "
            f"(covered: {', '.join(style_refs.TARGETS)}); a reference-grounded generation "
            "contract cannot be staged for it. This is a known limitation, not a claim that "
            "the target needs no contract."
        )

    if target == "SCENE_CHARACTER":
        if register not in style_refs.REGISTERS:
            errors.append(
                f"SCENE_CHARACTER needs --register {' or '.join(style_refs.REGISTERS)}, got {register!r}"
            )
    elif register:
        errors.append(f"--register is only meaningful for SCENE_CHARACTER, not {target}")

    scaffold = scaffolds.get(target) or {}
    framed = "positive_by_frame" in scaffold
    if framed:
        frames = sorted(scaffold["positive_by_frame"])
        if frame not in scaffold["positive_by_frame"]:
            errors.append(
                f"{target} framing picks the aspect and is a content decision the tool cannot "
                f"make: pass --frame {' or '.join(frames)}, got {frame!r}"
            )
    elif frame:
        errors.append(f"{target} has no framed scaffold; --frame is not accepted for it")

    if not isinstance(subject, str) or not subject.strip():
        errors.append("--subject is required: an unfilled [SUBJECT] slot is not a generation contract")

    if errors:
        raise PreflightError("preflight inputs do not validate; no packet is emitted", errors)

    # 3. Deterministic selection, then per-reference fail-closed checks.
    selected = style_refs.select(index, target, register=register, tags=tags, keys=keys, limit=limit)
    if not selected:
        raise PreflightError(
            "no references selected; no packet is emitted",
            [
                f"style_refs.select returned nothing for target={target} register={register} "
                f"tags={list(tags or [])} keys={list(keys or [])}. Do not substitute; widen "
                "the filter or stop."
            ],
        )

    banned = {
        str(entry.get("name", "")).strip().lower()
        for entry in index.get("excluded", [])
        if isinstance(entry, dict)
    }
    references = []
    for ref in selected:
        key = ref.get("key", "?")
        rel = ref.get("path")
        local = repo_root / rel
        if str(ref.get("name", "")).strip().lower() in banned:
            errors.append(f"{key}: {ref.get('name')!r} is excluded/deprecated and may not be selected")
        if ref.get("target") != target:
            errors.append(f"{key}: selected reference targets {ref.get('target')!r}, not {target!r}")
        if register and ref.get("register") != register:
            errors.append(f"{key}: selected reference register {ref.get('register')!r} != {register!r}")
        if not local.is_file():
            errors.append(f"{key}: reference file is missing: {rel}")
            continue
        blob = local.read_bytes()
        digest = sha256_bytes(blob)
        if digest != ref.get("sha256"):
            errors.append(f"{key}: sha256 mismatch for {rel}: index {ref.get('sha256')}, file {digest}")
        references.append(
            {
                "key": key,
                "name": ref.get("name"),
                "target": ref.get("target"),
                "register": ref.get("register"),
                "priority": ref.get("priority"),
                "tags": list(ref.get("tags") or []),
                "path": rel,
                "sha256": digest,
                "bytes": len(blob),
                "width": ref.get("width"),
                "height": ref.get("height"),
                "format": ref.get("format"),
                "raw_url": style_refs.raw_url(index, ref, repo_ref),
                "use_for": ref.get("use_for"),
                "do_not_use_for": ref.get("do_not_use_for"),
            }
        )
    if errors:
        raise PreflightError("selected references do not validate; no packet is emitted", errors)

    # 4. The canonical prompt, rendered by the one function that owns it.
    prompt = shotlist.render_prompt(spec, target, subject, frame)
    if prompt is None:
        raise PreflightError(
            "canonical prompt did not render",
            [f"shotlist.render_prompt returned nothing for {target}; the spec lost its scaffold"],
        )
    ps = spec.get("prompt_scaffolds") or {}
    positive = prompt.get("positive") or ""
    for token in (ps.get("style_token", "[STYLE]"), ps.get("subject_token", "[SUBJECT]")):
        if token in positive:
            errors.append(f"rendered prompt still carries the {token} token")
    if prompt.get("subject_filled") is not True:
        errors.append("rendered prompt reports subject_filled != True")
    struck = (spec.get("house_style") or {}).get("struck_clauses") or {}
    for phrase in struck:
        if phrase.startswith("_"):
            continue
        if phrase.lower() in positive.lower():
            errors.append(f"rendered prompt carries struck clause {phrase!r}; that is a regression")
    if errors:
        raise PreflightError("canonical prompt does not validate; no packet is emitted", errors)

    # 5. The contract: exactly what the generator is owed. Hashed canonically.
    contract = {
        "schema": CONTRACT_SCHEMA,
        "version": VERSION,
        "target": target,
        "register": register,
        "frame": frame,
        "subject": subject,
        "spec": {"path": spec_rel, "sha256": spec_sha},
        "style_refs_index": {"path": index_rel, "sha256": index_sha},
        "references": [{"key": r["key"], "path": r["path"], "sha256": r["sha256"]} for r in references],
        "prompt": prompt,
    }
    contract_sha = sha256_bytes(canonical_bytes(contract))

    capture = index.get("source_capture") or {}
    packet = {
        "schema": SCHEMA,
        "version": VERSION,
        "repo_ref": repo_ref,
        "repo_ref_note": (
            "operator-supplied exact commit id used to pin the raw URLs; the helper cannot "
            "prove it is pushed or that the checkout matches it"
        ),
        "target": target,
        "register": register,
        "frame": frame,
        "subject": subject,
        "selection_inputs": {
            "tags": list(tags or []),
            "keys": list(keys or []),
            "limit": limit if limit is not None else style_refs.DEFAULT_LIMIT.get(target, 4),
        },
        "spec": {"path": spec_rel, "sha256": spec_sha},
        "style_refs_index": {"path": index_rel, "sha256": index_sha},
        "reference_pack": {
            "verified": True,
            "references_in_pack": len(index.get("references") or []),
            "provenance": {
                "manifest": capture.get("manifest"),
                "result": capture.get("result"),
                "job_id": capture.get("job_id"),
                "reads": capture.get("reads"),
                "mutations": capture.get("mutations"),
            },
        },
        "selected_keys": [r["key"] for r in references],
        "references": references,
        "prompt": prompt,
        "generation_contract": contract,
        "generation_contract_sha256": contract_sha,
        "canonical_json": CANONICAL_JSON,
        "reference_modes": dict(REFERENCE_MODES),
        "runtime_state": dict(RUNTIME_STATE_UNVERIFIED),
        "runtime_note": RUNTIME_NOTE,
    }

    if roadmap is not None:
        rel, task = roadmap
        packet["workstream_task"] = {"roadmap": rel, "task": task.get("id")}
        decisions = [d for d in (task.get("open_decisions") or []) if isinstance(d, str)]
        packet["direction_review_required"] = {
            "source": rel,
            "task": task.get("id"),
            "open_decisions": decisions,
            "note": (
                "user-owned art-direction decisions still open on the task; surfaced, not "
                "settled. The helper infers no override from them."
            ) if decisions else "the task carries no open decisions",
        }
        packet["session_gates"] = [
            g for g in (task.get("session_gates") or []) if isinstance(g, dict)
        ]
    return packet


def prepare(
    repo_root: Path,
    spec_path: Path,
    index_path: Path,
    target: str,
    register: str | None,
    frame: str | None,
    subject: str,
    repo_ref: str,
    tags=None,
    keys=None,
    limit=None,
    workstream: str | None = None,
    task_id: str | None = None,
    approved=style_refs.APPROVED_CAPTURE,
) -> dict:
    """CLI-level wrapper: load the inputs, hash them, build the packet."""
    spec_blob = spec_path.read_bytes() if spec_path.exists() else None
    if spec_blob is None:
        raise PreflightError("art spec not found", [f"art spec not found: {spec_path}"])
    spec = load_json(spec_path, "art spec")
    index_blob = index_path.read_bytes() if index_path.exists() else None
    if index_blob is None:
        raise PreflightError("reference index not found", [f"reference index not found: {index_path}"])
    index = load_json(index_path, "reference index")
    roadmap = None
    if workstream or task_id:
        if not (workstream and task_id):
            raise PreflightError(
                "workstream inputs incomplete", ["--workstream and --task must be given together"]
            )
        roadmap = load_roadmap_task(repo_root, workstream, task_id)
    return build_packet(
        spec,
        rel_or_str(repo_root, spec_path),
        sha256_bytes(spec_blob),
        index,
        rel_or_str(repo_root, index_path),
        sha256_bytes(index_blob),
        repo_root,
        target,
        register,
        frame,
        subject,
        repo_ref,
        tags=tags,
        keys=keys,
        limit=limit,
        roadmap=roadmap,
        approved=approved,
    )


def check_packet(packet: dict, repo_root: Path, spec_path: Path, index_path: Path,
                 approved=style_refs.APPROVED_CAPTURE) -> list[str]:
    """Re-derive a staged packet's contract from the repository and compare.

    Answers an auditor's question: does the contract this session says it
    staged match what the repository renders now for the same inputs? It
    checks the recorded hash against the recorded contract, then rebuilds.
    It does not, and cannot, check the runtime_state fields.
    """
    errors: list[str] = []
    if packet.get("schema") != SCHEMA:
        errors.append(f"packet schema is {packet.get('schema')!r}, expected {SCHEMA!r}")
        return errors
    contract = packet.get("generation_contract")
    recorded = packet.get("generation_contract_sha256")
    if not isinstance(contract, dict) or not recorded:
        errors.append("packet carries no generation_contract / generation_contract_sha256")
        return errors
    recomputed = sha256_bytes(canonical_bytes(contract))
    if recomputed != recorded:
        errors.append(f"recorded contract hash {recorded} != recomputed {recomputed}; the packet was edited")
    inputs = packet.get("selection_inputs") or {}
    try:
        fresh = prepare(
            repo_root, spec_path, index_path,
            packet.get("target"), packet.get("register"), packet.get("frame"),
            packet.get("subject"), packet.get("repo_ref"),
            tags=inputs.get("tags"), keys=inputs.get("keys"), limit=inputs.get("limit"),
            approved=approved,
        )
    except PreflightError as exc:
        errors.append(f"{exc.headline}")
        errors.extend(exc.errors)
        return errors
    if fresh["generation_contract_sha256"] != recorded:
        errors.append(
            f"repository now renders contract {fresh['generation_contract_sha256']} for these "
            f"inputs, packet recorded {recorded}; the spec, index, references or prompt changed"
        )
    for field, closed in RUNTIME_STATE_UNVERIFIED.items():
        if field not in (packet.get("runtime_state") or {}):
            errors.append(f"packet runtime_state lacks {field!r}")
    return errors


# --------------------------------------------------------------------------
# human-readable rendering
# --------------------------------------------------------------------------


def render_human(packet: dict) -> str:
    title = f"GENERATION PREFLIGHT - {packet['target']}"
    if packet.get("register"):
        title += f" / {packet['register']}"
    if packet.get("frame"):
        title += f" / {packet['frame']}"
    out = [title, "=" * len(title), ""]
    out.append(f"Repo ref       : {packet['repo_ref']}  (operator-supplied; not proven pushed)")
    out.append(f"Spec           : {packet['spec']['path']}")
    out.append(f"                 sha256 {packet['spec']['sha256']}")
    out.append(f"Reference index: {packet['style_refs_index']['path']}")
    out.append(f"                 sha256 {packet['style_refs_index']['sha256']}")
    prov = packet["reference_pack"]["provenance"]
    out.append(
        f"Reference pack : VERIFIED - {packet['reference_pack']['references_in_pack']} references, "
        f"provenance {prov.get('manifest')} -> {prov.get('result')}, "
        f"{prov.get('reads')} reads, {prov.get('mutations')} mutations"
    )
    out.append("")
    out.append("SUBJECT - exactly as supplied")
    out.append("")
    out.append(f"  {packet['subject']}")
    out.append("")

    out.append("SELECTED REFERENCES - deterministic order; hydrate and LOOK at each individual image")
    out.append("")
    for position, ref in enumerate(packet["references"], 1):
        bits = [ref.get("priority") or ""]
        if ref.get("register"):
            bits.append(ref["register"])
        out.append(f"  {position}. {ref['key']}  -  {ref['name']}  [{' / '.join(b for b in bits if b)}]")
        out.append(f"     path   : {ref['path']}")
        out.append(f"     sha256 : {ref['sha256']}")
        out.append(f"     raw    : {ref['raw_url']}")
        out.append(f"     size   : {ref['width']}x{ref['height']} {ref['format']}, {ref['bytes']} bytes")
        out.append(f"     use    : {ref['use_for']}")
        if ref.get("do_not_use_for"):
            out.append(f"     LIMIT  : {ref['do_not_use_for']}")
        out.append("")

    prompt = packet["prompt"]
    out.append("CANONICAL GENERATION CONTRACT - shotlist.render_prompt over spec.prompt_scaffolds; nothing paraphrased")
    out.append("")
    out.append(f"  positive : {prompt.get('positive')}")
    if prompt.get("subject_line"):
        out.append(f"  subject  : {prompt['subject_line']}")
    out.append(f"  negative : {prompt.get('negative')}")
    if prompt.get("costume_grammar"):
        out.append(f"  costume  : {prompt['costume_grammar']}")
    if prompt.get("hard_negatives"):
        out.append(f"  hard neg : {prompt['hard_negatives']}")
    for extra in ("reserve_note", "design_note", "length_rule"):
        if prompt.get(extra):
            out.append(f"  {extra:<9}: {prompt[extra]}")
    out.append("")
    out.append(f"  contract sha256 : {packet['generation_contract_sha256']}")
    out.append(f"  canonical json  : {packet['canonical_json']}")
    out.append("")

    out.append("RUNTIME STATE - initialised UNVERIFIED; this helper cannot flip these")
    out.append("")
    for field, value in packet["runtime_state"].items():
        out.append(f"  {field:<34}: {value}")
    out.append("")
    out.append("  Reference modes a session may declare, once it has actually done the work:")
    for mode, meaning in packet["reference_modes"].items():
        out.append(f"    {mode:<19} {meaning}")
    out.append("")
    for line in _wrap(packet["runtime_note"], 78):
        out.append(f"  {line}")
    out.append("")

    review = packet.get("direction_review_required")
    if review is not None:
        out.append("DIRECTION REVIEW REQUIRED - user-owned; surfaced from the roadmap, not settled here")
        out.append("")
        out.append(f"  source: {review['source']} / {review['task']}")
        for item in review["open_decisions"]:
            out.append(f"  - {item}")
        if not review["open_decisions"]:
            out.append("  (the task carries no open decisions)")
        out.append("")
    gates = packet.get("session_gates")
    if gates is not None:
        out.append("SESSION GATES - from the roadmap task; proven only by this session")
        out.append("")
        for gate in gates:
            out.append(f"  [ ] {gate.get('id')}  before {gate.get('before')}  (on fail: {gate.get('on_fail')})")
            for line in _wrap(str(gate.get("requirement", "")), 70):
                out.append(f"      {line}")
        if not gates:
            out.append("  (none declared)")
        out.append("")

    out.append("Nothing above authorises a generation. generation_allowed stays False until the")
    out.append("session has proven every runtime field and every session gate for itself.")
    return "\n".join(out) + "\n"


def _wrap(text: str, width: int) -> list[str]:
    import textwrap

    return textwrap.wrap(text, width=width) or [""]


# --------------------------------------------------------------------------
# selftest
# --------------------------------------------------------------------------

ROAD_BANDIT_SUBJECT = (
    "generic Road Bandit; lone adult male roadside shinobi ambusher; anonymous and unbranded"
)
ROAD_BANDIT_EXPECTED_KEYS = ["commander_okabe", "winter_crow", "pale_fang", "old_ghost"]
# The plan-freeze base of this tool. Any exact 40-hex id pins the URLs; the
# fixture only needs one that is real and stable.
ROAD_BANDIT_FIXTURE_REF = "c5f8faaf2ddafe687b0dfb764ad5974e05823f86"


def _fixture_spec() -> dict:
    """A minimal spec carrying just what render_prompt and the checks read."""
    return {
        "targets": {
            "SCENE_CHARACTER": {"aspect": {"accepted": ["2:3", "1:1"]}, "format": "webp"},
            "SCENE_BACKGROUND": {"aspect": {"value": "3:2"}, "format": "webp"},
            "AI_AVATAR": {"aspect": {"value": "1:1"}, "format": "webp"},
        },
        "house_style": {
            "clauses": {
                "rendering": "crisp pixel lineart, flat cel shading",
                "lighting": "soft even lighting",
                "silhouette": "arms within the silhouette",
            },
            "struck_clauses": {"_note": "x", "smooth painterly shading": "wrong"},
            "costume_grammar": "dark layered wrap robe",
            "hard_negatives": "no headband, no clan symbol",
        },
        "prompt_scaffolds": {
            "style_token": "[STYLE]",
            "subject_token": "[SUBJECT]",
            "style_clause_order": ["rendering", "lighting", "silhouette"],
            "scaffolds": {
                "SCENE_CHARACTER": {
                    "positive_by_frame": {
                        "full": "single character, full body, [STYLE], on lime",
                        "bust": "single character, bust, [STYLE], on lime",
                    },
                    "default_frame": "full",
                    "subject_label": "SUBJECT: [SUBJECT]",
                    "negative": "no text, no props",
                    "carries_costume_grammar": True,
                },
                "SCENE_BACKGROUND": {
                    "positive": "wide scene, [SUBJECT], [STYLE], no characters",
                    "negative": "no people",
                    "reserve_note": "lower left open",
                    "carries_costume_grammar": False,
                },
                "AI_AVATAR": {
                    "positive": "single ninja, [STYLE]",
                    "subject_label": "SUBJECT: [SUBJECT]",
                    "negative": "no text",
                    "carries_costume_grammar": True,
                },
            },
            "style_clause_scope": {
                "by_target": {
                    "SCENE_CHARACTER": ["rendering", "lighting", "silhouette"],
                    "SCENE_BACKGROUND": ["rendering", "lighting"],
                    "AI_AVATAR": ["rendering"],
                }
            },
        },
    }


def selftest() -> int:
    import copy
    import tempfile

    failures: list[str] = []

    def want(condition: bool, label: str) -> None:
        print(("  ok   " if condition else "  FAIL ") + label)
        if not condition:
            failures.append(label)

    def fails_with(fn, needle: str) -> bool:
        try:
            fn()
        except PreflightError as exc:
            return any(needle in e for e in exc.errors) or needle in exc.headline
        return False

    with tempfile.TemporaryDirectory() as raw_tmp:
        tmp = Path(raw_tmp)
        index, repo = style_refs._fixture(tmp)
        spec = _fixture_spec()
        spec_path = repo / "spec.json"
        spec_path.write_text(json.dumps(spec), encoding="utf-8")
        index_path = repo / "style_refs.json"
        index_path.write_text(json.dumps(index), encoding="utf-8")
        ref = "a" * 40

        def go(target="SCENE_CHARACTER", register="NINJA", frame="full",
               subject="fixture subject", repo_ref=ref, index_obj=None, spec_obj=None,
               workstream=None, task=None, **kw):
            if index_obj is not None:
                index_path.write_text(json.dumps(index_obj), encoding="utf-8")
            if spec_obj is not None:
                spec_path.write_text(json.dumps(spec_obj), encoding="utf-8")
            try:
                return prepare(repo, spec_path, index_path, target, register, frame, subject,
                               repo_ref, workstream=workstream, task_id=task,
                               approved=style_refs.FIXTURE_APPROVED, **kw)
            finally:
                if index_obj is not None:
                    index_path.write_text(json.dumps(index), encoding="utf-8")
                if spec_obj is not None:
                    spec_path.write_text(json.dumps(spec), encoding="utf-8")

        print("a clean packet")
        packet = go()
        want(packet["schema"] == SCHEMA and packet["version"] == VERSION, "packet carries schema/version")
        want(packet["selected_keys"] == ["anchor", "second"], "selection order is style_refs order")
        want(packet["prompt"] == shotlist.render_prompt(spec, "SCENE_CHARACTER", "fixture subject", "full"),
             "prompt object equals shotlist.render_prompt field for field")
        want("[STYLE]" not in packet["prompt"]["positive"] and "[SUBJECT]" not in packet["prompt"]["positive"],
             "no token survives in the rendered prompt")
        want(packet["prompt"]["costume_grammar"] == "dark layered wrap robe",
             "costume grammar rides the packet when the scaffold carries it")
        want(packet["subject"] == "fixture subject", "subject text is echoed exactly")
        want(packet["target"] == "SCENE_CHARACTER" and packet["register"] == "NINJA" and packet["frame"] == "full",
             "target/register/frame are echoed")
        want(packet["spec"]["sha256"] == sha256_bytes(spec_path.read_bytes()), "spec hash is over the spec bytes")
        want(packet["style_refs_index"]["sha256"] == sha256_bytes(index_path.read_bytes()),
             "index hash is over the index bytes")
        for entry in packet["references"]:
            want(entry["sha256"] == sha256_bytes((repo / entry["path"]).read_bytes()),
                 f"{entry['key']}: packet hash equals the file bytes")
            want(entry["raw_url"].endswith(f"{ref}/{entry['path']}") and "/main/" not in entry["raw_url"],
                 f"{entry['key']}: raw URL is pinned to the exact ref, not main")
        want(packet["runtime_state"] == RUNTIME_STATE_UNVERIFIED, "runtime state initialises fail-closed")
        want(packet["runtime_state"]["generation_allowed"] is False, "generation_allowed is False")
        want(packet["runtime_state"]["reference_mode"] == "UNDECLARED", "reference mode is UNDECLARED")
        want(set(packet["reference_modes"]) == {"ATTACHED", "ASSISTANT_GROUNDED", "NOT_HYDRATED"},
             "the three reference modes are named")
        want("cannot" in packet["runtime_note"] and "ChatGPT" in packet["runtime_note"],
             "the packet says it cannot see conversation/image-tool state")
        want(packet["generation_contract_sha256"] == sha256_bytes(canonical_bytes(packet["generation_contract"])),
             "contract hash is the SHA-256 of the canonical contract JSON")
        want(packet["generation_contract"]["prompt"] == packet["prompt"],
             "the hashed contract carries the exact prompt object")

        print("\ndeterminism")
        again = go()
        want(again == packet, "two builds produce an identical packet")
        want(again["generation_contract_sha256"] == packet["generation_contract_sha256"],
             "contract hash is deterministic")
        want(json.loads(json.dumps(packet, ensure_ascii=False)) == packet, "packet round-trips through JSON")
        want(render_human(packet) == render_human(again), "human rendering is deterministic")
        text = render_human(packet)
        want("generation_allowed" in text and "False" in text, "human output shows generation_allowed False")
        want("GENERATION READY" not in text.upper() and "READY TO GENERATE" not in text.upper(),
             "human output never declares generation ready")
        want(packet["references"][0]["raw_url"] in text, "human output carries the pinned raw URL")
        other = go(subject="a different subject")
        want(other["generation_contract_sha256"] != packet["generation_contract_sha256"],
             "a different subject changes the contract hash")
        bust = go(frame="bust")
        want(bust["generation_contract_sha256"] != packet["generation_contract_sha256"]
             and bust["prompt"]["positive"] != packet["prompt"]["positive"],
             "a different frame renders a different contract")

        print("\nfail closed - reference pack")
        broken = copy.deepcopy(index)
        broken["references"][0]["sha256"] = "0" * 64
        want(fails_with(lambda: go(index_obj=broken), "sha256 mismatch"), "a hash mismatch refuses the packet")
        target_file = repo / index["references"][0]["path"]
        original = target_file.read_bytes()
        target_file.write_bytes(original + b"\x00")
        want(fails_with(go, "sha256 mismatch") or fails_with(go, "byte count mismatch"),
             "tampered reference bytes refuse the packet")
        target_file.write_bytes(original)
        target_file.unlink()
        want(fails_with(go, "is missing"), "a missing reference file refuses the packet")
        target_file.write_bytes(original)
        banned = copy.deepcopy(index)
        banned["references"][0]["name"] = "Nameless Ninja"
        want(fails_with(lambda: go(index_obj=banned), "excluded"), "an excluded/deprecated reference refuses the packet")
        moved = copy.deepcopy(index)
        moved["source_capture"]["manifest"] = "push/99_other.json"
        want(fails_with(lambda: go(index_obj=moved), "approved v1 capture"),
             "a provenance failure refuses the packet before selection")

        print("\nfail closed - inputs")
        want(fails_with(lambda: go(target="ICON"), "not in the art spec"), "an unknown target is refused")
        want(fails_with(lambda: go(target="AI_AVATAR", register=None, frame=None), "carries no references"),
             "a target the v1 pack does not cover is refused explicitly")
        want(fails_with(lambda: go(register="SAMURAI"), "needs --register"), "an unknown register is refused")
        want(fails_with(lambda: go(register=None), "needs --register"), "a missing scene-character register is refused")
        want(fails_with(lambda: go(target="SCENE_BACKGROUND", register="NINJA", frame=None), "only meaningful"),
             "a register on a background is refused")
        want(fails_with(lambda: go(frame="wide"), "pass --frame"), "an unknown frame is refused")
        want(fails_with(lambda: go(frame=None), "pass --frame"), "a missing frame on a framed target is refused")
        want(fails_with(lambda: go(target="SCENE_BACKGROUND", register=None, frame="full"), "no framed scaffold"),
             "a frame on an unframed target is refused")
        want(fails_with(lambda: go(subject="   "), "--subject is required"), "a blank subject is refused")
        for label, bad_ref in (("branch name", "main"), ("short", "abc123"), ("uppercase", "A" * 40)):
            want(fails_with(lambda: go(repo_ref=bad_ref), "repo ref must"), f"a floating/malformed repo ref is refused ({label})")
        want(fails_with(lambda: go(register="CIVILIAN"), "no references selected"),
             "an empty selection refuses rather than substituting")
        bg = go(target="SCENE_BACKGROUND", register=None, frame=None)
        want(bg["selected_keys"] == ["yard"] and bg["prompt"].get("reserve_note") == "lower left open",
             "a background packet selects backgrounds and carries the reserve note")

        print("\nfail closed - prompt")
        regressed = copy.deepcopy(spec)
        regressed["prompt_scaffolds"]["scaffolds"]["SCENE_CHARACTER"]["positive_by_frame"]["full"] += ", smooth painterly shading"
        want(fails_with(lambda: go(spec_obj=regressed), "struck clause"), "a struck clause in the scaffold is refused")
        lost = copy.deepcopy(spec)
        del lost["prompt_scaffolds"]["scaffolds"]["SCENE_CHARACTER"]
        want(fails_with(lambda: go(spec_obj=lost), "no prompt scaffold"), "a spec without the scaffold is refused")

        print("\nworkstream direction review")
        ws = repo / WORKSTREAMS_DIR / "fixture"
        ws.mkdir(parents=True)
        (ws / "roadmap.json").write_text(json.dumps({
            "tasks": [{
                "id": "art.scene_characters",
                "open_decisions": ["Final visual direction is the user's."],
                "session_gates": [{"id": "g1", "before": "image_generation",
                                   "requirement": "look", "on_fail": "STOP"}],
            }]
        }), encoding="utf-8")
        with_ws = go(workstream="fixture", task="art.scene_characters")
        want(with_ws["direction_review_required"]["open_decisions"] == ["Final visual direction is the user's."],
             "open decisions are surfaced as direction_review_required")
        want(with_ws["session_gates"][0]["id"] == "g1", "session gates are echoed from the roadmap task")
        want(with_ws["generation_contract_sha256"] == packet["generation_contract_sha256"],
             "the roadmap context does not change the generation contract hash")
        want("DIRECTION REVIEW REQUIRED" in render_human(with_ws) and "[ ] g1" in render_human(with_ws),
             "human output shows the review and the gates")
        want(fails_with(lambda: go(workstream="fixture", task="nope"), "carries no task"),
             "an unknown workstream task is refused")
        want(fails_with(lambda: go(workstream="fixture"), "given together"),
             "--workstream without --task is refused")

        print("\ncheck")
        want(check_packet(packet, repo, spec_path, index_path, approved=style_refs.FIXTURE_APPROVED) == [],
             "a freshly rendered packet checks clean against the repository")
        edited = copy.deepcopy(packet)
        edited["generation_contract"]["subject"] = "someone edited this"
        errs = check_packet(edited, repo, spec_path, index_path, approved=style_refs.FIXTURE_APPROVED)
        want(any("was edited" in e for e in errs), "an edited contract is caught by the recorded hash")
        want(check_packet(other, repo, spec_path, index_path, approved=style_refs.FIXTURE_APPROVED) == [],
             "a packet prepared for different inputs checks clean for those inputs")
        half = copy.deepcopy(packet)
        half["generation_contract"]["subject"] = "a different subject"
        half["generation_contract_sha256"] = sha256_bytes(canonical_bytes(half["generation_contract"]))
        errs = check_packet(half, repo, spec_path, index_path, approved=style_refs.FIXTURE_APPROVED)
        want(any("repository now renders" in e for e in errs),
             "a re-hashed contract whose prompt no longer matches its inputs is caught by rebuilding")
        spec_path.write_text(json.dumps(regressed), encoding="utf-8")
        errs = check_packet(packet, repo, spec_path, index_path, approved=style_refs.FIXTURE_APPROVED)
        spec_path.write_text(json.dumps(spec), encoding="utf-8")
        want(errs != [], "a spec change after staging is caught by check")

    print("\nroad bandit fixture against the real repository")
    repo_root = style_refs.default_repo_root()
    real_spec = default_spec_path()
    real_index = style_refs.default_index_path()
    if (repo_root / "art" / "style_refs").is_dir() and real_spec.exists() and real_index.exists() \
            and (repo_root / style_refs.HARVEST_INBOX).is_dir():
        try:
            rb = prepare(repo_root, real_spec, real_index, "SCENE_CHARACTER", "NINJA", "full",
                         ROAD_BANDIT_SUBJECT, ROAD_BANDIT_FIXTURE_REF)
        except PreflightError as exc:
            rb = None
            print(f"  FAIL {exc.headline}")
            for err in exc.errors:
                print(f"       - {err}")
            failures.append("road bandit prepare renders against the real repository")
        if rb is not None:
            want(rb["selected_keys"] == ROAD_BANDIT_EXPECTED_KEYS,
                 f"NINJA selection is exactly {', '.join(ROAD_BANDIT_EXPECTED_KEYS)} in that order")
            live_spec = json.loads(real_spec.read_text(encoding="utf-8"))
            want(rb["prompt"] == shotlist.render_prompt(live_spec, "SCENE_CHARACTER", ROAD_BANDIT_SUBJECT, "full"),
                 "Road Bandit prompt equals shotlist.render_prompt field for field")
            rb2 = prepare(repo_root, real_spec, real_index, "SCENE_CHARACTER", "NINJA", "full",
                          ROAD_BANDIT_SUBJECT, ROAD_BANDIT_FIXTURE_REF)
            want(rb2["generation_contract_sha256"] == rb["generation_contract_sha256"],
                 "Road Bandit contract hash is deterministic")
            want(all(r["name"].strip().lower() != "nameless ninja" for r in rb["references"]),
                 "no deprecated reference is admitted")
            want(rb["runtime_state"]["generation_allowed"] is False, "Road Bandit packet does not allow generation")
            print(f"       contract sha256 {rb['generation_contract_sha256']}")
    else:
        print("  SKIP no repository checkout with art/style_refs, the spec, the index and harvests/inbox;"
              " the Road Bandit fixture needs one")

    print()
    if failures:
        print(f"{len(failures)} FAILED")
        for label in failures:
            print(f"  - {label}")
        return 1
    print("generation_preflight selftest: all checks passed")
    return 0


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--selftest", action="store_true", help="run socket-free unit tests and exit")
    sub = parser.add_subparsers(dest="command")

    p_prep = sub.add_parser("prepare", help="render the deterministic generation preflight packet")
    p_prep.add_argument("--repo-root", type=Path, default=None)
    p_prep.add_argument("--spec", type=Path, default=None, help="path to 25x_DATA_art_spec.json")
    p_prep.add_argument("--index", type=Path, default=None, help="path to style_refs.json")
    p_prep.add_argument("--target", required=True, choices=sorted(style_refs.TARGETS))
    p_prep.add_argument("--register", choices=style_refs.REGISTERS, default=None)
    p_prep.add_argument("--frame", default=None, help="framing for framed targets (e.g. full, bust)")
    p_prep.add_argument("--subject", required=True, help="the [SUBJECT] text, used exactly as supplied")
    p_prep.add_argument("--repo-ref", required=True, help="exact 40-hex commit id to pin raw URLs to")
    p_prep.add_argument("--tag", action="append", default=[])
    p_prep.add_argument("--key", action="append", default=[])
    p_prep.add_argument("--limit", type=int, default=None)
    p_prep.add_argument("--workstream", default=None, help="workstream slug whose task surfaces open decisions")
    p_prep.add_argument("--task", default=None, help="task id within --workstream")
    p_prep.add_argument("--json", action="store_true", help="print the packet as JSON instead of text")
    p_prep.add_argument("--out", type=Path, default=None, help="also write the JSON packet here")

    p_check = sub.add_parser("check", help="re-derive a staged packet's contract from the repository")
    p_check.add_argument("packet", type=Path)
    p_check.add_argument("--repo-root", type=Path, default=None)
    p_check.add_argument("--spec", type=Path, default=None)
    p_check.add_argument("--index", type=Path, default=None)

    args = parser.parse_args(argv)
    if args.selftest:
        return selftest()
    if not args.command:
        parser.print_help()
        return 2

    repo_root = (args.repo_root or style_refs.default_repo_root()).resolve()
    spec_path = args.spec or default_spec_path()
    index_path = args.index or style_refs.default_index_path()

    if args.command == "prepare":
        try:
            packet = prepare(
                repo_root, spec_path, index_path,
                args.target, args.register, args.frame, args.subject, args.repo_ref,
                tags=args.tag, keys=args.key, limit=args.limit,
                workstream=args.workstream, task_id=args.task,
            )
        except PreflightError as exc:
            print(f"generation_preflight: PREFLIGHT FAILED - {exc.headline}", file=sys.stderr)
            for err in exc.errors:
                print(f"  - {err}", file=sys.stderr)
            print("generation is not allowed; nothing was staged", file=sys.stderr)
            return 1
        if args.out:
            args.out.write_text(json.dumps(packet, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        if args.json:
            print(json.dumps(packet, indent=2, ensure_ascii=False))
        else:
            print(render_human(packet), end="")
            if args.out:
                print(f"written  {args.out}")
        return 0

    if args.command == "check":
        try:
            packet = load_json(args.packet, "packet")
            errors = check_packet(packet, repo_root, spec_path, index_path)
        except PreflightError as exc:
            errors = [exc.headline] + exc.errors
        if errors:
            print(f"generation_preflight check: {len(errors)} error(s)", file=sys.stderr)
            for err in errors:
                print(f"  - {err}", file=sys.stderr)
            return 1
        print(f"generation_preflight check: OK - contract {packet['generation_contract_sha256']} "
              "matches the repository. Runtime state is not checkable here.")
        return 0

    parser.print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
