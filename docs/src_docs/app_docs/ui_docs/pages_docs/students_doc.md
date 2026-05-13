# students.py Documentation

## Navigation Table

| Name | Type | Description |
|------|------|-------------|
| [buildStudentsPage](#buildstudentspage) | Function | Renders the Student Management page with a full CRUD interface. |
| [_renderTable](#_rendertable) | Function | Clears and re-renders the students data table inside the given container. |
| [_openAddDialog](#_openadddialog) | Function | Opens the Add Student modal dialog. |
| [_submit](#_submit) | Function | Calls addStudent and refreshes the table on success within add dialog. |
| [_openEditDialog](#_openeditdialog) | Function | Opens the Edit Student modal dialog pre-populated with row data. |
| [_submit](#_submit-1) | Function | Calls updateStudent with changed fields and refreshes the table within edit dialog. |
| [_openDeleteDialog](#_opendeletedialog) | Function | Opens the Delete confirmation dialog for the selected student. |
| [_confirm](#_confirm) | Function | Calls deleteStudent and refreshes the table within delete dialog. |
| [_buildEmptyState](#_buildemptystate) | Function | Renders a centered empty-state placeholder when no records exist. |

## Overview
Represents the student administration view. Provides the core UI for fetching, searching, and managing student accounts. Wraps API operations inside graphical modal dialogs, preventing page navigation events while performing CRUD actions, strictly gating interactive modification pathways to administrative sessions.

## Detailed Breakdown Section

### buildStudentsPage

**Signature:**
```python
def buildStudentsPage() -> None
```

**Purpose:** Renders the Student Management page with a full CRUD interface.

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| None | — | — | — | — |

**Returns:**
| Type | Description |
|------|-------------|
| None | Modifies structural page layout context. |

**Source Code:**
```python
def buildStudentsPage() -> None:
    buildSidebar()

    with ui.column().classes("w-full min-h-screen bg-[#0a0d14] p-8 gap-6"):
        with ui.row().classes("w-full items-center justify-between"):
            with ui.column().classes("gap-1"):
                ui.label("Students").classes(
                    "text-white font-bold text-3xl tracking-tight"
                )
                ui.label("Manage student records.").classes(
                    "text-white/40 text-sm"
                )
            role = app.storage.user.get("user_role", "student")
            if role == "admin":
                ui.button(
                    "Add Student",
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
* **Line 2:** Renders `buildSidebar()`.
* **Line 13-14:** Checks user role validation.
* **Line 15-23:** Generates action button tied to `_openAddDialog` restricted to admins.
* **Line 25-26:** Defines and passes the `table_container` target frame to `_renderTable`.

**Dependencies:**
| Symbol | Kind | Purpose | Source |
|--------|------|---------|--------|
| buildSidebar | Internal | Menu layout | src.app.ui.components.sidebar |
| _renderTable | Internal | Data loading | students.py |

---

### _renderTable

**Primary Library:** `nicegui`
**Purpose:** Clears and re-renders the students data table inside the given container.

#### Overview
Fetches and structures the primary user dataset. Manages empty states, configures the frontend search indexing logic, applies layout restrictions, and programmatically injects Vue template nodes into the table hierarchy to surface backend destructive actions safely.

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
| None | Performs rendering side effects. |

#### Dependencies
* **Required Libraries:** `nicegui` (UI rendering)
* **Internal Modules:** `listStudents` (Dataset extraction), `_buildEmptyState` (Fallback layout)

#### Workflow (Executable Logic Only)

**Phase 1: Table Initialization**
* **Operation 1:** Purges `container` children.
* **Operation 2:** Resolves the student list via `listStudents()`. Identifies empty conditions triggering `_buildEmptyState()`.
* **Operation 3:** Generates visual framing including search input components.

**Phase 2: Configuration and Action Emplacement**
* **Operation 1:** Instantiates the `ui.table()` connecting static definitions (`STUDENT_COLUMNS`) and dynamic data arrays (`students`). Attaches `search.bind_value`.
* **Operation 2:** Re-evaluates administrative status. Upon success, appends standard Vue `<q-td>` cells enclosing edit and delete `<q-btn>` blocks via `.add_slot`.
* **Operation 3:** Ensures graphical column headers remain aligned by appending to `table.columns`.
* **Operation 4:** Binds interaction closures to `.on("edit")` and `.on("delete")` invoking dialog methods sequentially.

#### Source Code
```python
def _renderTable(container: ui.column) -> None:
    container.clear()
    students = listStudents()

    with container:
        if not students:
            _buildEmptyState("No students found. Add one to get started.")
            return

        with ui.card().classes(
            "w-full bg-[#161b27] border border-white/5 rounded-2xl p-0 overflow-hidden"
        ):
            with ui.row().classes(
                "w-full items-center justify-between px-6 py-4 "
                "bg-[#0f1117] border-b border-white/5"
            ):
                ui.label(f"All Students ({len(students)})").classes(
                    "text-white font-semibold text-base"
                )
                search = ui.input(placeholder="Search...").props(
                    "dense outlined dark"
                ).classes(
                    "bg-white/5 text-white/80 rounded-lg text-sm border border-white/10 w-56"
                )

            table = ui.table(
                columns=STUDENT_COLUMNS,
                rows=students,
                row_key="AM",
                pagination={"rowsPerPage": 10},
            ).classes("w-full text-white/80 text-sm").props("dark flat")

            search.bind_value(table, "filter")

            role = app.storage.user.get("user_role", "student")
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
