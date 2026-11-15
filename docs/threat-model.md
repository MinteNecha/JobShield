# Threat model (STRIDE)

| Threat | STRIDE | Control | Status |
| --- | --- | --- | --- |
| Fake employer signs up | Spoofing | Company record match, independent confirmation, manual review | Simulated lookup only |
| Stolen employer login | Spoofing, Elevation | Multi-factor sign-in, signed approvals, alerts on new devices | TODO (API key in prototype) |
| Forged or copied QR | Tampering | Ed25519 signatures, expiry, instant revocation, link-based verification | Done |
| Leak of applicant data | Information disclosure | Minimum data, encryption, no ID copies, no message text stored | Partly (design) |
| False or abusive reports | Tampering, Repudiation | Evidence thresholds, rate limits, audit log, appeal route | TODO |
| Flooding the WhatsApp number | Denial of service | Per-number rate limits, queueing, cached official data | TODO |
| Prompt injection via forwarded text | Tampering | AI only explains and never decides; input treated as untrusted | Design |
| Insider misuse | Elevation, Repudiation | Least privilege, separate signing keys, append-only audit log | TODO |
