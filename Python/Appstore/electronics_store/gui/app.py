"""Main application window — sidebar navigation between pages."""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QLabel,
    QPushButton, QStackedWidget, QSpacerItem, QSizePolicy, QFrame,
)
from PyQt6.QtCore import Qt

from electronics_store.config.constants import APP_NAME, APP_VERSION, WINDOW_WIDTH, WINDOW_HEIGHT, MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT
from electronics_store.config.settings import Settings
from electronics_store.services.auth_service import AuthService
from electronics_store.services.store_service import StoreService
from electronics_store.gui.login_page import LoginPage
from electronics_store.gui.store_page import StorePage
from electronics_store.gui.checkout_page import CheckoutPage
from electronics_store.gui.settings_page import SettingsPage
from electronics_store.assets.styles.theme import COLORS


class _NavButton(QPushButton):
    """Sidebar navigation button."""

    def __init__(self, icon: str, label: str, parent: QWidget | None = None) -> None:
        super().__init__(f"  {icon}   {label}", parent)
        self.setFixedHeight(44)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setCheckable(True)
        self._update_style(False)

    def _update_style(self, active: bool) -> None:
        if active:
            self.setStyleSheet(
                f"text-align: left; padding-left: 16px; font-weight: 600; font-size: 14px; "
                f"background-color: {COLORS['sidebar_active']}; color: {COLORS['primary']}; "
                f"border: none; border-radius: 8px;"
            )
        else:
            self.setStyleSheet(
                f"text-align: left; padding-left: 16px; font-weight: 500; font-size: 14px; "
                f"background-color: transparent; color: {COLORS['text_secondary']}; "
                f"border: none; border-radius: 8px;"
            )

    def set_active(self, active: bool) -> None:
        self.setChecked(active)
        self._update_style(active)


class MainWindow(QMainWindow):
    PAGE_LOGIN = 0
    PAGE_STORE = 1
    PAGE_CHECKOUT = 2
    PAGE_SETTINGS = 3

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle(f"{APP_NAME} v{APP_VERSION}")
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setMinimumSize(MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT)

        self._settings = Settings()
        self._auth_service = AuthService()
        self._store_service = StoreService()

        self._build_ui()
        self._connect_signals()
        self._show_page(self.PAGE_LOGIN)

    def _build_ui(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)
        root = QHBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── Sidebar ──
        self._sidebar = QFrame()
        self._sidebar.setFixedWidth(220)
        self._sidebar.setStyleSheet(
            f"background-color: {COLORS['sidebar_bg']}; "
            f"border-right: 1px solid {COLORS['border']};"
        )
        sidebar_layout = QVBoxLayout(self._sidebar)
        sidebar_layout.setContentsMargins(12, 16, 12, 16)
        sidebar_layout.setSpacing(6)

        # Brand
        brand = QLabel(f"  🖥  {APP_NAME}")
        brand.setStyleSheet(
            f"font-size: 16px; font-weight: 700; color: {COLORS['text']}; padding: 8px 0 16px 4px;"
        )
        sidebar_layout.addWidget(brand)

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet(f"color: {COLORS['border']};")
        sidebar_layout.addWidget(sep)
        sidebar_layout.addSpacing(8)

        self._nav_buttons: list[_NavButton] = []

        self._nav_store = _NavButton("🛒", "Store")
        self._nav_checkout = _NavButton("📦", "Checkout")
        self._nav_settings = _NavButton("⚙", "Settings")

        for btn in (self._nav_store, self._nav_checkout, self._nav_settings):
            sidebar_layout.addWidget(btn)
            self._nav_buttons.append(btn)

        sidebar_layout.addItem(
            QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        )

        # User / logout area
        self._user_label = QLabel("")
        self._user_label.setStyleSheet(
            f"color: {COLORS['text_secondary']}; font-size: 12px; padding: 4px;"
        )
        sidebar_layout.addWidget(self._user_label)

        self._logout_btn = QPushButton("Logout")
        self._logout_btn.setProperty("class", "danger")
        self._logout_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._logout_btn.setFixedHeight(36)
        sidebar_layout.addWidget(self._logout_btn)

        version_label = QLabel(f"v{APP_VERSION}")
        version_label.setProperty("class", "muted")
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sidebar_layout.addWidget(version_label)

        self._sidebar.hide()
        root.addWidget(self._sidebar)

        # ── Page stack ──
        self._stack = QStackedWidget()
        root.addWidget(self._stack, 1)

        self._login_page = LoginPage(self._auth_service)
        self._store_page = StorePage(self._store_service)
        self._checkout_page = CheckoutPage(self._store_service)
        self._settings_page = SettingsPage(self._settings)

        self._stack.addWidget(self._login_page)    # 0
        self._stack.addWidget(self._store_page)    # 1
        self._stack.addWidget(self._checkout_page) # 2
        self._stack.addWidget(self._settings_page) # 3

    def _connect_signals(self) -> None:
        self._login_page.login_successful.connect(self._on_login_success)
        self._store_page.go_to_cart.connect(lambda: self._show_page(self.PAGE_CHECKOUT))
        self._checkout_page.back_to_store.connect(lambda: self._show_page(self.PAGE_STORE))
        self._checkout_page.order_completed.connect(self._on_order_completed)
        self._logout_btn.clicked.connect(self._on_logout)

        self._nav_store.clicked.connect(lambda: self._show_page(self.PAGE_STORE))
        self._nav_checkout.clicked.connect(lambda: self._show_page(self.PAGE_CHECKOUT))
        self._nav_settings.clicked.connect(lambda: self._show_page(self.PAGE_SETTINGS))

    def _show_page(self, index: int) -> None:
        self._stack.setCurrentIndex(index)

        if index == self.PAGE_LOGIN:
            self._sidebar.hide()
        else:
            self._sidebar.show()

        for i, btn in enumerate(self._nav_buttons):
            btn.set_active(i + 1 == index)  # nav_buttons indices are 0-based but pages start at 1

        if index == self.PAGE_STORE:
            self._store_page.refresh_catalog()
        elif index == self.PAGE_CHECKOUT:
            self._checkout_page.refresh()

    def _on_login_success(self, display_name: str) -> None:
        self._user_label.setText(f"Logged in as\n{display_name}")
        self._show_page(self.PAGE_STORE)

    def _on_order_completed(self) -> None:
        self._show_page(self.PAGE_STORE)

    def _on_logout(self) -> None:
        self._auth_service.logout()
        self._store_service = StoreService()
        self._store_page._store = self._store_service
        self._checkout_page._store = self._store_service
        self._login_page.reset()
        self._user_label.setText("")
        self._show_page(self.PAGE_LOGIN)
