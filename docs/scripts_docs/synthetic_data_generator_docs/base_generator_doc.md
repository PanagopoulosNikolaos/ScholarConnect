# base_generator.py Documentation

## Navigation Table

| Name | Type | Description |
|------|------|-------------|
| [BaseGenerator](#basegenerator) | Class | Shared foundation for all ScholarConnect synthetic-data generators. |
| [BaseGenerator.__init__](#__init__) | Function | Initialises the shared Faker instance and RNG seed. |
| [BaseGenerator._regNumber](#_regNumber) | Function | Builds a formatted registration number used as a primary key. |

## Overview
This file defines the `BaseGenerator` class which acts as a shared foundation for all synthetic data generators within the ScholarConnect project. It sets up a common Faker instance and random seed for reproducibility and provides utility methods.

## Detailed Breakdown

## BaseGenerator

**Class Responsibility:** Provides the shared foundation for all ScholarConnect synthetic-data generators. It initializes a shared Faker instance (optionally seeded for reproducibility) and exposes common helper functions like `_regNumber` used by all inheriting sub-generators.

### __init__

**Signature:**
```python
def __init__(self, seed: int | None = None) -> None
```

**Purpose:** Initialises the shared Faker instance and RNG seed.

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| seed | int \| None | No | None | Integer seed for reproducible output |

**Returns:**
| Type | Description |
|------|-------------|
| None | Returns nothing |

**Source Code:**
```python
    def __init__(self, seed: int | None = None) -> None:
        self._seed = seed
        self._fake = Faker()

        if seed is not None:
            Faker.seed(seed)
            random.seed(seed)
```

**Implementation (Executable Logic Only):**
* **Line 0:** `def __init__(self, seed: int | None = None) -> None:` — Initializes the class instance.
* **Line 1:** `self._seed = seed` — Stores the optional random seed.
* **Line 2:** `self._fake = Faker()` — Instantiates the Faker library object.
* **Line 4:** `if seed is not None:` — Checks if a specific seed was provided.
* **Line 5:** `Faker.seed(seed)` — Seeds the Faker generator to ensure deterministic output.
* **Line 6:** `random.seed(seed)` — Seeds Python's built-in random module to ensure deterministic output.

**Dependencies:**
| Symbol | Kind | Purpose | Source |
|--------|------|---------|--------|
| Faker | External | Synthetic data generation | faker |
| random | External | Random number generation | random |

### _regNumber

**Signature:**
```python
def _regNumber(self, prefix: str, index: int, width: int = 6) -> str
```

**Purpose:** Builds a formatted registration number used as a primary key.

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| prefix | str | Yes | — | Capital-letter prefix, e.g. 'S' or 'P' |
| index | int | Yes | — | Numeric part of the identifier |
| width | int | No | 6 | Zero-pad width for the numeric segment |

**Returns:**
| Type | Description |
|------|-------------|
| str | A string like 'S000042' or 'P000007' |

**Source Code:**
```python
    def _regNumber(self, prefix: str, index: int, width: int = 6) -> str:
        return f"{prefix}{str(index).zfill(width)}"
```

**Implementation (Executable Logic Only):**
* **Line 0:** `def _regNumber(self, prefix: str, index: int, width: int = 6) -> str:` — Function definition.
* **Line 1:** `return f"{prefix}{str(index).zfill(width)}"` — Combines the string prefix with the zero-padded index to form the complete registration number.

**Dependencies:**
| Symbol | Kind | Purpose | Source |
|--------|------|---------|--------|
| None | None | None | None |
