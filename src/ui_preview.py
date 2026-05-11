import os
import sys

# Adds the project root to the system path to ensure the 'src' package is discoverable.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from nicegui import ui, app
from src.database import getConnection
from src.api_actions import (
    addStudent, getStudent, listStudents, updateStudent, deleteStudent,
    addProfessor, getProfessor, listProfessors, updateProfessor, deleteProfessor,
)

# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------

def _fetchAll(query: str, params=()):
    """
    Fetches all rows for a raw SQL query.

    Args:
        query (str): A parameterized SQL query.
        params (tuple): Query parameters.

    Returns:
        (list): A list of dictionaries representing each row.
    """
    conn = getConnection()
    try:
        cur = conn.cursor()
        cur.execute(query, params)
        return [dict(r) for r in cur.fetchall()]
    finally:
        conn.close()


def _execute(query: str, params=()):
    """
    Executes a raw SQL write query.

    Args:
        query (str): A parameterized SQL statement.
        params (tuple): Query parameters.

    Returns:
        (bool): True if at least one row was affected, False otherwise.
    """
    conn = getConnection()
    try:
        cur = conn.cursor()
        cur.execute(query, params)
        conn.commit()
        return cur.rowcount > 0
    except Exception:
        conn.rollback()
        return False
    finally:
        conn.close()


def _notify(msg: str, ntype: str = "positive"):
    """
    Displays a notification message.

    Args:
        msg (str): The notification text.
        ntype (str): Notification type ('positive', 'negative', 'warning', 'info').
    """
    ui.notify(msg, type=ntype, position="top-right", timeout=3000)


def _sidebar():
    """Renders the navigation sidebar."""
    ui.dark_mode().enable()
    with ui.header(elevated=True).classes("bg-primary"):
        ui.label("ScholarConnect").classes("text-xl font-bold text-white")
    with ui.left_drawer(top_corner=True, bottom_corner=True).classes("bg-grey-9"):
        with ui.column().classes("w-full q-pa-sm"):
            ui.button("Dashboard", icon="dashboard", on_click=lambda: ui.open("/")).props(
                "flat text-white"
            ).classes("w-full")
            ui.button("Students", icon="people", on_click=lambda: ui.open("/students")).props(
                "flat text-white"
            ).classes("w-full")
            ui.button("Instructors", icon="school",
                      on_click=lambda: ui.open("/professors")).props("flat text-white").classes(
                          "w-full"
                      )
            ui.button("Courses", icon="book", on_click=lambda: ui.open("/courses")).props(
                "flat text-white"
            ).classes("w-full")
            ui.button("Enrollments", icon="assignment",
                      on_click=lambda: ui.open("/enrollments")).props("flat text-white").classes(
                          "w-full"
                      )
            ui.button("Reviews", icon="star", on_click=lambda: ui.open("/evaluations")).props(
                "flat text-white"
            ).classes("w-full")


# ---------------------------------------------------------------------------
# Dashboard
# ---------------------------------------------------------------------------

@ui.page("/")
def dashboard():
    """
    Renders the dashboard page with summary statistics and quick actions.
    """
    _sidebar()
    with ui.column().classes("w-full p-4"):
        ui.label("Dashboard").classes("text-2xl font-bold mb-4")

        student_count = len(listStudents())
        professor_count = len(listProfessors())
        course_count = _fetchAll("SELECT COUNT(*) as c FROM COURSE")[0]["c"]
        enrollment_count = _fetchAll("SELECT COUNT(*) as c FROM ENROLLMENT")[0]["c"]
        eval_count = _fetchAll("SELECT COUNT(*) as c FROM EVALUATION")[0]["c"]

        with ui.grid(columns=3).classes("w-full gap-4"):
            with ui.card().classes("p-4 text-center"):
                ui.icon("people", size="48px").classes("text-blue-400")
                ui.label(f"{student_count}").classes("text-3xl font-bold")
                ui.label("Students").classes("text-sm text-grey-5")

            with ui.card().classes("p-4 text-center"):
                ui.icon("school", size="48px").classes("text-green-400")
                ui.label(f"{professor_count}").classes("text-3xl font-bold")
                ui.label("Instructors").classes("text-sm text-grey-5")

            with ui.card().classes("p-4 text-center"):
                ui.icon("book", size="48px").classes("text-purple-400")
                ui.label(f"{course_count}").classes("text-3xl font-bold")
                ui.label("Courses").classes("text-sm text-grey-5")

            with ui.card().classes("p-4 text-center"):
                ui.icon("assignment", size="48px").classes("text-orange-400")
                ui.label(f"{enrollment_count}").classes("text-3xl font-bold")
                ui.label("Enrollments").classes("text-sm text-grey-5")

            with ui.card().classes("p-4 text-center"):
                ui.icon("star", size="48px").classes("text-yellow-400")
                ui.label(f"{eval_count}").classes("text-3xl font-bold")
                ui.label("Reviews").classes("text-sm text-grey-5")


# ---------------------------------------------------------------------------
# Students
# ---------------------------------------------------------------------------

@ui.page("/students")
def students():
    """
    Renders the student management page with a data table and CRUD dialogs.
    """
    _sidebar()

    cols = [
        {"name": "am", "label": "AM", "field": "am", "sortable": True},
        {"name": "username", "label": "Username", "field": "username", "sortable": True},
        {"name": "first", "label": "First Name", "field": "first"},
        {"name": "last", "label": "Last Name", "field": "last"},
        {"name": "email", "label": "Email", "field": "email"},
        {"name": "actions", "label": "", "field": "actions"},
    ]
    table = ui.table(columns=cols, rows=[], row_key="id").classes("w-full")

    def refresh():
        """Reloads student data into the table."""
        rows = listStudents()
        table.rows = [
            {"id": s["AM"], "am": s["AM"], "username": s["Username"],
             "first": s["FirstName"], "last": s["LastName"], "email": s["email"]}
            for s in rows
        ]
        table.update()

    refresh()

    # -- Add dialog --
    def addDialog():
        with ui.dialog() as d, ui.card().classes("w-96"):
            ui.label("Add Student").classes("text-lg font-bold")
            am = ui.input("AM")
            uname = ui.input("Username")
            first = ui.input("First Name")
            last = ui.input("Last Name")
            email = ui.input("Email")
            pw = ui.input("Password", password_toggle_button=True)
            with ui.row():
                ui.button("Save", on_click=lambda: _doAdd(
                    d, am, pw, uname, email, first, last
                )).props("color=primary")
                ui.button("Cancel", on_click=d.close)
        d.open()

    def _doAdd(d, am, pw, uname, email, first, last):
        ok = addStudent(am.value, pw.value, uname.value, email.value,
                        first.value, last.value)
        if ok:
            _notify("Student added")
            d.close()
            refresh()
        else:
            _notify("Failed to add student (AM/Username/Email may already exist)", "negative")

    # -- Edit dialog --
    def editDialog(row):
        s = getStudent(row["id"])
        if not s:
            return
        with ui.dialog() as d, ui.card().classes("w-96"):
            ui.label("Edit Student").classes("text-lg font-bold")
            ui.label(f"AM: {s['AM']}").classes("text-sm text-grey")
            uname = ui.input("Username", value=s["Username"])
            first = ui.input("First Name", value=s["FirstName"])
            last = ui.input("Last Name", value=s["LastName"])
            email = ui.input("Email", value=s["email"])
            pw = ui.input("Password (leave blank to keep)", password_toggle_button=True)
            with ui.row():
                ui.button("Update", on_click=lambda: _doEdit(
                    d, s["AM"], uname, first, last, email, pw
                )).props("color=warning")
                ui.button("Cancel", on_click=d.close)
        d.open()

    def _doEdit(d, am, uname, first, last, email, pw):
        kwargs = {}
        if uname.value:
            kwargs["Username"] = uname.value
        if first.value:
            kwargs["FirstName"] = first.value
        if last.value:
            kwargs["LastName"] = last.value
        if email.value:
            kwargs["email"] = email.value
        if pw.value:
            kwargs["Password"] = pw.value
        ok = updateStudent(am, **kwargs)
        if ok:
            _notify("Student updated")
            d.close()
            refresh()
        else:
            _notify("Failed to update student", "negative")

    # -- Delete --
    def deleteRow(row):
        ok = deleteStudent(row["id"])
        if ok:
            _notify("Student deleted")
            refresh()
        else:
            _notify("Failed to delete student (may have enrollments)", "negative")

    with ui.row().classes("mb-4"):
        ui.button("Add Student", on_click=addDialog).props("color=primary")

    table.add_slot("body-cell-actions", """
        <q-td key="actions" :props="props">
            <q-btn dense flat icon="edit" color="warning" size="sm" @click="emit('edit', props.row)" />
            <q-btn dense flat icon="delete" color="negative" size="sm" @click="emit('delete', props.row)" />
        </q-td>
    """)
    table.on("edit", lambda e: editDialog(e.args))
    table.on("delete", lambda e: deleteRow(e.args))


# ---------------------------------------------------------------------------
# Instructors
# ---------------------------------------------------------------------------

@ui.page("/professors")
def professors():
    """
    Renders the instructor management page with a data table and CRUD dialogs.
    """
    _sidebar()

    cols = [
        {"name": "am", "label": "AM", "field": "am", "sortable": True},
        {"name": "username", "label": "Username", "field": "username", "sortable": True},
        {"name": "first", "label": "First Name", "field": "first"},
        {"name": "last", "label": "Last Name", "field": "last"},
        {"name": "email", "label": "Email", "field": "email"},
        {"name": "spec", "label": "Specialization", "field": "spec"},
        {"name": "actions", "label": "", "field": "actions"},
    ]
    table = ui.table(columns=cols, rows=[], row_key="id").classes("w-full")

    def refresh():
        """Reloads instructor data into the table."""
        rows = listProfessors()
        table.rows = [
            {"id": p["AM"], "am": p["AM"], "username": p["Username"],
             "first": p["FirstName"], "last": p["LastName"],
             "email": p["email"], "spec": p["Specialization"]}
            for p in rows
        ]
        table.update()

    refresh()

    def addDialog():
        with ui.dialog() as d, ui.card().classes("w-96"):
            ui.label("Add Instructor").classes("text-lg font-bold")
            am = ui.input("AM")
            uname = ui.input("Username")
            first = ui.input("First Name")
            last = ui.input("Last Name")
            email = ui.input("Email")
            spec = ui.input("Specialization")
            pw = ui.input("Password", password_toggle_button=True)
            with ui.row():
                ui.button("Save", on_click=lambda: _doAdd(
                    d, am, pw, uname, first, last, email, spec
                )).props("color=primary")
                ui.button("Cancel", on_click=d.close)
        d.open()

    def _doAdd(d, am, pw, uname, first, last, email, spec):
        ok = addProfessor(am.value, pw.value, uname.value, first.value,
                          last.value, email.value, spec.value)
        if ok:
            _notify("Instructor added")
            d.close()
            refresh()
        else:
            _notify("Failed to add instructor", "negative")

    def editDialog(row):
        p = getProfessor(row["id"])
        if not p:
            return
        with ui.dialog() as d, ui.card().classes("w-96"):
            ui.label("Edit Instructor").classes("text-lg font-bold")
            ui.label(f"AM: {p['AM']}").classes("text-sm text-grey")
            uname = ui.input("Username", value=p["Username"])
            first = ui.input("First Name", value=p["FirstName"])
            last = ui.input("Last Name", value=p["LastName"])
            email = ui.input("Email", value=p["email"])
            spec = ui.input("Specialization", value=p["Specialization"])
            pw = ui.input("Password (leave blank to keep)", password_toggle_button=True)
            with ui.row():
                ui.button("Update", on_click=lambda: _doEdit(
                    d, p["AM"], uname, first, last, email, spec, pw
                )).props("color=warning")
                ui.button("Cancel", on_click=d.close)
        d.open()

    def _doEdit(d, am, uname, first, last, email, spec, pw):
        kwargs = {}
        if uname.value:
            kwargs["Username"] = uname.value
        if first.value:
            kwargs["FirstName"] = first.value
        if last.value:
            kwargs["LastName"] = last.value
        if email.value:
            kwargs["email"] = email.value
        if spec.value:
            kwargs["Specialization"] = spec.value
        if pw.value:
            kwargs["Password"] = pw.value
        ok = updateProfessor(am, **kwargs)
        if ok:
            _notify("Instructor updated")
            d.close()
            refresh()
        else:
            _notify("Failed to update instructor", "negative")

    def deleteRow(row):
        ok = deleteProfessor(row["id"])
        if ok:
            _notify("Instructor deleted")
            refresh()
        else:
            _notify("Failed to delete instructor (may be teaching courses)", "negative")

    with ui.row().classes("mb-4"):
        ui.button("Add Instructor", on_click=addDialog).props("color=primary")

    table.add_slot("body-cell-actions", """
        <q-td key="actions" :props="props">
            <q-btn dense flat icon="edit" color="warning" size="sm" @click="emit('edit', props.row)" />
            <q-btn dense flat icon="delete" color="negative" size="sm" @click="emit('delete', props.row)" />
        </q-td>
    """)
    table.on("edit", lambda e: editDialog(e.args))
    table.on("delete", lambda e: deleteRow(e.args))


# ---------------------------------------------------------------------------
# Courses
# ---------------------------------------------------------------------------

@ui.page("/courses")
def courses():
    """
    Renders the course management page with a data table and add/delete actions.
    """
    _sidebar()

    cols = [
        {"name": "code", "label": "Code", "field": "code", "sortable": True},
        {"name": "title", "label": "Title", "field": "title", "sortable": True},
        {"name": "desc", "label": "Description", "field": "desc"},
        {"name": "cat", "label": "Category", "field": "cat"},
        {"name": "instructor", "label": "Instructor AM", "field": "instructor"},
        {"name": "actions", "label": "", "field": "actions"},
    ]
    table = ui.table(columns=cols, rows=[], row_key="id").classes("w-full")

    def refresh():
        """Reloads course data into the table."""
        rows = _fetchAll("SELECT * FROM COURSE")
        table.rows = [
            {"id": c["C_Code"], "code": c["C_Code"], "title": c["Title"],
             "desc": (c["Description"] or "")[:60],
             "cat": c["Category"] or "", "instructor": c["AM_Instructor"] or ""}
            for c in rows
        ]
        table.update()

    refresh()

    def addDialog():
        with ui.dialog() as d, ui.card().classes("w-96"):
            ui.label("Add Course").classes("text-lg font-bold")
            code = ui.input("Course Code")
            title = ui.input("Title")
            desc = ui.textarea("Description")
            cat = ui.input("Category")
            instr = ui.input("Instructor AM")
            with ui.row():
                ui.button("Save", on_click=lambda: _doAdd(
                    d, code, title, desc, cat, instr
                )).props("color=primary")
                ui.button("Cancel", on_click=d.close)
        d.open()

    def _doAdd(d, code, title, desc, cat, instr):
        ok = _execute(
            "INSERT INTO COURSE (C_Code, Title, Description, Category, AM_Instructor) "
            "VALUES (?, ?, ?, ?, ?)",
            (code.value, title.value, desc.value, cat.value, instr.value or None),
        )
        if ok:
            _notify("Course added")
            d.close()
            refresh()
        else:
            _notify("Failed to add course (code may already exist)", "negative")

    def deleteRow(row):
        ok = _execute("DELETE FROM COURSE WHERE C_Code = ?", (row["id"],))
        if ok:
            _notify("Course deleted")
            refresh()
        else:
            _notify("Failed to delete course (may have enrollments)", "negative")

    with ui.row().classes("mb-4"):
        ui.button("Add Course", on_click=addDialog).props("color=primary")

    table.add_slot("body-cell-actions", """
        <q-td key="actions" :props="props">
            <q-btn dense flat icon="delete" color="negative" size="sm" @click="emit('delete', props.row)" />
        </q-td>
    """)
    table.on("delete", lambda e: deleteRow(e.args))


# ---------------------------------------------------------------------------
# Enrollments
# ---------------------------------------------------------------------------

@ui.page("/enrollments")
def enrollments():
    """
    Renders the enrollment management page with a data table and add/delete actions.
    """
    _sidebar()

    cols = [
        {"name": "student", "label": "Student AM", "field": "student", "sortable": True},
        {"name": "course", "label": "Course Code", "field": "course", "sortable": True},
        {"name": "date", "label": "Start Date", "field": "date", "sortable": True},
        {"name": "actions", "label": "", "field": "actions"},
    ]
    table = ui.table(columns=cols, rows=[], row_key="id").classes("w-full")

    def refresh():
        """Reloads enrollment data into the table."""
        rows = _fetchAll("SELECT * FROM ENROLLMENT")
        table.rows = [
            {"id": f'{e["AM_Student"]}|{e["C_Code"]}',
             "student": e["AM_Student"], "course": e["C_Code"],
             "date": e["StartDate"]}
            for e in rows
        ]
        table.update()

    refresh()

    def addDialog():
        with ui.dialog() as d, ui.card().classes("w-96"):
            ui.label("Add Enrollment").classes("text-lg font-bold")
            student = ui.input("Student AM")
            course = ui.input("Course Code")
            date = ui.input("Start Date (YYYY-MM-DD)")
            with ui.row():
                ui.button("Save", on_click=lambda: _doAdd(
                    d, student, course, date
                )).props("color=primary")
                ui.button("Cancel", on_click=d.close)
        d.open()

    def _doAdd(d, student, course, date):
        ok = _execute(
            "INSERT INTO ENROLLMENT (AM_Student, C_Code, StartDate) VALUES (?, ?, ?)",
            (student.value, course.value, date.value),
        )
        if ok:
            _notify("Enrollment added")
            d.close()
            refresh()
        else:
            _notify("Failed to add enrollment (check student/course exist)", "negative")

    def deleteRow(row):
        parts = row["id"].split("|")
        ok = _execute(
            "DELETE FROM ENROLLMENT WHERE AM_Student = ? AND C_Code = ?",
            (parts[0], parts[1]),
        )
        if ok:
            _notify("Enrollment deleted")
            refresh()
        else:
            _notify("Failed to delete enrollment", "negative")

    with ui.row().classes("mb-4"):
        ui.button("Add Enrollment", on_click=addDialog).props("color=primary")

    table.add_slot("body-cell-actions", """
        <q-td key="actions" :props="props">
            <q-btn dense flat icon="delete" color="negative" size="sm" @click="emit('delete', props.row)" />
        </q-td>
    """)
    table.on("delete", lambda e: deleteRow(e.args))


# ---------------------------------------------------------------------------
# Evaluations (Reviews)
# ---------------------------------------------------------------------------

@ui.page("/evaluations")
def evaluations():
    """
    Renders the evaluation/review management page with a data table and CRUD actions.
    """
    _sidebar()

    cols = [
        {"name": "instructor", "label": "Instructor AM", "field": "instructor", "sortable": True},
        {"name": "student", "label": "Student AM", "field": "student", "sortable": True},
        {"name": "course", "label": "Course Code", "field": "course", "sortable": True},
        {"name": "rating", "label": "Rating", "field": "rating", "sortable": True},
        {"name": "comments", "label": "Comments", "field": "comments"},
        {"name": "actions", "label": "", "field": "actions"},
    ]
    table = ui.table(columns=cols, rows=[], row_key="id").classes("w-full")

    def refresh():
        """Reloads evaluation data into the table."""
        rows = _fetchAll("SELECT * FROM EVALUATION")
        table.rows = [
            {
                "id": f'{e["AM_Instructor"]}|{e["AM_Student"]}|{e["C_Code"]}',
                "instructor": e["AM_Instructor"],
                "student": e["AM_Student"],
                "course": e["C_Code"],
                "rating": e["Rating"],
                "comments": (e["Comments"] or "")[:50],
            }
            for e in rows
        ]
        table.update()

    refresh()

    def addDialog():
        with ui.dialog() as d, ui.card().classes("w-96"):
            ui.label("Add Review").classes("text-lg font-bold")
            instr = ui.input("Instructor AM")
            student = ui.input("Student AM")
            course = ui.input("Course Code")
            rating = ui.number("Rating (1-5)", min=1, max=5, value=5)
            comments = ui.textarea("Comments")
            with ui.row():
                ui.button("Save", on_click=lambda: _doAdd(
                    d, instr, student, course, rating, comments
                )).props("color=primary")
                ui.button("Cancel", on_click=d.close)
        d.open()

    def _doAdd(d, instr, student, course, rating, comments):
        ok = _execute(
            "INSERT INTO EVALUATION (AM_Instructor, AM_Student, C_Code, Rating, Comments) "
            "VALUES (?, ?, ?, ?, ?)",
            (instr.value, student.value, course.value,
             int(rating.value), comments.value),
        )
        if ok:
            _notify("Review added")
            d.close()
            refresh()
        else:
            _notify("Failed to add review (check IDs)", "negative")

    def deleteRow(row):
        parts = row["id"].split("|")
        ok = _execute(
            "DELETE FROM EVALUATION WHERE AM_Instructor = ? AND AM_Student = ? AND C_Code = ?",
            (parts[0], parts[1], parts[2]),
        )
        if ok:
            _notify("Review deleted")
            refresh()
        else:
            _notify("Failed to delete review", "negative")

    with ui.row().classes("mb-4"):
        ui.button("Add Review", on_click=addDialog).props("color=primary")

    table.add_slot("body-cell-actions", """
        <q-td key="actions" :props="props">
            <q-btn dense flat icon="delete" color="negative" size="sm" @click="emit('delete', props.row)" />
        </q-td>
    """)
    table.on("delete", lambda e: deleteRow(e.args))


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    """
    Starts the NiceGUI application.
    """
    ui.run(
        title="ScholarConnect",
        host="127.0.0.1",
        port=8080,
        dark=True,
        reload=False,
    )


if __name__ == "__main__":
    main()