from src.core.System_Manager import SystemManager


def show_menu():
    print("\n" + "=" * 50)
    print("1. Add student")
    print("2. Remove student")
    print("3. Add course")
    print("4. Remove course")
    print("5. Search courses")
    print("6. Record grade")
    print("7. Get all students")
    print("8. Get all courses")
    print("9. Enroll course")
    print("10. Exit")
    print("=" * 50)


def add_student_1(manager):
    name = input("Enter student name: ").strip()

    student_id = manager.add_student(name)

    if student_id is not None:
        print("Student ID:", student_id)


def remove_student(manager):
    try:
        student_id = int(input("Enter student ID: "))
        manager.remove_student(student_id)

    except ValueError:
        print("Invalid input. Student ID must be an integer.")


def add_course(manager):
    name = input("Enter course name: ").strip()

    course_id = manager.add_course(name)

    if course_id is not None:
        print("Course ID:", course_id)


def remove_course(manager):
    try:
        course_id = int(input("Enter course ID: "))
        manager.remove_course(course_id)

    except ValueError:
        print("Invalid input. Course ID must be an integer.")


def search_courses(manager):
    search_name = input("Enter course name to search: ").strip()

    courses = manager.search_courses(search_name)

    if courses:
        print("Matching courses:")

        for course in courses:
            print(course)
    else:
        print("No courses found with that name.")


def record_grade(manager):
    try:
        student_id = int(input("Enter student ID: "))
        course_id = int(input("Enter course ID: "))
        grade = float(input("Enter grade (0-100): "))

        manager.record_grade(student_id, course_id, grade)

    except ValueError:
        print("Invalid input. IDs must be integers and grade must be a number.")


def get_all_students(manager):
    students = manager.get_all_students()

    if students:
        print("All students:")

        for student in students:
            print(student)
    else:
        print("No students found.")


def get_all_courses(manager):
    courses = manager.get_all_courses()

    if courses:
        print("All courses:")

        for course in courses:
            print(course)
    else:
        print("No courses found.")


def enroll_course(manager):
    try:
        student_id = int(input("Enter student ID: "))
        course_id = int(input("Enter course ID: "))

        manager.enroll_course(student_id, course_id)

    except ValueError:
        print("Invalid input. IDs must be integers.")


def core():
    manager = SystemManager()

    while True:
        show_menu()

        choice = input("Enter choice: ").strip()

        if choice == "1":
            add_student_1(manager)

        elif choice == "2":
            remove_student(manager)

        elif choice == "3":
            add_course(manager)

        elif choice == "4":
            remove_course(manager)

        elif choice == "5":
            search_courses(manager)

        elif choice == "6":
            record_grade(manager)

        elif choice == "7":
            get_all_students(manager)

        elif choice == "8":
            get_all_courses(manager)

        elif choice == "9":
            enroll_course(manager)

        elif choice == "10":
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 10.")


if __name__ == "__main__":
    core()