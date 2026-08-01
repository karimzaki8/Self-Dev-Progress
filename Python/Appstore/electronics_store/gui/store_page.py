"""Store page — product catalog browsing and add-to-cart functionality.

Implements PDF steps 1–6 of the Store Interactive Interface:
  1. Display catalog table (name, price, stock)
  2. Customer selects a product by name
  3. Customer specifies quantity
  4. System calculates discount (5% per 5 units, max 25%)
  5. Display discounted price
  6. Option to add more products or proceed to checkout
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QSpinBox, QSpacerItem, QSizePolicy,
    QHeaderView, QAbstractItemView,
)
from PyQt6.QtCore import Qt, pyqtSignal

from electronics_store.services.store_service import StoreService
from electronics_store.models.cart import Cart
from electronics_store.utils.helpers import format_price
from electronics_store.gui.widgets.custom_widgets import Card, StatusBanner, SectionHeader
from electronics_store.assets.styles.theme import COLORS


class StorePage(QWidget):
    go_to_cart = pyqtSignal()

    def __init__(self, store_service: StoreService, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._store = store_service
        self._selected_product_name: str = ""
        self._build_ui()
        self.refresh_catalog()

    def _build_ui(self) -> None:
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(20)

        # ── Left: catalog ──
        left = QVBoxLayout()
        left.setSpacing(12)

        left.addWidget(SectionHeader("Product Catalog", "Browse our electronics collection"))

        # Search bar
        search_row = QHBoxLayout()
        self._search_input = QLineEdit()
        self._search_input.setPlaceholderText("Search products…")
        self._search_input.textChanged.connect(self._filter_catalog)
        search_row.addWidget(self._search_input, 1)
        left.addLayout(search_row)

        # Product table
        self._table = QTableWidget()
        self._table.setColumnCount(3)
        self._table.setHorizontalHeaderLabels(["Product Name", "Price (USD)", "In Stock"])
        self._table.setAlternatingRowColors(True)
        self._table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self._table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self._table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self._table.verticalHeader().setVisible(False)
        self._table.horizontalHeader().setStretchLastSection(True)
        self._table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self._table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self._table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self._table.itemSelectionChanged.connect(self._on_table_select)
        left.addWidget(self._table, 1)

        main_layout.addLayout(left, 3)

        # ── Right: selection panel ──
        right_card = Card(shadow=True)
        right_card.setFixedWidth(340)
        right = QVBoxLayout(right_card)
        right.setSpacing(14)
        right.setContentsMargins(24, 24, 24, 24)

        right.addWidget(SectionHeader("Add to Cart"))

        # Banner area
        self._banner_area = QVBoxLayout()
        right.addLayout(self._banner_area)

        # Product name input
        right.addWidget(QLabel("Product Name"))
        self._product_input = QLineEdit()
        self._product_input.setPlaceholderText("Select from table or type name")
        right.addWidget(self._product_input)

        # Quantity
        right.addWidget(QLabel("Quantity"))
        self._qty_spin = QSpinBox()
        self._qty_spin.setMinimum(1)
        self._qty_spin.setMaximum(9999)
        self._qty_spin.setValue(1)
        self._qty_spin.valueChanged.connect(self._update_preview)
        right.addWidget(self._qty_spin)

        # Preview card
        preview_frame = Card(shadow=False)
        preview_frame.setStyleSheet(
            f"background-color: {COLORS['input_bg']}; border-radius: 8px; padding: 12px;"
        )
        preview_layout = QVBoxLayout(preview_frame)
        preview_layout.setSpacing(6)

        self._preview_name = QLabel("—")
        self._preview_name.setStyleSheet("font-weight: 600; font-size: 15px;")
        preview_layout.addWidget(self._preview_name)

        self._preview_price = QLabel("Unit price: —")
        self._preview_price.setStyleSheet(f"color: {COLORS['text_secondary']};")
        preview_layout.addWidget(self._preview_price)

        self._preview_discount = QLabel("Discount: 0%")
        self._preview_discount.setStyleSheet(
            f"color: {COLORS['discount_text']}; background-color: {COLORS['discount_badge']}; "
            "border-radius: 4px; padding: 2px 8px; font-weight: 600;"
        )
        preview_layout.addWidget(self._preview_discount)

        self._preview_total = QLabel("Total: —")
        self._preview_total.setStyleSheet(
            f"font-weight: 700; font-size: 18px; color: {COLORS['primary']};"
        )
        preview_layout.addWidget(self._preview_total)

        right.addWidget(preview_frame)

        # Add to cart button
        self._add_btn = QPushButton("Add to Cart")
        self._add_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._add_btn.clicked.connect(self._on_add_to_cart)
        right.addWidget(self._add_btn)

        right.addItem(QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        # Cart summary & checkout button
        self._cart_summary = QLabel("Cart: 0 items")
        self._cart_summary.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 13px;")
        right.addWidget(self._cart_summary)

        self._checkout_btn = QPushButton("Proceed to Checkout →")
        self._checkout_btn.setProperty("class", "success")
        self._checkout_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._checkout_btn.clicked.connect(self.go_to_cart.emit)
        right.addWidget(self._checkout_btn)

        main_layout.addWidget(right_card)

    def refresh_catalog(self) -> None:
        self._table.setRowCount(0)
        for product in self._store.products:
            row = self._table.rowCount()
            self._table.insertRow(row)

            name_item = QTableWidgetItem(product.name)
            price_item = QTableWidgetItem(format_price(product.price))
            price_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            stock_item = QTableWidgetItem(str(product.stock))
            stock_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            if product.stock == 0:
                for item in (name_item, price_item, stock_item):
                    item.setForeground(Qt.GlobalColor.gray)

            self._table.setItem(row, 0, name_item)
            self._table.setItem(row, 1, price_item)
            self._table.setItem(row, 2, stock_item)

        self._update_cart_summary()

    def _filter_catalog(self, text: str) -> None:
        text_lower = text.lower()
        for row in range(self._table.rowCount()):
            name_item = self._table.item(row, 0)
            match = text_lower in name_item.text().lower() if name_item else True
            self._table.setRowHidden(row, not match)

    def _on_table_select(self) -> None:
        selected = self._table.selectedItems()
        if selected:
            row = selected[0].row()
            name = self._table.item(row, 0).text()
            self._product_input.setText(name)
            self._update_preview()

    def _update_preview(self) -> None:
        name = self._product_input.text().strip()
        product = self._store.find_product(name)
        qty = self._qty_spin.value()

        if product:
            discount_rate = Cart.calculate_discount_rate(qty)
            subtotal = product.price * qty
            discounted = subtotal * (1 - discount_rate)

            self._preview_name.setText(product.name)
            self._preview_price.setText(f"Unit price: {format_price(product.price)}")
            self._preview_discount.setText(f"Discount: {int(discount_rate * 100)}%")
            self._preview_total.setText(f"Total: {format_price(discounted)}")
        else:
            self._preview_name.setText("—")
            self._preview_price.setText("Unit price: —")
            self._preview_discount.setText("Discount: 0%")
            self._preview_total.setText("Total: —")

    def _clear_banner(self) -> None:
        while self._banner_area.count():
            item = self._banner_area.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def _show_banner(self, msg: str, variant: str = "error") -> None:
        self._clear_banner()
        banner = StatusBanner(msg, variant, dismissible=True)
        self._banner_area.addWidget(banner)

    def _on_add_to_cart(self) -> None:
        name = self._product_input.text().strip()
        qty = self._qty_spin.value()

        if not name:
            self._show_banner("Please enter a product name.", "warning")
            return

        ok, msg, item = self._store.add_to_cart(name, qty)
        if ok:
            self._show_banner(msg, "success")
            self._product_input.clear()
            self._qty_spin.setValue(1)
            self._update_preview()
            self.refresh_catalog()
        else:
            self._show_banner(msg, "error")

    def _update_cart_summary(self) -> None:
        cart = self._store.cart
        n = len(cart.items)
        total_qty = sum(i.quantity for i in cart.items)
        self._cart_summary.setText(
            f"Cart: {n} item{'s' if n != 1 else ''} ({total_qty} unit{'s' if total_qty != 1 else ''})"
        )
