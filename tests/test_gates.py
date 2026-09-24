#!/usr/bin/env python3
"""Tests for the security/privacy/data-integrity CI gate.

Stdlib unittest only. Run with:
    python3 -m unittest discover tests
"""
import subprocess
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SANITIZE = REPO_ROOT / "scripts" / "sanitize.py"
VALIDATE = REPO_ROOT / "scripts" / "validate_data.py"
FIXTURES = REPO_ROOT / "tests" / "fixtures" / "leaky"


def run(args):
    return subprocess.run(
        [sys.executable, *args], cwd=REPO_ROOT, capture_output=True, text=True
    )


class SanitizeGateTests(unittest.TestCase):
    def test_check_fails_on_leaky_fixtures(self):
        result = run([str(SANITIZE), "--check", str(FIXTURES)])
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

    def test_fixture_leaks_are_not_in_repo_wide_scan(self):
        # tests/fixtures/ must be excluded from the default repo-wide scan
        # so CI stays green even though the fixtures are intentionally dirty.
        result = run([str(SANITIZE), "--check"])
        self.assertNotIn("tests/fixtures", result.stdout)


class ValidateDataTests(unittest.TestCase):
    def test_validate_data_passes(self):
        result = run([str(VALIDATE)])
        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
        self.assertIn("Data integrity OK", result.stdout)


if __name__ == "__main__":
    unittest.main()
