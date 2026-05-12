"""
src/api_actions/course_management.py

Business logic layer for course-related operations in ScholarConnect.
Orchestrates assignment, enrollment, and query operations, validating
business rules before delegating to CRUD actions.
"""

from src.api_actions.course_actions import getCourse, updateCourse
from src.api_actions.enrollment_actions import addEnrollment, getEnrollment, deleteEnrollment
from src.api_actions.professor_actions import getProfessor
from src.api_actions.student_actions import getStudent
from src.database import getConnection


def assignProfessorToCourse(c_code, am_instructor):
    """
    Assigns a professor to a course after validating both entities exist.

    Args:
        c_code (str): The unique course identifier.
        am_instructor (str): The unique instructor identifier.

    Returns:
        dict: {"success": True} on success,
              {"success": False, "error": str} on failure.
    """
    course = getCourse(c_code)
    if not course:
        return {"success": False, "error": f"Course '{c_code}' not found."}

    professor = getProfessor(am_instructor)
    if not professor:
        return {"success": False, "error": f"Professor '{am_instructor}' not found."}

    result = updateCourse(c_code, AM_Instructor=am_instructor)
    if not result:
        return {"success": False, "error": "Failed to assign professor to course."}

    return {"success": True}


def removeProfessorFromCourse(c_code):
    """
    Removes the professor assignment from a course by setting AM_Instructor to NULL.

    Args:
        c_code (str): The unique course identifier.

    Returns:
        dict: {"success": True} on success,
              {"success": False, "error": str} on failure.
    """
    course = getCourse(c_code)
    if not course:
        return {"success": False, "error": f"Course '{c_code}' not found."}

    result = updateCourse(c_code, AM_Instructor=None)
    if not result:
        return {"success": False, "error": "Failed to remove professor from course."}

    return {"success": True}


def enrollStudentInCourse(am_student, c_code, start_date):
    """
    Enrolls a student in a course after validating both entities exist
    and that no duplicate enrollment exists.

    Args:
        am_student (str): The unique student identifier.
        c_code (str): The unique course identifier.
        start_date (str): The enrollment start date (YYYY-MM-DD).

    Returns:
        dict: {"success": True} on success,
              {"success": False, "error": str} on failure.
    """
    student = getStudent(am_student)
    if not student:
        return {"success": False, "error": f"Student '{am_student}' not found."}

    course = getCourse(c_code)
    if not course:
        return {"success": False, "error": f"Course '{c_code}' not found."}

    existing = getEnrollment(am_student, c_code)
    if existing:
        return {"success": False, "error": f"Student '{am_student}' is already enrolled in course '{c_code}'."}

    result = addEnrollment(am_student, c_code, start_date)
    if not result:
        return {"success": False, "error": "Failed to create enrollment."}

    return {"success": True}


def withdrawStudentFromCourse(am_student, c_code):
    """
    Withdraws a student from a course by deleting the enrollment record.

    Args:
        am_student (str): The unique student identifier.
        c_code (str): The unique course identifier.

    Returns:
        dict: {"success": True} on success,
              {"success": False, "error": str} on failure.
    """
    existing = getEnrollment(am_student, c_code)
    if not existing:
        return {"success": False, "error": f"Enrollment not found for student '{am_student}' in course '{c_code}'."}

    result = deleteEnrollment(am_student, c_code)
    if not result:
        return {"success": False, "error": "Failed to withdraw student from course."}

    return {"success": True}


def getCourseRoster(c_code):
    """
    Retrieves all students enrolled in a given course.

    Args:
        c_code (str): The unique course identifier.

    Returns:
        dict: {"success": True, "students": list} on success,
              {"success": False, "error": str} if course not found.
    """
    course = getCourse(c_code)
    if not course:
        return {"success": False, "error": f"Course '{c_code}' not found."}

    conn = getConnection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT s.AM, s.FirstName, s.LastName, s.email, e.StartDate
            FROM ENROLLMENT e
            JOIN STUDENT s ON s.AM = e.AM_Student
            WHERE e.C_Code = ?
            ORDER BY s.LastName, s.FirstName
            """,
            (c_code,)
        )
        rows = cursor.fetchall()
        return {"success": True, "students": [dict(row) for row in rows]}
    finally:
        conn.close()


def getProfessorCourseLoad(am_instructor):
    """
    Retrieves all courses taught by a given professor.

    Args:
        am_instructor (str): The unique instructor identifier.

    Returns:
        dict: {"success": True, "courses": list} on success,
              {"success": False, "error": str} if professor not found.
    """
    professor = getProfessor(am_instructor)
    if not professor:
        return {"success": False, "error": f"Professor '{am_instructor}' not found."}

    conn = getConnection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT C_Code, Title, Description, Category
            FROM COURSE
            WHERE AM_Instructor = ?
            ORDER BY Title
            """,
            (am_instructor,)
        )
        rows = cursor.fetchall()
        return {"success": True, "courses": [dict(row) for row in rows]}
    finally:
        conn.close()


def getStudentSchedule(am_student):
    """
    Retrieves all courses a student is enrolled in.

    Args:
        am_student (str): The unique student identifier.

    Returns:
        dict: {"success": True, "courses": list} on success,
              {"success": False, "error": str} if student not found.
    """
    student = getStudent(am_student)
    if not student:
        return {"success": False, "error": f"Student '{am_student}' not found."}

    conn = getConnection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT c.C_Code, c.Title, c.Description, c.Category,
                   c.AM_Instructor, e.StartDate
            FROM ENROLLMENT e
            JOIN COURSE c ON c.C_Code = e.C_Code
            WHERE e.AM_Student = ?
            ORDER BY c.Title
            """,
            (am_student,)
        )
        rows = cursor.fetchall()
        return {"success": True, "courses": [dict(row) for row in rows]}
    finally:
        conn.close()


def listAvailableStudents(c_code):
    """
    Retrieves students not currently enrolled in the specified course.
    Useful for enrollment forms where a user picks which student to add.

    Args:
        c_code (str): The unique course identifier.

    Returns:
        dict: {"success": True, "students": list} on success,
              {"success": False, "error": str} if course not found.
    """
    course = getCourse(c_code)
    if not course:
        return {"success": False, "error": f"Course '{c_code}' not found."}

    conn = getConnection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT AM, FirstName, LastName, email
            FROM STUDENT
            WHERE AM NOT IN (
                SELECT AM_Student FROM ENROLLMENT WHERE C_Code = ?
            )
            ORDER BY LastName, FirstName
            """,
            (c_code,)
        )
        rows = cursor.fetchall()
        return {"success": True, "students": [dict(row) for row in rows]}
    finally:
        conn.close()


def listAvailableCourses(am_student):
    """
    Retrieves courses a student is not currently enrolled in.
    Useful for enrollment forms where a student picks a course to join.

    Args:
        am_student (str): The unique student identifier.

    Returns:
        dict: {"success": True, "courses": list} on success,
              {"success": False, "error": str} if student not found.
    """
    student = getStudent(am_student)
    if not student:
        return {"success": False, "error": f"Student '{am_student}' not found."}

    conn = getConnection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT C_Code, Title, Description, Category, AM_Instructor
            FROM COURSE
            WHERE C_Code NOT IN (
                SELECT C_Code FROM ENROLLMENT WHERE AM_Student = ?
            )
            ORDER BY Title
            """,
            (am_student,)
        )
        rows = cursor.fetchall()
        return {"success": True, "courses": [dict(row) for row in rows]}
    finally:
        conn.close()