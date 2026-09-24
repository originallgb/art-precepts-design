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
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Callable, List, Optional, Pattern

REPO_ROOT = Path(__file__).resolve().parents[1]

# --------------------------------------------------------------------------
# Allowlists and known identifiers
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
# Private identifiers: NOT stored in this file.
#
# Low-entropy identifiers (usernames, the GCP project id, truncated session
# id prefixes) cannot be hidden by hashing: a digest of "abc" falls to a
# brute-force in milliseconds. They are loaded at run time from, in order:
#   1. $PRIVATE_IDENTIFIERS_JSON  (the JSON itself, e.g. a CI secret)
#   2. $PRIVATE_IDENTIFIERS_FILE  (a path)
#   3. ~/.config/art-precepts/private-identifiers.json
# Format: {"usernames": [...], "gcp_projects": [...], "session_uuids": [...]}
# With no private source the generic public patterns below still apply
# (any Windows/Unix home path, any keyword-tagged UUID, any private Drive
# folder id, any non-allowlisted email) and the digests below still catch
# the known session UUIDs, but bare username / project-id tokens are only
# detected when the private file is available.
# --------------------------------------------------------------------------

DIGEST_PREFIX = "art-precepts/v1:"


def uuid_digest(uuid_str: str) -> str:
    return hashlib.sha256((DIGEST_PREFIX + uuid_str.lower()).encode("utf-8")).hexdigest()


# SHA-256 digests of the known Antigravity/agy session UUIDs. A UUID has
# ~122 bits of entropy so its digest is safe to publish. Matching UUID
# tokens get the stable pseudonym below even with no keyword on the line.
KNOWN_SESSION_UUID_DIGESTS = {
    "aac1e8095138336e8041cf65faacec6dda2d6839ae5e8c3b0d276f739febc685",
    "d5103efcffe4302a1d707156c0e10dcea9e165f3bfe9807038796f4527b64b83",
    "43f64da1661e18379180d756daa5944826f3a0a29f0f3b76ad4e5b8da6c4eb7f",
    "a614cf029c384f9ef8284f890f9f72c7838ca37f085c4f20849dd79a2e5305c1",
    "4dd8b0ce9b87576e1cf2283491a91ef2537c4f4f2d6b1a88d66abb8268107843",
    "4a3169a28d117a83cce3264a4e774027045aa27aacdfa5ec78e86a92128605ec",
    "16aab051789c58dde1b374d6cd38991adad7f39689f2437ad50af487bfdfdf66",
    "0d238f0166896ef45df704dfe28ff0648773eb6f523d65242c93d1ad9379c2fd",
}


def load_private_identifiers() -> dict:
    ids = {"usernames": [], "gcp_projects": [], "session_uuids": []}
    raw = os.environ.get("PRIVATE_IDENTIFIERS_JSON")
    if not raw:
        path = Path(os.environ.get("PRIVATE_IDENTIFIERS_FILE")
                    or Path.home() / ".config" / "art-precepts" / "private-identifiers.json")
        try:
            raw = path.read_text(encoding="utf-8")
        except OSError:
            raw = None
    if raw:
        data = json.loads(raw)
        for key in ids:
            ids[key] = [str(v) for v in data.get(key, []) if str(v).strip()]
    return ids


PRIVATE = load_private_identifiers()
PRIVATE_UUIDS = {u.lower() for u in PRIVATE["session_uuids"]}

# UUIDs that must NEVER be touched even though they look like session ids.
UUID_ALLOWLIST = {
    "0a93466a-7961-4bed-89c6-b216653cab85",  # AI Studio app id
}

# Context keywords: a UUID not in the known digests/private list is only pseudonymised
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

# Nothing is excluded from the repo-wide scan by default: scripts/sanitize.py
# holds digests and generic patterns, never literals, and the tests
# synthesise their leaky samples at run time instead of committing them.
DEFAULT_EXCLUDE_GLOBS: List[str] = []

# Rewritten by --fix everywhere EXCEPT these globs, where matches are still
# reported by --check but the file content is left untouched.
NO_REWRITE_GLOBS = ["data/*.json", "data/*.tsv"]

UUID_RE_TXT = r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}"


def session_pseudonym(uuid_str: str) -> str:
    digest = hashlib.sha256(uuid_str.lower().encode("utf-8")).hexdigest()
    return f"agy-session-{digest[:4]}"



def is_known_session_uuid(uuid_str: str) -> bool:
    return uuid_digest(uuid_str) in KNOWN_SESSION_UUID_DIGESTS or uuid_str.lower() in PRIVATE_UUIDS



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
    r"(?:[A-Za-z]:\\+[Uu]sers\\+[^\\\s\"']+\\+(?:Documents\\+)?)?"
    r"\.gemini\\+antigravity\\+brain\\+(" + UUID_RE_TXT + r")\\+",
    re.IGNORECASE,
)
_BRAIN_FS = _re(
    r"(?:[A-Za-z]:/+[Uu]sers/+[^/\s\"']+/+(?:Documents/+)?|~/+|/(?:Users|home)/[^/\s\"']+/+)?"
    r"\.gemini/+antigravity/+brain/+(" + UUID_RE_TXT + r")/+",
    re.IGNORECASE,
)


def _brain_decide_bs(m: re.Match) -> Optional[str]:
    return "<agy-session>\\"


def _brain_decide_fs(m: re.Match) -> Optional[str]:
    return "<agy-session>/"


# --- 2. Antigravity repo paths
_REPO_PEACEFUL_D = _re(r"[Dd]:\\+Antigravity\\+peaceful-turing")
_REPO_PEACEFUL_USER_BS = _re(r"[Cc]:\\+[Uu]sers\\+[^\\\s\"']+\\+Documents\\+antigravity\\+peaceful-turing")
_REPO_PEACEFUL_USER_FS = _re(r"[Cc]:/+[Uu]sers/+[^/\s\"']+/+Documents/+antigravity/+peaceful-turing")
_REPO_WORKSPACE_D_BS = _re(r"[Dd]:\\+Antigravity\\+")
_REPO_WORKSPACE_D_FS = _re(r"[Dd]:/+Antigravity/+")

# --- 3. Generic Windows user path (C:\Users\<any name>\... -> %USERPROFILE%\...)
# System profiles and already-placeholdered names are not private.
_WIN_USER_SKIP = r"(?!(?:Public|Default|All Users|Default User)[\\/])(?![%<])"
_WIN_USER_BS = _re(r"[A-Za-z]:\\+[Uu]sers\\+" + _WIN_USER_SKIP + r"[^\\\s\"']+\\+")
_WIN_USER_FS = _re(r"[A-Za-z]:/+[Uu]sers/+" + _WIN_USER_SKIP + r"[^/\s\"']+/+")

# --- 4. G:\My Drive mirror
_GDRIVE_BS = _re(r"[Gg]:\\+My\s+Drive\\+")
_GDRIVE_FS = _re(r"[Gg]:/+My\s+Drive/+")

# --- 5. macOS/Linux home paths
_UNIX_HOME = _re(r"/(?:Users|home)/[^/\s\"']+/")

# --- 6. Standalone username token (from the private identifier source only)
_USERNAME_TOKEN = (
    _re(r"\b(?:" + "|".join(re.escape(u) for u in PRIVATE["usernames"]) + r")\b")
    if PRIVATE["usernames"] else None
)

# --- 7. Antigravity session UUIDs (generic, context-gated)
_UUID_ANY = _re(UUID_RE_TXT)

# Truncated known session ids (the first 8 hex digits, optionally followed
# by an ellipsis) -
# still identifying even without the full UUID, so pseudonymise the same
# known 8-hex first group on its own, word-bounded so it can't clip a
# longer, unrelated hex run.
# Prefixes are 32 bits, so they come from the private source only.
_KNOWN_UUID_PREFIXES = {u.split("-")[0].lower(): u.lower() for u in PRIVATE["session_uuids"]}
_UUID_PREFIX_RE = (
    _re(r"\b(" + "|".join(re.escape(p) for p in _KNOWN_UUID_PREFIXES) + r")\b(-…|…)?", re.IGNORECASE)
    if _KNOWN_UUID_PREFIXES else None
)

# --- 8. GCP project id
_GCP_PROJECT = (
    _re(r"\b(?:" + "|".join(re.escape(u) for u in PRIVATE["gcp_projects"]) + r")\b")
    if PRIVATE["gcp_projects"] else None
)

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
                       _REPO_PEACEFUL_USER_BS, lambda m: "<repo>"))
    rules.append(Rule("antigravity-repo", "Antigravity repo checkout path",
                       _REPO_PEACEFUL_USER_FS, lambda m: "<repo>"))
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

    if _USERNAME_TOKEN is not None:
        rules.append(Rule("username-token", "Standalone username token",
                           _USERNAME_TOKEN, lambda m: "<user>"))

    def _uuid_decide(m: re.Match) -> Optional[str]:
        uuid_val = m.group(0)
        if uuid_val.lower() in {u.lower() for u in UUID_ALLOWLIST}:
            return None
        if is_known_session_uuid(uuid_val):
            return session_pseudonym(uuid_val)
        line_start = m.string.rfind("\n", 0, m.start()) + 1
        line_end = m.string.find("\n", m.end())
        if line_end == -1:
            line_end = len(m.string)
        line = m.string[line_start:line_end].lower()
        if any(kw in line for kw in UUID_CONTEXT_KEYWORDS):
            return session_pseudonym(uuid_val)
        return None

    rules.append(Rule("agy-session-uuid", "Antigravity session UUID", _UUID_ANY, _uuid_decide))

    if _UUID_PREFIX_RE is not None:
        def _uuid_prefix_decide(m: re.Match) -> Optional[str]:
            return session_pseudonym(_KNOWN_UUID_PREFIXES[m.group(1).lower()])

        rules.append(Rule("agy-session-uuid", "Truncated Antigravity session id",
                           _UUID_PREFIX_RE, _uuid_prefix_decide))

    if _GCP_PROJECT is not None:
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

        try:
            rel_posix = f.resolve().relative_to(REPO_ROOT).as_posix()
        except ValueError:  # explicit path outside the repo
            rel_posix = str(f)
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


def _pat_bytes_regex(pat: Pattern[str]) -> str:
    """Python pattern -> filter-repo `regex:` body (IGNORECASE inlined)."""
    body = pat.pattern
    return f"(?i:{body})" if pat.flags & re.IGNORECASE else body


def _esc_repl(repl: str) -> str:
    return repl.replace("\\", "\\\\")


def emit_filter_repo_rules(out_path: str) -> int:
    """Write git-filter-repo --replace-text expressions derived from the
    same rules as --fix. The file necessarily contains the private literals,
    so it must live OUTSIDE the repo and is created 0600."""
    out = Path(out_path).resolve()
    if REPO_ROOT in out.parents:
        print("refusing to write literals inside the repo tree", file=sys.stderr)
        return 2
    rendered: List[str] = []
    # Constant-replacement rules, in build_rules() order (same precedence as
    # --fix). Match-dependent rules (UUIDs, Drive ids, emails) are expanded
    # explicitly below or, for emails, are check-only.
    for rule in build_rules():
        if rule.id in ("personal-email", "agy-session-uuid", "drive-folder-id"):
            continue
        repl = rule.decide(None)  # these decide() callables ignore the match
        rendered.append(f"regex:{_pat_bytes_regex(rule.pattern)}==>{_esc_repl(repl)}")
    # Known session UUIDs and prefixes (need the private source).
    for u in sorted(PRIVATE_UUIDS):
        rendered.append(f"{u}==>{session_pseudonym(u)}")
    for pref, full in sorted(_KNOWN_UUID_PREFIXES.items()):
        rendered.append(f"regex:\\b{re.escape(pref)}\\b(?:-…|…)?==>{session_pseudonym(full)}")
    allow = "|".join(re.escape(x) for x in sorted(SHEET_ID_ALLOWLIST) + [DRIVE_FOLDER_REDACTED])
    idre = r"[A-Za-z0-9_-]{6,}"
    rendered.append(f"regex:drive/folders/(?!(?:{allow})(?![A-Za-z0-9_-])){idre}==>drive/folders/{DRIVE_FOLDER_REDACTED}")
    rendered.append(f'regex:FOLDER_ID\\s*=\\s*"(?!(?:{allow})")' + idre + f'"==>FOLDER_ID = "{DRIVE_FOLDER_REDACTED}"')
    out.write_text("\n".join(rendered) + "\n", encoding="utf-8")
    out.chmod(0o600)
    print(f"wrote {len(rendered)} expressions to {out}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    if "--emit-filter-repo-rules" in sys.argv:
        idx = sys.argv.index("--emit-filter-repo-rules")
        return emit_filter_repo_rules(sys.argv[idx + 1])
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true", help="report violations, exit 1 if any found")
    mode.add_argument("--fix", action="store_true", help="rewrite fixable violations in place")
    parser.add_argument("--exclude", action="append", default=[], metavar="GLOB",
                         help="glob (relative to repo root) to skip; repeatable")
    parser.add_argument("--stdin", action="store_true",
                         help="read content from stdin instead of scanning tracked files")
    parser.add_argument("--emit-filter-repo-rules", metavar="FILE",
                         help="write git-filter-repo --replace-text expressions (contains private "
                              "literals; must be outside the repo) and exit")
    parser.add_argument("paths", nargs="*", help="specific files/dirs to scan instead of the full tree")
    args = parser.parse_args()

    mode_name = "check" if args.check else "fix"
    return run(mode_name, args.paths, args.exclude, args.stdin)


if __name__ == "__main__":
    sys.exit(main())
