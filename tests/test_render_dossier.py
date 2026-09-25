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
