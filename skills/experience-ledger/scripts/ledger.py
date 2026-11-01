"""Explicit local-only immutable experience records. Python 3.10+; no network."""
from __future__ import annotations

import argparse
from contextlib import contextmanager
from datetime import datetime
import json
import os
from pathlib import Path
import re
import stat
import sys
import tempfile

MAX_BYTES = 64 * 1024
MAX_RECORDS = 1000
ID = re.compile(r"[a-z0-9][a-z0-9-]{0,63}\Z")
MARKER = ".experience-ledger.json"
MARKER_BYTES = b'{"format":"experience-ledger","version":1}\n'
FIELDS = {"schema_version", "id", "kind", "status", "recorded_at", "author",
          "context", "claim", "applies_when", "sources", "verification",
          "counterexamples", "supersedes", "provenance"}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def text(value, label, limit=4000):
    require(isinstance(value, str) and bool(value.strip()) and len(value) <= limit,
            f"Invalid {label}")


def identifier(value):
    require(isinstance(value, str) and ID.fullmatch(value), "Invalid record ID")
    return value


def timestamp(value, label):
    require(isinstance(value, str), f"Invalid {label}")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        raise ValueError(f"Invalid {label}") from None
    require(parsed.tzinfo is not None and parsed.utcoffset() is not None,
            f"Timezone required for {label}")


def validate(record):
    require(isinstance(record, dict) and set(record) == FIELDS, "Unexpected or missing fields")
    require(type(record["schema_version"]) is int and record["schema_version"] == 1,
            "Unsupported schema version")
    identifier(record["id"])
    require(record["kind"] in ("hypothesis", "observation", "lesson"), "Invalid kind")
    require(record["status"] in ("provisional", "supported", "disputed", "retired"), "Invalid status")
    timestamp(record["recorded_at"], "recorded_at")
    for key in ("author", "context", "claim", "applies_when", "provenance"):
        text(record[key], key)
    sources = record["sources"]
    require(isinstance(sources, list) and 1 <= len(sources) <= 20, "Invalid sources")
    for source in sources:
        require(isinstance(source, dict) and set(source) == {"label", "locator"}, "Invalid source fields")
        for key in ("label", "locator"):
            text(source[key], "source " + key, 1000)
    verification = record["verification"]
    require(record["status"] != "supported" or verification is not None,
            "Supported status requires recorded verification")
    if verification is not None:
        require(isinstance(verification, dict) and set(verification) ==
                {"method", "result", "reviewer", "checked_at"}, "Invalid verification fields")
        for key in ("method", "result", "reviewer"):
            text(verification[key], "verification " + key)
        timestamp(verification["checked_at"], "checked_at")
    for key in ("counterexamples", "supersedes"):
        require(isinstance(record[key], list) and len(record[key]) <= 20, "Invalid " + key)
    for value in record["counterexamples"]:
        text(value, "counterexample")
    for value in record["supersedes"]:
        identifier(value)
        require(value != record["id"], "A record cannot supersede itself")
    require(len(set(record["supersedes"])) == len(record["supersedes"]), "Duplicate supersedes ID")
    return record


def safe_path(path):
    path = Path(path).expanduser()
    require(not str(path).startswith(("//", "\\\\")), "UNC or network path refused")
    require(path.is_absolute(), "Choose an absolute local path")
    require(".." not in path.parts, "Parent traversal refused")
    for component in (path, *path.parents):
        require(not component.is_symlink(), "Symlink path refused")
        try:
            attributes = getattr(component.lstat(), "st_file_attributes", 0)
        except FileNotFoundError:
            continue
        # Python 3.10/3.11 lack Path.is_junction(); Windows exposes reparse
        # attributes via lstat. Refuse all reparse points, not just junctions.
        require(not attributes & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400),
                "Windows reparse-point path refused")
    return path.resolve()


def root_path(path, existing=True):
    root = safe_path(path)
    for component in (root, *root.parents):
        require(not (component / ".git").exists(), "Choose a private directory outside repositories")
    # Also refuse this distributed skill directory even if copied without .git.
    skill = Path(__file__).resolve().parents[1]
    require(root != skill and skill not in root.parents, "Ledger cannot live inside the skill")
    if existing:
        require(root.is_dir(), "Ledger directory missing; explicitly initialize it")
        marker = safe_path(root / MARKER)
        require(marker.is_file(), "Ledger marker missing")
        with marker.open("rb") as stream:
            require(stream.read(len(MARKER_BYTES) + 1) == MARKER_BYTES, "Ledger marker mismatch")
    return root


def load_record(path):
    path = safe_path(path)
    with path.open("rb") as stream:
        raw = stream.read(MAX_BYTES + 1)
    require(len(raw) <= MAX_BYTES, "Record exceeds 64 KiB")
    return validate(json.loads(raw))


def publish_exclusive(path, payload):
    """Publish complete bytes atomically without replacing an existing name."""
    require(len(payload) <= MAX_BYTES, "Record exceeds 64 KiB")
    descriptor, temporary = tempfile.mkstemp(prefix=".ledger-pending-", dir=path.parent)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        # Atomic exclusive name creation on hard-link-capable local filesystems.
        os.link(temporary, path)
    finally:
        Path(temporary).unlink(missing_ok=True)


def record_paths(root):
    paths = []
    for item in root.iterdir():
        if item.name.endswith(".json") and item.name != MARKER:
            require(ID.fullmatch(item.stem), "Unexpected JSON file in ledger")
            paths.append(safe_path(item))
            require(len(paths) <= MAX_RECORDS, "Ledger exceeds 1,000 records")
    return sorted(paths)


@contextmanager
def write_lock(root):
    """Refuse simultaneous writers; never take over an existing lock."""
    lock = root / ".ledger-write.lock"
    descriptor = os.open(lock, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        os.close(descriptor)
        yield
    finally:
        lock.unlink()


def initialize(path):
    root = root_path(path, existing=False)
    require(root.parent.is_dir(), "Choose an existing parent directory")
    if root.exists():
        require(root.is_dir() and not any(root.iterdir()), "Initialization requires a new or empty directory")
    else:
        root.mkdir()
    publish_exclusive(root / MARKER, MARKER_BYTES)
    return {"initialized": True, "format": "experience-ledger", "network_api_calls": 0}


def put(path, input_path):
    root = root_path(path)
    record = load_record(input_path)
    payload = (json.dumps(record, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    with write_lock(root):
        require(len(record_paths(root)) < MAX_RECORDS, "Ledger is full")
        for prior in record["supersedes"]:
            previous = load_record(root / (prior + ".json"))
            require(previous["id"] == prior, "Prior record filename/ID mismatch")
        destination = root / (record["id"] + ".json")
        publish_exclusive(destination, payload)
    return {"created": record["id"], "kind": record["kind"], "status": record["status"],
            "truth_verified_by_helper": False, "network_api_calls": 0}


def listing(path):
    root = root_path(path)
    records = []
    for item in record_paths(root):
        record = load_record(item)
        require(record["id"] == item.stem, "Record filename/ID mismatch")
        records.append({key: record[key] for key in ("id", "kind", "status", "recorded_at", "supersedes")})
    return {"records": records, "network_api_calls": 0}


def show(path, record_id):
    root = root_path(path)
    record_id = identifier(record_id)
    record = load_record(root / (record_id + ".json"))
    require(record["id"] == record_id, "Record filename/ID mismatch")
    return record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("init", "put", "list", "show"):
        sub = commands.add_parser(name)
        sub.add_argument("--root", required=True)
        if name == "put":
            sub.add_argument("--input", required=True)
        if name == "show":
            sub.add_argument("--id", required=True)
    args = parser.parse_args()
    try:
        if args.command == "init":
            result = initialize(args.root)
        elif args.command == "put":
            result = put(args.root, args.input)
        elif args.command == "list":
            result = listing(args.root)
        else:
            result = show(args.root, args.id)
        print(json.dumps(result, ensure_ascii=False))
    except (ValueError, OSError, UnicodeError) as error:
        # No supplied record text, source locator or file path is printed on failure.
        if isinstance(error, UnicodeError):
            reason = "Invalid text encoding"
        elif isinstance(error, json.JSONDecodeError):
            reason = "Invalid JSON record"
        elif isinstance(error, ValueError):
            reason = str(error)
        else:
            reason = "Local file operation refused or unavailable"
        print(json.dumps({"error": type(error).__name__, "reason": reason,
                          "operation_failed": True}), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
