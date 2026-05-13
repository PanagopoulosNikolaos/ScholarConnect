"""
src/app/ui/components/forms.py

Reusable modal dialog forms for ScholarConnect CRUD operations.
Provides builder functions for Add/Edit dialogs for each entity type,
encapsulating field layout, validation rules, and submit handling.
"""

from typing import Any, Callable
from nicegui import ui


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _buildDialogShell(title: str) -> tuple[ui.dialog, ui.card]:
    """
    Creates the base dark-themed dialog shell with a title header.

    Args:
        title (str): The heading text displayed at the top of the dialog.

    Returns:
        tuple[ui.dialog, ui.card]: The dialog and its inner card container.
    """
    dialog = ui.dialog().props("persistent")
    with dialog:
        card = ui.card().classes(
            "bg-[#161b27] border border-white/10 rounded-2xl p-6 w-full max-w-lg"
        )
        with card:
            ui.label(title).classes("text-white font-semibold text-lg mb-4")
    return dialog, card


def _buildField(
    label: str,
    placeholder: str = "",
    value: str = "",
    rules: list | None = None,
    password: bool = False,
    required: bool = True,
) -> ui.input:
    """
    Renders a single dark-styled form input field.

    Args:
        label (str): The field label shown above the input.
        placeholder (str): Placeholder text inside the input.
        value (str): Pre-filled value for edit dialogs.
        rules (list | None): NiceGUI validation rule list. Defaults to None.
        password (bool): Renders the field as a password type when True.
        required (bool): Appends a required validator when True.

    Returns:
        ui.input: The constructed NiceGUI input element.
    """
    effective_rules = list(rules or [])
    if required:
        effective_rules.insert(0, lambda v: bool(v.strip()) or f"{label} is required")

    inp = (
        ui.input(label=label, placeholder=placeholder, value=value)
        .classes("w-full")
        .props(f"outlined dark dense {'type=password' if password else ''}")
    )
    if effective_rules:
        inp.validation = {f"{label}": effective_rules[0]}
    return inp


def _actionRow(
    on_submit: Callable,
    on_cancel: Callable,
    submit_label: str = "Save",
) -> None:
    """
    Renders the dialog's cancel / submit button row.

    Args:
        on_submit (Callable): Invoked when the submit button is clicked.
        on_cancel (Callable): Invoked when the cancel button is clicked.
        submit_label (str): Label text for the submit button. Defaults to 'Save'.
    """
    with ui.row().classes("w-full justify-end gap-3 mt-4"):
        ui.button("Cancel", on_click=on_cancel).props(
            "flat"
        ).classes("text-white/60 hover:text-white/90 no-uppercase")
        ui.button(submit_label, on_click=on_submit).classes(
            "bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg "
            "px-5 py-2 no-uppercase font-medium transition-colors duration-200"
        )


# ---------------------------------------------------------------------------
# Student forms
# ---------------------------------------------------------------------------

def buildStudentDialog(
    on_submit: Callable[[dict], None],
    initial_data: dict | None = None,
) -> ui.dialog:
    """
    Constructs the Add/Edit Student modal dialog.

    Renders fields for AM, password, email, first name, and last name.
    The AM field is read-only when editing an existing record.

    Args:
        on_submit (Callable[[dict], None]): Callback invoked with the form
            data dict on a valid submission.
        initial_data (dict | None): Pre-populated values for edit mode.
            When None the dialog operates in add mode.

    Returns:
        ui.dialog: The fully constructed dialog element.
    """
    is_edit = initial_data is not None
    title = "Edit Student" if is_edit else "Add Student"
    data = initial_data or {}

    dialog, card = _buildDialogShell(title)
    with card:
        with ui.column().classes("w-full gap-3"):
            am_input = _buildField(
                "AM (Student ID)", "e.g. STU001",
                value=data.get("AM", ""),
                required=not is_edit,
            )
            if is_edit:
                am_input.props("readonly")
                am_input.classes("opacity-60")

            first_input = _buildField(
                "First Name", value=data.get("FirstName", "")
            )
            last_input = _buildField(
                "Last Name", value=data.get("LastName", "")
            )
            email_input = _buildField(
                "Email", value=data.get("email", ""),
                rules=[lambda v: "@" in v or "Enter a valid email"],
            )
            if not is_edit:
                pwd_input = _buildField(
                    "Password", password=True
                )
            else:
                pwd_input = None

        def _submit():
            """Collects field values and delegates to the provided callback."""
            payload = {
                "AM": am_input.value.strip(),
                "FirstName": first_input.value.strip(),
                "LastName": last_input.value.strip(),
                "email": email_input.value.strip(),
            }
            if pwd_input:
                payload["Password"] = pwd_input.value
            on_submit(payload)
            dialog.close()

        _actionRow(_submit, dialog.close, submit_label="Save Student")

    return dialog


# ---------------------------------------------------------------------------
# Professor forms
# ---------------------------------------------------------------------------

def buildProfessorDialog(
    on_submit: Callable[[dict], None],
    initial_data: dict | None = None,
) -> ui.dialog:
    """
    Constructs the Add/Edit Professor modal dialog.

    Renders fields for AM, password, email, first name, last name, and
    specialization.  The AM field is read-only when editing.

    Args:
        on_submit (Callable[[dict], None]): Callback invoked with form data
            on valid submission.
        initial_data (dict | None): Pre-populated values for edit mode.
            When None the dialog operates in add mode.

    Returns:
        ui.dialog: The fully constructed dialog element.
    """
    is_edit = initial_data is not None
    title = "Edit Professor" if is_edit else "Add Professor"
    data = initial_data or {}

    dialog, card = _buildDialogShell(title)
    with card:
        with ui.column().classes("w-full gap-3"):
            am_input = _buildField(
                "AM (Instructor ID)", "e.g. PROF001",
                value=data.get("AM", ""),
                required=not is_edit,
            )
            if is_edit:
                am_input.props("readonly")
                am_input.classes("opacity-60")

            first_input = _buildField(
                "First Name", value=data.get("FirstName", "")
            )
            last_input = _buildField(
                "Last Name", value=data.get("LastName", "")
            )
            email_input = _buildField(
                "Email", value=data.get("email", ""),
                rules=[lambda v: "@" in v or "Enter a valid email"],
            )
            spec_input = _buildField(
                "Specialization", value=data.get("Specialization", ""),
                required=False,
            )
            if not is_edit:
                pwd_input = _buildField("Password", password=True)
            else:
                pwd_input = None

        def _submit():
            """Collects field values and delegates to the provided callback."""
            payload = {
                "AM": am_input.value.strip(),
                "FirstName": first_input.value.strip(),
                "LastName": last_input.value.strip(),
                "email": email_input.value.strip(),
                "Specialization": spec_input.value.strip(),
            }
            if pwd_input:
                payload["Password"] = pwd_input.value
            on_submit(payload)
            dialog.close()

        _actionRow(_submit, dialog.close, submit_label="Save Professor")

    return dialog


# ---------------------------------------------------------------------------
# Course forms
# ---------------------------------------------------------------------------

def buildCourseDialog(
    on_submit: Callable[[dict], None],
    professor_options: list[dict],
    initial_data: dict | None = None,
) -> ui.dialog:
    """
    Constructs the Add/Edit Course modal dialog.

    Renders fields for course code, title, description, category, and an
    optional professor assignment select.  The C_Code field is read-only
    when editing an existing record.

    Args:
        on_submit (Callable[[dict], None]): Callback invoked with form data
            on valid submission.
        professor_options (list[dict]): List of professor dicts with at least
            'AM', 'FirstName', and 'LastName' keys for the select options.
        initial_data (dict | None): Pre-populated values for edit mode.
            When None the dialog operates in add mode.

    Returns:
        ui.dialog: The fully constructed dialog element.
    """
    is_edit = initial_data is not None
    title = "Edit Course" if is_edit else "Add Course"
    data = initial_data or {}

    dialog, card = _buildDialogShell(title)
    with card:
        with ui.column().classes("w-full gap-3"):
            code_input = _buildField(
                "Course Code", "e.g. CS101",
                value=data.get("C_Code", ""),
                required=not is_edit,
            )
            if is_edit:
                code_input.props("readonly")
                code_input.classes("opacity-60")

            title_input = _buildField(
                "Title", value=data.get("Title", "")
            )
            desc_input = (
                ui.textarea(label="Description", value=data.get("Description", "") or "")
                .classes("w-full")
                .props("outlined dark dense rows=3")
            )
            cat_input = _buildField(
                "Category", value=data.get("Category", ""), required=False
            )

            # Build professor select options list
            prof_choices = {"": "-- None --"}
            prof_choices.update({
                p["AM"]: f"{p['FirstName']} {p['LastName']} ({p['AM']})"
                for p in professor_options
            })
            prof_select = (
                ui.select(
                    options=prof_choices,
                    label="Assign Professor",
                    value=data.get("AM_Instructor", "") or "",
                )
                .classes("w-full")
                .props("outlined dark dense emit-value map-options")
            )

        def _submit():
            """Collects field values and delegates to the provided callback."""
            payload = {
                "C_Code": code_input.value.strip(),
                "Title": title_input.value.strip(),
                "Description": desc_input.value.strip() or None,
                "Category": cat_input.value.strip() or None,
                "AM_Instructor": prof_select.value or None,
            }
            on_submit(payload)
            dialog.close()

        _actionRow(_submit, dialog.close, submit_label="Save Course")

    return dialog


# ---------------------------------------------------------------------------
# Enrollment forms
# ---------------------------------------------------------------------------

def buildEnrollmentDialog(
    on_submit: Callable[[dict], None],
    student_options: list[dict],
    course_options: list[dict],
    initial_data: dict | None = None,
) -> ui.dialog:
    """
    Constructs the Add/Edit Enrollment modal dialog.

    Renders student and course selects along with a start date field.
    Both selects are read-only when editing an existing enrollment record.

    Args:
        on_submit (Callable[[dict], None]): Callback invoked with form data
            on valid submission.
        student_options (list[dict]): Student dicts with 'AM', 'FirstName',
            and 'LastName' keys.
        course_options (list[dict]): Course dicts with 'C_Code' and 'Title'
            keys.
        initial_data (dict | None): Pre-populated values for edit mode.
            When None the dialog operates in add mode.

    Returns:
        ui.dialog: The fully constructed dialog element.
    """
    is_edit = initial_data is not None
    title = "Edit Enrollment" if is_edit else "Add Enrollment"
    data = initial_data or {}

    dialog, card = _buildDialogShell(title)
    with card:
        with ui.column().classes("w-full gap-3"):
            student_choices = {
                s["AM"]: f"{s['FirstName']} {s['LastName']} ({s['AM']})"
                for s in student_options
            }
            student_select = (
                ui.select(
                    options=student_choices,
                    label="Student",
                    value=data.get("AM_Student"),
                )
                .classes("w-full")
                .props(
                    f"outlined dark dense emit-value map-options "
                    f"{'readonly' if is_edit else ''}"
                )
            )

            course_choices = {
                c["C_Code"]: f"{c['Title']} ({c['C_Code']})"
                for c in course_options
            }
            course_select = (
                ui.select(
                    options=course_choices,
                    label="Course",
                    value=data.get("C_Code"),
                )
                .classes("w-full")
                .props(
                    f"outlined dark dense emit-value map-options "
                    f"{'readonly' if is_edit else ''}"
                )
            )

            date_input = _buildField(
                "Start Date", "YYYY-MM-DD",
                value=data.get("StartDate", ""),
                rules=[
                    lambda v: (len(v) == 10 and v[4] == "-" and v[7] == "-")
                    or "Use YYYY-MM-DD format"
                ],
            )

        def _submit():
            """Collects field values and delegates to the provided callback."""
            payload = {
                "AM_Student": student_select.value,
                "C_Code": course_select.value,
                "StartDate": date_input.value.strip(),
            }
            on_submit(payload)
            dialog.close()

        _actionRow(_submit, dialog.close, submit_label="Save Enrollment")

    return dialog


# ---------------------------------------------------------------------------
# Evaluation forms
# ---------------------------------------------------------------------------

def buildEvaluationDialog(
    on_submit: Callable[[dict], None],
    instructor_options: list[dict],
    student_options: list[dict],
    course_options: list[dict],
    initial_data: dict | None = None,
) -> ui.dialog:
    """
    Constructs the Add/Edit Evaluation modal dialog.

    Renders selects for instructor, student, and course along with rating
    (1-10) and optional comments fields.  All three ID selects are read-only
    when editing an existing evaluation record.

    Args:
        on_submit (Callable[[dict], None]): Callback invoked with form data
            on valid submission.
        instructor_options (list[dict]): Instructor dicts with 'AM',
            'FirstName', and 'LastName' keys.
        student_options (list[dict]): Student dicts with 'AM', 'FirstName',
            and 'LastName' keys.
        course_options (list[dict]): Course dicts with 'C_Code' and 'Title'
            keys.
        initial_data (dict | None): Pre-populated values for edit mode.
            When None the dialog operates in add mode.

    Returns:
        ui.dialog: The fully constructed dialog element.
    """
    is_edit = initial_data is not None
    title = "Edit Evaluation" if is_edit else "Add Evaluation"
    data = initial_data or {}

    dialog, card = _buildDialogShell(title)
    with card:
        with ui.column().classes("w-full gap-3"):
            instr_choices = {
                i["AM"]: f"{i['FirstName']} {i['LastName']} ({i['AM']})"
                for i in instructor_options
            }
            instr_select = (
                ui.select(
                    options=instr_choices,
                    label="Instructor",
                    value=data.get("AM_Instructor"),
                )
                .classes("w-full")
                .props(
                    f"outlined dark dense emit-value map-options "
                    f"{'readonly' if is_edit else ''}"
                )
            )

            student_choices = {
                s["AM"]: f"{s['FirstName']} {s['LastName']} ({s['AM']})"
                for s in student_options
            }
            student_select = (
                ui.select(
                    options=student_choices,
                    label="Student",
                    value=data.get("AM_Student"),
                )
                .classes("w-full")
                .props(
                    f"outlined dark dense emit-value map-options "
                    f"{'readonly' if is_edit else ''}"
                )
            )

            course_choices = {
                c["C_Code"]: f"{c['Title']} ({c['C_Code']})"
                for c in course_options
            }
            course_select = (
                ui.select(
                    options=course_choices,
                    label="Course",
                    value=data.get("C_Code"),
                )
                .classes("w-full")
                .props(
                    f"outlined dark dense emit-value map-options "
                    f"{'readonly' if is_edit else ''}"
                )
            )

            # Rating slider (1-10)
            rating_value = {"v": int(data.get("Rating") or 5)}
            with ui.row().classes("w-full items-center gap-3"):
                ui.label("Rating").classes("text-white/70 text-sm w-16")
                rating_slider = (
                    ui.slider(min=1, max=10, step=1, value=rating_value["v"])
                    .classes("flex-1")
                    .props("dark label")
                )
                rating_label = ui.label(str(rating_value["v"])).classes(
                    "text-indigo-400 font-bold w-6 text-center"
                )
                rating_slider.on(
                    "update:modelValue",
                    lambda e: rating_label.set_text(str(int(e.args))),
                )

            comments_input = (
                ui.textarea(
                    label="Comments",
                    value=data.get("Comments", "") or "",
                )
                .classes("w-full")
                .props("outlined dark dense rows=3")
            )

        def _submit():
            """Collects field values and delegates to the provided callback."""
            payload = {
                "AM_Instructor": instr_select.value,
                "AM_Student": student_select.value,
                "C_Code": course_select.value,
                "Rating": int(rating_slider.value),
                "Comments": comments_input.value.strip() or None,
            }
            on_submit(payload)
            dialog.close()

        _actionRow(_submit, dialog.close, submit_label="Save Evaluation")

    return dialog


# ---------------------------------------------------------------------------
# Confirmation dialog
# ---------------------------------------------------------------------------

def buildConfirmDialog(
    message: str,
    on_confirm: Callable,
) -> ui.dialog:
    """
    Constructs a generic destructive-action confirmation dialog.

    Renders a warning message with Cancel and Confirm buttons.  The dialog
    is persistent so it cannot be dismissed by clicking outside.

    Args:
        message (str): The human-readable confirmation prompt.
        on_confirm (Callable): Callback invoked when the user clicks Confirm.

    Returns:
        ui.dialog: The constructed confirmation dialog element.
    """
    dialog = ui.dialog().props("persistent")
    with dialog:
        with ui.card().classes(
            "bg-[#1e1624] border border-red-500/20 rounded-2xl p-6 max-w-sm"
        ):
            with ui.row().classes("items-center gap-3 mb-3"):
                ui.icon("warning", size="1.5rem").classes("text-red-400")
                ui.label("Confirm Deletion").classes(
                    "text-white font-semibold text-base"
                )
            ui.label(message).classes("text-white/70 text-sm mb-4")
            with ui.row().classes("w-full justify-end gap-3"):
                ui.button("Cancel", on_click=dialog.close).props("flat").classes(
                    "text-white/60 hover:text-white/90 no-uppercase"
                )
                ui.button(
                    "Delete",
                    on_click=lambda: [on_confirm(), dialog.close()],
                ).classes(
                    "bg-red-600 hover:bg-red-500 text-white rounded-lg "
                    "px-5 py-2 no-uppercase font-medium transition-colors duration-200"
                )
    return dialog
