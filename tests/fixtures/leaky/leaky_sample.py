# Synthetic fixture for tests/test_gates.py. Every value below is fake:
# no real credential, path, session id or address appears in this file.

# A fake-but-pattern-valid Google API key (gitleaks gcp-api-key pattern,
# AIza + 35 chars):
api_key = "AIzaSyDF4k3xxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# A Windows user path:
scratch_path = r"%USERPROFILE%\Downloads\notes.txt"

# An Antigravity/agy brain UUID path (fake UUID, not one of the repo's
# known session ids):
brain_db = r"<agy-session>\scratch\cache.db"

# A personal (non-allowlisted) email address:
contact_email = "jane.doe@example.org"
