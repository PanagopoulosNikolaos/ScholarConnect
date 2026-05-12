import random
import pandas as pd
from .base_generator import BaseGenerator


class ProfessorGenerator(BaseGenerator):
    """
    Generates synthetic rows for the INSTRUCTOR table.

    Each row includes: AM, Password, Username, FirstName, LastName, email, Specialization.
    Username is set equal to AM so the registration number doubles as the login handle.

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
            pd.DataFrame: DataFrame with columns matching the INSTRUCTOR schema.

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

            am = self._regNumber("P", idx)

            email = self._fake.email()
            while email in seen_emails:
                email = self._fake.email()
            seen_emails.add(email)

            rows.append({
                "AM":                  am,
                "Password":            self._fake.password(
                                           length=16,
                                           special_chars=True,
                                           digits=True,
                                           upper_case=True,
                                       ),
                "Username":            am,
                "FirstName":           first,
                "LastName":            last,
                "email":               email,
                "Specialization":      random.choice(self._SPECIALIZATIONS),
            })

        return pd.DataFrame(rows)