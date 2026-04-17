

import random
import pandas as pd
from .base_generator import BaseGenerator


class CourseGenerator(BaseGenerator):
    """
    Generates synthetic rows for the Courses table.

    Each row includes: course_code, title, category, and description.

    Functions:
        __init__    -- Initialises the generator with an optional seed.
        generate    -- Returns a DataFrame of n course rows.
    """

    # Course catalogue structured as (category, [titles]).
    _CATALOGUE: dict[str, list[str]] = {
        "Computer Science": [
            "Introduction to Programming",
            "Data Structures and Algorithms",
            "Operating Systems",
            "Compiler Design",
            "Theory of Computation",
        ],
        "Software Engineering": [
            "Software Requirements Engineering",
            "Agile Development",
            "Design Patterns",
            "Software Testing",
            "DevOps Fundamentals",
        ],
        "Data Science": [
            "Statistics for Data Science",
            "Machine Learning",
            "Deep Learning",
            "Data Visualisation",
            "Big Data Technologies",
        ],
        "Networking": [
            "Computer Networks",
            "Network Security",
            "Wireless Communications",
            "Cloud Computing",
            "Internet of Things",
        ],
        "Mathematics": [
            "Discrete Mathematics",
            "Linear Algebra",
            "Calculus",
            "Probability Theory",
            "Numerical Methods",
        ],
    }

    def __init__(self, seed: int | None = None) -> None:
        """
        Initialises CourseGenerator.

        Args:
            seed (int | None): RNG seed for reproducibility.
        """
        super().__init__(seed)

        # Flatten catalogue into (category, title) pairs once.
        self._course_pool: list[tuple[str, str]] = [
            (cat, title)
            for cat, titles in self._CATALOGUE.items()
            for title in titles
        ]

    def generate(self, n: int | None = None) -> pd.DataFrame:
        """
        Produces a DataFrame of synthetic course records.

        When n is None the entire predefined catalogue is used (25 courses).
        When n exceeds the catalogue size, extra rows are generated with
        Faker-derived titles to satisfy the request.

        Args:
            n (int | None): Number of course rows. Defaults to None (full catalogue).

        Returns:
            pd.DataFrame: DataFrame with columns matching the Courses schema.

        Raises:
            ValueError: If n is provided and less than 1.
        """
        if n is not None and n < 1:
            raise ValueError("n must be at least 1.")

        pool = list(self._course_pool)   # mutable copy
        random.shuffle(pool)

        # Pad with Faker data if more courses are requested than the catalogue holds.
        if n is not None and n > len(pool):
            categories = list(self._CATALOGUE.keys())
            for extra_idx in range(n - len(pool)):
                pool.append((
                    random.choice(categories),
                    self._fake.catch_phrase(),  # generic sentence as a course title
                ))

        target = n if n is not None else len(pool)
        rows: list[dict] = []

        for idx, (category, title) in enumerate(pool[:target], start=1):
            rows.append({
                "course_code":  self._reg_number("C", idx, width=4),
                "title":        title,
                "category":     category,
                "description":  self._fake.paragraph(nb_sentences=3),
            })

        return pd.DataFrame(rows)
