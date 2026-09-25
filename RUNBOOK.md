# Rowgate run: step by step

What to click, what to paste, and when to screenshot. Budget: **40 Bobcoins, no refill.**
Log every step's cost in `MEMORY.md` §6 (Bob IDE → Settings → General shows usage).

**Session reports are required for judging** (hackathon guide, "Exporting Bob task session
reports"). For **every** Bob task you run, including the rehearsal:

1. In Bob's chat panel: **Views and More Actions → History**. Make sure the Rowgate workspace is selected.
2. Open the task, then click the **task header** to show its consumption summary.
3. **Screenshot** the summary → `bob_sessions/ibm-hackathon-lablab_task<NN>_<short-description>.png`,
   for example `ibm-hackathon-lablab_task01_rehearsal.png`, `ibm-hackathon-lablab_task02_rowgate-run.png`.
4. Click **Export task history** → save it beside the screenshot with the same name and `.md`.

The name carries the team, the task number and a short description, so judges can match
each screenshot to its exported history.

Before committing, open each exported `.md` and make sure it contains no API keys or tokens;
`scripts/check_submission.sh` scans for them too. An exposed IBM credential gets the account suspended.

The in-run screenshots listed in step 3 are extra material for the video and slides.

---

## 0. Once: set up your machine (no coins)

Needs Git, Python 3.11+ and Bob IDE. On Windows use **Git Bash** for the `scripts/*.sh` commands.

```bash
git clone https://github.com/Ritapossible/Rowgate.git && cd Rowgate
git fetch origin feature/fast-checkout demo/start
git branch feature/fast-checkout origin/feature/fast-checkout
git branch demo/start origin/demo/start
python -m venv .venv
. .venv/bin/activate            # Windows Git Bash: . .venv/Scripts/activate
pip install -r requirements.txt
scripts/reset_demo.sh --force   # must end with "Ready."
```

## 1. Once: set up Bob (no coins)

1. Open the `Rowgate` folder in Bob IDE, signed in to the **hackathon** team
   **`ibm-hackathon-lablab`** (Settings → General). Never run Rowgate on a personal account.
2. **Skill:** `.bob/skills/rowgate/SKILL.md` is already in the repo. Check Bob lists it
   (Skills panel). If Bob asks to approve it on first use, approve.
3. **Mode:** create a custom mode and paste the fields from
   `rowgate/bob/contract-gate-mode.md`. If Bob writes the mode to a file in the repo, commit it.
4. **Command:** create a slash command and paste `rowgate/bob/rowgate-command.md`. If there is
   no slash-command screen, skip it and use the prompt in step 3 directly.
5. Tell Claude where Bob saved the mode and command files, so the docs can name them.

## 2. Rehearsal in Ask mode (≤ 3 coins)

Ask mode, paste:

> Use office_read on contract/api-contract.xlsx. List the ACTIVE rules on the Orders sheet
> whose HTTP status is inherited, and the rule they inherit from. Then give the address of
> Billing's HTTP status cell for rule BIL-007. No other output.

Expected: the `POST /orders` field rows inherit from **ORD-011** (`Orders!C14` = 201), and
BIL-007's status is the merged cell **Billing!D3** (200). If Bob gets this wrong, tell
Claude before spending more coins. Session report → `ibm-hackathon-lablab_task01_rehearsal`.

## 3. The run (Contract Gate mode)

Before the **recorded** run only:
- Get the human baseline done (`submission/BASELINE.md`), ideally by someone who hasn't seen the project.
- On GitHub, open a pull request from `feature/fast-checkout` into `main`. **Do not merge it.**
  CI runs and shows green: that is the video's opening shot (`submission/VIDEO.md`).
- Start the screen recorder.

Make sure you are on `feature/fast-checkout` and `scripts/reset_demo.sh` says `Ready.`

Type `/rowgate feature/fast-checkout`, or paste:

> Run the rowgate Skill on branch feature/fast-checkout against contract/api-contract.xlsx,
> base main. Start with scripts/collect_diff.sh, read the workbook with office_read, then
> present your plan and wait for my approval.

| Step | What you see | You do | Screenshot |
| --- | --- | --- | --- |
| Plan | Rows per resource | Check it names Orders, Billing, Auth/Errors and ignores PLANNED rows. Approve. | `02-plan.png` |
| Subagents | 3 running **at the same time** | Approve each spawn. **Screenshot while all three show as running**; that single frame is the evidence for "parallel tasks" and "subagents". If Bob runs them one after another, stop and tell Claude. | `03-subagents.png` |
| Tests | 3 files in `tests/contract/`, `run_contract_tests.sh before` red | Check each file name has the cell | `04-tests-red.png` |
| Findings | Summary from `render_dossier.py` | Check: 3 breaks, `Orders!D11` skipped, 0 problems | `05-findings.png` |
| Decide | Bob asks per finding | **F1 Orders!C14: fix code · F2 Billing!E9: record breaking change · F3 Auth!E5: fix code** | `06-decisions.png` |
| Workbook | `office_edit` on Billing and Changelog | Open the .xlsx and look at `Billing!H9` and the new Changelog row | `07-workbook.png` |
| After | `run_contract_tests.sh after`, green for F1 and F3 | Check `render_dossier.py` says 0 problems | `08-green.png` |

Expected result: **3 breaks** (`Orders!C14`, `Billing!E9`, `Auth!E5`), **1 skipped**
(`Orders!D11`, serialization alias), F1 and F3 red → green, F2 recorded as breaking with
`Billing!H9 = BREAKING` and a Changelog row. If any of these differ, stop and tell Claude.

## 4. Keep and publish (no coins)

```bash
git add tests/contract app contract .bob
git commit -m "Rowgate run: contract tests and approved decisions"
git push origin feature/fast-checkout
scripts/publish_run.sh          # exports the run + screenshots to main and pushes main
```

Then check the site's Run page shows the run once Vercel has deployed `main`, and run the
final check on `main`:

```bash
git checkout main && git pull
python scripts/run_numbers.py       # numbers for the slides, video and form
scripts/check_submission.sh         # must end with "Ready to submit."
git checkout feature/fast-checkout
```

## Dry runs

For a practice run, finish at step 3, then throw it away:

```bash
scripts/reset_demo.sh --force
```

For the **recorded** run, do not reset afterwards; do step 4.

## The pull request (for the video)

The pull request you opened before the recorded run updates when step 4 pushes
`feature/fast-checkout`. CI now runs `tests/contract`. With F2 recorded as a breaking change,
its test stays red, so the PR turns red: the signed contract gating the release. That is the
video's closing shot. **Never merge it.**
