import json
import os
from typing import Dict, List

from config import HISTORY_FILE


def load_history() -> List[Dict]:
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return []


def save_history(history: List[Dict]) -> None:
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)


def add_entry(entry: Dict) -> None:
    history = load_history()
    history.insert(0, entry)  # el más reciente primero
    save_history(history)