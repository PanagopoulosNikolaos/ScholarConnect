"""
src/api_actions/__init__.py

Public API for ScholarConnect database actions.
Exposes CRUD operations for students and professors.
"""

from .student_actions import (
    addStudent,
    getStudent,
    listStudents,
    updateStudent,
    deleteStudent,
)

from .professor_actions import (
    addProfessor,
    getProfessor,
    listProfessors,
    updateProfessor,
    deleteProfessor,
)

from .course_actions import (
    addCourse,
    getCourse,
    listCourses,
    updateCourse,
    deleteCourse,
)

from .enrollment_actions import (
    addEnrollment,
    getEnrollment,
    listEnrollments,
    updateEnrollment,
    deleteEnrollment,
)

from .evaluation_actions import (
    addEvaluation,
    getEvaluation,
    listEvaluations,
    updateEvaluation,
    deleteEvaluation,
)

from .course_management import (
    assignProfessorToCourse,
    removeProfessorFromCourse,
    enrollStudentInCourse,
    withdrawStudentFromCourse,
    getCourseRoster,
    getProfessorCourseLoad,
    getStudentSchedule,
    listAvailableStudents,
    listAvailableCourses,
)

__all__ = [
    "addStudent",
    "getStudent",
    "listStudents",
    "updateStudent",
    "deleteStudent",
    "addProfessor",
    "getProfessor",
    "listProfessors",
    "updateProfessor",
    "deleteProfessor",
    "addCourse",
    "getCourse",
    "listCourses",
    "updateCourse",
    "deleteCourse",
    "addEnrollment",
    "getEnrollment",
    "listEnrollments",
    "updateEnrollment",
    "deleteEnrollment",
    "addEvaluation",
    "getEvaluation",
    "listEvaluations",
    "updateEvaluation",
    "deleteEvaluation",
    "assignProfessorToCourse",
    "removeProfessorFromCourse",
    "enrollStudentInCourse",
    "withdrawStudentFromCourse",
    "getCourseRoster",
    "getProfessorCourseLoad",
    "getStudentSchedule",
    "listAvailableStudents",
    "listAvailableCourses",
]
