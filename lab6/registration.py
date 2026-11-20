class RegistrationError(Exception):
    pass


class Student:
    def __init__(self, student_id):
        self.student_id = student_id
        self.courses = {}

    @property
    def total_hours(self):
        return sum(self.courses.values())

    def register(self, code, hours):
        if self.total_hours + hours > 18:
            raise RegistrationError("credit-hour limit is 18")
        self.courses[code] = hours
