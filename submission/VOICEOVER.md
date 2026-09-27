# Voice-over: read sheet

Record this in one take per block, in a quiet room, phone voice memo is fine. Leave two
seconds of silence between blocks so the editor has something to cut on.

**Pace:** every block below is written to land at about **2 words per second**, which is an
unhurried speaking voice. The word count and the target length are given so you can check
yourself — if a block runs long, drop the sentence marked *(cut first)* rather than speeding up.

**Tone:** you are showing a colleague something you built, not selling. Flat and specific beats
enthusiastic. The numbers do the persuading.

---

### 1 · Landing page — 0:00–0:20 · 44 words

> This is Rowgate. It reads the API contract your partner actually signed — a spreadsheet — and
> turns the rows a release branch breaks into failing tests. Built as a custom mode and a Skill
> for IBM Bob. Here's the run it just did.

Let "a spreadsheet" land. It is the surprising word in the sentence.

### 2 · The pull request — 0:20–0:32 · 27 words

> Here's the pull request it was pointed at. Three commits, five files, every change defensible
> on its own. Nothing in the repository's own test suite objects.

### 3 · The workbook — 0:32–0:46 · 27 words

> But this is what the partner signed. Forty-one rules — inherited rows, merged cells, rows that
> are only planned. None of it appears in that diff.

### 4 · One command — 0:46–0:58 · 26 words

> One command. Contract Gate is a custom mode; the Rowgate Skill is the procedure it follows.
> *(cut first)* Both live in the repository, so anyone can run this.

### 5 · Plan and approve — 0:58–1:12 · 24 words

> Bob opens the spreadsheet directly and plans which signed rows this diff can touch. Then it
> stops and waits for me.

### 6 · Subagents — 1:12–1:35 · 45 words

> Three subagents check orders, billing and auth at the same time, each in its own clean context.
> That's the part one pass over a diff can't do — three resources, three contexts, no crosstalk,
> and one verdict per signed row.

### 7 · Four red tests — 1:35–1:53 · 40 words

> For every broken cell it writes one test, named after that cell. All four fail on this branch.
> If Bob had cited the wrong cell, its test would pass and the finding would die. The name is
> the proof.

### 8 · The human decides — 1:53–2:15 · 36 words

> Now a human decides. Three get fixed. One is accepted as a breaking change — and Bob writes
> that decision back into the signed workbook itself, setting the status cell and adding a
> changelog row.

### 9 · The run page — 2:15–2:31 · 32 words

> Everything here is measured, not claimed. And it skipped the rename that only looks like a
> break, because the serialization alias keeps the wire name identical.

Say "serialization alias" as two plain words, not as code.

### 10 · The numbers — 2:31–2:42 · 22 words

> I read the diff myself, already knowing where the breaks were, and found two of four in
> twelve minutes.

The admission is the point. Don't soften it.

### 11 · The payoff — 2:42–3:00 · 44 words

> And now the branch can't merge. Not because a model objected — because a row a person signed
> in a spreadsheet is a test, and it fails. The model read the sheet once. The tests stay.

Pause a full beat after "and it fails."
