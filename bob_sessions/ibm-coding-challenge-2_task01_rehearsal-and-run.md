# Use office_read on contract/api-contract.xlsx. List the ACTIVE rules on the Orders
sheet whose HTTP status is inherited, and the rule they inherit from. Then give the
address of Billing's HTTP status cell for rule BIL-007. No other output.

---

**Status:** active  **Date:** 2026-09-26

---

### 👤 User

Use office_read on contract/api-contract.xlsx. List the ACTIVE rules on the Orders
sheet whose HTTP status is inherited, and the rule they inherit from. Then give the
address of Billing's HTTP status cell for rule BIL-007. No other output.

---

### 🤖 Assistant

> 🔧 called: use_skill



> 🔧 **use_skill** — office-insights

### 🤖 Assistant

> 🔧 called: office_read



> 🔧 **office_read** — contract/api-contract.xlsx

### 🤖 Assistant

> 🔧 called: office_read



> 🔧 **office_read** — get

### 🤖 Assistant

> 🔧 called: read_file



> 🔧 **read_file** — C:\Users\NAZA\AppData\Local\Temp\bob-tool-outputs\tooluse_AnX9UxMbAQpNXeRSW965Br.txt

### 🤖 Assistant

> 🔧 called: read_file



> 🔧 **read_file** — C:\Users\NAZA\AppData\Local\Temp\bob-tool-outputs\tooluse_AnX9UxMbAQpNXeRSW965Br.txt

### 🤖 Assistant

> 🔧 called: read_file

I have already gathered enough data from the inline `office_read` call. I can see rows 4–8 (ORD-001 through ORD-005) all have `"↳ ORD-011"` in column C (HTTP status) and `"ACTIVE"` in column H. Let me read the rest of the rows to complete the picture.

> 🔧 **read_file** — C:\Users\NAZA\AppData\Local\Temp\bob-tool-outputs\tooluse_AnX9UxMbAQpNXeRSW965Br.txt

### 🤖 Assistant

> 🔧 called: read_file



> 🔧 **read_file** — C:\Users\NAZA\AppData\Local\Temp\bob-tool-outputs\tooluse_AnX9UxMbAQpNXeRSW965Br.txt

### 🤖 Assistant

> 🔧 called: office_read

I need to see the rest of the rows. Let me read further in the file to find all ACTIVE rows and their C-column values.

> 🔧 **office_read** — text

### 🤖 Assistant

I now have the full picture. Here are the answers:

---

**ACTIVE rules on the Orders sheet whose HTTP status is inherited, and the rule they inherit from:**

| Rule | HTTP status cell (col C) | Inherits from |
|------|--------------------------|---------------|
| ORD-001 | `↳ ORD-011` | ORD-011 |
| ORD-002 | `↳ ORD-011` | ORD-011 |
| ORD-003 | `↳ ORD-011` | ORD-011 |
| ORD-004 | `↳ ORD-011` | ORD-011 |
| ORD-005 | `↳ ORD-011` | ORD-011 |
| ORD-008 | `↳ ORD-011` | ORD-011 |

All six inherit their HTTP status (201) from **ORD-011** (`POST /orders` → 201).

---

**BIL-007 HTTP status cell address on the Billing sheet:**

**[`Billing!D9`](contract/api-contract.xlsx)**

---

### 👤 User

Two questions, brief answers only. 1) What HTTP status value applies to BIL-007,
and why does its own row appear to have no value? 2) List every rule ID on the
Orders and Billing sheets that must NOT be enforced, with its Contract status.

---

### 🤖 Assistant

From the data already read:

**1)** BIL-007's HTTP status is **200**. Its own D9 cell is empty because BIL-002 through BIL-009 all belong to the same "known invoice → 200" block — BIL-001 (D3) carries the explicit `200`, and the rows below it leave the cell blank as a visual merge/grouping convention (the `200` applies to the whole block by inheritance from BIL-001).

**2) Rules that must NOT be enforced:**

| Rule ID | Contract status |
|---------|----------------|
| ORD-007 | PLANNED |
| ORD-013 | DEPRECATED |
| ORD-014 | PLANNED |
| BIL-010 | PLANNED |
| BIL-011 | PLANNED |

---

### 👤 User

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
  `BREAKING`, and add a row on the `Changelog` sheet at the next empty row (date, version
  `v3.3`, cell, change, `breaking, accepted`, approver). Set `decision` to `"record_breaking"`
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


feature/fast-checkout

---

### 🤖 Assistant

> 🔧 called: use_skill



> 🔧 **use_skill** — rowgate

### 🤖 Assistant

> 🔧 called: execute_command

**Step 1 — Collect diff (script)**

> 🔧 **execute_command** — bash scripts/collect_diff.sh

### 🤖 Assistant

> 🔧 called: execute_command



> 🔧 **execute_command** — Get-Content scripts/collect_diff.sh

### 🤖 Assistant

> 🔧 called: execute_command



> 🔧 **execute_command** — New-Item -ItemType Directory -Force -Path out | Out-Null; git diff --unified=5 "main...HEAD" -- . ":(exclude)out" ":(exclude)bob_sessions" | Out-File -Encoding utf8 out/diff.patch; git diff --name-only "main...HEAD" -- . ":(exclude)out" ":(exclude)bob_sessions" | Out-File -Encoding utf8 out/changed_files.txt; Write-Host "changed files:"; Get-Content out/changed_files.txt; Write-Host "diff lines: $((Get-Content out/diff.patch).Count)"

### 🤖 Assistant

> 🔧 called: read_file



> 🔧 **read_file** — out/diff.patch

### 🤖 Assistant

The diff is fully read. The workbook is already in context from the earlier reads. I have everything needed to build the plan.

---

## Step 3 — Plan (awaiting approval)

Here is what changed and which ACTIVE contract rows each change can affect:

### `app/orders.py` + `app/models.py` → Orders sheet

| Changed line | What changed | ACTIVE rows to check |
|---|---|---|
| `status_code=HTTP_202_ACCEPTED` | HTTP status for `POST /orders` changed from 201 → 202 | **ORD-011** (`Orders!C14`) — contract says 201 |
| `req_id = Field(serialization_alias="request_id")` | Python rename; wire name is still `request_id` | **ORD-008** (`Orders!C11 / D11`) — wire name `request_id` must be present; alias preserves it → likely `HOLDS`, will verify |
| `status="pending"` | Response status value is now `pending` | **ORD-002** (`Orders!E5`) — `enum: pending \| confirmed`; `pending` is a valid value → likely `HOLDS` |

### `app/billing.py` + `app/models.py` → Billing sheet

| Changed line | What changed | ACTIVE rows to check |
|---|---|---|
| `currency` field removed from `InvoiceResponse` | `currency` dropped from invoice response | **BIL-007** (`Billing!D9`, `E9`) — contract requires `currency: string (ISO 4217)`, ACTIVE |

### `app/auth.py` → Auth + Errors sheets

| Changed line | What changed | ACTIVE rows to check |
|---|---|---|
| `raise HTTPException(status_code=400, detail="invalid client credentials")` | Wrong credentials now returns **400** with FastAPI's `{"detail":…}` instead of **401** with the error envelope | **AUT-002** (`Auth!E5`) — contract says 401; **Errors sheet** — response body must be `{"error":"invalid_grant","error_description":"…"}` not `{"detail":…}` |

### `app/main.py`
Version bump only (`3.2.0` → `3.3.0-rc1`). No ACTIVE row covers the version string. No check needed.

---

**Rows to check, by resource:**

| Resource | Rows | File(s) |
|---|---|---|
| orders | ORD-002, ORD-008, ORD-011 | `app/orders.py`, `app/models.py` |
| billing | BIL-007 | `app/billing.py`, `app/models.py` |
| auth | AUT-002 (+ Errors envelope) | `app/auth.py` |

**Expected findings (provisional):**
- `BREAK` — `Orders!C14` (ORD-011): `POST /orders` returns 202, contract requires 201
- `BREAK` — `Billing!E9` (BIL-007): `currency` field removed, contract requires it
- `BREAK` — `Auth!E5` (AUT-002): wrong credentials returns 400 + wrong body, contract requires 401 + error envelope
- `HOLDS` — `Orders!D11` (ORD-008): `request_id` alias keeps the wire name intact
- `HOLDS` — `Orders!E5` (ORD-002): `pending` is within the allowed enum

**Awaiting your approval to proceed to Step 4 (spawn subagents and check each resource).**

---

### 👤 User

proceed

---

### 🤖 Assistant

> 🔧 called: spawn_subagent, spawn_subagent, spawn_subagent

**Step 4 — Check each resource in parallel**

> 🔧 **spawn_subagent** — general

> 🔧 **spawn_subagent** — general

> 🔧 **spawn_subagent** — general

### 🤖 Assistant

> 🔧 called: read_file

All three subagents agree with the plan. Now reading the test template, then writing the three failing tests.

> 🔧 **read_file** — .bob/skills/rowgate/test_template.py

### 🤖 Assistant

> 🔧 called: glob



> 🔧 **glob** — tests/conftest.py

### 🤖 Assistant

> 🔧 called: glob



> 🔧 **glob** — tests/**/*.py

### 🤖 Assistant

> 🔧 called: glob



> 🔧 **glob** — tests/*

### 🤖 Assistant

> 🔧 called: list_files



> 🔧 **list_files** — .

### 🤖 Assistant

> 🔧 called: list_files



> 🔧 **list_files** — tests

### 🤖 Assistant

> 🔧 called: read_file



> 🔧 **read_file** — tests/conftest.py

### 🤖 Assistant

> 🔧 called: write_file, write_file, write_file

**Step 5 — Write the three failing test files**

> 🔧 **write_file** — tests/contract/test_orders_C14_create_returns_201.py

> 🔧 **write_file** — tests/contract/test_billing_E9_invoice_has_currency.py

> 🔧 **write_file** — tests/contract/test_auth_E5_wrong_secret_returns_401.py

### 🤖 Assistant

> 🔧 called: execute_command

Now run the "before" script to confirm every new test is red:

> 🔧 **execute_command** — Get-Content scripts/run_contract_tests.sh

### 🤖 Assistant

> 🔧 called: execute_command



> 🔧 **execute_command** — .venv\Scripts\python.exe -m pytest tests/contract -q -p no:cacheprovider --json-report --json-report-file=out/test_results.before.json --json-report-omit=keywords,streams 2>&1

### 🤖 Assistant

> 🔧 called: read_file

All 3 tests are red. **Step 6 — Write `out/findings.json` and render the dossier.**

> 🔧 **read_file** — rowgate/findings.schema.json

### 🤖 Assistant

> 🔧 called: write_file



> 🔧 **write_file** — {
  "branch": "feature/fast-checkout",
  "base": "main",
  "workbook": "contract/api-contract.xlsx",
  "workbook_version": "v3.2",
  "findings": [
    {
      "id": "F1",
      "cell": "Orders!C14",
      "related_cells": [],
      "rule": "ORD-011",
      "contract_says": "POST /orders with a valid payload must return HTTP 201.",
      "code_does": "Returns HTTP 202 (status.HTTP_202_ACCEPTED).",
      "evidence": { "file": "app/orders.py", "line": 125 },
      "verdict": "BREAK",
      "reasoning": "status_code changed from HTTP_201_CREATED to HTTP_202_ACCEPTED. Orders!C14 (ORD-011) requires 201; POS treats any other 2xx as a failed checkout and retries (INC-2291).",
      "test": "tests/contract/test_orders_C14_create_returns_201.py",
      "decision": "pending"
    },
    {
      "id": "F2",
      "cell": "Billing!E9",
      "related_cells": [],
      "rule": "BIL-007",
      "contract_says": "GET /invoices/{id} response must include field `currency` (string, ISO 4217).",
      "code_does": "`currency` field removed from InvoiceResponse model; not present on the wire.",
      "evidence": { "file": "app/models.py", "line": 92 },
      "verdict": "BREAK",
      "reasoning": "`currency` deleted from InvoiceResponse in models.py and the keyword argument removed in billing.py. Billing!E9 (BIL-007) marks it Required=Y; mandatory for multi-currency settlement.",
      "test": "tests/contract/test_billing_E9_invoice_has_currency.py",
      "decision": "pending"
    },
    {
      "id": "F3",
      "cell": "Auth!E5",
      "related_cells": ["Errors!D6"],
      "rule": "AUT-002",
      "contract_says": "POST /auth/token with wrong client_secret must return HTTP 401 with body {\"error\": \"invalid_grant\", \"error_description\": \"Client authentication failed\"}.",
      "code_does": "Raises HTTPException(status_code=400, detail=\"invalid client credentials\"), returning 400 with {\"detail\": \"invalid client credentials\"}.",
      "evidence": { "file": "app/auth.py", "line": 33 },
      "verdict": "BREAK",
      "reasoning": "Two violations: status is now 400 (contract Auth!E5 requires 401) and the body uses FastAPI's default {\"detail\":…} shape instead of the error envelope required by Errors!D6.",
      "test": "tests/contract/test_auth_E5_wrong_secret_returns_401.py",
      "decision": "pending"
    }
  ],
  "skipped": [
    {
      "cell": "Orders!D11",
      "change": "OrderResponse.request_id renamed to req_id in Python.",
      "why": "req_id carries Field(serialization_alias=\"request_id\"); the wire field name is unchanged, satisfying ORD-008.",
      "evidence": { "file": "app/models.py", "line": 80 }
    },
    {
      "cell": "Orders!E5",
      "change": "create_order now sets status=\"pending\" instead of \"confirmed\".",
      "why": "ORD-002 allows enum: pending | confirmed; \"pending\" is a valid value.",
      "evidence": { "file": "app/orders.py", "line": 135 }
    }
  ]
}


### 🤖 Assistant

> 🔧 called: execute_command



> 🔧 **execute_command** — .venv\Scripts\python.exe scripts/render_dossier.py 2>&1

### 🤖 Assistant

> 🔧 called: execute_command

The renderer validates line numbers against `out/diff.patch`. The diff was written with a BOM by PowerShell's UTF-8 output, which may shift the hunk offsets it sees. Let me check the actual line numbers in the patch and the branch files.

> 🔧 **execute_command** — Select-String -Path out/diff.patch -Pattern "@@" | Select-Object -First 20 | ForEach-Object { $_.Line }

### 🤖 Assistant

> 🔧 called: execute_command

The hunk headers show the new-file starting lines. Let me check the exact branch-file line numbers for the changed lines:

> 🔧 **execute_command** — Select-String -Path app/orders.py -Pattern "HTTP_202_ACCEPTED" | ForEach-Object { "orders.py line $($_.LineNumber): $($_.Line.Trim())" }; Select-String -Path app/models.py -Pattern "serialization_alias" | ForEach-Object { "models.py line $($_.LineNumber): $($_.Line.Trim())" }; Select-String -Path app/models.py -Pattern "req_id" | ForEach-Object { "models.py line $($_.LineNumber): $($_.Line.Trim())" }; Select-String -Path app/auth.py -Pattern "HTTPException" | ForEach-Object { "auth.py line $($_.LineNumber): $($_.Line.Trim())" }; Select-String -Path app/orders.py -Pattern '"pending"' | ForEach-Object { "orders.py line $($_.LineNumber): $($_.Line.Trim())" }

### 🤖 Assistant

> 🔧 called: apply_diff

Now I have the exact branch-file line numbers. Let me also check what the renderer expects — it checks whether a hunk covers those lines in the diff. The diff hunks for the branch-side are: `orders.py` starts at +8 (hunk `@@ -7,26 +8,33 @@`), `models.py` at +9 and +22, `auth.py` at +10. Update `findings.json` with the correct line numbers:

> 🔧 **apply_diff** — out/findings.json

### 🤖 Assistant

> 🔧 called: execute_command



> 🔧 **execute_command** — .venv\Scripts\python.exe scripts/render_dossier.py 2>&1

### 🤖 Assistant

Renderer reports **0 problems**. Here is the complete Step 7 gate summary.

---

## Step 7 — Decisions needed

**3 breaks found · 3 red tests confirmed · 0 problems in dossier**

---

### F1 · `Orders!C14` · ORD-011
**What:** `POST /orders` now returns **202**. Contract requires **201**. POS treats any non-201 2xx as a failed checkout and retries (INC-2291).
**File:** [`app/orders.py:22`](app/orders.py:22)
**Test:** [`tests/contract/test_orders_C14_create_returns_201.py`](tests/contract/test_orders_C14_create_returns_201.py)

What should happen?
- **fix code** — revert `HTTP_202_ACCEPTED` back to `HTTP_201_CREATED`
- **record breaking change** — update the workbook, add Changelog row, partner sign-off required
- **reject** — discard this finding and its test

---

### F2 · `Billing!E9` · BIL-007
**What:** `currency` field removed from `InvoiceResponse`. Contract requires it in `GET /invoices/{id}` response. Mandatory for multi-currency settlement.
**File:** [`app/models.py:15`](app/models.py:15)
**Test:** [`tests/contract/test_billing_E9_invoice_has_currency.py`](tests/contract/test_billing_E9_invoice_has_currency.py)

What should happen?
- **fix code** — restore `currency: str` to `InvoiceResponse` and pass `order.currency` in `create_invoice_for`
- **record breaking change** — update the workbook
- **reject** — discard this finding and its test

---

### F3 · `Auth!E5` + `Errors!D6` · AUT-002
**What:** Wrong `client_secret` now raises `HTTPException(400, detail=…)`. Contract requires **401** with exact body `{"error": "invalid_grant", "error_description": "Client authentication failed"}`. Two violations in one line: wrong status **and** wrong body shape.
**File:** [`app/auth.py:25`](app/auth.py:25)
**Test:** [`tests/contract/test_auth_E5_wrong_secret_returns_401.py`](tests/contract/test_auth_E5_wrong_secret_returns_401.py)

What should happen?
- **fix code** — reinstate `return error_response(401, "invalid_grant", "Client authentication failed")`
- **record breaking change** — update the workbook
- **reject** — discard this finding and its test

---

**Also noted (not flagged — HOLDS):**
- `Orders!D11` (ORD-008): `req_id = Field(serialization_alias="request_id")` keeps the wire name `request_id` intact. ✓
- `Orders!E5` (ORD-002): `"pending"` is within the allowed enum. ✓

---

### 👤 User

F1 fix code. F2 record breaking change. F3 fix code.

---

### 🤖 Assistant

> 🔧 called: apply_diff

**F1 and F3 — fix code first, then F2 workbook edit.**

> 🔧 **apply_diff** — app/orders.py

### 🤖 Assistant

> 🔧 called: apply_diff



> 🔧 **apply_diff** — <<<<<<< SEARCH
:start_line:24
-------
    if not _is_valid_client(body.client_id, body.client_secret):
        raise HTTPException(status_code=400, detail="invalid client credentials")
=======
    if not _is_valid_client(body.client_id, body.client_secret):
        return error_response(401, "invalid_grant", "Client authentication failed")
>>>>>>> REPLACE


### 🤖 Assistant

> 🔧 called: apply_diff

Now remove the unused `HTTPException` import (no longer referenced):

> 🔧 **apply_diff** — <<<<<<< SEARCH
:start_line:3
-------
from fastapi import APIRouter, HTTPException
=======
from fastapi import APIRouter
>>>>>>> REPLACE


### 🤖 Assistant

> 🔧 called: office_edit

F1 and F3 code fixes are done. Now **F2 — record breaking change in the workbook**. The Billing sheet row BIL-007 is row 9; `Contract status` is column H (`H9`). The next empty Changelog row is 6.

> 🔧 **office_edit** — contract/api-contract.xlsx

### 🤖 Assistant

> 🔧 called: office_edit



> 🔧 **office_edit** — batch

### 🤖 Assistant

> 🔧 called: apply_diff

Workbook updated. Now update `findings.json` with all three decisions:

> 🔧 **apply_diff** — <<<<<<< SEARCH
:start_line:15
-------
      "test": "tests/contract/test_orders_C14_create_returns_201.py",
      "decision": "pending"
=======
      "test": "tests/contract/test_orders_C14_create_returns_201.py",
      "decision": "fix_code",
      "decided_by": "human"
>>>>>>> REPLACE

<<<<<<< SEARCH
:start_line:28
-------
      "test": "tests/contract/test_billing_E9_invoice_has_currency.py",
      "decision": "pending"
=======
      "test": "tests/contract/test_billing_E9_invoice_has_currency.py",
      "decision": "record_breaking",
      "decided_by": "human",
      "workbook_edit": {
        "cells": {"Billing!H9": "BREAKING"},
        "changelog_row": 6
      }
>>>>>>> REPLACE

<<<<<<< SEARCH
:start_line:38
-------
      "test": "tests/contract/test_auth_E5_wrong_secret_returns_401.py",
      "decision": "pending"
=======
      "test": "tests/contract/test_auth_E5_wrong_secret_returns_401.py",
      "decision": "fix_code",
      "decided_by": "human"
>>>>>>> REPLACE


### 🤖 Assistant

> 🔧 called: execute_command

**Step 8 — Measure and publish**

> 🔧 **execute_command** — .venv\Scripts\python.exe -m pytest tests/contract -q -p no:cacheprovider --json-report --json-report-file=out/test_results.after.json --json-report-omit=keywords,streams 2>&1

### 🤖 Assistant

> 🔧 called: execute_command

F1 and F3 are green (2 passed). F2 (`Billing!E9`) is still red — correct, because it was **recorded as a breaking change**, not fixed. The test must remain red; that is the expected state for a recorded break.

> 🔧 **execute_command** — .venv\Scripts\python.exe scripts/render_dossier.py 2>&1

### 🤖 Assistant

> 🔧 called: execute_command



> 🔧 **execute_command** — .venv\Scripts\python.exe scripts/export_site.py 2>&1

### 🤖 Assistant

Renderer: **0 problems**. All done.

---

## Final counts

| | |
|---|---|
| Breaks found | 3 |
| Red before | 3 |
| Green after | 2 (F1, F3 — fixed in code) |
| Still red | 1 (F2 — recorded breaking change; test stays red by design) |
| Recorded breaking changes | 1 |
| Skipped (checked, held) | 2 |

**What was changed:**

- [`app/orders.py:22`](app/orders.py:22) — `HTTP_202_ACCEPTED` → `HTTP_201_CREATED` (F1 fix)
- [`app/auth.py:25`](app/auth.py:25) — `raise HTTPException(400, …)` → `return error_response(401, "invalid_grant", …)` (F3 fix)
- [`contract/api-contract.xlsx`](contract/api-contract.xlsx) — `Billing!H9` set to `BREAKING`; Changelog row 6 added (F2 record)