# Changelog

All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog,
and this project adheres to Semantic Versioning.


## [0.2.0] - 2026-05-08

### Added
- `init` command to initialize project and Google Drive setup.
- `auth` command to authenticate with Google and store credentials.
- `logout` command to remove stored credentials.
- Configurable file extension filtering for Google Drive scans.

### Changed
- The application now uses the operating system's standard configuration directory (XDG on Linux/macOS, AppData on Windows)

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