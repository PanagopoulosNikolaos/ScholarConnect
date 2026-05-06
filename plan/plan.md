# ScholarConnect Development Plan

This document outlines the strategic roadmap for ScholarConnect, a comprehensive platform designed to bridge the gap between students, teachers, and academic resources through a robust data-driven approach.

---

## Phase 1: Database Initialization
**Objective:** Establish a solid foundation for data storage and relational integrity.

| Task | Description | Status |
| :--- | :--- | :--- |
| **SQL Schema Implementation** | Create the DDL script to define tables for `Students`, `Professors`, `Courses`, `Enrollments`, `TeachingAssignments`, `ProfessorEvaluations`, and `EvaluationComments`. | Completed |
| **Integrity Constraints** | Define primary/foreign keys and constraints (e.g., UNIQUE email, CHECK constraints for grades). | Completed |

---

## Phase 2: Data Engineering
**Objective:** Generate, validate, and prepare synthetic data for realistic system testing.

| Task | Description | Status |
| :--- | :--- | :--- |
| **Synthetic Data Generation** | Develop a Python script (using `Faker` or `NumPy`) in `scripts/` to generate realistic datasets for all entities. | Completed |
| **CSV Generation & Storage Pipeline** | Generate CSV files from generated DataFrames and write them to `./data/` for downstream seeding. | Completed |
| **Referential Integrity Check** | Ensure Foreign Key alignment across the generated CSV/JSON files. | Completed |
| **Data Validation Pipeline** | Implement a `pandas` script to clean, format, and verify the synthetic data. | Pending |
| **Schema Matching** | Validate data types and ensure the dataframe structure matches the SQL schema exactly. | Pending |

---

## Phase 3: Backend Development
**Objective:** Build the core logic and data-access infrastructure.

| Task | Description | Status |
| :--- | :--- | :--- |
| **Database Connection Helper** | Establish a reusable SQLite connection module with row-factory and foreign-key enforcement. | Completed |
| **Database Seeding** | Automate SQLite database creation and populate tables using validated DataFrames / CSV files. | Completed |
| **Seeding Order Optimization** | Ensure the seeding process respects table dependencies and relational constraints. | Completed |
| **Student CRUD Actions** | Data-access functions for creating, reading, updating, and deleting student records. | Completed |
| **Professor CRUD Actions** | Data-access functions for creating, reading, updating, and deleting professor records. | Completed |
| **Course CRUD Actions** | Data-access functions for creating, reading, updating, and deleting course records. | Pending |
| **Enrollment CRUD Actions** | Data-access functions for enrollments (join table with grade). | Pending |
| **Course Management Logic** | Logic for assigning professors to courses and enrolling students. | Pending |

---

## Phase 4: UI — Decision Pending
**Objective:** Deliver a user-facing interface.

> **No final decision has been made yet.** The team and PM need to agree on which direction to take. The `plan/ui_plan.md` file contains a TUI-only draft that may be scrapped or expanded once a decision is reached.
>
> **Options:**
> - **TUI (Terminal)** — Fastest MVP. Uses Python stdlib. Can call `api_actions/` functions directly — no HTTP API needed.
> - **GUI (Desktop, e.g. PyQt/Tkinter)** — More polished but heavier. Still calls Python directly.
> - **Web-app (FastAPI + React/etc.)** — Most flexible. Requires building REST endpoints and a frontend framework.

| Task | Description | Status |
| :--- | :--- | :--- |
| **UI Planning & Decision** | Meet with team and PM to decide on TUI / GUI / Web-app. | In Progress |
| **UI Implementation** | Build the chosen interface. | Pending |
| **Documentation Update** | Update root README with run instructions and UX flow. | Pending |

---

## Phase 5: Hardening & Handover (Other Team Members)
**Objective:** Polish, validate, and finalize the system for production readiness.

| Task | Description | Status |
| :--- | :--- | :--- |
| **Data Validation Pipeline** | Implement a `pandas` script to clean, format, and verify the synthetic data. | Pending |
| **Schema Matching** | Validate data types and ensure the dataframe structure matches the SQL schema exactly. | Pending |
| **Integration Testing** | Verify that UI actions correctly update the database and reflect in API responses. | Pending |
| **System Finalization** | Perform full-stack integration tests and bug fixes. | Pending |