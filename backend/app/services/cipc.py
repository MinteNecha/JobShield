"""Company record lookup.

SIMULATED: reads the demo dataset. Real CIPC API access needs approval and a paid plan.
Keep this interface so the real client can replace it without touching callers.
"""
from .. import store


def lookup(registration_number: str) -> dict | None:
    for e in store.employers.values():
        if e["registration_number"] == registration_number:
            return e
    return None
