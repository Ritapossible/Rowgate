# Bob task session reports

One screenshot of the task consumption summary and one exported task history per Bob task,
named `ibm-hackathon-lablab_task<NN>_<description>`, as the hackathon guide requires. Team
`ibm-hackathon-lablab`, Enterprise plan, region US East.

| Task | What it was | Final cost | Run of record? |
| --- | --- | --- | --- |
| task01 | Workbook rehearsal, then a dry run, in one task | 6.24 | no — thrown away on purpose |
| task02 | Full `/rowgate` run | 6.10 | superseded |

**Read the coin figure from this table, not from the screenshots.** A Bob task's header shows
its cost *so far*, so a frame captured mid-task is always lower than the total: task01's shot
reads 1.50 and task02's reads about 4.49. The totals above were read off the finished task
headers in History. The running balance is in `MEMORY.md` §6.

## Two human corrections, stated plainly

Nothing in this project hides a human edit behind Bob's name.

1. **The Changelog date.** In task02 Bob wrote `2025-07-14` into the new Changelog row — a
   date from its own context, not today's. That is visible in the task02 screenshot. The date
   was corrected to `2026-09-26` before the run was published, so the screenshot and
   `run.json` disagree on that one cell. `.bob/skills/rowgate/SKILL.md` now tells Bob to read
   the date from `date +%F` instead of inventing one.

2. **The cited cells.** task02 cited `Auth!D5`, `Orders!H11` and `Orders!H5`. `D` is the
   Scenario column and `H` is the Contract status column; the rule those findings are about is
   stated in `Errors!D6`, `Orders!D11` and `Orders!E5`. The findings themselves were right —
   the references pointed at the wrong column of the right row. `SKILL.md` now carries a table
   telling Bob which cell states each kind of rule. The references were **not** hand-edited.

Both are why there is a run of record separate from task02.
