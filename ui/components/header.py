"""Header component."""

from reactpy import component, html

from ui.styles import (
    HEADER_STYLE,
    HEADER_TITLE_STYLE,
    LOGO_STYLE,
    STATUS_BADGE_STYLE,
    STATUS_DOT_STYLE,
)


@component
def Header():
    """Header with logo, title, and status badge."""
    return html.header(
        {"style": HEADER_STYLE},
        # Left side: Logo + Title
        html.div(
            {"style": {"display": "flex", "alignItems": "center", "gap": "12px"}},
            html.div({"style": LOGO_STYLE}, "MTL"),
            html.span({"style": HEADER_TITLE_STYLE}, "MTL ERP Assistant"),
        ),
        # Right side: Status badge
        html.div(
            {"style": STATUS_BADGE_STYLE},
            html.span({"style": STATUS_DOT_STYLE, "className": "status-dot"}),
            html.span({}, "Connected"),
        ),
    )
