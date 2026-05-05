#!/usr/bin/env bash

set -euo pipefail

omitted_paths="tests/*"
readonly omitted_paths

uv run --frozen --no-build coverage run --branch -m pytest "$@"
uv run --frozen --no-build coverage xml --omit="${omitted_paths}"
uv run --frozen --no-build coverage html --omit="${omitted_paths}"
uv run --frozen --no-build coverage report --omit="${omitted_paths}"
