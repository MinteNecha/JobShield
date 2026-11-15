"""In-memory store for the prototype.

TODO: replace with PostgreSQL (see db/schema.sql). Do not store message text.
"""
import json
from pathlib import Path

_data = json.loads((Path(__file__).parent / "data" / "demo_data.json").read_text())
employers: dict[str, dict] = {e["id"]: e for e in _data["employers"]}
recruiters: dict[str, dict] = {}
vacancies: dict[str, dict] = {}
passports: dict[str, dict] = {}
check_log: list[dict] = []  # time, result, reasons only


def employer_by_key(key: str) -> dict | None:
    return next((e for e in employers.values() if e["api_key"] == key), None)
