# course_generator.py Documentation

## Navigation Table

| Name | Type | Description |
|------|------|-------------|
| [CourseGenerator](#coursegenerator) | Class | Generates synthetic rows for the Courses table. |
| [CourseGenerator.__init__](#__init__) | Function | Initialises CourseGenerator. |
| [CourseGenerator.generate](#generate) | Function | Produces a DataFrame of synthetic course records. |

## Overview
This file contains the `CourseGenerator` class, which extends the `BaseGenerator` to produce synthetic rows for the Courses database table. It utilizes a predefined categorized dictionary of courses and can generate additional fallback titles using Faker if requested beyond its catalogue limits.

## Detailed Breakdown

## CourseGenerator

**Class Responsibility:** Generates synthetic data targeting the Courses schema. It produces records including `course_code`, `title`, `category`, and `description`. It manages a static dictionary of realistic course titles and can scale generation organically.

### __init__

**Signature:**
```python
def __init__(self, seed: int | None = None) -> None
```

**Purpose:** Initialises CourseGenerator and flattens the course catalogue.

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

        self._course_pool: list[tuple[str, str]] = [
            (cat, title)
            for cat, titles in self._CATALOGUE.items()
            for title in titles
        ]
```

**Implementation (Executable Logic Only):**
* **Line 0:** `def __init__(self, seed: int | None = None) -> None:` — Initializes the CourseGenerator instance.
* **Line 1:** `super().__init__(seed)` — Invokes the parent class constructor to set up Faker and randomness.
* **Line 3:** `self._course_pool: list[tuple[str, str]] = [...]` — Flattens the static `_CATALOGUE` dictionary into a list of tuples containing category and course title combinations.

**Dependencies:**
| Symbol | Kind | Purpose | Source |
|--------|------|---------|--------|
| BaseGenerator | Internal | Inheritance foundation | .base_generator |

### generate

**Primary Library:** `pandas`  
**Purpose:** Produces a DataFrame of synthetic course records.

#### Overview
Generates the specific number of course records requested. It randomizes the course pool and returns them as a pandas DataFrame. If the requested number exceeds the pre-defined catalogue size, it dynamically creates extra records using generic strings.

#### Signature
```python
def generate(self, n: int | None = None) -> pd.DataFrame
```

#### Parameters
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| n | int \| None | No | None | Number of course rows. Defaults to full catalogue size. |

#### Returns
| Type | Description |
|------|-------------|
| pd.DataFrame | DataFrame with columns matching the Courses schema. |

#### Raises
| Exception | Condition |
|-----------|-----------|
| ValueError | If `n` is provided and less than 1. |

#### Dependencies
* **Required Libraries:** `pandas` (Returning generated row sets)
* **Internal Modules:** `self._reg_number` (Generating formatted code numbers)

#### Workflow (Executable Logic Only)

**Phase 1: Validation and Pool Initialization**
Validates limits and shuffles the base catalogue items.
* **Operation 1:** Validates that `n` is 1 or greater if provided.
* **Operation 2:** Copies the current `_course_pool` to a localized mutable variable and shuffles its elements.

*Code Context:*
```python
        if n is not None and n < 1:
            raise ValueError("n must be at least 1.")

        pool = list(self._course_pool)
        random.shuffle(pool)
```

**Phase 2: Fallback Generation Padding**
Appends extra elements to the list if requested to produce more records than predefined.
* **Operation 1:** Checks if `n` is larger than the local `pool`'s length.
* **Operation 2:** Iteratively appends new course records using `random.choice` for category and `self._fake.catch_phrase()` for generating the titles until capacity is reached.

*Code Context:*
```python
        if n is not None and n > len(pool):
            categories = list(self._CATALOGUE.keys())
            for extra_idx in range(n - len(pool)):
                pool.append((
                    random.choice(categories),
                    self._fake.catch_phrase(),
                ))
```

**Phase 3: Row Construction**
Converts data sets into dictionary records and constructs the DataFrame.
* **Operation 1:** Sets the target number of records up to `n` or the size of `pool`.
* **Operation 2:** Iterates through the bounded target list, building course rows using the category and titles. Uses the `_reg_number` tool for IDs and `Faker.paragraph` for descriptions.
* **Operation 3:** Converts the constructed list of dictionaries into a `pd.DataFrame`.

#### Source Code
```python
    def generate(self, n: int | None = None) -> pd.DataFrame:
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
```

#### Usage Example
```python
generator = CourseGenerator(seed=42)
courses_df = generator.generate(n=30)
```

#### Common Issues & Related Functions
* **Issue:** Requesting `n < 1` triggers a `ValueError`.
