"""ai_ide package.

This repository historically supported running modules both as scripts
(e.g. `python ai_ide/ai_ide_v1756.py`) and as an importable package.

Having this file makes imports like `import ai_ide.agents_factory` work
reliably across entrypoints.
"""

from __future__ import annotations
