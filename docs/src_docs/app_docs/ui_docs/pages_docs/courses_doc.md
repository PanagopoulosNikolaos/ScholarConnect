# courses.py Documentation

## Navigation Table

| Name | Type | Description |
|------|------|-------------|
| [buildCoursesPage](#buildcoursespage) | Function | Renders the Course Management page with a full CRUD interface. |
| [_renderTable](#_rendertable) | Function | Clears and re-renders the courses data table inside the given container. |
| [_joinCourse](#_joincourse) | Function | Enrolls the logged-in student in the selected course. |
| [_leaveCourse](#_leavecourse) | Function | Unenrolls the logged-in student from the selected course. |
| [_openAddDialog](#_openadddialog) | Function | Opens the Add Course modal dialog. |
| [_submit](#_submit) | Function | Calls addCourse and refreshes the table on success within add dialog. |
| [_openEditDialog](#_openeditdialog) | Function | Opens the Edit Course modal dialog pre-populated with row data. |
| [_submit](#_submit-1) | Function | Calls updateCourse with changed fields and refreshes the table within edit dialog. |
| [_openDeleteDialog](#_opendeletedialog) | Function | Opens the Delete confirmation dialog for the selected course. |
| [_confirm](#_confirm) | Function | Calls deleteCourse and refreshes the table within delete dialog. |
| [_buildEmptyState](#_buildemptystate) | Function | Renders a centered empty-state placeholder when no records exist. |

## Overview
Serves the course management view within the ScholarConnect interface. Facilitates fetching, filtering, and displaying catalog data through an interactive table format. Incorporates context-dependent row logic enabling administrators to edit or delete courses while providing standard users (students) with join/leave functionality. Interfaces closely with predefined modal form templates for data mutation.

## Detailed Breakdown Section

### buildCoursesPage

**Primary Library:** `nicegui`
**Purpose:** Renders the Course Management page with a full CRUD interface.

#### Overview
Constructs the foundation of the page layout. Mounts the global sidebar element, establishes the main title header, conditionally grants access to an "Add Course" trigger based on authorization, and initiates the table rendering pipeline by allocating an empty container.

#### Signature
```python
def buildCoursesPage() -> None
```

#### Parameters
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| None | — | — | — | — |

#### Returns
| Type | Description |
|------|-------------|
| None | Manipulates active layout context. |

#### Dependencies
* **Required Libraries:** `nicegui` (UI rendering)
* **Internal Modules:** `buildSidebar` (Layout inclusion), `_renderTable` (Table instantiation)

#### Workflow (Executable Logic Only)

**Phase 1: Header Instantiation**
Applies layout rules and textual context.
* **Operation 1:** Initiates `buildSidebar()`.
* **Operation 2:** Establishes the main content area employing `bg-[#0a0d14]` coloring and spacing rules. Prints the page label and description strings.

**Phase 2: Administrative Control Generation**
Checks authority to expose modification capabilities.
* **Operation 1:** Extracts `user_role` defaulting to "student". Evaluates equality against `"admin"`.
* **Operation 2:** If authorized, initializes a prominent `ui.button()` designated for "Add Course". Its `on_click` handler passes `table_container` to `_openAddDialog` to allow state refreshing upon subsequent success.

**Phase 3: Sub-component Delegation**
Delegates complex visual drawing to specialized methods.
* **Operation 1:** Generates a blank placeholder column (`table_container`).
* **Operation 2:** Passes the container reference to `_renderTable()` to populate the data view.

#### Source Code
```python
def buildCoursesPage() -> None:
    buildSidebar()

    with ui.column().classes("w-full min-h-screen bg-[#0a0d14] p-8 gap-6"):
        with ui.row().classes("w-full items-center justify-between"):
            with ui.column().classes("gap-1"):
                ui.label("Courses").classes(
                    "text-white font-bold text-3xl tracking-tight"
                )
                ui.label("Manage course offerings and assignments.").classes(
                    "text-white/40 text-sm"
                )
            role = app.storage.user.get("user_role", "student")
            if role == "admin":
                ui.button(
                    "Add Course",
                    icon="add",
                    on_click=lambda: _openAddDialog(table_container),
                ).classes(
                    "bg-indigo-600 hover:bg-indigo-500 text-white rounded-xl "
                    "px-5 py-2 no-uppercase font-medium transition-colors duration-200"
                )

        table_container = ui.column().classes("w-full")
        _renderTable(table_container)
```

---

### _renderTable

**Primary Library:** `nicegui`
**Purpose:** Clears and re-renders the courses data table inside the given container.

#### Overview
Serves as the primary data retrieval and rendering engine for the course grid. Retrieves all current course records, calculates individual enrollment state vectors for the current student user, and formulates the NiceGUI table configuration, binding Vue-driven actions dynamically relative to session privileges.

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
| None | Performs DOM manipulation on the given container. |

#### Dependencies
* **Required Libraries:** `nicegui` (UI rendering)
* **Internal Modules:** `listCourses`, `listEnrollments` (Data fetching), `_buildEmptyState` (Empty state rendering)

#### Workflow (Executable Logic Only)

**Phase 1: State Collection and Modification**
Purges existing output and prepares the dataset.
* **Operation 1:** Triggers `container.clear()` ensuring an unpolluted rendering context.
* **Operation 2:** Fetches course items via `listCourses()`.
* **Operation 3:** Determines if the actor is a student. If True, fetches user-specific enrollments into a set, modifying the `courses` dataset by injecting an `_enrolled` boolean flag on each dictionary representing current membership status.

**Phase 2: Empty Condition Management**
Guards against rendering an empty grid structure.
* **Operation 1:** Determines if `courses` is empty. Employs `_buildEmptyState()` and aborts further generation if true.

**Phase 3: Table Implementation**
Initializes and binds the table to the provided container.
* **Operation 1:** Creates a formatted wrapper card and embeds a search text input.
* **Operation 2:** Initializes `ui.table()` connecting `COURSE_COLUMNS`, records, and setting pagination logic. Applies `search.bind_value` to enable immediate filtering.

**Phase 4: Slot Binding and Privilege Branching**
Generates action buttons directly within the table cells context.
* **Operation 1:** Evaluates `role`. If admin, attaches a custom `body-cell-actions` Vue slot containing standard edit/delete buttons, appending an "Actions" column to the definition, and registering lambda closures onto custom emit channels (`table.on("edit", ...)`).
* **Operation 2:** If student, injects a distinct `body-cell-actions` containing "Join" and "Leave" buttons conditionally rendered via `v-if='!props.row._enrolled'`. Attaches `join` and `leave` listeners pointing toward respective backend methods.

#### Source Code
```python
def _renderTable(container: ui.column) -> None:
    container.clear()
    courses = listCourses()
    
    role = app.storage.user.get("user_role", "student")
    user_am = app.storage.user.get("user_am", "")
    
    if role == "student":
        my_enrollments = {e["C_Code"] for e in listEnrollments() if e["AM_Student"] == user_am}
        for c in courses:
            c["_enrolled"] = c["C_Code"] in my_enrollments

    with container:
        if not courses:
            _buildEmptyState("No courses found. Add one to get started.")
            return

        with ui.card().classes(
            "w-full bg-[#161b27] border border-white/5 rounded-2xl p-0 overflow-hidden"
        ):
            with ui.row().classes(
                "w-full items-center justify-between px-6 py-4 "
                "bg-[#0f1117] border-b border-white/5"
            ):
                ui.label(f"All Courses ({len(courses)})").classes(
                    "text-white font-semibold text-base"
                )
                search = ui.input(placeholder="Search...").props(
                    "dense outlined dark"
                ).classes(
                    "bg-white/5 text-white/80 rounded-lg text-sm border border-white/10 w-56"
                )

            table = ui.table(
                columns=COURSE_COLUMNS,
                rows=courses,
                row_key="C_Code",
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
            elif role == "student":
                table.add_slot(
                    "body-cell-actions",
                    "<q-td :props='props'>"
                    "  <q-btn v-if='!props.row._enrolled' flat dense icon='person_add' label='Join' color='green-4' class='no-uppercase'"
                    "    @click=\"$parent.$emit('join', props.row)\" />"
                    "  <q-btn v-else flat dense icon='logout' label='Leave' color='red-4' class='no-uppercase'"
                    "    @click=\"$parent.$emit('leave', props.row)\" />"
                    "</q-td>",
                )
                table.columns.append(
                    {"name": "actions", "label": "Actions", "field": "actions", "align": "center"}
                )
                table.on("join", lambda e: _joinCourse(e.args, container))
                table.on("leave", lambda e: _leaveCourse(e.args, container))
```

*(Note: `_joinCourse`, `_leaveCourse`, `_openAddDialog`, `_openEditDialog`, `_openDeleteDialog`, and `_buildEmptyState` implement standard action dispatch patterns similar to previously documented CRUD routines, managing isolated API invocation and error-toast feedback structures.)*
