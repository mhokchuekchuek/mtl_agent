"""Customer Chatbot Streamlit UI."""

import os
from uuid import uuid4

import requests
import streamlit as st

# Page config
st.set_page_config(
    page_title="Customer Support - MTL ERP",
    page_icon="💬",
    layout="wide",
)

# API config (use environment variable for Docker)
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
CUSTOMER_CHAT_ENDPOINT = "/api/v1/chatbot/customer/chat"

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "session_started" not in st.session_state:
    st.session_state.session_started = False
if "thread_id" not in st.session_state:
    st.session_state.thread_id = ""
if "user_id" not in st.session_state:
    st.session_state.user_id = ""


def call_customer_api(query: str, thread_id: str, user_id: str) -> str:
    """Call customer chatbot API."""
    try:
        response = requests.post(
            f"{API_BASE_URL}{CUSTOMER_CHAT_ENDPOINT}",
            json={
                "query": query,
                "thread_id": thread_id,
                "user_id": user_id,
            },
            timeout=120,
        )
        response.raise_for_status()
        data = response.json()
        return data.get("response", "ไม่ได้รับการตอบกลับ")
    except requests.ConnectionError:
        return "❌ ไม่สามารถเชื่อมต่อ API Server ได้ กรุณาตรวจสอบว่า server กำลังทำงานอยู่"
    except requests.Timeout:
        return "❌ หมดเวลาในการเชื่อมต่อ กรุณาลองใหม่อีกครั้ง"
    except Exception as e:
        return f"❌ เกิดข้อผิดพลาด: {str(e)}"


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
    st.title("💬 Customer Support")
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
            value="customer_001",
            help="ID ของผู้ใช้งาน",
        )

        st.markdown("---")

        # Start button
        if st.button("🚀 เริ่มต้นสนทนา", use_container_width=True, type="primary"):
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

        if st.button("🔄 เริ่มใหม่", use_container_width=True):
            reset_session()
            st.rerun()

    st.markdown("---")
    st.caption("MTL ERP Assistant v1.0")


# Main content
if not st.session_state.session_started:
    # Welcome screen
    st.title("💬 ยินดีต้อนรับสู่ Customer Support")
    st.markdown(
        """
        ### บริการช่วยเหลือลูกค้า MTL ERP

        คุณสามารถสอบถามเกี่ยวกับ:
        - 🔍 ค้นหาสินค้า
        - 📦 ตรวจสอบสต็อก
        - 💰 สอบถามราคา
        - 🛒 สั่งซื้อสินค้า

        **กรุณากรอกข้อมูล Session ที่แถบด้านซ้ายเพื่อเริ่มต้นสนทนา**
        """
    )
else:
    # Chat interface
    st.title("💬 Customer Support Chat")

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("พิมพ์ข้อความของคุณ..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get assistant response
        with st.chat_message("assistant"):
            with st.spinner("กำลังคิด..."):
                response = call_customer_api(
                    query=prompt,
                    thread_id=st.session_state.thread_id,
                    user_id=st.session_state.user_id,
                )
            st.markdown(response)

        # Add assistant message
        st.session_state.messages.append({"role": "assistant", "content": response})
