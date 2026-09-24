#!/usr/bin/env python3
"""Single source of truth for the repo's private-identifier rules.

Scans (``--check``) or rewrites in place (``--fix``) every tracked text file
for local machine paths, usernames, Antigravity session ids, the GCP project
id, private Drive folder ids and personal email addresses, per
docs/security_ci_gate.md and issue #1.

Stdlib only. No dependencies.

Usage:
    python3 scripts/sanitize.py --check
    python3 scripts/sanitize.py --fix --exclude README.md
    python3 scripts/sanitize.py --check tests/fixtures/leaky
    git log -p --all | python3 scripts/sanitize.py --check --stdin
"""
from __future__ import annotations

import argparse
import fnmatch
import hashlib
import re
import subprocess
import sys
from pathlib import Path
from typing import Callable, List, Optional, Pattern

REPO_ROOT = Path(__file__).resolve().parents[1]

# --------------------------------------------------------------------------
# Allowlists and known identifiers
# --------------------------------------------------------------------------

# Antigravity/agy session UUIDs that get a stable pseudonym so the same
# session reads consistently across docs, even where no surrounding
# "agy/brain/session/conversation" keyword is present on the line.
KNOWN_SESSION_UUIDS = [
    "agy-session-2287",
    "agy-session-912e",
    "agy-session-addd",
    "agy-session-654f",
    "agy-session-bd7c",
    "agy-session-bbab",
    "agy-session-dde6",
    "agy-session-700c",
]

# UUIDs that must NEVER be touched even though they look like session ids.
UUID_ALLOWLIST = {
    "0a93466a-7961-4bed-89c6-b216653cab85",  # AI Studio app id
}

# Context keywords: a UUID not in KNOWN_SESSION_UUIDS is only pseudonymised
# when its line looks like it is naming an agy/brain/session/conversation.
UUID_CONTEXT_KEYWORDS = ("agy", "brain", "session", "conversation", "subagent", "sender")

# Google Sheet / spreadsheet ids that are public and must never be flagged.
SHEET_ID_ALLOWLIST = {
    "1Tznbdor6-JFLkGNtuN5StasMSopnLkhdqzgbq7NWdAU",  # project sheet (view-only)
    "1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms",  # Google's public sample sheet
}

DRIVE_FOLDER_REDACTED = "REDACTED_DRIVE_FOLDER_ID"

EMAIL_ALLOWED_EXACT = {"noreply@anthropic.com", "noreply@github.com"}
EMAIL_ALLOWED_SUFFIX = "@users.noreply.github.com"

# Files/paths never scanned at all, even with --check.
HARD_EXCLUDE_NAMES = {"bun.lock"}

# Excluded from the repo-wide scan by default (still scanned when passed
# explicitly on the command line, e.g. by the tests job).
# scripts/sanitize.py itself is excluded: it necessarily contains the
# literal rule text (the <user> token, the known session UUIDs, the <gcp-project>
# id) as pattern source, not as a leak. Everything else in the repo is
# still checked against it.
DEFAULT_EXCLUDE_GLOBS = ["tests/fixtures/*", "tests/fixtures/**", "scripts/sanitize.py"]

# Rewritten by --fix everywhere EXCEPT these globs, where matches are still
# reported by --check but the file content is left untouched.
NO_REWRITE_GLOBS = ["data/*.json", "data/*.tsv"]

UUID_RE_TXT = r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}"


def session_pseudonym(uuid_str: str) -> str:
    digest = hashlib.sha256(uuid_str.lower().encode("utf-8")).hexdigest()
    return f"agy-session-{digest[:4]}"


SESSION_PSEUDONYMS = {u: session_pseudonym(u) for u in KNOWN_SESSION_UUIDS}


# --------------------------------------------------------------------------
# Rule engine
# --------------------------------------------------------------------------

class Rule:
    """One privacy rule: a compiled pattern plus how to react to a match.

    ``decide`` receives the regex Match and the full line of text the match
    sits on, and returns the replacement string, or None to mean "not
    actually a violation, leave untouched, don't report".
    """

    def __init__(
        self,
        rule_id: str,
        description: str,
        pattern: Pattern[str],
        decide: Callable[[re.Match], Optional[str]],
        fixable: bool = True,
    ):
        self.id = rule_id
        self.description = description
        self.pattern = pattern
        self.decide = decide
        self.fixable = fixable


def _re(pattern: str, flags: int = 0) -> Pattern[str]:
    return re.compile(pattern, flags)


# --- 1. Antigravity/agy brain paths (apply before the generic user-path rule)
_BRAIN_BS = _re(
    r"(?:[A-Za-z]:\\+[Uu]sers\\+<user>\\+(?:Documents\\+)?)?"
    r"\.gemini\\+antigravity\\+brain\\+(" + UUID_RE_TXT + r")\\+",
    re.IGNORECASE,
)
_BRAIN_FS = _re(
    r"(?:[A-Za-z]:/+[Uu]sers/+<user>/+(?:Documents/+)?|~/+|/(?:Users|home)/[^/\s\"']+/+)?"
    r"\.gemini/+antigravity/+brain/+(" + UUID_RE_TXT + r")/+",
    re.IGNORECASE,
)


def _brain_decide_bs(m: re.Match) -> Optional[str]:
    return "<agy-session>\\"


def _brain_decide_fs(m: re.Match) -> Optional[str]:
    return "<agy-session>/"


# --- 2. Antigravity repo paths
_REPO_PEACEFUL_D = _re(r"[Dd]:\\+Antigravity\\+peaceful-turing")
_REPO_PEACEFUL_LGB = _re(r"[Cc]:\\+[Uu]sers\\+<user>\\+Documents\\+antigravity\\+peaceful-turing")
_REPO_PEACEFUL_LGB_FS = _re(r"[Cc]:/+[Uu]sers/+<user>/+Documents/+antigravity/+peaceful-turing")
_REPO_WORKSPACE_D_BS = _re(r"[Dd]:\\+Antigravity\\+")
_REPO_WORKSPACE_D_FS = _re(r"[Dd]:/+Antigravity/+")

# --- 3. Generic Windows user path (%USERPROFILE%\... -> %USERPROFILE%\...)
_WIN_USER_BS = _re(r"[A-Za-z]:\\+[Uu]sers\\+<user>\\+")
_WIN_USER_FS = _re(r"[A-Za-z]:/+[Uu]sers/+<user>/+")

# --- 4. G:\My Drive mirror
_GDRIVE_BS = _re(r"[Gg]:\\+My\s+Drive\\+")
_GDRIVE_FS = _re(r"[Gg]:/+My\s+Drive/+")

# --- 5. macOS/Linux home paths
_UNIX_HOME = _re(r"/(?:Users|home)/[^/\s\"']+/")

# --- 6. Standalone username token
_USERNAME_LGB = _re(r"\bLGB\b")

# --- 7. Antigravity session UUIDs (generic, context-gated)
_UUID_ANY = _re(UUID_RE_TXT)

# Truncated known session ids, e.g. "agy-session-2287" or "sender agy-session-912e" -
# still identifying even without the full UUID, so pseudonymise the same
# known 8-hex first group on its own, word-bounded so it can't clip a
# longer, unrelated hex run.
_KNOWN_UUID_PREFIXES = {u.split("-")[0]: u for u in KNOWN_SESSION_UUIDS}
_UUID_PREFIX_RE = _re(
    r"\b(" + "|".join(re.escape(p) for p in _KNOWN_UUID_PREFIXES) + r")\b(-…|…)?"
)

# --- 8. GCP project id
_GCP_PROJECT = _re(r"\bREDACTED-ID\b")

# --- 9. Private Drive folder ids
_DRIVE_FOLDER_URL = _re(r"drive/folders/([A-Za-z0-9_-]{6,})")
_DRIVE_FOLDER_LITERAL = _re(r'FOLDER_ID\s*=\s*"([A-Za-z0-9_-]{6,})"')

# --- 10. Personal emails (check-only)
_EMAIL = _re(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")


def _drive_id_ok(captured: str) -> bool:
    return captured == DRIVE_FOLDER_REDACTED or captured in SHEET_ID_ALLOWLIST


def _email_allowed(addr: str) -> bool:
    if addr in EMAIL_ALLOWED_EXACT:
        return True
    return addr.lower().endswith(EMAIL_ALLOWED_SUFFIX)


def build_rules() -> List[Rule]:
    rules: List[Rule] = []

    rules.append(Rule("agy-brain-path", "Antigravity brain scratch path", _BRAIN_BS, _brain_decide_bs))
    rules.append(Rule("agy-brain-path", "Antigravity brain scratch path", _BRAIN_FS, _brain_decide_fs))

    rules.append(Rule("antigravity-repo", "Antigravity repo checkout path",
                       _REPO_PEACEFUL_D, lambda m: "<repo>"))
    rules.append(Rule("antigravity-repo", "Antigravity repo checkout path",
                       _REPO_PEACEFUL_LGB, lambda m: "<repo>"))
    rules.append(Rule("antigravity-repo", "Antigravity repo checkout path",
                       _REPO_PEACEFUL_LGB_FS, lambda m: "<repo>"))
    rules.append(Rule("antigravity-repo", "Antigravity workspace path",
                       _REPO_WORKSPACE_D_BS, lambda m: "<workspace>\\"))
    rules.append(Rule("antigravity-repo", "Antigravity workspace path",
                       _REPO_WORKSPACE_D_FS, lambda m: "<workspace>/"))

    rules.append(Rule("windows-user-path", "Windows user home path",
                       _WIN_USER_BS, lambda m: "%USERPROFILE%\\"))
    rules.append(Rule("windows-user-path", "Windows user home path",
                       _WIN_USER_FS, lambda m: "%USERPROFILE%/"))

    rules.append(Rule("gdrive-mirror", "Google Drive Desktop mirror path",
                       _GDRIVE_BS, lambda m: "<drive-mirror>\\"))
    rules.append(Rule("gdrive-mirror", "Google Drive Desktop mirror path",
                       _GDRIVE_FS, lambda m: "<drive-mirror>/"))

    rules.append(Rule("unix-home-path", "macOS/Linux home path",
                       _UNIX_HOME, lambda m: "~/"))

    rules.append(Rule("username-lgb", "Standalone username token",
                       _USERNAME_LGB, lambda m: "<user>"))

    def _uuid_decide(m: re.Match) -> Optional[str]:
        uuid_val = m.group(0)
        if uuid_val.lower() in {u.lower() for u in UUID_ALLOWLIST}:
            return None
        known = {u.lower(): p for u, p in SESSION_PSEUDONYMS.items()}
        if uuid_val.lower() in known:
            return known[uuid_val.lower()]
        line_start = m.string.rfind("\n", 0, m.start()) + 1
        line_end = m.string.find("\n", m.end())
        if line_end == -1:
            line_end = len(m.string)
        line = m.string[line_start:line_end].lower()
        if any(kw in line for kw in UUID_CONTEXT_KEYWORDS):
            return session_pseudonym(uuid_val)
        return None

    rules.append(Rule("agy-session-uuid", "Antigravity session UUID", _UUID_ANY, _uuid_decide))

    def _uuid_prefix_decide(m: re.Match) -> Optional[str]:
        full_uuid = _KNOWN_UUID_PREFIXES[m.group(1)]
        return SESSION_PSEUDONYMS[full_uuid]

    rules.append(Rule("agy-session-uuid", "Truncated Antigravity session id",
                       _UUID_PREFIX_RE, _uuid_prefix_decide))

    rules.append(Rule("gcp-project-id", "Hardcoded GCP project id",
                       _GCP_PROJECT, lambda m: "<gcp-project>"))

    def _drive_url_decide(m: re.Match) -> Optional[str]:
        if _drive_id_ok(m.group(1)):
            return None
        return "drive/folders/" + DRIVE_FOLDER_REDACTED

    def _drive_literal_decide(m: re.Match) -> Optional[str]:
        if _drive_id_ok(m.group(1)):
            return None
        return 'FOLDER_ID = "' + DRIVE_FOLDER_REDACTED + '"'

    rules.append(Rule("drive-folder-id", "Private Drive folder id", _DRIVE_FOLDER_URL, _drive_url_decide))
    rules.append(Rule("drive-folder-id", "Private Drive folder id", _DRIVE_FOLDER_LITERAL, _drive_literal_decide))

    def _email_decide(m: re.Match) -> Optional[str]:
        addr = m.group(0)
        if _email_allowed(addr):
            return None
        return addr  # check-only: never rewritten

    rules.append(Rule("personal-email", "Personal email address", _EMAIL, _email_decide, fixable=False))

    return rules


class Finding:
    __slots__ = ("path", "line", "rule_id", "description")

    def __init__(self, path: str, line: int, rule_id: str, description: str):
        self.path = path
        self.line = line
        self.rule_id = rule_id
        self.description = description

    def __str__(self) -> str:
        return f"{self.path}:{self.line}: {self.rule_id}  ({self.description})"


def process_text(content: str, rules: List[Rule], source_label: str, allow_rewrite: bool):
    """Run every rule over content once, in order, masking claimed spans.

    Returns (new_content, findings). When allow_rewrite is False the
    returned content always equals the input (used for data/*.json|tsv and
    for --check-only rules), but findings are still collected.
    """
    findings: List[Finding] = []
    working = content

    for rule in rules:
        def _sub(m: re.Match, rule=rule) -> str:
            original = m.group(0)
            repl = rule.decide(m)
            if repl is None:
                return original
            line = working.count("\n", 0, m.start()) + 1
            findings.append(Finding(source_label, line, rule.id, rule.description))
            # Always mask the matched span in the working copy so later,
            # lower-precedence rules don't re-match the same text and
            # double-report it. Whether the *file* gets rewritten is a
            # separate decision, made by the caller (allow_rewrite).
            return repl

        working = rule.pattern.sub(_sub, working)

    if not allow_rewrite:
        return content, findings
    return working, findings


def is_binary(path: Path) -> bool:
    try:
        with open(path, "rb") as fh:
            chunk = fh.read(8192)
    except OSError:
        return True
    return b"\0" in chunk


def matches_any_glob(rel_posix: str, globs: List[str]) -> bool:
    return any(fnmatch.fnmatch(rel_posix, g) for g in globs)


def git_tracked_files() -> List[Path]:
    out = subprocess.run(
        ["git", "ls-files"], cwd=REPO_ROOT, capture_output=True, text=True, check=True
    ).stdout
    return [REPO_ROOT / line for line in out.splitlines() if line]


def collect_targets(explicit_paths: List[str], excludes: List[str]) -> List[Path]:
    if explicit_paths:
        targets: List[Path] = []
        for p in explicit_paths:
            pp = Path(p)
            if not pp.is_absolute():
                pp = REPO_ROOT / pp
            if pp.is_dir():
                targets.extend(sorted(f for f in pp.rglob("*") if f.is_file()))
            elif pp.is_file():
                targets.append(pp)
        default_excludes: List[str] = []
    else:
        targets = git_tracked_files()
        default_excludes = DEFAULT_EXCLUDE_GLOBS

    all_excludes = default_excludes + excludes
    result = []
    for f in targets:
        if not f.exists() or not f.is_file():
            continue
        if f.name in HARD_EXCLUDE_NAMES:
            continue
        try:
            rel_posix = f.resolve().relative_to(REPO_ROOT).as_posix()
        except ValueError:
            rel_posix = str(f)
        if matches_any_glob(rel_posix, all_excludes):
            continue
        if is_binary(f):
            continue
        result.append(f)
    return result


def run(mode: str, explicit_paths: List[str], excludes: List[str], use_stdin: bool) -> int:
    rules = build_rules()

    if use_stdin:
        content = sys.stdin.read()
        _, findings = process_text(content, rules, "stdin", allow_rewrite=False)
        for f in findings:
            print(str(f))
        if findings:
            print(f"\n{len(findings)} finding(s) on stdin.", file=sys.stderr)
            return 1
        print("No findings on stdin.")
        return 0

    files = collect_targets(explicit_paths, excludes)
    all_findings: List[Finding] = []
    fix_counts: dict = {}
    changed_files = 0

    for f in files:
        try:
            content = f.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue

        rel_posix = f.resolve().relative_to(REPO_ROOT).as_posix()
        rewritable = mode == "fix" and not matches_any_glob(rel_posix, NO_REWRITE_GLOBS)

        new_content, findings = process_text(content, rules, rel_posix, allow_rewrite=rewritable)
        all_findings.extend(findings)

        if mode == "fix" and rewritable and new_content != content:
            f.write_text(new_content, encoding="utf-8")
            changed_files += 1
            for fd in findings:
                if fd.rule_id != "personal-email":
                    fix_counts[fd.rule_id] = fix_counts.get(fd.rule_id, 0) + 1

    for finding in all_findings:
        print(str(finding))

    if mode == "fix":
        print(f"\n--fix rewrote {changed_files} file(s).", file=sys.stderr)
        for rule_id, count in sorted(fix_counts.items()):
            print(f"  {rule_id}: {count}", file=sys.stderr)
        remaining = [f for f in all_findings if f.rule_id == "personal-email"]
        no_rewrite_hits = [
            f for f in all_findings
            if matches_any_glob(f.path, NO_REWRITE_GLOBS)
        ]
        if remaining:
            print(f"\n{len(remaining)} email finding(s) require manual review (no auto-fix).",
                  file=sys.stderr)
        if no_rewrite_hits:
            print(f"\n{len(no_rewrite_hits)} finding(s) in data/*.json|tsv were reported but "
                  "NOT rewritten (protected).", file=sys.stderr)
        return 0

    # --check
    if all_findings:
        print(f"\n{len(all_findings)} finding(s).", file=sys.stderr)
        return 1
    print("No findings.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true", help="report violations, exit 1 if any found")
    mode.add_argument("--fix", action="store_true", help="rewrite fixable violations in place")
    parser.add_argument("--exclude", action="append", default=[], metavar="GLOB",
                         help="glob (relative to repo root) to skip; repeatable")
    parser.add_argument("--stdin", action="store_true",
                         help="read content from stdin instead of scanning tracked files")
    parser.add_argument("paths", nargs="*", help="specific files/dirs to scan instead of the full tree")
    args = parser.parse_args()

    mode_name = "check" if args.check else "fix"
    return run(mode_name, args.paths, args.exclude, args.stdin)


if __name__ == "__main__":
    sys.exit(main())
