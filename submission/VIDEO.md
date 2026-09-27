# Rowgate video: 3:00 script

Record the **real run** (`RUNBOOK.md` step 3) in full, then cut it down. Bob will take
minutes where the video shows seconds; that's what the edit is for. All numbers below are filled in from the run of record.

## Recording setup

- Screen recorder: OBS Studio (free) or the Xbox Game Bar (Windows: Win+Alt+R). 1920×1080, 30 fps.
- Bob IDE and browser zoomed to about **125%** so text is readable on a phone.
- Close notifications. Use one browser window with these tabs, left to right, in shot order:
  rowgate.vercel.app · PR **Files changed** · `api-contract.xlsx` (Excel or LibreOffice) ·
  Bob IDE · rowgate.vercel.app/run · PR **Checks**.
- Record the voice-over **separately** afterwards (phone voice memo in a quiet room is fine),
  then lay it over the cut. That's easier than talking while Bob works. The lines below are the
  shot list's short form; **`submission/VOICEOVER.md` is the sheet to read from**, timed to about
  two words per second with the word count per block.
- The frames that are not footage are already rendered in `submission/cards/`: the numbers card,
  the end card, and a transparent caption chip per cell. `scripts/render_cards.py` remakes them.

**The pull request is https://github.com/Ritapossible/Rowgate/pull/1, and it is red** — Bob's
contract test for `Billing!E9` is on the branch now, so CI fails on purpose. Open the PR on the
**Files changed** tab, never on Checks: the first PR shot exists to show that the diff looks
innocent. The red check is the last shot, where it is the payoff. Refresh the PR before
recording so no check is still spinning.

**The landing page opens the film.** Its hero already carries the thesis — *The contract they
signed is not in your diff* — so say less over it than you think you need to. Its stat row reads
live from the published run (4 broken · 4/4 proved · 2 skipped), which means the numbers appear
before you explain them. That is fine: treat the first twenty seconds as a trailer, not a lecture.

## Shot list and voice-over

Eleven shots, 3:00 exactly. The subagent shot and the final PR shot are the two that must not
be cut short.

| Time | On screen | Voice-over |
| --- | --- | --- |
| **0:00–0:20** | rowgate.vercel.app. Hold the hero: logo, **"The contract they signed is *not* in your diff."**, the Orders excerpt with `Orders!C14` highlighted. Scroll once to the stat row (4 · 4/4 · 2), then to the seven-step strip and let `office_read`, `Subagents`, `Human gate` pass | "This is Rowgate. It reads the API contract your partner actually signed — a spreadsheet — and turns the rows a release branch breaks into failing tests. Built as a custom mode and a Skill for IBM Bob. Here's the run it just did." |
| **0:20–0:32** | PR #1, **Files changed**. Scroll the five files: `orders.py` 201 → 202, `billing.py` dropping `currency`, `auth.py` swapping the error | "Here's the pull request it was pointed at. Three commits, five files, every change defensible on its own. Nothing in the repository's own test suite objects." |
| **0:32–0:46** | `api-contract.xlsx`: the Cover sign-off block, then Orders. Pause on the `↳ ORD-011` inherited rows and the merged `Billing!D3` | "But this is what the partner signed. Forty-one rules — inherited rows, merged cells, rows that are only planned. None of it appears in that diff." |
| **0:46–0:58** | Bob IDE: switch to **Contract Gate** mode, type `/rowgate feature/fast-checkout` | "One command." |
| **0:58–1:12** | `office_read` on the workbook, then the **Plan**; click approve | "Bob opens the spreadsheet directly and plans which signed rows this diff can touch. Then it stops and waits for me." |
| **1:12–1:35** | **Three subagents running in parallel** — hold, do not speed up | "Three subagents check orders, billing and auth at the same time, each in its own clean context." |
| **1:35–1:53** | `tests/contract/` with **four** files named after cells; terminal `run_contract_tests.sh before` → **4 red** | "For every broken cell it writes one test, named after that cell. All four fail on this branch. If Bob had cited the wrong cell, its test would pass and the finding would die — the name is the proof." |
| **1:53–2:15** | The decision prompt: fix `Orders!C14`, `Auth!E5`, `Errors!D6`; record a breaking change for `Billing!E9`. Then the spreadsheet: `Billing!H9 = BREAKING` and the new Changelog row | "Now a human decides. Three get fixed. One is accepted as a breaking change — and Bob writes that decision back into the signed workbook itself." |
| **2:15–2:31** | rowgate.vercel.app/run: a finding card (cell, diff line, red → green), then scroll to **Checked and skipped: `Orders!D11`** | "Everything here is measured, not claimed. And it skipped the rename that only *looks* like a break, because `serialization_alias` keeps the wire name identical." |
| **2:31–2:42** | Numbers card: 2 of 4 reading the diff vs 4 of 4 · 0 false alarms · 6.1 Bobcoins | "I read the diff myself, already knowing where the breaks were, and found two of four in twelve minutes." |
| **2:42–3:00** | **The payoff.** PR #1 → **Checks**, red. Zoom the failure: `FAILED tests/contract/test_billing_E9_invoice_has_currency.py — AssertionError: currency field is required (BIL-007)`, `1 failed, 17 passed`. End card: logo, rowgate.vercel.app, `bob_sessions/` | "And now the branch can't merge. Not because a model objected — because a row a person signed in a spreadsheet is a test, and it fails. The model read the sheet once. The tests stay." |

## Edit list

0. The opening is the only shot that is not from the run. Record it last, once the site shows
   the run of record, and keep the browser chrome clean — no bookmarks bar, no other tabs visible.
1. Cut Bob's thinking time down to 1–2 seconds per step. Keep the moment each result appears.
2. Speed up long scrolls ×2. Never speed up the subagent panel; let it breathe for about 5 seconds.
3. Zoom (crop) into: the plan, the subagent panel, a test file name, the red pytest line, `Billing!H9`.
4. Add small captions for cell names when they appear (`Orders!C14`, `Billing!E9`, `Auth!E5`,
   `Errors!D6`, `Orders!D11`).
5. Numbers card at 2:31: a plain frame in the site colours (forest-black background, cream text).
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
