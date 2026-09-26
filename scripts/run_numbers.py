"""Print the numbers from the latest published run, for the slides, video and submission text.

Reads web/public/data/run.json (written by export_site.py / publish_run.sh). No model involved.
The human baseline and Bobcoin figures are yours to fill in; see submission/BASELINE.md and
MEMORY.md §6.

Usage: python scripts/run_numbers.py
"""

import json
import sys
from pathlib import Path

# The table below uses an arrow, and on Windows stdout defaults to the cp1252 locale as soon as
# it is piped or redirected, which raises UnicodeEncodeError. Print UTF-8 regardless.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

RUN = Path(__file__).resolve().parent.parent / "web" / "public" / "data" / "run.json"


def main() -> int:
    if not RUN.exists():
        print("No published run yet (web/public/data/run.json). Finish the run and scripts/publish_run.sh first.")
        return 1
    run = json.loads(RUN.read_text(encoding="utf-8"))
    c = run["counts"]
    print("## Rowgate run numbers\n")
    print(f"- Branch: {run['doc']['branch']} vs {run['doc']['base']}, workbook {run['doc'].get('workbook_version') or run['doc']['workbook']}")
    print(f"- Broken contract cells found: **{c['breaks']}**")
    print(f"- Tests red on the branch: **{c['red_before']}/{c['breaks']}**")
    print(f"- Green after approved fixes: **{c['green_after']}/{c['breaks']}**")
    print(f"- Breaking changes recorded in the workbook: **{c['recorded']}** ({c['cells_changed']} cells edited)")
    print(f"- Lookalikes checked and skipped: **{c['skipped']}**")
    print(f"- Dossier problems: **{len(run['problems'])}**" + ("" if not run["problems"] else " (fix before recording!)"))
    print("\n| Finding | Cell | Test | Before → after | Decision |\n| --- | --- | --- | --- | --- |")
    for f in run["findings"]:
        print(f"| {f['id']} | {f['cell']} | `{f['test'].split('/')[-1]}` | {f.get('before') or '-'} → {f.get('after') or '-'} | {f['decision']} |")
    for s in run["skipped"]:
        print(f"| skipped | {s['cell']} | - | - | holds: {s['why']} |")
    print("\nStill to fill in by hand: human baseline (submission/BASELINE.md), Bobcoins used (MEMORY.md §6).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
