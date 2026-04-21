"""
scripts/__init__.py

Public API for the ScholarConnect synthetic-data package.

Importing from this package exposes all four generator classes directly,
so consumer code requires only a single import statement.

Usage:
    from scripts import StudentGenerator, ProfessorGenerator
    from scripts import CourseGenerator, RelationshipGenerator
"""

from .synthetic_data_generator import (
    StudentGenerator,
    ProfessorGenerator,
    CourseGenerator,
    RelationshipGenerator,
)

__all__ = [
    "StudentGenerator",
    "ProfessorGenerator",
    "CourseGenerator",
    "RelationshipGenerator",
]
