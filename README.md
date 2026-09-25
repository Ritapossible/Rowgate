# Rowgate

Rowgate checks a release branch against the **signed API contract spreadsheet** and writes
the contract test that fails when a row breaks. Every finding cites a cell (`Orders!C14`).
A human decides what happens next.

Built for the IBM Bob 2.0 Hackathon (lablab.ai, 25–27 Sep 2026). Status: in progress.

## Why

Pull request review sees the diff. The contract a partner signed is an `.xlsx` that never
enters the PR, so a status code or a required field changes while the review still looks
clean. Bob reads the signed spreadsheet once and writes tests that stay in the repo; every
later PR is then checked by pytest, with no model in the loop.

## What's in the repo

| Path | What |
| --- | --- |
| `app/` | Demo service (Kora Partner API, FastAPI): orders, billing, auth |
| `contract/api-contract.xlsx` | The signed contract: 6 sheets, 41 rules. Built by `scripts/build_contract.py` |
| `scripts/collect_diff.sh` | Captures the branch diff into `out/` (no model) |
| `scripts/run_contract_tests.sh` | Runs `tests/contract/`, saves a JSON report (no model) |
| `scripts/render_dossier.py` | Turns Bob's `out/findings.json` into `out/dossier.html` (no model) |
| `rowgate/findings.schema.json` | The format Bob must write |
| `tests/contract/` | Contract tests written by Rowgate, named after the cell they check |
| `bob_sessions/` | Screenshots of every Bob task summary |

Design: [ARCHITECTURE.md](ARCHITECTURE.md) · Plan: [PLAN.md](PLAN.md) · Decisions and facts: [MEMORY.md](MEMORY.md)

## Run the demo service locally

```bash
python -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
python -m pytest -q                      # smoke + renderer tests
uvicorn app.main:app --reload            # http://127.0.0.1:8000/docs
```

## License

MIT
