"""SCAMTRACE: links scam reports that share an identifier.

Identifiers are stored only as keyed hashes (HMAC-SHA256). A plain hash of a phone
number could be reversed by trying every number, so the key stays secret.
"""
import hashlib
import hmac
import re
import uuid
from collections import deque
from datetime import datetime, timezone

from ..config import settings


def normalise(kind: str, value: str) -> str:
    v = value.strip().lower()
    if kind == "phone":
        d = re.sub(r"\D", "", v)
        if d.startswith("0") and len(d) == 10:
            d = "27" + d[1:]
        return d
    if kind == "url":
        v = re.sub(r"^https?://", "", v).split("/")[0]
        return v.removeprefix("www.")
    return re.sub(r"\s+", "", v)


def hash_identifier(kind: str, value: str) -> str:
    msg = f"{kind}:{normalise(kind, value)}".encode()
    return hmac.new(settings.hash_key.encode(), msg, hashlib.sha256).hexdigest()


class ScamTrace:
    def __init__(self):
        self.reports: dict[str, dict] = {}

    def add_report(self, hashes: set[str], template_fp: str | None = None) -> str:
        rid = str(uuid.uuid4())
        self.reports[rid] = {"hashes": set(hashes), "template": template_fp,
                             "date": datetime.now(timezone.utc)}
        return rid

    def matches(self, hashes: set[str]) -> int:
        return sum(1 for r in self.reports.values() if r["hashes"] & hashes)

    def cluster(self, hashes: set[str]) -> set[str]:
        """Report ids linked (directly or through other reports) to these identifiers."""
        seen: set[str] = set()
        queue = deque(rid for rid, r in self.reports.items() if r["hashes"] & hashes)
        while queue:
            rid = queue.popleft()
            if rid in seen:
                continue
            seen.add(rid)
            for oid, o in self.reports.items():
                if oid not in seen and o["hashes"] & self.reports[rid]["hashes"]:
                    queue.append(oid)
        return seen
