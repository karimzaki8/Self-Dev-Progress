"""Login page implementing the multi-step authentication flow from the PDF.

Steps:
  1. Enter username → verify
  2. Enter password → verify
  3. System shows verification code → user inputs code → verify
  4. Welcome message → proceed to store
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QSpacerItem, QSizePolicy,
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer

from electronics_store.services.auth_service import AuthService
from electronics_store.gui.widgets.custom_widgets import Card, StatusBanner, SectionHeader, StepIndicator


class LoginPage(QWidget):
    login_successful = pyqtSignal(str)  # emits display_name

    def __init__(self, auth_service: AuthService, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._auth = auth_service
        self._step = 0  # 0=username, 1=password, 2=code, 3=welcome
        self._username = ""

        self._build_ui()

    def _build_ui(self) -> None:
        outer = QVBoxLayout(self)
        outer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        outer.setContentsMargins(40, 40, 40, 40)

        card = Card(shadow=True)
        card.setFixedWidth(480)
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(16)
        card_layout.setContentsMargins(32, 32, 32, 32)

        # Header
        header = SectionHeader("Electronics Store", "Sign in to your account")
        card_layout.addWidget(header)

        # Step indicator
        self._step_indicator = StepIndicator(["Username", "Password", "Verify", "Done"])
        card_layout.addWidget(self._step_indicator)
        card_layout.addSpacing(8)

        # Banner area
        self._banner_area = QVBoxLayout()
        card_layout.addLayout(self._banner_area)

        # Input label
        self._input_label = QLabel("Enter your username")
        self._input_label.setProperty("class", "subheading")
        card_layout.addWidget(self._input_label)

        # Verification code display (hidden by default)
        self._code_display = QLabel("")
        self._code_display.setProperty("class", "code")
        self._code_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._code_display.hide()
        card_layout.addWidget(self._code_display)

        # Text input
        self._input_field = QLineEdit()
        self._input_field.setPlaceholderText("Username")
        self._input_field.returnPressed.connect(self._on_submit)
        card_layout.addWidget(self._input_field)

        # Buttons row
        btn_row = QHBoxLayout()
        self._back_btn = QPushButton("Back")
        self._back_btn.setProperty("class", "secondary")
        self._back_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._back_btn.clicked.connect(self._on_back)
        self._back_btn.hide()
        btn_row.addWidget(self._back_btn)

        btn_row.addItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        self._submit_btn = QPushButton("Continue")
        self._submit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._submit_btn.clicked.connect(self._on_submit)
        btn_row.addWidget(self._submit_btn)

        card_layout.addLayout(btn_row)

        # Welcome label (hidden)
        self._welcome_label = QLabel("")
        self._welcome_label.setProperty("class", "heading")
        self._welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._welcome_label.hide()
        card_layout.addWidget(self._welcome_label)

        outer.addWidget(card)

    def _clear_banner(self) -> None:
        while self._banner_area.count():
            item = self._banner_area.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def _show_banner(self, message: str, variant: str = "error") -> None:
        self._clear_banner()
        banner = StatusBanner(message, variant, dismissible=True)
        self._banner_area.addWidget(banner)

    def _on_submit(self) -> None:
        text = self._input_field.text().strip()

        if self._step == 0:
            if not text:
                self._show_banner("Please enter a username.", "warning")
                return
            ok, msg = self._auth.verify_username(text)
            if ok:
                self._username = text
                self._step = 1
                self._update_ui()
                self._clear_banner()
            else:
                self._show_banner(msg, "error")

        elif self._step == 1:
            if not text:
                self._show_banner("Please enter your password.", "warning")
                return
            ok, code_or_msg = self._auth.verify_password(self._username, text)
            if ok:
                self._step = 2
                self._update_ui()
                self._clear_banner()
            else:
                self._show_banner(code_or_msg, "error")

        elif self._step == 2:
            if not text:
                self._show_banner("Please enter the verification code.", "warning")
                return
            ok, msg = self._auth.verify_code(self._username, text)
            if ok:
                self._step = 3
                self._welcome_msg = msg
                self._update_ui()
                self._clear_banner()
            else:
                self._show_banner(msg, "error")

    def _on_back(self) -> None:
        if self._step > 0:
            self._step -= 1
            self._clear_banner()
            self._update_ui()

    def _update_ui(self) -> None:
        self._step_indicator.set_step(self._step)
        self._input_field.clear()

        if self._step == 0:
            self._input_label.setText("Enter your username")
            self._input_field.setPlaceholderText("Username")
            self._input_field.setEchoMode(QLineEdit.EchoMode.Normal)
            self._input_field.show()
            self._submit_btn.show()
            self._submit_btn.setText("Continue")
            self._back_btn.hide()
            self._code_display.hide()
            self._welcome_label.hide()

        elif self._step == 1:
            self._input_label.setText("Enter your password")
            self._input_field.setPlaceholderText("Password")
            self._input_field.setEchoMode(QLineEdit.EchoMode.Password)
            self._input_field.show()
            self._submit_btn.show()
            self._submit_btn.setText("Continue")
            self._back_btn.show()
            self._code_display.hide()
            self._welcome_label.hide()

        elif self._step == 2:
            self._input_label.setText("Enter the verification code shown below")
            self._code_display.setText(self._auth.verification_code)
            self._code_display.show()
            self._input_field.setPlaceholderText("Verification code")
            self._input_field.setEchoMode(QLineEdit.EchoMode.Normal)
            self._input_field.show()
            self._submit_btn.show()
            self._submit_btn.setText("Verify")
            self._back_btn.show()
            self._welcome_label.hide()

        elif self._step == 3:
            self._input_label.hide()
            self._input_field.hide()
            self._code_display.hide()
            self._back_btn.hide()
            self._submit_btn.hide()
            self._welcome_label.setText(self._welcome_msg)
            self._welcome_label.show()
            self._show_banner("Login successful! Redirecting to the store…", "success")
            QTimer.singleShot(1800, self._emit_login)

        self._input_field.setFocus()

    def _emit_login(self) -> None:
        user = self._auth.current_user
        name = user.display_name if user else self._username
        self.login_successful.emit(name)

    def reset(self) -> None:
        self._step = 0
        self._username = ""
        self._clear_banner()
        self._input_label.show()
        self._update_ui()
