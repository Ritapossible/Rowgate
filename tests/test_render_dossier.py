"""The dossier renderer is deterministic code; test it on synthetic findings."""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def render(tmp_path, doc):
    findings = tmp_path / "findings.json"
    findings.write_text(json.dumps(doc))
    out = tmp_path / "dossier.html"
    proc = subprocess.run(
        [sys.executable, "scripts/render_dossier.py", "--findings", str(findings), "--out", str(out)],
        cwd=ROOT, capture_output=True, text=True,
    )
    return proc, out.read_text() if out.exists() else ""


def synthetic(test_path):
    return {
        "branch": "demo/synthetic", "base": "main", "workbook": "contract/api-contract.xlsx",
        "findings": [{
            "id": "F1", "cell": "Cover!B5", "contract_says": "version v3.2", "code_does": "reports v9",
            "evidence": {"file": "app/main.py", "hunk": "@@ -1 +1 @@\n-v3.2\n+v9"},
            "verdict": "BREAK", "reasoning": "synthetic", "test": test_path, "decision": "pending",
        }],
        "skipped": [{"cell": "Cover!B6", "why": "synthetic skip"}],
    }


def test_renders_cited_row_from_workbook(tmp_path):
    proc, html = render(tmp_path, synthetic("tests/test_smoke.py"))
    assert "Cover!B5" in html
    assert "v3.2" in html          # value read from the workbook row
    assert 'class="hit"' in html   # the cited cell is highlighted
    assert "synthetic skip" in html


def test_flags_break_without_cell_named_test(tmp_path):
    proc, html = render(tmp_path, synthetic("tests/contract/test_cover_B9_version.py"))
    assert proc.returncode == 1
    assert "test name cites B9 but finding cites Cover!B5" in html


sys.path.insert(0, str(ROOT / "scripts"))
import render_dossier as rd  # noqa: E402

PATCH = """diff --git a/app/x.py b/app/x.py
--- a/app/x.py
+++ b/app/x.py
@@ -10,5 +10,5 @@ def f():
 a = 1
 b = 2
-c = 3
+c = 4
 d = 5
 e = 6
"""


def test_excerpt_cuts_hunk_and_marks_cited_line():
    rows, err = rd.excerpt(rd.parse_patch(PATCH), "app/x.py", 12)
    assert err is None
    assert ("hit add", "+c = 4") in rows
    assert ("del", "-c = 3") in rows


def test_excerpt_reports_uncovered_line():
    rows, err = rd.excerpt(rd.parse_patch(PATCH), "app/x.py", 99)
    assert rows == [] and "no hunk" in err


def test_workbook_changes_are_measured_against_git():
    import io
    from openpyxl import load_workbook
    # Start from the committed copy, so a demo run that edits the file doesn't break this test.
    wb = load_workbook(io.BytesIO(rd.git("show", "HEAD:contract/api-contract.xlsx", binary=True)))
    wb["Billing"]["H9"] = "BREAKING"
    changes = rd.workbook_changes(wb, "HEAD", "contract/api-contract.xlsx")
    assert changes == [{"cell": "Billing!H9", "old": "ACTIVE", "new": "BREAKING"}]
