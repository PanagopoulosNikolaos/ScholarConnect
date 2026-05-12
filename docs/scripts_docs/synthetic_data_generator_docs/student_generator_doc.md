# student_generator.py Documentation

## Navigation Table

| Name | Type | Description |
|------|------|-------------|
| [StudentGenerator](#studentgenerator) | Class | Generates synthetic rows for the Students table. |
| [StudentGenerator.__init__](#__init__) | Function | Initialises StudentGenerator. |
| [StudentGenerator.generate](#generate) | Function | Produces a DataFrame of synthetic student records. |

## Overview
This file contains the `StudentGenerator` class which creates records corresponding to the Students table schema. By extending `BaseGenerator`, it utilizes shared dependencies while crafting deterministic identifiers (AM), equating the username to the AM, and verifying unique email addresses.

## Detailed Breakdown

## StudentGenerator

**Class Responsibility:** Constructs structured dictionary rows mapping synthetic student objects. Implements uniqueness constraint protections evaluating previous identities preventing key-duplicates over emails, and directly maps Username to AM for academic login realism.

### Constructor

**Signature:**
```python
def __init__(self, seed: int | None = None) -> None
```

**Purpose:** Initialises StudentGenerator.

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| seed | int \| None | No | None | RNG seed for reproducibility |

**Returns:**
| Type | Description |
|------|-------------|
| return_type | Returns nothing (None) |

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
**Purpose:** Produces a DataFrame of synthetic student records.

#### Overview
Computes user data iterations establishing secure passwords, name formatting, and randomized credentials representing student records. Implements a `while` loop guaranteeing `email` properties never encounter uniqueness collisions internally, and sets `Username` to `AM`.

#### Signature
```python
def generate(self, n: int = 50) -> pd.DataFrame
```

#### Parameters
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| n | int | No | 50 | Number of student rows to generate |

#### Returns
| Type | Description |
|------|-------------|
| pd.DataFrame | Tabular dataframe holding mapped data arrays |

#### Raises
| Exception | Condition |
|-----------|-----------|
| ValueError | Input `n` lies below `1` minimal threshold |

#### Dependencies
* **Required Libraries:** `pandas`
* **Internal Modules:** `self._regNumber`

#### Workflow (Executable Logic Only)

**Phase 1: Generation Limits and Set Instantiation**
Validates minimum limit bounds and prepares structures to filter uniqueness metrics.
* **Operation 1:** Throws `ValueError` exception for misconfigured arguments.
* **Operation 2:** Initializes set `seen_emails` for uniqueness checks and array list `rows`.

*Code Context:*
```python
        if n < 1:
            raise ValueError("n must be at least 1.")

        seen_emails: set[str] = set()
        rows: list[dict] = []
```

**Phase 2: Entity Property Population**
Builds attributes string values per student iterative component mapping.
* **Operation 1:** Derives `first` and `last` name from Faker structures.
* **Operation 2:** Generates an `am` (Registration Number) utilizing `self._regNumber`.
* **Operation 3:** Formulates similarly protected constraints dictating generic email fields looping duplicate conditions explicitly tracking.
* **Operation 4:** Compiles dictionaries assigning exact Student schema properties (AM, Password, Username, email, FirstName, LastName), specifically setting `Username` equivalent to `am`. Configures passwords utilizing Faker library length constraints. Appends row structure.

*Code Context:*
```python
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
```

**Phase 3: Formatting Return Values**
Packs list data to tabular structures.
* **Operation 1:** Constructs and returns a `pd.DataFrame` instance initialized using the assembled `rows`.

#### Source Code
```python
    def generate(self, n: int = 50) -> pd.DataFrame:
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
```

#### Usage Example
```python
generator = StudentGenerator(seed=42)
df = generator.generate(n=100)
```

#### Common Issues & Related Functions
* **Issue:** Slow operation when generating millions of rows due to collision checking.
