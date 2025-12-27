#!/usr/bin/env bash

set -euo pipefail

declare -ar DIRS=("str8ts_solver/" "tests/" "examples/")

uv run bandit -c bandit.yml -r "${DIRS[@]}"
uv run black --check "${DIRS[@]}"
uv run ruff check "${DIRS[@]}"
uv run mypy "${DIRS[@]}"
uv run pyright --warnings "${DIRS[@]}"
uv run isort --profile black --check "${DIRS[@]}"
uv run pylint "${DIRS[@]}"
uv run flake8 --count --max-line-length=88 --show-source --ignore=E203,W503 "${DIRS[@]}"
uv run xenon --max-absolute B --max-modules A --max-average A "${DIRS[@]}"
