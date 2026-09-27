"""Small JSON persistence helpers used by application modules."""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any


def load_json(path: str | Path, default: Any) -> Any:
    """Return JSON data from *path*, or a copy of *default* when it is empty."""
    file_path = Path(path)
    if not file_path.exists() or not file_path.read_text(encoding="utf-8").strip():
        return deepcopy(default)

    try:
        with file_path.open("r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError as error:
        raise ValueError(f"Invalid JSON in {file_path.name}.") from error


def save_json(path: str | Path, data: Any) -> None:
    """Write JSON data to *path* with readable formatting."""
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with file_path.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)
        file.write("\n")
