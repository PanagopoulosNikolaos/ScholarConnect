"""
src/app/ui/pages/auth.py

Authentication pages for the ScholarConnect web application.
Provides the login page UI and registration page UI, handling session
creation via NiceGUI's app.storage.user and delegating credential
validation to the database layer.
"""

from nicegui import ui, app
from src.api_actions import getStudent, getProfessor, addStudent, addProfessor


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _pageShell() -> None:
    """
    Applies the full-page dark background styling for auth screens.

    Sets the body background to match the application dark theme and
    prevents the default NiceGUI padding from interfering with the layout.
    """
    ui.add_head_html(
        "<style>"
        "  body { background: #0a0d14 !important; }"
        "  .nicegui-content { padding: 0 !important; }"
        "</style>"
    )


def _buildBrandBlock() -> None:
    """
    Renders the centered ScholarConnect brand header with icon and subtitle.

    Displays the application icon, name, and tagline above the auth card.
    """
    with ui.column().classes("items-center gap-2 mb-6"):
        ui.icon("school", size="3rem").classes("text-indigo-400")
        ui.label("ScholarConnect").classes(
            "text-white font-bold text-3xl tracking-tight"
        )
        ui.label("Academic Management Portal").classes(
            "text-white/40 text-sm"
        )


# ---------------------------------------------------------------------------
# Login page
# ---------------------------------------------------------------------------

def buildLoginPage() -> None:
    """
    Renders the login page for the ScholarConnect application.

    Presents a centered card with AM and password fields. On submission,
    looks up the AM in both STUDENT and INSTRUCTOR tables.  On success,
    writes 'authenticated', 'user_am', and 'user_role' to app.storage.user
    and redirects to the dashboard.  On failure, displays a notification.
    """
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
                """Validates credentials against the database and creates a session."""
                am = am_input.value.strip()
                pwd = pwd_input.value

                if not am or not pwd:
                    error_label.set_text("Please fill in all fields.")
                    error_label.classes(remove="hidden")
                    return

                # Admin bypass
                if am.lower() == "admin" and pwd == "admin":
                    app.storage.user["authenticated"] = True
                    app.storage.user["user_am"] = "admin"
                    app.storage.user["user_role"] = "admin"
                    ui.navigate.to("/dashboard")
                    return

                # Check student table first, then instructor table.
                record = getStudent(am)
                role = "student"
                if not record:
                    record = getProfessor(am)
                    role = "professor"

                if not record or record.get("Password") != pwd:
                    error_label.set_text("Invalid AM or password.")
                    error_label.classes(remove="hidden")
                    return

                # Persist session state in server-side user storage.
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


# ---------------------------------------------------------------------------
# Registration page
# ---------------------------------------------------------------------------

def buildRegisterPage() -> None:
    """
    Renders the registration page for the ScholarConnect application.

    Presents a form for new students to self-register.  On successful
    insertion, redirects the user to the login page.  Professors must be
    created by an admin via the Professors management page.
    """
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
                """Validates fields, calls addStudent, and navigates on success."""
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
