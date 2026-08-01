"""Checkout page — cart review, delivery/pickup, currency, order confirmation.

Implements PDF steps 7–10 plus extensions:
  7. Delivery ($200) or Pick-up ($50) charge
  8. Currency selection (USD, EUR, EGP) — invalid defaults to USD
  9. Final total display
  10. Order confirmation
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QRadioButton,
    QButtonGroup, QTableWidget, QTableWidgetItem, QComboBox,
    QSpacerItem, QSizePolicy, QHeaderView, QAbstractItemView, QFrame,
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer

from electronics_store.services.store_service import StoreService
from electronics_store.services.currency_service import CurrencyService
from electronics_store.config.constants import (
    DELIVERY_CHARGE, PICKUP_CHARGE, CURRENCY_RATES, CURRENCY_SYMBOLS,
)
from electronics_store.utils.helpers import format_price
from electronics_store.models.cart import Cart
from electronics_store.gui.widgets.custom_widgets import Card, StatusBanner, SectionHeader
from electronics_store.assets.styles.theme import COLORS


class CheckoutPage(QWidget):
    back_to_store = pyqtSignal()
    order_completed = pyqtSignal()

    def __init__(self, store_service: StoreService, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._store = store_service
        self._build_ui()

    def _build_ui(self) -> None:
        main = QHBoxLayout(self)
        main.setContentsMargins(24, 24, 24, 24)
        main.setSpacing(20)

        # ── Left: cart items ──
        left = QVBoxLayout()
        left.setSpacing(12)

        back_btn = QPushButton("← Back to Store")
        back_btn.setProperty("class", "secondary")
        back_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        back_btn.clicked.connect(self.back_to_store.emit)
        left.addWidget(back_btn, alignment=Qt.AlignmentFlag.AlignLeft)

        left.addWidget(SectionHeader("Your Cart", "Review items before placing your order"))

        self._banner_area = QVBoxLayout()
        left.addLayout(self._banner_area)

        self._cart_table = QTableWidget()
        self._cart_table.setColumnCount(6)
        self._cart_table.setHorizontalHeaderLabels([
            "Product", "Unit Price", "Qty", "Discount", "Subtotal", ""
        ])
        self._cart_table.setAlternatingRowColors(True)
        self._cart_table.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self._cart_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self._cart_table.verticalHeader().setVisible(False)
        self._cart_table.horizontalHeader().setStretchLastSection(False)
        self._cart_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        for col in range(1, 5):
            self._cart_table.horizontalHeader().setSectionResizeMode(
                col, QHeaderView.ResizeMode.ResizeToContents
            )
        self._cart_table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)
        self._cart_table.setColumnWidth(5, 80)
        left.addWidget(self._cart_table, 1)

        self._empty_label = QLabel("Your cart is empty. Go back and add some products!")
        self._empty_label.setProperty("class", "muted")
        self._empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._empty_label.hide()
        left.addWidget(self._empty_label)

        main.addLayout(left, 3)

        # ── Right: order summary ──
        right_card = Card(shadow=True)
        right_card.setFixedWidth(360)
        right = QVBoxLayout(right_card)
        right.setSpacing(14)
        right.setContentsMargins(24, 24, 24, 24)

        right.addWidget(SectionHeader("Order Summary"))

        # Delivery method
        delivery_group_label = QLabel("Shipping Method")
        delivery_group_label.setProperty("class", "subheading")
        right.addWidget(delivery_group_label)

        self._delivery_group = QButtonGroup(self)
        self._delivery_radio = QRadioButton(f"Delivery — {format_price(DELIVERY_CHARGE)}")
        self._pickup_radio = QRadioButton(f"Pick-up — {format_price(PICKUP_CHARGE)}")
        self._delivery_radio.setChecked(True)
        self._delivery_group.addButton(self._delivery_radio, 0)
        self._delivery_group.addButton(self._pickup_radio, 1)
        self._delivery_group.idToggled.connect(self._on_delivery_changed)
        right.addWidget(self._delivery_radio)
        right.addWidget(self._pickup_radio)

        right.addSpacing(4)

        # Currency
        currency_label = QLabel("Payment Currency")
        currency_label.setProperty("class", "subheading")
        right.addWidget(currency_label)

        self._currency_combo = QComboBox()
        for code in CURRENCY_RATES:
            symbol = CURRENCY_SYMBOLS[code]
            rate_text = f"1 USD = {CURRENCY_RATES[code]} {code}" if code != "USD" else "Base currency"
            self._currency_combo.addItem(f"{symbol}  {code} — {rate_text}", code)
        self._currency_combo.currentIndexChanged.connect(self._on_currency_changed)
        right.addWidget(self._currency_combo)

        right.addSpacing(4)

        # Price breakdown
        sep1 = QFrame()
        sep1.setFrameShape(QFrame.Shape.HLine)
        sep1.setStyleSheet(f"color: {COLORS['border']};")
        right.addWidget(sep1)

        self._subtotal_label = QLabel("Subtotal: $0.00")
        right.addWidget(self._subtotal_label)

        self._discount_label = QLabel("Discounts applied: included above")
        self._discount_label.setStyleSheet(f"color: {COLORS['discount_text']}; font-size: 13px;")
        right.addWidget(self._discount_label)

        self._shipping_label = QLabel(f"Shipping: {format_price(DELIVERY_CHARGE)}")
        right.addWidget(self._shipping_label)

        sep2 = QFrame()
        sep2.setFrameShape(QFrame.Shape.HLine)
        sep2.setStyleSheet(f"color: {COLORS['border']};")
        right.addWidget(sep2)

        self._total_label = QLabel("Total: $0.00")
        self._total_label.setStyleSheet(
            f"font-size: 22px; font-weight: 700; color: {COLORS['primary']};"
        )
        right.addWidget(self._total_label)

        self._currency_note = QLabel("")
        self._currency_note.setProperty("class", "muted")
        right.addWidget(self._currency_note)

        right.addItem(QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        # Place order
        self._place_order_btn = QPushButton("Place Order")
        self._place_order_btn.setProperty("class", "success")
        self._place_order_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._place_order_btn.clicked.connect(self._on_place_order)
        right.addWidget(self._place_order_btn)

        main.addWidget(right_card)

    # ── Data refresh ──

    def refresh(self) -> None:
        cart = self._store.cart
        self._populate_table(cart)
        self._update_totals(cart)
        is_empty = cart.is_empty
        self._cart_table.setVisible(not is_empty)
        self._empty_label.setVisible(is_empty)
        self._place_order_btn.setEnabled(not is_empty)

    def _populate_table(self, cart: Cart) -> None:
        self._cart_table.setRowCount(0)
        for i, item in enumerate(cart.items):
            row = self._cart_table.rowCount()
            self._cart_table.insertRow(row)

            self._cart_table.setItem(row, 0, QTableWidgetItem(item.product_name))

            price_item = QTableWidgetItem(format_price(item.unit_price))
            price_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self._cart_table.setItem(row, 1, price_item)

            qty_item = QTableWidgetItem(str(item.quantity))
            qty_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self._cart_table.setItem(row, 2, qty_item)

            disc_item = QTableWidgetItem(f"{int(item.discount_rate * 100)}%")
            disc_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self._cart_table.setItem(row, 3, disc_item)

            sub_item = QTableWidgetItem(format_price(item.discounted_total))
            sub_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self._cart_table.setItem(row, 4, sub_item)

            remove_btn = QPushButton("Remove")
            remove_btn.setProperty("class", "danger")
            remove_btn.setFixedHeight(30)
            remove_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            remove_btn.clicked.connect(lambda _, idx=i: self._remove_item(idx))
            self._cart_table.setCellWidget(row, 5, remove_btn)

    def _update_totals(self, cart: Cart) -> None:
        currency = cart.currency
        symbol = CurrencyService.get_symbol(currency)

        self._subtotal_label.setText(f"Subtotal: {format_price(cart.subtotal)}")
        self._shipping_label.setText(f"Shipping: {format_price(cart.service_charge)}")

        total = cart.total_in_currency
        self._total_label.setText(f"Total: {symbol}{total:,.2f} {currency}")

        if currency != "USD":
            rate = CurrencyService.get_rate(currency)
            self._currency_note.setText(
                f"Converted at 1 USD = {rate} {currency}"
            )
        else:
            self._currency_note.setText("")

    # ── Event handlers ──

    def _on_delivery_changed(self, button_id: int, checked: bool) -> None:
        if checked:
            method = "delivery" if button_id == 0 else "pickup"
            self._store.cart.delivery_method = method
            self._update_totals(self._store.cart)

    def _on_currency_changed(self, index: int) -> None:
        code = self._currency_combo.currentData()
        if code:
            self._store.cart.currency = code
            self._update_totals(self._store.cart)

    def _remove_item(self, index: int) -> None:
        self._store.remove_from_cart(index)
        self.refresh()

    def _clear_banner(self) -> None:
        while self._banner_area.count():
            item = self._banner_area.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def _show_banner(self, msg: str, variant: str = "info") -> None:
        self._clear_banner()
        banner = StatusBanner(msg, variant, dismissible=True)
        self._banner_area.addWidget(banner)

    def _on_place_order(self) -> None:
        if self._store.cart.is_empty:
            self._show_banner("Your cart is empty.", "warning")
            return

        order = self._store.checkout()
        self.refresh()

        symbol = CurrencyService.get_symbol(order.currency)
        self._show_banner(
            f"Order confirmed! Your order of {symbol}{order.total:,.2f} {order.currency} "
            f"is on its way. Thank you for shopping with us!",
            "success",
        )

        QTimer.singleShot(3000, self.order_completed.emit)
