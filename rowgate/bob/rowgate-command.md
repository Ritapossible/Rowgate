# /rowgate command (paste into Bob: create slash command)

**Name:** rowgate
**Description:** Gate a release branch against the signed contract workbook.
**Argument:** branch (default: current branch)

**Prompt**

Run the rowgate Skill on branch `$ARGUMENTS` (current branch if empty) against
`contract/api-contract.xlsx`, base `main`. Start with `scripts/collect_diff.sh`, read the
workbook with office_read, then present your plan and wait for my approval.
