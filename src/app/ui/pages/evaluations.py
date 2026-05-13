"""
src/app/ui/pages/evaluations.py

Evaluation management page for the ScholarConnect web application.
Provides a searchable table of all evaluation records with inline
Add, Edit, and Delete operations via modal dialogs.  Displays rating
values with color-coded badges for quick visual scanning.
"""

from nicegui import ui, app
from src.api_actions import (
    listEvaluations,
    listProfessors,
    listStudents,
    listCourses,
    addEvaluation,
    updateEvaluation,
    deleteEvaluation,
)
from src.app.ui.components.sidebar import buildSidebar
from src.app.ui.components.forms import buildEvaluationDialog, buildConfirmDialog


# Column definitions for the evaluations table.
EVALUATION_COLUMNS = [
    {"name": "AM_Instructor", "label": "Instructor AM", "field": "AM_Instructor", "sortable": True, "align": "left"},
    {"name": "AM_Student", "label": "Student AM", "field": "AM_Student", "sortable": True, "align": "left"},
    {"name": "C_Code", "label": "Course", "field": "C_Code", "sortable": True, "align": "left"},
    {"name": "Rating", "label": "Rating", "field": "Rating", "sortable": True, "align": "center"},
    {"name": "Comments", "label": "Comments", "field": "Comments", "sortable": False, "align": "left"},
]


def buildEvaluationsPage() -> None:
    """
    Renders the Evaluation Management page with a full CRUD interface.

    Displays the sidebar, page header with an Add Evaluation button, and a
    searchable data table.  The rating cell uses a color-coded badge scoped
    slot for visual clarity.
    """
    buildSidebar()

    with ui.column().classes("w-full min-h-screen bg-[#0a0d14] p-8 gap-6"):
        with ui.row().classes("w-full items-center justify-between"):
            with ui.column().classes("gap-1"):
                ui.label("Evaluations").classes(
                    "text-white font-bold text-3xl tracking-tight"
                )
                ui.label("Manage instructor evaluations of students.").classes(
                    "text-white/40 text-sm"
                )
            role = app.storage.user.get("user_role", "student")
            if role in ("admin", "professor"):
                ui.button(
                    "Add Evaluation",
                    icon="add",
                    on_click=lambda: _openAddDialog(table_container),
                ).classes(
                    "bg-indigo-600 hover:bg-indigo-500 text-white rounded-xl "
                    "px-5 py-2 no-uppercase font-medium transition-colors duration-200"
                )

        table_container = ui.column().classes("w-full")
        _renderTable(table_container)


def _renderTable(container: ui.column) -> None:
    """
    Clears and re-renders the evaluations data table inside the given container.

    Fetches the latest evaluation list, renders the styled table with a
    color-coded rating slot and edit/delete action buttons.

    Args:
        container (ui.column): The NiceGUI column element acting as the
            table mount point.
    """
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

            # Color-coded rating badge: green >= 7, yellow >= 4, red < 4.
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

            if role in ("admin", "professor"):
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


def _openAddDialog(container: ui.column) -> None:
    """
    Opens the Add Evaluation modal dialog with live entity option lists.

    Args:
        container (ui.column): The table container to refresh after success.
    """
    professors = listProfessors()
    students = listStudents()
    courses = listCourses()

    def _submit(data: dict) -> None:
        """Calls addEvaluation and refreshes the table on success."""
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


def _openEditDialog(row: dict, container: ui.column) -> None:
    """
    Opens the Edit Evaluation dialog pre-populated with row data.

    Only Rating and Comments are editable; the three ID fields are locked.

    Args:
        row (dict): The evaluation record dict selected for editing.
        container (ui.column): The table container to refresh after success.
    """
    professors = listProfessors()
    students = listStudents()
    courses = listCourses()

    def _submit(data: dict) -> None:
        """Calls updateEvaluation with changed fields and refreshes the table."""
        ok = updateEvaluation(
            am_instructor=data["AM_Instructor"],
            am_student=data["AM_Student"],
            c_code=data["C_Code"],
            Rating=data["Rating"],
            Comments=data.get("Comments"),
        )
        if ok:
            ui.notify("Evaluation updated successfully.", type="positive", position="top")
            _renderTable(container)
        else:
            ui.notify("Failed to update evaluation.", type="negative", position="top")

    dialog = buildEvaluationDialog(
        on_submit=_submit,
        instructor_options=professors,
        student_options=students,
        course_options=courses,
        initial_data=row,
    )
    dialog.open()


def _openDeleteDialog(row: dict, container: ui.column) -> None:
    """
    Opens the Delete confirmation dialog for the selected evaluation.

    Args:
        row (dict): The evaluation record dict selected for deletion.
        container (ui.column): The table container to refresh after deletion.
    """
    def _confirm() -> None:
        """Calls deleteEvaluation and refreshes the table."""
        ok = deleteEvaluation(row["AM_Instructor"], row["AM_Student"], row["C_Code"])
        if ok:
            ui.notify("Evaluation deleted.", type="warning", position="top")
            _renderTable(container)
        else:
            ui.notify("Failed to delete evaluation.", type="negative", position="top")

    dialog = buildConfirmDialog(
        message=(
            f"Delete evaluation by instructor '{row['AM_Instructor']}' "
            f"for student '{row['AM_Student']}' in course '{row['C_Code']}'?"
        ),
        on_confirm=_confirm,
    )
    dialog.open()


def _buildEmptyState(message: str) -> None:
    """
    Renders a centered empty-state placeholder when no records exist.

    Args:
        message (str): The descriptive message to display.
    """
    with ui.column().classes(
        "w-full items-center justify-center py-20 gap-3"
    ):
        ui.icon("inbox", size="3rem").classes("text-white/20")
        ui.label(message).classes("text-white/40 text-sm")
