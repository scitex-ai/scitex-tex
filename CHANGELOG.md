# Changelog

All notable changes to `scitex-tex` are documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/);
versions follow [Semantic Versioning](https://semver.org/).

## [0.1.8] - 2026-10-02

- Return the documented Matplotlib Figure from the current recording wrapper; retain the actual plotting dependency and real preview/layout/text assertions.
- Preserve trusted-main license and CLA policy, and run strict complete release tests in the digest-verified, job-owned CI SIF before normal OIDC publishing.

## [Unreleased]

### Added
- docs: refresh README, sphinx, and skills docs to reflect actual API

## [0.1.7]

- Release bump, workflow resync with scitex-dev v0.11.20
- Standardized GitHub Actions to scitex-dev canonical set

## [0.1.6]

- Test-quality cleanup: removed mocks, real matplotlib integration tests
- `try_import_optional` migration for optional scitex-str dependency
- Expanded subprocess timeout test coverage (real shell shim, no mocking)
- Skills leaves: 01_installation, 02_quick-start, 03_python-api
- README revamp with Problem & Solution / Architecture / Demo sections
- CHANGELOG.md + CONTRIBUTING.md added
- Audit-all integrated into test suite
- Umbrella `scitex` dependency dropped (PS139); switched to peer standalones
- scitex-dev pin floor bumped to 0.11.7
- Gitignore .scitex/ runtime artifacts

## [0.1.5]

- gitignore .scitex/ runtime artifacts (clew db etc)
- Cleared all 5 PS audit warnings (PS203, PS303, PS107/110/112/113)
- Release-safety: publish-pypi.yml opt-in (workflow_dispatch only)
- Skills: stripped trailing `<!-- EOF -->` (SK211)

## [0.1.4]

- Initial CHANGELOG entry — see git log for prior history.
