"""Check that the files the published run cites are really in the repository.

The Run page and the dossier describe tests Bob wrote, commits that carry the
approved fixes, and a workbook Bob edited. A dry run that is published and then
reset leaves those claims pointing at nothing, and the site ends up contradicting
the repository. This is the check that catches it.

Usage: python scripts/check_run_artifacts.py [--run web/public/data/run.json]
Exit code 1 if any cited artefact is missing.
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(subprocess.run(["git", "rev-parse", "--show-toplevel"],
                           capture_output=True, text=True, check=True).stdout.strip())

fail = False


def ok(msg: str) -> None:
    print(f"  ✓ {msg}")


def bad(msg: str) -> None:
    global fail
    fail = True
    print(f"  ✗ {msg}")


def git(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True)


def resolve(branch: str) -> str | None:
    """The run names a branch; it may only exist here as a remote-tracking ref."""
    for ref in (f"origin/{branch}", branch):
        if git("rev-parse", "--verify", "--quiet", f"{ref}^{{commit}}").returncode == 0:
            return ref
    return None


def exists(ref: str, path: str) -> bool:
    return git("cat-file", "-e", f"{ref}:{path}").returncode == 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", default="web/public/data/run.json")
    ap.add_argument("--pr", default="web/public/data/pr.json")
    args = ap.parse_args()

    run_path = ROOT / args.run
    if not run_path.exists():
        print(f"  ! no {args.run}: nothing published yet, skipping")
        return 0
    run = json.loads(run_path.read_text(encoding="utf-8"))

    branch = run["doc"]["branch"]
    base = run["doc"]["base"]
    ref = resolve(branch)
    if ref is None:
        bad(f"branch {branch} not found locally or on origin")
        return 1

    # 1. the contract tests Bob wrote
    tests = [f["test"] for f in run["findings"] if f.get("test")]
    missing = [t for t in tests if not exists(ref, t)]
    if missing:
        bad(f"{len(missing)} of {len(tests)} cited test file(s) are not committed on {ref}:")
        for t in missing:
            print(f"      {t}")
    else:
        ok(f"all {len(tests)} cited test file(s) committed on {ref}")

    # 2. the workbook Bob edited
    changes = run.get("changes") or []
    workbook = run["doc"]["workbook"]
    if changes:
        same = git("diff", "--quiet", base, ref, "--", workbook).returncode == 0
        if same:
            bad(f"run records {len(changes)} workbook cell change(s) but "
                f"{workbook} is identical on {base} and {ref}")
        else:
            ok(f"{workbook} differs from {base}, as the {len(changes)} recorded change(s) require")
    else:
        ok("run records no workbook changes")

    # 3. the commits the site advertises
    pr_path = ROOT / args.pr
    if pr_path.exists():
        pr = json.loads(pr_path.read_text(encoding="utf-8"))
        gone = [c for c in pr["commits"]
                if git("merge-base", "--is-ancestor", c["sha"], ref).returncode != 0]
        if gone:
            bad(f"{len(gone)} commit(s) shown on the Run page are not on {ref}:")
            for c in gone:
                print(f"      {c['sha']}  {c['subject']}")
        else:
            ok(f"all {len(pr['commits'])} commit(s) shown on the Run page are on {ref}")

    return 1 if fail else 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")  # Windows consoles default to cp1252
    sys.exit(main())
