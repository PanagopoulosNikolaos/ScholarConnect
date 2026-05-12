import pandas as pd
from .base_generator import BaseGenerator


class StudentGenerator(BaseGenerator):
    """
    Generates synthetic rows for the Students table.

    Each row includes: AM, Password, Username, email, FirstName, LastName
    mirroring the SQL schema exactly.  Username is set equal to AM so
    the registration number doubles as the login handle.

    Functions:
        __init__    -- Initialises the generator with an optional seed.
        generate    -- Returns a DataFrame of n student rows.
    """

    def __init__(self, seed: int | None = None) -> None:
        """
        Initialises StudentGenerator.

        Args:
            seed (int | None): RNG seed for reproducibility.
        """
        super().__init__(seed)

    def generate(self, n: int = 50) -> pd.DataFrame:
        """
        Produces a DataFrame of synthetic student records.

        Uniqueness constraints on AM and email are enforced with a
        set-based deduplication loop.

        Args:
            n (int): Number of student rows to generate. Defaults to 50.

        Returns:
            pd.DataFrame: DataFrame with columns matching the Students schema.

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

            am = self._regNumber("S", idx)

            # Generate a unique email address.
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
                "email":               email,
                "FirstName":           first,
                "LastName":            last,
            })

        return pd.DataFrame(rows)