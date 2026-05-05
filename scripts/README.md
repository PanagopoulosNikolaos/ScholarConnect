## Directory Summary
The `scripts` directory contains utility scripts for the ScholarConnect project, primarily the synthetic data generation engine. It orchestrates the creation of a complete, relational synthetic dataset including students, professors, courses, and their interactions.

## Documentation Index
- [`__init__.py`](../docs/scripts_docs/__init___doc.md) — Public API for the ScholarConnect synthetic-data package.
- [`main.py`](../docs/scripts_docs/main_doc.md) — Entry point script that orchestrates the full data generation workflow.
- [`seed_sqlite.py`](../docs/scripts_docs/seed_sqlite_doc.md) — Creates and seeds the local SQLite database from `db/schema.sql` and generated CSVs.
- [`synthetic_data_generator/`](synthetic_data_generator/README.md) — Subdirectory containing individual generator classes for specific database tables.
