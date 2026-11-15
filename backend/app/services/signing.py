"""Ed25519 signing for Verified Vacancy Passports (RFC 8032).

In production the private key lives in a managed vault (never in code or the repo).
"""
import base64
import json
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey


def canonical(payload: dict) -> bytes:
    return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()


class SigningService:
    def __init__(self, seed_b64: str = ""):
        if seed_b64:
            self._key = Ed25519PrivateKey.from_private_bytes(base64.b64decode(seed_b64))
        else:
            self._key = Ed25519PrivateKey.generate()  # temporary key for development
        self._pub = self._key.public_key()

    def sign(self, payload: dict) -> str:
        return base64.urlsafe_b64encode(self._key.sign(canonical(payload))).decode()

    def verify(self, payload: dict, signature: str) -> bool:
        try:
            self._pub.verify(base64.urlsafe_b64decode(signature), canonical(payload))
            return True
        except (InvalidSignature, ValueError):
            return False
