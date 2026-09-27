# lablab.ai submission form — paste-ready

Every field below is written to the form's limits. Character counts are checked; paste them
as they are. Categories and Technologies are pick-lists, so they are guidance, not text.

---

## Submission Title  (46 / 50)

Rowgate: the signed contract as a release gate

---

## Short Description  (215 / 255, min 50)

Rowgate reads the API contract your partner actually signed - a spreadsheet - cites the exact cell a release branch breaks, and writes the failing test that proves it. Built with IBM Bob. A human decides what ships.

---

## Long Description  (2808 / 4000 chars, 499 words — the prompt asks for 500 or less)

THE PROBLEM

In banking, telco and insurance, partner API integrations are agreed in a signed spreadsheet: status codes, required fields, error body shapes, one row per rule. That document is the contract. It is almost never turned into OpenAPI, and it never enters code review.

So a branch changes a status code from 201 to 202, or drops a currency field, and the pull request looks fine. Every change is defensible on its own and the repository's own tests stay green. Nothing in the diff says a signed row just broke. The cost lands after release as failed checkouts and rejected invoices, and nobody can point at the moment it happened.

THE SOLUTION

Rowgate is a release gate that reads the spreadsheet. Point it at a branch and each finding returns three things: the cell that broke, such as Orders!C14; a failing test named after it; and a human decision.

The cell citation is what makes it checkable. A review bot returns an opinion you have to trust. Rowgate returns a claim you can verify in two clicks: open the cell, read the signed rule, run the test. Every test must fail on the branch before the finding stands, so a wrong citation exposes itself.

The human then chooses per finding: fix the code, or accept it as a breaking change. Accepting is not a comment thread: Rowgate writes it back into the signed workbook - the status cell becomes BREAKING and a changelog row is added - so the spreadsheet stays the source of truth instead of drifting from the code.

WHO USES IT

Release owners and backend teams shipping against a partner contract. You run one command, approve a plan, decide per finding. The output is a web page and a single-file dossier where every number is measured, not asserted: code cut from the diff, pass and fail from pytest, workbook edits compared against git.

WHAT MAKES IT DIFFERENT

Most AI review tools summarise a diff. Rowgate brings in the document the diff cannot see, and it knows what not to flag. It skipped two changes that look like breaks: a field renamed from request_id to req_id, where a serialization alias keeps the wire name identical, and a status value inside the allowed enum. Each skip is shown with its reason. Zero false alarms matters as much as four true ones.

DOES IT WORK

Three commits broke four signed cells. Rowgate found all four, proved each with a failing test, skipped the two lookalikes, and cost 6.1 Bobcoins. Reading the same diff by hand found two of four in twelve minutes - and that was the author, who already knew where the breaks were.

The tests then stay in the repository, so every later pull request is checked by plain pytest in CI, with no model and no tokens. Our demo pull request is red today on the test for the row a human recorded as breaking: a spreadsheet row, written by a person, blocking a merge.

---

## IBM Bob Usage Statement  (3077 / 4000 chars)

Rowgate is not a wrapper around a Bob prompt. It is a procedure that Bob executes, and every judgment in the result is Bob's. IBM Bob 2.2.0, team ibm-coding-challenge-2, region US East. IBM watsonx.ai and watsonx Orchestrate are not used.

HOW IT IS BUILT IN BOB

Custom mode. "Contract Gate" is a workspace custom mode that constrains Bob to the four paths a run touches and forbids editing the application code outside an approved decision. Its definition is in the repo at rowgate/bob/contract-gate-mode.md.

Skill. The procedure lives in .bob/skills/rowgate/SKILL.md. It encodes the workbook's structure - which column states which kind of rule, how inherited rows resolve, that the Billing HTTP status cell is a merged range, that the Errors sheet is shared, and that PLANNED rows must be ignored - plus the naming rule for tests and an explicit list of things Bob must never do.

Slash command. /rowgate <branch> starts a run.

Custom Workflow authoring is not available in Bob 2.x, so Rowgate is deliberately a mode plus a Skill plus a command, and we never describe it as a workflow.

WHAT BOB DOES IN A RUN

1. office_read on contract/api-contract.xlsx. Bob opens the signed spreadsheet directly - 41 rules across 6 sheets - and resolves merged cells and inherited rows. We rehearsed this before spending on a run: Bob correctly reported that the POST /orders field rows inherit their status from ORD-011, and that BIL-007's status lives in the merged cell Billing!D3.

2. Plan mode. Bob maps the changed files to contract rows and proposes which rows the diff can touch. Nothing is written until a human approves.

3. Three parallel subagents, one per resource - orders, billing, auth - each with its own clean context, each returning a verdict per signed row. This is the step a single pass over a diff cannot do.

4. Agent mode writes one contract test per broken cell, named after the cell, for example tests/contract/test_orders_C14_create_returns_201.py. The test must fail on the branch or the finding does not stand, which makes a wrong citation self-detecting.

5. Human decision per finding, inside Bob.

6. office_edit writes the accepted breaking change back into the signed workbook: Billing!H9 set to BREAKING and a new Changelog row.

The mechanics around Bob are plain scripts with no model and no tokens: capturing the diff, running pytest, rendering the dossier.

EVIDENCE AND HONESTY

Two Bob tasks, 19.22 Bobcoins of the 40 allowed. Consumption screenshots and exported task histories are in bob_sessions/.

Bob's citations drifted in an early run, pointing at the Contract status column instead of the cell stating the rule. We fixed the Skill with a table naming which cell states each kind of rule; in the run of record Bob repeated the mistake once, was told which Skill rule it had broken, and re-cited the findings itself, renaming its own test file. Those references are Bob's, not hand-edited. The one human edit anywhere in the output - a date Bob invented in the changelog row - is documented in bob_sessions/README.md rather than hidden.

---

## Categories (pick-list)

Search the dropdown for these, in order of fit:

1. **Agent Builder track** — Rowgate is a custom mode, a Skill and three parallel subagents.
   If the hackathon scores by track, this is the one it belongs in.
2. **Developer Tools** / **Productivity** / **Testing** — whichever of these the list offers.
3. **Assistant** — only if nothing better appears.

Do not pick Art, Advertising, Automotive or Augmented Reality.

## Technologies Used (pick-list)

Search for and select, in this order:

1. **IBM Bob** (search "IBM" or "Bob" — this one is not optional)
2. **Python**
3. **FastAPI**
4. **React**
5. **Vercel**

If the list has **pytest**, **openpyxl**, **TypeScript** or **Vite**, add them. Do **not** add
watsonx.ai or watsonx Orchestrate — the project does not use them, and claiming a technology
that is not in the repository is the kind of thing a judge checks.

---

## Additional Information  (1900 / 2000)

VERIFY IT IN 60 SECONDS

1. rowgate.vercel.app/run - the published run. Every finding cites a cell, shows the diff line, and names its test. Nothing here is typed by hand; it is exported from the run's own output.
2. rowgate.vercel.app/dossier.html - the same run as one self-contained file.
3. github.com/Ritapossible/Rowgate/pull/1 - the pull request under review. CI is RED on purpose: test_billing_E9_invoice_has_currency fails because a human accepted that break instead of fixing it, and the workbook records it. 1 failed, 17 passed. Please do not merge it; the branch carries the planted breaks the demo depends on.
4. bob_sessions/ - consumption screenshots and exported task histories for both Bob tasks.
5. .bob/skills/rowgate/SKILL.md - the procedure Bob follows.

THINGS WE'D RATHER YOU HEAR FROM US

- The human baseline (2 of 4 breaks found in 12 minutes) was done by the author, who already knew where the breaks were. It flatters the manual comparison and still loses. A cold reviewer would not do better.
- In an early run Bob cited the wrong column - the Contract status cell instead of the cell stating the rule. We fixed the Skill with a table naming which cell states each kind of rule. In the run of record Bob made the mistake once more, was told which Skill rule it had broken, and re-cited the findings itself, renaming its own test file. Those references are Bob's, not hand-edited.
- Exactly one cell anywhere in the output is a human edit: a changelog date Bob invented rather than read from the clock. It is documented in bob_sessions/README.md rather than quietly corrected.

scripts/check_submission.sh is the gate we ran before submitting. It fails if a test the run cites is missing from the branch, if a commit shown on the site is not on it, or if the run claims workbook edits the workbook does not have.

19.22 of 40 Bobcoins used, across two tasks. MIT licensed.

---

## Step 2 and 3 of the form

- Demo: https://rowgate.vercel.app
- Run results: https://rowgate.vercel.app/run
- Repository (MIT): https://github.com/Ritapossible/Rowgate
- Bob session reports: https://github.com/Ritapossible/Rowgate/tree/main/bob_sessions
- Pull request (red on the contract test, do not merge): https://github.com/Ritapossible/Rowgate/pull/1
- Slides: upload `submission/rowgate-slides.pdf`
- Cover image: `web/public/og.png` (1200 x 630)
- Video: paste the link once it is uploaded
