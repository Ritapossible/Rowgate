#!/usr/bin/env bash
# Deterministic step: capture what the branch changed. No model involved.
# Usage: scripts/collect_diff.sh [branch=HEAD] [base=main]
set -euo pipefail
BRANCH="${1:-HEAD}"
BASE="${2:-main}"
cd "$(git rev-parse --show-toplevel)"
mkdir -p out
# --output writes the file directly, so a shell that adds a BOM on redirection cannot corrupt it
git diff --unified=5 --output=out/diff.patch "$BASE...$BRANCH" -- . ':!out' ':!bob_sessions'
git diff --name-only --output=out/changed_files.txt "$BASE...$BRANCH" -- . ':!out' ':!bob_sessions'
echo "base=$BASE branch=$BRANCH"
echo "changed files: $(wc -l < out/changed_files.txt)"
sed 's/^/  /' out/changed_files.txt
echo "diff: out/diff.patch ($(wc -l < out/diff.patch) lines)"
