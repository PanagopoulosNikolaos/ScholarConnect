# forms.py Documentation

## Navigation Table

| Name | Type | Description |
|------|------|-------------|
| [_buildDialogShell](#_builddialogshell) | Function | Creates the base dark-themed dialog shell with a title header. |
| [_buildField](#_buildfield) | Function | Renders a single dark-styled form input field. |
| [_actionRow](#_actionrow) | Function | Renders the dialog's cancel / submit button row. |
| [buildStudentDialog](#buildstudentdialog) | Function | Constructs the Add/Edit Student modal dialog. |
| [_submit](#_submit) | Function | Collects field values and delegates to the provided callback within student dialog. |
| [buildProfessorDialog](#buildprofessordialog) | Function | Constructs the Add/Edit Professor modal dialog. |
| [_submit](#_submit-1) | Function | Collects field values and delegates to the provided callback within professor dialog. |
| [buildCourseDialog](#buildcoursedialog) | Function | Constructs the Add/Edit Course modal dialog. |
| [_submit](#_submit-2) | Function | Collects field values and delegates to the provided callback within course dialog. |
| [buildEnrollmentDialog](#buildenrollmentdialog) | Function | Constructs the Add/Edit Enrollment modal dialog. |
| [_submit](#_submit-3) | Function | Collects field values and delegates to the provided callback within enrollment dialog. |
| [buildEvaluationDialog](#buildevaluationdialog) | Function | Constructs the Add/Edit Evaluation modal dialog. |
| [_submit](#_submit-4) | Function | Collects field values and delegates to the provided callback within evaluation dialog. |
| [buildConfirmDialog](#buildconfirmdialog) | Function | Constructs a generic destructive-action confirmation dialog. |

## Overview
Provides reusable modal dialog forms for ScholarConnect CRUD operations. Contains builder functions for Add/Edit dialogs for each entity type, encapsulating field layout, validation rules, and submit handling. Designed to apply specific dark-theme CSS classes and UI properties consistently across all components.

## Detailed Breakdown Section

### _buildDialogShell

**Signature:**
```python
def _buildDialogShell(title: str) -> tuple[ui.dialog, ui.card]
```

**Purpose:** Creates the base dark-themed dialog shell with a title header.

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| title | str | Yes | — | The heading text displayed at the top of the dialog. |

**Returns:**
| Type | Description |
|------|-------------|
| tuple[ui.dialog, ui.card] | The dialog and its inner card container. |

**Source Code:**
```python
def _buildDialogShell(title: str) -> tuple[ui.dialog, ui.card]:
    dialog = ui.dialog().props("persistent")
    with dialog:
        card = ui.card().classes(
            "bg-[#161b27] border border-white/10 rounded-2xl p-6 w-full max-w-lg"
        )
        with card:
            ui.label(title).classes("text-white font-semibold text-lg mb-4")
    return dialog, card
```

**Implementation (Executable Logic Only):**
* **Line 1:** `def _buildDialogShell(title: str) -> tuple[ui.dialog, ui.card]:` — Initializes dialog creation.
* **Line 2:** `dialog = ui.dialog().props("persistent")` — Instantiates a UI dialog with the `persistent` property, disabling the ability to close the dialog by clicking outside of its boundaries.
* **Line 3:** `with dialog:` — Opens the dialog context.
* **Line 4:** `card = ui.card().classes(...)` — Appends a card inside the dialog. The classes `bg-[#161b27]` sets a dark background color, `border border-white/10` adds a subtle border, `rounded-2xl` applies rounded corners, `p-6` sets padding, and `w-full max-w-lg` ensures the dialog expands fully up to a maximum large width.
* **Line 7:** `with card:` — Opens the card context.
* **Line 8:** `ui.label(title).classes("text-white font-semibold text-lg mb-4")` — Adds the title label with styling for visibility and spacing.
* **Line 9:** `return dialog, card` — Returns both references for further content injection.

**Dependencies:**
| Symbol | Kind | Purpose | Source |
|--------|------|---------|--------|
| ui.dialog | External | UI component initialization | nicegui |
| ui.card | External | UI component initialization | nicegui |
| ui.label | External | UI component initialization | nicegui |

---

### _buildField

**Primary Library:** `nicegui`
**Purpose:** Renders a single dark-styled form input field.

#### Overview
Configures and returns a text input field tailored for dark mode. Applies validation rules conditionally based on field requirements and handles specific input types such as passwords.

#### Signature
```python
def _buildField(
    label: str,
    placeholder: str = "",
    value: str = "",
    rules: list | None = None,
    password: bool = False,
    required: bool = True,
) -> ui.input
```

#### Parameters
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| label | str | Yes | — | The field label shown above the input. |
| placeholder | str | No | "" | Placeholder text inside the input. |
| value | str | No | "" | Pre-filled value for edit dialogs. |
| rules | list \| None | No | None | NiceGUI validation rule list. |
| password | bool | No | False | Renders the field as a password type when True. |
| required | bool | No | True | Appends a required validator when True. |

#### Returns
| Type | Description |
|------|-------------|
| ui.input | The constructed NiceGUI input element configured with specified properties. |

#### Dependencies
* **Required Libraries:** `nicegui` (UI rendering)

#### Workflow (Executable Logic Only)

**Phase 1: Validation Setup**
Initializes the rule set for the input field.
* **Operation 1:** Copies provided rules into `effective_rules` to prevent mutating the default argument.
* **Operation 2:** If `required` is true, injects a lambda function at the start of the list that verifies the string is not empty after stripping whitespace, ensuring mandatory fields are filled.

**Phase 2: Input Field Instantiation**
Creates the input component with appropriate styling and typing.
* **Operation 1:** Calls `ui.input()` with the provided label, placeholder, and initial value.
* **Operation 2:** Applies `.classes("w-full")` to ensure the input expands to fill its container width.
* **Operation 3:** Applies `.props(...)`. The `outlined` property surrounds the input with a border, `dark` adapts internal colors for dark backgrounds, `dense` reduces vertical padding, and `type=password` is conditionally added to obscure text input for sensitive data.

**Phase 3: Rule Application**
Binds the computed rules to the input instance.
* **Operation 1:** Assigns `effective_rules[0]` to the input's validation dictionary, linking the visual validation state to the required conditions.

#### Source Code
```python
def _buildField(
    label: str,
    placeholder: str = "",
    value: str = "",
    rules: list | None = None,
    password: bool = False,
    required: bool = True,
) -> ui.input:
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
```

---

### _actionRow

**Primary Library:** `nicegui`
**Purpose:** Renders the dialog's cancel / submit button row.

#### Overview
Establishes the interactive footer of a modal dialog. Contains buttons for submission and cancellation, applying specific utility classes to regulate layout, color contrast, and interactive behaviors according to modern UI patterns.

#### Signature
```python
def _actionRow(
    on_submit: Callable,
    on_cancel: Callable,
    submit_label: str = "Save",
) -> None
```

#### Parameters
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| on_submit | Callable | Yes | — | Invoked when the submit button is clicked. |
| on_cancel | Callable | Yes | — | Invoked when the cancel button is clicked. |
| submit_label | str | No | "Save" | Label text for the submit button. |

#### Returns
| Type | Description |
|------|-------------|
| None | Performs UI manipulation without returning objects. |

#### Dependencies
* **Required Libraries:** `nicegui` (UI rendering)

#### Workflow (Executable Logic Only)

**Phase 1: Container Initialization**
Creates a horizontally aligned container for the buttons.
* **Operation 1:** Instantiates a `ui.row()` with classes `w-full justify-end gap-3 mt-4`. This combination ensures the row spans the container (`w-full`), aligns children to the right edge (`justify-end`), spaces them uniformly (`gap-3`), and applies top margin (`mt-4`) to separate it from the form fields.

**Phase 2: Cancel Button Definition**
Renders the secondary dismissal action.
* **Operation 1:** Instantiates the 'Cancel' button, binding `on_click` to the provided `on_cancel` callback.
* **Operation 2:** Applies the `.props("flat")` property, which removes the default button background and border, presenting a minimalist appearance that de-emphasizes the action compared to the primary submit button.
* **Operation 3:** Applies `.classes("text-white/60 hover:text-white/90 no-uppercase")`. `text-white/60` sets the default text color to a semi-transparent white (60% opacity), which brightens to 90% opacity (`hover:text-white/90`) when the mouse cursor enters the element bounds. The `no-uppercase` class overrides the default Quasar framework behavior, preserving standard title-case capitalization.

**Phase 3: Submit Button Definition**
Renders the primary confirmation action.
* **Operation 1:** Instantiates the submit button, binding `on_click` to the provided `on_submit` callback.
* **Operation 2:** Applies `.classes(...)` which configures a solid background color (`bg-indigo-600`) that changes shade on interaction (`hover:bg-indigo-500`), rounded corners (`rounded-lg`), internal spacing (`px-5 py-2`), and an animation timing curve (`transition-colors duration-200`) to ensure state transitions appear smooth.

#### Source Code
```python
def _actionRow(
    on_submit: Callable,
    on_cancel: Callable,
    submit_label: str = "Save",
) -> None:
    with ui.row().classes("w-full justify-end gap-3 mt-4"):
        ui.button("Cancel", on_click=on_cancel).props(
            "flat"
        ).classes("text-white/60 hover:text-white/90 no-uppercase")
        ui.button(submit_label, on_click=on_submit).classes(
            "bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg "
            "px-5 py-2 no-uppercase font-medium transition-colors duration-200"
        )
```

---

### buildStudentDialog

**Primary Library:** `nicegui`
**Purpose:** Constructs the Add/Edit Student modal dialog.

#### Overview
Builds a cohesive data entry form for student records. Adapts its field requirements and read-only states dynamically based on whether it is initializing a new record or modifying an existing one. Contains an internal submission handler to extract state from input components.

#### Signature
```python
def buildStudentDialog(
    on_submit: Callable[[dict], None],
    initial_data: dict | None = None,
) -> ui.dialog
```

#### Parameters
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| on_submit | Callable[[dict], None] | Yes | — | Callback invoked with the form data dict on a valid submission. |
| initial_data | dict \| None | No | None | Pre-populated values for edit mode. |

#### Returns
| Type | Description |
|------|-------------|
| ui.dialog | The fully constructed dialog element containing the form. |

#### Dependencies
* **Required Libraries:** `nicegui` (UI rendering)
* **Internal Modules:** `_buildDialogShell`, `_buildField`, `_actionRow` (Form components)

#### Workflow (Executable Logic Only)

**Phase 1: Dialog Initialization**
Sets up the dialog container and determines operation mode.
* **Operation 1:** Evaluates `initial_data is not None` to set `is_edit`, determining if the dialog is in creation or modification mode.
* **Operation 2:** Initializes the shell using `_buildDialogShell()` with the appropriate title.

**Phase 2: Input Field Population**
Constructs all necessary input fields using `_buildField()`.
* **Operation 1:** Instantiates the 'AM' (Student ID) field. If `is_edit` is True, applies `.props("readonly")` and `.classes("opacity-60")` to prevent modification of the primary key and visually indicate its immutable state.
* **Operation 2:** Instantiates 'First Name' and 'Last Name' fields with any available initial data.
* **Operation 3:** Instantiates the 'Email' field, passing a custom lambda rule `lambda v: "@" in v` to enforce rudimentary email formatting.
* **Operation 4:** Conditionally adds a 'Password' field only if the dialog is in creation mode (`not is_edit`), configuring it as a secure password input.

**Phase 3: Action Binding**
Defines the submission logic and attaches it to the action row.
* **Operation 1:** Defines an internal `_submit()` function that constructs a dictionary from the current `.value` attributes of all instantiated fields, applying `.strip()` to remove leading/trailing whitespace.
* **Operation 2:** Executes `_actionRow()` passing the internal `_submit` function and `dialog.close` to wire the form buttons.

#### Source Code
```python
def buildStudentDialog(
    on_submit: Callable[[dict], None],
    initial_data: dict | None = None,
) -> ui.dialog:
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
            payload = {
                "AM": am_input.value.strip() if am_input.value else "",
                "FirstName": first_input.value.strip() if first_input.value else "",
                "LastName": last_input.value.strip() if last_input.value else "",
                "email": email_input.value.strip() if email_input.value else "",
            }
            if pwd_input:
                payload["Password"] = pwd_input.value
            on_submit(payload)
            dialog.close()

        _actionRow(_submit, dialog.close, submit_label="Save Student")

    return dialog
```

---

### buildProfessorDialog

**Primary Library:** `nicegui`
**Purpose:** Constructs the Add/Edit Professor modal dialog.

#### Overview
Builds the UI component responsible for professor record creation and editing. Implements conditional logic to handle primary key immutability and aggregates user input into a standardized payload.

#### Signature
```python
def buildProfessorDialog(
    on_submit: Callable[[dict], None],
    initial_data: dict | None = None,
) -> ui.dialog
```

#### Parameters
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| on_submit | Callable[[dict], None] | Yes | — | Callback invoked with form data on valid submission. |
| initial_data | dict \| None | No | None | Pre-populated values for edit mode. |

#### Returns
| Type | Description |
|------|-------------|
| ui.dialog | The fully constructed dialog element. |

#### Dependencies
* **Required Libraries:** `nicegui` (UI rendering)
* **Internal Modules:** `_buildDialogShell`, `_buildField`, `_actionRow` (Form components)

#### Workflow (Executable Logic Only)

**Phase 1: Dialog Initialization**
Sets up the base layout and context.
* **Operation 1:** Determines `is_edit` status based on the presence of `initial_data`.
* **Operation 2:** Initializes the base card structure via `_buildDialogShell()`.

**Phase 2: Field Instantiation**
Adds inputs for professor-specific attributes.
* **Operation 1:** Creates 'AM (Instructor ID)' input. If `is_edit` is True, disables editing by applying `readonly` and visual fading (`opacity-60`).
* **Operation 2:** Instantiates text inputs for standard fields including 'First Name', 'Last Name', 'Email', and 'Specialization'.
* **Operation 3:** Appends a 'Password' field only during record creation.

**Phase 3: Payload Compilation**
Defines the submission routine.
* **Operation 1:** Implements an internal `_submit()` closure capturing the input component references.
* **Operation 2:** Constructs a dictionary containing the `.value` strings, parsing them and appending the password field if available.
* **Operation 3:** Triggers `on_submit` and closes the modal.

#### Source Code
```python
def buildProfessorDialog(
    on_submit: Callable[[dict], None],
    initial_data: dict | None = None,
) -> ui.dialog:
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
            payload = {
                "AM": am_input.value.strip() if am_input.value else "",
                "FirstName": first_input.value.strip() if first_input.value else "",
                "LastName": last_input.value.strip() if last_input.value else "",
                "email": email_input.value.strip() if email_input.value else "",
                "Specialization": spec_input.value.strip() if spec_input.value else None,
            }
            if pwd_input:
                payload["Password"] = pwd_input.value
            on_submit(payload)
            dialog.close()

        _actionRow(_submit, dialog.close, submit_label="Save Professor")

    return dialog
```

---

### buildCourseDialog

**Primary Library:** `nicegui`
**Purpose:** Constructs the Add/Edit Course modal dialog.

#### Overview
Generates the form for managing academic courses, including standard text inputs, text areas for descriptions, and a mapped selection dropdown for assigning an instructor.

#### Signature
```python
def buildCourseDialog(
    on_submit: Callable[[dict], None],
    professor_options: list[dict],
    initial_data: dict | None = None,
) -> ui.dialog
```

#### Parameters
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| on_submit | Callable[[dict], None] | Yes | — | Callback invoked with form data on valid submission. |
| professor_options | list[dict] | Yes | — | List of professor dicts for the select options. |
| initial_data | dict \| None | No | None | Pre-populated values for edit mode. |

#### Returns
| Type | Description |
|------|-------------|
| ui.dialog | The fully constructed dialog element. |

#### Dependencies
* **Required Libraries:** `nicegui` (UI rendering)
* **Internal Modules:** `_buildDialogShell`, `_buildField`, `_actionRow` (Form components)

#### Workflow (Executable Logic Only)

**Phase 1: Foundation Setup**
Prepares dialog context.
* **Operation 1:** Determines boolean `is_edit` state.
* **Operation 2:** Initializes the visual shell container using `_buildDialogShell`.

**Phase 2: Standard Inputs**
Adds simple field components.
* **Operation 1:** Creates the 'Course Code' input, locking it as read-only if modifying an existing course.
* **Operation 2:** Creates the 'Title' input.
* **Operation 3:** Initializes a `ui.textarea` for 'Description', applying `outlined dark dense rows=3` properties for multiline capacity.

**Phase 3: Dropdown Construction**
Formats and creates the assignment selector.
* **Operation 1:** Constructs a `prof_choices` dictionary mapping `AM` keys to formatted display strings encompassing the professor's full name and ID.
* **Operation 2:** Instantiates `ui.select()` with the constructed options. The `emit-value map-options` properties configure the component to display the formatted string to the user but return the underlying `AM` key value programmatically.

**Phase 4: Submission Processing**
Creates the closure to handle form completion.
* **Operation 1:** Constructs a payload dictionary by extracting and stripping values.
* **Operation 2:** Invokes `on_submit` and closes the modal using `_actionRow`.

#### Source Code
```python
def buildCourseDialog(
    on_submit: Callable[[dict], None],
    professor_options: list[dict],
    initial_data: dict | None = None,
) -> ui.dialog:
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
            payload = {
                "C_Code": code_input.value.strip() if code_input.value else "",
                "Title": title_input.value.strip() if title_input.value else "",
                "Description": desc_input.value.strip() if desc_input.value else None,
                "Category": cat_input.value.strip() if cat_input.value else None,
                "AM_Instructor": prof_select.value or None,
            }
            on_submit(payload)
            dialog.close()

        _actionRow(_submit, dialog.close, submit_label="Save Course")

    return dialog
```

---

### buildEnrollmentDialog

**Primary Library:** `nicegui`
**Purpose:** Constructs the Add/Edit Enrollment modal dialog.

#### Overview
Renders the form linking a student to a course via selection components, parsing and enforcing correct date format validation. Employs read-only properties to prevent modifying the relational keys after initial creation.

#### Signature
```python
def buildEnrollmentDialog(
    on_submit: Callable[[dict], None],
    student_options: list[dict],
    course_options: list[dict],
    initial_data: dict | None = None,
) -> ui.dialog
```

#### Parameters
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| on_submit | Callable[[dict], None] | Yes | — | Callback invoked with form data on valid submission. |
| student_options | list[dict] | Yes | — | Student dicts with 'AM', 'FirstName', and 'LastName' keys. |
| course_options | list[dict] | Yes | — | Course dicts with 'C_Code' and 'Title' keys. |
| initial_data | dict \| None | No | None | Pre-populated values for edit mode. |

#### Returns
| Type | Description |
|------|-------------|
| ui.dialog | The fully constructed dialog element. |

#### Dependencies
* **Required Libraries:** `nicegui` (UI rendering)
* **Internal Modules:** `_buildDialogShell`, `_buildField`, `_actionRow` (Form components)

#### Workflow (Executable Logic Only)

**Phase 1: Dialog Instantiation**
Begins dialog building.
* **Operation 1:** Determines mode based on `initial_data` and executes `_buildDialogShell()`.

**Phase 2: Relational Selectors Construction**
Generates mapping lists and dropdown UI items.
* **Operation 1:** Constructs the `student_choices` mapping dictionary and instantiates `ui.select()`. Conditionally applies the `readonly` property within its `.props()` method if `is_edit` is True.
* **Operation 2:** Constructs the `course_choices` mapping dictionary and instantiates `ui.select()`, also conditionally enforcing `readonly`.

**Phase 3: Date Validation Configuration**
Applies specific formatting rules for string-based date entry.
* **Operation 1:** Invokes `_buildField()` for the Start Date. Injects a lambda rule ensuring length equals 10 and hyphens appear at indexes 4 and 7, validating the `YYYY-MM-DD` ISO format.

**Phase 4: Submission State Extraction**
Finalizes and wires submission.
* **Operation 1:** Defines `_submit()` to extract values, triggering `on_submit` callback.
* **Operation 2:** Adds the submit button row.

#### Source Code
```python
def buildEnrollmentDialog(
    on_submit: Callable[[dict], None],
    student_options: list[dict],
    course_options: list[dict],
    initial_data: dict | None = None,
) -> ui.dialog:
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
            payload = {
                "AM_Student": student_select.value,
                "C_Code": course_select.value,
                "StartDate": date_input.value.strip() if date_input.value else "",
            }
            on_submit(payload)
            dialog.close()

        _actionRow(_submit, dialog.close, submit_label="Save Enrollment")

    return dialog
```

---

### buildEvaluationDialog

**Primary Library:** `nicegui`
**Purpose:** Constructs the Add/Edit Evaluation modal dialog.

#### Overview
Builds the performance review interface. Uses multiple relation selectors alongside an interactive slider element for numerical ranking, implementing a mutable rating label connected to slider events. Selectors are configured with input filtering to handle large entity sets efficiently.

#### Signature
```python
def buildEvaluationDialog(
    on_submit: Callable[[dict], None],
    instructor_options: list[dict],
    student_options: list[dict],
    course_options: list[dict],
    initial_data: dict | None = None,
) -> ui.dialog
```

#### Parameters
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| on_submit | Callable[[dict], None] | Yes | — | Callback invoked with form data on valid submission. |
| instructor_options | list[dict] | Yes | — | Instructor dicts with 'AM', 'FirstName', and 'LastName' keys. |
| student_options | list[dict] | Yes | — | Student dicts with 'AM', 'FirstName', and 'LastName' keys. |
| course_options | list[dict] | Yes | — | Course dicts with 'C_Code' and 'Title' keys. |
| initial_data | dict \| None | No | None | Pre-populated values for edit mode. |

#### Returns
| Type | Description |
|------|-------------|
| ui.dialog | The fully constructed dialog element. |

#### Dependencies
* **Required Libraries:** `nicegui` (UI rendering)
* **Internal Modules:** `_buildDialogShell`, `_buildField`, `_actionRow` (Form components)

#### Workflow (Executable Logic Only)

**Phase 1: Standard Initialization**
Sets up base structure.
* **Operation 1:** Determines edit mode and starts the shell.

**Phase 2: Entity Selection Lists**
Constructs three primary relational dropdowns for Instructor, Student, and Course entities.
* **Operation 1:** Maps `instructor_options` to `ui.select`. The `with_input=True` property is enabled to allow user filtering via text input. The component is set to `readonly` if the dialog is in edit mode.
* **Operation 2:** Maps `student_options` to `ui.select` with `with_input=True` for filtering and conditional `readonly` state.
* **Operation 3:** Maps `course_options` to `ui.select` with `with_input=True` for filtering and conditional `readonly` state.

**Phase 3: Interactive Slider Logic**
Implements a 1-10 range slider with dynamic text updates.
* **Operation 1:** Encapsulates the initial integer rating in a `rating_value` dictionary.
* **Operation 2:** Instantiates `ui.slider()` with bounds `min=1` and `max=10`.
* **Operation 3:** Creates a static `ui.label()` component to display the current selection.
* **Operation 4:** Binds a callback to the slider's `update:modelValue` event to execute `rating_label.set_text()`, ensuring real-time display updates.

**Phase 4: Submission Handling**
Completes the form structure and defines retrieval logic.
* **Operation 1:** Configures a `ui.textarea` for subjective review comments.
* **Operation 2:** Defines an internal `_submit()` closure that collects the current values from selectors and the slider, ensuring keys (AM / C_Code) are correctly captured.
* **Operation 3:** Integrates `_actionRow()` to finalize the layout.

#### Source Code
```python
def buildEvaluationDialog(
    on_submit: Callable[[dict], None],
    instructor_options: list[dict],
    student_options: list[dict],
    course_options: list[dict],
    initial_data: dict | None = None,
) -> ui.dialog:
    is_edit = initial_data is not None
    title = "Edit Evaluation" if is_edit else "Add Evaluation"
    data = initial_data or {}

    dialog, card = _buildDialogShell(title)
    with card:
        with ui.column().classes("w-full gap-3"):
            
            # INSTRUCTOR SELECT
            instr_choices = {
                i["AM"]: f"{i['FirstName']} {i['LastName']} ({i['AM']})"
                for i in instructor_options
            }
            instr_select = (
                ui.select(
                    options=instr_choices,
                    label="Instructor",
                    value=data.get("AM_Instructor"),
                    with_input=True, # Allows typing to filter options
                )
                .classes("w-full")
                .props(
                    f"outlined dark dense "
                    f"{'readonly' if is_edit else ''}"
                )
            )

            # STUDENT SELECT
            student_choices = {
                s["AM"]: f"{s['FirstName']} {s['LastName']} ({s['AM']})"
                for s in student_options
            }
            student_select = (
                ui.select(
                    options=student_choices,
                    label="Student",
                    value=data.get("AM_Student"),
                    with_input=True, # Allows typing to filter options
                )
                .classes("w-full")
                .props(
                    f"outlined dark dense "
                    f"{'readonly' if is_edit else ''}"
                )
            )

            # COURSE SELECT
            course_choices = {
                c["C_Code"]: f"{c['Title']} ({c['C_Code']})"
                for c in course_options
            }
            course_select = (
                ui.select(
                    options=course_choices,
                    label="Course",
                    value=data.get("C_Code"),
                    with_input=True, # Allows typing to filter options
                )
                .classes("w-full")
                .props(
                    f"outlined dark dense "
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
            # These values will now correctly return the dictionary keys (AM / C_Code)
            payload = {
                "AM_Instructor": instr_select.value,
                "AM_Student": student_select.value,
                "C_Code": course_select.value,
                "Rating": int(rating_slider.value),
                "Comments": comments_input.value.strip() if comments_input.value else None,
            }
            on_submit(payload)
            dialog.close()

        _actionRow(_submit, dialog.close, submit_label="Save Evaluation")

    return dialog
```

---

### buildConfirmDialog

**Primary Library:** `nicegui`
**Purpose:** Constructs a generic destructive-action confirmation dialog.

#### Overview
Generates an alert modal styled for potentially destructive actions (e.g., deletion). Restricts closure by background clicking and implements an integrated callback closure method that ensures destruction occurs simultaneously with window dismissal.

#### Signature
```python
def buildConfirmDialog(
    message: str,
    on_confirm: Callable,
) -> ui.dialog
```

#### Parameters
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| message | str | Yes | — | The human-readable confirmation prompt. |
| on_confirm | Callable | Yes | — | Callback invoked when the user clicks Confirm. |

#### Returns
| Type | Description |
|------|-------------|
| ui.dialog | The constructed confirmation dialog element. |

#### Dependencies
* **Required Libraries:** `nicegui` (UI rendering)

#### Workflow (Executable Logic Only)

**Phase 1: Card Configuration**
Generates the base visual environment indicating alert/danger state.
* **Operation 1:** Creates a dialog with `props("persistent")` to require explicit button interaction to dismiss.
* **Operation 2:** Initializes a `ui.card()` applying `bg-[#1e1624] border-red-500/20` classes to establish a subtle red-tinted dark background signaling caution.

**Phase 2: Content Rendering**
Constructs visual warning indicators.
* **Operation 1:** Combines a warning icon (`text-red-400`) and a bold "Confirm Deletion" header.
* **Operation 2:** Appends the dynamic `message` argument as secondary text using `text-white/70`.

**Phase 3: Action Button Specification**
Implements localized buttons distinct from standard form flows.
* **Operation 1:** Defines a Cancel button executing `dialog.close`, styled minimally via the `.props("flat")` property, which omits background color, and `.classes("text-white/60 hover:text-white/90 no-uppercase")` to provide semi-transparent white text that becomes solid on interaction, with disabled title casing.
* **Operation 2:** Defines a Delete button. Implements `on_click=lambda: [on_confirm(), dialog.close()]` which executes an inline array containing two calls, synchronously invoking the provided destruction callback and immediately closing the modal.
* **Operation 3:** Applies `.classes(...)` using `bg-red-600 hover:bg-red-500` to emphatically color the primary action button red, enforcing the danger indication context.

#### Source Code
```python
def buildConfirmDialog(
    message: str,
    on_confirm: Callable,
) -> ui.dialog:
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
```
