
import random
import pandas as pd
from .base_generator import BaseGenerator


class ProfessorGenerator(BaseGenerator):
    """
    Generates synthetic rows for the Professors table.

    Each row includes: registration_number, first_name, last_name,
    email, and specialization.

    Functions:
        __init__    -- Initialises the generator with an optional seed.
        generate    -- Returns a DataFrame of n professor rows.
    """

    # Academic specialisations for a university system.
    _SPECIALIZATIONS = [
        "Computer Science",
        "Software Engineering",
        "Data Science",
        "Artificial Intelligence",
        "Cybersecurity",
        "Networking",
        "Database Systems",
        "Mathematics",
        "Physics",
        "Electrical Engineering",
        "Information Systems",
        "Human-Computer Interaction",
    ]

    def __init__(self, seed: int | None = None) -> None:
        """
        Initialises ProfessorGenerator.

        Args:
            seed (int | None): RNG seed for reproducibility.
        """
        super().__init__(seed)

    def generate(self, n: int = 10) -> pd.DataFrame:
        """
        Produces a DataFrame of synthetic professor records.

        Args:
            n (int): Number of professor rows to generate. Defaults to 10.

        Returns:
            pd.DataFrame: DataFrame with columns matching the Professors schema.

        Raises:
            ValueError: If n is less than 1.
        """
        if n < 1:
            raise ValueError("n must be at least 1.")

        seen_emails: set[str] = set()
        rows: list[dict] = []

        for idx in range(1, n + 1):
            first = self._fake.first_name()
            last  = self._fake.last_name()

            email = self._fake.email()
            while email in seen_emails:
                email = self._fake.email()
            seen_emails.add(email)

            rows.append({
                "registration_number": self._reg_number("P", idx),
                "first_name":          first,
                "last_name":           last,
                "email":               email,
                "specialization":      random.choice(self._SPECIALIZATIONS),
            })

        return pd.DataFrame(rows)
