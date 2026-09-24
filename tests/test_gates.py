#!/usr/bin/env python3
"""Tests for the security/privacy/data-integrity CI gate.

Stdlib unittest only. Run with:
    python3 -m unittest discover tests
"""
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SANITIZE = REPO_ROOT / "scripts" / "sanitize.py"
VALIDATE = REPO_ROOT / "scripts" / "validate_data.py"


def run(args, env=None):
    full_env = dict(os.environ)
    # Never let a developer's private identifier file leak into a test's
    # expectations: tests opt in explicitly via `env`.
    full_env["PRIVATE_IDENTIFIERS_FILE"] = os.devnull
    full_env.pop("PRIVATE_IDENTIFIERS_JSON", None)
    full_env.update(env or {})
    return subprocess.run(
        [sys.executable, *args], cwd=REPO_ROOT, capture_output=True, text=True, env=full_env
    )


def write_leaky_sample(directory: Path) -> Path:
    """Synthesise a deliberately leaky file at test time.

    Every leaky token is assembled from fragments, so no leak-shaped literal
    exists in this repo's source or history (nothing to allowlist, exclude
    or rewrite). All values are fake.
    """
    bs = "\\"
    fake_uuid = "-".join(["11111111", "2222", "4333", "8444", "555555555555"])
    lines = [
        "scratch_path = r'C:" + bs + "Users" + bs + "JaneDoe" + bs + "notes.txt'",
        "brain_db = r'C:" + bs + "Users" + bs + "JaneDoe" + bs + ".gemini" + bs
        + "antigravity" + bs + "brain" + bs + fake_uuid + bs + "cache.db'",
        "contact = '" + "jane.doe" + "@" + "example.org" + "'",
    ]
    path = directory / "leaky_sample.py"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


class SanitizeGateTests(unittest.TestCase):
    def test_check_fails_on_leaky_sample(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = run([str(SANITIZE), "--check", str(write_leaky_sample(Path(tmp)))])
        self.assertEqual(result.returncode, 1, msg=result.stdout + result.stderr)
        self.assertIn("agy-brain-path", result.stdout)
        self.assertIn("windows-user-path", result.stdout)
        self.assertIn("personal-email", result.stdout)

    def test_check_passes_on_clean_tree(self):
        # The real tracked tree, excluding the deliberately-leaky fixtures
        # (which are excluded from the repo-wide scan by default) and
        # README.md (owned by the repo maintainer, out of scope for this
        # gate's automated rewriting but not expected to contain findings).
        result = run([str(SANITIZE), "--check"])
        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)

    def test_repo_has_no_leak_fixtures(self):
        # Leaky material is synthesised at test time; none is committed.
        self.assertFalse((REPO_ROOT / "tests" / "fixtures").exists())


TEST_UUID = "22222222-3333-4444-8555-666666666666"  # synthetic


class NoLiteralIdentifierTests(unittest.TestCase):
    """The rule source must not itself be a disclosure."""

    def test_sanitize_script_is_scanned_and_clean(self):
        # Explicit paths bypass the default excludes, so this proves the
        # script needs no self-exclusion.
        result = run([str(SANITIZE), "--check", "scripts/sanitize.py"])
        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)

    def test_private_source_drives_detection(self):
        with tempfile.TemporaryDirectory() as tmp:
            ids = Path(tmp) / "ids.json"
            ids.write_text(json.dumps({
                "usernames": ["ZZTestUser"],
                "gcp_projects": ["zz-test-project"],
                "session_uuids": [TEST_UUID],
            }))
            sample = Path(tmp) / "sample.txt"
            sample.write_text(
                "user ZZTestUser project zz-test-project\n"
                f"id {TEST_UUID} short {TEST_UUID[:8]}\n"
            )
            env = {"PRIVATE_IDENTIFIERS_FILE": str(ids)}
            hit = run([str(SANITIZE), "--check", str(sample)], env)
            self.assertEqual(hit.returncode, 1, msg=hit.stdout + hit.stderr)
            for rule in ("username-token", "gcp-project-id", "agy-session-uuid"):
                self.assertIn(rule, hit.stdout)
            # Without the private source the same text is not flagged.
            miss = run([str(SANITIZE), "--check", str(sample)])
            self.assertEqual(miss.returncode, 0, msg=miss.stdout + miss.stderr)

    def test_emit_rules_refuses_repo_tree(self):
        result = run([str(SANITIZE), "--emit-filter-repo-rules", str(REPO_ROOT / "rules.txt")])
        self.assertEqual(result.returncode, 2)

    def test_emitted_rules_are_written_outside_repo_and_private(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "rules.txt"
            result = run([str(SANITIZE), "--emit-filter-repo-rules", str(out)])
            self.assertEqual(result.returncode, 0, msg=result.stderr)
            self.assertEqual(out.stat().st_mode & 0o077, 0)


class ValidateDataTests(unittest.TestCase):
    def test_validate_data_passes(self):
        result = run([str(VALIDATE)])
        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
        self.assertIn("Data integrity OK", result.stdout)


if __name__ == "__main__":
    unittest.main()
