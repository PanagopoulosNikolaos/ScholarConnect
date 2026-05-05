"""
seed_sqlite.py

Creates a SQLite database from db/schema.sql and loads generated CSV files
from ./data into the corresponding tables.
"""

from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path
import pandas as pd


TABLE_TO_CSV: dict[str, str] = {
    "Students": "Students.csv",
    "Professors": "Professors.csv",
    "Courses": "Courses.csv",
    "TeachingAssignments": "TeachingAssignments.csv",
    "Enrollments": "Enrollments.csv",
    "ProfessorEvaluations": "ProfessorEvaluations.csv",
    "EvaluationComments": "EvaluationComments.csv",
}

DELETE_ORDER: list[str] = [
    "EvaluationComments",
    "ProfessorEvaluations",
    "Enrollments",
    "TeachingAssignments",
    "Courses",
    "Professors",
    "Students",
]


def parseArgs() -> argparse.Namespace:
    """
    Parses command-line arguments for the SQLite seeding workflow.

    Returns:
        argparse.Namespace: Parsed CLI arguments.
    """
    parser = argparse.ArgumentParser(
        description="Create and seed ScholarConnect SQLite database.",
    )
    parser.add_argument(
        "--db-path",
        default="db/scholarconnect.sqlite3",
        help="Output SQLite database path.",
    )
    parser.add_argument(
        "--schema-path",
        default="db/schema.sql",
        help="Path to SQLite schema SQL file.",
    )
    parser.add_argument(
        "--data-dir",
        default="data",
        help="Directory containing CSV files produced by scripts.main.",
    )
    return parser.parse_args()


def createSchema(conn: sqlite3.Connection, schema_path: Path) -> None:
    """
    Creates database schema from a SQL file.

    Args:
        conn (sqlite3.Connection): Active SQLite connection.
        schema_path (Path): Path to the schema.sql file.
    """
    sql_text = schema_path.read_text(encoding="utf-8")
    conn.executescript(sql_text)


def loadTable(conn: sqlite3.Connection, table_name: str, csv_path: Path) -> int:
    """
    Loads a CSV file into one SQLite table.

    Args:
        conn (sqlite3.Connection): Active SQLite connection.
        table_name (str): Destination table name.
        csv_path (Path): Source CSV file path.

    Returns:
        int: Number of inserted rows.
    """
    data_frame = pd.read_csv(csv_path)
    data_frame.to_sql(table_name, conn, if_exists="append", index=False)
    return len(data_frame)


def main() -> None:
    """
    Builds and seeds ScholarConnect SQLite database from local CSV files.

    Returns:
        None
    """
    args = parseArgs()
    db_path = Path(args.db_path)
    schema_path = Path(args.schema_path)
    data_dir = Path(args.data_dir)

    if not schema_path.exists():
        raise FileNotFoundError(f"Schema file not found: {schema_path}")
    if not data_dir.exists():
        raise FileNotFoundError(f"Data directory not found: {data_dir}")

    db_path.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(db_path) as conn:
        conn.execute("PRAGMA foreign_keys = ON;")
        createSchema(conn=conn, schema_path=schema_path)
        with conn:
            for table_name in DELETE_ORDER:
                conn.execute(f"DELETE FROM {table_name};")

            inserted_counts: dict[str, int] = {}
            for table_name, csv_name in TABLE_TO_CSV.items():
                csv_path = data_dir / csv_name
                if not csv_path.exists():
                    raise FileNotFoundError(f"CSV file not found: {csv_path}")
                inserted_counts[table_name] = loadTable(
                    conn=conn,
                    table_name=table_name,
                    csv_path=csv_path,
                )

    print("\n--- ScholarConnect SQLite Seed Summary ---")
    print(f"  DB file: {db_path}")
    for table_name, count in inserted_counts.items():
        print(f"  {table_name:<25} {count:>6} rows")
    print("------------------------------------------\n")


if __name__ == "__main__":
    main()
