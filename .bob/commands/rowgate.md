---
description: Gate a release branch against the signed contract workbook
argument-hint: <branch>
---
Run the rowgate Skill on branch $1 (current branch if empty) against `contract/api-contract.xlsx`, base `main`. Start with `scripts/collect_diff.sh`, read the workbook with office_read, then present your plan and wait for my approval.
