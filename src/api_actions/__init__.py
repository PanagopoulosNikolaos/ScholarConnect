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
]
