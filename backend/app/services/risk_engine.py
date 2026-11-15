"""Risk engine: transparent rules first. ML and AI only support the rules.

Rating logic
- verified   : only when a valid, unexpired, unrevoked passport matches (see verification.py)
- high_risk  : a hard rule fires, or the combined score reaches the threshold
- unverified : everything else (we never say "verified" without proof)
"""
import re
from dataclasses import dataclass
from datetime import datetime, timezone

from ..config import settings
from ..schemas import CheckRequest, CheckResponse, Evidence, Reason
from .scamtrace import ScamTrace, hash_identifier

FREE_MAIL = {"gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "icloud.com", "live.com"}
PHONE_RE = re.compile(r"(?:\+27|0)\d[\d\s\-]{7,12}\d")
URL_RE = re.compile(r"https?://[^\s]+", re.I)


@dataclass(frozen=True)
class Rule:
    id: str
    text: str
    pattern: str
    weight: int
    hard: bool = False


RULES = [
    Rule("PAYMENT_REQUEST", "It asks you to pay money. Real jobs never charge you.",
         r"(onboarding|registration|admin|administration|training|application|processing|uniform|vetting)\s+fee"
         r"|\bpay\s+(a|an|the)?\s*(r\s?\d[\d,\.]*|fee|deposit)|\bdeposit\b|\bsend\s+(r\s?\d[\d,\.]*|money)"
         r"|\br\s?\d[\d,\.]*\s+(fee|deposit)", 60, hard=True),
    Rule("ID_OR_BANK_REQUEST", "It asks for your ID or bank details before any interview or offer.",
         r"copy of (your )?(id|identity)|id (copy|document|number)|certified copy"
         r"|bank(ing)? (details|statement|card)|account number|\botp\b|\bpin\b", 35),
    Rule("URGENCY", "It pushes you to decide quickly.",
         r"\burgent(ly)?\b|immediately|today only|within 24 hours|act now|limited slots|last chance", 10),
    Rule("SHORT_LINK", "It uses a shortened link that hides where it goes.",
         r"bit\.ly|tinyurl\.com|cutt\.ly|rb\.gy|t\.co/", 15),
    Rule("OVERSEAS_OFFER", "It offers work overseas. This is a common trafficking lure.",
         r"dubai|abroad|overseas|saudi|qatar|visa sponsorship|work visa|ticket will be paid"
         r"|relocation package|thailand|cyprus", 25),
    Rule("WHATSAPP_ONLY", "It only uses WhatsApp for hiring.",
         r"whatsapp (us|me|only)|contact us on whatsapp|apply via whatsapp", 10),
    Rule("GUARANTEED", "It promises a guaranteed job or income.",
         r"guaranteed\s+(job|income|salary|placement)", 20),
]

ADVICE = [
    "Never pay to get a job. The Employment Services Act bans fees for work seekers.",
    "Share your CV first. Share your ID only after a written offer.",
    "Ask the recruiter for a Verified Vacancy Passport or confirm the vacancy on the employer's official website.",
]


class RiskEngine:
    def __init__(self, scamtrace: ScamTrace):
        self.scamtrace = scamtrace

    def ml_score(self, text: str) -> int | None:
        """TODO (Kea): small scikit-learn classifier + text similarity to known scam templates.
        Must only support the rules and never override a hard rule."""
        return None

    def assess(self, req: CheckRequest) -> CheckResponse:
        now = datetime.now(timezone.utc)
        text = req.message or ""
        reasons: list[Reason] = []
        evidence: list[Evidence] = []
        trafficking = False
        hard = False

        for rule in RULES:
            if re.search(rule.pattern, text, re.I):
                reasons.append(Reason(id=rule.id, text=rule.text, weight=rule.weight))
                hard = hard or rule.hard
                trafficking = trafficking or rule.id == "OVERSEAS_OFFER"

        if req.sender_email:
            domain = req.sender_email.split("@")[-1].lower()
            if domain in FREE_MAIL:
                reasons.append(Reason(id="FREE_EMAIL", weight=15,
                                      text="The sender uses a free email address, not a company address."))

        hashes = set()
        for p in ([req.phone] if req.phone else []) + PHONE_RE.findall(text):
            hashes.add(hash_identifier("phone", p))
        for u in ([req.url] if req.url else []) + URL_RE.findall(text):
            hashes.add(hash_identifier("url", u))
        if hashes:
            n = self.scamtrace.matches(hashes)
            evidence.append(Evidence(source="SCAMTRACE", checked_at=now,
                                     result=f"{n} earlier scam report(s) share an identifier" if n else "no earlier reports"))
            if n:
                reasons.append(Reason(id="SCAMTRACE_HIT", weight=40,
                                      text=f"A number or link in this message appears in {n} earlier scam report(s)."))

        score = min(100, sum(r.weight for r in reasons))
        rating = "high_risk" if hard or score >= settings.high_risk_threshold else "unverified"
        advice = list(ADVICE)
        if trafficking:
            advice.insert(0, "Overseas job offers can be trafficking lures. Do not travel or pay. Get help: National Human Trafficking Hotline, 0800 222 777.")
        if not reasons:
            expl = "We found no red flags, but this job is not verified. Ask for proof before you apply."
        else:
            expl = " ".join(r.text for r in reasons)
        return CheckResponse(rating=rating, score=score, reasons=reasons, evidence=evidence,
                             trafficking_alert=trafficking, advice=advice, explanation=expl)
