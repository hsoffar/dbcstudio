# Roadmap

## Near Term

- Validation engine
  - bit overlap detection
  - DLC fit checks
  - duplicate signal/message name checks
- Undo/redo command stack
- Better signal editing ergonomics (inline validators, keyboard-heavy flows)

## Mid Term

- Full DBC feature coverage:
  - attributes (`BA_`, `BA_DEF_`, `BA_DEF_DEF_`)
  - comments (`CM_`)
  - value tables (`VAL_`)
  - multiplexing and signal groups
- Interactive bit editor (drag and resize signal ranges)
- Message-level diagnostics sidebar

## Longer Term

- Real-time CAN integration for live decode/encode testing
- Compare/merge mode for two DBC files
- Plugin architecture for project-specific transforms
- Exporters for documentation artifacts (HTML/PDF signal sheets)

## Quality Goals

- Deterministic save output
- Strong backward compatibility with common DBC toolchains
- Clear and actionable error messages
- Fast handling of large DBC files
