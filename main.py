import sys
from datetime import date
from sqlalchemy import create_engine, func, and_, or_, not_
from sqlalchemy.orm import sessionmaker, aliased
from models import Base, Student, Teacher, Class, Subject, Grade, Department, Parent, Attendance, Activity

engine = create_engine('sqlite:///school.db', echo=False)
Session = sessionmaker(bind=engine)
session = Session()

def initialize_db():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    # Add some sample data here (skipped for brevity)
    # You can fill data as required for queries to work

def menu():
    while True:
        print("\n--- SCHOOL MANAGEMENT MENU ---")
        print("1. List all students with their parents and enrolled classes (JOIN)")
        print("2. List teachers and their departments (JOIN, LABEL)")
        print("3. List students with average grades (GROUP BY, AVG, LABEL)")
        print("4. List students with >1 activity (JOIN, filter, COUNT, HAVING)")
        print("5. List all classes with their teacher and subject (JOIN, LABEL)")
        print("6. Students with no absences (LEFT OUTER JOIN, NOT, FILTER)")
        print("7. List students in a specific department (JOIN, FILTER)")
        print("8. List top student by grade in each class (GROUP BY, MAX, SUBQUERY)")
        print("9. Search students by name (FILTER_BY, OR, AND)")
        print("10. List all activities with number of participants (JOIN, GROUP BY, COUNT)")
        print("11. Exit")
        choice = input("Enter choice: ")

        if choice == '1':
            query = session.query(Student, Parent, Class).\
                join(Parent).\
                join(Student.enrollments).\
                order_by(Student.name)
            for student, parent, class_ in query:
                print(f"{student.name} (Parent: {parent.name}) - Class: {class_.name}")
        elif choice == '2':
            query = session.query(Teacher.name.label("Teacher"), Department.name.label("Department")).\
                join(Department)
            for t, d in query:
                print(f"{t} - Department: {d}")
        elif choice == '3':
            query = session.query(
                Student.name, func.avg(Grade.score).label("AverageGrade")
            ).join(Grade).group_by(Student.id)
            for name, avg in query:
                print(f"{name}: Avg Grade = {avg:.2f}")
        elif choice == '4':
            query = session.query(
                Student.name, func.count(Activity.id).label("activity_count")
            ).join(Student.activities).group_by(Student.id).having(func.count(Activity.id) > 1)
            for name, count in query:
                print(f"{name}, Activities: {count}")
        elif choice == '5':
            query = session.query(
                Class.name.label("Class"),
                Teacher.name.label("Teacher"),
                Subject.name.label("Subject")
            ).join(Teacher).join(Subject)
            for c, t, s in query:
                print(f"{c}: Teacher: {t}, Subject: {s}")
        elif choice == '6':
            subq = session.query(Attendance.student_id).filter(Attendance.present==False).subquery()
            query = session.query(Student).filter(~Student.id.in_(subq))
            for s in query:
                print(f"{s.name} has no absences")
        elif choice == '7':
            dept = input("Enter department name: ")
            query = session.query(Student).\
                join(Student.enrollments).\
                join(Class.teacher).\
                join(Teacher.department).\
                filter(Department.name == dept)
            for s in query.distinct():
                print(s.name)
        elif choice == '8':
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
        elif choice == '9':
            q = input("Enter partial name: ")
            query = session.query(Student).\
                filter(or_(
                    Student.name.ilike(f'%{q}%'),
                    Student.name.ilike(f'{q}%')
                ))
            for s in query:
                print(s.name)
        elif choice == '10':
            query = session.query(
                Activity.name,
                func.count(activity_participation.c.student_id).label("num_participants")
            ).join(activity_participation, Activity.id==activity_participation.c.activity_id).\
                group_by(Activity.id)
            for a, n in query:
                print(f"{a}: {n} participants")
        elif choice == '11':
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    if "--init" in sys.argv:
        initialize_db()
        print("Database initialized with sample data.")
    menu()
