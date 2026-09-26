#!/usr/bin/env bash
# Deterministic step: publish the current Rowgate run to the website.
# Run it on the branch Bob reviewed, after render_dossier.py reports 0 problems.
# It exports the site data, copies it and the bob_sessions/ screenshots onto main,
# commits there, pushes main, and returns to the branch you started on.
#
# Usage: scripts/publish_run.sh [--no-push]
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
# Prefer the repo venv, so the scripts work in a terminal where it was not activated.
if [[ -n "${PYTHON:-}" ]]; then PY="$PYTHON"
elif [[ -x .venv/Scripts/python.exe ]]; then PY=.venv/Scripts/python.exe
elif [[ -x .venv/bin/python ]]; then PY=.venv/bin/python
else PY=python; fi
BRANCH=$(git rev-parse --abbrev-ref HEAD)
[[ "$BRANCH" != "main" ]] || { echo "Run this on the reviewed branch, not main."; exit 1; }
[[ -f out/findings.json ]] || { echo "No out/findings.json: finish the run first."; exit 1; }

"$PY" scripts/render_dossier.py
"$PY" scripts/export_site.py --branch "$BRANCH" --base main

STAGE=$(mktemp -d)
cp -r web/public/data "$STAGE/data"
cp web/public/dossier.html "$STAGE/dossier.html"
# Copy only the top-level files: "cp -r dir/." nested bob_sessions inside itself, and each
# publish then added another level.
mkdir -p "$STAGE/bob_sessions"
find bob_sessions -maxdepth 1 -type f -exec cp {} "$STAGE/bob_sessions/" \; 2>/dev/null || true
git checkout -q -- web/public/data 2>/dev/null || true
rm -f web/public/dossier.html web/public/data/run.json

git stash push -q --include-untracked -m "rowgate-publish" || true
git checkout -q main
cp "$STAGE"/data/*.json web/public/data/
cp "$STAGE/dossier.html" web/public/dossier.html
find "$STAGE/bob_sessions" -maxdepth 1 -type f -exec cp {} bob_sessions/ \;
git add web/public/data web/public/dossier.html bob_sessions
git commit -q -m "Publish Rowgate run on $BRANCH" && echo "committed on main"
if [[ "${1:-}" != "--no-push" ]]; then git push -q origin main && echo "pushed main"; fi
git checkout -q "$BRANCH"
git stash pop -q 2>/dev/null || true
rm -rf "$STAGE"
echo "Published. The Run page updates after Vercel deploys main."
