#!/usr/bin/env bash
# Put the repo back in the demo's starting state and check it: the untouched PR branch,
# the signed workbook unedited, no contract tests yet, empty out/.
# Run before every dry run and before the recording.
#
# Usage: scripts/reset_demo.sh           check only; refuses if there are uncommitted changes
#        scripts/reset_demo.sh --force   discard run leftovers and move the branch back to demo/start
#
# demo/start is a branch that marks the untouched PR. Never commit to it.
set -uo pipefail
cd "$(git rev-parse --show-toplevel)"
BRANCH=feature/fast-checkout
START=$(git rev-parse --verify -q refs/heads/demo/start || git rev-parse --verify -q refs/remotes/origin/demo/start)
[[ -n "$START" ]] || { echo "No demo/start branch (git fetch origin demo/start)"; exit 1; }
# Prefer the repo venv, so the scripts work in a terminal where it was not activated.
if [[ -n "${PYTHON:-}" ]]; then PY="$PYTHON"
elif [[ -x .venv/Scripts/python.exe ]]; then PY=.venv/Scripts/python.exe
elif [[ -x .venv/bin/python ]]; then PY=.venv/bin/python
else PY=python; fi
FORCE=0; [[ "${1:-}" == "--force" ]] && FORCE=1

dirty=$(git status --porcelain -- . ':!out' ':!bob_sessions')
if [[ -n "$dirty" ]]; then
  if [[ $FORCE -eq 0 ]]; then
    echo "Uncommitted changes (bob_sessions/ and out/ are ignored here):"
    echo "$dirty"
    echo "Re-run with --force to discard them."
    exit 1
  fi
  git checkout -q -- .
  git clean -fdq -- tests/contract app contract
fi
if [[ $FORCE -eq 1 ]]; then
  git checkout -q -B "$BRANCH" "$START"
else
  git checkout -q "$BRANCH"
fi
find out -mindepth 1 ! -name .gitkeep -delete 2>/dev/null

fail=0
check() { if eval "$2" >/dev/null 2>&1; then echo "  ✓ $1"; else echo "  ✗ $1"; fail=1; fi; }
echo "Demo state:"
check "on $BRANCH at demo/start" "[[ \$(git rev-parse HEAD) == \$(git rev-parse $START) ]]"
check "tooling identical to main" "git diff --quiet main HEAD -- scripts rowgate .bob contract tests/conftest.py tests/test_smoke.py pytest.ini requirements.txt"
check "PR changes only app/ (5 files)" "[[ \$(git diff --name-only main...HEAD | grep -cv '^app/') == 0 && \$(git diff --name-only main...HEAD | wc -l) == 5 ]]"
check "no contract tests yet" "! ls tests/contract/test_*.py"
check "workbook identical to main" "git diff --quiet main -- contract/api-contract.xlsx"
check "out/ empty" "[[ -z \$(find out -mindepth 1 ! -name .gitkeep) ]]"
check "existing tests green (the PR looks mergeable)" "$PY -m pytest -q -p no:cacheprovider tests --ignore=tests/contract"
if [[ $fail -eq 0 ]]; then echo "Ready."; else echo "Not ready. Fix the ✗ items (scripts/reset_demo.sh --force resets to demo/start)."; fi
exit $fail
