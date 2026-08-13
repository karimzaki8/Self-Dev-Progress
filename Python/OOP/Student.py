class Student:

    _id_counter = 1  
    def __init__(self, name):
        self.student_id = Student._id_counter
        Student._id_counter += 1
        self.name = name

        self.grades = {}
        self.enrolled_courses = []

    def __str__ (self):
        return f"Student ID: {self.student_id}, Name: {self.name} Grades: {self.grades}, Enrolled Courses: {self.enrolled_courses}"

    def add_grade(self, course_id, grade):
        self.grades[course_id] = grade

    def enrolled_in_course(self, course_id):
            self.enrolled_courses.append(course_id)