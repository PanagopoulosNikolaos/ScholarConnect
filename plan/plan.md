# ScholarConnect Development Plan

This document outlines the strategic roadmap for ScholarConnect, a comprehensive platform designed to bridge the gap between students, teachers, and academic resources through a robust data-driven approach.

---

## Phase 1: Database Initialization
**Objective:** Establish a solid foundation for data storage and relational integrity.

| Task | Description | Status |
| :--- | :--- | :--- |
| **SQL Schema Implementation** | Create the DDL script to define tables for `Students`, `Instructors`, `Courses`, `Enrollments`, and `Evaluations`. | Completed |
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
| **Course CRUD Actions** | Data-access functions for creating, reading, updating, and deleting course records. | Completed |
| **Enrollment CRUD Actions** | Data-access functions for enrollments (join table with grade). | Completed |
| **Evaluation CRUD Actions** | Data-access functions for evaluations/reviews. | Completed |
| **Course Management Logic** | Logic for assigning professors to courses and enrolling students. | Completed |
| **Password Hashing** | Hash passwords on insert/update in student and professor CRUD actions (bcrypt/passlib). | Team Mate |

---

## Phase 4: UI Implementation
**Objective:** Deliver a user-facing interface via NiceGUI (web-based).

Chosen framework: **NiceGUI** — simplest path to a functional web UI that can call `api_actions/` functions directly without building an HTTP API layer.

| Task | Description | Status |
| :--- | :--- | :--- |
| **UI Preview Prototype** | Functional NiceGUI preview with dashboard, CRUD tables for all entities, sidebar navigation, and dark mode. | Completed |
| **Authentication Screens** | Login/register/logout flows with session management. | Pending |
| **UI Hardening** | Input validation, error handling, UX polish. | Pending |
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