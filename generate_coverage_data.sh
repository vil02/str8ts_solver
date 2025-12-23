#!/usr/bin/env bash

set -euo pipefail

omitted_paths="tests/*"
readonly omitted_paths

uv run coverage run --branch -m pytest "$@"
uv run coverage xml --omit="${omitted_paths}"
uv run coverage html --omit="${omitted_paths}"
uv run coverage report --omit="${omitted_paths}"
