APP_STYLESHEET = """
QMainWindow {
    background: #f6f8fb;
}
QWidget {
    font-family: "IBM Plex Sans";
    font-size: 13px;
    color: #1f2933;
}
QFrame#Panel {
    border: 1px solid #d7dde5;
    border-radius: 10px;
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #ffffff, stop:1 #f5f7fa);
}
QLabel#Title {
    font-size: 16px;
    font-weight: 700;
    color: #0f172a;
}
QPushButton {
    background: #0f766e;
    border: 1px solid #0b5e58;
    color: #ffffff;
    border-radius: 8px;
    padding: 6px 10px;
    font-weight: 600;
}
QPushButton:hover {
    background: #0d9488;
}
QPushButton:disabled {
    background: #9ca3af;
    border-color: #9ca3af;
}
QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox {
    background: #ffffff;
    border: 1px solid #c7ced8;
    border-radius: 7px;
    padding: 4px 6px;
}
QListWidget, QTableWidget {
    background: #ffffff;
    border: 1px solid #c7ced8;
    border-radius: 8px;
    gridline-color: #e4e9ef;
}
QHeaderView::section {
    background: #eef2f7;
    border: 0;
    border-bottom: 1px solid #dbe2ea;
    padding: 4px;
    font-weight: 600;
}
QStatusBar {
    background: #e9eef4;
}
"""
