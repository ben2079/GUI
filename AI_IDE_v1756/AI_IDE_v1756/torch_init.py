from __future__ import annotations

"""Proxy to the ai_ide torch initialization helpers."""

from ai_ide.torch_init import init_torch_cuda, summarize_torch_environment, select_device  # noqa: E402

__all__ = ["init_torch_cuda", "summarize_torch_environment", "select_device"]
