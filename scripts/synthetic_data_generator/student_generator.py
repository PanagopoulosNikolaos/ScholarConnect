
import random
import pandas as pd
from .base_generator import BaseGenerator


class StudentGenerator(BaseGenerator):
    """
    Generates synthetic rows for the Students table.

    Each row includes: registration_number, full_name, username,
    password, and email — mirroring the SQL schema exactly.

    Functions:
        __init__    -- Initialises the generator with an optional seed.
        generate    -- Returns a DataFrame of n student rows.
    """

    # Academic-domain usernames keep a realistic feel.
    _username_suffixes = ["_uni", "_stud", "2024", "2025", "_sc", ""]

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

        Uniqueness constraints on registration_number, username, and email
        are enforced with a set-based deduplication loop.

        Args:
            n (int): Number of student rows to generate. Defaults to 50.

        Returns:
            pd.DataFrame: DataFrame with columns matching the Students schema.

        Raises:
            ValueError: If n is less than 1.
        """
        if n < 1:
            raise ValueError("n must be at least 1.")

        seen_usernames: set[str] = set()
        seen_emails: set[str] = set()
        rows: list[dict] = []

        for idx in range(1, n + 1):
            first = self._fake.first_name()
            last  = self._fake.last_name()

            # Build a unique username derived from the person's name.
            base_uname = f"{first.lower()}.{last.lower()}"
            suffix     = random.choice(self._username_suffixes)
            username   = f"{base_uname}{suffix}"
            # Append a counter suffix when collisions occur.
            while username in seen_usernames:
                username = f"{base_uname}{suffix}{random.randint(1, 999)}"
            seen_usernames.add(username)

            # Generate a unique email address.
            email = self._fake.email()
            while email in seen_emails:
                email = self._fake.email()
            seen_emails.add(email)

            rows.append({
                "registration_number": self._regNumber("S", idx),
                "full_name":           f"{first} {last}",
                "username":            username,
                "password":            self._fake.password(
                                           length=16,
                                           special_chars=True,
                                           digits=True,
                                           upper_case=True,
                                       ),
                "email":               email,
            })

        return pd.DataFrame(rows)
