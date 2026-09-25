# Rowgate video: 3:00 script

Record the **real run** (`RUNBOOK.md` step 3) in full, then cut it down. Bob will take
minutes where the video shows seconds; that's what the edit is for. Numbers marked **[N]**
come from `python scripts/run_numbers.py`, **[B]** from `submission/BASELINE.md`.

## Recording setup

- Screen recorder: OBS Studio (free) or the Xbox Game Bar (Windows: Win+Alt+R). 1920×1080, 30 fps.
- Bob IDE and browser zoomed to about **125%** so text is readable on a phone.
- Close notifications. Use one browser window with these tabs, in order: GitHub PR ·
  `api-contract.xlsx` (Excel or LibreOffice) · Bob IDE · rowgate.vercel.app/run.
- Record the voice-over **separately** afterwards (phone voice memo in a quiet room is fine),
  then lay it over the cut. That's easier than talking while Bob works.

## Shot list and voice-over

| Time | On screen | Voice-over |
| --- | --- | --- |
| **0:00–0:15** | The GitHub pull request `feature/fast-checkout`: 5 files, green checks | "This pull request speeds up checkout. Five files, tests green. It looks mergeable." |
| **0:15–0:32** | Open `api-contract.xlsx`: Cover sheet with the sign-off block, then scroll the Orders sheet | "But the partner signed this spreadsheet: 41 rules for status codes, required fields and error bodies. None of it is in the diff." |
| **0:32–0:45** | Bob IDE: switch to **Contract Gate** mode, type `/rowgate feature/fast-checkout` | "Rowgate is a custom mode and a Skill for IBM Bob. One command." |
| **0:45–1:00** | Bob reading the workbook, then the **Plan** it proposes; click approve | "Bob reads the workbook directly: merged cells, inherited rules, rows that are only planned. It plans which rows this diff can touch, and waits for me." |
| **1:00–1:25** | **Three subagents running in parallel** (hold here, this is the key shot) | "Then three subagents check orders, billing and auth in parallel, each in its own context." |
| **1:25–1:45** | `tests/contract/` with three files named after cells; terminal: `run_contract_tests.sh before`, **red** | "For every broken cell, Bob writes one test named after it, and every test fails on this branch. If Bob had cited the wrong cell, the test would pass and the finding would die." |
| **1:45–2:10** | The decision prompt: fix code for Orders!C14 and Auth!E5, record breaking change for Billing!E9. Then the spreadsheet: `Billing!H9 = BREAKING` and the new Changelog row | "Now a human decides. Two get fixed. One is accepted as a breaking change, and Bob writes that into the signed workbook itself." |
| **2:10–2:35** | rowgate.vercel.app/run: stats row, one finding card (cell highlighted, diff line, red → green), then scroll to **Checked and skipped: Orders!D11** | "Everything here is measured: code from the diff, pass and fail from pytest, workbook edits from git. And it skipped the rename that only *looks* like a break, because the wire name didn't change." |
| **2:35–2:50** | Numbers card: **[B] of 3** by reading the diff vs **[N] of 3** with Rowgate, 0 false alarms, **[N]/[N]** red → decided | "Reading the diff, I found [B] of 3 and flagged the harmless rename. Rowgate found all three and flagged nothing wrong." |
| **2:50–3:00** | The PR again, now **red** on the contract test; end card with logo, rowgate.vercel.app, and `bob_sessions/` in the repo | "The model read the sheet once. The tests stay, so every future pull request is checked for free. Rowgate: the signed contract, as a release gate." |

## Edit list

1. Cut Bob's thinking time down to 1–2 seconds per step. Keep the moment each result appears.
2. Speed up long scrolls ×2. Never speed up the subagent panel; let it breathe for about 5 seconds.
3. Zoom (crop) into: the plan, the subagent panel, a test file name, the red pytest line, `Billing!H9`.
4. Add small captions for cell names when they appear (`Orders!C14`, `Billing!E9`, `Auth!E5`, `Orders!D11`).
5. Numbers card at 2:35: a plain frame in the site colours (forest-black background, cream text).
6. Export 1080p MP4, under 3:00. Upload to YouTube as **Unlisted** (or wherever lablab asks) and put the link in the form.

## Don't

- Don't call Rowgate a "workflow". Say "custom mode and Skill".
- Don't show a personal Bob account; the team in Settings must be `ibm-hackathon-lablab`.
- Don't show sample data. Everything on screen must come from the recorded run.
