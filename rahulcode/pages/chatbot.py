"""
SmartCampus AI - AI Assistant Chatbot View
Streamlit chat interface for academic queries, notice summaries, resume tips, mock interviews, and career roadmap generation.
"""
import streamlit as st
from core.session import SessionManager
from services.ai_service import AIService
from services.notice_service import NoticeService
from services.placement_service import PlacementService

def render_chatbot_page():
    """Renders Streamlit Chat AI Assistant interface."""
    user = SessionManager.get_current_user()
    user_name = user.get("full_name", "Student") if user else "Student"

    ai_svc = AIService()
    notice_svc = NoticeService()
    placement_svc = PlacementService()

    st.markdown("### 🤖 SmartCampus AI Career & Academic Assistant")
    st.markdown("<p style='color: #94A3B8; font-size: 14px;'>Ask questions about campus notices, placement prep, resume feedback, or request a career roadmap.</p>", unsafe_allow_html=True)

    # Preset Prompt Shortcuts
    st.markdown("**💡 Quick Prompt Shortcuts:**")
    p1, p2, p3, p4 = st.columns(4)

    preset_prompt = None
    with p1:
        if st.button("📢 Summarize Notices", use_container_width=True):
            preset_prompt = "Can you summarize the latest campus notices for me?"
    with p2:
        if st.button("💼 Placement Prep", use_container_width=True):
            preset_prompt = "Give me placement preparation tips and top technical interview questions."
    with p3:
        if st.button("📝 Resume Guidance", use_container_width=True):
            preset_prompt = "What key skills and project sections should I include on my resume?"
    with p4:
        if st.button("🗺 Career Roadmap", use_container_width=True):
            preset_prompt = "Generate a step-by-step career growth roadmap for my engineering department."

    st.markdown("<hr style='margin: 15px 0 20px 0; opacity: 0.1;'>", unsafe_allow_html=True)

    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = [
            {
                "role": "assistant",
                "content": f"Hello {user_name}! 👋 I am **SmartCampus AI**. How can I assist your learning or career path today?"
            }
        ]

    # Render Chat Messages History
    for message in st.session_state["chat_history"]:
        avatar = "🤖" if message["role"] == "assistant" else "👤"
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

    # User Chat Input
    user_input = st.chat_input("Type your question or choose a prompt shortcut above...") or preset_prompt

    if user_input:
        # Append User Message
        st.session_state["chat_history"].append({"role": "user", "content": user_input})
        with st.chat_message("user", avatar="👤"):
            st.markdown(user_input)

        # Context objects
        notices_ctx = notice_svc.get_all_notices()
        placements_ctx = placement_svc.get_all_placements()

        # Generate Assistant Response
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("SmartCampus AI is thinking..."):
                response_text = ai_svc.generate_chat_response(
                    user_message=user_input,
                    chat_history=st.session_state["chat_history"],
                    user_context=user,
                    notices_context=notices_ctx,
                    placements_context=placements_ctx
                )
                st.markdown(response_text)

        # Append Assistant Response
        st.session_state["chat_history"].append({"role": "assistant", "content": response_text})

    # Clear Chat History Option
    if len(st.session_state["chat_history"]) > 1:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🗑️ Clear Conversation History"):
            st.session_state["chat_history"] = [
                {
                    "role": "assistant",
                    "content": f"Hello {user_name}! 👋 History cleared. How can I assist you?"
                }
            ]
            st.rerun()
