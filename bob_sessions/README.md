# Bob task session reports

One screenshot of the task consumption summary and one exported task history per Bob task,
named `ibm-hackathon-lablab_task<NN>_<description>`, as the hackathon guide requires. Team
`ibm-hackathon-lablab`, Enterprise plan, region US East.

| Task | What it was | Final cost | Run of record? |
| --- | --- | --- | --- |
| task01 | Workbook rehearsal, then a dry run, in one task | 6.24 | no — thrown away on purpose |
| task02 | Full `/rowgate` run | 6.10 | superseded |
| task03 | Full `/rowgate` run, citations re-cited by Bob on request | 6.02 | **yes** |

**Read the coin figure from this table, not from the screenshots.** A Bob task's header shows
its cost *so far*, so a frame captured mid-task is always lower than the total: task01's shot
reads 1.50 and task02's reads about 4.49. The totals above were read off the finished task
headers in History. 18.36 of the 40 Bobcoins were spent, leaving 21.64; the running balance is
in `MEMORY.md` §6.

In task03 the three subagents ran **in parallel** — confirmed on screen while the run was
recorded, which is the evidence for the parallel-subagents claim.

## The human corrections, stated plainly

Nothing in this project hides a human edit behind Bob's name.

1. **The Changelog date — a hand edit, including in the run of record.** Bob wrote
   `2025-07-14` into the new Changelog row in task01, task02 and again in task03: a date from
   its own context, not today's. Before task03 the Skill was changed to tell it to run
   `date +%F` and copy the output; it wrote `2025-07-14` anyway, so it is not reading the clock
   it was given. `Changelog!A6` was therefore set to `2026-09-26` by hand, and F2's
   `workbook_edit.cells` in `findings.json` updated to match so the renderer still measures the
   claim against the file. **That one cell is a human edit, not Bob's output.** The task03
   screenshot and transcript still show `2025-07-14`; the disagreement is deliberate and is
   this note.

2. **The cited cells — corrected by Bob, not by hand.** task02 cited `Auth!D5`, `Orders!H11`
   and `Orders!H5`. `D` is the Scenario column and `H` is the Contract status column; the rule
   each finding is about is stated in `Errors!D6`, `Orders!D11` and `Orders!E5`. `SKILL.md`
   gained a table naming which cell states each kind of rule. In task03 Bob repeated the same
   three mistakes on its first pass, was told which Skill rule it had broken, and re-cited them
   itself — renaming its own test file to
   `test_errors_D6_invalid_secret_error_envelope.py` and putting `Auth!E5` in `related_cells`.
   The references in the run of record are **Bob's**, never hand-edited.

The findings, verdicts, tests and code fixes in the run of record are Bob's throughout. The
single exception is the date cell in item 1.
