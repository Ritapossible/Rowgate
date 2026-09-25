# lablab.ai submission: paste-ready

Fill **[N]** from `python scripts/run_numbers.py` and **[B]** from `submission/BASELINE.md`.
Run `scripts/check_submission.sh` before you press Submit.

## Project title

Rowgate

## Short description (one or two sentences)

Rowgate checks a release branch against the signed API contract spreadsheet and writes the
contract test that fails when a row breaks. Every finding cites a cell, and a human decides
what ships.

## Long description

Pull request review sees the diff. The API contract a partner signed is a spreadsheet that
never enters that diff, so a status code or a required field changes while the review still
looks clean. Partner integrations in banking, telco and insurance are signed exactly this way,
and they rarely become OpenAPI.

Rowgate runs inside IBM Bob as a Contract Gate custom mode and a Rowgate Skill, started with
`/rowgate`. Bob reads the workbook directly with `office_read`, including merged cells,
inherited rules, a shared error sheet and rows that are only planned. In Plan mode it maps the
diff to contract rows and waits for approval. Three parallel subagents check orders, billing
and auth, each in its own context. In Agent mode Bob writes one contract test per broken cell,
named after the cell, and every test must fail on the branch, so a wrong citation cannot
survive. A human then decides per finding: fix the code, or record a breaking change, which Bob
writes back into the signed workbook with `office_edit`.

Everything in the result is measured rather than claimed: code excerpts are cut from the diff,
pass and fail come from pytest, and workbook edits are compared against git. The tests stay in
the repository, so every later pull request is checked by plain pytest in CI, with no model and
no tokens.

On a sample partner API with three planted breaks and one harmless rename, reading the diff
found [B] of 3 and flagged the rename. Rowgate found [N] of 3, skipped the rename with the
reason (the wire name is unchanged), and proved each break with a failing test.

## Technologies / tags

IBM Bob, Bob custom modes, Bob Skills, subagents, Plan mode, Agent mode, office_read,
office_edit, Python, FastAPI, pytest, openpyxl, React, Vite, Vercel

## Links

- Demo: https://rowgate.vercel.app
- Run results: https://rowgate.vercel.app/run
- Repository (MIT): https://github.com/Ritapossible/Rowgate
- Bob session reports: https://github.com/Ritapossible/Rowgate/tree/main/bob_sessions
- Video: [paste the link after upload]
- Slides: [upload the PDF exported from submission/SLIDES.md]
- Cover image: `web/public/og.png` (1200 × 630)

## Category / use case

Release readiness and testing: the part of code review that misses what the diff doesn't show.
