# DBC Studio

DBC Studio is a modern desktop editor and visualizer for CAN DBC files, built in Python with Qt.
It is designed for fast editing workflows with an intuitive UI similar in spirit to professional automotive tools.

## Highlights

- Modern desktop UX with split-pane layout and clean visual styling.
- Open, edit, and save DBC files.
- Message editing: name, frame ID, DLC, sender.
- Frame ID input mode switch: decimal or hex (`0x...`).
- Signal editing table with constrained selections for safer editing:
  - Endian: `Little Endian` / `Big Endian`
  - Signedness: `Unsigned` / `Signed`
- Live signal bit-layout visualization.
- Fast message filtering by name, decimal frame ID, or hex frame ID.

## Why Qt/PySide6

For a Vector-like local desktop tool, `PySide6` is the best fit:

- Native desktop behavior on Linux/Windows/macOS.
- Rich widgets and layout primitives for data-heavy editors.
- Strong custom drawing support for bit-level visualizations.
- Mature ecosystem and long-term maintainability.

DBC parsing/writing uses `cantools` for reliable compatibility with real-world DBC workflows.

## Quick Start

### Option A: Run without install (recommended for active development)

```bash
./start_dbcstudio.sh
```

The launcher:

- Auto-selects a Python interpreter that already has both `PySide6` and `cantools`.
- Checks active virtualenv and project `.venv` first.
- Runs from `src/` directly using `PYTHONPATH`.

Force interpreter explicitly if needed:

```bash
DBCSTUDIO_PYTHON=python3.8 ./start_dbcstudio.sh
```

### Option B: Editable install

```bash
python -m pip install -e .
dbc-studio
```

Also available:

```bash
dbcstudio
```

## Installation Notes

If your OS uses an externally managed Python environment (PEP 668), use a virtualenv:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -e .
```

## Supported Python

- `Python >= 3.8`

## Screens and UX Model

Main layout has 3 panes:

1. Message browser
   - Search/filter messages
   - Select active message
2. Message and signal editor
   - Edit message metadata
   - Add/remove signals
   - Edit signal fields in a table
3. Bit layout visualization
   - Colorized, immediate representation of signal bit allocation

## Current Scope

Implemented in this version:

- Core message/signal editing.
- DBC load and save for essential message/signal structures.
- Modernized visual styling and clearer editing controls.

Planned next:

- Advanced DBC constructs (`BA_`, `CM_`, `VAL_`, multiplexing, signal groups).
- Validation rules (overlap detection, DLC fit checks, duplicate names).
- Undo/redo and change history.
- Better color legend and interactive bit-level editing.
- Import/export diagnostics and schema checks.

## Repository Layout

- `pyproject.toml`: package metadata and dependencies.
- `start_dbcstudio.sh`: no-install launcher.
- `src/dbcstudio/__main__.py`: application entrypoint.
- `src/dbcstudio/main_window.py`: main UI and interaction logic.
- `src/dbcstudio/widgets.py`: custom visualization widgets.
- `src/dbcstudio/dbc_io.py`: DBC load/save conversion.
- `src/dbcstudio/model.py`: document/message/signal models.
- `src/dbcstudio/style.py`: Qt stylesheet theme.
- `tests/test_dbc_io.py`: baseline persistence test.
- `docs/`: deeper documentation.

## Testing

```bash
pytest -q
```

## Documentation Index

- `docs/getting-started.md`
- `docs/user-guide.md`
- `docs/architecture.md`
- `docs/development.md`
- `docs/roadmap.md`

## License

MIT (recommended for broad adoption and low-friction usage).
