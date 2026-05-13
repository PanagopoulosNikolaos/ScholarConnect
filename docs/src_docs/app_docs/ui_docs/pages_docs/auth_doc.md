# auth.py Documentation

## Navigation Table

| Name | Type | Description |
|------|------|-------------|
| [_pageShell](#_pageshell) | Function | Applies the full-page dark background styling for auth screens. |
| [_buildBrandBlock](#_buildbrandblock) | Function | Renders the centered ScholarConnect brand header with icon and subtitle. |
| [buildLoginPage](#buildloginpage) | Function | Renders the login page for the ScholarConnect application. |
| [_doLogin](#_dologin) | Function | Validates credentials against the database and creates a session within login page. |
| [buildRegisterPage](#buildregisterpage) | Function | Renders the registration page for the ScholarConnect application. |
| [_doRegister](#_doregister) | Function | Validates fields, calls addStudent, and navigates on success within registration page. |

## Overview
Provides authentication pages for the ScholarConnect web application. Implements the login page UI and registration page UI, handling session creation via local storage and delegating credential validation to the underlying API database layer.

## Detailed Breakdown Section

### _pageShell

**Signature:**
```python
def _pageShell() -> None
```

**Purpose:** Applies the full-page dark background styling for auth screens.

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| None | — | — | — | — |

**Returns:**
| Type | Description |
|------|-------------|
| None | Executes a side effect that modifies page styling. |

**Source Code:**
```python
def _pageShell() -> None:
    ui.add_head_html(
        "<style>"
        "  body { background: #0a0d14 !important; }"
        "  .nicegui-content { padding: 0 !important; }"
        "</style>"
    )
```

**Implementation (Executable Logic Only):**
* **Line 2:** `ui.add_head_html(...)` — Appends raw CSS targeting the `body` and `.nicegui-content` classes to override default paddings and enforce a strict `#0a0d14` background color utilizing the `!important` modifier.

**Dependencies:**
| Symbol | Kind | Purpose | Source |
|--------|------|---------|--------|
| ui.add_head_html | External | Injecting CSS into the DOM head | nicegui |

---

### _buildBrandBlock

**Signature:**
```python
def _buildBrandBlock() -> None
```

**Purpose:** Renders the centered ScholarConnect brand header with icon and subtitle.

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| None | — | — | — | — |

**Returns:**
| Type | Description |
|------|-------------|
| None | Modifies the active UI layout context. |

**Source Code:**
```python
def _buildBrandBlock() -> None:
    with ui.column().classes("items-center gap-2 mb-6"):
        ui.icon("school", size="3rem").classes("text-indigo-400")
        ui.label("ScholarConnect").classes(
            "text-white font-bold text-3xl tracking-tight"
        )
        ui.label("Academic Management Portal").classes(
            "text-white/40 text-sm"
        )
```

**Implementation (Executable Logic Only):**
* **Line 2:** `with ui.column().classes("items-center gap-2 mb-6"):` — Creates a vertically aligned flex container centering its children.
* **Line 3-8:** Instantiates a large `school` icon in indigo, followed by bold title text, and a smaller, low-opacity subtitle description.

**Dependencies:**
| Symbol | Kind | Purpose | Source |
|--------|------|---------|--------|
| ui.column | External | Structural layout | nicegui |

---

### buildLoginPage

**Primary Library:** `nicegui`
**Purpose:** Renders the login page for the ScholarConnect application.

#### Overview
Builds the user authentication interface consisting of a centered card over a dark background. Instantiates username and password inputs, configures an error reporting label, and defines the validation logic executed upon form submission, interacting with both the student and professor data sources.

#### Signature
```python
def buildLoginPage() -> None
```

#### Parameters
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| None | — | — | — | — |

#### Returns
| Type | Description |
|------|-------------|
| None | Modifies the active page context. |

#### Dependencies
* **Required Libraries:** `nicegui` (UI rendering)
* **Internal Modules:** `_pageShell`, `_buildBrandBlock` (Layout), `getStudent`, `getProfessor` (Database queries)

#### Workflow (Executable Logic Only)

**Phase 1: Environment Setup**
Initializes the base styling and layout structure.
* **Operation 1:** Executes `_pageShell()` to establish the background context.
* **Operation 2:** Initializes a container column covering the entire viewport (`absolute inset-0 items-center justify-center`) and embeds the branding via `_buildBrandBlock()`.
* **Operation 3:** Opens a `ui.card()` containing the login components.

**Phase 2: Form Input Construction**
Renders the necessary text entry components and an invisible error container.
* **Operation 1:** Creates `am_input` for the username, applying `.props("outlined dark dense")` for styling.
* **Operation 2:** Creates `pwd_input` configured with `type=password` to mask input.
* **Operation 3:** Instantiates `error_label` with `.classes("... hidden")`, remaining invisible until triggered by validation failures.

**Phase 3: Logic Definition and Binding**
Creates the inline submission handler and binds it to the interface.
* **Operation 1:** Defines `_doLogin()` which extracts input values.
* **Operation 2:** Performs emptiness checks, un-hiding the `error_label` on failure.
* **Operation 3:** Provides a hardcoded admin bypass for 'admin' credentials.
* **Operation 4:** Queries `getStudent()`. If no record is found, checks `getProfessor()`. Evaluates the returned dictionary's password against the input.
* **Operation 5:** Writes `authenticated`, `user_am`, and `user_role` to `app.storage.user` upon success and executes `ui.navigate.to("/dashboard")`.
* **Operation 6:** Renders the primary submit button bound to `_doLogin`, followed by a link leading to the registration view.

#### Source Code
```python
def buildLoginPage() -> None:
    _pageShell()

    with ui.column().classes(
        "absolute inset-0 items-center justify-center"
    ):
        _buildBrandBlock()

        with ui.card().classes(
            "bg-[#161b27] border border-white/10 rounded-2xl p-8 w-full max-w-sm"
        ):
            ui.label("Sign In").classes(
                "text-white font-semibold text-xl mb-5"
            )

            am_input = (
                ui.input(label="AM / Username", placeholder="Your registration number")
                .classes("w-full")
                .props("outlined dark dense")
            )
            pwd_input = (
                ui.input(label="Password", placeholder="Your password")
                .classes("w-full mt-2")
                .props("outlined dark dense type=password")
            )

            error_label = ui.label("").classes(
                "text-red-400 text-xs mt-1 hidden"
            )

            def _doLogin() -> None:
                am = am_input.value.strip()
                pwd = pwd_input.value

                if not am or not pwd:
                    error_label.set_text("Please fill in all fields.")
                    error_label.classes(remove="hidden")
                    return

                if am.lower() == "admin" and pwd == "admin":
                    app.storage.user["authenticated"] = True
                    app.storage.user["user_am"] = "admin"
                    app.storage.user["user_role"] = "admin"
                    ui.navigate.to("/dashboard")
                    return

                record = getStudent(am)
                role = "student"
                if not record:
                    record = getProfessor(am)
                    role = "professor"

                if not record or record.get("Password") != pwd:
                    error_label.set_text("Invalid AM or password.")
                    error_label.classes(remove="hidden")
                    return

                app.storage.user["authenticated"] = True
                app.storage.user["user_am"] = am
                app.storage.user["user_role"] = role
                ui.navigate.to("/dashboard")

            ui.button("Sign In", on_click=_doLogin).classes(
                "w-full mt-5 bg-indigo-600 hover:bg-indigo-500 text-white "
                "rounded-lg py-3 no-uppercase font-semibold text-sm "
                "transition-colors duration-200"
            )

            with ui.row().classes("w-full justify-center mt-4"):
                ui.label("No account?").classes("text-white/40 text-xs")
                ui.link("Register here", "/register").classes(
                    "text-indigo-400 text-xs hover:text-indigo-300 ml-1"
                )
```

---

### buildRegisterPage

**Primary Library:** `nicegui`
**Purpose:** Renders the registration page for the ScholarConnect application.

#### Overview
Builds the user creation interface targeting new student enrollments. Accumulates necessary profile information, validates field completion and formatting, executes insertion into the database, and provides client-side notification routing back to the authentication sequence.

#### Signature
```python
def buildRegisterPage() -> None
```

#### Parameters
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| None | — | — | — | — |

#### Returns
| Type | Description |
|------|-------------|
| None | Modifies the active page context. |

#### Dependencies
* **Required Libraries:** `nicegui` (UI rendering)
* **Internal Modules:** `_pageShell`, `_buildBrandBlock` (Layout), `addStudent` (Database creation)

#### Workflow (Executable Logic Only)

**Phase 1: Interface Initialization**
Constructs layout structure.
* **Operation 1:** Executes `_pageShell()` and builds branding via `_buildBrandBlock()`.
* **Operation 2:** Initializes a dark-themed card container.

**Phase 2: Component Generation**
Populates the card with required input fields.
* **Operation 1:** Creates sequentially spaced inputs for AM, First Name, Last Name, and Email, applying `outlined dark dense` to match the application aesthetic.
* **Operation 2:** Appends the Password input configured to mask text.
* **Operation 3:** Prepares a hidden error reporting label.

**Phase 3: Validation and Submission Handling**
Defines execution logic on interaction.
* **Operation 1:** Creates `_doRegister()` which strips strings from all inputs.
* **Operation 2:** Evaluates the `all()` condition across inputs. If any are empty, updates the error label and un-hides it.
* **Operation 3:** Enforces a rudimentary email format check relying on the presence of an `@` character.
* **Operation 4:** Executes `addStudent()` via the API layer. Upon false, indicates a collision error. Upon true, triggers a `ui.notify` toast with `type="positive"` and navigates back to the root path `/` for authentication.

#### Source Code
```python
def buildRegisterPage() -> None:
    _pageShell()

    with ui.column().classes(
        "absolute inset-0 items-center justify-center py-10"
    ):
        _buildBrandBlock()

        with ui.card().classes(
            "bg-[#161b27] border border-white/10 rounded-2xl p-8 w-full max-w-sm"
        ):
            ui.label("Create Student Account").classes(
                "text-white font-semibold text-xl mb-5"
            )

            am_input = (
                ui.input(label="AM (Student ID)", placeholder="e.g. STU001")
                .classes("w-full")
                .props("outlined dark dense")
            )
            first_input = (
                ui.input(label="First Name")
                .classes("w-full mt-2")
                .props("outlined dark dense")
            )
            last_input = (
                ui.input(label="Last Name")
                .classes("w-full mt-2")
                .props("outlined dark dense")
            )
            email_input = (
                ui.input(label="Email")
                .classes("w-full mt-2")
                .props("outlined dark dense")
            )
            pwd_input = (
                ui.input(label="Password")
                .classes("w-full mt-2")
                .props("outlined dark dense type=password")
            )

            error_label = ui.label("").classes(
                "text-red-400 text-xs mt-1 hidden"
            )

            def _doRegister() -> None:
                am = am_input.value.strip()
                first = first_input.value.strip()
                last = last_input.value.strip()
                email = email_input.value.strip()
                pwd = pwd_input.value

                if not all([am, first, last, email, pwd]):
                    error_label.set_text("All fields are required.")
                    error_label.classes(remove="hidden")
                    return

                if "@" not in email:
                    error_label.set_text("Enter a valid email address.")
                    error_label.classes(remove="hidden")
                    return

                success = addStudent(
                    AM=am, Password=pwd, email=email,
                    FirstName=first, LastName=last
                )
                if not success:
                    error_label.set_text(
                        "Registration failed. AM or email may already exist."
                    )
                    error_label.classes(remove="hidden")
                    return

                ui.notify(
                    "Account created. Please sign in.",
                    type="positive",
                    position="top",
                )
                ui.navigate.to("/")

            ui.button("Register", on_click=_doRegister).classes(
                "w-full mt-5 bg-indigo-600 hover:bg-indigo-500 text-white "
                "rounded-lg py-3 no-uppercase font-semibold text-sm "
                "transition-colors duration-200"
            )

            with ui.row().classes("w-full justify-center mt-4"):
                ui.label("Already have an account?").classes(
                    "text-white/40 text-xs"
                )
                ui.link("Sign in", "/").classes(
                    "text-indigo-400 text-xs hover:text-indigo-300 ml-1"
                )
```
