"""
src/app/ui/pages/dashboard.py

Dashboard page for the ScholarConnect web application.
Displays high-level system statistics as metric cards and provides
quick-action shortcuts to navigate to the primary entity management pages.
"""

from nicegui import ui, app
from src.api_actions import (
    listStudents,
    listProfessors,
    listCourses,
    listEnrollments,
    listEvaluations,
    getStudent,
    getProfessor,
)
from src.app.ui.components.sidebar import buildSidebar


def buildDashboardPage() -> None:
    """
    Renders the dashboard page layout with statistics cards and navigation.

    Fetches live counts from the database for students, professors, courses,
    enrollments, and evaluations, then renders each as a metric card inside a
    responsive grid.  Wraps the content in the shared sidebar navigation.
    """
    # Fetch all counts up-front to minimise repeated DB connections.
    students = listStudents()
    professors = listProfessors()
    courses = listCourses()
    enrollments = listEnrollments()
    evaluations = listEvaluations()

    # Role-based filtering
    role = app.storage.user.get("user_role", "student")
    user_am = app.storage.user.get("user_am", "")
    
    # Calculate filtered metrics
    my_enrollments = enrollments
    my_evals = evaluations
    
    if role == "student":
        my_enrollments = [e for e in enrollments if e["AM_Student"] == user_am]
        my_evals = [e for e in evaluations if e["AM_Student"] == user_am]
    elif role == "professor":
        my_evals = [e for e in evaluations if e["AM_Instructor"] == user_am]

    # Compute average rating from non-null evaluation records.
    ratings = [e["Rating"] for e in my_evals if e.get("Rating") is not None]
    avg_rating = round(sum(ratings) / len(ratings), 1) if ratings else 0.0

    buildSidebar()

    with ui.column().classes("w-full min-h-screen bg-transparent p-8 gap-8"):
        # Page header
        with ui.column().classes("gap-1"):
            # Welcome message
            display_name = user_am
            if role == "student":
                rec = getStudent(user_am)
                if rec:
                    display_name = f"{rec.get('FirstName', '')} {rec.get('LastName', '')} ({user_am})"
            elif role == "professor":
                rec = getProfessor(user_am)
                if rec:
                    display_name = f"{rec.get('FirstName', '')} {rec.get('LastName', '')} ({user_am})"
            elif role == "admin":
                display_name = "Administrator"

            ui.label(f"Welcome, {display_name}").classes(
                "text-indigo-400 font-semibold text-sm uppercase tracking-wider mb-[-4px]"
            )
            ui.label("Dashboard").classes(
                "text-white font-bold text-3xl tracking-tight"
            )
            ui.label("System overview and key metrics.").classes(
                "text-white/40 text-sm"
            )

        # KPI metric cards grid
        _buildMetricGrid(
            students=len(students),
            professors=len(professors),
            courses=len(courses),
            enrollments=len(my_enrollments),
            evaluations=len(my_evals),
            avg_rating=avg_rating,
        )

        # Quick-action shortcuts
        _buildQuickActions()


def _buildMetricGrid(
    students: int,
    professors: int,
    courses: int,
    enrollments: int,
    evaluations: int,
    avg_rating: float,
) -> None:
    """
    Renders a responsive grid of KPI metric cards.

    Each card displays an icon, a numeric value, and a label.  Cards use a
    subtle gradient accent to provide visual distinction.

    Args:
        students (int): Total number of student records.
        professors (int): Total number of instructor records.
        courses (int): Total number of course records.
        enrollments (int): Total number of enrollment records.
        evaluations (int): Total number of evaluation records.
        avg_rating (float): Average rating across all evaluations.
    """
    cards = [
        ("group", str(students), "Students", "#6366f1", "/students"),
        ("person", str(professors), "Professors", "#8b5cf6", "/professors"),
        ("menu_book", str(courses), "Courses", "#3b82f6", "/courses"),
        ("assignment", str(enrollments), "Enrollments", "#06b6d4", "/enrollments"),
        ("star_rate", str(evaluations), "Evaluations", "#f59e0b", "/evaluations"),
        ("trending_up", str(avg_rating), "Avg. Rating", "#10b981", None),
    ]

    with ui.grid(columns=3).classes("w-full gap-4"):
        for icon_name, value, label, color, path in cards:
            _buildMetricCard(icon_name, value, label, color, path)


def _buildMetricCard(
    icon_name: str,
    value: str,
    label: str,
    accent_color: str,
    path: str | None,
) -> None:
    """
    Renders a single KPI metric card.

    Displays an icon on the left, a large numeric value and label on the
    right, and applies a subtle top-border accent in the provided color.
    Clicking the card navigates to the associated path when provided.

    Args:
        icon_name (str): Material Design icon identifier.
        value (str): The metric value to display prominently.
        label (str): The human-readable metric description.
        accent_color (str): Hex color string for the icon and accent border.
        path (str | None): Router path to navigate to on click, or None to
            disable navigation.
    """
    cursor_class = "cursor-pointer hover:border-white/20" if path else ""

    card = ui.card().classes(
        f"bg-[rgba(22,27,39,0.5)] border border-white/5 rounded-2xl p-6 "
        f"transition-all duration-200 {cursor_class} hover-lift "
        f"hover:bg-[rgba(28,34,53,0.7)] backdrop-blur-md"
    ).style(f"border-top: 2px solid {accent_color}60")
    if path:
        card.on("click", lambda p=path: ui.navigate.to(p))
    with card:
        with ui.row().classes("items-center gap-4 w-full"):
            with ui.element("div").classes(
                "rounded-xl p-3 flex items-center justify-center"
            ).style(f"background: {accent_color}18"):
                ui.icon(icon_name, size="1.8rem").style(f"color: {accent_color}")

            with ui.column().classes("gap-0"):
                ui.label(value).classes(
                    "text-white font-bold text-4xl leading-tight tracking-tight drop-shadow-md"
                )
                ui.label(label).classes("text-white/60 text-sm font-medium uppercase tracking-wider mt-1")


def _buildQuickActions() -> None:
    """
    Renders the quick-action shortcut cards below the KPI grid.

    Each card acts as a labeled navigation button to a management section,
    presented in a horizontal row with icon, title, and a brief description.
    """
    ui.label("Quick Actions").classes(
        "text-white font-semibold text-lg mt-2"
    )

    role = app.storage.user.get("user_role", "student")

    actions = []
    if role == "admin":
        actions.extend([
            ("group_add", "Add Student", "Register a new student record.", "/students"),
            ("person_add", "Add Professor", "Onboard a new instructor.", "/professors"),
            ("library_add", "Add Course", "Create a new course offering.", "/courses"),
            ("playlist_add", "Add Enrollment", "Enroll a student in a course.", "/enrollments"),
        ])
    elif role == "professor":
        actions.extend([
            ("library_add", "Add Course", "Create a new course offering.", "/courses"),
            ("star_rate", "Add Evaluation", "Grade a student.", "/evaluations"),
        ])
    else:
        actions.extend([
            ("playlist_add", "Enroll in Course", "Join a new class.", "/enrollments"),
        ])

    with ui.grid(columns=4).classes("w-full gap-4"):
        for icon_name, title, desc, path in actions:
            card = ui.card().classes(
                "bg-[rgba(22,27,39,0.5)] border border-white/5 rounded-2xl p-6 "
                "cursor-pointer hover:bg-[rgba(28,34,53,0.7)] hover:border-indigo-500/50 "
                "transition-all duration-200 hover-lift backdrop-blur-md"
            )
            card.on("click", lambda p=path: ui.navigate.to(p))
            with card:
                ui.icon(icon_name, size="1.5rem").classes("text-indigo-400 mb-2")
                ui.label(title).classes(
                    "text-white font-semibold text-sm"
                )
                ui.label(desc).classes("text-white/40 text-xs mt-1")
