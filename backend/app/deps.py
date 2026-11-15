from fastapi import Header, HTTPException

from . import store
from .config import settings
from .services.risk_engine import RiskEngine
from .services.scamtrace import ScamTrace
from .services.signing import SigningService
from .services.verification import VerificationService

scamtrace = ScamTrace()
signer = SigningService(settings.signing_seed_b64)
verification = VerificationService(signer)
risk = RiskEngine(scamtrace)


def current_employer(x_api_key: str = Header(default="")) -> dict:
    """Prototype auth. TODO: employer sign-in with multi-factor authentication."""
    employer = store.employer_by_key(x_api_key)
    if not employer:
        raise HTTPException(status_code=401, detail="Invalid or missing X-API-Key")
    return employer
