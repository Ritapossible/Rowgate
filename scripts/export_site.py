"""Deterministic step: export what the web app shows as static JSON. No model involved.

Writes web/public/data/
  contract.json   every sheet of the workbook: cells, merged ranges, row status, notes
  pr.json         the pull request under review: commits and diff (base...branch)
  run.json        the latest Rowgate run, measured like the dossier (only if out/findings.json exists)
and copies out/dossier.html to web/public/dossier.html when it exists.

Commit these files; Vercel then serves the site without Python or a server.

Usage: python scripts/export_site.py [--branch feature/fast-checkout] [--base main]
"""

import argparse
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

from openpyxl import load_workbook
from openpyxl.utils.cell import get_column_letter

sys.path.insert(0, str(Path(__file__).resolve().parent))
import render_dossier as rd  # noqa: E402

ROOT = rd.ROOT
OUT = ROOT / "web" / "public" / "data"
WORKBOOK = "contract/api-contract.xlsx"
STATUSES = {"ACTIVE", "PLANNED", "DEPRECATED", "BREAKING"}


def export_contract() -> dict:
    wb = load_workbook(ROOT / WORKBOOK)
    sheets, totals = [], {"rules": 0, "ACTIVE": 0, "PLANNED": 0, "DEPRECATED": 0, "BREAKING": 0}
    for ws in wb.worksheets:
        cells = [["" if (v := ws.cell(row=r, column=c).value) is None else str(v)
                  for c in range(1, ws.max_column + 1)] for r in range(1, ws.max_row + 1)]
        header_row = next((r for r in range(1, min(ws.max_row, 10) + 1)
                           if ws.cell(row=r, column=1).value in rd.HEADER_KEYS), None)
        status_col = None
        if header_row:
            status_col = next((c for c in range(1, ws.max_column + 1)
                               if ws.cell(row=header_row, column=c).value == "Contract status"), None)
        row_status = {}
        for r in range(1, ws.max_row + 1):
            rule = ws.cell(row=r, column=1).value
            if isinstance(rule, str) and rule[:4] in ("ORD-", "BIL-", "AUT-", "ERR-"):
                totals["rules"] += 1
                status = ws.cell(row=r, column=status_col).value if status_col else None
                if status is None:  # Errors sheet keeps PLANNED in its Notes column
                    status = "PLANNED" if "PLANNED" in [str(v) for v in cells[r - 1]] else "ACTIVE"
                if status in STATUSES:
                    row_status[r] = status
                    if ws.title != "Errors":
                        totals[status] += 1
        sheets.append({
            "name": ws.title,
            "maxRow": ws.max_row,
            "maxCol": ws.max_column,
            "letters": [get_column_letter(c) for c in range(1, ws.max_column + 1)],
            "headerRow": header_row,
            "statusCol": status_col,
            "cells": cells,
            "merges": [{"r1": m.min_row, "c1": m.min_col, "r2": m.max_row, "c2": m.max_col}
                       for m in ws.merged_cells.ranges],
            "rowStatus": row_status,
            "notes": {c.coordinate: c.comment.text for row in ws.iter_rows() for c in row if c.comment},
        })
    cover = wb["Cover"]
    return {
        "workbook": WORKBOOK,
        "title": cover["A1"].value,
        "partner": cover["B3"].value,
        "version": cover["B5"].value,
        "signed": cover["B6"].value,
        "totals": totals,
        "sheets": sheets,
    }


def export_pr(branch: str, base: str) -> dict:
    patch_text = rd.git("diff", "--unified=5", f"{base}...{branch}", "--", "app") or ""
    files = []
    for path, hunks in rd.parse_patch(patch_text).items():
        out = []
        for hunk in hunks:
            m = rd.HUNK_HEAD.match(hunk[0])
            old_no, new_no = int(m.group(1)), int(m.group(3))
            lines = []
            for text in hunk[1:]:
                kind = {"+": "add", "-": "del", "\\": "meta"}.get(text[:1], "ctx")
                lines.append({"kind": kind, "text": text[1:],
                              "old": old_no if kind in ("ctx", "del") else None,
                              "new": new_no if kind in ("ctx", "add") else None})
                if kind in ("ctx", "del"):
                    old_no += 1
                if kind in ("ctx", "add"):
                    new_no += 1
            out.append({"header": hunk[0], "lines": lines})
        added = sum(1 for h in out for l in h["lines"] if l["kind"] == "add")
        removed = sum(1 for h in out for l in h["lines"] if l["kind"] == "del")
        files.append({"path": path, "added": added, "removed": removed, "hunks": out})
    log = rd.git("log", "--format=%h%x09%s", f"{base}..{branch}") or ""
    commits = [dict(zip(("sha", "subject"), line.split("\t", 1))) for line in log.splitlines()][::-1]
    return {"branch": branch, "base": base, "commits": commits, "files": files}


def export_run() -> dict | None:
    findings = ROOT / "out" / "findings.json"
    if not findings.exists():
        return None
    ctx = rd.build_context(findings, ROOT / "out" / "diff.patch")
    for item in ctx["findings"] + ctx["skipped"]:
        item["diff"] = [{"kind": k, "text": t} for k, t in item["diff"]]
    return ctx


def write(name: str, data) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / name).write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n")
    print(f"wrote web/public/data/{name}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--branch", default="feature/fast-checkout")
    ap.add_argument("--base", default="main")
    args = ap.parse_args()

    write("contract.json", export_contract())
    write("pr.json", export_pr(args.branch, args.base))
    run = export_run()
    if run is None:
        print("no out/findings.json: run.json left as is (the site shows 'no run published yet' without it)")
    else:
        write("run.json", run)
    dossier = ROOT / "out" / "dossier.html"
    if dossier.exists():
        shutil.copyfile(dossier, ROOT / "web" / "public" / "dossier.html")
        print("copied out/dossier.html to web/public/dossier.html")
    write("site.json", {
        "exportedAt": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "head": rd.git("rev-parse", "--short", "HEAD"),
        "hasRun": (OUT / "run.json").exists(),
        "hasDossier": (ROOT / "web" / "public" / "dossier.html").exists(),
        "repo": "https://github.com/Ritapossible/Rowgate",
    })
    return 0


if __name__ == "__main__":
    sys.exit(main())
