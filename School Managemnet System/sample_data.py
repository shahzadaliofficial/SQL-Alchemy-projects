from datetime import date, timedelta
import random
from models import (
    Department, Teacher, Subject, Class, Parent,
    Student, Grade, Activity, Attendance
)

'''
I've created a comprehensive sample data generator that includes:

10 Departments
20 Teachers
16 Subjects
30 Classes
50 Parents
50 Students
15 Activities
Multiple grades per student per class
Attendance records for the past month
'''
def generate_sample_data(session):
    # Sample department names
    department_names = [
        "Mathematics", "Science", "English", "History", "Computer Science",
        "Physical Education", "Art", "Music", "Foreign Languages", "Social Studies"
    ]
    
    # Create departments
    departments = []
    for name in department_names:
        dept = Department(name=name)
        departments.append(dept)
        session.add(dept)
    
    # Sample teacher names
    first_names = ["John", "Jane", "Michael", "Sarah", "David", "Lisa", "Robert", "Mary", "William", "Elizabeth"]
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"]
    
    # Create 20 teachers
    teachers = []
    for _ in range(20):
        name = f"{random.choice(first_names)} {random.choice(last_names)}"
        teacher = Teacher(
            name=name,
            department=random.choice(departments)
        )
        teachers.append(teacher)
        session.add(teacher)
    
    # Sample subject names
    subject_names = [
        "Algebra", "Geometry", "Biology", "Chemistry", "Physics",
        "World History", "Literature", "Grammar", "Programming",
        "Physical Education", "Art History", "Music Theory",
        "Spanish", "French", "Economics", "Geography"
    ]
    
    # Create subjects
    subjects = []
    for name in subject_names:
        subject = Subject(name=name)
        subjects.append(subject)
        session.add(subject)
    
    # Create 30 classes
    classes = []
    for i in range(30):
        class_name = f"{random.choice(subject_names)} {random.randint(101, 401)}"
        class_ = Class(
            name=class_name,
            teacher=random.choice(teachers),
            subject=random.choice(subjects)
        )
        classes.append(class_)
        session.add(class_)
    
    # Generate 50 parents
    parents = []
    for _ in range(50):
        name = f"{random.choice(first_names)} {random.choice(last_names)}"
        parent = Parent(name=name)
        parents.append(parent)
        session.add(parent)
    
    # Generate 50 students
    students = []
    start_date = date(2005, 1, 1)
    for _ in range(50):
        # Generate random birth date between 2005 and 2010
        days_to_add = random.randint(0, 365 * 5)  # 5 years range
        birth_date = start_date + timedelta(days=days_to_add)
        
        name = f"{random.choice(first_names)} {random.choice(last_names)}"
        # Assign 2-4 random classes to each student
        assigned_classes = random.sample(classes, random.randint(2, 4))
        
        student = Student(
            name=name,
            dob=birth_date,
            parent=random.choice(parents),
            enrollments=assigned_classes
        )
        students.append(student)
        session.add(student)
    
    # Create activities
    activity_names = [
        "Chess Club", "Drama Club", "Science Club", "Math Team",
        "Basketball Team", "Soccer Team", "Debate Club", "Art Club",
        "Music Band", "Student Council", "Environmental Club",
        "Robotics Club", "Photography Club", "Book Club", "Coding Club"
    ]
    
    activities = []
    for name in activity_names:
        activity = Activity(name=name)
        activities.append(activity)
        session.add(activity)
    
    # Assign 1-3 activities to each student
    for student in students:
        assigned_activities = random.sample(activities, random.randint(1, 3))
        student.activities.extend(assigned_activities)
    
    # Generate grades for each student in their classes
    for student in students:
        for class_ in student.enrollments:
            # Generate 3 grades per class per student
            for _ in range(3):
                grade = Grade(
                    student=student,
                    class_=class_,
                    score=random.uniform(60.0, 100.0)
                )
                session.add(grade)
    
    # Generate attendance records for the past month
    today = date(2025, 6, 2)  # Current date
    for i in range(30):  # Past 30 days
        current_date = today - timedelta(days=i)
        # Skip weekends
        if current_date.weekday() >= 5:  # 5 is Saturday, 6 is Sunday
            continue
        for student in students:
            # 90% chance of being present
            is_present = random.random() < 0.9
            attendance = Attendance(
                student=student,
                date=current_date,
                present=is_present
            )
            session.add(attendance)
    
    # Commit all changes
    session.commit()
