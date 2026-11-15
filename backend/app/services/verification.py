"""Three checks behind a Verified Vacancy Passport:
1. Employer identity  2. Recruiter authority  3. Vacancy approval."""
import secrets
import uuid
from datetime import datetime, timedelta, timezone

from .. import store
from ..schemas import PassportStatus
from .signing import SigningService


class VerificationService:
    def __init__(self, signer: SigningService):
        self.signer = signer

    def issue_passport(self, employer: dict, vacancy: dict, valid_days: int) -> dict:
        now = datetime.now(timezone.utc)
        payload = {
            "passport_id": str(uuid.uuid4()),
            "vacancy_id": vacancy["id"],
            "employer_id": employer["id"],
            "recruiter_id": vacancy.get("recruiter_id"),
            "issued_at": now.isoformat(),
            "expires_at": (now + timedelta(days=valid_days)).isoformat(),
            "nonce": secrets.token_hex(8),
        }
        record = {"payload": payload, "signature": self.signer.sign(payload), "revoked": False}
        store.passports[payload["passport_id"]] = record
        return record

    def verify_passport(self, passport_id: str) -> PassportStatus:
        now = datetime.now(timezone.utc)
        rec = store.passports.get(passport_id)
        if not rec:
            return PassportStatus(passport_id=passport_id, status="unknown", checked_at=now)
        p = rec["payload"]
        employer = store.employers.get(p["employer_id"], {})
        vac = store.vacancies.get(p["vacancy_id"], {})
        rec_ = store.recruiters.get(p["recruiter_id"] or "", {})
        base = dict(passport_id=passport_id, employer=employer.get("name"), recruiter=rec_.get("name"),
                    vacancy=vac.get("title"), apply_url=vac.get("apply_url"),
                    expires_at=datetime.fromisoformat(p["expires_at"]), checked_at=now)
        if not self.signer.verify(p, rec["signature"]):
            return PassportStatus(**{**base, "status": "bad_signature"})
        if rec["revoked"]:
            return PassportStatus(**{**base, "status": "revoked"})
        if now >= base["expires_at"]:
            return PassportStatus(**{**base, "status": "expired"})
        return PassportStatus(**{**base, "status": "valid"})

    def revoke(self, passport_id: str) -> bool:
        rec = store.passports.get(passport_id)
        if not rec:
            return False
        rec["revoked"] = True
        return True
