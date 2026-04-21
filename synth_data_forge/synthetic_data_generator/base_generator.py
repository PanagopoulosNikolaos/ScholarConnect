

import random
from faker import Faker


class BaseGenerator:
    """
    Shared foundation for all ScholarConnect synthetic-data generators.

    Owns a single Faker instance (optionally seeded for reproducibility)
    and exposes helpers used by every sub-generator.

    Functions:
        __init__    -- Initialises Faker and stores the RNG seed.
        _regNumber  -- Generates a zero-padded registration-number string.
    """

    def __init__(self, seed: int | None = None) -> None:
        """
        Initialises the shared Faker instance and RNG seed.

        Args:
            seed (int | None): Integer seed for reproducible output.
                               Defaults to None (non-deterministic).
        """
        self._seed = seed
        self._fake = Faker()

        if seed is not None:
            Faker.seed(seed)
            random.seed(seed)

    def _regNumber(self, prefix: str, index: int, width: int = 6) -> str:
        """
        Builds a formatted registration number used as a primary key.

        Args:
            prefix (str): Capital-letter prefix, e.g. 'S' or 'P'.
            index  (int): Numeric part of the identifier.
            width  (int): Zero-pad width for the numeric segment.

        Returns:
            str: A string like 'S000042' or 'P000007'.
        """
        return f"{prefix}{str(index).zfill(width)}"
