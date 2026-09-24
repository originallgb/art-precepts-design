# First public version: finish line

Target: publish a secure, honestly described work in progress. A finished
playbook, improved clustering, a polished app and a complete case study
are **not** requirements for the first public version.

This is a short companion to [release issue #5](https://github.com/originallgb/art-precepts-design/issues/5)
and the existing [security gate](https://github.com/originallgb/art-precepts-design/issues/1).
It does not declare either complete. Snapshot: 24 September 2026, repository
still private; release PRs #3 and #4 open.

## Before changing visibility

- [ ] Integrate the reviewed security and documentation changes with the new
  README. Run the checks on that exact version. Do not mistake green checks
  on an older PR head for a checked release.
- [ ] Remove secrets and the private identifiers selected for removal from
  the public tree and history, including scanner rule definitions. Check
  the refs that will be published; keep the original archive private.
- [ ] Resolve the public data scope. The current datasets still contain
  museum descriptions and private Drive references. Include only material
  whose redistribution basis is established; use a separate public export
  if necessary, preserving private originals.
- [ ] Verify linked Sheet access and that private Drive images/folders remain
  private. A link or file ID does not establish its permissions. Remove an
  unavailable public-facing link rather than inventing its status.
- [ ] Review the final release evidence against issue #1, then change visibility
  and enable the required branch checks. Verify the public README and its
  links without relying on the owner's signed-in access.

## After publication

Record the published commit and date here, with links to passing checks.
Start the next small experiment in the [journal](../journal/README.md).

Avoid hosting the historical app as a public API for this first release.
Sharing source and a working record does not require operating a service.
