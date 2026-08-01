"""User preferences management — persisted to a local JSON file."""

import json
import os
from typing import Any

from electronics_store.config.constants import PREFERENCES_FILE, DEFAULT_CURRENCY


_DEFAULTS: dict[str, Any] = {
    "currency": DEFAULT_CURRENCY,
    "delivery_method": "delivery",
    "theme": "light",
    "remember_username": False,
    "saved_username": "",
}


class Settings:
    def __init__(self) -> None:
        self._path = os.path.join(
            os.path.expanduser("~"), ".electronics_store", PREFERENCES_FILE
        )
        self._data: dict[str, Any] = dict(_DEFAULTS)
        self._load()

    def _load(self) -> None:
        try:
            if os.path.exists(self._path):
                with open(self._path, "r") as fh:
                    stored = json.load(fh)
                for k, v in stored.items():
                    if k in _DEFAULTS:
                        self._data[k] = v
        except (json.JSONDecodeError, OSError):
            pass

    def save(self) -> None:
        os.makedirs(os.path.dirname(self._path), exist_ok=True)
        with open(self._path, "w") as fh:
            json.dump(self._data, fh, indent=2)

    def get(self, key: str) -> Any:
        return self._data.get(key, _DEFAULTS.get(key))

    def set(self, key: str, value: Any) -> None:
        self._data[key] = value

    def reset(self) -> None:
        self._data = dict(_DEFAULTS)
        self.save()
