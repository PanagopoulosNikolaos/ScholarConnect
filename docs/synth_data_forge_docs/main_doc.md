# main.py Documentation

## Navigation Table

| Name | Type | Description |
|------|------|-------------|
| [main](#main) | Function | Generates all ScholarConnect tables and prints a row-count summary. |

## Overview
This file serves as the entry point for synthetic data generation in the ScholarConnect project. It instantiates generators in foreign-key dependency order to create all seven tables. The script functions as a quick smoke-test that confirms the package is wired correctly by printing a summary row count.

## Detailed Breakdown

### main

**Signature:**
```python
def main() -> None
```

**Purpose:** Generates all ScholarConnect tables and prints a row-count summary.

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| None | None | No | — | Takes no arguments |

**Returns:**
| Type | Description |
|------|-------------|
| None | Returns nothing |

**Source Code:**
```python
def main() -> None:
    # Standalone entity tables

    students_df   = StudentGenerator(seed=SEED).generate(n=N_STUDENTS)
    professors_df = ProfessorGenerator(seed=SEED).generate(n=N_PROFESSORS)
    courses_df    = CourseGenerator(seed=SEED).generate(n=N_COURSES)

    # Relationship / junction tables

    rel_gen = RelationshipGenerator(
        students_df=students_df,
        professors_df=professors_df,
        courses_df=courses_df,
        seed=SEED,
    )

    teaching_df   = rel_gen.generateTeaching(max_courses_per_prof=4)
    enrollments_df = rel_gen.generateEnrollments(
        min_courses_per_student=2,
        max_courses_per_student=7,
        grade_null_probability=0.10,
    )
    evaluations_df = rel_gen.generateEvaluations(evaluation_probability=0.35)
    comments_df    = rel_gen.generateEvaluationComments(
        evaluations_df=evaluations_df,
        max_comments_per_eval=3,
        comment_probability=0.65,
    )

    # Summary

    table_summary = {
        "Students":             students_df,
        "Professors":           professors_df,
        "Courses":              courses_df,
        "TeachingAssignments":  teaching_df,
        "Enrollments":          enrollments_df,
        "ProfessorEvaluations": evaluations_df,
        "EvaluationComments":   comments_df,
    }

    print("\n--- ScholarConnect Synthetic Data Summary ---")
    for table_name, df in table_summary.items():
        print(f"  {table_name:<25} {len(df):>6} rows")
    print("--------------------------------------------\n")
    # save dataset to "./data"
    for table_name, df in table_summary.items():
            df.to_csv(f"./data/{table_name}.csv", index=False)
```

**Implementation (Executable Logic Only):**
* **Line 0:** `def main() -> None:` — Entry point definition.
* **Line 4:** `students_df = StudentGenerator(seed=SEED).generate(n=N_STUDENTS)` — Generates the students dataframe.
* **Line 5:** `professors_df = ProfessorGenerator(seed=SEED).generate(n=N_PROFESSORS)` — Generates the professors dataframe.
* **Line 6:** `courses_df = CourseGenerator(seed=SEED).generate(n=N_COURSES)` — Generates the courses dataframe.
* **Line 10:** `rel_gen = RelationshipGenerator(...)` — Initializes the relationship generator with generated entities.
* **Line 17:** `teaching_df = rel_gen.generateTeaching(...)` — Generates teaching assignments.
* **Line 18:** `enrollments_df = rel_gen.generateEnrollments(...)` — Generates student enrollments.
* **Line 23:** `evaluations_df = rel_gen.generateEvaluations(...)` — Generates professor evaluations.
* **Line 24:** `comments_df = rel_gen.generateEvaluationComments(...)` — Generates comments for the evaluations.
* **Line 32:** `table_summary = {...}` — Aggregates all dataframes into a dictionary.
* **Line 43:** `print("\n--- ScholarConnect Synthetic Data Summary ---")` — Prints the summary header.
* **Line 44:** `for table_name, df in table_summary.items():` — Iterates through the dataframes to print their row counts.
* **Line 47:** `for table_name, df in table_summary.items():` — Iterates through the dataframes to save them.
* **Line 48:** `df.to_csv(...)` — Saves each dataframe to a CSV file in the data directory.

**Dependencies:**
| Symbol | Kind | Purpose | Source |
|--------|------|---------|--------|
| StudentGenerator | Internal | Student data generation | synth_data_forge.synthetic_data_generator |
| ProfessorGenerator | Internal | Professor data generation | synth_data_forge.synthetic_data_generator |
| CourseGenerator | Internal | Course data generation | synth_data_forge.synthetic_data_generator |
| RelationshipGenerator | Internal | Relationship data generation | synth_data_forge.synthetic_data_generator |
