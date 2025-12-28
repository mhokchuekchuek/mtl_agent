# ui

Start ReactPy web UI for MTL ERP Assistant.

## Usage

```bash
python main.py ui [OPTIONS]
```

## Options

| Option | Short | Default | Description |
|--------|-------|---------|-------------|
| `--host` | `-h` | `0.0.0.0` | Host to bind |
| `--port` | `-p` | `8501` | Port to bind |

## Examples

```bash
# Default (0.0.0.0:8501)
python main.py ui

# Custom port
python main.py ui --port 8502

# Localhost only
python main.py ui --host 127.0.0.1
```

## Docker

```bash
docker-compose up -d ui
```

Access at: http://localhost:8501

## Architecture

The UI is built with **ReactPy** (Python reactive UI framework) and **FastAPI**.

### File Structure

```
ui/
├── __init__.py          # Package init
├── app.py               # Main ReactPy application
├── server.py            # FastAPI + ReactPy server
├── api_client.py        # HTTP client for backend API
├── config.py            # Configuration settings
├── state.py             # AppState dataclass
├── styles.py            # CSS constants and style dicts
└── components/
    ├── __init__.py
    ├── header.py            # Header with logo, title, status
    ├── sidebar.py           # Chatbot tabs, sessions list, new chat
    ├── chat_area.py         # Chat header, messages, input
    ├── message_bubble.py    # User/Assistant message bubbles
    ├── typing_indicator.py  # Animated typing dots
    └── new_chat_modal.py    # Create session modal
```

### Components

| Component | Description |
|-----------|-------------|
| `Header` | Logo "MTL", title "MTL ERP Assistant", status badge |
| `Sidebar` | Customer/Client tabs, session list, "Add New Chat" button |
| `ChatArea` | Chat header, messages area, input field |
| `MessageBubble` | User (right, dark) / Assistant (left, gray) messages |
| `TypingIndicator` | Animated dots while waiting for API response |
| `NewChatModal` | Modal form for creating new chat sessions |

### Features

- Two chatbot types: **Customer Support** (💬) and **BI Analytics** (📊)
- Session management (create, select, list)
- Real-time message display with typing indicator
- Thai language support
- Charts support for Client chatbot (BI Analytics)
- Responsive design matching mockup
