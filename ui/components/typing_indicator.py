"""Typing indicator component with animated dots."""

from reactpy import component, html

from ui.styles import (
    MESSAGE_ASSISTANT_STYLE,
    TYPING_DOT_STYLE,
    TYPING_INDICATOR_STYLE,
)


@component
def TypingIndicator():
    """Animated typing indicator with three bouncing dots."""
    return html.div(
        {"style": MESSAGE_ASSISTANT_STYLE},
        html.div(
            {"style": TYPING_INDICATOR_STYLE},
            html.span({"style": TYPING_DOT_STYLE, "className": "typing-dot"}),
            html.span({"style": TYPING_DOT_STYLE, "className": "typing-dot"}),
            html.span({"style": TYPING_DOT_STYLE, "className": "typing-dot"}),
        ),
    )
