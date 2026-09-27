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
   Note whether you'd have called the auth response one problem or two — the answer key explains why it counts as two cells.

## Record

| | Your result |
| --- | --- |
| Minutes spent | |
| Problems you flagged (write each one down) | |
| Did you flag the `request_id` → `req_id` rename as a break? (yes/no) | |
| Would you have approved the PR? (yes/no) | |

Put these numbers into the slides (**[B]**) and the video's numbers card.

---

*Answers (don't read until you've filled in the table). Three edits were planted, and they
break four signed cells:*

| Cell | What broke |
| --- | --- |
| `Orders!C14` | create returns 202 instead of 201 |
| `Billing!E9` | `currency` dropped from the invoice |
| `Auth!E5` | wrong secret returns 400 instead of 401 |
| `Errors!D6` | that response is FastAPI's `{"detail": ...}` instead of the shared error envelope |

*The auth edit breaks two cells, the status and the body shape, which is why the cell count is
four while the edit count is three. Count yourself against whichever you flagged: a reviewer who
says "auth is wrong" has found one problem, not two. The `request_id` → `req_id` rename is
harmless, because `serialization_alias="request_id"` keeps the wire name unchanged — flagging it
is a false positive.*
