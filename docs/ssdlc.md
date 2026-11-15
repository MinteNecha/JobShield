# Secure System Development Lifecycle (SSDLC)

Our lifecycle follows the NIST Secure Software Development Framework (SP 800-218). This is the working checklist for the repo.

| Phase | What we do | Where it lives |
| --- | --- | --- |
| 1. Plan and assess risk | Identify what we protect (applicant data, signing keys, employer accounts) and legal duties (POPIA, Employment Services Act, Cybercrimes Act) | `docs/threat-model.md` |
| 2. Design and threat model | STRIDE per component, security requirements from OWASP ASVS | `docs/threat-model.md`, architecture document |
| 3. Build securely | Code review on every pull request, no secrets in git, typed schemas, parameterised queries once PostgreSQL is added | `.gitignore`, `.env.example`, `schemas.py` |
| 4. Test | Unit tests for rules and signing, OWASP ZAP scan in the pipeline, external penetration test before the pilot goes public | `backend/tests`, CI |
| 5. Release | Separate test and production, infrastructure as code, keys in a managed vault | `docker-compose.yml` |
| 6. Operate and respond | Monitoring, backups with tested restores, incident plan including notifying the Information Regulator when required | TODO |

## Pull request checklist
- [ ] Tests added or updated and passing
- [ ] No secrets, real personal data or real scam messages committed
- [ ] New input is validated
- [ ] New data collected is justified, minimal and documented
- [ ] Rating logic still fails safe ("could not verify", never "verified")
