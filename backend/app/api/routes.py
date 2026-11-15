import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException

from .. import deps, store
from ..config import settings
from ..schemas import (CheckRequest, CheckResponse, Evidence, PassportStatus, RecruiterCreate,
                       ReportRequest, VacancyCreate)
from ..services import data_shield
from ..services.scamtrace import hash_identifier

router = APIRouter(prefix="/v1")


@router.post("/check", response_model=CheckResponse)
def check(req: CheckRequest):
    """Check-a-Job: passport first, otherwise risk rating from the message."""
    if req.passport_id:
        st = deps.verification.verify_passport(req.passport_id)
        now = datetime.now(timezone.utc)
        ev = Evidence(source="JobShield passport", result=st.status, checked_at=now)
        if st.status == "valid":
            res = CheckResponse(rating="verified", score=0, reasons=[], evidence=[ev],
                                explanation=f"Employer, recruiter and vacancy confirmed for {st.vacancy} at {st.employer}.")
        else:
            res = CheckResponse(rating="high_risk" if st.status in ("bad_signature", "revoked") else "unverified",
                                score=0, reasons=[], evidence=[ev],
                                explanation=f"This passport is {st.status}. Do not treat the vacancy as verified.")
    else:
        res = deps.risk.assess(req)
    store.check_log.append({"time": datetime.now(timezone.utc).isoformat(), "rating": res.rating,
                            "reasons": [r.id for r in res.reasons]})  # no message text kept
    return res


@router.get("/passport/{passport_id}", response_model=PassportStatus)
def get_passport(passport_id: str):
    return deps.verification.verify_passport(passport_id)


@router.post("/passport/{passport_id}/revoke")
def revoke_passport(passport_id: str, employer: dict = Depends(deps.current_employer)):
    rec = store.passports.get(passport_id)
    if not rec or rec["payload"]["employer_id"] != employer["id"]:
        raise HTTPException(404, "Passport not found for this employer")
    deps.verification.revoke(passport_id)
    return {"passport_id": passport_id, "status": "revoked"}


@router.post("/report")
def report(req: ReportRequest):
    hashes = {hash_identifier("phone", p) for p in req.phones}
    hashes |= {hash_identifier("url", u) for u in req.urls}
    hashes |= {hash_identifier("account", a) for a in req.accounts}
    if not hashes:
        raise HTTPException(422, "Provide at least one phone, url or account")
    rid = deps.scamtrace.add_report(hashes)
    return {"report_id": rid, "linked_reports": len(deps.scamtrace.cluster(hashes)) - 1}


@router.post("/employer/recruiters")
def invite_recruiter(body: RecruiterCreate, employer: dict = Depends(deps.current_employer)):
    rid = str(uuid.uuid4())
    store.recruiters[rid] = {"id": rid, "employer_id": employer["id"], **body.model_dump()}
    return store.recruiters[rid]


@router.post("/employer/vacancies")
def create_vacancy(body: VacancyCreate, employer: dict = Depends(deps.current_employer)):
    """Employer admin approves a vacancy and gets a signed passport."""
    if body.recruiter_id:
        rec = store.recruiters.get(body.recruiter_id)
        if not rec or rec["employer_id"] != employer["id"]:
            raise HTTPException(422, "Recruiter was not invited by this employer")
    vid = str(uuid.uuid4())
    vacancy = {"id": vid, "employer_id": employer["id"], "title": body.title,
               "apply_url": body.apply_url, "recruiter_id": body.recruiter_id}
    store.vacancies[vid] = vacancy
    passport = deps.verification.issue_passport(employer, vacancy, min(body.valid_days, settings.passport_days))
    pid = passport["payload"]["passport_id"]
    return {"vacancy_id": vid, "passport_id": pid, "verify_url": f"{settings.public_url}/verify/{pid}"}


@router.get("/shield/{stage}")
def shield(stage: str):
    return data_shield.guidance(stage)


@router.get("/whatsapp/webhook")
def whatsapp_verify(hub_mode: str = "", hub_challenge: str = "", hub_verify_token: str = ""):
    """TODO: WhatsApp Business API webhook verification and message handling."""
    return {"status": "stub"}
