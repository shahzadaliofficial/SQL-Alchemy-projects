from sqlalchemy import (
    create_engine, Column, Integer, String, Date, ForeignKey, Table, Float, Boolean, func
)
from sqlalchemy.orm import relationship, declarative_base, backref

Base = declarative_base()

# Junction Table for Many-to-Many: Student <-> Activity
activity_participation = Table(
    'activity_participation', Base.metadata,
    Column('student_id', ForeignKey('students.id'), primary_key=True),
    Column('activity_id', ForeignKey('activities.id'), primary_key=True)
)

# Junction Table for Many-to-Many: Student <-> Class (Enrollments)
enrollments = Table(
    'enrollments', Base.metadata,
    Column('student_id', ForeignKey('students.id'), primary_key=True),
    Column('class_id', ForeignKey('classes.id'), primary_key=True)
)

class Department(Base):
    __tablename__ = 'departments'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    teachers = relationship("Teacher", back_populates="department")

class Teacher(Base):
    __tablename__ = 'teachers'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    department_id = Column(Integer, ForeignKey('departments.id'))
    department = relationship("Department", back_populates="teachers")
    classes = relationship("Class", back_populates="teacher")

class Parent(Base):
    __tablename__ = 'parents'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    students = relationship("Student", back_populates="parent")

class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    dob = Column(Date)
    parent_id = Column(Integer, ForeignKey('parents.id'))
    parent = relationship("Parent", back_populates="students")
    enrollments = relationship('Class', secondary=enrollments, back_populates='students')
    grades = relationship("Grade", back_populates="student")
    attendance = relationship("Attendance", back_populates="student")
    activities = relationship("Activity", secondary=activity_participation, back_populates="participants")

class Class(Base):
    __tablename__ = 'classes'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    teacher_id = Column(Integer, ForeignKey('teachers.id'))
    teacher = relationship("Teacher", back_populates="classes")
    students = relationship('Student', secondary=enrollments, back_populates='enrollments')
    subject_id = Column(Integer, ForeignKey('subjects.id'))
    subject = relationship("Subject", back_populates="classes")

class Subject(Base):
    __tablename__ = 'subjects'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    classes = relationship("Class", back_populates="subject")

class Grade(Base):
    __tablename__ = 'grades'
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'))
    class_id = Column(Integer, ForeignKey('classes.id'))
    score = Column(Float)
    student = relationship("Student", back_populates="grades")
    class_ = relationship("Class")

class Attendance(Base):
    __tablename__ = 'attendance'
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'))
    date = Column(Date)
    present = Column(Boolean)
    student = relationship("Student", back_populates="attendance")

class Activity(Base):
    __tablename__ = 'activities'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    participants = relationship("Student", secondary=activity_participation, back_populates="activities")
