# Bob task session reports

One screenshot of the task consumption summary and one exported task history per Bob task,
named `ibm-hackathon-lablab_task<NN>_<description>`, as the hackathon guide requires. Team
`ibm-hackathon-lablab`, Enterprise plan, region US East.

| Task | Bob task id | What it was | Final cost |
| --- | --- | --- | --- |
| task01 | `ee9a0d46…` | Workbook rehearsal, then a dry run, in one task | 6.24 |
| task02 | `b0a94399…` | A full `/rowgate` run, published; then, **continuing in the same task**, the run of record — citations re-cited by Bob on request | see `MEMORY.md` §6 |

**Two tasks, not three.** The run of record was not a new Bob task: it continued task02's, so
there is one screenshot and one exported history for both. `task02_rowgate-run.md` is the
complete export and contains both runs, including the citation correction. An earlier note here
claimed a separate "task03" at 6.02 — that was wrong, and the cost of task02 is still to be read
off the task header; `MEMORY.md` §6 explains why the two readings taken so far conflict.

**A Bob task's header shows its cost *so far*.** A frame captured mid-task is always lower than
the total: task01's shot reads 1.50 and task02's about 4.49. Because the run of record continued
task02, task02's screenshot was taken before that work and understates it. The running balance
is in `MEMORY.md` §6.

The three subagents ran **in parallel** in the run of record — confirmed on screen while it was
recorded, which is the evidence for the parallel-subagents claim.

## The human corrections, stated plainly

Nothing in this project hides a human edit behind Bob's name.

1. **The Changelog date — a hand edit, including in the run of record.** Bob wrote
   `2025-07-14` into the new Changelog row in task01, in task02's first run and again in the run of record: a date from
   its own context, not today's. Before the run of record the Skill was changed to tell it to run
   `date +%F` and copy the output; it wrote `2025-07-14` anyway, so it is not reading the clock
   it was given. `Changelog!A6` was therefore set to `2026-09-26` by hand, and F2's
   `workbook_edit.cells` in `findings.json` updated to match so the renderer still measures the
   claim against the file. **That one cell is a human edit, not Bob's output.** The
   screenshot and transcript still show `2025-07-14`; the disagreement is deliberate and is
   this note.

2. **The cited cells — corrected by Bob, not by hand.** task02 cited `Auth!D5`, `Orders!H11`
   and `Orders!H5`. `D` is the Scenario column and `H` is the Contract status column; the rule
   each finding is about is stated in `Errors!D6`, `Orders!D11` and `Orders!E5`. `SKILL.md`
   gained a table naming which cell states each kind of rule. In the run of record Bob repeated the same
   three mistakes on its first pass, was told which Skill rule it had broken, and re-cited them
   itself — renaming its own test file to
   `test_errors_D6_invalid_secret_error_envelope.py` and putting `Auth!E5` in `related_cells`.
   The references in the run of record are **Bob's**, never hand-edited.

The findings, verdicts, tests and code fixes in the run of record are Bob's throughout. The
single exception is the date cell in item 1.
