# ScholarConnect UI Plan (NiceGUI Web App)

## Goal

Deliver a responsive, rich web-based interface for the ScholarConnect platform, allowing users to manage academic data through a modern browser experience:

1.  **Dashboard**: High-level statistics and system overview.
2.  **Authentication**: Secure login, registration, and logout flows.
3.  **Data Management**: Full CRUD operations for Students, Instructors, Courses, Enrollments, and Evaluations.

## Chosen Direction

Build a **Web GUI** using **NiceGUI** (Python framework).

### Reasoning
- **Unified Stack**: Logic and UI are both written in Python, reducing context switching and deployment complexity.
- **Rich Components**: Built on top of Quasar and Vue.js, providing premium-feeling elements (tables, dialogs, charts) out of the box.
- **Fast Iteration**: Real-time reloading and direct access to backend `api_actions` without intermediate REST/GraphQL layers.
- **Responsive Design**: Mobile-friendly layouts by default.

## Scope

### In Scope
- **Interactive Dashboard**: Visual cards showing total counts of students, professors, and courses.
- **Entity Tables**: Searchable, sortable tables for all primary entities.
- **CRUD Dialogs**: Modal forms for adding and editing records with validation.
- **Authentication Flow**:
    - Dedicated Login and Registration pages.
    - Session-based access control.
    - Persistent logout action in the sidebar.
- **State Management**: Using `app.storage` for user sessions.

### Out of Scope
- **Complex Analytics**: Advanced data visualization or export (PDF/Excel).
- **Public API**: External HTTP access for third-party integrations.
- **Theme Customizer**: Allowing users to change primary colors (locked to dark mode for MVP).

## Proposed Structure

```text
src/
  app/
    ui/
      main.py           # Application entry point and routing
      pages/
        dashboard.py    # Main landing page
        auth.py         # Login and registration screens
        students.py     # Student management
        professors.py   # Instructor management
        courses.py      # Course and Enrollment management
      components/
        sidebar.py      # Shared navigation component
        forms.py        # Reusable form elements
        tables.py       # Customized data table wrappers
  api_actions/          # Backend business logic (shared logic)
  database.py           # SQLite connection management
```

## Data & Auth Strategy

- **Backend**: Direct calls to `src/api_actions/` modules.
- **Session**: Use `nicegui.app.storage.user` to track authentication status and AM (Identity).
- **Validation**: Client-side validation via NiceGUI component props (`rules`, `validation`) and server-side checks in service layers.
- **Persistence**: SQLite remains the source of truth; no client-side database caching.

## Implementation Phases

1.  **Foundation (Completed)**
    - Initialize NiceGUI and establish routing.
    - Build `ui_preview.py` prototype with Dashboard and basic CRUD tables.
2.  **Authentication & Security (Next)**
    - Implement `auth_service` for session handling.
    - Build Login/Register pages.
    - Add page-level decorators for access control.
3.  **Feature Parity & Refactoring**
    - Migrate logic from `ui_preview.py` into structured modules (`src/app/ui/pages/`).
    - Finalize Enrollments and Evaluations management screens.
4.  **UX Hardening**
    - Add meaningful notifications for all actions.
    - Implement confirmation dialogs for deletions.
    - Refine table column layouts and search filters.
5.  **Documentation**
    - Update root README with setup and run instructions for the web app.

## Run Target

```bash
conda run -n py14 python -m src.app.ui.main
```

## Notes

- The current `src/ui_preview.py` serves as the functional reference for the final modular implementation.
- All UI actions must handle database exceptions gracefully to prevent application crashes.
