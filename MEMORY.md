# Rowgate — Project Memory

Durable context for anyone (human, Bob, or another agent) picking up this repo. Read this
before changing scope or wording. Update it whenever a fact is verified, a decision is made,
or Bobcoins are spent.

---

## 1. The event

| Item | Value |
| --- | --- |
| Hackathon | IBM Bob 2.0 Hackathon (lablab.ai) — https://lablab.ai/ai-hackathons/ibm-bob-2-hackathon |
| Build window | 25 Sep 2026 11:00 EDT → 27 Sep 2026 11:00 EDT (16:00 WAT → 16:00 WAT) |
| Submission deadline | 27 Sep 2026, 15:00 UTC (16:00 WAT) |
| Prize pool | $12,000 |
| Registered | ~15,700 |
| Last round (June 2026) | 5,628 participants, 503 submissions |
| Judging (per hackathon guide, relayed) | Application of Bob, business value, originality, presentation |
| Hard rules (per hackathon guide, relayed) | 40 Bobcoins, no refill · original work · MIT license · `bob_sessions/` screenshots of Bob task summaries or disqualified |

"Relayed" = taken from the official guide via a second source; re-read the guide at kickoff.

## 2. Verified facts about Bob (with sources)

| Fact | Source |
| --- | --- |
| Custom **Workflow** authoring is not available; only built-in and Premium Package workflows (Java, IBM i, IBM Z) | Bob V2 announcement — https://bob.ibm.com/blog/bob-v2-release-announcement/ |
| Non-agentic steps and the Select Action gate live in Premium Package workflows | https://bob.ibm.com/docs/ide/premium-packages/bob-for-i/workflows · Heidloff write-up |
| Skills: `<project>/.bob/skills/<name>/SKILL.md`, YAML frontmatter (`name`, `description`), may bundle scripts; activation asks approval by default | https://bob.ibm.com/docs/ide/features/skills |
| Slash commands and custom modes exist since 1.0.1 | Changelog — https://bob.ibm.com/docs/ide/changelog |
| Subagents (parallel, isolated context) since 2.0.0; modes can restrict which subagents run; each spawn needs explicit approval | Changelog 2.0.0 |
| Reads `.docx`, `.pdf`, `.xlsx` natively; Ask / Plan / Agent modes; parallel tool calls; single self-contained HTML summary | Bob V2 announcement |
| `office_read` and `office_edit` for `.docx`, `.xlsx`, `.pptx` — **2.1.0 (Aug 2026)**. Edit = set values, add/remove content, find-and-replace. Comments not mentioned | Changelog 2.1.0 |
| Hackathon account: invite email from the IBM Bob team **at the start of the hackathon** to the registration email ("added as a team member to ibm-hackathon-xxx", Enterprise plan). 40 Bobcoins auto-applied, no top-up. Sign in with an IBMid on the registration email. Usage shown in Bob IDE → Settings → General. Use only the `ibm-coding-challenge-xxx` instance during the event | Hackathon guide (May 2026 edition) — https://watsonx-hackathons-2026.s3.us.cloud-object-storage.appdomain.cloud/Lablab-IBM-Bob-hackathon-guide-May-2026.pdf |
| Separate personal free trial: 50 Bobcoins for 30 days | https://bob.ibm.com/trial |
| 2.2.0 (Sep 2026): live subagent tool results in chat; `plugins/` subdirectory for skills, modes, rules, MCP; HTTPS hook handlers | Changelog 2.2.0 |

### Unverified — check at kickoff (Fri 25 Sep)

- [ ] Which Bob version the hackathon accounts run (need ≥ 2.1.0 for `office_edit`).
- [ ] Slash command file location (`.bob/commands/`?) and format.
- [ ] Custom mode file location/format and how to restrict subagents in it.
- [ ] Whether `plugins/rowgate/` packaging works.
- [ ] Whether `office_edit` can append a row to another sheet (Changelog) in one call.
- [ ] Bobcoin cost of one subagent spawn and of one full run.
- [ ] Rules on pre-event work: confirm at kickoff that non-AI scaffolding built before 16:00 WAT is fine (see D12).
- [ ] Whether kickoff changes the Bobcoin budget or unlocks workflow authoring. If authoring unlocks, reconsider; do not plan on it.

## 3. Decisions (and why)

| # | Decision | Why |
| --- | --- | --- |
| D1 | Build Rowgate, not Clause | One document, one branch, one red test. Clause (xlsx + pdf + docx) was too wide for 48h solo |
| D2 | Never call it a "workflow" in the video, README, or submission | IBM judges know custom workflow authoring isn't available; the claim would cost the Bob-usage score |
| D3 | Implementation = Contract Gate **mode** + Rowgate **Skill** + `/rowgate` + scripts + Plan→Agent + parallel subagents + `office_read`/`office_edit` | All user-authorable; same building blocks that won last round (Pedigree) |
| D4 | Pitch: "Bob reads the signed spreadsheet once and writes tests that stay in the repo" | Answers "why AI?": Bob does the fuzzy reading once, then pytest guards every later PR at zero cost |
| D5 | Tests are named after the cell (`test_orders_C14_...`) | The test name is the citation; wrong citation = failing demo, which is the credibility claim |
| D6 | Bob writes `findings.json` (fixed schema); a script renders the HTML | Rendering is the same every run and costs no Bobcoins |
| D7 | Breaking-change recording = Status cell `BREAKING` + new Changelog row, via `office_edit` | Comments aren't a documented `office_edit` operation |
| D8 | Messy workbook (6 sheets, merged headers, notes, 40+ rows) plus one decoy the tool must skip | "3 planted, 3 found" looks rigged; skipping a lookalike shows precision |
| D9 | Decoy = `request_id` renamed `req_id` with a serialization alias, so the wire format is unchanged | Grounded in a real contract fact; a diff skim flags it, a correct reading doesn't |
| D10 | FastAPI + pytest demo service | Smallest stack where status codes and response fields are explicit |
| D11 | No web app, no watsonx, no OpenAPI | Score comes from Bob being the engine; scope is the strategy |
| D12 | Non-AI scaffolding (service, workbook, scripts, renderer) built before kickoff; every Bob step waits for the hackathon account | lablab's general rule allows libraries and non-AI scaffolding; the guide adds nothing stricter. Bob sessions must be on the `ibm-coding-challenge-xxx` instance for valid `bob_sessions/` evidence. Watch kickoff for rule changes |
| D13 | Bob never writes test outcomes; `run_contract_tests.sh before/after` saves pytest reports and the renderer reads them | Red → green is measured, not claimed |
| D14 | Test files named `tests/contract/test_<sheet>_<cell>_<what>.py`; renderer rejects a mismatch | Enforces D5 mechanically |

## 4. Positioning

- **One-liner:** Rowgate checks a release branch against the signed API spreadsheet and writes the contract test that fails when a row breaks.
- **Why not OpenAPI / Pact / Schemathesis?** Partner integrations in banking, telco and insurance are signed as spreadsheets and never become OpenAPI. Rowgate is for the contract nobody converted.
- **Why not another review bot?** Review bots emit opinions. Rowgate emits a cell citation and a test that can be proven wrong.
- **Precedent:** Pedigree won 1st in June 2026 with a custom mode + Skill + MCP + one verifiable page ("Code Passport"). Atlas (repo-as-city-map) was 2nd.
- **Demo proof:** eye review of the diff finds 1 of 3 breaks and flags the decoy. Rowgate finds 3 of 3, skips the decoy with a reason, test red → green.

## 5. Words to use / avoid

| Use | Avoid |
| --- | --- |
| Contract Gate mode, Rowgate Skill, `/rowgate` | "Bob workflow", "workflow engine", "Select Action" |
| Plan mode approval, subagent approval | "zero-token steps" as a Bob feature (they're our scripts) |
| "cites the cell", "writes the test" | "AI-powered review", "copilot" |

## 6. Bobcoin ledger (40 total, no refill)

| When | Mode | What | Coins | Remaining |
| --- | --- | --- | --- | --- |
| — | — | start | 0 | 40 |

Budget: rehearsal ≤ 8 · dry run 1 ≤ 10 · dry run 2 ≤ 10 · recorded run ≤ 8 · reserve ≥ 4.
If dry run 1 costs more than 12, cut to two subagents (see ARCHITECTURE §8).

## 7. Session log

| When (WAT) | What happened |
| --- | --- |
| 24 Sep | Idea chosen (Rowgate). Bob capability limits verified. Repo created; ARCHITECTURE, MEMORY, PLAN written. |
| 25 Sep AM | Phase 1 scaffold built before kickoff (D12): service, 41-rule workbook, branch with 3 breaks + decoy, scripts, renderer. 10 tests green on main and branch. 0 Bobcoins used. |
