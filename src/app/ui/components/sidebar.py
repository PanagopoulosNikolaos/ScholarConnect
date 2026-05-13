"""
src/app/ui/components/sidebar.py

Reusable left-hand navigation sidebar for the ScholarConnect web application.
Renders the application brand header, primary navigation links, and a
persistent logout button anchored at the bottom of the drawer.
"""

from nicegui import ui, app


def buildSidebar() -> None:
    """
    Constructs the application's left-hand navigation drawer.

    Renders the brand header, all primary navigation links (Dashboard,
    Students, Professors, Courses, Enrollments, Evaluations), and a logout
    button pinned to the bottom of the drawer.  Must be called inside a
    NiceGUI page function to attach to the current page context.

    Note: fixed=True is intentionally omitted so Quasar's layout system
    automatically offsets the main content area to the right of the drawer.
    """
    with ui.left_drawer().classes(
        "bg-[#0f1117] border-r border-white/5 flex flex-col"
    ).style("min-width: 240px; width: 240px"):
        # Brand / logo block
        with ui.column().classes("items-center py-8 px-4 gap-1"):
            ui.icon("school", size="2.5rem").classes("text-indigo-400")
            ui.label("ScholarConnect").classes(
                "text-white font-bold text-lg tracking-wide"
            )
            ui.label("Academic Portal").classes("text-white/40 text-xs")

        ui.separator().classes("opacity-10 mx-4 my-2")

        # Navigation links list
        nav_items = [
            ("dashboard", "Dashboard", "/dashboard"),
            ("group", "Students", "/students"),
            ("person", "Professors", "/professors"),
            ("menu_book", "Courses", "/courses"),
            ("assignment", "Enrollments", "/enrollments"),
            ("star_rate", "Evaluations", "/evaluations"),
        ]

        with ui.column().classes("flex-1 gap-1 px-3"):
            for icon_name, label_text, path in nav_items:
                _buildNavLink(icon_name, label_text, path)

        ui.separator().classes("opacity-10 mx-4 my-2")

        # Logout row pinned to the bottom
        with ui.column().classes("px-3 pb-6"):
            _buildNavRow(
                icon_name="logout",
                label_text="Logout",
                on_click=_handleLogout,
                active=False,
                danger=True,
            )


def _buildNavLink(icon_name: str, label_text: str, path: str) -> None:
    """
    Renders a single navigation link row inside the sidebar.

    Applies an active highlight when the current URL matches the link's
    target path.  Uses a plain clickable row rather than ui.button() to
    prevent Quasar's button from rendering the icon name as slot text.

    Args:
        icon_name (str): The Material Design icon identifier string.
        label_text (str): The human-readable label displayed next to the icon.
        path (str): The NiceGUI router path the row navigates to on click.
    """
    current_path = ui.context.client.page.path if ui.context else "/"
    is_active = current_path == path
    _buildNavRow(
        icon_name=icon_name,
        label_text=label_text,
        on_click=lambda p=path: ui.navigate.to(p),
        active=is_active,
    )


def _buildNavRow(
    icon_name: str,
    label_text: str,
    on_click,
    active: bool = False,
    danger: bool = False,
) -> None:
    """
    Renders a styled clickable row used for both nav links and the logout action.

    Args:
        icon_name (str): Material Design icon name.
        label_text (str): Display text shown beside the icon.
        on_click (Callable): Handler invoked when the row is clicked.
        active (bool): Applies the active/selected highlight style when True.
        danger (bool): Applies red danger styling (used for logout).
    """
    if danger:
        row_classes = (
            "w-full flex items-center gap-3 px-4 py-3 rounded-xl "
            "cursor-pointer transition-all duration-200 "
            "text-red-400 hover:bg-red-500/10"
        )
        icon_classes = "text-red-400"
        label_classes = "text-red-400 text-sm font-medium"
    elif active:
        row_classes = (
            "w-full flex items-center gap-3 px-4 py-3 rounded-xl "
            "cursor-pointer transition-all duration-200 "
            "bg-indigo-500/20 border border-indigo-500/30"
        )
        icon_classes = "text-indigo-300"
        label_classes = "text-indigo-300 text-sm font-medium"
    else:
        row_classes = (
            "w-full flex items-center gap-3 px-4 py-3 rounded-xl "
            "cursor-pointer transition-all duration-200 "
            "hover:bg-white/5 border border-transparent"
        )
        icon_classes = "text-white/50"
        label_classes = "text-white/60 text-sm font-medium hover:text-white/90"

    with ui.row().classes(row_classes).on("click", on_click):
        ui.icon(icon_name, size="1.2rem").classes(icon_classes)
        ui.label(label_text).classes(label_classes)


async def _handleLogout() -> None:
    """
    Clears the user session and redirects to the login page.

    Deletes the 'authenticated', 'user_am', and 'user_role' keys from user
    storage to invalidate the current session before navigating to root.
    """
    app.storage.user.pop("authenticated", None)
    app.storage.user.pop("user_am", None)
    app.storage.user.pop("user_role", None)
    ui.navigate.to("/")
