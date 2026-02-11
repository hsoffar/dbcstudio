#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Let callers override interpreter explicitly.
if [[ -n "${DBCSTUDIO_PYTHON:-}" ]]; then
  PYTHON_BIN="$DBCSTUDIO_PYTHON"
else
  # Candidate interpreters in priority order.
  CANDIDATES=()
  if [[ -n "${VIRTUAL_ENV:-}" && -x "${VIRTUAL_ENV}/bin/python" ]]; then
    CANDIDATES+=("${VIRTUAL_ENV}/bin/python")
  fi
  if [[ -x "$ROOT_DIR/.venv/bin/python" ]]; then
    CANDIDATES+=("$ROOT_DIR/.venv/bin/python")
  fi
  CANDIDATES+=("python3.8" "python3" "python")

  PYTHON_BIN=""
  for candidate in "${CANDIDATES[@]}"; do
    if ! command -v "$candidate" >/dev/null 2>&1; then
      continue
    fi
    if "$candidate" -c "import importlib.util,sys;sys.exit(0 if (importlib.util.find_spec('PySide6') and importlib.util.find_spec('cantools')) else 1)" >/dev/null 2>&1; then
      PYTHON_BIN="$candidate"
      break
    fi
  done

  if [[ -z "$PYTHON_BIN" ]]; then
    echo "No Python interpreter with both PySide6 and cantools was found." >&2
    echo "Set DBCSTUDIO_PYTHON=/path/to/python or install deps in your venv." >&2
    exit 1
  fi
fi

# Run directly from source tree (no pip install required).
export PYTHONPATH="$ROOT_DIR/src${PYTHONPATH:+:$PYTHONPATH}"

exec "$PYTHON_BIN" -m dbcstudio "$@"
