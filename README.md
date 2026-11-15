# JobShield

> Verify South African job offers before you apply: employer, recruiter and vacancy checks, signed passports and scam linking.

JobShield is a recruitment trust and verification layer for South Africa. Scammers copy real company names, so a job that *looks* legitimate proves nothing. JobShield checks three things:

1. **Is the employer real?** (company record)
2. **Is the recruiter allowed?** (invited by the employer)
3. **Is the vacancy approved?** (approved by the employer, with an official apply link)

When all three pass, the employer gets a signed, expiring, revocable **Verified Vacancy Passport** (a QR code or link). Job seekers can also paste or forward a job message and get a rating (**Verified, Unverified, High risk**) with reasons and evidence. **SCAMTRACE** links scam reports that share a phone number, account or website.

JobShield gives evidence-backed risk assessment. **It never guarantees that a job is genuine.** If a source cannot be reached, it says "could not verify", never "verified".

Built by **Team Nikolaos** for the NEMISA Digital Innovation Discothon 2026 (Youth Employment and Digital Entrepreneurship, with a cybersecurity angle).

## Status: prototype skeleton

| Area | State |
| --- | --- |
| Risk engine (transparent rules) | Working, with tests |
| Passport signing (Ed25519), verify, revoke | Working, with tests |
| SCAMTRACE (keyed hashes, linked reports) | Working in memory |
| Data Shield (what is safe to share, by stage) | Working |
| Web app (check, verify, employer demo) | Working skeleton |
| CIPC and agency register | **Simulated** demo data. Real access needs approval |
| ML model and AI explanations | TODO (see `risk_engine.py`) |
| WhatsApp Business API bot | TODO (webhook stub) |
| PostgreSQL storage | TODO (schema in `db/schema.sql`) |
| Employer sign-in with MFA, rate limiting | TODO |

All data in this repo is simulated. Do not commit real scam messages, personal data or keys.

## Project layout

```
backend/            FastAPI service
  app/api/          REST routes (/v1/check, /v1/passport, /v1/report, /v1/employer/...)
  app/services/     risk_engine, signing, scamtrace, verification, data_shield, cipc (simulated)
  app/data/         SIMULATED demo dataset
  tests/            pytest
frontend/           React + Vite web app
db/schema.sql       PostgreSQL schema for the production version
docs/
  submission/       Technical architecture and campaign story (LaTeX, for Overleaf)
  ssdlc.md          Secure development lifecycle checklist
  threat-model.md   STRIDE threat table
.github/workflows/  CI (backend tests, frontend build)
```

## Run it

Backend (Python 3.12):

```bash
cd backend
pip install -r requirements.txt
pytest -q
uvicorn app.main:app --reload      # http://localhost:8000/docs
```

Frontend (Node 20):

```bash
cd frontend
npm install
npm run dev                         # http://localhost:5173
```

Try the demo employer key `dev-key-demo-employer-1` in the Employers tab (simulated, development only).

Copy `.env.example` to `.env` and set your own keys. Never commit `.env`.

## API at a glance

| Endpoint | Caller | Purpose |
| --- | --- | --- |
| `POST /v1/check` | Job seeker | Rating with reasons for a message, or verify by `passport_id` |
| `GET /v1/passport/{id}` | Anyone | Signature, expiry and revocation check |
| `POST /v1/report` | Job seeker | Report a scam (stored as keyed hashes) |
| `POST /v1/employer/recruiters` | Employer | Invite a recruiter |
| `POST /v1/employer/vacancies` | Employer | Approve a vacancy and issue a passport |
| `POST /v1/passport/{id}/revoke` | Employer | Revoke instantly |
| `GET /v1/shield/{stage}` | Job seeker | What is safe to share at this stage |

## Security and privacy principles

- Collect the minimum. No message text and no ID copies are stored by default.
- Scam identifiers are stored only as keyed hashes (HMAC-SHA256).
- Passports are signed with Ed25519; the private key belongs in a managed vault, not in the repo.
- Clear rules decide. Machine learning supports them. AI only explains and never decides.
- Built with POPIA, the Employment Services Act and the Cybercrimes Act in mind. See `docs/ssdlc.md`.

## Roadmap

1. Discothon weekend: clickable prototype on a labelled demo dataset.
2. Months 1 to 3: UJ pilot, WhatsApp bot, about 10 pilot employers, penetration test.
3. Months 4 to 9: TVET colleges, employer dashboard, real CIPC and agency integrations once approved.
4. Months 10 to 12: scale and a scam-intelligence API for partners (year 2).

## Team

Amar Mustafa (frontend, backend, marketing) · Mintesinot Necha (backend infrastructure, project overview, business requirements) · Keamogetse Maremela (AI, data and finance)
