# main.py Documentation

## Navigation Table

| Name | Type | Description |
|------|------|-------------|
| [_requireAuth](#_requireauth) | Function | Checks whether the current session is authenticated. |
| [_applyGlobalStyles](#_applyglobalstyles) | Function | Injects global CSS applied across all pages. |
| [loginPage](#loginpage) | Function | Serves the login page at the root path. |
| [registerPage](#registerpage) | Function | Serves the student self-registration page. |
| [dashboardPage](#dashboardpage) | Function | Serves the main dashboard page. |
| [studentsPage](#studentspage) | Function | Serves the Student Management page. |
| [professorsPage](#professorspage) | Function | Serves the Professor Management page. |
| [coursesPage](#coursespage) | Function | Serves the Course Management page. |
| [enrollmentsPage](#enrollmentspage) | Function | Serves the Enrollment Management page. |
| [evaluationsPage](#evaluationspage) | Function | Serves the Evaluation Management page. |

## Overview
Serves as the application entry point for the ScholarConnect web application. Configures global styling parameters, manages session authentication verification routing, defines application endpoints via decorators, and initializes the local server environment.

## Detailed Breakdown Section

### _requireAuth

**Signature:**
```python
def _requireAuth() -> bool
```

**Purpose:** Checks whether the current session is authenticated.

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| None | — | — | — | — |

**Returns:**
| Type | Description |
|------|-------------|
| bool | True if the user is authenticated, False otherwise. |

**Source Code:**
```python
def _requireAuth() -> bool:
    if not app.storage.user.get("authenticated"):
        ui.navigate.to("/")
        return False
    return True
```

**Implementation (Executable Logic Only):**
* **Line 2:** `if not app.storage.user.get("authenticated"):` — Inspects the session storage dictionary for a verified authentication flag.
* **Line 3:** `ui.navigate.to("/")` — Redirects unverified access attempts to the root login endpoint.
* **Line 4:** `return False` — Returns boolean False to block downstream function execution in the calling route.
* **Line 5:** `return True` — Returns True allowing the protected page logic to proceed.

**Dependencies:**
| Symbol | Kind | Purpose | Source |
|--------|------|---------|--------|
| app.storage.user | External | Session state verification | nicegui |
| ui.navigate.to | External | Browser redirection | nicegui |

---

### _applyGlobalStyles

**Primary Library:** `nicegui`
**Purpose:** Injects global CSS applied across all pages.

#### Overview
Establishes the foundational visual language of the application by embedding a global CSS stylesheet into the HTML `<head>`. Modifies native Quasar classes to align with premium dark-mode aesthetic goals, including custom font families, scrollbar dimensions, glassmorphism effects, and animation properties.

#### Signature
```python
def _applyGlobalStyles() -> None
```

#### Parameters
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| None | — | — | — | — |

#### Returns
| Type | Description |
|------|-------------|
| None | Injects styling blocks directly into the page context. |

#### Dependencies
* **Required Libraries:** `nicegui` (UI rendering)

#### Workflow (Executable Logic Only)

**Phase 1: Stylesheet Injection**
Appends raw CSS to the Document Object Model.
* **Operation 1:** Calls `ui.add_head_html()` passing a multiline string containing `<style>` tags.
* **Operation 2:** Defines font imports via `@import url(...)` connecting to Google Fonts for 'Inter' and 'Outfit' families.
* **Operation 3:** Applies global base styling (`body { ... }`) configuring a radial gradient background that transitions from `#111424` to `#0a0d14` using the `!important` flag to override framework defaults.
* **Operation 4:** Implements component-level overrides. The `q-drawer` styling utilizes `background: rgba(15, 17, 23, 0.7)` and `backdrop-filter: blur(12px)` to generate a semi-transparent glassmorphism visual effect over underlying elements.
* **Operation 5:** Implements table rendering rules (`.q-table__container`), establishing specific text opacity, border radii (`16px`), and interaction hover colors (`rgba(99,102,241,0.08)`) to maintain cohesive styling across dynamic datasets.

#### Source Code
```python
def _applyGlobalStyles() -> None:
    ui.add_head_html(
        """
        <style>
          @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Outfit:wght@400;500;600;700&display=swap');

          body {
            font-family: 'Inter', sans-serif;
            background: radial-gradient(circle at top right, #111424, #0a0d14 50%) !important;
            color: #e2e8f0;
            margin: 0;
            min-height: 100vh;
          }

          /* Headings premium font */
          h1, h2, h3, h4, h5, h6, .text-3xl, .text-lg {
            font-family: 'Outfit', sans-serif;
          }

          /* Scrollbar */
          ::-webkit-scrollbar { width: 8px; height: 8px; }
          ::-webkit-scrollbar-track { background: transparent; }
          ::-webkit-scrollbar-thumb { background: #2d3748; border-radius: 4px; }
          ::-webkit-scrollbar-thumb:hover { background: #4a5568; }

          /* NiceGUI overrides */
          .nicegui-content { padding: 0 !important; max-width: none !important; }
          
          /* Sidebar Glassmorphism */
          .q-drawer { 
            background: rgba(15, 17, 23, 0.7) !important;
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border-right: 1px solid rgba(255, 255, 255, 0.05) !important;
          }

          /* Remove Quasar button text-transform */
          .no-uppercase { text-transform: none !important; letter-spacing: normal !important; }

          /* Table premium dark theme overrides */
          .q-table__container { 
            background: rgba(22, 27, 39, 0.6) !important;
            backdrop-filter: blur(10px);
            border-radius: 16px;
            border: 1px solid rgba(255,255,255,0.05);
          }
          .q-table tbody tr:hover td { background: rgba(99,102,241,0.08) !important; }
          .q-table th { 
            color: rgba(255,255,255,0.4) !important; 
            font-weight: 600; 
            font-size: 0.75rem; 
            text-transform: uppercase; 
            letter-spacing: 0.08em; 
            border-bottom: 1px solid rgba(255,255,255,0.08) !important; 
          }
          .q-table td { 
            border-bottom: 1px solid rgba(255,255,255,0.04) !important; 
            color: rgba(255,255,255,0.85); 
          }

          /* Input premium overrides */
          .q-field--outlined .q-field__control { 
            background: rgba(255,255,255,0.03) !important; 
            border-radius: 12px;
            transition: all 0.3s ease;
          }
          .q-field__label { color: rgba(255,255,255,0.4) !important; }
          .q-field__native { color: rgba(255,255,255,0.95) !important; }
          .q-field--outlined .q-field__control:hover:before { border-color: rgba(99,102,241,0.4) !important; }
          .q-field--focused .q-field__control:before { 
            border-color: #6366f1 !important; 
            box-shadow: 0 0 0 2px rgba(99,102,241,0.2);
          }

          /* Notification premium positioning */
          .q-notification { 
            border-radius: 12px !important; 
            font-family: 'Inter', sans-serif !important; 
            background: rgba(22, 27, 39, 0.9) !important;
            backdrop-filter: blur(8px);
            border: 1px solid rgba(255,255,255,0.1);
          }
          
          /* Card hover animations */
          .hover-lift {
            transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
          }
          .hover-lift:hover {
            transform: translateY(-4px);
            box-shadow: 0 12px 24px -8px rgba(0,0,0,0.5);
          }
        </style>
        """
    )
```

---

### loginPage

**Primary Library:** `nicegui`
**Purpose:** Serves the login page at the root path.

#### Overview
Defines the primary access route (`/`). Applies base styling constraints and immediately inspects session status to dynamically bypass authentication for returning active users. Defers actual component rendering to a specialized builder module.

#### Signature
```python
@ui.page("/")
def loginPage() -> None
```

#### Parameters
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| None | — | — | — | — |

#### Returns
| Type | Description |
|------|-------------|
| None | Controls page rendering execution flow. |

#### Dependencies
* **Required Libraries:** `nicegui` (UI routing)
* **Internal Modules:** `_applyGlobalStyles` (Styling application), `buildLoginPage` (Page construction)

#### Workflow (Executable Logic Only)

**Phase 1: Environment Setup**
* **Operation 1:** Executes `_applyGlobalStyles()` to establish the foundational DOM constraints.

**Phase 2: Authentication Check**
* **Operation 1:** Inspects `app.storage.user.get("authenticated")`. If True, initiates a redirect to `/dashboard` via `ui.navigate.to()` and executes a `return` statement, aborting further generation of the login UI components.

**Phase 3: Render Delegation**
* **Operation 1:** If unauthenticated, calls `buildLoginPage()` to attach form structures to the active page context.

#### Source Code
```python
@ui.page("/")
def loginPage() -> None:
    _applyGlobalStyles()
    if app.storage.user.get("authenticated"):
        ui.navigate.to("/dashboard")
        return
    buildLoginPage()
```

---

### registerPage

**Signature:**
```python
@ui.page("/register")
def registerPage() -> None
```

**Purpose:** Serves the student self-registration page.

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| None | — | — | — | — |

**Returns:**
| Type | Description |
|------|-------------|
| None | Page rendering handler. |

**Source Code:**
```python
@ui.page("/register")
def registerPage() -> None:
    _applyGlobalStyles()
    buildRegisterPage()
```

**Implementation (Executable Logic Only):**
* **Line 1:** `@ui.page("/register")` — Associates function with URL endpoint.
* **Line 3:** `_applyGlobalStyles()` — Ensures consistent rendering.
* **Line 4:** `buildRegisterPage()` — Delegates component construction.

**Dependencies:**
| Symbol | Kind | Purpose | Source |
|--------|------|---------|--------|
| buildRegisterPage | Internal | UI generation | src.app.ui.pages.auth |

---

### dashboardPage

**Signature:**
```python
@ui.page("/dashboard")
def dashboardPage() -> None
```

**Purpose:** Serves the main dashboard page.

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| None | — | — | — | — |

**Returns:**
| Type | Description |
|------|-------------|
| None | Page rendering handler. |

**Source Code:**
```python
@ui.page("/dashboard")
def dashboardPage() -> None:
    _applyGlobalStyles()
    if not _requireAuth():
        return
    buildDashboardPage()
```

**Implementation (Executable Logic Only):**
* **Line 1:** `@ui.page("/dashboard")` — Maps route to handler.
* **Line 3:** `_applyGlobalStyles()` — Applies base DOM styling.
* **Line 4:** `if not _requireAuth(): return` — Verifies authentication state, aborting rendering if unauthenticated.
* **Line 6:** `buildDashboardPage()` — Executes the view builder.

**Dependencies:**
| Symbol | Kind | Purpose | Source |
|--------|------|---------|--------|
| _requireAuth | Internal | Access control guard | main.py |
| buildDashboardPage | Internal | UI Generation | src.app.ui.pages.dashboard |

*(Note: Similar standard implementations repeat for studentsPage, professorsPage, coursesPage, enrollmentsPage, and evaluationsPage)*
