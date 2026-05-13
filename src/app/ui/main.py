"""
src/app/ui/main.py

Application entry point for the ScholarConnect NiceGUI web application.
Configures global app settings, defines all page routes with access control
decorators, and starts the NiceGUI server.

Run with:
    conda run -n py14 python -m src.app.ui.main
"""

from nicegui import ui, app

from src.app.ui.pages.auth import buildLoginPage, buildRegisterPage
from src.app.ui.pages.dashboard import buildDashboardPage
from src.app.ui.pages.students import buildStudentsPage
from src.app.ui.pages.professors import buildProfessorsPage
from src.app.ui.pages.courses import buildCoursesPage
from src.app.ui.pages.enrollments import buildEnrollmentsPage
from src.app.ui.pages.evaluations import buildEvaluationsPage


# ---------------------------------------------------------------------------
# Access control guard
# ---------------------------------------------------------------------------

def _requireAuth() -> bool:
    """
    Checks whether the current session is authenticated.

    Redirects unauthenticated requests to the login page.  Returns True when
    the session is valid, allowing page rendering to proceed.

    Returns:
        bool: True if the user is authenticated, False otherwise.
    """
    if not app.storage.user.get("authenticated"):
        ui.navigate.to("/")
        return False
    return True


# ---------------------------------------------------------------------------
# Global styles
# ---------------------------------------------------------------------------

def _applyGlobalStyles() -> None:
    """
    Injects global CSS applied across all pages.

    Applies the dark base background, custom scrollbar styling, Quasar
    dark-mode font overrides, and removes default NiceGUI page padding for
    pages that manage their own layout.
    """
    ui.add_head_html(
        """
        <style>
          @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

          * { font-family: 'Inter', sans-serif; box-sizing: border-box; }

          body {
            background: #0a0d14 !important;
            color: #e2e8f0;
            margin: 0;
          }

          /* Scrollbar */
          ::-webkit-scrollbar { width: 6px; height: 6px; }
          ::-webkit-scrollbar-track { background: #0f1117; }
          ::-webkit-scrollbar-thumb { background: #2d3748; border-radius: 3px; }
          ::-webkit-scrollbar-thumb:hover { background: #4a5568; }

          /* NiceGUI overrides */
          .nicegui-content { padding: 0 !important; max-width: none !important; }
          .q-drawer { background: #0f1117 !important; }

          /* Remove Quasar button text-transform */
          .no-uppercase { text-transform: none !important; letter-spacing: normal !important; }

          /* Table dark theme overrides */
          .q-table__container { background: transparent !important; }
          .q-table tbody tr:hover td { background: rgba(99,102,241,0.05) !important; }
          .q-table th { color: rgba(255,255,255,0.5) !important; font-weight: 600; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.05em; border-bottom: 1px solid rgba(255,255,255,0.08) !important; }
          .q-table td { border-bottom: 1px solid rgba(255,255,255,0.04) !important; color: rgba(255,255,255,0.80); }

          /* Input dark overrides */
          .q-field--outlined .q-field__control { background: rgba(255,255,255,0.04) !important; }
          .q-field__label { color: rgba(255,255,255,0.5) !important; }
          .q-field__native { color: rgba(255,255,255,0.9) !important; }
          .q-field--outlined .q-field__control:hover:before { border-color: rgba(99,102,241,0.5) !important; }
          .q-field--focused .q-field__control:before { border-color: #6366f1 !important; }

          /* Notification positioning */
          .q-notification { border-radius: 12px !important; font-family: 'Inter', sans-serif !important; }
        </style>
        """
    )


# ---------------------------------------------------------------------------
# Page route definitions
# ---------------------------------------------------------------------------

@ui.page("/")
def loginPage() -> None:
    """
    Serves the login page at the root path.

    Redirects already-authenticated users directly to the dashboard,
    avoiding redundant re-authentication.
    """
    _applyGlobalStyles()
    if app.storage.user.get("authenticated"):
        ui.navigate.to("/dashboard")
        return
    buildLoginPage()


@ui.page("/register")
def registerPage() -> None:
    """
    Serves the student self-registration page.
    """
    _applyGlobalStyles()
    buildRegisterPage()


@ui.page("/dashboard")
def dashboardPage() -> None:
    """
    Serves the main dashboard page.  Requires authentication.
    """
    _applyGlobalStyles()
    if not _requireAuth():
        return
    buildDashboardPage()


@ui.page("/students")
def studentsPage() -> None:
    """
    Serves the Student Management page.  Requires authentication.
    """
    _applyGlobalStyles()
    if not _requireAuth():
        return
    buildStudentsPage()


@ui.page("/professors")
def professorsPage() -> None:
    """
    Serves the Professor Management page.  Requires authentication.
    """
    _applyGlobalStyles()
    if not _requireAuth():
        return
    buildProfessorsPage()


@ui.page("/courses")
def coursesPage() -> None:
    """
    Serves the Course Management page.  Requires authentication.
    """
    _applyGlobalStyles()
    if not _requireAuth():
        return
    buildCoursesPage()


@ui.page("/enrollments")
def enrollmentsPage() -> None:
    """
    Serves the Enrollment Management page.  Requires authentication.
    """
    _applyGlobalStyles()
    if not _requireAuth():
        return
    buildEnrollmentsPage()


@ui.page("/evaluations")
def evaluationsPage() -> None:
    """
    Serves the Evaluation Management page.  Requires authentication.
    """
    _applyGlobalStyles()
    if not _requireAuth():
        return
    buildEvaluationsPage()


# ---------------------------------------------------------------------------
# Application startup
# ---------------------------------------------------------------------------

ui.run(
    title="ScholarConnect",
    host="0.0.0.0",
    port=8080,
    dark=True,
    storage_secret="scholarconnect-secret-key-change-in-production",
    favicon="school",
    reload=False,
)
