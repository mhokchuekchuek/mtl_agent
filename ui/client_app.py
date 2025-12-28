"""Client BI Analytics Streamlit UI."""

import os
from uuid import uuid4

import requests
import streamlit as st
import streamlit.components.v1 as components

# Page config
st.set_page_config(
    page_title="BI Analytics - MTL ERP",
    page_icon="📊",
    layout="wide",
)

# API config (use environment variable for Docker)
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
CLIENT_CHAT_ENDPOINT = "/api/v1/chatbot/client/chat"

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "session_started" not in st.session_state:
    st.session_state.session_started = False
if "thread_id" not in st.session_state:
    st.session_state.thread_id = ""
if "user_id" not in st.session_state:
    st.session_state.user_id = ""


def call_client_api(query: str, thread_id: str, user_id: str) -> dict:
    """Call client chatbot API."""
    try:
        response = requests.post(
            f"{API_BASE_URL}{CLIENT_CHAT_ENDPOINT}",
            json={
                "query": query,
                "thread_id": thread_id,
                "user_id": user_id,
            },
            timeout=120,
        )
        response.raise_for_status()
        data = response.json()
        return {
            "response": data.get("response", "ไม่ได้รับการตอบกลับ"),
            "intent": data.get("intent"),
            "chart_html": data.get("chart_html"),
        }
    except requests.ConnectionError:
        return {
            "response": "❌ ไม่สามารถเชื่อมต่อ API Server ได้ กรุณาตรวจสอบว่า server กำลังทำงานอยู่",
            "intent": None,
            "chart_html": None,
        }
    except requests.Timeout:
        return {
            "response": "❌ หมดเวลาในการเชื่อมต่อ กรุณาลองใหม่อีกครั้ง",
            "intent": None,
            "chart_html": None,
        }
    except Exception as e:
        return {
            "response": f"❌ เกิดข้อผิดพลาด: {str(e)}",
            "intent": None,
            "chart_html": None,
        }


def start_session():
    """Start a new chat session."""
    st.session_state.session_started = True
    st.session_state.messages = []


def reset_session():
    """Reset session to start over."""
    st.session_state.session_started = False
    st.session_state.messages = []
    st.session_state.thread_id = ""
    st.session_state.user_id = ""


# Sidebar - Session Configuration
with st.sidebar:
    st.title("📊 BI Analytics")
    st.markdown("---")

    if not st.session_state.session_started:
        st.subheader("🔧 ตั้งค่า Session")

        # Thread ID
        thread_id = st.text_input(
            "Session ID",
            value=str(uuid4())[:8],
            help="ID สำหรับระบุ session การสนทนา",
        )

        # User ID
        user_id = st.text_input(
            "User ID",
            value="analyst_001",
            help="ID ของผู้ใช้งาน",
        )

        st.markdown("---")

        # Start button
        if st.button("🚀 เริ่มต้นวิเคราะห์", use_container_width=True, type="primary"):
            if thread_id and user_id:
                st.session_state.thread_id = thread_id
                st.session_state.user_id = user_id
                start_session()
                st.rerun()
            else:
                st.error("กรุณากรอก Session ID และ User ID")
    else:
        st.subheader("📋 Session Info")
        st.markdown(f"**Session ID:** `{st.session_state.thread_id}`")
        st.markdown(f"**User ID:** `{st.session_state.user_id}`")

        st.markdown("---")

        if st.button("�� เริ่มใหม่", use_container_width=True):
            reset_session()
            st.rerun()

    st.markdown("---")
    st.caption("MTL ERP Assistant v1.0")


# Main content
if not st.session_state.session_started:
    # Welcome screen
    st.title("📊 ยินดีต้อนรับสู่ BI Analytics")
    st.markdown(
        """
        ### ระบบวิเคราะห์ข้อมูลธุรกิจ MTL ERP

        คุณสามารถสอบถามเกี่ยวกับ:
        - 📈 วิเคราะห์ยอดขาย
        - 👥 ข้อมูลลูกค้า
        - 📦 สถิติสินค้า
        - 💹 รายงานและ Dashboard
        - 💬 ประวัติการสนทนาของลูกค้า

        **กรุณากรอกข้อมูล Session ที่แถบด้านซ้ายเพื่อเริ่มต้นวิเคราะห์**
        """
    )
else:
    # Chat interface
    st.title("📊 BI Analytics Chat")

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            # Show intent badge if available
            if message.get("intent"):
                st.caption(f"📊 Intent: {message['intent']}")
            st.markdown(message["content"])

            # Show chart if available
            if message.get("chart_html"):
                components.html(message["chart_html"], height=500, scrolling=True)

    # Chat input
    if prompt := st.chat_input("ถามคำถามเกี่ยวกับข้อมูลธุรกิจ..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get assistant response
        with st.chat_message("assistant"):
            with st.spinner("กำลังวิเคราะห์..."):
                result = call_client_api(
                    query=prompt,
                    thread_id=st.session_state.thread_id,
                    user_id=st.session_state.user_id,
                )

            # Show intent if available
            if result.get("intent"):
                st.caption(f"📊 Intent: {result['intent']}")

            st.markdown(result["response"])

            # Show chart if available
            if result.get("chart_html"):
                components.html(result["chart_html"], height=500, scrolling=True)

        # Add assistant message with chart
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": result["response"],
                "intent": result.get("intent"),
                "chart_html": result.get("chart_html"),
            }
        )
