# Data Leak Inspector

> Find sensitive data. Fix risky permissions.

**Data Leak Inspector** is a CLI tool that helps you identify potentially exposed files in your storage systems — starting with Google Drive.

Instead of scanning file contents, DLI analyzes **metadata and permissions** to quickly highlight files that may be publicly accessible or shared.


## 🚀 Features (v0.1)

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
- 🧪 Demo dataset for quick testing


## 🧠 How It Works

DLI does not read file contents.

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
git clone https://github.com/yourusername/data-leak-inspector.git
cd data-leak-inspector


pip install -e .
```


## 🧪 Run with Demo Data
``` BBash
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


## ⚠️ Limitations (v0.1)

- ❌ No content scanning (PII detection)
- ❌ No Google Docs content parsing
- ❌ Heuristic-based risk (metadata only)


## 🛣 Roadmap

### v0.1 (current)
- Metadata scanning
- Google Drive integration
- Exposure detection


## 🧠 Philosophy

DLI is designed to:

- ✔ Minimize permissions
- ✔ Respect user privacy
- ✔ Deliver fast insights
- ✔ Be transparent in analysis


## 🤝 Contributing

Contributions are welcome.

1. Fork the repo
2. Create a branch
3. Submit a PR