#!/usr/bin/env bash
# Deterministic step: capture what the branch changed. No model involved.
# Usage: scripts/collect_diff.sh [branch=HEAD] [base=main]
set -euo pipefail
BRANCH="${1:-HEAD}"
BASE="${2:-main}"
cd "$(git rev-parse --show-toplevel)"
mkdir -p out
git diff --unified=5 "$BASE...$BRANCH" -- . ':!out' ':!bob_sessions' > out/diff.patch
git diff --name-only "$BASE...$BRANCH" -- . ':!out' ':!bob_sessions' > out/changed_files.txt
echo "base=$BASE branch=$BRANCH"
echo "changed files: $(wc -l < out/changed_files.txt)"
sed 's/^/  /' out/changed_files.txt
echo "diff: out/diff.patch ($(wc -l < out/diff.patch) lines)"
