# evaluations.py Documentation

## Navigation Table

| Name | Type | Description |
|------|------|-------------|
| [buildEvaluationsPage](#buildevaluationspage) | Function | Renders the Evaluation Management page with a full CRUD interface. |
| [_renderTable](#_rendertable) | Function | Clears and re-renders the evaluations data table inside the given container. |
| [_openAddDialog](#_openadddialog) | Function | Opens the Add Evaluation modal dialog with live entity option lists. |
| [_submit](#_submit) | Function | Calls addEvaluation and refreshes the table on success within add dialog. |
| [_openEditDialog](#_openeditdialog) | Function | Opens the Edit Evaluation dialog pre-populated with row data. |
| [_submit](#_submit-1) | Function | Calls updateEvaluation with changed fields and refreshes the table within edit dialog. |
| [_openDeleteDialog](#_opendeletedialog) | Function | Opens the Delete confirmation dialog for the selected evaluation. |
| [_confirm](#_confirm) | Function | Calls deleteEvaluation and refreshes the table within delete dialog. |
| [_buildEmptyState](#_buildemptystate) | Function | Renders a centered empty-state placeholder when no records exist. |

## Overview
Defines the management page for academic evaluations within the ScholarConnect platform. Provides sophisticated role-restricted filtering mapping professors to their subjects and students to their enrollments, displaying data within a searchable table characterized by visually impactful, color-coded grading badges. Encapsulates logic for invoking complex modal structures for evaluation insertion and modification.

## Detailed Breakdown Section

### _renderTable

**Primary Library:** `nicegui`
**Purpose:** Clears and re-renders the evaluations data table inside the given container.

#### Overview
Executes comprehensive rendering parameters regarding student reviews. Manages three-tier role filtering (admin, student, professor) logic prior to constructing the data view. Inserts specialized Vue template structures utilizing ternary coloring logic to instantly categorize review states visually via integer bounds checking.

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
| None | Performs direct UI mutations. |

#### Dependencies
* **Required Libraries:** `nicegui` (UI rendering)
* **Internal Modules:** `listEvaluations` (Dataset population)

#### Workflow (Executable Logic Only)

**Phase 1: Dataset Population and Privilege Scoping**
Pulls data and restricts accessibility dynamically.
* **Operation 1:** Empties prior UI tree within `container`.
* **Operation 2:** Resolves current `role` and `user_am`. Fetches comprehensive evaluation data map via `listEvaluations()`.
* **Operation 3:** Applies exclusionary filters based on entity ID matches: student filtering checks `AM_Student`, while professor filtering restricts based on `AM_Instructor`. Administrator context receives unfiltered data naturally.

**Phase 2: Base UI Rendering**
Constructs table infrastructure logic.
* **Operation 1:** Triggers empty state render if evaluation array length evaluates to zero.
* **Operation 2:** Deploys standard application aesthetic wrappers and establishes standard configuration metrics (columns, row keys, paging rules).

**Phase 3: Color-Coded Grading Application**
Implements complex Vue string logic for the 'Rating' slot.
* **Operation 1:** Utilizes `table.add_slot("body-cell-Rating", ...)` to inject a raw template block over the rating integer column.
* **Operation 2:** Executes an inline Vue ternary operator (`props.value >= 7 ? 'green-8' : props.value >= 4 ? 'amber-8' : 'red-8'`) within the `color` attribute of `<q-badge>`. This mechanism assigns a distinct color classification based on absolute performance metrics immediately without relying on Python-side event processing or CSS overrides.

**Phase 4: Global Action Assignment**
Attaches universal modification pathways.
* **Operation 1:** Unlike other pages that restrict editing to admins, adds standard edit/delete action slots indiscriminately (evaluations logic permits self-modification).
* **Operation 2:** Sets action listening lambdas targeting the designated CRUD flow routines.

#### Source Code
```python
def _renderTable(container: ui.column) -> None:
    container.clear()
    
    role = app.storage.user.get("user_role", "student")
    user_am = app.storage.user.get("user_am", "")
    
    evaluations = listEvaluations()
    
    if role == "student":
        evaluations = [e for e in evaluations if e["AM_Student"] == user_am]
    elif role == "professor":
        evaluations = [e for e in evaluations if e["AM_Instructor"] == user_am]

    with container:
        if not evaluations:
            _buildEmptyState("No evaluations found. Add one to get started.")
            return

        with ui.card().classes(
            "w-full bg-[#161b27] border border-white/5 rounded-2xl p-0 overflow-hidden"
        ):
            with ui.row().classes(
                "w-full items-center justify-between px-6 py-4 "
                "bg-[#0f1117] border-b border-white/5"
            ):
                ui.label(f"All Evaluations ({len(evaluations)})").classes(
                    "text-white font-semibold text-base"
                )
                search = ui.input(placeholder="Search...").props(
                    "dense outlined dark"
                ).classes(
                    "bg-white/5 text-white/80 rounded-lg text-sm border border-white/10 w-56"
                )

            table = ui.table(
                columns=EVALUATION_COLUMNS,
                rows=evaluations,
                row_key="AM_Instructor",
                pagination={"rowsPerPage": 10},
            ).classes("w-full text-white/80 text-sm").props("dark flat")

            search.bind_value(table, "filter")

            table.add_slot(
                "body-cell-Rating",
                """
                <q-td :props='props'>
                  <q-badge
                    :color="props.value >= 7 ? 'green-8' : props.value >= 4 ? 'amber-8' : 'red-8'"
                    class="text-white font-bold px-2 py-1 rounded-lg text-xs"
                  >
                    {{ props.value }} / 10
                  </q-badge>
                </q-td>
                """,
            )

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

---

### _openAddDialog

**Primary Library:** `nicegui`
**Purpose:** Opens the Add Evaluation modal dialog with live entity option lists.

#### Overview
Computes highly specific relational arrays to limit the dropdown selections visible during evaluation creation. Ensures that a student may only evaluate professors for classes they actively attend, preventing irrelevant dataset manipulation. 

#### Signature
```python
def _openAddDialog(container: ui.column) -> None
```

#### Parameters
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| container | ui.column | Yes | — | The table container to refresh after success. |

#### Returns
| Type | Description |
|------|-------------|
| None | Actuates the UI context directly. |

#### Dependencies
* **Required Libraries:** `nicegui` (UI rendering)
* **Internal Modules:** `buildEvaluationDialog` (Modal factory), `listProfessors`, `listStudents`, `listCourses`, `listEnrollments` (Data fetching)

#### Workflow (Executable Logic Only)

**Phase 1: Base Fetching**
Extracts comprehensive lists.
* **Operation 1:** Initiates queries for standard domains (professors, students, courses).

**Phase 2: Relational Filtering (Student Logic)**
Narrows lists based on specific foreign-key associations.
* **Operation 1:** Restricts `students` selection strictly to the current user's profile.
* **Operation 2:** Parses `listEnrollments` to generate a subset `my_course_codes` detailing exclusively courses the student attends. Filters `courses` utilizing this subset.
* **Operation 3:** Derives `my_instructor_ams` from the narrowed `courses` set. Filters `professors` to include only those responsible for the user's specific sections.

**Phase 3: Relational Filtering (Professor Logic)**
* **Operation 1:** Restricts the instructor dropdown strictly to the active user profile, allowing any student/course mapping.

**Phase 4: Component Spawning**
Builds the modal via factory function.
* **Operation 1:** Constructs an embedded `_submit` method interfacing directly with `addEvaluation`.
* **Operation 2:** Opens the dialog created by `buildEvaluationDialog`.

#### Source Code
```python
def _openAddDialog(container: ui.column) -> None:
    professors = listProfessors()
    students = listStudents()
    courses = listCourses()
    
    role = app.storage.user.get("user_role", "student")
    user_am = app.storage.user.get("user_am", "")
    if role == "student":
        students = [s for s in students if s["AM"] == user_am]
        my_enrollments = [e for e in listEnrollments() if e["AM_Student"] == user_am]
        my_course_codes = {e["C_Code"] for e in my_enrollments}
        courses = [c for c in courses if c["C_Code"] in my_course_codes]
        my_instructor_ams = {c["AM_Instructor"] for c in courses if c.get("AM_Instructor")}
        professors = [p for p in professors if p["AM"] in my_instructor_ams]
    elif role == "professor":
        professors = [p for p in professors if p["AM"] == user_am]

    def _submit(data: dict) -> None:
        ok = addEvaluation(
            am_instructor=data["AM_Instructor"],
            am_student=data["AM_Student"],
            c_code=data["C_Code"],
            rating=data["Rating"],
            comments=data.get("Comments"),
        )
        if ok:
            ui.notify("Evaluation added successfully.", type="positive", position="top")
            _renderTable(container)
        else:
            ui.notify(
                "Failed to add evaluation. It may already exist for this combination.",
                type="negative",
                position="top",
            )

    dialog = buildEvaluationDialog(
        on_submit=_submit,
        instructor_options=professors,
        student_options=students,
        course_options=courses,
    )
    dialog.open()
```
