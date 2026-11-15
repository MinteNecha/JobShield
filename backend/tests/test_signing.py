from app.services.signing import SigningService


def test_sign_and_verify_roundtrip():
    s = SigningService()
    p = {"passport_id": "abc", "vacancy_id": "v1"}
    assert s.verify(p, s.sign(p))


def test_tampered_payload_fails():
    s = SigningService()
    p = {"passport_id": "abc", "vacancy_id": "v1"}
    sig = s.sign(p)
    assert not s.verify({**p, "vacancy_id": "v2"}, sig)
