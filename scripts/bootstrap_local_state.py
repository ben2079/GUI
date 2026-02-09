from __future__ import annotations

import shutil
from pathlib import Path


def _copy_if_missing(src: Path, dst: Path) -> None:
    if dst.exists():
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dst)


def main() -> int:
    repo = Path(__file__).resolve().parents[1]

    # Root-level local DBs (kept ignored, but useful to bootstrap)
    root_dispatcher_example = repo / "dispatcher_doc_db.example.json"
    root_dispatcher = repo / "dispatcher_doc_db.json"

    pkg_root = repo / "AI_IDE_v1756" / "AI_IDE_v1756"
    pkg_appdata = pkg_root / "AppData"

    db_example = pkg_root / "db.example.json"
    db_local = pkg_root / "db.json"

    env_example = pkg_root / ".env.example"
    env_local = pkg_root / ".env"

    # Create expected runtime directories (empty is fine)
    for d in (
        pkg_appdata,
        pkg_appdata / "generated",
        pkg_appdata / "icon_cache",
        pkg_appdata / "templates",
        pkg_appdata / "VSM_0_Data",
        pkg_appdata / "VSM_1_Data",
        pkg_appdata / "VSM_2_Data",
        pkg_appdata / "VSM_3_Data",
        pkg_appdata / "VSM_4_Data",
    ):
        d.mkdir(parents=True, exist_ok=True)

    # Copy safe example files into ignored local defaults
    if root_dispatcher_example.exists():
        _copy_if_missing(root_dispatcher_example, root_dispatcher)

    if db_example.exists():
        _copy_if_missing(db_example, db_local)

    if env_example.exists():
        _copy_if_missing(env_example, env_local)

    print("Bootstrapped local state (AppData dirs + example .env/db).")
    print("Next: set OPENAI_API_KEY in AI_IDE_v1756/AI_IDE_v1756/.env (local, ignored).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
