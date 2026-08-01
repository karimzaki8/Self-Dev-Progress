"""Reusable custom Qt widgets."""

from PyQt6.QtWidgets import (
    QFrame, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QWidget,
    QGraphicsDropShadowEffect,
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor

from electronics_store.assets.styles.theme import COLORS


class Card(QFrame):
    """A styled card container with optional shadow."""

    def __init__(self, parent: QWidget | None = None, shadow: bool = True) -> None:
        super().__init__(parent)
        self.setProperty("class", "card")
        if shadow:
            effect = QGraphicsDropShadowEffect(self)
            effect.setBlurRadius(20)
            effect.setOffset(0, 2)
            effect.setColor(QColor(0, 0, 0, 25))
            self.setGraphicsEffect(effect)


class StatusBanner(QFrame):
    """Dismissible banner for success / error / info messages."""

    dismissed = pyqtSignal()

    def __init__(
        self,
        message: str,
        variant: str = "info",
        parent: QWidget | None = None,
        dismissible: bool = True,
    ) -> None:
        super().__init__(parent)
        bg_map = {
            "success": ("#DCFCE7", "#166534"),
            "error": ("#FEE2E2", "#991B1B"),
            "info": ("#DBEAFE", "#1E40AF"),
            "warning": ("#FEF3C7", "#92400E"),
        }
        bg, fg = bg_map.get(variant, bg_map["info"])
        self.setStyleSheet(
            f"background-color: {bg}; border-radius: 8px; padding: 12px 16px;"
        )

        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 10, 16, 10)
        lbl = QLabel(message)
        lbl.setStyleSheet(f"color: {fg}; font-weight: 600; font-size: 14px; background: transparent;")
        lbl.setWordWrap(True)
        layout.addWidget(lbl, 1)

        if dismissible:
            btn = QPushButton("✕")
            btn.setFixedSize(28, 28)
            btn.setStyleSheet(
                f"background: transparent; color: {fg}; font-size: 16px; "
                "font-weight: 700; border: none; padding: 0;"
            )
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(self._dismiss)
            layout.addWidget(btn)

    def _dismiss(self) -> None:
        self.dismissed.emit()
        self.hide()


class SectionHeader(QWidget):
    """Section header with title and optional subtitle."""

    def __init__(
        self,
        title: str,
        subtitle: str = "",
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 8)
        layout.setSpacing(4)

        title_lbl = QLabel(title)
        title_lbl.setProperty("class", "heading")
        layout.addWidget(title_lbl)

        if subtitle:
            sub_lbl = QLabel(subtitle)
            sub_lbl.setProperty("class", "muted")
            layout.addWidget(sub_lbl)


class StepIndicator(QWidget):
    """Horizontal step progress indicator for the login flow."""

    def __init__(self, steps: list[str], parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._steps = steps
        self._current = 0
        self._labels: list[QLabel] = []
        self._circles: list[QLabel] = []

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        for i, step_text in enumerate(steps):
            col = QVBoxLayout()
            col.setAlignment(Qt.AlignmentFlag.AlignHCenter)

            circle = QLabel(str(i + 1))
            circle.setFixedSize(36, 36)
            circle.setAlignment(Qt.AlignmentFlag.AlignCenter)
            circle.setStyleSheet(self._circle_style(i == 0))
            self._circles.append(circle)
            col.addWidget(circle, alignment=Qt.AlignmentFlag.AlignHCenter)

            lbl = QLabel(step_text)
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl.setStyleSheet("font-size: 12px; color: #64748B;")
            self._labels.append(lbl)
            col.addWidget(lbl)

            layout.addLayout(col)

            if i < len(steps) - 1:
                line = QFrame()
                line.setFrameShape(QFrame.Shape.HLine)
                line.setFixedHeight(2)
                line.setStyleSheet(f"background-color: {COLORS['border']}; margin-top: -18px;")
                layout.addWidget(line, 1)

    def set_step(self, index: int) -> None:
        self._current = index
        for i, (circle, lbl) in enumerate(zip(self._circles, self._labels)):
            active = i <= index
            circle.setStyleSheet(self._circle_style(active))
            lbl.setStyleSheet(
                f"font-size: 12px; font-weight: {'600' if active else '400'}; "
                f"color: {COLORS['text'] if active else COLORS['text_muted']};"
            )

    @staticmethod
    def _circle_style(active: bool) -> str:
        if active:
            return (
                f"background-color: {COLORS['primary']}; color: white; "
                "border-radius: 18px; font-weight: 700; font-size: 14px;"
            )
        return (
            f"background-color: {COLORS['border']}; color: {COLORS['text_muted']}; "
            "border-radius: 18px; font-weight: 600; font-size: 14px;"
        )
