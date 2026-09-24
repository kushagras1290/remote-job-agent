# Remote Job Agent — zero-cost/local-first

A continuously running Python service for remote-job discovery, India eligibility filtering,
deduplication, ranking, application preparation, and tracking.

## Cost guardrails

This build deliberately has **no paid API dependency**.

- No OpenAI API key
- No paid database
- No paid scheduler
- No paid hosting provisioned
- No automatic job submission
- SQLite persistence
- Deterministic ranking by default
- Optional local Ollama integration can be added later without changing the data model

The service therefore costs **₹0 in software/API usage** while it runs on hardware you already own.
If you later deploy to a cloud provider, the cloud provider's own pricing/free-tier rules apply.

## Sources in v1

Adapters are isolated so one source failing does not stop the pipeline.

- Remote OK JSON API
- Remotive public API
- We Work Remotely RSS
- Himalayas public API

Other boards can be added as adapters only when their access method is reliable and permitted.

## Pipeline

```text
sources
  -> normalize
  -> fingerprint/deduplicate
  -> India eligibility
  -> deterministic relevance score
  -> SQLite
  -> approval queue
```

The application stage intentionally stops at `READY_FOR_REVIEW`. A browser/application adapter
must never submit without an explicit user action.

## Quick start

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -e .
copy .env.example .env   # Windows
# cp .env.example .env   # macOS/Linux

remote-job-agent init-db
remote-job-agent run-once
remote-job-agent status
remote-job-agent daemon
```

Stop the daemon with Ctrl+C.

## Search profile

Edit `src/remote_job_agent/profile.py` to tune roles and skills. The default profile is aimed at
AI/ML/GenAI/Python engineering roles and rejects obvious US/EU-only jobs before scoring.

## Safety

- `AUTO_SUBMIT=false` is enforced.
- Salary/legal/work-authorization questions are never guessed.
- No credentials are committed.
- Network failures are isolated per source.
- Deduplication is idempotent.
