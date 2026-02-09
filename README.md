# GUI workspace

This repository contains the **AI IDE v1756** project (Python + PySide6/Qt) with a modular backend (RAG + agent workflows) and a local packaging setup.

## Quickstart

Create a virtualenv and install editable:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

Run the app entrypoint:

```bash
python -m AI_IDE_v1756.AI_IDE_v1756.ai_ide
```

## Why it may look "incomplete"

This repo is cleaned for **public reference**: local/private runtime artifacts (PDFs, vector stores, histories, caches) are intentionally not tracked.

To bootstrap a fresh clone with an empty-but-valid local state, run:

```bash
python scripts/bootstrap_local_state.py
```

Then set your `OPENAI_API_KEY` in `AI_IDE_v1756/AI_IDE_v1756/.env` (this file stays ignored).


## Repo hygiene (public reference)

This repo uses an `AppData/` folder for local runtime state (history, vector stores, caches, generated files). These are intentionally **ignored** for a clean, linkable reference repo.

See `AI_IDE_v1756/AI_IDE_v1756/AppData/README.md` for what is tracked vs ignored.

If you need a clean starting point for local runs, use:
- `dispatcher_doc_db.example.json`
- `AI_IDE_v1756/AI_IDE_v1756/db.example.json`

Copy them to `dispatcher_doc_db.json` / `db.json` locally if needed (these copies remain ignored).
