# ALDE

## ⚠️ Security Notice - READ FIRST

**Before using this application:**

1. **🔐 Never commit your `.env` file** - It contains your API keys
2. **🔑 Set `OPENAI_API_KEY` in `ALDE/ALDE/.env`** (see `.env.example` for template)
3. **🛡️ Keep your API keys private** - Never share them or commit them to Git
4. **📋 Read [SECURITY.md](SECURITY.md)** for complete security guidelines
5. **🤝 Review [CONTRIBUTING.md](CONTRIBUTING.md)** before contributing

**Quick Security Check:**
```bash
# Verify .env is ignored by Git
git check-ignore ALDE/ALDE/.env
# Should output: ALDE/ALDE/.env

# Check for accidentally committed secrets
./scripts/check_history_for_secrets.sh
```

---

## About

This repository contains the **AI IDE v1756** project (Python + PySide6/Qt) with a modular backend (RAG + agent workflows) and a local packaging setup.

## Quickstart

If you cloned without submodules, initialize them first:

```bash
git submodule update --init --recursive
```

Create a virtualenv and install editable:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

Run the app entrypoint:

```bash
python -m ALDE.ALDE.alde
```

## Why it may look "incomplete"

This repo is cleaned for **public reference**: local/private runtime artifacts (PDFs, vector stores, histories, caches) are intentionally not tracked.

To bootstrap a fresh clone with an empty-but-valid local state, run:

```bash
python scripts/bootstrap_local_state.py
```

Then set your `OPENAI_API_KEY` in `ALDE/ALDE/.env` (this file stays ignored).


## Repo hygiene (public reference)

This repo uses an `AppData/` folder for local runtime state (history, vector stores, caches, generated files). These are intentionally **ignored** for a clean, linkable reference repo.

See `ALDE/ALDE/AppData/README.md` for what is tracked vs ignored.

If you need a clean starting point for local runs, use:
- `dispatcher_doc_db.example.json`
- `ALDE/ALDE/db.example.json`

Copy them to `dispatcher_doc_db.json` / `db.json` locally if needed (these copies remain ignored).
