"""
src/app/ui/components/tables.py

Customized data table wrapper components for the ScholarConnect application.
Provides a factory function that creates consistently styled NiceGUI tables
with search filtering, column formatting, and action button integration.
"""

from typing import Any, Callable
from nicegui import ui


def buildDataTable(
    columns: list[dict],
    rows: list[dict],
    on_edit: Callable[[dict], None] | None = None,
    on_delete: Callable[[dict], None] | None = None,
    row_key: str = "id",
    title: str = "",
) -> ui.table:
    """
    Constructs a styled, searchable data table with optional action buttons.

    Renders a NiceGUI table wrapped in a dark-themed card.  When callbacks are
    provided, an 'Actions' column is appended containing Edit and Delete icon
    buttons per row.  A search input filters rows client-side against all
    string column values.

    Args:
        columns (list[dict]): NiceGUI column descriptor dicts with at minimum
            'name', 'label', and 'field' keys.
        rows (list[dict]): Row data dicts matching the column field names.
        on_edit (Callable[[dict], None], optional): Callback invoked with the
            row dict when the edit button is clicked.  Defaults to None.
        on_delete (Callable[[dict], None], optional): Callback invoked with the
            row dict when the delete button is clicked.  Defaults to None.
        row_key (str): The field name used as the unique row key. Defaults to
            'id'.
        title (str): Optional section title rendered above the table.

    Returns:
        ui.table: The constructed NiceGUI table element.
    """
    # Append an actions column only when at least one callback is supplied.
    display_columns = list(columns)
    has_actions = on_edit is not None or on_delete is not None
    if has_actions:
        display_columns.append(
            {"name": "actions", "label": "Actions", "field": "actions", "align": "center"}
        )

    with ui.card().classes(
        "w-full bg-[#161b27] border border-white/5 rounded-2xl p-0 overflow-hidden"
    ):
        # Table header with optional title and search field
        with ui.row().classes(
            "w-full items-center justify-between px-6 py-4 bg-[#0f1117] border-b border-white/5"
        ):
            if title:
                ui.label(title).classes("text-white font-semibold text-base")
            else:
                ui.space()

            search_input = ui.input(placeholder="Search...").classes(
                "bg-white/5 text-white/80 rounded-lg px-3 py-1 text-sm "
                "border border-white/10 w-56"
            ).props("dense outlined dark")

        table = ui.table(
            columns=display_columns,
            rows=rows,
            row_key=row_key,
            pagination={"rowsPerPage": 10, "sortBy": None},
        ).classes("w-full text-white/80 text-sm").props("dark flat")

        # Bind client-side search filter to the table's filter property.
        search_input.bind_value(table, "filter")

        if has_actions:
            # Inject action buttons into each row using a scoped slot.
            table.add_slot(
                "body-cell-actions",
                _buildActionSlot(on_edit, on_delete),
            )

    return table


def _buildActionSlot(
    on_edit: Callable[[dict], None] | None,
    on_delete: Callable[[dict], None] | None,
) -> str:
    """
    Generates the Vue-template scoped slot string for the actions cell.

    Produces a q-td containing icon buttons for edit and delete operations.
    Each button is conditionally rendered based on which callbacks are provided.

    Args:
        on_edit (Callable[[dict], None] | None): Edit callback reference.
        on_delete (Callable[[dict], None] | None): Delete callback reference.

    Returns:
        str: The raw Vue template string for the actions slot.
    """
    # Slot template uses props.row to pass the full row dict to Python callbacks.
    edit_btn = (
        "<q-btn flat round dense icon='edit' color='indigo-4' "
        "@click=\"$parent.$emit('edit', props.row)\" />"
        if on_edit
        else ""
    )
    delete_btn = (
        "<q-btn flat round dense icon='delete' color='red-4' "
        "@click=\"$parent.$emit('delete', props.row)\" />"
        if on_delete
        else ""
    )
    return (
        f"<q-td :props='props'>"
        f"  <div class='flex gap-1 justify-center'>"
        f"    {edit_btn}"
        f"    {delete_btn}"
        f"  </div>"
        f"</q-td>"
    )


def registerTableEvents(
    table: ui.table,
    on_edit: Callable[[dict], None] | None = None,
    on_delete: Callable[[dict], None] | None = None,
) -> None:
    """
    Attaches Python-side event handlers to a table's custom Vue events.

    Connects the 'edit' and 'delete' custom events emitted by the action slot
    template to their respective Python callback functions.

    Args:
        table (ui.table): The NiceGUI table instance to attach events to.
        on_edit (Callable[[dict], None] | None): Called with the row dict on
            edit. Defaults to None.
        on_delete (Callable[[dict], None] | None): Called with the row dict on
            delete. Defaults to None.
    """
    if on_edit:
        table.on("edit", lambda e: on_edit(e.args))
    if on_delete:
        table.on("delete", lambda e: on_delete(e.args))
