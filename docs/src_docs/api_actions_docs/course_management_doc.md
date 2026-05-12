# course_management.py Documentation

## Navigation Table

| Name | Type | Description |
|------|------|-------------|
| [assignProfessorToCourse](#assignprofessortocourse) | Function | Assigns a professor to a course after validating both entities exist. |
| [removeProfessorFromCourse](#removeprofessorfromcourse) | Function | Removes the professor assignment from a course by setting AM_Instructor to NULL. |
| [enrollStudentInCourse](#enrollstudentincourse) | Function | Enrolls a student in a course after validating both entities exist and that no duplicate enrollment exists. |
| [withdrawStudentFromCourse](#withdrawstudentfromcourse) | Function | Withdraws a student from a course by deleting the enrollment record. |
| [getCourseRoster](#getcourseroster) | Function | Retrieves all students enrolled in a given course. |
| [getProfessorCourseLoad](#getprofessorcourseload) | Function | Retrieves all courses taught by a given professor. |
| [getStudentSchedule](#getstudentschedule) | Function | Retrieves all courses a student is enrolled in. |
| [listAvailableStudents](#listavailablestudents) | Function | Retrieves students not currently enrolled in the specified course. |
| [listAvailableCourses](#listavailablecourses) | Function | Retrieves courses a student is not currently enrolled in. |

## Overview
This file implements the business logic layer for course-related operations in ScholarConnect. It orchestrates multi-step workflows such as professor assignment and student enrollment, enforcing validation rules before delegating to the underlying CRUD actions. The module provides query convenience functions for course rosters, professor course loads, student schedules, and available enrollment candidates.

## Detailed Breakdown

### assignProfessorToCourse

**Signature:**
```python
def assignProfessorToCourse(c_code, am_instructor)
```

**Purpose:** Assigns a professor to a course after validating both entities exist.

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| c_code | str | Yes | — | The unique course identifier. |
| am_instructor | str | Yes | — | The unique instructor identifier. |

**Returns:**
| Type | Description |
|------|-------------|
| dict | `{"success": True}` on success, `{"success": False, "error": str}` on failure. |

**Source Code:**
```python
def assignProfessorToCourse(c_code, am_instructor):
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
```

**Implementation (Executable Logic Only):**
* **Line 0:** `def assignProfessorToCourse(...)` — Accepts course code and instructor identifier.
* **Line 1:** `course = getCourse(c_code)` — Retrieves course record to verify existence.
* **Line 2:** `if not course:` — Guards against invalid course codes.
* **Line 5:** `professor = getProfessor(am_instructor)` — Retrieves instructor record to verify existence.
* **Line 6:** `if not professor:` — Guards against invalid instructor identifiers.
* **Line 9:** `result = updateCourse(c_code, ...)` — Delegates to CRUD update to set the instructor foreign key.
* **Line 10:** `if not result:` — Checks for update failure.
* **Line 13:** `return {"success": True}` — Signals successful assignment.

**Dependencies:**
| Symbol | Kind | Purpose | Source |
|--------|------|---------|--------|
| getCourse | Internal | Verify course existence | src.api_actions.course_actions |
| getProfessor | Internal | Verify instructor existence | src.api_actions.professor_actions |
| updateCourse | Internal | Persist professor assignment | src.api_actions.course_actions |


### removeProfessorFromCourse

**Signature:**
```python
def removeProfessorFromCourse(c_code)
```

**Purpose:** Removes the professor assignment from a course by setting AM_Instructor to NULL.

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| c_code | str | Yes | — | The unique course identifier. |

**Returns:**
| Type | Description |
|------|-------------|
| dict | `{"success": True}` on success, `{"success": False, "error": str}` on failure. |

**Source Code:**
```python
def removeProfessorFromCourse(c_code):
    course = getCourse(c_code)
    if not course:
        return {"success": False, "error": f"Course '{c_code}' not found."}

    result = updateCourse(c_code, AM_Instructor=None)
    if not result:
        return {"success": False, "error": "Failed to remove professor from course."}

    return {"success": True}
```

**Implementation (Executable Logic Only):**
* **Line 0:** `def removeProfessorFromCourse(c_code):` — Accepts course code for unassignment.
* **Line 1:** `course = getCourse(c_code)` — Verifies target course exists.
* **Line 2:** `if not course:` — Early exit for invalid course codes.
* **Line 5:** `result = updateCourse(c_code, ...)` — Sets instructor foreign key to NULL via CRUD update.
* **Line 6:** `if not result:` — Handles update failure case.
* **Line 9:** `return {"success": True}` — Confirms successful removal.

**Dependencies:**
| Symbol | Kind | Purpose | Source |
|--------|------|---------|--------|
| getCourse | Internal | Verify course existence | src.api_actions.course_actions |
| updateCourse | Internal | Nullify instructor assignment | src.api_actions.course_actions |


### enrollStudentInCourse

**Signature:**
```python
def enrollStudentInCourse(am_student, c_code, start_date)
```

**Purpose:** Enrolls a student in a course after validating both entities exist and that no duplicate enrollment exists.

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| am_student | str | Yes | — | The unique student identifier. |
| c_code | str | Yes | — | The unique course identifier. |
| start_date | str | Yes | — | The enrollment start date (YYYY-MM-DD). |

**Returns:**
| Type | Description |
|------|-------------|
| dict | `{"success": True}` on success, `{"success": False, "error": str}` on failure. |

**Source Code:**
```python
def enrollStudentInCourse(am_student, c_code, start_date):
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
```

**Implementation (Executable Logic Only):**
* **Line 0:** `def enrollStudentInCourse(...)` — Accepts student, course, and start date.
* **Line 1:** `student = getStudent(am_student)` — Verifies student identity in the system.
* **Line 2:** `if not student:` — Rejects nonexistent students.
* **Line 5:** `course = getCourse(c_code)` — Verifies course exists in the catalog.
* **Line 6:** `if not course:` — Rejects nonexistent courses.
* **Line 9:** `existing = getEnrollment(am_student, c_code)` — Checks for existing enrollment to prevent duplicates.
* **Line 10:** `if existing:` — Returns error when duplicate enrollment is detected.
* **Line 13:** `result = addEnrollment(...)` — Delegates to CRUD to persist the enrollment record.
* **Line 14:** `if not result:` — Checks for persistence failure.
* **Line 17:** `return {"success": True}` — Confirms successful enrollment.

**Dependencies:**
| Symbol | Kind | Purpose | Source |
|--------|------|---------|--------|
| getStudent | Internal | Verify student existence | src.api_actions.student_actions |
| getCourse | Internal | Verify course existence | src.api_actions.course_actions |
| getEnrollment | Internal | Check duplicate enrollment | src.api_actions.enrollment_actions |
| addEnrollment | Internal | Persist new enrollment | src.api_actions.enrollment_actions |


### withdrawStudentFromCourse

**Signature:**
```python
def withdrawStudentFromCourse(am_student, c_code)
```

**Purpose:** Withdraws a student from a course by deleting the enrollment record.

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| am_student | str | Yes | — | The unique student identifier. |
| c_code | str | Yes | — | The unique course identifier. |

**Returns:**
| Type | Description |
|------|-------------|
| dict | `{"success": True}` on success, `{"success": False, "error": str}` on failure. |

**Source Code:**
```python
def withdrawStudentFromCourse(am_student, c_code):
    existing = getEnrollment(am_student, c_code)
    if not existing:
        return {"success": False, "error": f"Enrollment not found for student '{am_student}' in course '{c_code}'."}

    result = deleteEnrollment(am_student, c_code)
    if not result:
        return {"success": False, "error": "Failed to withdraw student from course."}

    return {"success": True}
```

**Implementation (Executable Logic Only):**
* **Line 0:** `def withdrawStudentFromCourse(...)` — Accepts student and course identifiers.
* **Line 1:** `existing = getEnrollment(am_student, c_code)` — Verifies enrollment record exists before deletion.
* **Line 2:** `if not existing:` — Prevents deletion of nonexistent enrollments.
* **Line 5:** `result = deleteEnrollment(...)` — Delegates to CRUD to remove the enrollment record.
* **Line 6:** `if not result:` — Handles deletion failure.
* **Line 9:** `return {"success": True}` — Confirms withdrawal.

**Dependencies:**
| Symbol | Kind | Purpose | Source |
|--------|------|---------|--------|
| getEnrollment | Internal | Verify enrollment exists | src.api_actions.enrollment_actions |
| deleteEnrollment | Internal | Remove enrollment record | src.api_actions.enrollment_actions |


### getCourseRoster

**Signature:**
```python
def getCourseRoster(c_code)
```

**Purpose:** Retrieves all students enrolled in a given course.

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| c_code | str | Yes | — | The unique course identifier. |

**Returns:**
| Type | Description |
|------|-------------|
| dict | `{"success": True, "students": list}` on success, `{"success": False, "error": str}` if course not found. |

**Source Code:**
```python
def getCourseRoster(c_code):
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
```

**Implementation (Executable Logic Only):**
* **Line 0:** `def getCourseRoster(c_code):` — Accepts course code to query.
* **Line 1:** `course = getCourse(c_code)` — Validates course exists before querying enrollment.
* **Line 2:** `if not course:` — Rejects invalid course identifiers early.
* **Line 6:** `cursor.execute(...)` — Executes JOIN query linking ENROLLMENT and STUDENT tables filtered by course code.
* **Line 15:** `rows = cursor.fetchall()` — Materializes all matching enrollment rows.
* **Line 16:** `return {"success": True, "students": ...}` — Returns structured result with student list.
* **Line 18:** `conn.close()` — Releases database connection in the finally block.

**Dependencies:**
| Symbol | Kind | Purpose | Source |
|--------|------|---------|--------|
| getCourse | Internal | Verify course existence | src.api_actions.course_actions |
| getConnection | External | Establish database link | src.database |


### getProfessorCourseLoad

**Signature:**
```python
def getProfessorCourseLoad(am_instructor)
```

**Purpose:** Retrieves all courses taught by a given professor.

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| am_instructor | str | Yes | — | The unique instructor identifier. |

**Returns:**
| Type | Description |
|------|-------------|
| dict | `{"success": True, "courses": list}` on success, `{"success": False, "error": str}` if professor not found. |

**Source Code:**
```python
def getProfessorCourseLoad(am_instructor):
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
```

**Implementation (Executable Logic Only):**
* **Line 0:** `def getProfessorCourseLoad(am_instructor):` — Accepts instructor identifier.
* **Line 1:** `professor = getProfessor(am_instructor)` — Validates instructor identity.
* **Line 2:** `if not professor:` — Prevents query for nonexistent professors.
* **Line 8:** `cursor.execute(...)` — Queries COURSE table filtered by instructor foreign key.
* **Line 14:** `rows = cursor.fetchall()` — Collects all course records assigned to the instructor.
* **Line 15:** `return {"success": True, "courses": ...}` — Returns structured result with course list.
* **Line 17:** `conn.close()` — Safely closes database connection.

**Dependencies:**
| Symbol | Kind | Purpose | Source |
|--------|------|---------|--------|
| getProfessor | Internal | Verify instructor existence | src.api_actions.professor_actions |
| getConnection | External | Establish database link | src.database |


### getStudentSchedule

**Signature:**
```python
def getStudentSchedule(am_student)
```

**Purpose:** Retrieves all courses a student is enrolled in.

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| am_student | str | Yes | — | The unique student identifier. |

**Returns:**
| Type | Description |
|------|-------------|
| dict | `{"success": True, "courses": list}` on success, `{"success": False, "error": str}` if student not found. |

**Source Code:**
```python
def getStudentSchedule(am_student):
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
```

**Implementation (Executable Logic Only):**
* **Line 0:** `def getStudentSchedule(am_student):` — Accepts student identifier.
* **Line 1:** `student = getStudent(am_student)` — Validates student exists in the system.
* **Line 2:** `if not student:` — Guards against invalid student identifiers.
* **Line 8:** `cursor.execute(...)` — Executes JOIN query across ENROLLMENT and COURSE tables filtered by student.
* **Line 15:** `rows = cursor.fetchall()` — Collects all course records for the student.
* **Line 16:** `return {"success": True, "courses": ...}` — Returns structured result with course list and enrollment metadata.
* **Line 18:** `conn.close()` — Releases database connection.

**Dependencies:**
| Symbol | Kind | Purpose | Source |
|--------|------|---------|--------|
| getStudent | Internal | Verify student existence | src.api_actions.student_actions |
| getConnection | External | Establish database link | src.database |


### listAvailableStudents

**Signature:**
```python
def listAvailableStudents(c_code)
```

**Purpose:** Retrieves students not currently enrolled in the specified course. Useful for enrollment forms where a user picks which student to add.

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| c_code | str | Yes | — | The unique course identifier. |

**Returns:**
| Type | Description |
|------|-------------|
| dict | `{"success": True, "students": list}` on success, `{"success": False, "error": str}` if course not found. |

**Source Code:**
```python
def listAvailableStudents(c_code):
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
```

**Implementation (Executable Logic Only):**
* **Line 0:** `def listAvailableStudents(c_code):` — Accepts course code.
* **Line 1:** `course = getCourse(c_code)` — Validates target course exists.
* **Line 2:** `if not course:` — Rejects invalid course identifiers.
* **Line 8:** `cursor.execute(...)` — Executes subquery filtering out enrolled students using NOT IN.
* **Line 14:** `rows = cursor.fetchall()` — Materializes result set of available students.
* **Line 15:** `return {"success": True, "students": ...}` — Returns structured result with student list.
* **Line 17:** `conn.close()` — Safely closes database connection.

**Dependencies:**
| Symbol | Kind | Purpose | Source |
|--------|------|---------|--------|
| getCourse | Internal | Verify course existence | src.api_actions.course_actions |
| getConnection | External | Establish database link | src.database |


### listAvailableCourses

**Signature:**
```python
def listAvailableCourses(am_student)
```

**Purpose:** Retrieves courses a student is not currently enrolled in. Useful for enrollment forms where a student picks a course to join.

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| am_student | str | Yes | — | The unique student identifier. |

**Returns:**
| Type | Description |
|------|-------------|
| dict | `{"success": True, "courses": list}` on success, `{"success": False, "error": str}` if student not found. |

**Source Code:**
```python
def listAvailableCourses(am_student):
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
```

**Implementation (Executable Logic Only):**
* **Line 0:** `def listAvailableCourses(am_student):` — Accepts student identifier.
* **Line 1:** `student = getStudent(am_student)` — Validates student identity.
* **Line 2:** `if not student:` — Guards against invalid student identifiers.
* **Line 8:** `cursor.execute(...)` — Executes subquery filtering out enrolled courses using NOT IN.
* **Line 14:** `rows = cursor.fetchall()` — Collects all available course records.
* **Line 15:** `return {"success": True, "courses": ...}` — Returns structured result with course list.
* **Line 17:** `conn.close()` — Releases database connection.

**Dependencies:**
| Symbol | Kind | Purpose | Source |
|--------|------|---------|--------|
| getStudent | Internal | Verify student identity in the system | src.api_actions.student_actions |
| getConnection | External | Establish database link | src.database |