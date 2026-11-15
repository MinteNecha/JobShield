"""Applicant Data Shield: tells the user what is safe to share at each stage."""
STAGES = {
    "application": {"safe": ["CV", "portfolio links"], "not_yet": ["ID copy", "bank details", "OTP or PIN"]},
    "interview": {"safe": ["CV", "references", "qualifications"], "not_yet": ["ID copy", "bank details", "OTP or PIN"]},
    "written_offer": {"safe": ["ID copy (to the verified employer only)"], "not_yet": ["OTP or PIN"]},
    "signed_contract": {"safe": ["bank details (to the verified employer only)"], "not_yet": ["OTP or PIN"]},
}


def guidance(stage: str) -> dict:
    return STAGES.get(stage, STAGES["application"])
