"""Settings read from environment variables (see .env.example)."""
import os


class Settings:
    hash_key: str = os.environ.get("JOBSHIELD_HASH_KEY", "dev-only-change-me")
    signing_seed_b64: str = os.environ.get("JOBSHIELD_SIGNING_SEED", "")
    public_url: str = os.environ.get("JOBSHIELD_PUBLIC_URL", "http://localhost:5173")
    passport_days: int = int(os.environ.get("JOBSHIELD_PASSPORT_DAYS", "30"))
    high_risk_threshold: int = 60


settings = Settings()
