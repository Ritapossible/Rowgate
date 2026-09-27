# Voice-over: read sheet

Written for the footage that exists: **three clips — the website, the Bob IDE subagent run, and
the pull request.** The eleven-shot list in `VIDEO.md` assumes footage of the workbook, the tests
going red and the decision prompt; none of that was captured, so the website clip carries it
instead. Everything claimed below is visible in one of the three clips or on the site.

Record each block as its own take, in a quiet room, phone voice memo is fine. Leave two seconds
of silence between blocks. Pace is about **two words per second** — unhurried. Word counts are
given so you can check a block without a stopwatch.

Total: **2 minutes 20 seconds** of speech. If your clips run longer, stretch the pauses rather
than the words.

---

## Clip 1 · The website — about 60 seconds

Land on the hero, scroll slowly: headline, the stat row, the seven-step strip, then the Run page
— a finding card, then "Checked and skipped".

### 1a · over the hero · 24 words · 0:00–0:12

> This is Rowgate. It reads the API contract your partner actually signed — a spreadsheet — and
> turns the rows a release branch breaks into failing tests.

*Let "a spreadsheet" land. It's the surprising word.*

### 1b · over the stat row and the step strip · 46 words · 0:12–0:35

> A partner signs a document. Forty-one rules: status codes, required fields, error bodies.
> Then a branch quietly changes one, the diff looks fine, the tests stay green, and nobody finds
> out until the partner's system rejects it. That document never enters code review.

### 1c · over the Run page, on a finding card · 42 words · 0:35–0:55

> Here's a real run. Four signed cells broken on one branch. Every finding cites the exact cell,
> shows the line of code that breaks it, and comes with a test named after that cell — which
> fails, then passes once it's fixed.

### 1d · over "Checked and skipped" · 30 words · 0:55–1:10

> It also knows what not to flag. A field renamed in Python, but the alias keeps the wire name
> identical, so the contract still holds. Skipped, with the reason.

---

## Clip 2 · Bob IDE, the subagents — about 45 seconds

Hold on the three subagents running together. This is the clip judges score "application of Bob"
from, so don't rush it.

### 2a · as the run starts · 34 words · 1:10–1:27

> This is IBM Bob. Rowgate is a custom mode and a Skill — one command. Bob opens the spreadsheet
> directly, plans which signed rows the diff can touch, and waits for me to approve.

### 2b · over the three subagents · 44 words · 1:27–1:50

> Then three subagents check orders, billing and auth at the same time, each in its own clean
> context. That's the part one pass over a diff can't do — three resources, no crosstalk, one
> verdict per signed row.

### 2c · as it finishes · 40 words · 1:50–2:10

> Four breaks, four failing tests. Then a human decides each one. Three get fixed in code. One
> is accepted as a breaking change — and Bob writes that back into the signed workbook itself.

---

## Clip 3 · The pull request — about 25 seconds

Files changed first if you have it, then the red check. Zoom the failure line.

### 3a · over the diff, if you have it · 22 words · 2:10–2:20

> This is the pull request it was pointed at. Three commits, five files, every change defensible
> on its own.

*If your clip opens straight on the red check, skip 3a and go to 3b.*

### 3b · over the red check · 44 words · 2:20–2:40

> And now it can't merge. Not because a model objected — because a row a person signed in a
> spreadsheet is a test, and it fails. The model read the sheet once. The tests stay, and every
> future pull request is checked for free.

*Pause a full beat after "and it fails."*

### 3c · over the end card · 26 words · 2:40–2:50

> I read that diff myself, already knowing where the breaks were, and found two of four in
> twelve minutes. Rowgate found all four.

*The admission is the point. Don't soften it, and don't speed up.*

---

## If you are short of time

Cut **1b** and **3a**. That loses 68 words, about 35 seconds, and the film still makes its whole
argument: what it is, a real run, the subagents, the red check, the honest comparison.

Do not cut **2b** or **3b**.
