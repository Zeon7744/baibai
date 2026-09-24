# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Added
- Baichuan MCP server v2: 12 standard tools (read/write/file/search/tts/speech)
- GitHub Actions workflow: `sync-gitee-gitcode.yml` — auto sync to Gitee + GitCode mirrors
- GitHub Actions workflow: `afdian-sponsors.yml` — auto sync Afdian sponsors to README
- README unified template: consistent badges, sponsorship block, multi-platform table
- FUNDING.yml: Afdian + GitHub Sponsors integration
- CONTRIBUTING.md: contributor guidelines

### Changed
- `pyproject.toml`: version bumped to 1.2.0
- Added `markdown>=3.5.0` dependency
- Updated project URLs to include Changelog and PyPI

### Fixed
- README: fixed version badge (was 1.3.0, now 1.2.0)
- README: removed auto-generated junk content at bottom

---

## [v1.2.0] — 2026-09-05

### Added
- MCP server v2 with 12 standard tools
- GitHub Actions auto-sync to Gitee and GitCode
- PyPI publishing readiness (pyproject.toml configured)
- Release tag: v1.2.0

### Changed
- Upgraded from v1.1.0 beta to stable release

---

## [v1.1.0] — 2026-08-20

### Added
- Initial MCP server v1 implementation
- Basic CLI tools: check-format, analyze, classify
- README and documentation structure

---

[v1.2.0]: https://github.com/Zeon7744/baibai/releases/tag/v1.2.0
[v1.1.0]: https://github.com/Zeon7744/baibai/releases/tag/v1.1.0
