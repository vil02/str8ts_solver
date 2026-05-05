#!/usr/bin/env bash

set -euo pipefail

declare -ar DIRS=("str8ts_solver/" "tests/" "examples/")

uv run --frozen --no-build bandit -c bandit.yml -r "${DIRS[@]}"
uv run --frozen --no-build black --check "${DIRS[@]}"
uv run --frozen --no-build ruff check "${DIRS[@]}"
uv run --frozen --no-build mypy "${DIRS[@]}"
uv run --frozen --no-build pyright --warnings "${DIRS[@]}"
uv run --frozen --no-build isort --profile black --check "${DIRS[@]}"
uv run --frozen --no-build pylint "${DIRS[@]}"
uv run --frozen --no-build flake8 --count --max-line-length=88 --show-source --ignore=E203,W503 "${DIRS[@]}"
uv run --frozen --no-build xenon --max-absolute B --max-modules A --max-average A "${DIRS[@]}"
