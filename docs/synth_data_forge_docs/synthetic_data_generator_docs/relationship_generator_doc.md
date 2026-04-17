# relationship_generator.py Documentation

## Navigation Table

| Name | Type | Description |
|------|------|-------------|
| [RelationshipGenerator](#relationshipgenerator) | Class | Generates synthetic rows for all four relationship/junction tables. |
| [RelationshipGenerator.__init__](#__init__) | Function | Initialises RelationshipGenerator with pre-built entity DataFrames. |
| [RelationshipGenerator.generateTeaching](#generateteaching) | Function | Produces TeachingAssignments rows. |
| [RelationshipGenerator.generateEnrollments](#generateenrollments) | Function | Produces Enrollments rows linking students to courses. |
| [RelationshipGenerator.generateEvaluations](#generateevaluations) | Function | Produces ProfessorEvaluations rows. |
| [RelationshipGenerator.generateEvaluationComments](#generateevaluationcomments) | Function | Produces EvaluationComments rows for the given evaluations. |

## Overview
This file introduces the `RelationshipGenerator` class, which constructs complex relational database junction tables. It integrates directly with previously generated entities (Students, Professors, Courses) ensuring that foreign key relationships represent realistic distributions without orphans or constraint violations.

## Detailed Breakdown

## RelationshipGenerator

**Class Responsibility:** Takes multiple initialized independent entity data tables and constructs valid relationship bridges: `TeachingAssignments`, `Enrollments`, `ProfessorEvaluations`, and `EvaluationComments`. It orchestrates logic to maintain uniqueness within join tables and apply reasonable probabilities.

### __init__

**Signature:**
```python
def __init__(self, students_df: pd.DataFrame, professors_df: pd.DataFrame, courses_df: pd.DataFrame, seed: int | None = None) -> None
```

**Purpose:** Initialises RelationshipGenerator with pre-built entity DataFrames.

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| students_df | pd.DataFrame | Yes | — | Output of StudentGenerator.generate() |
| professors_df | pd.DataFrame | Yes | — | Output of ProfessorGenerator.generate() |
| courses_df | pd.DataFrame | Yes | — | Output of CourseGenerator.generate() |
| seed | int \| None | No | None | RNG seed for reproducibility |

**Returns:**
| Type | Description |
|------|-------------|
| None | Returns nothing |

**Source Code:**
```python
    def __init__(
        self,
        students_df:   pd.DataFrame,
        professors_df: pd.DataFrame,
        courses_df:    pd.DataFrame,
        seed:          int | None = None,
    ) -> None:
        super().__init__(seed)

        self._students   = students_df
        self._professors = professors_df
        self._courses    = courses_df

        self._student_ids   = students_df["registration_number"].tolist()
        self._professor_ids = professors_df["registration_number"].tolist()
        self._course_codes  = courses_df["course_code"].tolist()
```

**Implementation (Executable Logic Only):**
* **Line 0:** `def __init__(...) -> None:` — Method signature mapping primary inputs.
* **Line 7:** `super().__init__(seed)` — Setup via base generator class.
* **Line 9:** `self._students = students_df` — Caches the DataFrame argument.
* **Line 10:** `self._professors = professors_df` — Caches the DataFrame argument.
* **Line 11:** `self._courses = courses_df` — Caches the DataFrame argument.
* **Line 13:** `self._student_ids = students_df["registration_number"].tolist()` — Casts index keys for sampling algorithms.
* **Line 14:** `self._professor_ids = professors_df["registration_number"].tolist()` — Casts index keys for sampling algorithms.
* **Line 15:** `self._course_codes = courses_df["course_code"].tolist()` — Casts index keys for sampling algorithms.

**Dependencies:**
| Symbol | Kind | Purpose | Source |
|--------|------|---------|--------|
| BaseGenerator | Internal | Inheritance foundation | .base_generator |

### generateTeaching

**Primary Library:** `pandas`  
**Purpose:** Produces TeachingAssignments rows linking professors and courses.

#### Overview
Iterates over all established professors and assigns them a bounded random count of courses they teach. Identifies previously assigned sets using a unique lookup table to prevent duplication.

#### Signature
```python
def generateTeaching(self, max_courses_per_prof: int = 3) -> pd.DataFrame
```

#### Parameters
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| max_courses_per_prof | int | No | 3 | Upper bound on courses per professor |

#### Returns
| Type | Description |
|------|-------------|
| pd.DataFrame | Table matching `TeachingAssignments` structure |

#### Dependencies
* **Required Libraries:** `pandas`, `random`

#### Workflow (Executable Logic Only)

**Phase 1: Assignment Mapping**
Computes randomized relationships by iterating target identifiers.
* **Operation 1:** Initiates an empty `seen_pairs` set and `rows` list array.
* **Operation 2:** Explores every ID within `_professor_ids`. Determines course volume randomly against `max_courses_per_prof`.
* **Operation 3:** Samples exact course targets utilizing `random.sample()`. Adds a composite tuple `(prof_id, code)` exclusively if missing from `seen_pairs`.

*Code Context:*
```python
        for prof_id in self._professor_ids:
            n_courses = random.randint(1, max(1, max_courses_per_prof))
            assigned = random.sample(
                self._course_codes,
                k=min(n_courses, len(self._course_codes)),
            )
            for code in assigned:
                pair = (prof_id, code)
                if pair not in seen_pairs:
                    seen_pairs.add(pair)
                    rows.append({
                        "professor_registration_number": prof_id,
                        "course_code":                  code,
                    })
```

**Phase 2: Data Transformation**
Returns standardized data table.
* **Operation 1:** Wraps computed collection array in `pd.DataFrame`.

#### Source Code
```python
    def generateTeaching(
        self,
        max_courses_per_prof: int = 3,
    ) -> pd.DataFrame:
        seen_pairs: set[tuple[str, str]] = set()
        rows: list[dict] = []

        for prof_id in self._professor_ids:
            n_courses = random.randint(1, max(1, max_courses_per_prof))
            # Sample without replacement up to available courses.
            assigned = random.sample(
                self._course_codes,
                k=min(n_courses, len(self._course_codes)),
            )
            for code in assigned:
                pair = (prof_id, code)
                if pair not in seen_pairs:
                    seen_pairs.add(pair)
                    rows.append({
                        "professor_registration_number": prof_id,
                        "course_code":                  code,
                    })

        return pd.DataFrame(rows)
```

### generateEnrollments

**Primary Library:** `pandas`  
**Purpose:** Produces Enrollments rows linking students to courses.

#### Overview
Maps students randomly onto courses reflecting enrollment logic, assigning pseudo-random dates restricted around modern academic timelines and conditionally providing evaluation grades or NULL metrics (when marked in-progress).

#### Signature
```python
def generateEnrollments(self, min_courses_per_student: int = 2, max_courses_per_student: int = 6, grade_null_probability: float = 0.15) -> pd.DataFrame
```

#### Parameters
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| min_courses_per_student | int | No | 2 | Minimum courses enrolled per student |
| max_courses_per_student | int | No | 6 | Maximum courses enrolled per student |
| grade_null_probability | float | No | 0.15 | Likelihood the grade holds no score value |

#### Returns
| Type | Description |
|------|-------------|
| pd.DataFrame | Dataframe of enrollment interactions |

#### Raises
| Exception | Condition |
|-----------|-----------|
| ValueError | Invalid constraints regarding probability fractions or bounding minimums exceeding maximums |

#### Dependencies
* **Required Libraries:** `pandas`, `datetime.date`, `datetime.timedelta`, `random`

#### Workflow (Executable Logic Only)

**Phase 1: Input Validation and Timeline Base**
Guards variables against logical conflicts, setting reference offsets for times.
* **Operation 1:** Throws `ValueError` exception for misconfigured arguments.
* **Operation 2:** Resolves the window interval from `academic_year_start` to `academic_year_end` calculated relative to the system clock.

**Phase 2: Distribution Generation**
Constructs independent associations reflecting realistic student involvement.
* **Operation 1:** Traverses students computing variable constraints `n_courses`.
* **Operation 2:** Extrapolates elements through `random.sample`, registering tuples into `seen_pairs` identically matching previous approaches.
* **Operation 3:** Determines randomized `grade` based heavily on `grade_null_probability`, falling back to float `4.0-10.0` distribution metrics.
* **Operation 4:** Formulates the string representation utilizing `timedelta` shifting offsets around the `academic_year_start`.

*Code Context:*
```python
                    grade = (
                        None
                        if random.random() < grade_null_probability
                        else round(random.uniform(4.0, 10.0), 2)
                    )

                    enroll_date = academic_year_start + timedelta(
                        days=random.randint(
                            0,
                            (academic_year_end - academic_year_start).days,
                        )
                    )
```

#### Source Code
```python
    def generateEnrollments(
        self,
        min_courses_per_student: int = 2,
        max_courses_per_student: int = 6,
        grade_null_probability:  float = 0.15,
    ) -> pd.DataFrame:
        if not (0.0 <= grade_null_probability <= 1.0):
            raise ValueError("grade_null_probability must be between 0.0 and 1.0.")
        if min_courses_per_student > max_courses_per_student:
            raise ValueError("min_courses_per_student cannot exceed max_courses_per_student.")

        seen_pairs: set[tuple[str, str]] = set()
        rows: list[dict] = []

        # Define an enrolment date window spanning the current academic year.
        academic_year_start = date(date.today().year - 1, 9, 1)
        academic_year_end   = date.today()

        for student_id in self._student_ids:
            n_courses = random.randint(
                min_courses_per_student,
                min(max_courses_per_student, len(self._course_codes)),
            )
            enrolled = random.sample(self._course_codes, k=n_courses)

            for code in enrolled:
                pair = (student_id, code)
                if pair not in seen_pairs:
                    seen_pairs.add(pair)

                    # Null grade models a course still in progress.
                    grade = (
                        None
                        if random.random() < grade_null_probability
                        else round(random.uniform(4.0, 10.0), 2)
                    )

                    enroll_date = academic_year_start + timedelta(
                        days=random.randint(
                            0,
                            (academic_year_end - academic_year_start).days,
                        )
                    )

                    rows.append({
                        "student_registration_number": student_id,
                        "course_code":                 code,
                        "grade":                       grade,
                        "enrollment_date":             enroll_date,
                    })

        return pd.DataFrame(rows)
```

### generateEvaluations

**Primary Library:** `pandas`  
**Purpose:** Produces ProfessorEvaluations rows.

#### Overview
Iterates against permutations joining all existing students facing all existing professors. Executes probability comparisons to include or pass the iteration. Included mappings record numerical evaluation scoring metrics.

#### Signature
```python
def generateEvaluations(self, evaluation_probability: float = 0.40) -> pd.DataFrame
```

#### Parameters
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| evaluation_probability | float | No | 0.40 | Likelihood student executes a review |

#### Returns
| Type | Description |
|------|-------------|
| pd.DataFrame | Dataframe matching `ProfessorEvaluations` specification |

#### Raises
| Exception | Condition |
|-----------|-----------|
| ValueError | Float variable not bound between `0.0` and `1.0` constraints |

#### Dependencies
* **Required Libraries:** `pandas`, `random`

#### Workflow (Executable Logic Only)

**Phase 1: Dual Iteration Check**
Reviews probability limits ensuring correct values, maps relationships iteratively conditionally.
* **Operation 1:** Ensures argument inputs stand within bounds.
* **Operation 2:** Evaluates two `for` loops across identities.
* **Operation 3:** Resolves condition `if random.random() < evaluation_probability` returning uniformly distributed decimals bound `1.0` through `10.0` upon validation limit pass.

*Code Context:*
```python
        for student_id in self._student_ids:
            for prof_id in self._professor_ids:
                if random.random() < evaluation_probability:
                    rows.append({
                        "student_registration_number":   student_id,
                        "professor_registration_number": prof_id,
                        "grade": round(random.uniform(1.0, 10.0), 2),
                    })
```

#### Source Code
```python
    def generateEvaluations(
        self,
        evaluation_probability: float = 0.40,
    ) -> pd.DataFrame:
        if not (0.0 <= evaluation_probability <= 1.0):
            raise ValueError("evaluation_probability must be between 0.0 and 1.0.")

        rows: list[dict] = []

        for student_id in self._student_ids:
            for prof_id in self._professor_ids:
                if random.random() < evaluation_probability:
                    rows.append({
                        "student_registration_number":   student_id,
                        "professor_registration_number": prof_id,
                        "grade": round(random.uniform(1.0, 10.0), 2),
                    })

        return pd.DataFrame(rows)
```

### generateEvaluationComments

**Primary Library:** `pandas`  
**Purpose:** Produces EvaluationComments rows for the given evaluations.

#### Overview
Maps generated evaluation reviews taking probability filters to dictate whether individual evaluation instances get contextual string comment data attached. Uses randomized templates to emulate realistic feedback formats.

#### Signature
```python
def generateEvaluationComments(self, evaluations_df: pd.DataFrame, max_comments_per_eval: int = 3, comment_probability: float = 0.70) -> pd.DataFrame
```

#### Parameters
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| evaluations_df | pd.DataFrame | Yes | — | Output of generateEvaluations() |
| max_comments_per_eval | int | No | 3 | Upper bound on comments attached |
| comment_probability | float | No | 0.70 | Probability metric per evaluation |

#### Returns
| Type | Description |
|------|-------------|
| pd.DataFrame | Structure detailing comment instances attached to student-prof mappings |

#### Raises
| Exception | Condition |
|-----------|-----------|
| ValueError | Input `DataFrame` lacks data entirely, or percentages cross bounds |

#### Dependencies
* **Required Libraries:** `pandas`, `random`

#### Workflow (Executable Logic Only)

**Phase 1: Probability Attachment Matrix**
Iterates data table objects directly parsing existing structural ties.
* **Operation 1:** Scrutinizes arguments throwing errors against null tables or incorrect percentage bounds.
* **Operation 2:** Initializes numerical identification counter `comment_id`.
* **Operation 3:** Traverses `evaluations_df.iterrows()` using `random.random()` probability validation to jump `continue` or proceed parsing.
* **Operation 4:** Distributes random `n_comments` per review, parsing random choice values `_COMMENT_TEMPLATES`. Records generated mapping rows, increments identification variable tracking unique components.

*Code Context:*
```python
        for _, eval_row in evaluations_df.iterrows():
            if random.random() > comment_probability:
                continue

            n_comments = random.randint(1, max(1, max_comments_per_eval))
            for _ in range(n_comments):
                rows.append({
                    "comment_id":                    comment_id,
                    "student_registration_number":   eval_row["student_registration_number"],
                    "professor_registration_number": eval_row["professor_registration_number"],
                    "comment_text":                  random.choice(self._COMMENT_TEMPLATES),
                })
                comment_id += 1
```

#### Source Code
```python
    def generateEvaluationComments(
        self,
        evaluations_df:      pd.DataFrame,
        max_comments_per_eval: int = 3,
        comment_probability: float = 0.70,
    ) -> pd.DataFrame:
        if evaluations_df.empty:
            raise ValueError("evaluations_df must not be empty.")
        if not (0.0 <= comment_probability <= 1.0):
            raise ValueError("comment_probability must be between 0.0 and 1.0.")

        rows: list[dict] = []
        comment_id = 1

        for _, eval_row in evaluations_df.iterrows():
            if random.random() > comment_probability:
                continue  # This evaluation receives no comments.

            n_comments = random.randint(1, max(1, max_comments_per_eval))
            for _ in range(n_comments):
                rows.append({
                    "comment_id":                    comment_id,
                    "student_registration_number":   eval_row["student_registration_number"],
                    "professor_registration_number": eval_row["professor_registration_number"],
                    "comment_text":                  random.choice(self._COMMENT_TEMPLATES),
                })
                comment_id += 1

        return pd.DataFrame(rows)
```
