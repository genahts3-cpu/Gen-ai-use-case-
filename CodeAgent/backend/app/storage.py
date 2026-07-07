import json
from pathlib import Path
from typing import List
from .models import UseCase

DATA_FILE = Path(__file__).parent / "data" / "usecases.json"


def ensure_data_file():
    if not DATA_FILE.parent.exists():
        DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not DATA_FILE.exists():
        DATA_FILE.write_text("[]", encoding="utf-8")


def load_usecases() -> List[UseCase]:
    ensure_data_file()
    raw = DATA_FILE.read_text(encoding="utf-8")
    data = json.loads(raw or "[]")
    return [UseCase(**item) for item in data]


def save_usecases(usecases: List[UseCase]):
    ensure_data_file()
    DATA_FILE.write_text(
        json.dumps([u.model_dump() for u in usecases], indent=2),
        encoding="utf-8",
    )
