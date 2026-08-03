"""
SmartCampus AI - Sidebar Navigation Component
Renders the navigation menu, active user profile snippet, and logout button.
"""
import streamlit as st
from core.session import SessionManager
from authentication.logout import perform_logout

def render_sidebar() -> str:
    """Renders sidebar navigation and returns selected page name."""
    user = SessionManager.get_current_user()

    with st.sidebar:
        # App Logo & Branding Header
        st.markdown("""
        <div style="text-align: center; padding: 10px 0 20px 0;">
            <h2 style="font-family: 'Outfit', sans-serif; font-weight: 800; background: linear-gradient(135deg, #6366F1, #A855F7, #EC4899); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 0;">SmartCampus AI</h2>
            <p style="color: #94A3B8; font-size: 11px; margin-top: 2px; letter-spacing: 1px;">NEXT-GEN CAMPUS ENGINE</p>
        </div>
        """, unsafe_allow_html=True)

        # Logged In User Profile Summary Card
        if user:
            st.markdown(f"""
            <div style="background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; padding: 12px; margin-bottom: 20px; text-align: center;">
                <div style="font-weight: 700; color: #F8FAFC; font-size: 15px;">👤 {user.get('full_name')}</div>
                <div style="color: #6366F1; font-size: 12px; font-weight: 600;">{user.get('department')}</div>
                <div style="color: #64748B; font-size: 11px;">ID: {user.get('student_id')}</div>
            </div>
            """, unsafe_allow_html=True)

        # Navigation Options
        pages = {
            "🏠 Home": "Home",
            "📊 Dashboard": "Dashboard",
            "📢 Notice Board": "Notice Board",
            "💼 Placements": "Placements",
            "🎯 Workshops": "Workshops",
            "🤖 SmartCampus AI Assistant": "SmartCampus AI Assistant",
            "⚙ Settings": "Settings"
        }

        current_active = st.session_state.get("active_page", "Home")

        st.markdown("<p style='font-size: 11px; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 1px; margin-left: 5px;'>Navigation</p>", unsafe_allow_html=True)

        for label, page_key in pages.items():
            is_selected = (current_active == page_key)
            # Render custom styling button for active vs inactive
            button_type = "primary" if is_selected else "secondary"
            if st.button(label, use_container_width=True, key=f"nav_{page_key}"):
                st.session_state["active_page"] = page_key
                st.rerun()

        st.markdown("<hr style='margin: 25px 0 15px 0; opacity: 0.15;'>", unsafe_allow_html=True)

        # Logout Action
        if st.button("🚪 Logout", use_container_width=True, key="nav_logout"):
            perform_logout()

    return st.session_state.get("active_page", "Home")
