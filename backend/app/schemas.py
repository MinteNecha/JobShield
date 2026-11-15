from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class Reason(BaseModel):
    id: str
    text: str
    weight: int


class Evidence(BaseModel):
    source: str
    result: str
    checked_at: datetime


class CheckRequest(BaseModel):
    message: Optional[str] = Field(None, max_length=5000)
    url: Optional[str] = None
    phone: Optional[str] = None
    sender_email: Optional[str] = None
    passport_id: Optional[str] = None


class CheckResponse(BaseModel):
    rating: str  # verified | unverified | high_risk
    score: int
    reasons: list[Reason]
    evidence: list[Evidence]
    trafficking_alert: bool = False
    could_not_verify: bool = False
    advice: list[str] = []
    explanation: str = ""
    disclaimer: str = (
        "JobShield gives an evidence-backed risk rating. It never guarantees that a job is genuine."
    )


class ReportRequest(BaseModel):
    phones: list[str] = []
    urls: list[str] = []
    accounts: list[str] = []
    template_text: Optional[str] = Field(None, max_length=5000)


class RecruiterCreate(BaseModel):
    name: str
    agency: Optional[str] = None
    email: str


class VacancyCreate(BaseModel):
    title: str
    apply_url: str
    recruiter_id: Optional[str] = None
    valid_days: int = 30


class PassportStatus(BaseModel):
    passport_id: str
    status: str  # valid | expired | revoked | unknown | bad_signature
    employer: Optional[str] = None
    recruiter: Optional[str] = None
    vacancy: Optional[str] = None
    apply_url: Optional[str] = None
    expires_at: Optional[datetime] = None
    checked_at: datetime
