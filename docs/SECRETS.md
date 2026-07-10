# Secrets Management & Local Credentials
> Local database credentials, database security guidelines, and rules to prevent credential exposure in public repositories.

*Design / Planned — Not yet implemented*

---

## 1. Local Credentials Model

ExamShield runs entirely on local machines and does not use cloud authentication services, cloud databases, or third-party ML API keys.

```
┌────────────────────────────────────────────────────────┐
│ Client Desktop PC (Local Host OS)                      │
├────────────────────────────────────────────────────────┤
│  [ SQLite DB File ] ──► (Uses default OS file permissions)│
│                                                        │
│  No public network access                              │
│  No hardcoded database passwords                       │
└────────────────────────────────────────────────────────┘
```

Because SQLite databases are stored as single files directly on disk, access security relies on standard operating system file permissions rather than network passwords:
*   Configure the `/data/` folder permissions to restrict read/write access to the active exam-cell user account.
*   Do not hardcode database password keys in python scripts or store credentials in the code repository.

---

## 2. Preventing Key Exposure in Git

To prevent configuration settings, model weights, or student CSV rosters from being committed to the public Git repository, include the following directories in `.gitignore`:

```
# .gitignore
# Python virtual environment
.venv/
__pycache__/
*.pyc

# Local data directories containing student scripts and rosters
data/corpus/
data/results/
data/register.csv
db.sqlite3

# Model weight caches
.cache/
```

Never commit database backup files (`.db`, `.sqlite`) or CSV roster records containing actual student names and grades.

---

## 3. Related Documents

*   [Technology Stack Specifications](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/TECH_STACK.md)
*   [Local Storage specifications](file:///Users/gaurav/Desktop/MyProjects/E-Shield/app/storage/README.md)
*   [Secure Development Guidelines](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/SECURE_DEVELOPMENT.md)

## To-Do List

- [ ] Setup .env templates
- [ ] Configure local secrets manager integration
- [ ] Review document for technical accuracy against current implementation.
- [ ] Ensure all referenced internal links are valid and working.
- [ ] Add architectural or workflow diagrams where applicable.
- [ ] Proofread for grammar, consistency, and tone.
- [ ] Cross-reference with SYSTEM_DESIGN.md for alignment.
- [ ] Verify that security considerations are documented if relevant.
- [ ] Add examples or code snippets to clarify complex sections.
- [ ] Check formatting (headers, bolding, lists) for readability.
