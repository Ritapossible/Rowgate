# What Bob produced in the run of record

These are the artifacts of the Rowgate run on `feature/fast-checkout`, copied here by
`scripts/publish_run.sh` so they are on `main` where anyone browsing the repo will find them.

| File | What it is |
| --- | --- |
| `findings.json` | Bob's own output: one entry per broken ACTIVE row, with the cell it cites, the verdict, the reasoning, the test it wrote, and the human's decision. Everything else in the run is rendered from this. |
| `test_*.py` | The contract tests Bob wrote, one per broken cell, each named after the cell it enforces. |

**These are copies.** The live tests run from `tests/contract/` on `feature/fast-checkout`,
where CI executes them against the branch: three pass after the approved fixes, and
`test_billing_E9_invoice_has_currency.py` stays red because the human recorded that row as a
breaking change instead of fixing it. That red test is the gate holding the release.

The rendered view of the same run is `web/public/dossier.html`, and the site reads
`web/public/data/run.json`. The Bob task transcripts are in `bob_sessions/`.
