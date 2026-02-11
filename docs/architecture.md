# Architecture

## High-Level Design

DBC Studio is organized into clear layers:

1. Data model layer
2. DBC I/O layer
3. UI layer
4. Visualization layer

## Modules

### `src/dbcstudio/model.py`

Defines domain objects:

- `DbcDocument`
- `MessageModel`
- `SignalModel`

This layer is intentionally GUI-agnostic.

### `src/dbcstudio/dbc_io.py`

Responsibilities:

- Read DBC using `cantools`.
- Convert parsed objects into internal models.
- Serialize internal models back to DBC text format.

Design note:

- `cantools` import is lazy in `load_dbc()` so save-only/testing flows can still run in limited environments.

### `src/dbcstudio/main_window.py`

Primary orchestration layer:

- Constructs Qt widgets and layout.
- Handles user events.
- Synchronizes UI state with model state.
- Applies message/signal mutations.
- Triggers visualization updates.

### `src/dbcstudio/widgets.py`

Contains custom widgets for rendering non-trivial visuals:

- `SignalBitLayout` draws bit grid and signal occupancy.

### `src/dbcstudio/style.py`

Defines Qt stylesheet to enforce visual language:

- panel cards
- typography and spacing
- control styling

## Data Flow

1. User opens a DBC file.
2. `load_dbc()` returns `DbcDocument`.
3. UI binds selected `MessageModel` into editable controls.
4. Signal table edits update in-memory `SignalModel` objects.
5. Visualization reads current message and repaints.
6. Save serializes current model back to DBC text.

## Key UX Decisions

- Keep message selection always visible.
- Keep bit map visible while editing signals.
- Use constrained dropdowns for binary/enum-like fields.
- Support both hex and decimal frame-ID mental models.

## Known Constraints

- Current save path focuses on core message/signal content and not all advanced DBC constructs.
- Visualization is view-only in v1 (no drag/drop bit editing yet).

## Extension Points

- Add validation service layer for errors/warnings.
- Add command stack for undo/redo.
- Add plugin hooks for custom exporters/importers.
- Add richer DBC sections parser/serializer coverage.
