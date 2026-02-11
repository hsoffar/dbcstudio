# Getting Started

## Prerequisites

- Python 3.8+
- Linux/macOS/Windows
- `pip`

## Run Directly from Source

Use the project launcher:

```bash
./start_dbcstudio.sh
```

It automatically chooses a Python interpreter with required dependencies.

To force a specific interpreter:

```bash
DBCSTUDIO_PYTHON=python3.8 ./start_dbcstudio.sh
```

## Editable Install

```bash
python -m pip install -e .
```

Launch:

```bash
dbc-studio
```

## First Session Checklist

1. Open a DBC file with `Open DBC`.
2. Select a message in the left pane.
3. Toggle Frame ID display (`Decimal` / `Hex`) as needed.
4. Edit signals in table form.
5. Use Endian/Signed dropdowns to avoid invalid text values.
6. Save changes with `Save` or `Save As`.

## Troubleshooting

### `ModuleNotFoundError: PySide6`

The selected Python does not have GUI dependencies installed.

- Use the interpreter where dependencies are installed.
- Or run `python -m pip install -e .` in your active environment.

### Command Not Found (`dbcstudio` / `dbc-studio`)

- Use `./start_dbcstudio.sh`.
- Or reinstall editable package in your current environment.

### Externally Managed Python (PEP 668)

Create a virtual environment and install there:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
```
