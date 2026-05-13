# professors.py Documentation

## Navigation Table

| Name | Type | Description |
|------|------|-------------|
| [buildProfessorsPage](#buildprofessorspage) | Function | Renders the Professor Management page with a full CRUD interface. |
| [_renderTable](#_rendertable) | Function | Clears and re-renders the professors data table inside the given container. |
| [_openAddDialog](#_openadddialog) | Function | Opens the Add Professor modal dialog. |
| [_submit](#_submit) | Function | Calls addProfessor and refreshes the table on success within add dialog. |
| [_openEditDialog](#_openeditdialog) | Function | Opens the Edit Professor modal dialog pre-populated with row data. |
| [_submit](#_submit-1) | Function | Calls updateProfessor with changed fields and refreshes the table within edit dialog. |
| [_openDeleteDialog](#_opendeletedialog) | Function | Opens the Delete confirmation dialog for the selected professor. |
| [_confirm](#_confirm) | Function | Calls deleteProfessor and refreshes the table within delete dialog. |
| [_buildEmptyState](#_buildemptystate) | Function | Renders a centered empty-state placeholder when no records exist. |

## Overview
Serves the instructor entity management view within ScholarConnect. Retrieves and displays faculty records in a tabulated structure, integrating secure creation, modification, and deletion dialogs specifically limited to administrative users. Operates exclusively via asynchronous modal interactions to prevent page refreshing.

## Detailed Breakdown Section

### buildProfessorsPage

**Signature:**
```python
def buildProfessorsPage() -> None
```

**Purpose:** Renders the Professor Management page with a full CRUD interface.

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| None | — | — | — | — |

**Returns:**
| Type | Description |
|------|-------------|
| None | Instantiates UI structures directly. |

**Source Code:**
```python
def buildProfessorsPage() -> None:
    buildSidebar()

    with ui.column().classes("w-full min-h-screen bg-[#0a0d14] p-8 gap-6"):
        with ui.row().classes("w-full items-center justify-between"):
            with ui.column().classes("gap-1"):
                ui.label("Professors").classes(
                    "text-white font-bold text-3xl tracking-tight"
                )
                ui.label("Manage instructor records.").classes(
                    "text-white/40 text-sm"
                )
            role = app.storage.user.get("user_role", "student")
            if role == "admin":
                ui.button(
                    "Add Professor",
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
* **Line 2:** Executes `buildSidebar()`.
* **Line 13-14:** Checks user session for administrative privileges.
* **Line 15-23:** Generates the 'Add Professor' action button bound to `_openAddDialog` if authorized.
* **Line 25-26:** Creates an empty reference container and invokes `_renderTable`.

**Dependencies:**
| Symbol | Kind | Purpose | Source |
|--------|------|---------|--------|
| buildSidebar | Internal | Menu layout | src.app.ui.components.sidebar |
| _renderTable | Internal | Data loading | professors.py |

---

### _renderTable

**Primary Library:** `nicegui`
**Purpose:** Clears and re-renders the professors data table inside the given container.

#### Overview
Constitutes the core visual generator for professor data. Fetches unstructured record lists, implements placeholder displays when empty, and configures the `ui.table` to map data models to predefined visual columns, while conditionally embedding Vue template action buttons for authorized accounts.

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
| None | Performs DOM injection. |

#### Dependencies
* **Required Libraries:** `nicegui` (UI rendering)
* **Internal Modules:** `listProfessors` (Data fetching), `_buildEmptyState` (Fallback layout)

#### Workflow (Executable Logic Only)

**Phase 1: Table Initialization**
* **Operation 1:** Clears `container` and fetches `professors` array.
* **Operation 2:** Evaluates length of `professors` and renders empty state if zero.
* **Operation 3:** Generates the dark-themed card wrapper containing the search input and total record count.

**Phase 2: Configuration and Action Emplacement**
* **Operation 1:** Initiates the `ui.table()` utilizing `PROFESSOR_COLUMNS` and binding `search.bind_value` for reactive filtering.
* **Operation 2:** Re-evaluates `role`. If "admin", uses `.add_slot` to insert raw HTML strings representing Vue icon buttons (`q-btn`) bound to custom Vue emission events (`@click=\"$parent.$emit('edit', props.row)\"`).
* **Operation 3:** Appends the "actions" field definition to `table.columns` to ensure correct grid spacing.
* **Operation 4:** Binds Python handlers via `.on()` to capture the Vue event emissions, passing the selected `e.args` (row dictionary) into `_openEditDialog` and `_openDeleteDialog`.

#### Source Code
```python
def _renderTable(container: ui.column) -> None:
    container.clear()
    professors = listProfessors()

    with container:
        if not professors:
            _buildEmptyState("No professors found. Add one to get started.")
            return

        with ui.card().classes(
            "w-full bg-[#161b27] border border-white/5 rounded-2xl p-0 overflow-hidden"
        ):
            with ui.row().classes(
                "w-full items-center justify-between px-6 py-4 "
                "bg-[#0f1117] border-b border-white/5"
            ):
                ui.label(f"All Professors ({len(professors)})").classes(
                    "text-white font-semibold text-base"
                )
                search = ui.input(placeholder="Search...").props(
                    "dense outlined dark"
                ).classes(
                    "bg-white/5 text-white/80 rounded-lg text-sm border border-white/10 w-56"
                )

            table = ui.table(
                columns=PROFESSOR_COLUMNS,
                rows=professors,
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
