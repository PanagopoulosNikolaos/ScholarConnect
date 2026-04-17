

import random
from datetime import date, timedelta
import pandas as pd
from .base_generator import BaseGenerator


class RelationshipGenerator(BaseGenerator):
    """
    Generates synthetic rows for all four relationship/junction tables.

    Requires pre-generated Students, Professors, and Courses DataFrames so
    that all foreign-key constraints are satisfied by construction.

    Tables produced:
        - TeachingAssignments    (professor <-> course, 1-to-many)
        - Enrollments            (student   <-> course, many-to-many)
        - ProfessorEvaluations   (student   -> professor, many-to-many)
        - EvaluationComments     (multivalued comments on evaluations)

    Functions:
        __init__                  -- Stores entity DataFrames and seed.
        generateTeaching          -- Returns TeachingAssignments DataFrame.
        generateEnrollments       -- Returns Enrollments DataFrame.
        generateEvaluations       -- Returns ProfessorEvaluations DataFrame.
        generateEvaluationComments-- Returns EvaluationComments DataFrame.
    """

    # Possible professor-feedback sentences for evaluation comments.
    _COMMENT_TEMPLATES = [
        "Excellent explanations and very supportive during office hours.",
        "The course material was well-structured and engaging.",
        "Sometimes lectures moved too fast, but overall a great professor.",
        "Very knowledgeable in the subject, though feedback on assignments was slow.",
        "Clear and concise delivery; highly recommended.",
        "The professor was approachable and answered questions thoroughly.",
        "Assignments were challenging but helped reinforce the content.",
        "Could improve the practical component of the course.",
        "Outstanding guidance throughout the semester.",
        "Lectures were informative, though more real-world examples would help.",
    ]

    def __init__(
        self,
        students_df:   pd.DataFrame,
        professors_df: pd.DataFrame,
        courses_df:    pd.DataFrame,
        seed:          int | None = None,
    ) -> None:
        """
        Initialises RelationshipGenerator with pre-built entity DataFrames.

        Args:
            students_df   (pd.DataFrame): Output of StudentGenerator.generate().
            professors_df (pd.DataFrame): Output of ProfessorGenerator.generate().
            courses_df    (pd.DataFrame): Output of CourseGenerator.generate().
            seed          (int | None):  RNG seed for reproducibility.
        """
        super().__init__(seed)

        self._students   = students_df
        self._professors = professors_df
        self._courses    = courses_df

        # Extract primary-key lists for FK sampling.
        self._student_ids   = students_df["registration_number"].tolist()
        self._professor_ids = professors_df["registration_number"].tolist()
        self._course_codes  = courses_df["course_code"].tolist()

    # TeachingAssignments

    def generateTeaching(
        self,
        max_courses_per_prof: int = 3,
    ) -> pd.DataFrame:
        """
        Produces TeachingAssignments rows.

        Each professor is assigned between 1 and max_courses_per_prof courses.
        Duplicate (professor, course) pairs are eliminated.

        Args:
            max_courses_per_prof (int): Upper bound on courses per professor.
                                        Defaults to 3.

        Returns:
            pd.DataFrame: Columns — professor_registration_number, course_code.
        """
        seen_pairs: set[tuple[str, str]] = set()
        rows: list[dict] = []

        for prof_id in self._professor_ids:
            n_courses = random.randint(1, max(1, max_courses_per_prof))
            # Sample without replacement up to available courses.
            assigned = random.sample(
                self._course_codes,
                k=min(n_courses, len(self._course_codes)),
            )
            for code in assigned:
                pair = (prof_id, code)
                if pair not in seen_pairs:
                    seen_pairs.add(pair)
                    rows.append({
                        "professor_registration_number": prof_id,
                        "course_code":                  code,
                    })

        return pd.DataFrame(rows)

    # Enrollments

    def generateEnrollments(
        self,
        min_courses_per_student: int = 2,
        max_courses_per_student: int = 6,
        grade_null_probability:  float = 0.15,
    ) -> pd.DataFrame:
        """
        Produces Enrollments rows linking students to courses.

        Each student is enrolled in a random number of courses within the
        given range.  Grade is nullable to model in-progress enrolments.

        Args:
            min_courses_per_student (int):   Minimum courses enrolled per student.
            max_courses_per_student (int):   Maximum courses enrolled per student.
            grade_null_probability  (float): Probability a grade is NULL (0.0 – 1.0).

        Returns:
            pd.DataFrame: Columns — student_registration_number, course_code,
                          grade, enrollment_date.

        Raises:
            ValueError: If probabilities or range boundaries are invalid.
        """
        if not (0.0 <= grade_null_probability <= 1.0):
            raise ValueError("grade_null_probability must be between 0.0 and 1.0.")
        if min_courses_per_student > max_courses_per_student:
            raise ValueError("min_courses_per_student cannot exceed max_courses_per_student.")

        seen_pairs: set[tuple[str, str]] = set()
        rows: list[dict] = []

        # Define an enrolment date window spanning the current academic year.
        academic_year_start = date(date.today().year - 1, 9, 1)
        academic_year_end   = date.today()

        for student_id in self._student_ids:
            n_courses = random.randint(
                min_courses_per_student,
                min(max_courses_per_student, len(self._course_codes)),
            )
            enrolled = random.sample(self._course_codes, k=n_courses)

            for code in enrolled:
                pair = (student_id, code)
                if pair not in seen_pairs:
                    seen_pairs.add(pair)

                    # Null grade models a course still in progress.
                    grade = (
                        None
                        if random.random() < grade_null_probability
                        else round(random.uniform(4.0, 10.0), 2)
                    )

                    enroll_date = academic_year_start + timedelta(
                        days=random.randint(
                            0,
                            (academic_year_end - academic_year_start).days,
                        )
                    )

                    rows.append({
                        "student_registration_number": student_id,
                        "course_code":                 code,
                        "grade":                       grade,
                        "enrollment_date":             enroll_date,
                    })

        return pd.DataFrame(rows)

    # ProfessorEvaluations

    def generateEvaluations(
        self,
        evaluation_probability: float = 0.40,
    ) -> pd.DataFrame:
        """
        Produces ProfessorEvaluations rows.

        Each (student, professor) pair is included independently with the
        given probability, keeping evaluation volume realistic.

        Args:
            evaluation_probability (float): Likelihood a student evaluates a
                                            given professor (0.0 – 1.0).
                                            Defaults to 0.40.

        Returns:
            pd.DataFrame: Columns — student_registration_number,
                          professor_registration_number, grade.

        Raises:
            ValueError: If evaluation_probability is outside [0.0, 1.0].
        """
        if not (0.0 <= evaluation_probability <= 1.0):
            raise ValueError("evaluation_probability must be between 0.0 and 1.0.")

        rows: list[dict] = []

        for student_id in self._student_ids:
            for prof_id in self._professor_ids:
                if random.random() < evaluation_probability:
                    rows.append({
                        "student_registration_number":   student_id,
                        "professor_registration_number": prof_id,
                        "grade": round(random.uniform(1.0, 10.0), 2),
                    })

        return pd.DataFrame(rows)

    # EvaluationComments

    def generateEvaluationComments(
        self,
        evaluations_df:      pd.DataFrame,
        max_comments_per_eval: int = 3,
        comment_probability: float = 0.70,
    ) -> pd.DataFrame:
        """
        Produces EvaluationComments rows for the given evaluations.

        Models the multivalued Comments attribute from the ER diagram: each
        ProfessorEvaluation can have 0-max_comments_per_eval comments.

        Args:
            evaluations_df        (pd.DataFrame): Output of generateEvaluations().
            max_comments_per_eval (int):          Upper bound on comments per evaluation.
            comment_probability   (float):        Probability any single evaluation
                                                  receives at least one comment.

        Returns:
            pd.DataFrame: Columns — comment_id, student_registration_number,
                          professor_registration_number, comment_text.

        Raises:
            ValueError: If evaluations_df is empty or probabilities are invalid.
        """
        if evaluations_df.empty:
            raise ValueError("evaluations_df must not be empty.")
        if not (0.0 <= comment_probability <= 1.0):
            raise ValueError("comment_probability must be between 0.0 and 1.0.")

        rows: list[dict] = []
        comment_id = 1

        for _, eval_row in evaluations_df.iterrows():
            if random.random() > comment_probability:
                continue  # This evaluation receives no comments.

            n_comments = random.randint(1, max(1, max_comments_per_eval))
            for _ in range(n_comments):
                rows.append({
                    "comment_id":                    comment_id,
                    "student_registration_number":   eval_row["student_registration_number"],
                    "professor_registration_number": eval_row["professor_registration_number"],
                    "comment_text":                  random.choice(self._COMMENT_TEMPLATES),
                })
                comment_id += 1

        return pd.DataFrame(rows)
