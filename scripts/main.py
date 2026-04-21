"""
main.py

Entry point for synthetic data generation in the ScholarConnect project.

Instantiates each generator in foreign-key dependency order, generates all
seven tables, and prints a summary row count for each — serving as a quick
smoke-test that confirms the package is wired correctly.

Dependency order (mirrors FK constraints from db_relations_diagram.md):
    1. Students              -- no dependencies
    2. Professors            -- no dependencies
    3. Courses               -- no dependencies
    4. TeachingAssignments   -- depends on Professors, Courses
    5. Enrollments           -- depends on Students, Courses
    6. ProfessorEvaluations  -- depends on Students, Professors
    7. EvaluationComments    -- depends on ProfessorEvaluations
"""

from . import (
    StudentGenerator,
    ProfessorGenerator,
    CourseGenerator,
    RelationshipGenerator,
)

# Configuration

seed           = 42    # Ensures identical output on every run.
n_students     = 80
n_professors   = 12
n_courses      = None  # None → full 25-course catalogue.


def main() -> None:
    """
    Generates all ScholarConnect tables and prints a row-count summary.

    Returns:
        None
    """
    # Standalone entity tables

    students_df   = StudentGenerator(seed=seed).generate(n=n_students)
    professors_df = ProfessorGenerator(seed=seed).generate(n=n_professors)
    courses_df    = CourseGenerator(seed=seed).generate(n=n_courses)

    # Relationship / junction tables

    rel_gen = RelationshipGenerator(
        students_df=students_df,
        professors_df=professors_df,
        courses_df=courses_df,
        seed=seed,
    )

    teaching_df   = rel_gen.generateTeaching(max_courses_per_prof=4)
    enrollments_df = rel_gen.generateEnrollments(
        min_courses_per_student=2,
        max_courses_per_student=7,
        grade_null_probability=0.10,
    )
    evaluations_df = rel_gen.generateEvaluations(evaluation_probability=0.35)
    comments_df    = rel_gen.generateEvaluationComments(
        evaluations_df=evaluations_df,
        max_comments_per_eval=3,
        comment_probability=0.65,
    )

    # Summary

    table_summary = {
        "Students":             students_df,
        "Professors":           professors_df,
        "Courses":              courses_df,
        "TeachingAssignments":  teaching_df,
        "Enrollments":          enrollments_df,
        "ProfessorEvaluations": evaluations_df,
        "EvaluationComments":   comments_df,
    }

    print("\n--- ScholarConnect Synthetic Data Summary ---")
    for table_name, df in table_summary.items():
        print(f"  {table_name:<25} {len(df):>6} rows")
    print("--------------------------------------------\n")
    # save dataset to "./data"
    for table_name, df in table_summary.items():
            df.to_csv(f"./data/{table_name}.csv", index=False)

    
if __name__ == "__main__":
    main()
