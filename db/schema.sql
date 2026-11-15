-- PostgreSQL schema for the production version (the prototype uses an in-memory store).
CREATE TABLE employers (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  registration_number TEXT NOT NULL UNIQUE,
  status TEXT NOT NULL,
  verified_at TIMESTAMPTZ
);
CREATE TABLE recruiters (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  employer_id UUID NOT NULL REFERENCES employers(id),
  name TEXT NOT NULL,
  agency TEXT,
  email TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'invited'
);
CREATE TABLE vacancies (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  employer_id UUID NOT NULL REFERENCES employers(id),
  recruiter_id UUID REFERENCES recruiters(id),
  title TEXT NOT NULL,
  apply_url TEXT NOT NULL,
  expires_at TIMESTAMPTZ NOT NULL,
  status TEXT NOT NULL DEFAULT 'approved'
);
CREATE TABLE passports (
  id UUID PRIMARY KEY,
  vacancy_id UUID NOT NULL REFERENCES vacancies(id),
  signature TEXT NOT NULL,
  issued_at TIMESTAMPTZ NOT NULL,
  expires_at TIMESTAMPTZ NOT NULL,
  revoked BOOLEAN NOT NULL DEFAULT FALSE
);
-- No message text is stored by default.
CREATE TABLE check_log (
  id BIGSERIAL PRIMARY KEY,
  checked_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  rating TEXT NOT NULL,
  reasons TEXT[] NOT NULL DEFAULT '{}'
);
-- Identifiers are keyed hashes (HMAC-SHA256), never plain phone numbers.
CREATE TABLE scam_reports (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  reported_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  template_fingerprint TEXT
);
CREATE TABLE scam_report_identifiers (
  report_id UUID NOT NULL REFERENCES scam_reports(id),
  kind TEXT NOT NULL CHECK (kind IN ('phone','url','account')),
  hash TEXT NOT NULL,
  PRIMARY KEY (report_id, kind, hash)
);
CREATE INDEX ON scam_report_identifiers (hash);
