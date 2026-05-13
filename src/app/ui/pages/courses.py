"""
src/app/ui/pages/courses.py

Course management page for the ScholarConnect web application.
Provides a searchable, sortable table of all courses with inline
Add, Edit, and Delete operations via modal dialogs.  Professor assignment
is handled through the course dialog's select field.
"""

from nicegui import ui, app
from src.api_actions import (
    listCourses,
    listProfessors,
    addCourse,
    updateCourse,
    deleteCourse,
    addEnrollment,
    listEnrollments,
    deleteEnrollment,
)
import datetime
from src.app.ui.components.sidebar import buildSidebar
from src.app.ui.components.forms import buildCourseDialog, buildConfirmDialog


# Column definitions for the courses table.
COURSE_COLUMNS = [
    {"name": "C_Code", "label": "Code", "field": "C_Code", "sortable": True, "align": "left"},
    {"name": "Title", "label": "Title", "field": "Title", "sortable": True, "align": "left"},
    {"name": "Category", "label": "Category", "field": "Category", "sortable": True, "align": "left"},
    {"name": "AM_Instructor", "label": "Instructor AM", "field": "AM_Instructor", "sortable": True, "align": "left"},
    {"name": "Description", "label": "Description", "field": "Description", "sortable": False, "align": "left"},
]


def buildCoursesPage() -> None:
    """
    Renders the Course Management page with a full CRUD interface.

    Displays the sidebar, page header with an Add Course button, and a
    searchable data table.  Add and edit dialogs include a professor
    assignment select populated from live data.
    """
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


def _renderTable(container: ui.column) -> None:
    """
    Clears and re-renders the courses data table inside the given container.

    Fetches the latest course list from the database, builds the styled
    table with edit and delete action buttons, and registers event handlers.

    Args:
        container (ui.column): The NiceGUI column element acting as the
            table mount point.
    """
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


def _joinCourse(row: dict, container: ui.column) -> None:
    """
    Enrolls the logged-in student in the selected course.
    """
    user_am = app.storage.user.get("user_am")
    if not user_am:
        return
        
    c_code = row["C_Code"]
    start_date = datetime.date.today().isoformat()
    
    ok = addEnrollment(
        am_student=user_am,
        c_code=c_code,
        start_date=start_date
    )
    
    if ok:
        ui.notify(f"Successfully joined {row['Title']}!", type="positive", position="top")
        _renderTable(container)
    else:
        ui.notify("You are already enrolled or joining failed.", type="negative", position="top")


def _leaveCourse(row: dict, container: ui.column) -> None:
    """
    Unenrolls the logged-in student from the selected course.
    """
    user_am = app.storage.user.get("user_am")
    if not user_am:
        return
        
    c_code = row["C_Code"]
    
    ok = deleteEnrollment(
        am_student=user_am,
        c_code=c_code,
    )
    
    if ok:
        ui.notify(f"Left {row['Title']}.", type="warning", position="top")
        _renderTable(container)
    else:
        ui.notify("Failed to leave course.", type="negative", position="top")


def _openAddDialog(container: ui.column) -> None:
    """
    Opens the Add Course modal dialog.

    Loads the current professor list to populate the assignment select before
    opening the dialog.

    Args:
        container (ui.column): The table container to refresh after success.
    """
    professors = listProfessors()

    def _submit(data: dict) -> None:
        """Calls addCourse and refreshes the table on success."""
        ok = addCourse(
            c_code=data["C_Code"],
            title=data["Title"],
            description=data.get("Description"),
            category=data.get("Category"),
            am_instructor=data.get("AM_Instructor"),
        )
        if ok:
            ui.notify("Course added successfully.", type="positive", position="top")
            _renderTable(container)
        else:
            ui.notify(
                "Failed to add course. Course code may already exist.",
                type="negative",
                position="top",
            )

    dialog = buildCourseDialog(on_submit=_submit, professor_options=professors)
    dialog.open()


def _openEditDialog(row: dict, container: ui.column) -> None:
    """
    Opens the Edit Course modal dialog pre-populated with row data.

    Args:
        row (dict): The course record dict selected for editing.
        container (ui.column): The table container to refresh after success.
    """
    professors = listProfessors()

    def _submit(data: dict) -> None:
        """Calls updateCourse with changed fields and refreshes the table."""
        ok = updateCourse(
            c_code=data["C_Code"],
            Title=data["Title"],
            Description=data.get("Description"),
            Category=data.get("Category"),
            AM_Instructor=data.get("AM_Instructor"),
        )
        if ok:
            ui.notify("Course updated successfully.", type="positive", position="top")
            _renderTable(container)
        else:
            ui.notify("Failed to update course.", type="negative", position="top")

    dialog = buildCourseDialog(
        on_submit=_submit,
        professor_options=professors,
        initial_data=row,
    )
    dialog.open()


def _openDeleteDialog(row: dict, container: ui.column) -> None:
    """
    Opens the Delete confirmation dialog for the selected course.

    Args:
        row (dict): The course record dict selected for deletion.
        container (ui.column): The table container to refresh after deletion.
    """
    def _confirm() -> None:
        """Calls deleteCourse and refreshes the table."""
        ok = deleteCourse(row["C_Code"])
        if ok:
            ui.notify("Course deleted.", type="warning", position="top")
            _renderTable(container)
        else:
            ui.notify("Failed to delete course.", type="negative", position="top")

    dialog = buildConfirmDialog(
        message=f"Permanently delete course '{row['Title']}' ({row['C_Code']})?",
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
