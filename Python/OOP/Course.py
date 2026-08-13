class Course:
    _id_counter = 1
    def __init__(self, name,):
        self.course_id = Course._id_counter
        Course._id_counter += 1
        self.name = name
        self.enrolled_students = []

    def __str__(self):
        return f"Course ID: {self.course_id}, Name: {self.name}, Enrolled Students: {self.enrolled_students}"
    def __repr__(self):
        return f"Course({self.course_id}, {self.name}, {self.enrolled_students})"
    def enroll_student(self, student_name: str|None="test")-> None:
        '''
        This Function enrolls a student in the course by adding their name to the enrolled_students list.
        Args:
            student_name (str): The name of the student to enroll. Defaults to "test".
            returns:
                None
            Example:
                course = Course("Math 101")
                course.enroll_student("Karim Zaki")
                print(course.enrolled_students)  # Output: ['Karim Zaki']
        '''
        if student_name is not None:
            self.enrolled_students.append(student_name)
            print(f"Student '{student_name}' has been enrolled in the course '{self.name}'.")

        else:
            print("No student name provided. Enrollment failed.")

    def remove_student(self, student_name: str|None="test")-> None:
        '''
        This Function removes a student from the course by removing their name from the enrolled_students list.
        Args:
            student_name (str): The name of the student to remove. Defaults to "test".
            returns:
                None
        '''
        if student_name in self.enrolled_students:
            self.enrolled_students.remove(student_name)
            print(f"Student '{student_name}' has been removed from the course '{self.name}'.")
        else:
            print(f"Student '{student_name}' is not enrolled in the course '{self.name}'. Removal failed.")