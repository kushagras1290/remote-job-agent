from __future__ import annotations

import json
import os
from dataclasses import asdict
from typing import Iterable

from .models import Job


class FirebaseConfigError(RuntimeError):
    """Raised when Firebase persistence is enabled but credentials are missing."""


def _client():
    """Create a Firestore client lazily so local discovery works without Firebase."""
    try:
        import firebase_admin
        from firebase_admin import credentials, firestore
    except ImportError as exc:
        raise FirebaseConfigError(
            "Firebase support requires the 'firebase' optional dependency: "
            "pip install -e '.[firebase]'"
        ) from exc

    if not firebase_admin._apps:
        raw = os.getenv("FIREBASE_SERVICE_ACCOUNT_JSON", "").strip()
        if not raw:
            raise FirebaseConfigError("FIREBASE_SERVICE_ACCOUNT_JSON is not configured")
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise FirebaseConfigError("FIREBASE_SERVICE_ACCOUNT_JSON is invalid JSON") from exc
        firebase_admin.initialize_app(credentials.Certificate(payload))

    return firestore.client()


def upsert_jobs(jobs: Iterable[Job], collection: str = "jobs") -> int:
    """Idempotently persist jobs keyed by their stable fingerprint."""
    db = _client()
    count = 0
    batch = db.batch()

    for job in jobs:
        ref = db.collection(collection).document(job.fingerprint)
        payload = asdict(job)
        payload["fingerprint"] = job.fingerprint
        batch.set(ref, payload, merge=True)
        count += 1

        # Firestore batches support at most 500 writes; leave headroom.
        if count % 450 == 0:
            batch.commit()
            batch = db.batch()

    if count % 450:
        batch.commit()
    return count
