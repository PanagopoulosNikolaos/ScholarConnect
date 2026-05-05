# ScholarConnect

ScholarConnect is a centralized academic management platform designed to streamline interactions between students and teachers. The system focuses on robust data management, automated grading, and a seamless user experience.



---

## Getting Started

To get started with the project, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/PanagopoulosNikolaos/ScholarConnect.git
    ```
2.  **Install dependencies:**
    ```bash
    conda run -n py14 pip install -r requirements.txt
    ```
3.  **Generate synthetic datasets (using conda env `py14`):**
    ```bash
    conda run -n py14 python -m scripts.main
    ```
4.  **Create and seed SQLite database:**
    ```bash
    conda run -n py14 python -m scripts.seed_sqlite --db-path db/scholarconnect.sqlite3
    ```
5.  **Explore the Documentation:**
    - [Database Schema](db/schema.md)
    - [SQLite Schema SQL](db/schema.sql)
    - [Development Plan](plan/plan.md)
    - [UI Plan](plan/ui_plan.md)

## Technologies Used

- **Backend:** Python, FastAPI, SQLAlchemy
- **Database:** SQLite
- **Data Engineering:** Pandas, Faker, NumPy
- **Frontend:** Python TUI (planned), with optional future web API + frontend split

## Planned UI Approach (MVP)

The first interactive client will be a **Python TUI (terminal UI)** focused on:

1. Login
2. Logout
3. Manual account creation

This keeps the learning curve low while still delivering a real user flow on top of SQLite.

---

*Note: This project is currently under active development.*
