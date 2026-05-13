"""
src/app/ui/pages/professors.py

Professor management page for the ScholarConnect web application.
Provides a searchable, sortable table of all instructors with inline
Add, Edit, and Delete operations via modal dialogs.
"""

from nicegui import ui
from src.api_actions import (
    listProfessors,
    addProfessor,
    updateProfessor,
    deleteProfessor,
)
from src.app.ui.components.sidebar import buildSidebar
from src.app.ui.components.forms import buildProfessorDialog, buildConfirmDialog


# Column definitions for the professors table.
PROFESSOR_COLUMNS = [
    {"name": "AM", "label": "AM", "field": "AM", "sortable": True, "align": "left"},
    {"name": "FirstName", "label": "First Name", "field": "FirstName", "sortable": True, "align": "left"},
    {"name": "LastName", "label": "Last Name", "field": "LastName", "sortable": True, "align": "left"},
    {"name": "email", "label": "Email", "field": "email", "sortable": True, "align": "left"},
    {"name": "Specialization", "label": "Specialization", "field": "Specialization", "sortable": True, "align": "left"},
]


def buildProfessorsPage() -> None:
    """
    Renders the Professor Management page with a full CRUD interface.

    Displays the sidebar, page header with an Add Professor button, and a
    searchable data table.  All add, edit, and delete operations use modal
    dialogs without full page reloads.
    """
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


def _renderTable(container: ui.column) -> None:
    """
    Clears and re-renders the professors data table inside the given container.

    Fetches the latest professor list from the database, builds the styled
    table with edit and delete action buttons, and registers event handlers.

    Args:
        container (ui.column): The NiceGUI column element acting as the
            table mount point.
    """
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
    Opens the Add Professor modal dialog.

    Args:
        container (ui.column): The table container to refresh after success.
    """
    def _submit(data: dict) -> None:
        """Calls addProfessor and refreshes the table on success."""
        ok = addProfessor(
            AM=data["AM"],
            Password=data.get("Password", ""),
            FirstName=data["FirstName"],
            LastName=data["LastName"],
            email=data["email"],
            Specialization=data.get("Specialization", ""),
        )
        if ok:
            ui.notify("Professor added successfully.", type="positive", position="top")
            _renderTable(container)
        else:
            ui.notify(
                "Failed to add professor. AM or email may already exist.",
                type="negative",
                position="top",
            )

    dialog = buildProfessorDialog(on_submit=_submit)
    dialog.open()


def _openEditDialog(row: dict, container: ui.column) -> None:
    """
    Opens the Edit Professor modal dialog pre-populated with row data.

    Args:
        row (dict): The professor record dict selected for editing.
        container (ui.column): The table container to refresh after success.
    """
    def _submit(data: dict) -> None:
        """Calls updateProfessor with changed fields and refreshes the table."""
        ok = updateProfessor(
            AM=data["AM"],
            FirstName=data["FirstName"],
            LastName=data["LastName"],
            email=data["email"],
            Specialization=data.get("Specialization", ""),
        )
        if ok:
            ui.notify("Professor updated successfully.", type="positive", position="top")
            _renderTable(container)
        else:
            ui.notify("Failed to update professor.", type="negative", position="top")

    dialog = buildProfessorDialog(on_submit=_submit, initial_data=row)
    dialog.open()


def _openDeleteDialog(row: dict, container: ui.column) -> None:
    """
    Opens the Delete confirmation dialog for the selected professor.

    Args:
        row (dict): The professor record dict selected for deletion.
        container (ui.column): The table container to refresh after deletion.
    """
    def _confirm() -> None:
        """Calls deleteProfessor and refreshes the table."""
        ok = deleteProfessor(row["AM"])
        if ok:
            ui.notify("Professor deleted.", type="warning", position="top")
            _renderTable(container)
        else:
            ui.notify("Failed to delete professor.", type="negative", position="top")

    dialog = buildConfirmDialog(
        message=f"Permanently delete professor '{row['FirstName']} {row['LastName']}' ({row['AM']})?",
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
