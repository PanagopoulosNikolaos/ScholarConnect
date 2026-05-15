<p align="center">
  <img src="assets/Logo.png" alt="ScholarConnect Logo">
</p>

# ScholarConnect

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![NiceGUI](https://img.shields.io/badge/UI-NiceGUI-orange.svg)](https://nicegui.io/)
[![SQLite](https://img.shields.io/badge/Database-SQLite-003B57.svg)](https://www.sqlite.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

ScholarConnect is a centralized academic management platform designed to streamline interactions between students and teachers. It provides a premium, dark-themed interface for managing courses, enrollments, and academic evaluations.

---

## Getting Started

It is recommended to use a **Virtual Environment** or **Conda** to manage dependencies.

### 1. Installation
```bash
# Clone the repository
git clone https://github.com/PanagopoulosNikolaos/ScholarConnect.git
cd ScholarConnect

# Install dependencies
conda run -n py14 pip install -r requirements.txt
```

### 2. Data Initialization
```bash
# Generate synthetic datasets
conda run -n py14 python -m scripts.main

# Create and seed SQLite database
conda run -n py14 python -m scripts.seed_sqlite --db-path db/scholarconnect.sqlite3
```

### 3. Running the Application
```bash
conda run -n py14 python -m src.app.ui.main
```
- **Access:** Open `http://localhost:8080` in your browser.
- **Admin Login:** Use `admin` for both Username and Password.

---

## Technologies Used

- **Frontend:** [NiceGUI](https://nicegui.io/) (Premium Dark Mode, Glassmorphism)
- **Backend:** Python 3.10+
- **Database:** SQLite
- **Data Engineering:** Pandas, Faker

---

## Documentation
- [Database Schema](db/schema.md)
- [Development Plan](plan/plan.md)
- [Security Audit](plan/security_audit.md)
