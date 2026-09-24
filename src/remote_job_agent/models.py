from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from hashlib import sha256
import re

def utcnow_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def norm(value: str | None) -> str:
    value = value or ""
    value = re.sub(r"\s+", " ", value).strip().lower()
    return value

@dataclass(slots=True)
class Job:
    source: str
    source_id: str
    company: str
    title: str
    url: str
    description: str = ""
    location: str = ""
    salary: str = ""
    tags: list[str] = field(default_factory=list)
    published_at: str = ""
    discovered_at: str = field(default_factory=utcnow_iso)
    eligibility: str = "UNKNOWN"
    score: int = 0
    status: str = "DISCOVERED"
    reason: str = ""

    @property
    def fingerprint(self) -> str:
        raw = "|".join([
            norm(self.company),
            norm(self.title),
            norm(self.location),
            norm(self.url).split("?")[0],
        ])
        return sha256(raw.encode("utf-8")).hexdigest()
