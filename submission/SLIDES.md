# Rowgate slides (7 slides)

Built for the four judging criteria: **application of Bob**, **business value**,
**originality**, **presentation**. One idea per slide, big type, real screenshots.
Numbers marked **[N]** come from `python scripts/run_numbers.py` after the run;
**[B]** from `submission/BASELINE.md`; **[C]** from `MEMORY.md` §6.

Visual style: the site's palette (forest-black `#0F1611`, cream `#E8DCB8`, paper `#F5F2EA`,
amber `#E3B64F` for the cited cell), serif headlines (Newsreader), logo from
`web/public/logo.svg`. Use `web/public/og.png` as the title-slide image if short on time.

---

## 1. Title

**Rowgate**
*The contract they signed is not in your diff.*

- Logo, one line: "Cites the broken cell · writes the failing test · built with IBM Bob"
- Links: rowgate.vercel.app · github.com/Ritapossible/Rowgate
- Name: Ritapossible, IBM Bob 2.0 Hackathon 2026

**Say (10 s):** "Rowgate gates a release on the contract your partner actually signed: a spreadsheet."

---

## 2. The problem *(business value)*

**Review reads the diff. The partner signed a spreadsheet.**

Left: the PR, 5 files, +24 −12, existing tests green, "looks mergeable".
Right: `api-contract.xlsx`, 41 signed rules, 6 sheets, 0 of them in the diff.

- Partner integrations in banking, telco and insurance are signed as spreadsheets and never become OpenAPI.
- A status code or a required field changes; nothing in the PR says so.
- The cost lands after release: failed checkouts, rejected invoices, support tickets.

**Say:** "In our demo the pull request is green. It still breaks three signed rows."

---

## 3. What Rowgate returns *(originality)*

**A cell. A failing test. A decision.**

Screenshot: one finding card from the Run page (`Orders!C14`, the signed row with the cell
highlighted, the diff line, `test_orders_C14_create_returns_201.py` red → green).

- Every finding cites one cell, like `Orders!C14`, not a paragraph of opinion.
- The test is named after the cell and must fail on the branch. A wrong citation shows up as a test that doesn't fail.
- The human chooses: fix the code, or record a breaking change **in the workbook itself**.

**Say:** "Review bots produce opinions. Rowgate produces a claim you can check."

---

## 4. How it runs inside IBM Bob *(application of technology)*

**Bob does the judgment. Scripts do the mechanics.**

Diagram, left to right, Bob steps in cream and script steps in grey:

`collect_diff.sh` → **office_read** the workbook → **Plan mode** (you approve) →
**3 parallel subagents** (orders · billing · auth) → **Agent mode** writes tests →
`run_contract_tests.sh` → **human decision** → **office_edit** the workbook → `render_dossier.py`

- Contract Gate **custom mode** + Rowgate **Skill** + `/rowgate`
- Document understanding: merged cells, inherited rules, a shared Errors sheet, PLANNED rows it must ignore
- Screenshot: the subagent panel mid-run

**Say:** "Every Bob 2 feature here is doing a job, not decorating a slide."

---

## 5. Proof: the run *(presentation)*

**[N] of [N] broken cells found. 0 false alarms.**

| | Reading the diff | Rowgate |
| --- | --- | --- |
| Breaks found | **[B]** of 3 | **[N]** of 3 |
| Harmless rename flagged as a break | **[B]** | no, skipped with the reason |
| Proven by a failing test | none | **[N]/[N]** red |
| Time | **[B]** min | **[N]** min |

Screenshot: the "Checked and skipped" card for `Orders!D11` (renamed in Python, same name on the wire).

**Say:** "It also knows what *not* to flag. That's the difference between a gate and a noise machine."

---

## 6. After the run *(business value)*

**The model reads the sheet once. The tests stay.**

- The contract tests live in `tests/contract/`, so every later pull request is checked by plain pytest in CI, with no model and no tokens.
- Screenshot: the GitHub PR from `feature/fast-checkout`, red on the contract test for the recorded breaking change.
- Cost: **[C]** Bobcoins for the whole run, then zero per PR.
- Every number is measured: code from the diff, pass/fail from pytest, workbook edits from git.

---

## 7. Close

**Rowgate: the signed contract, as a release gate.**

- Try it: rowgate.vercel.app → Run · Contract (`/contract?cell=Orders!C14`) · Docs
- Code: github.com/Ritapossible/Rowgate (MIT), Bob session reports in `bob_sessions/`
- Next: any spreadsheet contract (API mappings, data contracts, SLA tables) → tests

---

## Checklist before exporting the PDF

- [ ] Every **[N]**, **[B]**, **[C]** replaced with a real number
- [ ] Screenshots from the real run, not the sample
- [ ] No use of the word "workflow" for Rowgate (it's the Contract Gate mode + Rowgate Skill)
- [ ] Exported as PDF for the lablab form
