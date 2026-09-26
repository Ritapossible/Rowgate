# Prompt for the local agent: operate the recorded Rowgate run

Paste everything below the line into Claude Code on the machine running Bob IDE.

---

You are operating the machine for the **recorded** Rowgate run for the IBM Bob 2.0
Hackathon. Read `RUNBOOK.md`, `MEMORY.md` §6 and `submission/VIDEO.md` first.

## The one rule

**IBM Bob does the analysis. You do not.** Never write or edit a file under
`tests/contract/`, never edit `out/findings.json`, never fix anything in `app/` or
`contract/api-contract.xlsx` yourself, and never hand-correct a cell reference Bob
produced. If Bob gets something wrong, say so and stop — a judge comparing the
transcript with the diff must see that every finding came from Bob. Your job is
git, scripts, screenshots and checking.

## Budget

**27.66 Bobcoins left. A run costs about 6.1.** That is four runs. Do not spend any
on rehearsals — task01 already proved Bob reads the `↳ ORD-011` inheritance and the
merged `Billing!D3` correctly. One recorded run, two in reserve.

## 1. Prepare (no coins)

```bash
git checkout main && git pull
git checkout feature/fast-checkout && git merge main
scripts/reset_demo.sh --force      # reverts tracked files; commit tooling changes first
```

`reset_demo.sh` must end with `Ready.` Then confirm the branch is in the
pre-run state — it should still contain the planted breaks:

```bash
grep -n "HTTP_202_ACCEPTED" app/orders.py     # expect a hit
grep -n "status_code=400" app/auth.py         # expect a hit
ls tests/contract/                            # expect .gitkeep only
```

If any of those is wrong, stop and report. Then open the pull request
`feature/fast-checkout` → `main` on GitHub if it is not open. **Never merge it.**

## 2. The run (about 6.1 coins) — the user drives Bob, you watch

The user runs `/rowgate feature/fast-checkout` in Contract Gate mode with the screen
recorder going. Watch the repo and tell them, out loud and immediately, if:

- **Cell citations land in the wrong column.** Breaks must cite the cell that states
  the broken rule, and skips must cite the field or type cell:

  | Expected | Not |
  | --- | --- |
  | `Orders!C14` (HTTP status) | — |
  | `Billing!E9` (Field) | — |
  | `Auth!E5` (HTTP status) | — |
  | `Errors!D6` (Body shape) | `Auth!D5` — that is the Scenario column |
  | `Orders!D11` skipped (Field) | `Orders!H11` — that is Contract status |
  | `Orders!E5` skipped (Type) | `Orders!H5` — that is Contract status |

  The published run got the last three wrong. `.bob/skills/rowgate/SKILL.md` now has a
  citation table that should fix it. **If they drift again, stop the run and report** —
  do not fix the references yourself.

- **The three subagents do not run at the same time.** The single frame showing all
  three running is the evidence for "parallel subagents". If they run in sequence,
  stop and report.

- **The Changelog row has the wrong date or approver.** It must be today's date and a
  person's name, not a branch name.

The decisions are the user's: **F1 fix code · F2 record breaking change · F3 and F4 fix
code.** Do not answer for them.

## 3. Keep it — in this order, before anything else

The last run was published and then thrown away, so the site advertised five commits
that do not exist on GitHub. **Do not let that happen again.** The moment Bob finishes
and `render_dossier.py` reports 0 problems:

```bash
git add tests/contract app contract .bob
git commit -m "Rowgate run: contract tests and approved decisions"
git push -u origin feature/fast-checkout
```

**Commit and push the branch BEFORE publishing.** `export_site.py` reads
`git log main..feature/fast-checkout`, so a commit that does not exist yet cannot
appear on the Run page, and a commit that is never pushed becomes a phantom.

Then, and only then:

```bash
scripts/publish_run.sh
```

**Do not run `scripts/reset_demo.sh` after this.** The recorded run stays on the branch.

## 4. Screenshots

In Bob: **Views and More Actions → History**, open the task, click the task header to
show the consumption summary, screenshot it, then **Export task history**. Save both as:

```
bob_sessions/ibm-hackathon-lablab_task03_recorded-run.png
bob_sessions/ibm-hackathon-lablab_task03_recorded-run.md
```

If the capture is a low-resolution frame and the cell references are unreadable, run
`python scripts/clean_shots.py <folder> <dest.png>=<source.jpg>` to sharpen it. Open
the exported `.md` and check it contains no API keys before committing.

Report the task's final Bobcoin cost so the ledger in `MEMORY.md` §6 can be updated.

## 5. Verify (no coins)

```bash
git checkout main && git pull
python scripts/run_numbers.py
scripts/check_submission.sh
```

`check_submission.sh` must end with **`Ready to submit.`** It now fails if the tests
Bob cited are not committed on the branch, if a commit shown on the Run page is not an
ancestor of it, or if the run records workbook changes the workbook does not have. If
any of those is red, the run was not kept properly — report it, do not paper over it.

Finally, confirm `rowgate.vercel.app/run` shows the new run once Vercel deploys `main`
(hard-refresh; the site caches `site.json`). If Vercel says rate-limited, redeploy the
latest `main` deployment by hand from the dashboard.

## Report back

- The finding count and every cited cell, so it can be checked against the table above
- Whether the three subagents ran in parallel
- The task's Bobcoin cost
- The `check_submission.sh` output verbatim
