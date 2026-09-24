from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Settings:
    database_path: Path = Path(os.getenv("DATABASE_PATH", "./data/jobs.db"))
    poll_seconds: int = max(300, int(os.getenv("POLL_SECONDS", "1800")))
    min_score: int = min(100, max(0, int(os.getenv("MIN_SCORE", "55"))))
    max_job_age_days: int = max(1, int(os.getenv("MAX_JOB_AGE_DAYS", "14")))
    auto_submit: bool = os.getenv("AUTO_SUBMIT", "false").strip().lower() == "true"

settings = Settings()

if settings.auto_submit:
    raise RuntimeError(
        "AUTO_SUBMIT=true is intentionally blocked in v1. "
        "Applications require explicit human review."
    )
