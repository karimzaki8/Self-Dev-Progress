"""
config/config.py
-----------------
Central place for all dataset-specific settings.

The whole point of keeping these values here (instead of hard-coding them
inside preprocessing.py) is that the SAME preprocessing functions can be
reused on a completely different dataset tomorrow. You would only need to
edit this file - never the functions themselves.
"""

# Path to the raw data file used by main.py
DATA_FILE_PATH = "data/raw/titanic.csv"

COLUMNS_TO_DROP = [
    "PassengerId",
    "Name",
    "Ticket",
]
