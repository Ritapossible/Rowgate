# Human baseline: reading the diff without Rowgate

The video and slides compare Rowgate with an honest manual review. About 15 minutes, no
Bobcoins.

**Who should do it:** someone who has **not** seen this project, ideally a developer friend.
You already know where the breaks are, so your own time and score would flatter the diff.
If nobody else is available, do it yourself and say so plainly on the slide ("the author, who
knew the answers, still needed N minutes"), or drop the comparison and show only Rowgate's
measured numbers.

## How

1. Open the pull request diff (`main...feature/fast-checkout`) on GitHub, **Files changed** tab.
2. Start a timer.
3. Review it the way a normal reviewer would: read the diff; open the workbook only if the diff
   makes you want to. Stop when you would approve or request changes.
4. Stop the timer. Write down every problem you flagged, **before** looking at the answers below.

## Record

| | Your result |
| --- | --- |
| Minutes spent | |
| Breaks you flagged (of 3) | |
| Did you flag the `request_id` → `req_id` rename as a break? (yes/no) | |
| Would you have approved the PR? (yes/no) | |

Put these numbers into the slides (**[B]**) and the video's numbers card.

---

*Answers (don't read until you've filled in the table): the three breaks are `Orders!C14`
(create returns 202 instead of 201), `Billing!E9` (`currency` dropped from the invoice) and
`Auth!E5` (wrong secret returns 400 `{"detail": ...}` instead of 401 `invalid_grant`). The
rename is harmless because `serialization_alias="request_id"` keeps the wire name.*
