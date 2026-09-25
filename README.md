<img src="web/public/logo.svg" width="72" alt="Rowgate logo: an arch gate with a spreadsheet row through it and one amber cell">

# Rowgate

Rowgate checks a release branch against the **signed API contract spreadsheet** and writes
the contract test that fails when a row breaks. Every finding cites a cell (`Orders!C14`).
A human decides what happens next.

Built with IBM Bob for the IBM Bob 2.0 Hackathon (lablab.ai, 25–27 Sep 2026).

**Live:** [rowgate.vercel.app](https://rowgate.vercel.app) · [Run results](https://rowgate.vercel.app/run) ·
[Contract explorer](https://rowgate.vercel.app/contract?cell=Orders!C14) · [Docs](https://rowgate.vercel.app/docs) ·
Bob session reports in [`bob_sessions/`](bob_sessions/)

## How it runs in IBM Bob

Rowgate is a **Contract Gate custom mode** and a **Rowgate Skill** (`.bob/skills/rowgate/SKILL.md`),
started with `/rowgate`:

1. `scripts/collect_diff.sh` captures the branch diff (script, no tokens).
2. Bob reads `contract/api-contract.xlsx` with **office_read**: merged cells, inherited rules, a shared Errors sheet, PLANNED rows it must ignore.
3. **Plan mode** maps the diff to contract rows; you approve.
4. **Three parallel subagents** check orders, billing and auth.
5. **Agent mode** writes one failing test per broken cell, named after the cell.
6. You decide per finding: fix the code, or record a breaking change, which Bob writes into the workbook with **office_edit**.
7. Scripts measure and publish: pytest before/after, the dossier, the website.

Step by step, with the expected result: [`RUNBOOK.md`](RUNBOOK.md).

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
| `scripts/export_site.py` | Exports contract, PR and run data for the web app (no model) |
| `web/` | The web app deployed on Vercel |
| `.bob/skills/rowgate/` | The Rowgate Skill and a contract-test template |
| `rowgate/bob/` | Contract Gate mode and `/rowgate` command definitions |
| `scripts/publish_run.sh` | Publishes a finished run and its session reports to the site |
| `scripts/check_submission.sh` | Pre-submission check (session reports, no credentials, run published) |
| `bob_sessions/` | Screenshots of every Bob task summary |

Design: [ARCHITECTURE.md](ARCHITECTURE.md) · Plan: [PLAN.md](PLAN.md) · Decisions and facts: [MEMORY.md](MEMORY.md)

## Web app (Vercel)

`web/` is a static Vite + React site with three pages: **Overview**, **Run** (the latest
Rowgate run, measured) and **Contract** (the signed workbook, with deep links such as
`/contract?cell=Orders!C14`). It reads JSON from `web/public/data/`, written by
`scripts/export_site.py`, so Vercel needs no Python and no server.

Deploy: on vercel.com, **Add New → Project**, import `Ritapossible/Rowgate`, set
**Root Directory** to `web`, keep the detected Vite settings, **Deploy**. Every push to
`main` redeploys.

Publish a run: after a Rowgate run, `python scripts/export_site.py`, then commit
`web/public/data/` and `web/public/dossier.html`.

```bash
cd web && npm install && npm run dev      # http://localhost:5173
```

## Run the demo service locally

```bash
python -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
python -m pytest -q                      # smoke + renderer tests
uvicorn app.main:app --reload            # http://127.0.0.1:8000/docs
```

## License

MIT
