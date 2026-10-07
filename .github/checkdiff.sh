#!/bin/sh
set -e

# Regenerated files keep their content but not their mtime.
git update-index -q --refresh || true
if ! git diff-index --quiet HEAD --; then
    echo 'Uncommitted changes detected:'
    git diff-index HEAD --
    return 1
fi
