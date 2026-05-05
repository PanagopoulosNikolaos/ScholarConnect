# seed_sqlite.py Documentation

## Navigation Table

| Name | Type | Description |
|------|------|-------------|
| [parseArgs](#parseargs) | Function | Parses command-line arguments for the SQLite seeding workflow. |
| [createSchema](#createschema) | Function | Creates database schema from a SQL file. |
| [loadTable](#loadtable) | Function | Loads a CSV file into one SQLite table. |
| [main](#main) | Function | Builds and seeds ScholarConnect SQLite database from local CSV files. |

## Overview
This file creates and seeds the local ScholarConnect SQLite database. It loads table definitions from `db/schema.sql`, clears existing rows in foreign-key-safe order, and imports CSV datasets from `data/`.

## Detailed Breakdown

### parseArgs

**Signature:**
```python
def parseArgs() -> argparse.Namespace
```

**Purpose:** Parses command-line arguments for the SQLite seeding workflow.

### createSchema

**Signature:**
```python
def createSchema(conn: sqlite3.Connection, schema_path: Path) -> None
```

**Purpose:** Creates database schema from a SQL file.

### loadTable

**Signature:**
```python
def loadTable(conn: sqlite3.Connection, table_name: str, csv_path: Path) -> int
```

**Purpose:** Loads a CSV file into one SQLite table and returns inserted row count.

### main

**Signature:**
```python
def main() -> None
```

**Purpose:** Builds and seeds ScholarConnect SQLite database from local CSV files.

## CLI Usage

```bash
conda run -n py14 python -m scripts.seed_sqlite --db-path db/scholarconnect.sqlite3
```

Optional arguments:

- `--schema-path` (default: `db/schema.sql`)
- `--data-dir` (default: `data`)
