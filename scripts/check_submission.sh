#!/usr/bin/env bash
# Pre-submission check. Run on main after scripts/publish_run.sh. No model involved.
# Usage: scripts/check_submission.sh
set -uo pipefail
cd "$(git rev-parse --show-toplevel)"
# Prefer the repo venv, so the scripts work in a terminal where it was not activated.
if [[ -n "${PYTHON:-}" ]]; then PY="$PYTHON"
elif [[ -x .venv/Scripts/python.exe ]]; then PY=.venv/Scripts/python.exe
elif [[ -x .venv/bin/python ]]; then PY=.venv/bin/python
else PY=python; fi
fail=0; warn=0
ok()   { echo "  ✓ $1"; }
bad()  { echo "  ✗ $1"; fail=1; }
note() { echo "  ! $1"; warn=1; }

echo "Required"
grep -q "MIT License" LICENSE 2>/dev/null && ok "MIT LICENSE" || bad "LICENSE missing or not MIT"
png=$(find bob_sessions -type f \( -iname '*.png' -o -iname '*.jpg' \) | wc -l)
md=$(find bob_sessions -type f -iname '*.md' | wc -l)
[[ $png -gt 0 ]] && ok "bob_sessions: $png screenshot(s)" || bad "bob_sessions: no consumption-summary screenshots"
[[ $md -gt 0 ]] && ok "bob_sessions: $md exported task history file(s)" || bad "bob_sessions: no exported task history (.md) files"
[[ $md -ge $png || $png -eq 0 ]] || note "fewer exported .md files ($md) than screenshots ($png): export every task"

if [[ -f web/public/data/run.json ]]; then
  n=$("$PY" -c "import json;print(len(json.load(open('web/public/data/run.json'))['problems']))")
  [[ $n == 0 ]] && ok "published run has 0 problems" || bad "published run has $n problem(s): see the Run page"
else
  bad "no published run (web/public/data/run.json): run scripts/publish_run.sh"
fi
[[ -f web/public/dossier.html ]] && ok "single-file dossier published" || bad "web/public/dossier.html missing"

echo "Safety"
# IBM Cloud API keys are 44 chars of [A-Za-z0-9_-]; also catch obvious key names and private keys.
secrets=$( { git ls-files; find bob_sessions -type f; } | sort -u | grep -v -E '\.(png|jpg|xlsx)$|package-lock\.json' \
  | xargs -r grep -n -I -E '(api[_-]?key|apikey|IBM_CLOUD|BOB_API|secret_key|access_token)["'"'"' ]*[:=]["'"'"' ]*[A-Za-z0-9_\-]{20,}|-----BEGIN [A-Z ]*PRIVATE KEY|\b[A-Za-z0-9_-]{44}\b' 2>/dev/null \
  | grep -v -E 'demo-secret-kora-pos|sha512-|integrity' | head -5)
[[ -z "$secrets" ]] && ok "no credential-like strings found" || { bad "possible credentials, remove before submitting:"; echo "$secrets" | sed 's/^/      /'; }

echo "Wording"
wf=$(grep -rn -i "workflow" README.md submission web/src .bob rowgate/bob 2>/dev/null | grep -v -i -E "don't call|no use of the word" | head -3)
[[ -z "$wf" ]] && ok "no 'workflow' wording in public-facing files" || { note "'workflow' appears (Rowgate is a custom mode + Skill):"; echo "$wf" | sed 's/^/      /'; }
ph=$(grep -n -E '\[(N|B|C)\]' submission/*.md 2>/dev/null | grep -v -E 'Numbers marked|Fill \*\*|come from|Put these numbers|Every \*\*\[N\]' | head -3)
[[ -z "$ph" ]] && ok "no [N]/[B]/[C] placeholders left in submission/" || { note "placeholders still in submission/ (fill them in your copy of the slides/form):"; echo "$ph" | sed 's/^/      /'; }

echo "Tests"
"$PY" -m pytest -q -p no:cacheprovider tests --ignore=tests/contract >/dev/null 2>&1 && ok "test suite green on $(git rev-parse --abbrev-ref HEAD)" || bad "test suite failing"

echo
if [[ $fail -eq 0 ]]; then echo "Ready to submit.$([[ $warn -eq 1 ]] && echo ' (check the ! notes)')"; else echo "Not ready: fix the ✗ items."; fi
exit $fail
