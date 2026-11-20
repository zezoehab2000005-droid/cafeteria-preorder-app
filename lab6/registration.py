class Student:
    def __init__(self, student_id):
        self.student_id = student_id
        self.total_hours = 0

    def register(self, code, hours):
        self.total_hours += hours
