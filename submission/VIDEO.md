# Rowgate video: 3:00 script

Record the **real run** (`RUNBOOK.md` step 3) in full, then cut it down. Bob will take
minutes where the video shows seconds; that's what the edit is for. All numbers below are filled in from the run of record.

## Recording setup

- Screen recorder: OBS Studio (free) or the Xbox Game Bar (Windows: Win+Alt+R). 1920×1080, 30 fps.
- Bob IDE and browser zoomed to about **125%** so text is readable on a phone.
- Close notifications. Use one browser window with these tabs, in order:
  PR **Files changed** · `api-contract.xlsx` (Excel or LibreOffice) · Bob IDE ·
  rowgate.vercel.app/run · PR **Checks**.
- Record the voice-over **separately** afterwards (phone voice memo in a quiet room is fine),
  then lay it over the cut. That's easier than talking while Bob works.

**The pull request is https://github.com/Ritapossible/Rowgate/pull/1, and it is red** — Bob's
contract test for `Billing!E9` now lives on the branch, so CI fails on purpose. Open on the
**Files changed** tab, never on Checks: the point of the first shot is that the diff looks
innocent. Save the red check for the last shot, where it is the payoff. Refresh the PR before
recording so no check is still spinning.

## Shot list and voice-over

| Time | On screen | Voice-over |
| --- | --- | --- |
| **0:00–0:15** | PR #1, **Files changed** tab. Scroll the five files: `orders.py` 201 → 202, `billing.py` losing `currency`, `auth.py` swapping the error | "This pull request speeds up checkout. Three commits, five files. Every change is defensible on its own, and nothing in the repository's own test suite objects." |
| **0:15–0:32** | Open `api-contract.xlsx`: the Cover sheet sign-off block, then scroll Orders. Pause on the `↳ ORD-011` inherited rows and the merged `Billing!D3` | "But the partner signed this spreadsheet. Forty-one rules for status codes, required fields and error bodies — inherited rows, merged cells, rows that are only planned. None of it appears in the diff." |
| **0:32–0:45** | Bob IDE: switch to **Contract Gate** mode, type `/rowgate feature/fast-checkout` | "Rowgate is a custom mode and a Skill for IBM Bob. One command." |
| **0:45–1:00** | Bob reading the workbook with `office_read`, then the **Plan**; click approve | "Bob reads the workbook directly and plans which signed rows this diff can touch. Then it waits for me." |
| **1:00–1:25** | **Three subagents running in parallel** — hold here, this is the key shot | "Three subagents check orders, billing and auth at the same time, each in its own context." |
| **1:25–1:45** | `tests/contract/` with **four** files named after cells; terminal: `run_contract_tests.sh before`, **4 red** | "For every broken cell, Bob writes one test named after that cell. All four fail on this branch. If Bob had cited the wrong cell, its test would pass and the finding would die — the name is the proof." |
| **1:45–2:10** | The decision prompt: fix code for `Orders!C14`, `Auth!E5` and `Errors!D6`; record a breaking change for `Billing!E9`. Then the spreadsheet: `Billing!H9 = BREAKING` and the new Changelog row | "Now a human decides. Three get fixed. One is accepted as a breaking change — and Bob writes that decision back into the signed workbook itself, with `office_edit`." |
| **2:10–2:32** | rowgate.vercel.app/run: the stats row, one finding card (cell, diff line, red → green), then scroll to **Checked and skipped: `Orders!D11`** | "Everything here is measured, not claimed: code from the diff, pass and fail from pytest, workbook edits from git. And it skipped the rename that only *looks* like a break, because `serialization_alias` keeps the wire name identical." |
| **2:32–2:45** | Numbers card: **2 of 4** reading the diff vs **4 of 4** with Rowgate · 0 false alarms · 4/4 proven red · 6.1 Bobcoins | "I read the diff myself, already knowing where the breaks were, and found two of four in twelve minutes. Rowgate found all four, proved each with a failing test, and flagged nothing that wasn't broken." |
| **2:45–3:00** | **The payoff.** PR #1 → **Checks** tab, now red. Zoom the failure: `FAILED tests/contract/test_billing_E9_invoice_has_currency.py — AssertionError: currency field is required (BIL-007)`, `1 failed, 17 passed`. End card: logo, rowgate.vercel.app, `bob_sessions/` | "And the branch can't merge. Not because a model objected — because a row a person signed in a spreadsheet is now a test, and it fails. The model read the sheet once. The tests stay, and every future pull request is checked for free." |

## Edit list

1. Cut Bob's thinking time down to 1–2 seconds per step. Keep the moment each result appears.
2. Speed up long scrolls ×2. Never speed up the subagent panel; let it breathe for about 5 seconds.
3. Zoom (crop) into: the plan, the subagent panel, a test file name, the red pytest line, `Billing!H9`.
4. Add small captions for cell names when they appear (`Orders!C14`, `Billing!E9`, `Auth!E5`,
   `Errors!D6`, `Orders!D11`).
5. Numbers card at 2:32: a plain frame in the site colours (forest-black background, cream text).
6. The last shot earns a beat of silence. Let the red ✗ and the `BIL-007` assertion sit on screen
   for a full second before the end card.
7. Export 1080p MP4, under 3:00. Upload to YouTube as **Unlisted** (or wherever lablab asks) and put the link in the form.

## Don't

- Don't call Rowgate a "workflow". Say "custom mode and Skill".
- Don't show a personal Bob account; the team in Settings must be `ibm-coding-challenge-2`.
- Don't show sample data. Everything on screen must come from the recorded run.
- Don't open on the PR's Checks tab. It is red from the start now, which gives away the ending.
- Don't say the PR was green. Say the repository's own test suite passes, which is what is true:
  the only failure is the contract test Bob wrote.
