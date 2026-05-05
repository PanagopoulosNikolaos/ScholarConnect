# ScholarConnect UI Plan (Base)

## Goal

Deliver a very simple interactive client for SQLite-backed authentication flows:

1. Manual account creation
2. Login
3. Logout

## Chosen Direction

Build a **Python TUI (terminal user interface)** as the MVP.

Reasoning:
- Lower complexity than web (no browser/frontend stack).
- Better UX than plain shell prompts.
- Easy to run for all team members through conda (`py14`).

## Scope (MVP)

### In Scope
- Account creation form
- Login form
- Logout action
- Basic authenticated home screen
- SQLite persistence
- Password hashing and verification

### Out of Scope (for now)
- Full course management flows
- Rich dashboards/charts
- HTTP API and browser frontend
- Role-based authorization matrix

## Proposed Structure

```
src/
  app/
    tui/
      main.py
      screens/
        welcome_screen.py
        login_screen.py
        register_screen.py
        home_screen.py
    services/
      auth_service.py
      account_service.py
    db/
      sqlite.py
      queries.py
```

## Data Strategy

- Use SQLite (`db/scholarconnect.sqlite3`) as the source of truth.
- Keep login lookups on indexed unique fields (`username`, `email`).
- Use parameterized SQL only.
- Keep a simple in-memory session object for current logged-in user in the TUI process.

## Auth Rules (MVP)

- Account creation requires:
  - unique username
  - unique email
  - password with minimum length
- Login accepts username + password.
- Passwords are never stored in plain text.
- Logout clears the in-memory session state.

## Implementation Phases

1. **Foundation**
   - Add UI dependencies and app entry point.
   - Add DB connection helper and query module.
2. **Auth Services**
   - Implement create account, login verification, logout/session handling.
3. **TUI Screens**
   - Build welcome/login/register/home screens and navigation.
4. **Hardening**
   - Input validation, clear error messages, and basic smoke tests.
5. **Docs**
   - Update root README with run instructions and UX flow.

## Run Target (planned)

```bash
conda run -n py14 python -m src.app.tui.main
```

## Notes

- Keep UI logic and DB/auth logic separated from day one.
- TUI-first does not block future migration to web; service modules can be reused behind an API later.
