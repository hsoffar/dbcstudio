from __future__ import annotations

from pathlib import Path
from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QFileDialog,
    QFormLayout,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QSplitter,
    QStatusBar,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from .dbc_io import load_dbc, save_dbc
from .model import DbcDocument, MessageModel, SignalModel
from .style import APP_STYLESHEET
from .widgets import SignalBitLayout


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("DBC Studio")
        self.resize(1280, 760)
        self.setStyleSheet(APP_STYLESHEET)

        self.doc = DbcDocument(messages=[])
        self.current_message_index: Optional[int] = None

        self._build_ui()
        self._bind_events()
        self._refresh_message_list()

    def _build_ui(self) -> None:
        central = QWidget()
        root = QVBoxLayout(central)
        root.setContentsMargins(14, 14, 14, 14)
        root.setSpacing(10)

        top_bar = QHBoxLayout()
        self.open_btn = QPushButton("Open DBC")
        self.save_btn = QPushButton("Save")
        self.save_as_btn = QPushButton("Save As")
        self.add_msg_btn = QPushButton("Add Message")
        self.remove_msg_btn = QPushButton("Remove Message")
        top_bar.addWidget(self.open_btn)
        top_bar.addWidget(self.save_btn)
        top_bar.addWidget(self.save_as_btn)
        top_bar.addSpacing(12)
        top_bar.addWidget(self.add_msg_btn)
        top_bar.addWidget(self.remove_msg_btn)
        top_bar.addStretch(1)
        root.addLayout(top_bar)

        splitter = QSplitter(Qt.Horizontal)

        left = self._panel_widget("Messages")
        left_layout = left.layout()
        self.message_search = QLineEdit()
        self.message_search.setPlaceholderText("Filter by name or frame id...")
        self.message_list = QListWidget()
        left_layout.addWidget(self.message_search)
        left_layout.addWidget(self.message_list)

        center = self._panel_widget("Message Editor")
        center_layout = center.layout()

        form = QFormLayout()
        self.msg_name = QLineEdit()
        self.msg_frame_id = QSpinBox()
        self.msg_frame_id.setMaximum(0x1FFFFFFF)
        self.msg_frame_id_mode = QComboBox()
        self.msg_frame_id_mode.addItems(["Decimal", "Hex"])
        frame_id_row = QWidget()
        frame_id_layout = QHBoxLayout(frame_id_row)
        frame_id_layout.setContentsMargins(0, 0, 0, 0)
        frame_id_layout.setSpacing(8)
        frame_id_layout.addWidget(self.msg_frame_id)
        frame_id_layout.addWidget(self.msg_frame_id_mode)
        self.msg_length = QSpinBox()
        self.msg_length.setRange(0, 64)
        self.msg_sender = QLineEdit()
        self.msg_sender.setPlaceholderText("e.g. BodyController")
        form.addRow("Name", self.msg_name)
        form.addRow("Frame ID", frame_id_row)
        form.addRow("Length", self.msg_length)
        form.addRow("Sender", self.msg_sender)
        center_layout.addLayout(form)
        self._set_frame_id_display_mode("Decimal")

        signal_row = QHBoxLayout()
        signal_title = QLabel("Signals")
        signal_title.setObjectName("Title")
        self.add_signal_btn = QPushButton("Add Signal")
        self.remove_signal_btn = QPushButton("Remove Signal")
        signal_row.addWidget(signal_title)
        signal_row.addStretch(1)
        signal_row.addWidget(self.add_signal_btn)
        signal_row.addWidget(self.remove_signal_btn)
        center_layout.addLayout(signal_row)

        self.signal_table = QTableWidget(0, 8)
        self.signal_table.setHorizontalHeaderLabels(
            ["Name", "Start", "Length", "Endian", "Signed", "Scale", "Offset", "Unit"]
        )
        self.signal_table.horizontalHeader().setStretchLastSection(True)
        center_layout.addWidget(self.signal_table)

        right = self._panel_widget("Bit Layout")
        right_layout = right.layout()
        self.bit_layout = SignalBitLayout()
        right_layout.addWidget(self.bit_layout)

        splitter.addWidget(left)
        splitter.addWidget(center)
        splitter.addWidget(right)
        splitter.setSizes([300, 620, 360])
        root.addWidget(splitter)

        self.setCentralWidget(central)
        self.setStatusBar(QStatusBar())
        self.statusBar().showMessage("Ready")

    def _panel_widget(self, title: str) -> QFrame:
        frame = QFrame()
        frame.setObjectName("Panel")
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)
        label = QLabel(title)
        label.setObjectName("Title")
        layout.addWidget(label)
        return frame

    def _bind_events(self) -> None:
        self.open_btn.clicked.connect(self.open_file)
        self.save_btn.clicked.connect(self.save_file)
        self.save_as_btn.clicked.connect(self.save_file_as)
        self.add_msg_btn.clicked.connect(self.add_message)
        self.remove_msg_btn.clicked.connect(self.remove_message)
        self.message_list.currentRowChanged.connect(self._message_selected)
        self.message_search.textChanged.connect(self._refresh_message_list)

        self.msg_name.editingFinished.connect(self._apply_message_fields)
        self.msg_frame_id.editingFinished.connect(self._apply_message_fields)
        self.msg_frame_id_mode.currentTextChanged.connect(self._set_frame_id_display_mode)
        self.msg_length.editingFinished.connect(self._apply_message_fields)
        self.msg_sender.editingFinished.connect(self._apply_message_fields)

        self.add_signal_btn.clicked.connect(self.add_signal)
        self.remove_signal_btn.clicked.connect(self.remove_signal)
        self.signal_table.itemChanged.connect(self._on_signal_table_changed)

    def open_file(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Open DBC File",
            str(Path.cwd()),
            "DBC Files (*.dbc);;All Files (*)",
        )
        if not path:
            return

        try:
            self.doc = load_dbc(path)
        except Exception as exc:  # pragma: no cover - Qt pathway
            QMessageBox.critical(self, "Open failed", str(exc))
            return

        self.current_message_index = 0 if self.doc.messages else None
        self._refresh_message_list()
        self._load_selected_message()
        self.statusBar().showMessage(f"Loaded {path}")

    def save_file(self) -> None:
        if self.doc.path:
            self._apply_message_fields()
            self._pull_signals_from_table()
            save_dbc(self.doc, self.doc.path)
            self.statusBar().showMessage(f"Saved {self.doc.path}")
            return
        self.save_file_as()

    def save_file_as(self) -> None:
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Save DBC File",
            str(Path.cwd() / "untitled.dbc"),
            "DBC Files (*.dbc)",
        )
        if not path:
            return
        self.doc.path = path
        self.save_file()

    def add_message(self) -> None:
        name = self._unique_message_name("NewMessage")
        message = MessageModel(
            frame_id=self._next_frame_id(),
            name=name,
            length=8,
            senders=["Vector__XXX"],
            signals=[],
        )
        self.doc.messages.append(message)
        self.current_message_index = len(self.doc.messages) - 1
        self._refresh_message_list()
        self._load_selected_message()

    def remove_message(self) -> None:
        if self.current_message_index is None:
            return
        del self.doc.messages[self.current_message_index]
        if not self.doc.messages:
            self.current_message_index = None
        else:
            self.current_message_index = max(0, self.current_message_index - 1)
        self._refresh_message_list()
        self._load_selected_message()

    def add_signal(self) -> None:
        message = self._current_message()
        if not message:
            return
        existing = {sig.name for sig in message.signals}
        base = "Signal"
        idx = 1
        while f"{base}{idx}" in existing:
            idx += 1
        message.signals.append(
            SignalModel(
                name=f"{base}{idx}",
                start=0,
                length=8,
                byte_order="little_endian",
                is_signed=False,
                scale=1.0,
                offset=0.0,
                minimum=0.0,
                maximum=255.0,
                unit="",
                receivers=["Vector__XXX"],
            )
        )
        self._load_signals(message)
        self.bit_layout.set_message(message)

    def remove_signal(self) -> None:
        message = self._current_message()
        if not message:
            return
        row = self.signal_table.currentRow()
        if row < 0 or row >= len(message.signals):
            return
        del message.signals[row]
        self._load_signals(message)
        self.bit_layout.set_message(message)

    def _message_selected(self, row: int) -> None:
        names = self._filtered_message_indices()
        if row < 0 or row >= len(names):
            return
        self.current_message_index = names[row]
        self._load_selected_message()

    def _load_selected_message(self) -> None:
        message = self._current_message()
        for widget in [self.msg_name, self.msg_frame_id, self.msg_length, self.msg_sender]:
            widget.blockSignals(True)

        if not message:
            self.msg_name.setText("")
            self.msg_frame_id.setValue(0)
            self.msg_length.setValue(0)
            self.msg_sender.setText("")
            self.signal_table.setRowCount(0)
            self.bit_layout.set_message(None)
        else:
            self.msg_name.setText(message.name)
            self.msg_frame_id.setValue(message.frame_id)
            self.msg_length.setValue(message.length)
            self.msg_sender.setText(message.senders[0] if message.senders else "")
            self._load_signals(message)
            self.bit_layout.set_message(message)

        for widget in [self.msg_name, self.msg_frame_id, self.msg_length, self.msg_sender]:
            widget.blockSignals(False)

    def _apply_message_fields(self) -> None:
        message = self._current_message()
        if not message:
            return
        message.name = self.msg_name.text().strip() or message.name
        message.frame_id = int(self.msg_frame_id.value())
        message.length = int(self.msg_length.value())
        sender = self.msg_sender.text().strip()
        message.senders = [sender] if sender else []
        self._refresh_message_list()

    def _load_signals(self, message: MessageModel) -> None:
        self.signal_table.blockSignals(True)
        self.signal_table.setRowCount(len(message.signals))
        for row, signal in enumerate(message.signals):
            values = [
                signal.name,
                str(signal.start),
                str(signal.length),
                _pretty(signal.scale),
                _pretty(signal.offset),
                signal.unit,
            ]
            for col, value in enumerate(values):
                actual_col = col if col < 3 else col + 2
                self.signal_table.setItem(row, actual_col, QTableWidgetItem(value))
            self._set_signal_choice(
                row,
                3,
                ["Little Endian", "Big Endian"],
                "Little Endian" if signal.byte_order == "little_endian" else "Big Endian",
            )
            self._set_signal_choice(
                row,
                4,
                ["Unsigned", "Signed"],
                "Signed" if signal.is_signed else "Unsigned",
            )
        self.signal_table.blockSignals(False)

    def _set_signal_choice(self, row: int, col: int, choices: list[str], current_value: str) -> None:
        combo = QComboBox()
        combo.addItems(choices)
        combo.setCurrentText(current_value)
        combo.currentIndexChanged.connect(self._on_signal_choice_changed)
        self.signal_table.setCellWidget(row, col, combo)

    def _signal_choice_text(self, row: int, col: int, fallback: str) -> str:
        widget = self.signal_table.cellWidget(row, col)
        if not isinstance(widget, QComboBox):
            return fallback
        text = widget.currentText().strip()
        return text if text else fallback

    def _set_frame_id_display_mode(self, mode: str) -> None:
        self.msg_frame_id.blockSignals(True)
        if mode == "Hex":
            self.msg_frame_id.setDisplayIntegerBase(16)
            self.msg_frame_id.setPrefix("0x")
        else:
            self.msg_frame_id.setDisplayIntegerBase(10)
            self.msg_frame_id.setPrefix("")
        self.msg_frame_id.blockSignals(False)
        self._apply_message_fields()

    def _on_signal_choice_changed(self, _index: int) -> None:
        self._pull_signals_from_table()
        self.bit_layout.set_message(self._current_message())

    def _pull_signals_from_table(self) -> None:
        message = self._current_message()
        if not message:
            return

        parsed: list[SignalModel] = []
        for row in range(self.signal_table.rowCount()):
            name = _item_text(self.signal_table, row, 0, fallback=f"Signal{row + 1}")
            start = _item_int(self.signal_table, row, 1, fallback=0)
            length = max(1, _item_int(self.signal_table, row, 2, fallback=1))
            endian_text = self._signal_choice_text(row, 3, fallback="Little Endian")
            signed_text = self._signal_choice_text(row, 4, fallback="Unsigned")
            scale = _item_float(self.signal_table, row, 5, fallback=1.0)
            offset = _item_float(self.signal_table, row, 6, fallback=0.0)
            unit = _item_text(self.signal_table, row, 7, fallback="")
            parsed.append(
                SignalModel(
                    name=name,
                    start=max(0, start),
                    length=min(length, 64),
                    byte_order="little_endian" if endian_text == "Little Endian" else "big_endian",
                    is_signed=signed_text == "Signed",
                    scale=scale,
                    offset=offset,
                    minimum=None,
                    maximum=None,
                    unit=unit,
                    receivers=["Vector__XXX"],
                )
            )

        message.signals = parsed

    def _on_signal_table_changed(self, _item: QTableWidgetItem) -> None:
        self._pull_signals_from_table()
        self.bit_layout.set_message(self._current_message())

    def _refresh_message_list(self) -> None:
        self.message_list.blockSignals(True)
        self.message_list.clear()
        for idx in self._filtered_message_indices():
            msg = self.doc.messages[idx]
            self.message_list.addItem(QListWidgetItem(f"0x{msg.frame_id:X}  {msg.name}"))

        if self.current_message_index is not None:
            filtered = self._filtered_message_indices()
            if self.current_message_index in filtered:
                self.message_list.setCurrentRow(filtered.index(self.current_message_index))
        self.message_list.blockSignals(False)

    def _filtered_message_indices(self) -> list[int]:
        query = self.message_search.text().strip().lower()
        if not query:
            return list(range(len(self.doc.messages)))
        result: list[int] = []
        for i, message in enumerate(self.doc.messages):
            if (
                query in message.name.lower()
                or query in f"{message.frame_id:x}"
                or query in f"0x{message.frame_id:x}"
                or query in str(message.frame_id)
            ):
                result.append(i)
        return result

    def _current_message(self) -> Optional[MessageModel]:
        if self.current_message_index is None:
            return None
        if self.current_message_index >= len(self.doc.messages):
            return None
        return self.doc.messages[self.current_message_index]

    def _next_frame_id(self) -> int:
        used = {msg.frame_id for msg in self.doc.messages}
        frame_id = 0x100
        while frame_id in used:
            frame_id += 1
        return frame_id

    def _unique_message_name(self, base: str) -> str:
        used = set(self.doc.message_names())
        if base not in used:
            return base
        idx = 1
        while f"{base}{idx}" in used:
            idx += 1
        return f"{base}{idx}"


def _item_text(table: QTableWidget, row: int, col: int, fallback: str) -> str:
    item = table.item(row, col)
    if not item:
        return fallback
    text = item.text().strip()
    return text if text else fallback


def _item_int(table: QTableWidget, row: int, col: int, fallback: int) -> int:
    try:
        return int(_item_text(table, row, col, str(fallback)), 0)
    except ValueError:
        return fallback


def _item_float(table: QTableWidget, row: int, col: int, fallback: float) -> float:
    try:
        return float(_item_text(table, row, col, str(fallback)))
    except ValueError:
        return fallback


def _pretty(value: float) -> str:
    return f"{value:.12g}"
