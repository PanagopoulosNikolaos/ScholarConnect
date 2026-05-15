## Directory Summary
The `db` directory contains the database schema definitions, Entity-Relationship Diagrams (ERD), and the local SQLite database file for ScholarConnect.

## Documentation Index
- [`schema.sql`](schema.sql) — The SQL DDL for creating the database tables and constraints.
- [`diagrams.md`](diagrams.md) — Visual documentation of the database schema using Mermaid diagrams.
- [`high_level_erd.mmd`](high_level_erd.mmd) — High-level Mermaid ERD source file.
- [`logical_schema.mmd`](logical_schema.mmd) — Logical schema Mermaid source file.

## Database File
- `scholarconnect.sqlite3` — The local SQLite database (created via `scripts/seed_sqlite.py`). This file is ignored by version control.
