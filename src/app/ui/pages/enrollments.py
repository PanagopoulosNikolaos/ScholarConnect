"""
src/app/ui/pages/enrollments.py

Enrollment management page for the ScholarConnect web application.
Provides a searchable table of all enrollment records with inline
Add, Edit (start date only), and Delete operations via modal dialogs.
"""

from nicegui import ui, app
from src.api_actions import (
    listEnrollments,
    listStudents,
    listCourses,
    addEnrollment,
    updateEnrollment,
    deleteEnrollment,
)
from src.app.ui.components.sidebar import buildSidebar
from src.app.ui.components.forms import buildEnrollmentDialog, buildConfirmDialog


# Column definitions for the enrollments table.
ENROLLMENT_COLUMNS = [
    {"name": "AM_Student", "label": "Student AM", "field": "AM_Student", "sortable": True, "align": "left"},
    {"name": "C_Code", "label": "Course Code", "field": "C_Code", "sortable": True, "align": "left"},
    {"name": "StartDate", "label": "Start Date", "field": "StartDate", "sortable": True, "align": "left"},
]


def buildEnrollmentsPage() -> None:
    """
    Renders the Enrollment Management page with a full CRUD interface.

    Displays the sidebar, page header with an Add Enrollment button, and a
    searchable data table.  The Add dialog dynamically populates student and
    course selects from live data.
    """
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


def _renderTable(container: ui.column) -> None:
    """
    Clears and re-renders the enrollments data table inside the given container.

    Fetches the latest enrollment list and renders the styled table with
    edit and delete action buttons.

    Args:
        container (ui.column): The NiceGUI column element acting as the
            table mount point.
    """
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


def _openAddDialog(container: ui.column) -> None:
    """
    Opens the Add Enrollment modal dialog with live student and course options.

    Args:
        container (ui.column): The table container to refresh after success.
    """
    students = listStudents()
    courses = listCourses()

    def _submit(data: dict) -> None:
        """Calls addEnrollment and refreshes the table on success."""
        ok = addEnrollment(
            am_student=data["AM_Student"],
            c_code=data["C_Code"],
            start_date=data["StartDate"],
        )
        if ok:
            ui.notify("Enrollment added successfully.", type="positive", position="top")
            _renderTable(container)
        else:
            ui.notify(
                "Failed to add enrollment. Student may already be enrolled.",
                type="negative",
                position="top",
            )

    dialog = buildEnrollmentDialog(
        on_submit=_submit,
        student_options=students,
        course_options=courses,
    )
    dialog.open()


def _openEditDialog(row: dict, container: ui.column) -> None:
    """
    Opens the Edit Enrollment dialog pre-populated with row data.

    Only the StartDate field is editable; AM_Student and C_Code are locked.

    Args:
        row (dict): The enrollment record dict selected for editing.
        container (ui.column): The table container to refresh after success.
    """
    students = listStudents()
    courses = listCourses()

    def _submit(data: dict) -> None:
        """Calls updateEnrollment with the new start date and refreshes the table."""
        ok = updateEnrollment(
            am_student=data["AM_Student"],
            c_code=data["C_Code"],
            StartDate=data["StartDate"],
        )
        if ok:
            ui.notify("Enrollment updated successfully.", type="positive", position="top")
            _renderTable(container)
        else:
            ui.notify("Failed to update enrollment.", type="negative", position="top")

    dialog = buildEnrollmentDialog(
        on_submit=_submit,
        student_options=students,
        course_options=courses,
        initial_data=row,
    )
    dialog.open()


def _openDeleteDialog(row: dict, container: ui.column) -> None:
    """
    Opens the Delete confirmation dialog for the selected enrollment.

    Args:
        row (dict): The enrollment record dict selected for deletion.
        container (ui.column): The table container to refresh after deletion.
    """
    def _confirm() -> None:
        """Calls deleteEnrollment and refreshes the table."""
        ok = deleteEnrollment(row["AM_Student"], row["C_Code"])
        if ok:
            ui.notify("Enrollment deleted.", type="warning", position="top")
            _renderTable(container)
        else:
            ui.notify("Failed to delete enrollment.", type="negative", position="top")

    dialog = buildConfirmDialog(
        message=(
            f"Remove enrollment of student '{row['AM_Student']}' "
            f"from course '{row['C_Code']}'?"
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
