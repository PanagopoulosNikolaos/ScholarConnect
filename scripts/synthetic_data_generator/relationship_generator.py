

import random
from datetime import date, timedelta
import pandas as pd
from .base_generator import BaseGenerator


class RelationshipGenerator(BaseGenerator):
    """
    Generates synthetic rows for all relationship tables.

    Requires pre-generated Students, Professors, and Courses DataFrames so
    that all foreign-key constraints are satisfied by construction.

    Tables produced:
        - ENROLLMENT (student <-> course, many-to-many)
        - EVALUATION (student -> instructor evaluating a specific course)

    Functions:
        __init__                  -- Stores entity DataFrames and seed.
        generateEnrollments       -- Returns ENROLLMENT DataFrame.
        generateEvaluations       -- Returns EVALUATION DataFrame.
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
        self._student_ids   = students_df["AM"].tolist()
        self._course_codes  = courses_df["C_Code"].tolist()

    # Enrollments

    def generateEnrollments(
        self,
        min_courses_per_student: int = 2,
        max_courses_per_student: int = 6,
    ) -> pd.DataFrame:
        """
        Produces ENROLLMENT rows linking students to courses.

        Each student is enrolled in a random number of courses within the
        given range.

        Args:
            min_courses_per_student (int):   Minimum courses enrolled per student.
            max_courses_per_student (int):   Maximum courses enrolled per student.

        Returns:
            pd.DataFrame: Columns — AM_Student, C_Code, StartDate.

        Raises:
            ValueError: If range boundaries are invalid.
        """
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

                    enroll_date = academic_year_start + timedelta(
                        days=random.randint(
                            0,
                            (academic_year_end - academic_year_start).days,
                        )
                    )

                    rows.append({
                        "AM_Student": student_id,
                        "C_Code":     code,
                        "StartDate":  enroll_date,
                    })

        return pd.DataFrame(rows)

    # Evaluations

    def generateEvaluations(
        self,
        evaluation_probability: float = 0.40,
    ) -> pd.DataFrame:
        """
        Produces EVALUATION rows.

        Each (student, course) pair is evaluated independently with the
        given probability, keeping evaluation volume realistic. We extract
        the course's assigned instructor to fill the AM_Instructor field.

        Args:
            evaluation_probability (float): Likelihood a student evaluates a
                                            given course (0.0 – 1.0).
                                            Defaults to 0.40.

        Returns:
            pd.DataFrame: Columns — AM_Instructor, AM_Student, C_Code, Rating, Comments.

        Raises:
            ValueError: If evaluation_probability is outside [0.0, 1.0].
        """
        if not (0.0 <= evaluation_probability <= 1.0):
            raise ValueError("evaluation_probability must be between 0.0 and 1.0.")

        rows: list[dict] = []

        for student_id in self._student_ids:
            for _, course_row in self._courses.iterrows():
                if random.random() < evaluation_probability:
                    comment = random.choice(self._COMMENT_TEMPLATES) if random.random() < 0.7 else None
                    rows.append({
                        "AM_Instructor": course_row["AM_Instructor"],
                        "AM_Student":    student_id,
                        "C_Code":        course_row["C_Code"],
                        "Rating":        round(random.uniform(1.0, 10.0), 0),
                        "Comments":      comment
                    })

        return pd.DataFrame(rows)
