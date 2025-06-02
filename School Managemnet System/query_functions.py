from sqlalchemy import func, and_, or_, not_
from models import Student, Teacher, Class, Subject, Grade, Department, Parent, Attendance, Activity, activity_participation

class SchoolQueries:
    def __init__(self, session):
        self.session = session

    def list_students_with_parents_and_classes(session):
        query = session.query(Student, Parent, Class).\
            join(Parent).\
            join(Student.enrollments).\
            order_by(Student.name)
        for student, parent, class_ in query:
            print(f"{student.name} (Parent: {parent.name}) - Class: {class_.name}")

    def list_teachers_and_departments(session):
        query = session.query(Teacher.name.label("Teacher"), Department.name.label("Department")).\
            join(Department)
        for t, d in query:
            print(f"{t} - Department: {d}")

    def list_student_average_grades(session):
        query = session.query(
            Student.name, func.avg(Grade.score).label("AverageGrade")
        ).join(Grade).group_by(Student.id)
        for name, avg in query:
            print(f"{name}: Avg Grade = {avg:.2f}")

    def list_students_multiple_activities(session):
        query = session.query(
            Student.name, func.count(Activity.id).label("activity_count")
        ).join(Student.activities).group_by(Student.id).having(func.count(Activity.id) > 1)
        for name, count in query:
            print(f"{name}, Activities: {count}")

    def list_classes_with_teachers_subjects(session):
        query = session.query(
            Class.name.label("Class"),
            Teacher.name.label("Teacher"),
            Subject.name.label("Subject")
        ).join(Teacher).join(Subject)
        for c, t, s in query:
            print(f"{c}: Teacher: {t}, Subject: {s}")

    def list_students_no_absences(session):
        subq = session.query(Attendance.student_id).filter(Attendance.present==False).subquery()
        query = session.query(Student).filter(~Student.id.in_(subq))
        for s in query:
            print(f"{s.name} has no absences")

    def list_students_by_department(session):
        dept = input("Enter department name: ")
        query = session.query(Student).\
            join(Student.enrollments).\
            join(Class.teacher).\
            join(Teacher.department).\
            filter(Department.name == dept)
        for s in query.distinct():
            print(s.name)

    def list_top_students_by_class(session):
        subq = session.query(
            Grade.class_id,
            func.max(Grade.score).label("max_score")
        ).group_by(Grade.class_id).subquery()
        query = session.query(
            Class.name,
            Student.name,
            Grade.score
        ).join(Grade, Class.id==Grade.class_id).\
            join(Student, Grade.student_id==Student.id).\
            join(subq, and_(
                Grade.class_id==subq.c.class_id,
                Grade.score==subq.c.max_score
            ))
        for c, s, g in query:
            print(f"Top for {c}: {s} ({g})")

    def search_students_by_name(session):
        q = input("Enter partial name: ")
        query = session.query(Student).\
            filter(or_(
                Student.name.ilike(f'%{q}%'),
                Student.name.ilike(f'{q}%')
            ))
        for s in query:
            print(s.name)

    def list_activities_with_participants(session):
        query = session.query(
            Activity.name,
            func.count(activity_participation.c.student_id).label("num_participants")
        ).join(activity_participation, Activity.id==activity_participation.c.activity_id).\
            group_by(Activity.id)
        for a, n in query:
            print(f"{a}: {n} participants")
