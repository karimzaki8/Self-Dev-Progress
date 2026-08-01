"""Application-wide Qt stylesheet and color palette."""

COLORS = {
    "primary": "#2563EB",
    "primary_hover": "#1D4ED8",
    "primary_pressed": "#1E40AF",
    "success": "#16A34A",
    "success_hover": "#15803D",
    "danger": "#DC2626",
    "danger_hover": "#B91C1C",
    "warning": "#F59E0B",
    "bg": "#F8FAFC",
    "surface": "#FFFFFF",
    "border": "#E2E8F0",
    "text": "#1E293B",
    "text_secondary": "#64748B",
    "text_muted": "#94A3B8",
    "input_bg": "#F1F5F9",
    "input_focus": "#DBEAFE",
    "header_bg": "#1E293B",
    "header_text": "#F8FAFC",
    "sidebar_bg": "#F1F5F9",
    "sidebar_active": "#DBEAFE",
    "table_alt": "#F8FAFC",
    "table_header": "#E2E8F0",
    "discount_badge": "#DCFCE7",
    "discount_text": "#166534",
}


def get_stylesheet() -> str:
    c = COLORS
    return f"""
    /* ─── Global ─── */
    QMainWindow, QWidget {{
        background-color: {c["bg"]};
        color: {c["text"]};
        font-family: "Segoe UI", "Helvetica Neue", Arial, sans-serif;
        font-size: 14px;
    }}

    /* ─── Buttons ─── */
    QPushButton {{
        background-color: {c["primary"]};
        color: white;
        border: none;
        border-radius: 6px;
        padding: 10px 24px;
        font-weight: 600;
        font-size: 14px;
        min-height: 20px;
    }}
    QPushButton:hover {{
        background-color: {c["primary_hover"]};
    }}
    QPushButton:pressed {{
        background-color: {c["primary_pressed"]};
    }}
    QPushButton:disabled {{
        background-color: {c["border"]};
        color: {c["text_muted"]};
    }}
    QPushButton[class="success"] {{
        background-color: {c["success"]};
    }}
    QPushButton[class="success"]:hover {{
        background-color: {c["success_hover"]};
    }}
    QPushButton[class="danger"] {{
        background-color: {c["danger"]};
    }}
    QPushButton[class="danger"]:hover {{
        background-color: {c["danger_hover"]};
    }}
    QPushButton[class="secondary"] {{
        background-color: transparent;
        color: {c["primary"]};
        border: 2px solid {c["primary"]};
    }}
    QPushButton[class="secondary"]:hover {{
        background-color: {c["input_focus"]};
    }}

    /* ─── Line edits ─── */
    QLineEdit {{
        background-color: {c["input_bg"]};
        border: 2px solid {c["border"]};
        border-radius: 6px;
        padding: 10px 14px;
        font-size: 14px;
        color: {c["text"]};
        selection-background-color: {c["primary"]};
    }}
    QLineEdit:focus {{
        border-color: {c["primary"]};
        background-color: {c["input_focus"]};
    }}

    /* ─── Combo boxes ─── */
    QComboBox {{
        background-color: {c["input_bg"]};
        border: 2px solid {c["border"]};
        border-radius: 6px;
        padding: 8px 14px;
        font-size: 14px;
        min-height: 20px;
    }}
    QComboBox:focus {{
        border-color: {c["primary"]};
    }}
    QComboBox::drop-down {{
        border: none;
        width: 30px;
    }}
    QComboBox QAbstractItemView {{
        background-color: {c["surface"]};
        border: 1px solid {c["border"]};
        selection-background-color: {c["sidebar_active"]};
        selection-color: {c["text"]};
    }}

    /* ─── Labels ─── */
    QLabel {{
        color: {c["text"]};
    }}
    QLabel[class="heading"] {{
        font-size: 22px;
        font-weight: 700;
        color: {c["text"]};
    }}
    QLabel[class="subheading"] {{
        font-size: 16px;
        font-weight: 600;
        color: {c["text_secondary"]};
    }}
    QLabel[class="muted"] {{
        color: {c["text_muted"]};
        font-size: 13px;
    }}
    QLabel[class="error"] {{
        color: {c["danger"]};
        font-weight: 600;
    }}
    QLabel[class="success"] {{
        color: {c["success"]};
        font-weight: 600;
    }}
    QLabel[class="code"] {{
        font-family: "Consolas", "Courier New", monospace;
        font-size: 28px;
        font-weight: 700;
        color: {c["primary"]};
        letter-spacing: 8px;
        padding: 12px 20px;
        background-color: {c["input_bg"]};
        border: 2px dashed {c["primary"]};
        border-radius: 8px;
    }}

    /* ─── Tables ─── */
    QTableWidget {{
        background-color: {c["surface"]};
        border: 1px solid {c["border"]};
        border-radius: 8px;
        gridline-color: {c["border"]};
        font-size: 13px;
    }}
    QTableWidget::item {{
        padding: 8px 12px;
    }}
    QTableWidget::item:selected {{
        background-color: {c["sidebar_active"]};
        color: {c["text"]};
    }}
    QHeaderView::section {{
        background-color: {c["table_header"]};
        color: {c["text"]};
        font-weight: 600;
        padding: 10px 12px;
        border: none;
        border-bottom: 2px solid {c["border"]};
    }}
    QTableWidget::item:alternate {{
        background-color: {c["table_alt"]};
    }}

    /* ─── Scroll bars ─── */
    QScrollBar:vertical {{
        background-color: transparent;
        width: 10px;
        margin: 0;
    }}
    QScrollBar::handle:vertical {{
        background-color: {c["text_muted"]};
        border-radius: 5px;
        min-height: 30px;
    }}
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0;
    }}

    /* ─── Radio buttons ─── */
    QRadioButton {{
        font-size: 14px;
        spacing: 8px;
        padding: 6px 0;
    }}
    QRadioButton::indicator {{
        width: 18px;
        height: 18px;
    }}

    /* ─── Group boxes ─── */
    QGroupBox {{
        font-weight: 600;
        font-size: 14px;
        border: 1px solid {c["border"]};
        border-radius: 8px;
        margin-top: 12px;
        padding: 16px 12px 12px 12px;
    }}
    QGroupBox::title {{
        subcontrol-origin: margin;
        subcontrol-position: top left;
        padding: 4px 12px;
        color: {c["text_secondary"]};
    }}

    /* ─── Frames / cards ─── */
    QFrame[class="card"] {{
        background-color: {c["surface"]};
        border: 1px solid {c["border"]};
        border-radius: 10px;
        padding: 20px;
    }}

    /* ─── Progress bar ─── */
    QProgressBar {{
        border: none;
        border-radius: 4px;
        background-color: {c["input_bg"]};
        text-align: center;
        font-size: 12px;
        min-height: 8px;
        max-height: 8px;
    }}
    QProgressBar::chunk {{
        background-color: {c["primary"]};
        border-radius: 4px;
    }}

    /* ─── Spin box ─── */
    QSpinBox {{
        background-color: {c["input_bg"]};
        border: 2px solid {c["border"]};
        border-radius: 6px;
        padding: 8px 14px;
        font-size: 14px;
        min-height: 20px;
    }}
    QSpinBox:focus {{
        border-color: {c["primary"]};
    }}

    /* ─── Check box ─── */
    QCheckBox {{
        font-size: 14px;
        spacing: 8px;
    }}
    QCheckBox::indicator {{
        width: 18px;
        height: 18px;
    }}

    /* ─── Message box ─── */
    QMessageBox {{
        background-color: {c["surface"]};
    }}
    QMessageBox QLabel {{
        font-size: 14px;
    }}
    """
