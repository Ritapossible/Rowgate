---
name: rowgate
description: Check a release branch against the signed API contract workbook (contract/api-contract.xlsx), cite every broken cell, and write one failing contract test per broken cell. Use when asked to run Rowgate, gate a release against the contract, or check a branch against the spreadsheet.
---

# Rowgate

You check a release branch against the **signed contract workbook** and turn each broken
row into a failing test. You cite cells, not opinions. A human decides what happens next.

Scripts do the mechanics. You do the reading and the judgment. Keep token use low: read the
diff and the workbook, not the whole repository.

## Inputs

- Branch under review: the current branch (normally `feature/fast-checkout`), base `main`.
- Workbook: `contract/api-contract.xlsx`. Read it with `office_read`.
- Diff: `out/diff.patch`, written by `scripts/collect_diff.sh`.

## Procedure

### 1. Collect (script, no reasoning)

```bash
scripts/collect_diff.sh
```

Read `out/changed_files.txt`, then `out/diff.patch`. Do not open unchanged files unless a
finding needs one.

### 2. Read the workbook

Use `office_read` on `contract/api-contract.xlsx`. Workbook rules:

- Only rows whose **Contract status** is `ACTIVE` are enforced. Rows marked `PLANNED` or
  `DEPRECATED` are informational. **Never flag them.** (On the Errors sheet, PLANNED is in the
  Notes column.)
- `↳ ORD-011` in a cell means the value is **inherited** from rule ORD-011. The status code
  for every `POST /orders` field row is the one in the ORD-011 row.
- On Billing, the HTTP status is **one merged cell** (`D3:D9`) that applies to rows 3–9.
- Every error response must use the envelope on the **Errors** sheet:
  `{"error": "<code>", "error_description": "<text>"}`. FastAPI's default `{"detail": ...}` breaks it.
- A cell address is `Sheet!<column><row>`, for example `Orders!C14`.

### Which cell to cite

Cite the cell that **states the rule being broken**, not the row's bookkeeping columns.
This applies to findings and to `skipped` entries alike.

| What broke | Cite | Example |
| --- | --- | --- |
| An HTTP status | the **HTTP status** cell (Orders C, Billing D, Auth E) | `Orders!C14` |
| A field missing, renamed or retyped | the **Field** cell (Orders D, Billing E) | `Billing!E9` |
| A value outside an allowed set | the **Type** cell holding that set (Orders E, Billing F) | `Orders!E5` |
| An error body shape | the **Body (exact shape)** cell on Errors (column D) | `Errors!D6` |

**Never cite the Contract status column** (Orders H, Billing H, Auth G). Those cells say
`ACTIVE` or `PLANNED`; they are not the rule. Never cite the Scenario or Endpoint column
either. Put supporting rows in `related_cells`, for example an Auth status break whose body
shape lives on Errors: `"cell": "Auth!E5", "related_cells": ["Errors!D6"]`.

### 3. Plan (Plan mode; stop for approval)

Map each changed file to the contract rows it can affect. List, per resource, the rows you
will check and why. **Wait for the human to approve the plan** before writing anything.

### 4. Check each resource in parallel

Spawn one subagent per resource, each with only its sheet(s) and its changed file(s):

| Subagent | Sheets | Files |
| --- | --- | --- |
| orders | Orders | `app/orders.py`, `app/models.py` |
| billing | Billing | `app/billing.py`, `app/models.py` |
| auth | Auth, Errors | `app/auth.py`, `app/errors.py` |

Each subagent returns, for every ACTIVE row it checked: cell, rule ID, verdict
(`BREAK` or `HOLDS`), the file and **line number in the branch version**, and one sentence why.

**Before calling a rename a break, check what goes on the wire.** A field renamed in Python
but kept on the wire with `Field(serialization_alias="...")` (or `alias=`) still satisfies
the contract. Report it as `HOLDS` with that reason; it belongs under `skipped`.

### 5. Write the failing tests (Agent mode)

For each `BREAK`, write exactly one test file:

- Path: `tests/contract/test_<sheet>_<cell>_<what>.py`, sheet in lower case, cell as written,
  for example `tests/contract/test_orders_C14_create_returns_201.py`.
- Start from `.bob/skills/rowgate/test_template.py`. Use the `client` fixture from
  `tests/conftest.py`. One assertion block per contract row. Put the cell and rule in the
  docstring.
- Assert what the **contract** says, not what the code does.

Then run (script):

```bash
scripts/run_contract_tests.sh before
```

Every new test must **fail** on the branch. If one passes, your citation is wrong: fix or
drop the finding. Do not continue until each finding has a red test.

### 6. Write `out/findings.json`

Follow `rowgate/findings.schema.json` exactly. Rules:

- One entry per `BREAK`; `decision` is `"pending"`.
- `evidence` is `{"file": ..., "line": ...}`. **Do not quote code**; the renderer cuts the
  excerpt from the diff.
- Use `related_cells` for referenced rows (for example the Errors row an Auth rule points to).
- Every lookalike you checked and cleared goes in `skipped` with `cell`, `change`, `why` and
  `evidence`.

Then render (script) and show the human the summary:

```bash
python scripts/render_dossier.py
```

### 7. Decide (human gate)

Ask, per finding: **fix code**, **record breaking change**, or **reject**. Do nothing until
answered.

- **fix code**: make the smallest change in `app/` that makes that test pass. Touch nothing
  else. Set `decision` to `"fix_code"` and `decided_by`.
- **record breaking change**: with `office_edit`, set that row's `Contract status` cell to
  `BREAKING`, and add a row on the `Changelog` sheet at the next empty row: **today's real
  date**, written as a `YYYY-MM-DD` string like the rows above it (do not copy the date from
  the row above, and do not write a date value); version `v3.3`; the cell; the change; the
  decision `breaking, accepted`; and in `Approved by` the **person** who decided, the same
  name you put in `decided_by` (never a branch name). Set `decision` to `"record_breaking"`
  and `workbook_edit` to the cells you changed and the Changelog row number.
- **reject**: delete that test file, set `decision` to `"reject"`.

Never change product code without a `fix code` decision for that finding.

### 8. Measure and publish (scripts)

```bash
scripts/run_contract_tests.sh after
python scripts/render_dossier.py
python scripts/export_site.py
```

`render_dossier.py` must report **0 problems**. If it lists any, fix the finding it names.
Report the counts to the human: breaks found, red before, green after, recorded, skipped.

## Never

- Flag a PLANNED or DEPRECATED row.
- Quote code in `findings.json` or claim a test result; scripts measure both.
- Edit `main`, the `demo/start` branch, or any file outside `app/`, `tests/contract/`,
  `out/` and (for recorded breaking changes only) `contract/api-contract.xlsx`.
- Describe Rowgate as anything other than the Contract Gate mode and this Skill.
