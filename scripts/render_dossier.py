"""Deterministic step: render out/dossier.html from Bob's findings. No model involved.

Inputs
  out/findings.json                 written by Bob (schema: rowgate/findings.schema.json)
  out/diff.patch                    from scripts/collect_diff.sh; hunks are cut from here by file + line
  out/test_results.before.json      pytest JSON report on the untouched branch (optional)
  out/test_results.after.json       pytest JSON report after the approved changes (optional)
  contract/api-contract.xlsx        cited rows are read from the workbook, and every cell that
                                    differs from the base branch's copy is listed as measured

Nothing in the dossier's evidence is taken on Bob's word: code comes from the diff, test
outcomes from pytest, workbook edits from comparing the file with git.

Usage: python scripts/render_dossier.py [--findings out/findings.json] [--out out/dossier.html]
"""

import argparse
import io
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape
from openpyxl import load_workbook
from openpyxl.utils.cell import coordinate_from_string, column_index_from_string, get_column_letter

ROOT = Path(__file__).resolve().parent.parent
CELL = re.compile(r"^([A-Za-z]+)!([A-Z]+[0-9]+)$")
TEST = re.compile(r"^tests/contract/test_[a-z]+_([A-Z]+[0-9]+)_[a-z0-9_]+\.py$")
HUNK_HEAD = re.compile(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@")
HEADER_KEYS = {"Rule", "Code", "Date", "Party"}
EXCERPT = 6  # lines of context either side of the cited line


# --- diff -------------------------------------------------------------------------------

def parse_patch(text: str) -> dict[str, list[list[str]]]:
    """file → list of hunks (each a list of lines, starting with the @@ header)."""
    files: dict[str, list[list[str]]] = {}
    current = None
    for line in text.splitlines():
        if line.startswith("diff --git"):
            current = None  # file headers ("--- a/...") until the next "+++" are not hunk lines
        elif line.startswith("+++ "):
            path = line[4:].strip()
            current = files.setdefault(path[2:] if path.startswith("b/") else path, [])
        elif line.startswith("@@") and current is not None:
            current.append([line])
        elif current and line[:1] in (" ", "+", "-", "\\"):
            current[-1].append(line)
    return files


def excerpt(patch: dict, file: str, line: int | None) -> tuple[list[tuple[str, str]], str | None]:
    """Cut the hunk that covers `line` (new-file numbering) down to a few lines around it."""
    hunks = patch.get(file)
    if not hunks:
        return [], f"{file} is not in out/diff.patch"
    for hunk in hunks:
        m = HUNK_HEAD.match(hunk[0])
        new_start, new_len = int(m.group(3)), int(m.group(4) or 1)
        if line is not None and not (new_start <= line < new_start + max(new_len, 1)):
            continue
        rows, new_no = [], new_start
        for text in hunk[1:]:
            kind = {"+": "add", "-": "del"}.get(text[:1], "ctx")
            at = new_no
            if kind != "del":
                new_no += 1
            if line is None or abs(at - line) <= EXCERPT:
                rows.append(("hit " + kind if kind != "del" and at == line else kind, text))
        head = f"@@ {file} around line {line} @@" if line else hunk[0]
        return [("at", head)] + rows, None
    return [], f"no hunk in out/diff.patch covers {file}:{line}"


# --- workbook ---------------------------------------------------------------------------

def git(*args: str, binary: bool = False):
    try:
        out = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, check=True).stdout
        return out if binary else out.decode().strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def cited_row(wb, ref: str) -> dict | None:
    """The header row and the cited row, so the dossier shows the cell in context."""
    m = CELL.match(ref)
    if not m or m.group(1) not in wb.sheetnames:
        return None
    ws = wb[m.group(1)]
    col_letter, row = coordinate_from_string(m.group(2))
    col = column_index_from_string(col_letter)
    header_row = next(
        (r for r in range(1, min(row, 10)) if ws.cell(row=r, column=1).value in HEADER_KEYS), None
    )
    width = ws.max_column

    def value(r, c):
        v = ws.cell(row=r, column=c).value
        if v is None:  # merged block: show the value from the top-left cell
            for rng in ws.merged_cells.ranges:
                if rng.min_row <= r <= rng.max_row and rng.min_col <= c <= rng.max_col:
                    v = ws.cell(row=rng.min_row, column=rng.min_col).value
                    break
        return "" if v is None else str(v)

    return {
        "sheet": m.group(1),
        "letters": [get_column_letter(c) for c in range(1, width + 1)],
        "headers": [value(header_row, c) for c in range(1, width + 1)] if header_row else [],
        "cells": [value(row, c) for c in range(1, width + 1)],
        "row": row,
        "hit": col - 1,
    }


def workbook_changes(wb, base: str, path: str) -> list[dict] | None:
    """Every cell whose value differs from the base branch's copy of the workbook."""
    blob = git("show", f"{base}:{path}", binary=True)
    if blob is None:
        return None
    old = load_workbook(io.BytesIO(blob))
    changes = []
    for name in wb.sheetnames:
        new_ws = wb[name]
        old_ws = old[name] if name in old.sheetnames else None
        rows = max(new_ws.max_row, old_ws.max_row if old_ws else 0)
        cols = max(new_ws.max_column, old_ws.max_column if old_ws else 0)
        for r in range(1, rows + 1):
            for c in range(1, cols + 1):
                a = old_ws.cell(row=r, column=c).value if old_ws else None
                b = new_ws.cell(row=r, column=c).value
                if a != b:
                    changes.append({"cell": f"{name}!{get_column_letter(c)}{r}",
                                    "old": "" if a is None else str(a), "new": "" if b is None else str(b)})
    return changes


# --- tests ------------------------------------------------------------------------------

def outcomes(path: Path) -> dict[str, str]:
    """Map test file → worst outcome in a pytest-json-report file."""
    if not path.exists():
        return {}
    report = json.loads(path.read_text())
    result: dict[str, str] = {}
    rank = {"passed": 0, "skipped": 1, "failed": 2, "error": 3}
    for t in report.get("tests", []):
        file = t["nodeid"].split("::")[0]
        outcome = t.get("outcome", "error")
        if rank.get(outcome, 3) >= rank.get(result.get(file, "passed"), 0):
            result[file] = outcome
    return result


# --- checks -----------------------------------------------------------------------------

def validate(doc: dict) -> list[str]:
    """The checks that matter for the demo. Problems are shown in the dossier, not hidden."""
    problems = []
    for key in ("branch", "base", "workbook", "findings", "skipped"):
        if key not in doc:
            problems.append(f"findings.json is missing '{key}'")
    for f in doc.get("findings", []):
        fid = f.get("id", "?")
        cell = CELL.match(f.get("cell", ""))
        if not cell:
            problems.append(f"{fid}: cell '{f.get('cell')}' is not Sheet!A1 form")
        m = TEST.match(f.get("test", ""))
        if not m:
            problems.append(f"{fid}: BREAK without a correctly named test (tests/contract/test_<sheet>_<cell>_<what>.py)")
        elif cell and m.group(1) != cell.group(2):
            problems.append(f"{fid}: test name cites {m.group(1)} but finding cites {f['cell']}")
        elif not (ROOT / f["test"]).exists():
            problems.append(f"{fid}: {f['test']} does not exist")
    return problems


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--findings", default="out/findings.json")
    ap.add_argument("--out", default="out/dossier.html")
    ap.add_argument("--patch", default="out/diff.patch")
    args = ap.parse_args()

    doc = json.loads((ROOT / args.findings).read_text())
    problems = validate(doc)
    workbook_path = doc.get("workbook", "contract/api-contract.xlsx")
    wb = load_workbook(ROOT / workbook_path)
    patch_file = ROOT / args.patch
    patch = parse_patch(patch_file.read_text()) if patch_file.exists() else {}
    if not patch_file.exists():
        problems.append(f"{args.patch} not found: run scripts/collect_diff.sh first")
    before = outcomes(ROOT / "out/test_results.before.json")
    after = outcomes(ROOT / "out/test_results.after.json")
    changes = workbook_changes(wb, doc.get("base", "main"), workbook_path)
    changed_cells = {c["cell"]: c["new"] for c in changes or []}

    def evidence_rows(owner: str, ev) -> list:
        if not isinstance(ev, dict) or "file" not in ev:
            return []
        if ev.get("hunk"):  # explicit hunk from Bob: shown, but only if it really is in the diff
            body = [l for l in ev["hunk"].splitlines() if l[:1] in "+-"]
            text = "\n".join(l for h in patch.get(ev["file"], []) for l in h)
            if any(l not in text for l in body):
                problems.append(f"{owner}: quoted hunk does not match out/diff.patch for {ev['file']}")
            return [("at" if l.startswith("@@") else {"+": "add", "-": "del"}.get(l[:1], "ctx"), l)
                    for l in ev["hunk"].splitlines()]
        rows, err = excerpt(patch, ev["file"], ev.get("line"))
        if err and patch:
            problems.append(f"{owner}: {err}")
        return rows

    findings = []
    for f in doc.get("findings", []):
        fid = f.get("id", "?")
        for cell, value in ((f.get("workbook_edit") or {}).get("cells") or {}).items():
            if changes is not None and changed_cells.get(cell) != value:
                problems.append(f"{fid}: claims {cell} = {value}, but the workbook has "
                                f"{changed_cells.get(cell, 'no change there')!r}")
        findings.append({
            **f,
            "row": cited_row(wb, f.get("cell", "")),
            "related": [cited_row(wb, c) for c in f.get("related_cells", [])],
            "diff": evidence_rows(fid, f.get("evidence")),
            "before": before.get(f.get("test", "")),
            "after": after.get(f.get("test", "")),
        })
    skipped = [{**s, "row": cited_row(wb, s.get("cell", "")),
                "diff": evidence_rows(s.get("cell", "skipped"), s.get("evidence"))}
               for s in doc.get("skipped", [])]

    counts = {
        "breaks": len(findings),
        "skipped": len(skipped),
        "red_before": sum(1 for f in findings if f["before"] == "failed"),
        "green_after": sum(1 for f in findings if f["after"] == "passed"),
        "recorded": sum(1 for f in findings if f.get("decision") == "record_breaking"),
        "cells_changed": len(changes or []),
    }

    env = Environment(loader=FileSystemLoader(ROOT / "rowgate"), autoescape=select_autoescape(["html", "j2"]))
    html = env.get_template("dossier.html.j2").render(
        doc=doc, findings=findings, skipped=skipped, counts=counts, problems=problems,
        changes=changes, head=git("rev-parse", "--short", "HEAD"),
        generated=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
    )
    out = ROOT / args.out
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html)
    print(f"wrote {args.out}: {counts['breaks']} breaks, {counts['skipped']} skipped, "
          f"{counts['cells_changed']} workbook cells changed, {len(problems)} problems")
    for p in problems:
        print(f"  ! {p}", file=sys.stderr)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
