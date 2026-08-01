"""Entry point for the Electronics Store desktop application."""

import os
import sys

# When running as `python main.py` from inside the package directory,
# the parent folder must be on sys.path so that `electronics_store` resolves.
_pkg_dir = os.path.dirname(os.path.abspath(__file__))
_root_dir = os.path.dirname(_pkg_dir)
if _root_dir not in sys.path:
    sys.path.insert(0, _root_dir)

from PyQt6.QtWidgets import QApplication

from electronics_store.gui.app import MainWindow
from electronics_store.assets.styles.theme import get_stylesheet


def main() -> None:
    app = QApplication(sys.argv)
    app.setApplicationName("Electronics Store")
    app.setStyle("Fusion")
    app.setStyleSheet(get_stylesheet())

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
