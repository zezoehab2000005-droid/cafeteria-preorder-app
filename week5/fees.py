from enum import Enum

PRICE_PER_CREDIT_HOUR = 350
LARGE_FEE_THRESHOLD = 6000
LARGE_FEE_REDUCTION = 200
SUMMER_SUPPLEMENT = 150


class StudentType(Enum):
    REGULAR = 1
    STAFF_CHILD = 2
    SCHOLARSHIP = 3


PRICE_SHARE = {
    StudentType.REGULAR: 1.0,
    StudentType.STAFF_CHILD: 0.5,
    StudentType.SCHOLARSHIP: 0.0,
}


def tuition_fee(courses, kind, summer=False, discount=0, extras=[]):
    total = (
        sum(course["h"] for course in courses)
        * PRICE_PER_CREDIT_HOUR
        * PRICE_SHARE[kind]
    )
    if total > LARGE_FEE_THRESHOLD:
        total -= LARGE_FEE_REDUCTION
    if summer:
        total += SUMMER_SUPPLEMENT
    return total - discount + sum(extras)


def fee_report(courses, kind, summer=False, discount=0):
    fee = tuition_fee(courses, kind, summer, discount)
    if kind == StudentType.REGULAR:
        print("Student fee: " + str(fee))
    elif kind == StudentType.STAFF_CHILD:
        print("Staff child fee: " + str(fee))
    if fee > LARGE_FEE_THRESHOLD:
        print("High fee")
    return fee


def process_all(students):
    for student in students:
        if student["type"] == StudentType.REGULAR:
            fee = tuition_fee(student["courses"], StudentType.REGULAR, student["summer"])
        if student["type"] == StudentType.STAFF_CHILD:
            fee = tuition_fee(student["courses"], StudentType.STAFF_CHILD, student["summer"])
        print(student["name"], fee)
