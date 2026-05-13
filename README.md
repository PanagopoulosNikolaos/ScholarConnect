# ScholarConnect

ScholarConnect is a centralized academic management platform designed to streamline interactions between students and teachers. 

---

## Getting Started

> Conda or Virtual Enviroment recommended as faker cannot be installed on the root environment.
> `sudo apt install python3-faker` will fail.

#### Conda docs: [Documentation](https://docs.conda.io/en/latest/miniconda.html)
#### Python Virtual Enviroment docs: [Documentation](https://docs.python.org/3/library/venv.html)
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
5.  **Run the Web Application:**
    ```bash
    conda run -n py14 python -m src.app.ui.main
    ```
    - The app will be available at `http://localhost:8080`.
    - **Admin Login:** Use `admin` for both AM/Username and Password to access the full platform.

6.  **Explore the Documentation:**
    - [Database Schema](db/schema.md)
    - [SQLite Schema SQL](db/schema.sql)
    - [Development Plan](plan/plan.md)
    - [UI Plan](plan/ui_plan.md)

## Technologies Used

- **Backend:** Python, sqlite3
- **Database:** SQLite
- **Data Engineering:** Pandas, Faker
- **Frontend:** NiceGUI (Web-based)



*Note: This project is currently under active development.*
