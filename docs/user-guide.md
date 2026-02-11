# User Guide

## Interface Overview

DBC Studio uses a 3-pane workflow:

- Left: message list and filter.
- Center: message metadata + signal table.
- Right: bit layout visualization.

## Working with Messages

### Add Message

Click `Add Message`.

Default behavior:

- Auto-generated unique message name.
- Auto-assigned frame ID.
- Default DLC of 8.

### Remove Message

Select a message and click `Remove Message`.

### Edit Message Fields

- `Name`
- `Frame ID`
- `Length`
- `Sender`

Frame ID can be displayed/edited in:

- Decimal
- Hex (with `0x` prefix)

The underlying value is preserved while the display mode changes.

## Working with Signals

### Add Signal

Click `Add Signal`.

A new signal is created with sane defaults.

### Remove Signal

Select a row and click `Remove Signal`.

### Edit Signal Columns

- `Name`
- `Start`
- `Length`
- `Endian` (dropdown)
- `Signed` (dropdown)
- `Scale`
- `Offset`
- `Unit`

Dropdown-constrained fields reduce input mistakes and make data normalization predictable.

## Bit Layout Visualization

The right pane renders signal occupancy over a fixed 64-bit canvas.

- Colored blocks show bit ranges used by signals.
- The legend text lists each signal and its bit range.
- Updates are immediate when values change.

## Filtering Messages

The search box matches:

- message name
- frame ID in decimal
- frame ID in hex (with or without `0x`)

## Save Behavior

- `Save` writes to current file path.
- `Save As` writes to a new file path.
- If no file is opened yet, `Save` falls back to `Save As`.

## Best Practices

1. Keep frame IDs consistent in one notation during a session.
2. Use dropdown fields instead of free text for constrained attributes.
3. Save frequently before large signal refactors.
4. Validate output with your CAN decoding toolchain after major edits.
