# student_generator.py Documentation

## Navigation Table

| Name | Type | Description |
|------|------|-------------|
| [StudentGenerator](#studentgenerator) | Class | Generates synthetic rows for the Students table. |
| [StudentGenerator.__init__](#__init__) | Function | Initialises StudentGenerator. |
| [StudentGenerator.generate](#generate) | Function | Produces a DataFrame of synthetic student records. |

## Overview
This file contains the `StudentGenerator` class which creates records corresponding to the Students table schema. By extending `BaseGenerator`, it utilizes shared dependencies while crafting deterministic identifiers representing structured usernames and email addresses.

## Detailed Breakdown

## StudentGenerator

**Class Responsibility:** Constructs structured dictionary rows mapping synthetic user objects modeling academic environments. Implements unique constraint protections evaluating previous identities preventing key-duplicates over emails or usernames within generations.

### __init__

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
**Purpose:** Produces a DataFrame of synthetic student records.

#### Overview
Computes user data iterations establishing secure passwords, domain formatting, and randomized credentials representing student interactions. Implements multiple `while` loops guaranteeing `username` and `email` properties never encounter uniqueness collisions internally.

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
* **Required Libraries:** `pandas`, `random`
* **Internal Modules:** `self._regNumber`

#### Workflow (Executable Logic Only)

**Phase 1: Generation Limits and Set Instantiation**
Validates minimum limit bounds and prepares structures to filter uniqueness metrics.
* **Operation 1:** Throws `ValueError` exception for misconfigured arguments.
* **Operation 2:** Initializes sets `seen_usernames` and `seen_emails` monitoring history tables. Sets array list `rows`.

*Code Context:*
```python
        if n < 1:
            raise ValueError("n must be at least 1.")

        seen_usernames: set[str] = set()
        seen_emails: set[str] = set()
        rows: list[dict] = []
```

**Phase 2: Entity Property Population**
Builds attributes string values per student iterative component mapping.
* **Operation 1:** Derives `first_name` and `last_name` faker structures.
* **Operation 2:** Calculates deterministic usernames utilizing generated names, looping conditionally `username in seen_usernames` avoiding collision artifacts via integer appendages. Records established ID.
* **Operation 3:** Formulates similarly protected constraints dictating generic email fields looping duplicate conditions explicitly tracking.
* **Operation 4:** Compiles dictionaries assigning primary key indexes using helper functions. Configures passwords utilizing Faker library length constraints adding uppercase/digits properties explicitly. Appends row structure.

*Code Context:*
```python
        for idx in range(1, n + 1):
            first = self._fake.first_name()
            last  = self._fake.last_name()

            base_uname = f"{first.lower()}.{last.lower()}"
            suffix     = random.choice(self._USERNAME_SUFFIXES)
            username   = f"{base_uname}{suffix}"
            while username in seen_usernames:
                username = f"{base_uname}{suffix}{random.randint(1, 999)}"
            seen_usernames.add(username)

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
```

#### Source Code
```python
    def generate(self, n: int = 50) -> pd.DataFrame:
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
            suffix     = random.choice(self._USERNAME_SUFFIXES)
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
```
