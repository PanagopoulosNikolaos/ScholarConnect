# enrollments.py Documentation

## Navigation Table

| Name | Type | Description |
|------|------|-------------|
| [buildEnrollmentsPage](#buildenrollmentspage) | Function | Renders the Enrollment Management page with a full CRUD interface. |
| [_renderTable](#_rendertable) | Function | Clears and re-renders the enrollments data table inside the given container. |
| [_openAddDialog](#_openadddialog) | Function | Opens the Add Enrollment modal dialog with live student and course options. |
| [_submit](#_submit) | Function | Calls addEnrollment and refreshes the table on success within add dialog. |
| [_openEditDialog](#_openeditdialog) | Function | Opens the Edit Enrollment dialog pre-populated with row data. |
| [_submit](#_submit-1) | Function | Calls updateEnrollment with the new start date and refreshes the table within edit dialog. |
| [_openDeleteDialog](#_opendeletedialog) | Function | Opens the Delete confirmation dialog for the selected enrollment. |
| [_confirm](#_confirm) | Function | Calls deleteEnrollment and refreshes the table within delete dialog. |
| [_buildEmptyState](#_buildemptystate) | Function | Renders a centered empty-state placeholder when no records exist. |

## Overview
Coordinates the enrollment management interface enabling authorized users to associate students with specific courses. Renders an interactive table exhibiting existing relations, enforces access controls ensuring students only review their distinct enrollments, and provides comprehensive administrative CRUD operations connected to standard interface models.

## Detailed Breakdown Section

### buildEnrollmentsPage

**Signature:**
```python
def buildEnrollmentsPage() -> None
```

**Purpose:** Renders the Enrollment Management page with a full CRUD interface.

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| None | — | — | — | — |

**Returns:**
| Type | Description |
|------|-------------|
| None | Instantiates UI structural framework on the page. |

**Source Code:**
```python
def buildEnrollmentsPage() -> None:
    buildSidebar()

    with ui.column().classes("w-full min-h-screen bg-[#0a0d14] p-8 gap-6"):
        with ui.row().classes("w-full items-center justify-between"):
            with ui.column().classes("gap-1"):
                ui.label("Enrollments").classes(
                    "text-white font-bold text-3xl tracking-tight"
                )
                ui.label("Manage student course enrollments.").classes(
                    "text-white/40 text-sm"
                )
            role = app.storage.user.get("user_role", "student")
            if role == "admin":
                ui.button(
                    "Add Enrollment",
                    icon="add",
                    on_click=lambda: _openAddDialog(table_container),
                ).classes(
                    "bg-indigo-600 hover:bg-indigo-500 text-white rounded-xl "
                    "px-5 py-2 no-uppercase font-medium transition-colors duration-200"
                )

        table_container = ui.column().classes("w-full")
        _renderTable(table_container)
```

**Implementation (Executable Logic Only):**
* **Line 2:** Calls `buildSidebar()` to provide navigation structure.
* **Line 13-14:** Fetches `user_role` and conditionally checks for `admin` status.
* **Line 15-22:** If administrative privileges are present, initializes an interactive 'Add Enrollment' button mapped to instantiate the creation modal via `_openAddDialog`.
* **Line 24-25:** Declares the `table_container` element and executes data-loading logic by invoking `_renderTable`.

**Dependencies:**
| Symbol | Kind | Purpose | Source |
|--------|------|---------|--------|
| buildSidebar | Internal | Menu layout structure | src.app.ui.components.sidebar |
| _renderTable | Internal | Data fetching and table drawing | enrollments.py |

---

### _renderTable

**Primary Library:** `nicegui`
**Purpose:** Clears and re-renders the enrollments data table inside the given container.

#### Overview
Builds the table grid responsible for displaying student-course links. Actuates role-based filtering mechanics to restrict standard user context while compiling the dataset, before wrapping output in standard styling wrappers and wiring slot-driven administrative tools.

#### Signature
```python
def _renderTable(container: ui.column) -> None
```

#### Parameters
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| container | ui.column | Yes | — | The NiceGUI column element acting as the table mount point. |

#### Returns
| Type | Description |
|------|-------------|
| None | Performs UI modification side-effects. |

#### Dependencies
* **Required Libraries:** `nicegui` (UI rendering)
* **Internal Modules:** `listEnrollments` (Data fetching), `_buildEmptyState` (Layout placeholder)

#### Workflow (Executable Logic Only)

**Phase 1: Filter Logic Setup**
Reconstructs output based on scope.
* **Operation 1:** Clears existing `container` hierarchy.
* **Operation 2:** Evaluates local `role` context. Obtains total list via `listEnrollments()`.
* **Operation 3:** Initiates list comprehension shrinking `enrollments` down to only items corresponding to `AM_Student == user_am` when `role` equals `"student"`.

**Phase 2: Visual Table Generation**
Constructs table interface logic.
* **Operation 1:** Identifies emptiness and draws `_buildEmptyState()` if applicable, returning immediately.
* **Operation 2:** Instantiates styled outer structure with dynamic counts text (`len(enrollments)`). 
* **Operation 3:** Instantiates standard filtered `ui.table` utilizing `row_key="AM_Student"`.

**Phase 3: Administrative Extensions**
Supplies control interfaces solely to administrative accounts.
* **Operation 1:** Assesses if `role` is "admin".
* **Operation 2:** Employs `.add_slot` with raw Vue template HTML for 'edit' and 'delete' buttons on custom event loops.
* **Operation 3:** Pushes "Actions" struct into `.columns` list dynamically and establishes Python hooks onto `.on("edit", ...)` to open respective configuration dialogs.

#### Source Code
```python
def _renderTable(container: ui.column) -> None:
    container.clear()
    
    role = app.storage.user.get("user_role", "student")
    user_am = app.storage.user.get("user_am", "")
    
    enrollments = listEnrollments()
    
    if role == "student":
        enrollments = [e for e in enrollments if e["AM_Student"] == user_am]

    with container:
        if not enrollments:
            _buildEmptyState("No enrollments found. Add one to get started.")
            return

        with ui.card().classes(
            "w-full bg-[#161b27] border border-white/5 rounded-2xl p-0 overflow-hidden"
        ):
            with ui.row().classes(
                "w-full items-center justify-between px-6 py-4 "
                "bg-[#0f1117] border-b border-white/5"
            ):
                ui.label(f"All Enrollments ({len(enrollments)})").classes(
                    "text-white font-semibold text-base"
                )
                search = ui.input(placeholder="Search...").props(
                    "dense outlined dark"
                ).classes(
                    "bg-white/5 text-white/80 rounded-lg text-sm border border-white/10 w-56"
                )

            table = ui.table(
                columns=ENROLLMENT_COLUMNS,
                rows=enrollments,
                row_key="AM_Student",
                pagination={"rowsPerPage": 10},
            ).classes("w-full text-white/80 text-sm").props("dark flat")

            search.bind_value(table, "filter")

            if role == "admin":
                table.add_slot(
                    "body-cell-actions",
                    "<q-td :props='props'>"
                    "  <q-btn flat round dense icon='edit' color='indigo-4'"
                    "    @click=\"$parent.$emit('edit', props.row)\" />"
                    "  <q-btn flat round dense icon='delete' color='red-4'"
                    "    @click=\"$parent.$emit('delete', props.row)\" />"
                    "</q-td>",
                )
                table.columns.append(
                    {"name": "actions", "label": "Actions", "field": "actions", "align": "center"}
                )

                table.on("edit", lambda e: _openEditDialog(e.args, container))
                table.on("delete", lambda e: _openDeleteDialog(e.args, container))
```
