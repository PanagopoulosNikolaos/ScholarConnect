# professor_generator.py Documentation

## Navigation Table

| Name | Type | Description |
|------|------|-------------|
| [ProfessorGenerator](#professorgenerator) | Class | Generates synthetic rows for the Professors table. |
| [ProfessorGenerator.__init__](#__init__) | Function | Initialises ProfessorGenerator. |
| [ProfessorGenerator.generate](#generate) | Function | Produces a DataFrame of synthetic professor records. |

## Overview
This file contains the `ProfessorGenerator` class, responsible for producing synthetic data for the Professors table. It handles the generation of unique IDs, names, emails, and academic specialisations, building off the shared logic in `BaseGenerator`.

## Detailed Breakdown

## ProfessorGenerator

**Class Responsibility:** Generates randomized records mirroring the Professors schema, creating realistic fields such as names, unique emails, and randomized academic specialisations from a predefined set.

### __init__

**Signature:**
```python
def __init__(self, seed: int | None = None) -> None
```

**Purpose:** Initialises ProfessorGenerator.

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| seed | int \| None | No | None | RNG seed for reproducibility |

**Returns:**
| Type | Description |
|------|-------------|
| None | Returns nothing |

**Source Code:**
```python
    def __init__(self, seed: int | None = None) -> None:
        super().__init__(seed)
```

**Implementation (Executable Logic Only):**
* **Line 0:** `def __init__(self, seed: int | None = None) -> None:` — Initializes the instance.
* **Line 1:** `super().__init__(seed)` — Invokes the parent constructor.

**Dependencies:**
| Symbol | Kind | Purpose | Source |
|--------|------|---------|--------|
| BaseGenerator | Internal | Inheritance foundation | .base_generator |

### generate

**Primary Library:** `pandas`  
**Purpose:** Produces a DataFrame of synthetic professor records.

#### Overview
Iterates `n` times to create distinct records representing professors. Generates first name, last name, and a verified-unique email using a while-loop collision check. Binds each professor to a randomized specialization and compiles the final result into a DataFrame.

#### Signature
```python
def generate(self, n: int = 10) -> pd.DataFrame
```

#### Parameters
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| n | int | No | 10 | Number of professor rows to generate. |

#### Returns
| Type | Description |
|------|-------------|
| pd.DataFrame | DataFrame with columns matching the Professors schema. |

#### Raises
| Exception | Condition |
|-----------|-----------|
| ValueError | If `n` is less than 1. |

#### Dependencies
* **Required Libraries:** `pandas` (Formatting row data), `random` (Specialization choices)
* **Internal Modules:** `self._regNumber` (Generating IDs)

#### Workflow (Executable Logic Only)

**Phase 1: Setup and Validation**
Validates minimum limit bounds and prepares variables.
* **Operation 1:** Checks if `n` is `< 1` and throws `ValueError` if so.
* **Operation 2:** Initializes a set `seen_emails` to track uniqueness and a list `rows` for accumulating data.

*Code Context:*
```python
        if n < 1:
            raise ValueError("n must be at least 1.")

        seen_emails: set[str] = set()
        rows: list[dict] = []
```

**Phase 2: Generation Loop**
Iteratively generates specific details for every requested professor.
* **Operation 1:** Extracts `first_name` and `last_name` using `self._fake`.
* **Operation 2:** Generates an `email`, entering a `while` loop until a unique email string is discovered, and saves it into `seen_emails`.
* **Operation 3:** Constructs the row dictionary using `_regNumber`, Faker values, and a randomly selected `_SPECIALIZATIONS` string, then appends it to `rows`.

*Code Context:*
```python
        for idx in range(1, n + 1):
            first = self._fake.first_name()
            last  = self._fake.last_name()

            email = self._fake.email()
            while email in seen_emails:
                email = self._fake.email()
            seen_emails.add(email)

            rows.append({
                "registration_number": self._regNumber("P", idx),
                "first_name":          first,
                "last_name":           last,
                "email":               email,
                "specialization":      random.choice(self._SPECIALIZATIONS),
            })
```

**Phase 3: Formatting Return Values**
Packs list data to tabular structures.
* **Operation 1:** Constructs and returns a `pd.DataFrame` instance initialized using the assembled `rows`.

#### Source Code
```python
    def generate(self, n: int = 10) -> pd.DataFrame:
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
                "registration_number": self._regNumber("P", idx),
                "first_name":          first,
                "last_name":           last,
                "email":               email,
                "specialization":      random.choice(self._SPECIALIZATIONS),
            })

        return pd.DataFrame(rows)
```

#### Usage Example
```python
generator = ProfessorGenerator(seed=42)
df = generator.generate(n=15)
```

#### Common Issues & Related Functions
* **Issue:** Slow operation when generating millions of rows due to collision checking.
