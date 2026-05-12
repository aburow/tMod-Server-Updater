#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
if [ -d "$ROOT_DIR/tests" ]; then
  exec "$ROOT_DIR/scripts/run_uv_tool.sh" pytest tests/ -q --tb=short
fi

echo "No tests/ directory found; skipping pytest hook."
