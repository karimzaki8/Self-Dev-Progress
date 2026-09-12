"""
main.py
-------
Entry point that wires the preprocessing functions together into a
small interactive pipeline:

    1. Read the dataset (path comes from config/config.py).
    2. Let the user choose what to do next:
         a) Remove the unnecessary features listed in config.py
         b) Check the datatypes / data-quality report
         c) Do both
         d) Quit
"""

from config import config
from preprocessing import Read_data_file, Drop_unnecessary_features, Check_data_type


def print_menu():
    print("\nWhat would you like to do?")
    print("  1) Remove unnecessary features (columns from config.py)")
    print("  2) Check data types (data-quality report)")
    print("  3) Do both")
    print("  4) Quit")


def main():
    print(f"Reading dataset from: {config.DATA_FILE_PATH}")
    df = Read_data_file(config.DATA_FILE_PATH)

    if df is None:
        print("Pipeline stopped: could not load the dataset.")
        return

    while True:
        print_menu()
        choice = input("Enter your choice (1-4): ").strip()

        if choice == "1":
            df = Drop_unnecessary_features(df, config.COLUMNS_TO_DROP)

        elif choice == "2":
            Check_data_type(df)

        elif choice == "3":
            df = Drop_unnecessary_features(df, config.COLUMNS_TO_DROP)
            Check_data_type(df)

        elif choice == "4":
            print("Exiting pipeline. Goodbye!")
            break

        else:
            print("Invalid choice, please enter a number between 1 and 4.")


if __name__ == "__main__":
    main()
