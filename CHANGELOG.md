# Changelog

All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog,
and this project adheres to Semantic Versioning.

## [Unreleased]

### Added
- 

### Changed
- 

### Fixed
- 

### ⚠️ Breaking Changes
- 


## [0.2.0] - 2026-05-

### Added
- `init` command to
- `auth` command to
- `logout` command to
- escaneo filtro por extensiones (configurable file extension filtering for Google Drive scans)

### Changed
- The application now uses the operating system's standard configuration directory (XDG on Linux/macOS, AppData on Windows)

### Fixed
- `--demo` flag to use bundled demo data for basic scanning.
- `--report` flag to export scan results as JSON

### ⚠️ Breaking Changes
- Configuration and credentials will be moved to the new OS-specific location and must be migrated manually

---

## [0.1.0] - 2026-05-05

### Added
- Initial release of the `dli` CLI
- `scan` command to analyze file permissions in Google Drive
- `--gdrive` flag to use Google Drive as a storage backend (mock implementation)
- `--mode` flag with `basic` (metadata) and `deep` (content analysis) options
- `--verbose` flag for debug-level logging
- `--quiet` flag to limit output to warnings and errors
- Progress indicators for file fetching and scanning
- Persistence layer using SQLite