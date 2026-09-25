# Rowgate — 48-Hour Build Plan

Build window: **Fri 25 Sep 16:00 WAT → Sun 27 Sep 16:00 WAT** (11:00 EDT → 11:00 EDT).
Target: submit by **Sun 14:00 WAT**. The last two hours are buffer, not work time.

Rule for every phase: it ends when its **exit check** passes, not when the clock runs out.
If a phase overruns by more than 2 hours, cut from its "cut if late" list.

Architecture: `ARCHITECTURE.md` · Facts, decisions, Bobcoin ledger: `MEMORY.md`

---

## Phase 0 — Before kickoff (Thu 24 Sep)

- [x] Register on lablab.ai
- [x] Create an IBMid on the registration email (needed to sign in to Bob)
- [x] Create repo, write ARCHITECTURE / MEMORY / PLAN
- [ ] Install Bob IDE, sign in, note the version number in MEMORY §2
- [ ] Skim Bob docs for: custom mode file format, slash command path, `office_edit` usage
- [x] Prepare local env: `pip install -r requirements.txt`
- [ ] Sleep. The recorded run needs a clear head on Sunday.

Non-AI scaffolding may be built before kickoff; all Bob work waits for the hackathon account (MEMORY D12).

## Kickoff (Fri 16:00 WAT)

- [x] Find the IBM Bob invite email (check spam; search "IBM Bob"), accept it
- [x] Hackathon account confirmed: team `ibm-hackathon-lablab`, Enterprise, 40 Bobcoins, 0 used (25 Sep 19:36 WAT)
- [ ] Sign in to Bob IDE on the computer and select team `ibm-hackathon-lablab`

## Phase 1 — Fixture · 0 Bobcoins · ✅ done Fri 25 Sep morning (before kickoff, no Bob)

Build the thing Rowgate reviews. No Bob tokens spent here.

- [x] `LICENSE` (MIT), `README.md` stub, `.gitignore` (`out/*`, keep `out/dossier.html` at the end)
- [x] `app/` FastAPI service on `main`: orders, billing, auth; Pydantic models
- [x] `tests/test_smoke.py` passing on `main`
- [x] `scripts/build_contract.py` → `contract/api-contract.xlsx`: 6 sheets (Cover, Orders, Billing, Auth, Errors, Changelog), merged headers, notes column, 40+ rows, column order differs between sheets
- [x] Fix final cell addresses; update ARCHITECTURE §5 table
- [x] Branch `feature/fast-checkout`: breaks 1–3 plus the decoy, each as a plausible code change
- [x] Reference check (kept out of the repo): all 27 ACTIVE rows hold on `main`; on the branch exactly `Orders!C14`, `Billing!E9`, `Auth!E5` fail and `Orders!D11` holds
- [x] `scripts/collect_diff.sh`, `scripts/run_contract_tests.sh`

**Exit check:** on the branch, `pytest tests/test_smoke.py` is green (PR looks mergeable), and opening the xlsx by hand you can point at the 3 cells the branch violates.

Cut if late: Cover sheet polish, Notes column realism.

## Phase 2 — Rowgate in Bob (starts at kickoff, Fri 16:00 WAT) · ≤ 18 Bobcoins

Phase 1 finished early, so Phase 2 starts at kickoff and the later phases gain ~8h of slack.

- [x] `rowgate/findings.schema.json`
- [x] `scripts/render_dossier.py` + `rowgate/dossier.html.j2`, tested on synthetic findings (light/dark, phone width)
- [x] Evidence is measured: diff excerpts by file + line, workbook edits by comparing with git (ARCHITECTURE §4)
- [x] `scripts/reset_demo.sh` + `demo/start` branch; CI (`.github/workflows/tests.yml`) runs all tests on every PR
- [x] Full simulated run (placeholder tests, scripted workbook edit): dossier renders with 0 problems
- [x] `.bob/skills/rowgate/SKILL.md`: procedure, schema, test naming rule, decoy guidance ("check serialization aliases before flagging a rename"), "never edit app/ unless decision = fix_code"; test template beside it
- [x] Contract Gate custom mode text (`rowgate/bob/contract-gate-mode.md`), `/rowgate` command text, `RUNBOOK.md`, `scripts/publish_run.sh`
- [ ] Create the mode and command in Bob (paste); note where Bob saves them
- [ ] `/rowgate` slash command (skip if the path is unclear; invoke the Skill directly)
- [ ] Rehearse prompts in **Ask mode** on one sheet (≤ 8 coins). Log in MEMORY §6
- [ ] **Dry run 1**, full path (≤ 10 coins). Record cost per subagent in MEMORY §6
- [ ] Screenshot **every** Bob task summary into `bob_sessions/` as you go, named `NN-<step>.png`

**Exit check:** one run produces `findings.json` with 3 BREAK + 1 skipped decoy, 3 test files named by cell, all red on the branch, and a rendered `out/dossier.html`.

Cut if late (in order): slash command → third subagent (merge auth into billing) → `office_edit` step.

## Phase 3 — Decisions + workbook edit (Sat 16:00 → Sat 22:00, ~6h) · ≤ 10 Bobcoins

- [ ] Decision step: F1 = fix code, F2 = record breaking change, F3 = fix code (shows both paths)
- [ ] Fix-code path: minimal patch, rerun → green, captured in `findings.json`
- [ ] Breaking path: `office_edit` sets `Billing!<Status>` = `BREAKING`, appends a Changelog row
- [ ] Renderer shows before/after test status and the workbook edits
- [ ] **Dry run 2** end to end after `scripts/reset_demo.sh --force`

**Exit check:** dossier shows 3 findings with red → green (or recorded breaking change), 1 skipped decoy with reason, workbook edit visible when re-opening the xlsx.

Cut if late: the breaking-change path (keep all three as fix-code).

## Phase 4 — Recorded run (Sat 22:00 → Sun 06:00, with sleep) · ≤ 8 Bobcoins

- [ ] Reset: `scripts/reset_demo.sh --force` → all 7 checks ✓
- [ ] Time the "human" baseline: skim the diff only, note what you catch and how long it takes
- [ ] Screen-record the Rowgate run once, cleanly. **Stop iterating after this.**
- [ ] Final `bob_sessions/` screenshots; commit final `out/dossier.html`
- [ ] `python scripts/export_site.py`, commit `web/public/data/` + `web/public/dossier.html`; check the Vercel site shows the run
- [ ] Record numbers: human (N of 3, decoy flagged?, minutes) vs Rowgate (3 of 3, decoy skipped, minutes)

**Exit check:** a clean recording exists and the numbers are written in MEMORY.

## Phase 5 — Package + submit (Sun 06:00 → Sun 14:00)

- [ ] README: one-liner, the "who does what" table, how to run pytest without Bob, screenshots
- [ ] Slides (5–6): problem → what ships → how Bob runs it → demo numbers → why it's not a review bot → install (one folder)
- [ ] 3-minute video (script below)
- [ ] Submission text (below), repo URL, **Vercel URL**, video URL, slides
- [ ] Check: MIT license present · `bob_sessions/` populated · repo public · no "workflow" wording outside `.github/` (`grep -ri workflow --exclude-dir=.github --exclude-dir=.git .`)
- [ ] **Submit by 14:00 WAT**

## Video script (3:00)

| Time | Shot |
| --- | --- |
| 0:00–0:20 | The PR: small diff, smoke tests green, "looks mergeable". |
| 0:20–0:40 | Open `api-contract.xlsx`: signed cover sheet, 40+ rows. "The contract the partner signed never enters the PR." |
| 0:40–1:25 | `/rowgate feature/fast-checkout`: Plan mode plan → approve → **three subagents running live**. Hold on this. |
| 1:25–1:55 | Tests written with cell names; pytest red on the branch. |
| 1:55–2:25 | Decision: fix code for F1/F3 → green. Record breaking change for F2 → Bob edits the workbook; show the Changelog row. |
| 2:25–2:45 | Dossier: cell · hunk · red→green. Scroll to "Skipped: request_id alias, wire format unchanged". |
| 2:45–3:00 | Numbers: human 1/3 + false alarm vs Rowgate 3/3 + 0 false alarms. "The tests stay. Every future PR is checked without a model." End on `bob_sessions/`. |

## Submission text (draft)

**Title:** Rowgate

**Short:** Rowgate checks a release branch against the signed API spreadsheet and writes the
contract test that fails when a row breaks. Every finding cites a cell. A human decides
before anything changes.

**Long:** Pull request review sees the diff. The API contract a partner signed is a
spreadsheet that never shows up in that diff, so status codes and required fields change
while the review still looks clean. Rowgate runs inside IBM Bob as a Contract Gate mode and
a Rowgate Skill. Bob reads the workbook with `office_read`, maps the branch to contract rows
in Plan mode, and checks each resource in a parallel subagent. In Agent mode it writes one
contract test per broken cell, named after the cell, and the test fails on the branch. A
human then chooses to fix the code or record a breaking change, which Bob writes back into
the workbook with `office_edit`. The tests stay in the repo, so every later PR is checked by
pytest with no model involved. On a sample service, reading the diff found 1 of 3 breaks and
flagged a harmless rename. Rowgate found all 3, skipped the rename with a reason, and proved
each break with a red-to-green test.
