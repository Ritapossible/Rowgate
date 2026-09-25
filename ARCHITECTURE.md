# Rowgate — Architecture

Rowgate checks a release branch against the **signed API contract spreadsheet** and writes
the contract test that fails when a row breaks. Every finding cites a cell (`Orders!C14`),
every cell gets a test, and a human decides what happens next.

Built on IBM Bob 2.x features only: a **custom mode**, a **Skill**, a **slash command**,
**Plan → Agent** modes, **parallel subagents**, and **`office_read` / `office_edit`** for the
workbook. Deterministic work (diff, test run, HTML rendering) is done by scripts, never by
the model.

> Vocabulary rule: Rowgate is **not** a Bob "Workflow". The workflow engine (non-agentic
> steps, Select Action gate) ships only in IBM's Premium Packages. We say
> "Contract Gate mode + Rowgate Skill + `/rowgate`". See `MEMORY.md`.

---

## 1. The run, end to end

```
 developer                    Bob (Contract Gate mode)                     scripts (no tokens)
 ─────────                    ────────────────────────                     ───────────────────
 /rowgate feature/x ───────▶  load Rowgate Skill
                              ├─ run ──────────────────────────────────▶  scripts/collect_diff.sh
                              │                                            → out/diff.patch
                              │                                            → out/changed_files.txt
                              ├─ office_read contract/api-contract.xlsx
                              │
                              ├─ PLAN MODE: which rows can this diff touch?
                              │     plan lists sheet → rows → changed files
 approve plan  ◀──────────────┤     ◀── HUMAN GATE 1 (plan approval)
                              │
                              ├─ spawn subagents in parallel (approval per spawn)
                              │     ┌ orders   : Orders sheet  vs app/orders.py
                              │     ├ billing  : Billing sheet vs app/billing.py
                              │     └ auth     : Auth + Errors sheets vs app/auth.py
                              │   each returns: row verdicts {BREAK | OK | DECOY-OK}
                              │
                              ├─ merge → out/findings.json (fixed schema)
                              │
                              ├─ AGENT MODE: write tests/contract/test_<sheet>_<cell>_*.py
                              ├─ run ──────────────────────────────────▶  scripts/run_contract_tests.sh
                              │                                            → out/test_results.json (red)
                              │
 choose per finding ◀─────────┤     ◀── HUMAN GATE 2 (decision)
   [fix code] [record breaking change] [reject finding]
                              │
                              ├─ fix code      → minimal patch in app/, rerun → green
                              ├─ record break  → office_edit: Status cell = BREAKING,
                              │                  append row to Changelog sheet
                              ├─ reject        → finding marked rejected, test removed
                              │
                              └─ run ──────────────────────────────────▶  scripts/render_dossier.py
                                                                           → out/dossier.html
```

Two human gates, both native to Bob: approving the Plan-mode plan, and approving each
subagent spawn / the Agent-mode decision prompt. Product code is only changed when a human
picks **fix code** for that specific finding.

## 2. Who does what

| Step | Done by | Why |
| --- | --- | --- |
| Diff the branch, list changed files | `scripts/collect_diff.sh` | Deterministic, free, reproducible |
| Read the workbook (sheets, merged headers, notes) | Bob `office_read` | Document understanding is the point |
| Map diff → contract rows | Bob, **Plan mode** | Judgment; human approves before any write |
| Per-resource verdicts | Bob **subagents**, in parallel | Isolated context per resource; visible in chat (2.2.0 "live subagent tool results") |
| Write contract tests | Bob, **Agent mode** | Turning a human spreadsheet into executable checks is the AI work |
| Run tests | `scripts/run_contract_tests.sh` (pytest) | Deterministic |
| Record breaking change in the workbook | Bob `office_edit` (2.1.0+) | Closes the loop in the signed artifact |
| Render the dossier | `scripts/render_dossier.py` | Same output every run, zero Bobcoins |

The core pitch lives in this table: **Bob reads the signed spreadsheet once and writes tests
that stay in the repo. Every later PR is guarded by pytest, with no model in the loop.**

## 3. Repository layout (target)

```
rowgate/
├── ARCHITECTURE.md              # this file
├── MEMORY.md                    # facts, decisions, open questions, Bobcoin ledger
├── PLAN.md                      # 48-hour build plan
├── LICENSE                      # MIT (required by the hackathon)
├── README.md                    # submission-facing
│
├── app/                         # demo service (FastAPI) — the thing under review
│   ├── main.py
│   ├── orders.py                # POST /orders, GET /orders/{id}
│   ├── billing.py               # GET /invoices/{id}
│   ├── auth.py                  # POST /auth/token
│   └── models.py                # Pydantic models (decoy alias lives here)
│
├── contract/
│   └── api-contract.xlsx        # the "signed" contract — messy on purpose
│
├── tests/
│   ├── test_smoke.py            # existing suite; passes on the branch (diff "looks fine")
│   └── contract/                # written by Rowgate; test name = cell citation
│
├── scripts/
│   ├── collect_diff.sh          # git diff main...HEAD → out/
│   ├── run_contract_tests.sh    # pytest tests/contract --json-report → out/
│   ├── render_dossier.py        # findings.json + test_results.json → dossier.html
│   └── build_contract.py        # generates contract/api-contract.xlsx (fixture source)
│
├── rowgate/
│   ├── findings.schema.json     # the contract between Bob and the renderer
│   └── dossier.html.j2          # template for the renderer
│
├── .bob/                        # Bob configuration (paths to verify at kickoff)
│   ├── skills/rowgate/SKILL.md  # the procedure; references scripts/ and schema
│   ├── commands/rowgate.md      # /rowgate <branch>   (path unverified)
│   └── <custom mode file>       # "Contract Gate" mode; restricts subagents
│
├── out/                         # generated per run (gitignored except the final dossier)
└── bob_sessions/                # screenshots of every Bob task summary (REQUIRED)
```

If the 2.2.0 `plugins/` folder works in the hackathon build, `.bob/skills`, the mode and the
command move into `plugins/rowgate/` so Rowgate installs into any repo by copying one folder.

## 4. The findings contract (`rowgate/findings.schema.json`)

Bob's only structured output. The renderer trusts nothing else.

```jsonc
{
  "branch": "feature/fast-checkout",
  "base": "main",
  "workbook": "contract/api-contract.xlsx",
  "workbook_version": "v3.2 (signed 2026-08-14)",
  "findings": [
    {
      "id": "F1",
      "cell": "Orders!C14",
      "related_cells": [],                   // e.g. ["Errors!D6"] for a referenced row
      "rule": "ORD-011",
      "contract_says": "POST /orders → 201 Created",
      "code_does": "returns 202 Accepted",
      "evidence": { "file": "app/orders.py", "hunk": "@@ -41,7 +41,7 @@ ...", "line": 44 },
      "verdict": "BREAK",                    // findings are breaks only; lookalikes go in "skipped"
      "reasoning": "one or two sentences",
      "test": "tests/contract/test_orders_C14_create_returns_201.py",
      "decision": "fix_code",                // fix_code | record_breaking | reject | pending
      "decided_by": "release owner",
      "workbook_edit": null                  // or { "cells": { "Billing!H9": "BREAKING" }, "changelog_row": 6 }
    }
  ],
  "skipped": [
    { "cell": "Orders!D11", "change": "request_id renamed to req_id", "why": "serialization alias keeps the wire name request_id" }
  ]
}
```

Test outcomes are **not** written by Bob. `scripts/run_contract_tests.sh before` and
`... after` save pytest JSON reports (`out/test_results.before.json` / `.after.json`); the
renderer reads red → green from those, so the badges can't be claimed, only measured.

Rules (enforced by `scripts/render_dossier.py`, shown in a red box in the dossier):
- A `BREAK` without a test file named after its cell is invalid.
- The test must exist on disk.
- Test file names must contain the cell (`test_<sheet>_<cell>_...`), so the test name *is* the citation.
- `skipped` is shown in the dossier. It shows the precision half of the demo: Rowgate says why it did not flag something.

## 5. Demo fixture

### Service
Small FastAPI app, three resources, one Pydantic models file. `main` is contract-compliant.
Branch `feature/fast-checkout` is a plausible "speed up checkout" change that carries the breaks.

### Workbook (`contract/api-contract.xlsx`)
Messy on purpose, so reading it is real document understanding:

| Sheet | Contents |
| --- | --- |
| `Cover` | Partner name, version, sign-off block, merged title cells |
| `Orders` | Endpoint, method, status, required fields, error body, Status column, notes |
| `Billing` | Same shape, different column order |
| `Auth` | Token endpoint, error codes |
| `Errors` | Shared error-body catalogue referenced by the other sheets |
| `Changelog` | Date, cell, change, decision, approver |

Merged header rows, a column-letter shift between sheets, a free-text Notes column, and at
least 40 data rows so the three breaks are not obvious by eye.

### Planted changes on `feature/fast-checkout`

| # | Cell (target) | Contract | Branch | Expected verdict |
| --- | --- | --- | --- | --- |
| 1 | `Orders!C14` | `POST /orders` → **201** | returns **202** | BREAK |
| 2 | `Billing!E9` | `GET /invoices/{id}` requires `currency` | field dropped from response model | BREAK |
| 3 | `Auth!E5` (+ `Errors!D6`) | wrong client_secret → **401** with `{"error":"invalid_grant", ...}` | returns **400** `{"detail":...}` | BREAK |
| D | `Orders!D11` | `request_id` required in response | renamed `req_id` in code **with** `serialization_alias="request_id"` | DECOY-OK (skip) |

These addresses are final: `scripts/build_contract.py` asserts them on every build.
The existing tests pass on the branch, so the PR looks mergeable. The branch also carries
noise that is *not* a break: a `_price_cents` helper, a log line, a constant-time secret
comparison, a version bump, and `status` moving from `confirmed` to `pending` (both allowed
by `Orders!E5`).

Other traps in the workbook: `ORD-007`, `ORD-014`, `BIL-010/011`, `AUT-005`, `ERR-003/007`
are PLANNED and `ORD-013` is DEPRECATED, so none of them may be flagged. Field rows on
Orders inherit their status code from `ORD-011` ("↳ ORD-011"), and Billing's status code is
one merged cell (`D3:D9`). The next free Changelog row is 6.

## 6. Dossier (`out/dossier.html`)

One self-contained page (inline CSS, no external requests):

1. Header: branch, workbook version, run time, counts (3 BREAK / 1 skipped / 0 errors).
2. Per finding: the cell and its row rendered as a mini table, then the diff hunk, then the test name with red → green badges, then the decision and who made it.
3. Skipped section: the decoy and why it was skipped.
4. Workbook edits: cells changed by `office_edit` plus the new Changelog row.
5. Footer: rollback note (revert commit SHA) and how to re-run pytest without Bob.

## 7. Non-goals

- No web app, auth, database, or multi-tenant anything.
- No watsonx or other model outside Bob.
- No PDF/DOCX policy checking (that was the earlier "Clause" idea; out of scope).
- No auto-merge. No rewriting product code without a per-finding human decision.
- No OpenAPI generation. The target is the contract nobody converted to OpenAPI.

## 8. Risks and fallbacks

| Risk | Fallback |
| --- | --- |
| `office_edit` missing in the hackathon build | Drop the workbook-edit shot; decision recorded in `findings.json` and dossier only |
| `office_edit` can't write comments | Already designed around: Status cell value + Changelog row only |
| `.bob/commands/` path differs | Start via the Skill by name; the slash command is nice-to-have |
| Custom mode can't restrict subagents as expected | Keep the mode for its instructions; mention restriction only if shown |
| Subagent run too expensive in Bobcoins | Two subagents (orders+billing, auth+errors) instead of three |
| Bob misses the decoy or flags it | Tighten Skill instructions on serialization aliases; that is the precision story, worth the rehearsal |
| Live run flakes during recording | Record the best clean run; `bob_sessions/` screenshots are the evidence |
