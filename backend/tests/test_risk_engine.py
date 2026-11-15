from app.schemas import CheckRequest
from app.services.risk_engine import RiskEngine
from app.services.scamtrace import ScamTrace, hash_identifier

SCAM = ("Congratulations! You are shortlisted for a junior developer job at R22 000. "
        "Pay the R250 onboarding fee today and send a copy of your ID.")


def test_payment_request_is_high_risk():
    res = RiskEngine(ScamTrace()).assess(CheckRequest(message=SCAM))
    assert res.rating == "high_risk"
    assert "PAYMENT_REQUEST" in {r.id for r in res.reasons}


def test_clean_message_is_never_verified():
    res = RiskEngine(ScamTrace()).assess(CheckRequest(message="We are hiring a developer. Apply on our website."))
    assert res.rating == "unverified"


def test_overseas_offer_raises_trafficking_alert():
    res = RiskEngine(ScamTrace()).assess(CheckRequest(message="Great jobs in Dubai, ticket will be paid"))
    assert res.trafficking_alert


def test_scamtrace_links_reports_and_flags_number():
    st = ScamTrace()
    h = hash_identifier("phone", "082 123 4567")
    st.add_report({h})
    st.add_report({h, hash_identifier("url", "http://fake-jobs.example/apply")})
    assert st.matches({hash_identifier("phone", "+27821234567")}) == 2
    res = RiskEngine(st).assess(CheckRequest(message="Call 082 123 4567 about the job"))
    assert "SCAMTRACE_HIT" in {r.id for r in res.reasons}
