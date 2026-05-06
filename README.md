# Data Leak Inspector

 # data-leak-inspector

![Tests](https://github.com/Smithech/data-leak-inspector/actions/workflows/publish.yml/badge.svg)
[![PyPI](https://img.shields.io/pypi/v/data-leak-inspector.svg)](https://pypi.org/project/data-leak-inspector/)
[![Python](https://img.shields.io/pypi/pyversions/data-leak-inspector.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![Ruff](https://img.shields.io/badge/code%20style-ruff-brightgreen)


> Find sensitive data. Fix risky permissions.

**Data Leak Inspector** is a CLI tool that helps you identify potentially exposed files in your storage systems — starting with Google Drive.

Instead of scanning file contents, DLI analyzes **metadata and permissions** to quickly highlight files that may be publicly accessible or shared.


## 🚀 Features

- 🔍 Metadata-based scanning (no file content access)
- ☁️ Google Drive integration
- 📂 Scans all files (including nested ones)
- 🔐 Exposure detection based on permissions
    - Public (anyone with link)
    - Shared (users, groups, domain)
    - Private
- 💬 Human-readable explanations
- 📊 Clean CLI output with summaries
- ⚡ Progress bar during scanning


## 🧠 How It Works

`DLI` does not read file contents.

Instead, it analyzes:

- File permissions (Google Drive API)
- Sharing settings
- Basic metadata (name, type, timestamps)

This allows:

```
✔ Faster scans
✔ Lower permissions required
✔ Easier approval for Google APIs
✔ Better privacy guarantees
```

## 📸 Example Output

``` Bash
Scanning 12/120: payroll.xlsx ████████████ 100%

SCAN RESULTS (BASIC)

[PUBLIC ] payroll_2024.xlsx
          → anyone with link (reader)

[SHARED ] team_notes.docx
          → shared with 3 user(s)

[PRIVATE] personal.txt
          → only accessible by owner

Summary:
  Total files: 120
  Public: 5
  Shared: 18
  Private: 97
```

## ⚙️ Installation
``` Bash
pip install data-leak-inspector
``` 

## 🧪 Run with Demo Data
``` Bash
dli scan --demo
```

## ☁️ Google Drive Setup


### 1. Create credentials
- Go to Google Cloud Console
- Enable Google Drive API
- Create OAuth credentials (Desktop app)
- Download `credentials.json`

### 2. Place credentials

Create the directory:

``` Bash
~/Documents/dli/
```

Add:

```
credentials.json
```

### 3. Run scan
``` Bash
dli scan --gdrive
``` 

On first run:

- Browser will open for authentication
- A token.json file will be created


## 🧾 CLI Usage

``` Bash
dli scan [OPTIONS]
``` 

### Options
| Option    | Description                     |
|-----------|---------------------------------|
| `--demo`    | Use built-in demo dataset       |
| `--gdrive`  | Scan Google Drive               |
| `--verbose` | Show debug logs                 |
| `--quiet`   | Show only errors                |
| `--report`  | Export results to JSON          |


## 📁 Project Structure

``` 
leak_inspector/
├── application/
│   ├── scanner.py
│   ├── risk_evaluator.py
│   └── ports/
├── domain/
│   ├── models.py
│   ├── enums.py
│   └── reporting.py
├── infrastructure/
│   ├── storage/
│   └── gdrive/
├── interfaces/
│   └── cli/
``` 

## 🔐 Exposure Levels

| Level   | Description                               |
|:--------|:------------------------------------------|
| PUBLIC  | Accessible by anyone with link            |
| SHARED  | Shared with specific users/groups         |
| PRIVATE | Only accessible by owner                  |


## 📜 Changelog

All notable changes to this project are documented in the CHANGELOG.md file.

We follow the conventions defined by Keep a Changelog and adhere to Semantic Versioning. Each release includes categorized changes such as:

- **Added** for new features
- **Changed** for updates to existing behavior
- **Fixed** for bug fixes
- **Security** for vulnerability patches

An **Unreleased** section is also maintained to track upcoming changes before they are officially released.

When upgrading, we recommend reviewing the changelog to understand new features, bug fixes, and any potential breaking changes.


## 🧠 Philosophy

DLI is designed to:

- ✔ Minimize permissions
- ✔ Respect user privacy
- ✔ Deliver fast insights
- ✔ Be transparent in analysis