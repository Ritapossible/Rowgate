#!/usr/bin/env bash
# Deterministic step: run the contract tests and save machine-readable results.
# Usage: scripts/run_contract_tests.sh [label]   label = before | after (default: latest)
# Writes out/test_results.<label>.json. Exit code is pytest's (non-zero = a contract row is broken).
set -uo pipefail
cd "$(git rev-parse --show-toplevel)"
mkdir -p out
LABEL="${1:-latest}"
# Prefer the repo venv, so the scripts work in a terminal where it was not activated.
if [[ -n "${PYTHON:-}" ]]; then PY="$PYTHON"
elif [[ -x .venv/Scripts/python.exe ]]; then PY=.venv/Scripts/python.exe
elif [[ -x .venv/bin/python ]]; then PY=.venv/bin/python
else PY=python; fi
REPORT="out/test_results.$LABEL.json"
if ! ls tests/contract/test_*.py >/dev/null 2>&1; then
  echo "no contract tests yet in tests/contract/"
  exit 0
fi
"$PY" -m pytest tests/contract -q -p no:cacheprovider \
  --json-report --json-report-file="$REPORT" --json-report-omit=keywords,streams
status=$?
echo "results: $REPORT (pytest exit $status)"
exit $status
