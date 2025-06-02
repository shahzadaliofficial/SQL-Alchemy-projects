from query_functions import SchoolQueries

def menu(session):
    queries = SchoolQueries(session)
    menu_options = {
        '1': queries.list_students_with_parents_and_classes,
        '2': queries.list_teachers_and_departments,
        '3': queries.list_student_average_grades,
        '4': queries.list_students_multiple_activities,
        '5': queries.list_classes_with_teachers_subjects,
        '6': queries.list_students_no_absences,
        '7': queries.list_students_by_department,
        '8': queries.list_top_students_by_class,
        '9': queries.search_students_by_name,
        '10':queries.list_activities_with_participants
    }

    while True:
        menuMessage='''--- SCHOOL MANAGEMENT MENU ---
1. List all students with their parents and enrolled classes (JOIN)
2. List teachers and their departments (JOIN, LABEL)
3. List students with average grades (GROUP BY, AVG, LABEL)
4. List students with >1 activity (JOIN, filter, COUNT, HAVING)
5. List all classes with their teacher and subject (JOIN, LABEL)
6. Students with no absences (LEFT OUTER JOIN, NOT, FILTER)
7. List students in a specific department (JOIN, FILTER)
8. List top student by grade in each class (GROUP BY, MAX, SUBQUERY)
9. Search students by name (FILTER_BY, OR, AND)
10. List all activities with number of participants (JOIN, GROUP BY, COUNT)
11. Exit
        
Enter choice: '''
        choice = input(menuMessage)

        if choice == '11':
            print("Goodbye!")
            break
        elif choice in menu_options:
            try:
                menu_options[choice]()
            except Exception as e:
                print(f"Error: {e}")
        else:
            print("Invalid choice.")

