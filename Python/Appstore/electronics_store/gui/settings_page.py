"""Settings page — user preferences management."""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QComboBox, QCheckBox, QSpacerItem, QSizePolicy,
)
from PyQt6.QtCore import Qt, pyqtSignal

from electronics_store.config.settings import Settings
from electronics_store.config.constants import CURRENCY_RATES, CURRENCY_SYMBOLS
from electronics_store.gui.widgets.custom_widgets import Card, SectionHeader, StatusBanner


class SettingsPage(QWidget):
    settings_changed = pyqtSignal()

    def __init__(self, settings: Settings, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._settings = settings
        self._build_ui()
        self._load_values()

    def _build_ui(self) -> None:
        outer = QVBoxLayout(self)
        outer.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        outer.setContentsMargins(40, 40, 40, 40)

        card = Card(shadow=True)
        card.setFixedWidth(520)
        layout = QVBoxLayout(card)
        layout.setSpacing(16)
        layout.setContentsMargins(32, 32, 32, 32)

        layout.addWidget(SectionHeader("Settings", "Customize your experience"))

        self._banner_area = QVBoxLayout()
        layout.addLayout(self._banner_area)

        # Default currency
        layout.addWidget(QLabel("Default Currency"))
        self._currency_combo = QComboBox()
        for code in CURRENCY_RATES:
            symbol = CURRENCY_SYMBOLS[code]
            self._currency_combo.addItem(f"{symbol}  {code}", code)
        layout.addWidget(self._currency_combo)

        # Default delivery method
        layout.addWidget(QLabel("Default Shipping Method"))
        self._delivery_combo = QComboBox()
        self._delivery_combo.addItem("Delivery", "delivery")
        self._delivery_combo.addItem("Pick-up", "pickup")
        layout.addWidget(self._delivery_combo)

        # Remember username
        self._remember_check = QCheckBox("Remember username on login")
        layout.addWidget(self._remember_check)

        layout.addSpacing(12)

        # Buttons
        btn_row = QHBoxLayout()
        reset_btn = QPushButton("Reset to Defaults")
        reset_btn.setProperty("class", "secondary")
        reset_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        reset_btn.clicked.connect(self._on_reset)
        btn_row.addWidget(reset_btn)

        btn_row.addItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        save_btn = QPushButton("Save Settings")
        save_btn.setProperty("class", "success")
        save_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        save_btn.clicked.connect(self._on_save)
        btn_row.addWidget(save_btn)

        layout.addLayout(btn_row)

        outer.addWidget(card)
        outer.addItem(QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

    def _load_values(self) -> None:
        currency = self._settings.get("currency")
        idx = self._currency_combo.findData(currency)
        if idx >= 0:
            self._currency_combo.setCurrentIndex(idx)

        delivery = self._settings.get("delivery_method")
        idx = self._delivery_combo.findData(delivery)
        if idx >= 0:
            self._delivery_combo.setCurrentIndex(idx)

        self._remember_check.setChecked(self._settings.get("remember_username"))

    def _clear_banner(self) -> None:
        while self._banner_area.count():
            item = self._banner_area.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def _show_banner(self, msg: str, variant: str = "success") -> None:
        self._clear_banner()
        banner = StatusBanner(msg, variant, dismissible=True)
        self._banner_area.addWidget(banner)

    def _on_save(self) -> None:
        self._settings.set("currency", self._currency_combo.currentData())
        self._settings.set("delivery_method", self._delivery_combo.currentData())
        self._settings.set("remember_username", self._remember_check.isChecked())
        self._settings.save()
        self._show_banner("Settings saved successfully!", "success")
        self.settings_changed.emit()

    def _on_reset(self) -> None:
        self._settings.reset()
        self._load_values()
        self._show_banner("Settings reset to defaults.", "info")
        self.settings_changed.emit()
