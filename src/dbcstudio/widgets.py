from __future__ import annotations

from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPainter, QPen
from PySide6.QtWidgets import QWidget

from .model import MessageModel


class SignalBitLayout(QWidget):
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self._message: Optional[MessageModel] = None
        self.setMinimumHeight(220)

    def set_message(self, message: Optional[MessageModel]) -> None:
        self._message = message
        self.update()

    def paintEvent(self, event) -> None:  # noqa: N802
        del event
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor("#ffffff"))

        margin = 12
        cols = 8
        rows = 8
        grid_w = self.width() - 2 * margin
        grid_h = self.height() - 2 * margin
        cell_w = grid_w / cols
        cell_h = grid_h / rows

        pen = QPen(QColor("#d8dee8"))
        painter.setPen(pen)

        for r in range(rows + 1):
            y = margin + r * cell_h
            painter.drawLine(margin, int(y), self.width() - margin, int(y))
        for c in range(cols + 1):
            x = margin + c * cell_w
            painter.drawLine(int(x), margin, int(x), self.height() - margin)

        if not self._message:
            painter.setPen(QColor("#64748b"))
            painter.drawText(self.rect(), Qt.AlignCenter, "Select a message to view bit layout")
            return

        palette = [
            QColor("#0ea5e9"),
            QColor("#f59e0b"),
            QColor("#10b981"),
            QColor("#ef4444"),
            QColor("#6366f1"),
            QColor("#14b8a6"),
        ]
        for idx, signal in enumerate(self._message.signals):
            color = palette[idx % len(palette)]
            start = signal.start
            end = min(signal.start + signal.length - 1, 63)
            for bit in range(start, end + 1):
                row = bit // 8
                col = bit % 8
                x = margin + col * cell_w
                y = margin + row * cell_h
                painter.fillRect(int(x + 1), int(y + 1), int(cell_w - 1), int(cell_h - 1), color)

            painter.setPen(QColor("#0f172a"))
            painter.drawText(
                margin + 6,
                margin + 16 + (idx * 16),
                f"{signal.name}: bit {signal.start}..{signal.start + signal.length - 1}",
            )

        painter.end()
