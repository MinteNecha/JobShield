from fastapi.testclient import TestClient

from app.main import app

c = TestClient(app)
KEY = {"X-API-Key": "dev-key-demo-employer-1"}


def test_full_passport_flow_and_revocation():
    rec = c.post("/v1/employer/recruiters", json={"name": "Sam", "email": "sam@demosoftware.example"}, headers=KEY).json()
    v = c.post("/v1/employer/vacancies", headers=KEY, json={
        "title": "Junior Developer", "apply_url": "https://demosoftware.example/careers/1",
        "recruiter_id": rec["id"]}).json()
    st = c.get(f"/v1/passport/{v['passport_id']}").json()
    assert st["status"] == "valid" and st["employer"] == "Demo Software (Pty) Ltd"
    assert c.post("/v1/check", json={"passport_id": v["passport_id"]}).json()["rating"] == "verified"
    assert c.post(f"/v1/passport/{v['passport_id']}/revoke", headers=KEY).status_code == 200
    assert c.get(f"/v1/passport/{v['passport_id']}").json()["status"] == "revoked"


def test_employer_endpoints_need_key():
    assert c.post("/v1/employer/vacancies", json={"title": "x", "apply_url": "y"}).status_code == 401


def test_check_scam_message():
    r = c.post("/v1/check", json={"message": "Pay a R250 registration fee to start"}).json()
    assert r["rating"] == "high_risk"
