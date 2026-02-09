"""Compatibility shim.

This project historically had multiple chat completion modules.
To keep the codebase consistent, all callers should use
`ai_ide.chat_completion`.

This module intentionally re-exports everything from `chat_completion.py`
so legacy imports keep working without maintaining a second implementation.
"""

from __future__ import annotations

from .chat_completion import *  # noqa: F401,F403
