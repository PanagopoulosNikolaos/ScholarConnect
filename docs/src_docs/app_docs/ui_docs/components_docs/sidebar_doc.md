# sidebar.py Documentation

## Navigation Table

| Name | Type | Description |
|------|------|-------------|
| [buildSidebar](#buildsidebar) | Function | Constructs the application's left-hand navigation drawer. |
| [_buildNavLink](#_buildnavlink) | Function | Renders a single navigation link row inside the sidebar. |
| [_buildNavRow](#_buildnavrow) | Function | Renders a styled clickable row used for both nav links and the logout action. |
| [_handleLogout](#_handlelogout) | Function | Clears the user session and redirects to the login page. |

## Overview
Provides a reusable left-hand navigation sidebar component for the ScholarConnect web application. Responsible for rendering the application brand header, generating dynamic primary navigation links, and maintaining a persistent logout button anchored at the bottom of the drawer.

## Detailed Breakdown Section

### buildSidebar

**Primary Library:** `nicegui`
**Purpose:** Constructs the application's left-hand navigation drawer.

#### Overview
Assembles the main structural component of the left-side navigation system. Creates a flexbox column to house branding elements, a central dynamic list of navigational route options, and a fixed lower section for session termination. Implements structural styling specifically avoiding `fixed=True` to allow proper integration with Quasar's automatic layout offsetting mechanics.

#### Signature
```python
def buildSidebar() -> None
```

#### Parameters
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| None | — | — | — | — |

#### Returns
| Type | Description |
|------|-------------|
| None | Appends structural elements to the active NiceGUI page context. |

#### Dependencies
* **Required Libraries:** `nicegui` (UI rendering)
* **Internal Modules:** `_buildNavLink` (Link rendering), `_buildNavRow` (Button structure), `_handleLogout` (Session termination)

#### Workflow (Executable Logic Only)

**Phase 1: Drawer Initialization**
Creates the main vertical container for the sidebar.
* **Operation 1:** Initiates `ui.left_drawer()` applying `.classes("bg-transparent flex flex-col")` and `.style("min-width: 260px; width: 260px")` to establish a fixed-width, vertical flex container with a transparent background intended to layer over global glassmorphism effects.

**Phase 2: Branding Section**
Constructs the visual header.
* **Operation 1:** Generates a nested column with `items-center py-8 px-4 gap-1` classes.
* **Operation 2:** Emplaces the 'school' icon, main title text ("ScholarConnect"), and a descriptive subtitle.
* **Operation 3:** Adds a subtle visual separator utilizing a low-opacity `ui.separator()`.

**Phase 3: Route Generation**
Defines and iterates over the available application paths.
* **Operation 1:** Retrieves the user role from session storage (defaulting to 'student').
* **Operation 2:** Initializes a list of tuples containing the Material icon string, display label, and target path.
* **Operation 3:** Opens a flexible column (`flex-1`) allowing this section to expand, pushing subsequent elements downward. Iterates over the `nav_items` list, invoking `_buildNavLink` for each entry.

**Phase 4: Session Control Area**
Creates the static footer section for logout.
* **Operation 1:** Appends a final separator.
* **Operation 2:** Invokes `_buildNavRow` hardcoded with the 'logout' action, marked as dangerous (`danger=True`) to alter visual signaling.

#### Source Code
```python
def buildSidebar() -> None:
    with ui.left_drawer().classes(
        "bg-transparent flex flex-col"
    ).style("min-width: 260px; width: 260px"):
        with ui.column().classes("items-center py-8 px-4 gap-1"):
            ui.icon("school", size="3rem").classes("text-indigo-400 drop-shadow-lg")
            ui.label("ScholarConnect").classes(
                "text-white font-extrabold text-xl tracking-tight mt-2"
            )
            ui.label("Academic Portal").classes("text-indigo-200/60 text-xs font-semibold uppercase tracking-widest")

        ui.separator().classes("opacity-10 mx-4 my-2")

        role = app.storage.user.get("user_role", "student")
        nav_items = [
            ("dashboard", "Dashboard", "/dashboard"),
            ("group", "Students", "/students"),
            ("person", "Professors", "/professors"),
            ("menu_book", "Courses", "/courses"),
            ("assignment", "Enrollments", "/enrollments"),
            ("star_rate", "Evaluations", "/evaluations"),
        ]

        with ui.column().classes("flex-1 gap-1 px-3"):
            for icon_name, label_text, path in nav_items:
                _buildNavLink(icon_name, label_text, path)

        ui.separator().classes("opacity-10 mx-4 my-2")

        with ui.column().classes("px-3 pb-6"):
            _buildNavRow(
                icon_name="logout",
                label_text="Logout",
                on_click=_handleLogout,
                active=False,
                danger=True,
            )
```

---

### _buildNavLink

**Signature:**
```python
def _buildNavLink(icon_name: str, label_text: str, path: str) -> None
```

**Purpose:** Renders a single navigation link row inside the sidebar.

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| icon_name | str | Yes | — | The Material Design icon identifier string. |
| label_text | str | Yes | — | The human-readable label displayed next to the icon. |
| path | str | Yes | — | The NiceGUI router path the row navigates to on click. |

**Returns:**
| Type | Description |
|------|-------------|
| None | Component builder function. |

**Source Code:**
```python
def _buildNavLink(icon_name: str, label_text: str, path: str) -> None:
    current_path = ui.context.client.page.path if ui.context else "/"
    is_active = current_path == path
    _buildNavRow(
        icon_name=icon_name,
        label_text=label_text,
        on_click=lambda p=path: ui.navigate.to(p),
        active=is_active,
    )
```

**Implementation (Executable Logic Only):**
* **Line 2:** `current_path = ui.context.client.page.path if ui.context else "/"` — Determines the current URL context safely.
* **Line 3:** `is_active = current_path == path` — Computes boolean status indicating whether this specific link represents the currently active page.
* **Line 4:** `_buildNavRow(...)` — Delegates actual UI construction, mapping the click event to a navigational routing command utilizing `ui.navigate.to()`.

**Dependencies:**
| Symbol | Kind | Purpose | Source |
|--------|------|---------|--------|
| _buildNavRow | Internal | Layout generation | sidebar.py |
| ui.context | External | State interrogation | nicegui |

---

### _buildNavRow

**Primary Library:** `nicegui`
**Purpose:** Renders a styled clickable row used for both nav links and the logout action.

#### Overview
A generalized factory function responsible for the precise visual formatting of interactive list items. Resolves specific styling states (active highlight, danger mode, standard mode) by dynamically adjusting typography and container properties, achieving a highly polished interactive feel.

#### Signature
```python
def _buildNavRow(
    icon_name: str,
    label_text: str,
    on_click,
    active: bool = False,
    danger: bool = False,
) -> None
```

#### Parameters
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| icon_name | str | Yes | — | Material Design icon name. |
| label_text | str | Yes | — | Display text shown beside the icon. |
| on_click | Callable | Yes | — | Handler invoked when the row is clicked. |
| active | bool | No | False | Applies the active/selected highlight style when True. |
| danger | bool | No | False | Applies red danger styling (used for logout). |

#### Returns
| Type | Description |
|------|-------------|
| None | Emits structured DOM elements into parent context. |

#### Dependencies
* **Required Libraries:** `nicegui` (UI rendering)

#### Workflow (Executable Logic Only)

**Phase 1: State Evaluation and Style Selection**
Determines the correct CSS configuration based on provided boolean flags.
* **Operation 1:** Checks `danger`. If True, assigns red-tinted formatting classes including a background hover effect (`hover:bg-red-500/10`) and matching text/icon colors to signify destructive potential.
* **Operation 2:** If not dangerous, checks `active`. If True, applies an emphasis state consisting of a complex gradient background (`bg-gradient-to-r from-indigo-500/20 to-purple-500/10`), an outer shadow (`shadow-[0_0_15px_rgba(99,102,241,0.1)]`), and high-opacity indigo text styling.
* **Operation 3:** If neither condition applies, falls back to a default low-opacity idle state incorporating a subtle right-translation animation upon hover (`hover:translate-x-1`).

**Phase 2: Component Instantiation**
Applies calculated properties to DOM elements.
* **Operation 1:** Initializes `ui.row()` with the computed container classes and binds the provided `on_click` handler.
* **Operation 2:** Inserts the `ui.icon()` applying the resolved icon classes.
* **Operation 3:** Inserts the `ui.label()` applying the computed text styling.

#### Source Code
```python
def _buildNavRow(
    icon_name: str,
    label_text: str,
    on_click,
    active: bool = False,
    danger: bool = False,
) -> None:
    if danger:
        row_classes = (
            "w-full flex items-center gap-3 px-4 py-3 rounded-xl "
            "cursor-pointer transition-all duration-200 "
            "text-red-400 hover:bg-red-500/10"
        )
        icon_classes = "text-red-400"
        label_classes = "text-red-400 text-sm font-medium"
    elif active:
        row_classes = (
            "w-full flex items-center gap-3 px-4 py-3 rounded-xl "
            "cursor-pointer transition-all duration-300 "
            "bg-gradient-to-r from-indigo-500/20 to-purple-500/10 border border-indigo-500/30 shadow-[0_0_15px_rgba(99,102,241,0.1)]"
        )
        icon_classes = "text-indigo-300 drop-shadow-md"
        label_classes = "text-indigo-200 text-sm font-semibold tracking-wide"
    else:
        row_classes = (
            "w-full flex items-center gap-3 px-4 py-3 rounded-xl "
            "cursor-pointer transition-all duration-200 "
            "hover:bg-white/5 border border-transparent hover:translate-x-1"
        )
        icon_classes = "text-white/40 group-hover:text-white/80 transition-colors"
        label_classes = "text-white/50 text-sm font-medium hover:text-white/90 transition-colors"

    with ui.row().classes(row_classes).on("click", on_click):
        ui.icon(icon_name, size="1.2rem").classes(icon_classes)
        ui.label(label_text).classes(label_classes)
```

---

### _handleLogout

**Signature:**
```python
async def _handleLogout() -> None
```

**Purpose:** Clears the user session and redirects to the login page.

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| None | — | — | — | — |

**Returns:**
| Type | Description |
|------|-------------|
| None | Executes session state mutations. |

**Source Code:**
```python
async def _handleLogout() -> None:
    app.storage.user.pop("authenticated", None)
    app.storage.user.pop("user_am", None)
    app.storage.user.pop("user_role", None)
    ui.navigate.to("/")
```

**Implementation (Executable Logic Only):**
* **Line 2-4:** Extracts and discards key authentication identifiers (`authenticated`, `user_am`, `user_role`) from the NiceGUI server-side user storage dictionary utilizing `.pop(key, None)` to prevent raising KeyErrors if already absent.
* **Line 5:** Issues a routing command redirecting the client browser back to the root application path.
