# Development Guide

## Local Setup

### Preferred: launcher workflow

```bash
./start_dbcstudio.sh
```

### Editable package workflow

```bash
python -m pip install -e .
```

## Run Tests

```bash
pytest -q
```

## Build Confidence Checks

Use both checks before publishing changes:

```bash
python3 -m compileall src tests
pytest -q
```

## Code Organization Rules

- Keep models pure and independent from Qt.
- Keep DBC I/O conversions centralized in `dbc_io.py`.
- Keep UI behavior in `main_window.py`.
- Put reusable custom drawing widgets in `widgets.py`.

## Editing Principles

- Preserve compatibility with Python 3.8+.
- Prefer constrained UI controls for structured values.
- Add tests when changing serialization behavior.
- Keep docs updated with any user-visible behavior changes.

## Packaging Notes

- CLI entrypoints are defined in `pyproject.toml`:
  - `dbc-studio`
  - `dbcstudio`

## Suggested Contribution Process

1. Branch from `main`.
2. Implement focused change.
3. Run tests and compile checks.
4. Update docs.
5. Open PR with screenshots for UI changes.

## Common Pitfalls

- Running with a Python interpreter missing `PySide6`.
- Mixing multiple Python versions with different site-packages.
- Forgetting to refresh editable install when changing package metadata.
