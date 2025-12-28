"""Message bubble component."""

from datetime import datetime
from typing import Optional

import markdown
from reactpy import component, html

from ui.styles import (
    ASSISTANT_BUBBLE_STYLE,
    INTENT_BADGE_STYLE,
    MESSAGE_ASSISTANT_STYLE,
    MESSAGE_TIME_STYLE,
    MESSAGE_USER_STYLE,
    USER_BUBBLE_STYLE,
)

# Markdown converter with common extensions
md = markdown.Markdown(extensions=["fenced_code", "tables", "nl2br"])


def render_markdown(text: str) -> str:
    """Convert markdown text to HTML."""
    md.reset()
    return md.convert(text)


# CSS for markdown content inside bubbles
MARKDOWN_STYLE = """
.markdown-content p { margin: 0 0 8px 0; }
.markdown-content p:last-child { margin-bottom: 0; }
.markdown-content ul, .markdown-content ol { margin: 8px 0; padding-left: 20px; }
.markdown-content li { margin: 4px 0; }
.markdown-content code {
    background: rgba(0,0,0,0.1);
    padding: 2px 6px;
    border-radius: 4px;
    font-family: monospace;
    font-size: 0.9em;
}
.markdown-content pre {
    background: rgba(0,0,0,0.1);
    padding: 12px;
    border-radius: 8px;
    overflow-x: auto;
    margin: 8px 0;
}
.markdown-content pre code {
    background: none;
    padding: 0;
}
.markdown-content table {
    border-collapse: collapse;
    margin: 8px 0;
    width: 100%;
}
.markdown-content th, .markdown-content td {
    border: 1px solid rgba(0,0,0,0.2);
    padding: 8px;
    text-align: left;
}
.markdown-content th {
    background: rgba(0,0,0,0.1);
}
.markdown-content strong { font-weight: 600; }
.markdown-content em { font-style: italic; }
.markdown-content a { color: #3b82f6; text-decoration: underline; }
.markdown-content h1, .markdown-content h2, .markdown-content h3 {
    margin: 12px 0 8px 0;
    font-weight: 600;
}
.markdown-content h1 { font-size: 1.3em; }
.markdown-content h2 { font-size: 1.2em; }
.markdown-content h3 { font-size: 1.1em; }
"""


@component
def MessageBubble(
    role: str,
    content: str,
    timestamp: Optional[datetime] = None,
    intent: Optional[str] = None,
    chart_html: Optional[str] = None,
):
    """Render a single message bubble."""
    time_str = timestamp.strftime("%H:%M") if timestamp else ""

    if role == "user":
        return html.div(
            {"style": MESSAGE_USER_STYLE},
            html.div({"style": USER_BUBBLE_STYLE}, content),
            html.span({"style": MESSAGE_TIME_STYLE}, time_str),
        )
    else:
        # Assistant message - render markdown
        content_html = render_markdown(content)

        # Merge bubble style with markdown class
        bubble_style = {**ASSISTANT_BUBBLE_STYLE}

        bubble_content = [
            # Inject markdown CSS
            html.style(MARKDOWN_STYLE),
            html.div(
                {
                    "style": bubble_style,
                    "className": "markdown-content",
                    "dangerouslySetInnerHTML": {"__html": content_html},
                }
            ),
        ]

        # Add chart if present
        if chart_html:
            bubble_content.append(
                html.div(
                    {
                        "style": {
                            "marginTop": "12px",
                            "background": "white",
                            "border": "1px solid #e2e8f0",
                            "borderRadius": "8px",
                            "padding": "16px",
                        },
                        "dangerouslySetInnerHTML": {"__html": chart_html},
                    }
                )
            )

        # Build message with optional intent badge
        children = []
        if intent:
            children.append(html.span({"style": INTENT_BADGE_STYLE}, f"📊 {intent}"))
        children.extend(bubble_content)
        children.append(html.span({"style": MESSAGE_TIME_STYLE}, time_str))

        return html.div({"style": MESSAGE_ASSISTANT_STYLE}, *children)
