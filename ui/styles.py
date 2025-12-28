"""CSS constants and style dictionaries for ReactPy UI components."""

# ============== Colors ==============
PRIMARY_BLUE = "#3b82f6"
PRIMARY_BLUE_HOVER = "#2563eb"
DARK_BLUE = "#1e3a5f"
DARK_BLUE_LIGHT = "#2d4a6f"
GREEN_ACCENT = "#10b981"

# Backgrounds
BG_LIGHT = "#f8fafc"
BG_WHITE = "#ffffff"
BG_LIGHT_GRAY = "#f1f5f9"
BG_GRAY = "#e2e8f0"

# Borders
BORDER_GRAY = "#e2e8f0"

# Text colors
TEXT_DARK = "#1e293b"
TEXT_MEDIUM = "#374151"
TEXT_GRAY = "#475569"
TEXT_LIGHT_GRAY = "#64748b"
TEXT_LIGHTER = "#94a3b8"

# Badge colors
BADGE_BLUE_BG = "#e0f2fe"
BADGE_BLUE_TEXT = "#0369a1"
INTENT_BADGE_BG = "#dbeafe"
INTENT_BADGE_TEXT = "#1d4ed8"

# ============== Gradients ==============
HEADER_GRADIENT = "linear-gradient(135deg, #1e3a5f 0%, #2d4a6f 100%)"

# ============== Typography ==============
FONT_FAMILY = (
    '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen, Ubuntu, sans-serif'
)

# ============== Spacing ==============
SPACING_XS = "4px"
SPACING_SM = "8px"
SPACING_MD = "12px"
SPACING_LG = "16px"
SPACING_XL = "24px"

# ============== Border Radius ==============
RADIUS_SM = "4px"
RADIUS_MD = "8px"
RADIUS_LG = "12px"
RADIUS_FULL = "20px"

# ============== Shadows ==============
SHADOW_SM = "0 2px 8px rgba(0, 0, 0, 0.1)"
SHADOW_MD = "0 -2px 8px rgba(0, 0, 0, 0.05)"
SHADOW_LG = "0 20px 40px rgba(0, 0, 0, 0.2)"

# ============== Keyframe Animations (for injection) ==============
KEYFRAMES_CSS = """
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}

@keyframes typing {
    0%, 60%, 100% { transform: translateY(0); }
    30% { transform: translateY(-4px); }
}
"""

# ============== Global Styles ==============
GLOBAL_STYLES = f"""
* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: {FONT_FAMILY};
    background-color: {BG_LIGHT};
    height: 100vh;
    overflow: hidden;
}}

{KEYFRAMES_CSS}

.status-dot {{
    animation: pulse 2s infinite;
}}

.typing-dot {{
    animation: typing 1.4s infinite ease-in-out;
}}

.typing-dot:nth-child(2) {{
    animation-delay: 0.2s;
}}

.typing-dot:nth-child(3) {{
    animation-delay: 0.4s;
}}
"""

# ============== Component Styles ==============

# Header
HEADER_STYLE = {
    "background": HEADER_GRADIENT,
    "color": "white",
    "padding": f"{SPACING_LG} {SPACING_XL}",
    "display": "flex",
    "justifyContent": "space-between",
    "alignItems": "center",
    "boxShadow": SHADOW_SM,
    "minHeight": "72px",
}

LOGO_STYLE = {
    "width": "40px",
    "height": "40px",
    "background": "white",
    "borderRadius": RADIUS_MD,
    "display": "flex",
    "alignItems": "center",
    "justifyContent": "center",
    "fontWeight": "bold",
    "color": DARK_BLUE,
    "fontSize": "18px",
}

HEADER_TITLE_STYLE = {
    "fontSize": "20px",
    "fontWeight": "600",
}

STATUS_BADGE_STYLE = {
    "display": "flex",
    "alignItems": "center",
    "gap": SPACING_SM,
    "background": "rgba(255, 255, 255, 0.15)",
    "padding": f"{SPACING_SM} {SPACING_LG}",
    "borderRadius": RADIUS_FULL,
    "fontSize": "14px",
}

STATUS_DOT_STYLE = {
    "width": "8px",
    "height": "8px",
    "background": GREEN_ACCENT,
    "borderRadius": "50%",
    "display": "inline-block",
}

# Sidebar
SIDEBAR_STYLE = {
    "width": "300px",
    "minWidth": "300px",
    "maxWidth": "300px",
    "background": BG_WHITE,
    "borderRight": f"1px solid {BORDER_GRAY}",
    "display": "flex",
    "flexDirection": "column",
    "height": "100%",
}

CHATBOT_TABS_STYLE = {
    "display": "flex",
    "borderBottom": f"1px solid {BORDER_GRAY}",
}

CHATBOT_TAB_STYLE = {
    "flex": "1",
    "padding": SPACING_LG,
    "border": "none",
    "background": BG_LIGHT,
    "fontSize": "14px",
    "fontWeight": "500",
    "cursor": "pointer",
    "display": "flex",
    "flexDirection": "column",
    "alignItems": "center",
    "gap": SPACING_XS,
    "color": TEXT_LIGHT_GRAY,
    "borderBottom": "3px solid transparent",
    "transition": "all 0.2s",
}

CHATBOT_TAB_ACTIVE_STYLE = {
    **CHATBOT_TAB_STYLE,
    "background": BG_WHITE,
    "color": DARK_BLUE,
    "borderBottom": f"3px solid {PRIMARY_BLUE}",
}

SESSIONS_CONTAINER_STYLE = {
    "flex": "1",
    "overflowY": "auto",
    "padding": SPACING_MD,
}

SESSIONS_HEADER_STYLE = {
    "fontSize": "12px",
    "fontWeight": "600",
    "color": TEXT_LIGHT_GRAY,
    "textTransform": "uppercase",
    "letterSpacing": "0.5px",
    "padding": f"{SPACING_SM} {SPACING_MD}",
}

SESSION_ITEM_STYLE = {
    "padding": f"{SPACING_MD} {SPACING_LG}",
    "borderRadius": RADIUS_MD,
    "cursor": "pointer",
    "marginBottom": SPACING_XS,
    "border": "1px solid transparent",
    "transition": "all 0.2s",
}

SESSION_ITEM_ACTIVE_STYLE = {
    **SESSION_ITEM_STYLE,
    "background": "#eff6ff",
    "borderColor": PRIMARY_BLUE,
}

SESSION_TITLE_STYLE = {
    "fontSize": "14px",
    "fontWeight": "500",
    "color": TEXT_DARK,
    "marginBottom": SPACING_XS,
    "display": "flex",
    "alignItems": "center",
    "gap": SPACING_SM,
}

SESSION_PREVIEW_STYLE = {
    "fontSize": "12px",
    "color": TEXT_LIGHT_GRAY,
    "whiteSpace": "nowrap",
    "overflow": "hidden",
    "textOverflow": "ellipsis",
}

SESSION_META_STYLE = {
    "display": "flex",
    "justifyContent": "space-between",
    "marginTop": "6px",
    "fontSize": "11px",
    "color": TEXT_LIGHTER,
}

SESSION_BADGE_STYLE = {
    "fontSize": "10px",
    "padding": "2px 6px",
    "background": BADGE_BLUE_BG,
    "color": BADGE_BLUE_TEXT,
    "borderRadius": RADIUS_SM,
}

NEW_CHAT_SECTION_STYLE = {
    "padding": SPACING_LG,
    "borderTop": f"1px solid {BORDER_GRAY}",
    "background": BG_LIGHT,
}

NEW_CHAT_BTN_STYLE = {
    "width": "100%",
    "padding": SPACING_MD,
    "background": PRIMARY_BLUE,
    "color": "white",
    "border": "none",
    "borderRadius": RADIUS_MD,
    "fontSize": "14px",
    "fontWeight": "500",
    "cursor": "pointer",
    "display": "flex",
    "alignItems": "center",
    "justifyContent": "center",
    "gap": SPACING_SM,
}

# Chat Area
CHAT_CONTAINER_STYLE = {
    "flex": "1",
    "display": "flex",
    "flexDirection": "column",
    "background": BG_WHITE,
    "height": "100%",
}

CHAT_HEADER_STYLE = {
    "padding": f"{SPACING_LG} {SPACING_XL}",
    "borderBottom": f"1px solid {BORDER_GRAY}",
    "display": "flex",
    "justifyContent": "space-between",
    "alignItems": "center",
}

CHAT_TITLE_STYLE = {
    "fontSize": "18px",
    "fontWeight": "600",
    "color": DARK_BLUE,
}

CHAT_SUBTITLE_STYLE = {
    "fontSize": "13px",
    "color": TEXT_LIGHT_GRAY,
    "marginTop": SPACING_XS,
}

SESSION_INFO_STYLE = {
    "background": BG_LIGHT_GRAY,
    "padding": f"{SPACING_SM} {SPACING_MD}",
    "borderRadius": RADIUS_MD,
    "fontSize": "12px",
}

SESSION_INFO_LABEL_STYLE = {
    "color": TEXT_LIGHT_GRAY,
}

SESSION_INFO_VALUE_STYLE = {
    "color": DARK_BLUE,
    "fontWeight": "600",
    "fontFamily": "monospace",
}

CHAT_MESSAGES_STYLE = {
    "flex": "1",
    "overflowY": "auto",
    "padding": SPACING_XL,
    "display": "flex",
    "flexDirection": "column",
    "gap": SPACING_LG,
}

# Messages
MESSAGE_STYLE = {
    "display": "flex",
    "flexDirection": "column",
    "maxWidth": "70%",
}

MESSAGE_USER_STYLE = {
    **MESSAGE_STYLE,
    "alignSelf": "flex-end",
    "alignItems": "flex-end",
}

MESSAGE_ASSISTANT_STYLE = {
    **MESSAGE_STYLE,
    "alignSelf": "flex-start",
    "alignItems": "flex-start",
}

MESSAGE_BUBBLE_BASE = {
    "padding": f"{SPACING_MD} {SPACING_LG}",
    "borderRadius": RADIUS_LG,
    "fontSize": "14px",
    "lineHeight": "1.5",
    "whiteSpace": "pre-wrap",
}

USER_BUBBLE_STYLE = {
    **MESSAGE_BUBBLE_BASE,
    "background": DARK_BLUE,
    "color": "white",
    "borderBottomRightRadius": RADIUS_SM,
}

ASSISTANT_BUBBLE_STYLE = {
    **MESSAGE_BUBBLE_BASE,
    "background": BG_GRAY,
    "color": TEXT_DARK,
    "borderBottomLeftRadius": RADIUS_SM,
}

MESSAGE_TIME_STYLE = {
    "fontSize": "11px",
    "color": TEXT_LIGHTER,
    "marginTop": SPACING_XS,
}

INTENT_BADGE_STYLE = {
    "fontSize": "11px",
    "padding": f"{SPACING_XS} {SPACING_SM}",
    "background": INTENT_BADGE_BG,
    "color": INTENT_BADGE_TEXT,
    "borderRadius": RADIUS_SM,
    "marginBottom": SPACING_SM,
    "display": "inline-block",
    "fontWeight": "500",
}

# Typing Indicator
TYPING_INDICATOR_STYLE = {
    "display": "flex",
    "gap": SPACING_XS,
    "padding": f"{SPACING_MD} {SPACING_LG}",
    "background": BG_GRAY,
    "borderRadius": RADIUS_LG,
    "width": "fit-content",
}

TYPING_DOT_STYLE = {
    "width": "8px",
    "height": "8px",
    "background": TEXT_LIGHT_GRAY,
    "borderRadius": "50%",
}

# Input Area
INPUT_AREA_STYLE = {
    "padding": f"{SPACING_LG} {SPACING_XL}",
    "borderTop": f"1px solid {BORDER_GRAY}",
    "background": BG_WHITE,
    "boxShadow": SHADOW_MD,
}

INPUT_CONTAINER_STYLE = {
    "display": "flex",
    "gap": SPACING_MD,
    "alignItems": "center",
}

MESSAGE_INPUT_STYLE = {
    "flex": "1",
    "padding": "14px 18px",
    "border": f"2px solid {BORDER_GRAY}",
    "borderRadius": RADIUS_LG,
    "fontSize": "14px",
    "outline": "none",
    "fontFamily": FONT_FAMILY,
}

SEND_BUTTON_STYLE = {
    "width": "48px",
    "height": "48px",
    "background": PRIMARY_BLUE,
    "color": "white",
    "border": "none",
    "borderRadius": RADIUS_LG,
    "cursor": "pointer",
    "fontSize": "20px",
    "display": "flex",
    "alignItems": "center",
    "justifyContent": "center",
}

# Modal
MODAL_OVERLAY_STYLE = {
    "position": "fixed",
    "top": "0",
    "left": "0",
    "right": "0",
    "bottom": "0",
    "background": "rgba(0, 0, 0, 0.5)",
    "display": "flex",
    "alignItems": "center",
    "justifyContent": "center",
    "zIndex": "1000",
}

MODAL_STYLE = {
    "background": BG_WHITE,
    "borderRadius": RADIUS_LG,
    "padding": SPACING_XL,
    "width": "400px",
    "maxWidth": "90%",
    "boxShadow": SHADOW_LG,
}

MODAL_HEADER_STYLE = {
    "fontSize": "18px",
    "fontWeight": "600",
    "color": TEXT_DARK,
    "marginBottom": "20px",
    "display": "flex",
    "justifyContent": "space-between",
    "alignItems": "center",
}

MODAL_CLOSE_STYLE = {
    "background": "none",
    "border": "none",
    "fontSize": "24px",
    "color": TEXT_LIGHT_GRAY,
    "cursor": "pointer",
}

FORM_GROUP_STYLE = {
    "marginBottom": SPACING_LG,
}

FORM_LABEL_STYLE = {
    "display": "block",
    "fontSize": "14px",
    "fontWeight": "500",
    "color": TEXT_MEDIUM,
    "marginBottom": "6px",
}

FORM_INPUT_STYLE = {
    "width": "100%",
    "padding": "12px 14px",
    "border": f"2px solid {BORDER_GRAY}",
    "borderRadius": RADIUS_MD,
    "fontSize": "14px",
    "outline": "none",
    "boxSizing": "border-box",
    "fontFamily": FONT_FAMILY,
}

FORM_HINT_STYLE = {
    "fontSize": "12px",
    "color": TEXT_LIGHT_GRAY,
    "marginTop": SPACING_XS,
}

MODAL_ACTIONS_STYLE = {
    "display": "flex",
    "gap": SPACING_MD,
    "marginTop": SPACING_XL,
}

BTN_SECONDARY_STYLE = {
    "flex": "1",
    "padding": SPACING_MD,
    "background": BG_LIGHT_GRAY,
    "color": TEXT_GRAY,
    "border": "none",
    "borderRadius": RADIUS_MD,
    "fontSize": "14px",
    "fontWeight": "500",
    "cursor": "pointer",
}

BTN_PRIMARY_STYLE = {
    "flex": "1",
    "padding": SPACING_MD,
    "background": PRIMARY_BLUE,
    "color": "white",
    "border": "none",
    "borderRadius": RADIUS_MD,
    "fontSize": "14px",
    "fontWeight": "500",
    "cursor": "pointer",
}

# Empty State
EMPTY_STATE_STYLE = {
    "flex": "1",
    "display": "flex",
    "flexDirection": "column",
    "alignItems": "center",
    "justifyContent": "center",
    "color": TEXT_LIGHT_GRAY,
    "textAlign": "center",
    "padding": "40px",
}

EMPTY_STATE_ICON_STYLE = {
    "fontSize": "48px",
    "marginBottom": SPACING_LG,
}

EMPTY_STATE_TITLE_STYLE = {
    "fontSize": "18px",
    "fontWeight": "600",
    "color": TEXT_DARK,
    "marginBottom": SPACING_SM,
}

EMPTY_STATE_TEXT_STYLE = {
    "fontSize": "14px",
    "maxWidth": "300px",
}

# Main Layout
MAIN_CONTAINER_STYLE = {
    "display": "flex",
    "height": "calc(100vh - 72px)",
}

APP_CONTAINER_STYLE = {
    "height": "100vh",
    "display": "flex",
    "flexDirection": "column",
    "fontFamily": FONT_FAMILY,
    "background": BG_LIGHT,
}
