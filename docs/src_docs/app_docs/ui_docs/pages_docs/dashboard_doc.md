# dashboard.py Documentation

## Navigation Table

| Name | Type | Description |
|------|------|-------------|
| [buildDashboardPage](#builddashboardpage) | Function | Renders the dashboard page layout with statistics cards and navigation. |
| [_buildMetricGrid](#_buildmetricgrid) | Function | Renders a responsive grid of KPI metric cards. |
| [_buildMetricCard](#_buildmetriccard) | Function | Renders a single KPI metric card. |
| [_buildQuickActions](#_buildquickactions) | Function | Renders the quick-action shortcut cards below the KPI grid. |

## Overview
Provides the central dashboard view for the ScholarConnect web application. Responsible for gathering aggregate statistics across multiple database entities, calculating conditional metrics based on the user's operational role, and displaying this data through a grid of metric cards. Incorporates context-sensitive shortcut buttons facilitating quick navigation to primary management tasks.

## Detailed Breakdown Section

### buildDashboardPage

**Primary Library:** `nicegui`
**Purpose:** Renders the dashboard page layout with statistics cards and navigation.

#### Overview
Serves as the main orchestrator for the dashboard interface. Executes preliminary data fetching from the API actions layer to calculate key performance indicators, applies filtering logic relative to the current user's role (admin, professor, or student), and delegates UI rendering to specialized internal rendering sub-functions.

#### Signature
```python
def buildDashboardPage() -> None
```

#### Parameters
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| None | — | — | — | — |

#### Returns
| Type | Description |
|------|-------------|
| None | Modifies the active page context. |

#### Dependencies
* **Required Libraries:** `nicegui` (UI rendering)
* **Internal Modules:** `listStudents`, `listProfessors`, `listCourses`, `listEnrollments`, `listEvaluations`, `getStudent`, `getProfessor` (Database queries), `buildSidebar`, `_buildMetricGrid`, `_buildQuickActions` (UI generation)

#### Workflow (Executable Logic Only)

**Phase 1: Data Accumulation**
Gathers unadulterated dataset states.
* **Operation 1:** Executes list-fetching functions across the primary domain models to acquire absolute counts.

**Phase 2: Role-Based Computation**
Isolates relevant records according to security context.
* **Operation 1:** Extracts `role` and `user_am` from `app.storage.user`.
* **Operation 2:** Evaluates `role`. If "student", filters enrollments and evaluations strictly matching the `AM_Student` key.
* **Operation 3:** If "professor", filters evaluations matching `AM_Instructor`.
* **Operation 4:** Computes `avg_rating` by iterating through filtered evaluations, extracting valid ratings, summing them, and dividing by total count, rounding to a single decimal place. Defends against division-by-zero errors.

**Phase 3: Page Rendering**
Generates the structural layout and dynamic header.
* **Operation 1:** Emplaces the navigation sidebar.
* **Operation 2:** Determines a `display_name` by querying the specific user entity table based on their role to append the individual's First and Last name.
* **Operation 3:** Renders headers and executes `_buildMetricGrid` utilizing the calculated list lengths and averages.
* **Operation 4:** Invokes `_buildQuickActions()`.

#### Source Code
```python
def buildDashboardPage() -> None:
    students = listStudents()
    professors = listProfessors()
    courses = listCourses()
    enrollments = listEnrollments()
    evaluations = listEvaluations()

    role = app.storage.user.get("user_role", "student")
    user_am = app.storage.user.get("user_am", "")
    
    my_enrollments = enrollments
    my_evals = evaluations
    
    if role == "student":
        my_enrollments = [e for e in enrollments if e["AM_Student"] == user_am]
        my_evals = [e for e in evaluations if e["AM_Student"] == user_am]
    elif role == "professor":
        my_evals = [e for e in evaluations if e["AM_Instructor"] == user_am]

    ratings = [e["Rating"] for e in my_evals if e.get("Rating") is not None]
    avg_rating = round(sum(ratings) / len(ratings), 1) if ratings else 0.0

    buildSidebar()

    with ui.column().classes("w-full min-h-screen bg-transparent p-8 gap-8"):
        with ui.column().classes("gap-1"):
            display_name = user_am
            if role == "student":
                rec = getStudent(user_am)
                if rec:
                    display_name = f"{rec.get('FirstName', '')} {rec.get('LastName', '')} ({user_am})"
            elif role == "professor":
                rec = getProfessor(user_am)
                if rec:
                    display_name = f"{rec.get('FirstName', '')} {rec.get('LastName', '')} ({user_am})"
            elif role == "admin":
                display_name = "Administrator"

            ui.label(f"Welcome, {display_name}").classes(
                "text-indigo-400 font-semibold text-sm uppercase tracking-wider mb-[-4px]"
            )
            ui.label("Dashboard").classes(
                "text-white font-bold text-3xl tracking-tight"
            )
            ui.label("System overview and key metrics.").classes(
                "text-white/40 text-sm"
            )

        _buildMetricGrid(
            students=len(students),
            professors=len(professors),
            courses=len(courses),
            enrollments=len(my_enrollments),
            evaluations=len(my_evals),
            avg_rating=avg_rating,
        )

        _buildQuickActions()
```

---

### _buildMetricGrid

**Signature:**
```python
def _buildMetricGrid(
    students: int,
    professors: int,
    courses: int,
    enrollments: int,
    evaluations: int,
    avg_rating: float,
) -> None
```

**Purpose:** Renders a responsive grid of KPI metric cards.

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| students | int | Yes | — | Total number of student records. |
| professors | int | Yes | — | Total number of instructor records. |
| courses | int | Yes | — | Total number of course records. |
| enrollments | int | Yes | — | Total number of enrollment records. |
| evaluations | int | Yes | — | Total number of evaluation records. |
| avg_rating | float | Yes | — | Average rating across all evaluations. |

**Returns:**
| Type | Description |
|------|-------------|
| None | Instantiates UI structures. |

**Source Code:**
```python
def _buildMetricGrid(
    students: int,
    professors: int,
    courses: int,
    enrollments: int,
    evaluations: int,
    avg_rating: float,
) -> None:
    cards = [
        ("group", str(students), "Students", "#6366f1", "/students"),
        ("person", str(professors), "Professors", "#8b5cf6", "/professors"),
        ("menu_book", str(courses), "Courses", "#3b82f6", "/courses"),
        ("assignment", str(enrollments), "Enrollments", "#06b6d4", "/enrollments"),
        ("star_rate", str(evaluations), "Evaluations", "#f59e0b", "/evaluations"),
        ("trending_up", str(avg_rating), "Avg. Rating", "#10b981", None),
    ]

    with ui.grid(columns=3).classes("w-full gap-4"):
        for icon_name, value, label, color, path in cards:
            _buildMetricCard(icon_name, value, label, color, path)
```

**Implementation (Executable Logic Only):**
* **Line 9-16:** Packages the primitive metrics into a structured list of configuration tuples, mapping each semantic value to an explicit icon, label string, color hex code, and destination route.
* **Line 18:** Initiates a CSS grid container defining a fixed three-column layout.
* **Line 19-20:** Iterates over the configurations, delegating the physical generation to `_buildMetricCard()`.

**Dependencies:**
| Symbol | Kind | Purpose | Source |
|--------|------|---------|--------|
| _buildMetricCard | Internal | UI card instantiation | dashboard.py |

---

### _buildMetricCard

**Primary Library:** `nicegui`
**Purpose:** Renders a single KPI metric card.

#### Overview
Implements a highly styled, reusable informational tile. Configures hover states dynamically dependent on navigability, applying glassmorphism borders (`backdrop-blur-md`), drop shadows, and specific hex-color integrations to denote category association visually.

#### Signature
```python
def _buildMetricCard(
    icon_name: str,
    value: str,
    label: str,
    accent_color: str,
    path: str | None,
) -> None
```

#### Parameters
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| icon_name | str | Yes | — | Material Design icon identifier. |
| value | str | Yes | — | The metric value to display prominently. |
| label | str | Yes | — | The human-readable metric description. |
| accent_color | str | Yes | — | Hex color string for the icon and accent border. |
| path | str \| None | Yes | — | Router path to navigate to on click, or None to disable navigation. |

#### Returns
| Type | Description |
|------|-------------|
| None | Adds styled components to the current view. |

#### Dependencies
* **Required Libraries:** `nicegui` (UI rendering)

#### Workflow (Executable Logic Only)

**Phase 1: Dynamic Style Computation**
Resolves interaction states based on routing properties.
* **Operation 1:** Constructs `cursor_class` containing cursor interaction utilities only if `path` evaluates as True.
* **Operation 2:** Initializes a `ui.card()` passing complex background opacities (`rgba(22,27,39,0.5)`), applying the computed `cursor_class`, and enforcing an inline `style` rule applying a solid top-border incorporating the specific `accent_color`.

**Phase 2: Event Binding and Formatting**
Wires actions and inserts inner elements.
* **Operation 1:** Registers a click event redirecting to `path` if defined.
* **Operation 2:** Creates an internal row layout. Renders a customized div container colored with a low-opacity version of the accent color to encase the primary icon.
* **Operation 3:** Embeds the string `value` applying large typography scale (`text-4xl`), tracking adjustments, and drop shadows to establish data hierarchy, followed by the standardized uppercase sub-label.

#### Source Code
```python
def _buildMetricCard(
    icon_name: str,
    value: str,
    label: str,
    accent_color: str,
    path: str | None,
) -> None:
    cursor_class = "cursor-pointer hover:border-white/20" if path else ""

    card = ui.card().classes(
        f"bg-[rgba(22,27,39,0.5)] border border-white/5 rounded-2xl p-6 "
        f"transition-all duration-200 {cursor_class} hover-lift "
        f"hover:bg-[rgba(28,34,53,0.7)] backdrop-blur-md"
    ).style(f"border-top: 2px solid {accent_color}60")
    if path:
        card.on("click", lambda p=path: ui.navigate.to(p))
    with card:
        with ui.row().classes("items-center gap-4 w-full"):
            with ui.element("div").classes(
                "rounded-xl p-3 flex items-center justify-center"
            ).style(f"background: {accent_color}18"):
                ui.icon(icon_name, size="1.8rem").style(f"color: {accent_color}")

            with ui.column().classes("gap-0"):
                ui.label(value).classes(
                    "text-white font-bold text-4xl leading-tight tracking-tight drop-shadow-md"
                )
                ui.label(label).classes("text-white/60 text-sm font-medium uppercase tracking-wider mt-1")
```

---

### _buildQuickActions

**Primary Library:** `nicegui`
**Purpose:** Renders the quick-action shortcut cards below the KPI grid.

#### Overview
Provides context-aware functional endpoints. Inspects the user's role to supply a tailored list of operational links represented as horizontal cards, ensuring an administrator has access to creation workflows while a student receives enrollment pathways.

#### Signature
```python
def _buildQuickActions() -> None
```

#### Parameters
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| None | — | — | — | — |

#### Returns
| Type | Description |
|------|-------------|
| None | Alters page layout with interaction buttons. |

#### Dependencies
* **Required Libraries:** `nicegui` (UI rendering)

#### Workflow (Executable Logic Only)

**Phase 1: Action Resolution**
Constructs appropriate functionality map.
* **Operation 1:** Retrieves `user_role` from session storage.
* **Operation 2:** Evaluates conditional blocks appending tuples (icon, title, description, URL path) to the `actions` array corresponding to the privileges associated with admin, professor, or student roles.

**Phase 2: Card Iteration and Instantiation**
Draws the cards within a structural grid.
* **Operation 1:** Initializes a 4-column grid.
* **Operation 2:** Loops across the configured `actions` array. Instantiates `ui.card()`, applying specific hover interaction aesthetics (`hover:border-indigo-500/50`) and binding navigation lambda callbacks. 
* **Operation 3:** Emplaces the descriptive icon, title text, and supplemental description inside each card scope.

#### Source Code
```python
def _buildQuickActions() -> None:
    ui.label("Quick Actions").classes(
        "text-white font-semibold text-lg mt-2"
    )

    role = app.storage.user.get("user_role", "student")

    actions = []
    if role == "admin":
        actions.extend([
            ("group_add", "Add Student", "Register a new student record.", "/students"),
            ("person_add", "Add Professor", "Onboard a new instructor.", "/professors"),
            ("library_add", "Add Course", "Create a new course offering.", "/courses"),
            ("playlist_add", "Add Enrollment", "Enroll a student in a course.", "/enrollments"),
        ])
    elif role == "professor":
        actions.extend([
            ("library_add", "Add Course", "Create a new course offering.", "/courses"),
            ("star_rate", "Add Evaluation", "Grade a student.", "/evaluations"),
        ])
    else:
        actions.extend([
            ("playlist_add", "Enroll in Course", "Join a new class.", "/courses"),
            ("star_rate", "Add Evaluation", "Evaluate a course/instructor.", "/evaluations"),
        ])

    with ui.grid(columns=4).classes("w-full gap-4"):
        for icon_name, title, desc, path in actions:
            card = ui.card().classes(
                "bg-[rgba(22,27,39,0.5)] border border-white/5 rounded-2xl p-6 "
                "cursor-pointer hover:bg-[rgba(28,34,53,0.7)] hover:border-indigo-500/50 "
                "transition-all duration-200 hover-lift backdrop-blur-md"
            )
            card.on("click", lambda p=path: ui.navigate.to(p))
            with card:
                ui.icon(icon_name, size="1.5rem").classes("text-indigo-400 mb-2")
                ui.label(title).classes(
                    "text-white font-semibold text-sm"
                )
                ui.label(desc).classes("text-white/40 text-xs mt-1")
```
