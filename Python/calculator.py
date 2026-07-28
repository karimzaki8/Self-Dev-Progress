def get_number(prompt):
    """Keep asking until the user enters a valid number."""
    while True:
        value = input(prompt)
        try:
            return float(value)
        except ValueError:
            print("Invalid input. Please enter a valid number.")


def get_yes_no(prompt):
    """Keep asking until the user answers yes or no."""
    while True:
        answer = input(prompt).strip().lower()
        if answer in ("yes", "y"):
            return True
        elif answer in ("no", "n"):
            return False
        else:
            print("Please answer 'yes' or 'no'.")


def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    return a / b


def main():
    print("=" * 40)
    print("Welcome to the Basic Calculator")
    print("=" * 40)

    while True:
        print("\nPlease choose an operation:")
        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        print("4. Division")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == "5":
            print("\nThank you for using the Basic Calculator. Goodbye!")
            break

        if choice not in ("1", "2", "3", "4"):
            print("Invalid choice. Please select a number between 1 and 5.")
            continue

        num1 = get_number("Enter the first number: ")
        num2 = get_number("Enter the second number: ")

        if choice == "1":
            result = add(num1, num2)
            print(f"\nThe result of adding {num1} and {num2} is {result}.")

        elif choice == "2":
            result = subtract(num1, num2)
            print(f"\nThe result of subtracting {num2} from {num1} is {result}.")

        elif choice == "3":
            result = multiply(num1, num2)
            print(f"\nThe result of multiplying {num1} and {num2} is {result}.")

        elif choice == "4":
            while num2 == 0:
                print("Error: Division by zero is not allowed.")
                num2 = get_number("Enter a non-zero second number: ")
            result = divide(num1, num2)
            print(f"\nThe result of dividing {num1} by {num2} is {result}.")

        if not get_yes_no("\nWould you like to perform another calculation? (yes/no): "):
            print("\nThank you for using the Basic Calculator. Goodbye!")
            break


if __name__ == "__main__":
    main()
