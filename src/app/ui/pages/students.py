"""
src/app/ui/pages/students.py

Student management page for the ScholarConnect web application.
Provides a searchable, sortable table of all students with inline
Add, Edit, and Delete operations via modal dialogs.
"""

from nicegui import ui
from src.api_actions import (
    listStudents,
    addStudent,
    updateStudent,
    deleteStudent,
)
from src.app.ui.components.sidebar import buildSidebar
from src.app.ui.components.forms import buildStudentDialog, buildConfirmDialog


# Column definitions for the students table.
STUDENT_COLUMNS = [
    {"name": "AM", "label": "AM", "field": "AM", "sortable": True, "align": "left"},
    {"name": "FirstName", "label": "First Name", "field": "FirstName", "sortable": True, "align": "left"},
    {"name": "LastName", "label": "Last Name", "field": "LastName", "sortable": True, "align": "left"},
    {"name": "email", "label": "Email", "field": "email", "sortable": True, "align": "left"},
    {"name": "Username", "label": "Username", "field": "Username", "sortable": False, "align": "left"},
]


def buildStudentsPage() -> None:
    """
    Renders the Student Management page with a full CRUD interface.

    Displays the sidebar, page header with an Add Student button, and a
    searchable data table.  All add, edit, and delete operations are
    performed via modal dialogs without full page reloads.
    """
    buildSidebar()

    with ui.column().classes("w-full min-h-screen bg-[#0a0d14] p-8 gap-6"):
        # Page header row
        with ui.row().classes("w-full items-center justify-between"):
            with ui.column().classes("gap-1"):
                ui.label("Students").classes(
                    "text-white font-bold text-3xl tracking-tight"
                )
                ui.label("Manage student records.").classes(
                    "text-white/40 text-sm"
                )
            ui.button(
                "Add Student",
                icon="add",
                on_click=lambda: _openAddDialog(table_container),
            ).classes(
                "bg-indigo-600 hover:bg-indigo-500 text-white rounded-xl "
                "px-5 py-2 no-uppercase font-medium transition-colors duration-200"
            )

        # Mutable container that holds the table so it can be re-rendered.
        table_container = ui.column().classes("w-full")
        _renderTable(table_container)


def _renderTable(container: ui.column) -> None:
    """
    Clears and re-renders the students data table inside the given container.

    Fetches the latest student list from the database, builds the table with
    edit and delete action callbacks, and registers the custom Vue events.

    Args:
        container (ui.column): The NiceGUI column element acting as the
            table mount point.
    """
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

            # Inject scoped action slot for edit/delete buttons.
            table.add_slot(
                "body-cell-actions",
                "<q-td :props='props'>"
                "  <q-btn flat round dense icon='edit' color='indigo-4'"
                "    @click=\"$parent.$emit('edit', props.row)\" />"
                "  <q-btn flat round dense icon='delete' color='red-4'"
                "    @click=\"$parent.$emit('delete', props.row)\" />"
                "</q-td>",
            )
            # Append the actions column header dynamically.
            table.columns.append(
                {"name": "actions", "label": "Actions", "field": "actions", "align": "center"}
            )

            table.on("edit", lambda e: _openEditDialog(e.args, container))
            table.on("delete", lambda e: _openDeleteDialog(e.args, container))


def _openAddDialog(container: ui.column) -> None:
    """
    Opens the Add Student modal dialog.

    Args:
        container (ui.column): The table container to refresh after success.
    """
    def _submit(data: dict) -> None:
        """Calls addStudent and refreshes the table on success."""
        ok = addStudent(
            AM=data["AM"],
            Password=data.get("Password", ""),
            email=data["email"],
            FirstName=data["FirstName"],
            LastName=data["LastName"],
        )
        if ok:
            ui.notify("Student added successfully.", type="positive", position="top")
            _renderTable(container)
        else:
            ui.notify(
                "Failed to add student. AM or email may already exist.",
                type="negative",
                position="top",
            )

    dialog = buildStudentDialog(on_submit=_submit)
    dialog.open()


def _openEditDialog(row: dict, container: ui.column) -> None:
    """
    Opens the Edit Student modal dialog pre-populated with row data.

    Args:
        row (dict): The student record dict selected for editing.
        container (ui.column): The table container to refresh after success.
    """
    def _submit(data: dict) -> None:
        """Calls updateStudent with changed fields and refreshes the table."""
        ok = updateStudent(
            AM=data["AM"],
            FirstName=data["FirstName"],
            LastName=data["LastName"],
            email=data["email"],
        )
        if ok:
            ui.notify("Student updated successfully.", type="positive", position="top")
            _renderTable(container)
        else:
            ui.notify("Failed to update student.", type="negative", position="top")

    dialog = buildStudentDialog(on_submit=_submit, initial_data=row)
    dialog.open()


def _openDeleteDialog(row: dict, container: ui.column) -> None:
    """
    Opens the Delete confirmation dialog for the selected student.

    Args:
        row (dict): The student record dict selected for deletion.
        container (ui.column): The table container to refresh after deletion.
    """
    def _confirm() -> None:
        """Calls deleteStudent and refreshes the table."""
        ok = deleteStudent(row["AM"])
        if ok:
            ui.notify("Student deleted.", type="warning", position="top")
            _renderTable(container)
        else:
            ui.notify("Failed to delete student.", type="negative", position="top")

    dialog = buildConfirmDialog(
        message=f"Permanently delete student '{row['FirstName']} {row['LastName']}' ({row['AM']})?",
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
