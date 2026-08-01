# Electronics Store — Desktop Application

A modern, standalone desktop application for an electronics store built with **Python** and **PyQt6**. It implements a complete shopping experience with multi-step authentication, product browsing, discount-based pricing, multi-currency checkout, and order confirmation.

---

## Features

### User Login (Multi-Step Authentication)
1. Username entry and verification
2. Password entry and verification
3. System-generated random verification code displayed to the user
4. User inputs the verification code for final verification
5. "Welcome" message upon successful login

### Product Catalog
- Displays all electronics products in a table with **name**, **price**, and **stock**
- Real-time search/filter by product name
- Click-to-select products from the table

### Shopping Cart
- Add products by name with a chosen quantity
- Automatic **quantity-based discount**: 5% for every 5 units purchased (max 25%)
- Live price preview before adding to cart
- Remove individual items from the cart

### Checkout & Order
- **Delivery** ($200) or **Pick-up** ($50) shipping options
- **Multi-currency support**: USD, EUR, EGP with exchange-rate conversion
- Invalid currency selection defaults to USD
- Full price breakdown (subtotal, discounts, shipping, total)
- Order confirmation with stock reduction

### Settings
- Default currency preference
- Default shipping method
- Remember-username option
- Preferences persisted locally as JSON

### Error Handling
- Product-not-found validation
- Quantity-exceeds-stock validation
- Input validation on every form
- User-friendly banners for success, error, warning, and info messages

---

## Project Structure

```
electronics_store/
├── main.py                          # Application entry point
├── requirements.txt                 # Python dependencies
├── README.md                        # This file
├── config/
│   ├── constants.py                 # App-wide constants (prices, rates, dimensions)
│   └── settings.py                  # User preferences (load/save JSON)
├── models/
│   ├── product.py                   # Product data model
│   ├── user.py                      # User data model
│   ├── cart.py                      # Shopping cart with discount logic
│   └── order.py                     # Completed order record
├── services/
│   ├── auth_service.py              # Multi-step login flow
│   ├── store_service.py             # Catalog, cart, and checkout operations
│   └── currency_service.py          # Currency conversion utilities
├── gui/
│   ├── app.py                       # Main window with sidebar navigation
│   ├── login_page.py                # Login UI (4-step wizard)
│   ├── store_page.py                # Product catalog & add-to-cart
│   ├── checkout_page.py             # Cart review, shipping, currency, confirm
│   ├── settings_page.py             # User preferences UI
│   └── widgets/
│       └── custom_widgets.py        # Reusable widgets (Card, Banner, StepIndicator)
├── utils/
│   ├── validators.py                # Input validation helpers
│   └── helpers.py                   # Utility functions (code gen, price formatting)
├── data/
│   └── store_data.py                # Initial product catalog & user accounts
└── assets/
    └── styles/
        └── theme.py                 # Qt stylesheet & color palette
```

---

## Prerequisites

- **Python 3.10+** (tested with 3.12)
- **pip** (Python package manager)
- Operating system: Windows, macOS, or Linux

---

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd <repository-root>
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv

# Activate:
# Windows:
venv\Scripts\activate
# macOS / Linux:
source venv/bin/activate
```

### 3. Install the package

The recommended approach — installs the package so all imports resolve correctly:

```bash
pip install -e .
```

Alternatively, install just the requirements:

```bash
pip install -r electronics_store/requirements.txt
```

On Linux you may also need system Qt runtime libraries:

```bash
sudo apt-get install -y libegl1 libxkbcommon0 libxcb-cursor0 libgl1
```

---

## How to Run

**Option A — after `pip install -e .` (recommended):**

```bash
electronics-store
```

or from anywhere:

```bash
python -m electronics_store.main
```

**Option B — without installing (run from the repository root):**

```bash
python run.py
```

**Option C — run directly from inside the package folder:**

```bash
cd electronics_store
python main.py
```

All three options work on Windows, macOS, and Linux.

### Default Credentials

| Username | Password   | Display Name   |
|----------|------------|----------------|
| admin    | admin123   | Administrator  |
| user     | user123    | Customer       |
| guest    | guest123   | Guest User     |

---

## Usage Guide

### Logging In
1. Enter your **username** and click *Continue*.
2. Enter your **password** and click *Continue*.
3. The system displays a 6-digit **verification code**. Type it exactly and click *Verify*.
4. You will see a *Welcome* message and be redirected to the store.

### Browsing & Adding Products
1. The **Product Catalog** table shows all available electronics.
2. Click a row or type a product name in the *Add to Cart* panel.
3. Set the **quantity** — the discount preview updates live:
   - 5–9 units → 5% off
   - 10–14 units → 10% off
   - 15–19 units → 15% off
   - 20–24 units → 20% off
   - 25+ units → 25% off (maximum)
4. Click **Add to Cart**.
5. Repeat for more products, or click **Proceed to Checkout**.

### Checkout
1. Review your cart items. Remove any if needed.
2. Choose **Delivery** ($200) or **Pick-up** ($50).
3. Select your **payment currency** (USD / EUR / EGP).
4. Verify the **total** and click **Place Order**.
5. The system confirms the order is on its way.

### Settings
Access via the sidebar ⚙ **Settings** button:
- Set default currency and shipping method.
- Enable "Remember username" for faster login.
- Click **Save Settings** to persist, or **Reset to Defaults**.

---

## Packaging as an Executable (.exe)

### Using PyInstaller

1. Install PyInstaller:

```bash
pip install pyinstaller
```

2. Build the executable:

```bash
pyinstaller --onefile --windowed \
  --name "ElectronicsStore" \
  --add-data "electronics_store:electronics_store" \
  electronics_store/main.py
```

3. The executable will be in the `dist/` folder:

```
dist/ElectronicsStore          # Linux / macOS
dist/ElectronicsStore.exe      # Windows
```

### Platform-Specific Notes

- **Windows**: Use `--icon=icon.ico` to add a custom icon.
- **macOS**: Use `--icon=icon.icns` and `--osx-bundle-identifier=com.example.electronics-store`.
- **Linux**: The resulting binary is a self-contained ELF executable.

---

## Architecture

The application follows a **clean modular architecture** with clear separation of concerns:

| Layer        | Responsibility                                        |
|--------------|-------------------------------------------------------|
| **GUI**      | PyQt6 widgets, pages, and navigation                  |
| **Services** | Business logic (auth, store operations, currency)     |
| **Models**   | Data structures (Product, Cart, Order, User)          |
| **Config**   | Constants and user preferences                        |
| **Utils**    | Input validation and helper functions                 |
| **Data**     | Initial catalog and user seed data                    |

All layers communicate through well-defined interfaces. The GUI never directly manipulates data — it delegates to services which operate on models.

---

## Design Assumptions

1. **User accounts are pre-seeded** — no registration flow since the PDF describes login only.
2. **Exchange rates are static constants** — the PDF specifies USD, EUR, and EGP without mentioning live rates.
3. **Stock resets on application restart** — no persistent database; the catalog reloads from `store_data.py`.
4. **Verification code is displayed on-screen** — per the PDF, the system "displays it to the user."
5. **Prices are in USD** — all catalog prices are USD-denominated; conversion happens at checkout.

---

## License

This project is provided as-is for educational and demonstration purposes.
