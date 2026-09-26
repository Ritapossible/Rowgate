# What Bob produced in the run of record

These are the artifacts of the Rowgate run on `feature/fast-checkout`, copied here by
`scripts/publish_run.sh` so they are on `main` where anyone browsing the repo will find them.

| File | What it is |
| --- | --- |
| `findings.json` | Bob's own output: one entry per broken ACTIVE row, with the cell it cites, the verdict, the reasoning, the test it wrote, and the human's decision. Everything else in the run is rendered from this. |
| `test_*.py` | The contract tests Bob wrote, one per broken cell, each named after the cell it enforces. |

**These are copies.** The live tests belong in `tests/contract/` on `feature/fast-checkout`,
where CI executes them against the branch: three pass after the approved fixes, and
`test_billing_E9_invoice_has_currency.py` stays red because the human recorded that row as a
breaking change instead of fixing it. That red test is the gate holding the release.

Verify it rather than taking this file's word for it:

```bash
git ls-tree --name-only origin/feature/fast-checkout tests/contract
python scripts/check_run_artifacts.py
```

`check_run_artifacts.py` fails if any test cited by the published run is missing from the
branch, if a commit shown on the Run page is not on it, or if the run records workbook edits
the workbook does not have. It runs as part of `scripts/check_submission.sh`.

The rendered view of the same run is `web/public/dossier.html`, and the site reads
`web/public/data/run.json`. The Bob task transcripts are in `bob_sessions/`.
