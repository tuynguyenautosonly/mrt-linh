"""Synthetic, local-only behavioral tests; no private records or model calls."""
from concurrent.futures import ThreadPoolExecutor
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("ledger", Path(__file__).with_name("ledger.py"))
ledger = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ledger)


def sample(record_id="synthetic-01"):
    return {"schema_version": 1, "id": record_id, "kind": "hypothesis",
            "status": "provisional", "recorded_at": "2026-01-01T09:00:00+00:00",
            "author": "Synthetic author", "context": "Invented bench exercise",
            "claim": "One candidate explanation", "applies_when": "This exercise only",
            "sources": [{"label": "Invented source", "locator": "synthetic:exercise"}],
            "verification": None, "counterexamples": ["An alternative may fit"],
            "supersedes": [], "provenance": "Authored synthetic test"}


class LedgerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.base = Path(self.temp.name).resolve()
        self.root = self.base / "private-ledger"
        ledger.initialize(self.root)

    def tearDown(self):
        self.temp.cleanup()

    def input(self, record):
        path = self.base / (record["id"] + "-input.json")
        path.write_text(json.dumps(record), encoding="utf-8")
        return path

    def test_roundtrip_preserves_uncertainty_and_metadata_list(self):
        record = sample()
        result = ledger.put(self.root, self.input(record))
        self.assertFalse(result["truth_verified_by_helper"])
        self.assertEqual(ledger.show(self.root, record["id"]), record)
        metadata = ledger.listing(self.root)["records"][0]
        self.assertEqual(metadata["status"], "provisional")
        self.assertNotIn("claim", metadata)
        self.assertNotIn("sources", metadata)

    def test_duplicate_id_never_overwrites(self):
        record = sample()
        path = self.input(record)
        ledger.put(self.root, path)
        before = (self.root / "synthetic-01.json").read_bytes()
        record["claim"] = "Different content"
        with self.assertRaises(FileExistsError):
            ledger.put(self.root, self.input(record))
        self.assertEqual((self.root / "synthetic-01.json").read_bytes(), before)

    def test_revision_requires_existing_prior_and_keeps_history(self):
        prior = sample()
        revision = sample("synthetic-02")
        revision["supersedes"] = [prior["id"]]
        path = self.input(revision)
        with self.assertRaises(FileNotFoundError):
            ledger.put(self.root, path)
        ledger.put(self.root, self.input(prior))
        ledger.put(self.root, path)
        self.assertEqual(ledger.show(self.root, prior["id"]), prior)
        self.assertEqual(len(ledger.listing(self.root)["records"]), 2)

    def test_supported_requires_verification_not_invented_by_helper(self):
        record = sample()
        record["status"] = "supported"
        with self.assertRaises(ValueError):
            ledger.validate(record)
        record["verification"] = {"method": "Invented check description",
                                  "result": "Synthetic result", "reviewer": "Example reviewer",
                                  "checked_at": "2026-01-01T10:00:00+00:00"}
        self.assertEqual(ledger.validate(record)["status"], "supported")

    def test_bad_schema_timestamp_and_traversal_refused(self):
        for mutate in (lambda r: r.update(extra="not accepted"),
                       lambda r: r.update(recorded_at="2026-01-01T10:00:00"),
                       lambda r: r.update(id="../outside"),
                       lambda r: r.update(supersedes=["synthetic-01"])):
            record = sample()
            mutate(record)
            with self.assertRaises(ValueError):
                ledger.validate(record)
        with self.assertRaises(ValueError):
            ledger.show(self.root, "../outside")
        with self.assertRaises(ValueError):
            ledger.root_path(Path("relative-ledger"))

    def test_repo_and_distributed_skill_storage_refused(self):
        repository = self.base / "repository"
        repository.mkdir()
        (repository / ".git").write_text("gitdir: synthetic", encoding="utf-8")
        with self.assertRaises(ValueError):
            ledger.initialize(repository / "notes")
        with self.assertRaises(ValueError):
            ledger.root_path(Path(ledger.__file__).resolve().parents[1] / "private-notes", False)

    def test_oversized_input_refused(self):
        path = self.base / "large.json"
        path.write_bytes(b" " * (ledger.MAX_BYTES + 1))
        with self.assertRaises(ValueError):
            ledger.put(self.root, path)
        self.assertEqual(ledger.listing(self.root)["records"], [])

    def test_unsupported_atomic_publication_leaves_no_record_or_temp(self):
        path = self.input(sample())
        with patch.object(ledger.os, "link", side_effect=OSError("synthetic unsupported filesystem")):
            with self.assertRaises(OSError):
                ledger.put(self.root, path)
        self.assertEqual([p.name for p in self.root.iterdir()], [ledger.MARKER])

    def test_existing_lock_is_not_stolen(self):
        lock = self.root / ".ledger-write.lock"
        lock.write_text("synthetic other writer", encoding="utf-8")
        with self.assertRaises(FileExistsError):
            ledger.put(self.root, self.input(sample()))
        self.assertEqual(lock.read_text(encoding="utf-8"), "synthetic other writer")

    def test_concurrent_same_id_has_one_writer(self):
        path = self.input(sample())
        def write():
            try:
                ledger.put(self.root, path)
                return "created"
            except FileExistsError:
                return "refused"
        with ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(lambda _: write(), range(2)))
        self.assertEqual(sorted(results), ["created", "refused"])
        self.assertEqual(ledger.show(self.root, "synthetic-01"), sample())

    def test_capacity_bound_before_write(self):
        ledger.put(self.root, self.input(sample()))
        with patch.object(ledger, "MAX_RECORDS", 1):
            with self.assertRaises(ValueError):
                ledger.put(self.root, self.input(sample("synthetic-02")))
        self.assertFalse((self.root / "synthetic-02.json").exists())

    def test_symlink_record_refused(self):
        target = self.input(sample())
        link = self.root / "synthetic-01.json"
        try:
            link.symlink_to(target)
        except OSError as error:
            self.skipTest("Local symlink creation unavailable: " + type(error).__name__)
        with self.assertRaises(ValueError):
            ledger.show(self.root, "synthetic-01")

    def test_reparse_attribute_refused_without_is_junction(self):
        # Emulate 3.10/3.11: no useful is_junction API and is_symlink=False.
        # lstat file attributes must still detect a Windows junction/reparse path.
        attributes = SimpleNamespace(st_file_attributes=0x400)
        with patch.object(ledger.Path, "is_symlink", return_value=False), \
             patch.object(ledger.Path, "is_junction", None, create=True), \
             patch.object(ledger.Path, "lstat", return_value=attributes):
            with self.assertRaisesRegex(ValueError, "reparse-point"):
                ledger.safe_path(self.root)

    def test_cli_invalid_timestamps_do_not_echo_supplied_content(self):
        marker = "SYNTHETIC-PRIVATE-TIMESTAMP-MARKER"
        for field in ("recorded_at", "checked_at"):
            record = sample()
            if field == "recorded_at":
                record[field] = marker
            else:
                record["verification"] = {"method": "Synthetic check", "result": "Invented result",
                                          "reviewer": "Example reviewer", "checked_at": marker}
            path = self.input(record)
            result = subprocess.run([sys.executable, ledger.__file__, "put", "--root", str(self.root),
                                     "--input", str(path)], capture_output=True, text=True, check=False)
            self.assertEqual(result.returncode, 1)
            output = result.stdout + result.stderr
            self.assertNotIn(marker, output)
            self.assertIn("Invalid " + field, output)

    def test_cli_invalid_utf8_does_not_echo_bad_bytes(self):
        marker = "SYNTHETIC-PRIVATE-ENCODING-MARKER"
        path = self.base / "invalid-text.json"
        path.write_bytes(b'{"claim":"' + marker.encode("ascii") + b'\xff"}')
        result = subprocess.run([sys.executable, ledger.__file__, "put", "--root", str(self.root),
                                 "--input", str(path)], capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 1)
        output = result.stdout + result.stderr
        self.assertNotIn(marker, output)
        self.assertNotIn("0xff", output)
        self.assertIn("Invalid text encoding", output)


if __name__ == "__main__":
    unittest.main()
