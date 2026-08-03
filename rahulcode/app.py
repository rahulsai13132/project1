"""
SmartCampus AI - Main Application Entrypoint
Streamlit app initialization, session state verification, custom CSS injection,
sidebar navigation, and page router.
"""
import streamlit as st
from pathlib import Path

# Set Page Config MUST be the very first Streamlit call
st.set_page_config(
    page_title="SmartCampus AI – College Management System",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Core imports
from core.config import Config
from core.session import SessionManager
from database_engine.json_database import JSONDatabaseManager
from authentication.login import render_login_page
from authentication.register import render_registration_page
from components.sidebar import render_sidebar
from components.navbar import render_navbar
from components.footer import render_footer
from pages.home import render_home_page
from pages.dashboard import render_dashboard_page
from pages.notice_board import render_notice_board_page
from pages.placements import render_placements_page
from pages.workshops import render_workshops_page
from pages.chatbot import render_chatbot_page
from pages.settings import render_settings_page
from utils.logger import logger

def load_css():
    """Injects custom CSS from assets/styles.css into the app."""
    css_path = Config.ASSETS_DIR / "styles.css"
    if css_path.exists():
        with open(css_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def main():
    # 1. Initialize Database Engine & Session
    JSONDatabaseManager()
    SessionManager.init_session()
    
    # 2. Inject CSS styles
    load_css()

    # 3. Authentication Routing Check
    if not SessionManager.is_authenticated():
        # Display Auth View Container (Login or Register)
        st.markdown("<div style='max-width: 700px; margin: 40px auto; padding: 20px;'>", unsafe_allow_html=True)
        auth_view = st.session_state.get("auth_view", "login")
        if auth_view == "register":
            render_registration_page()
        else:
            render_login_page()
        st.markdown("</div>", unsafe_allow_html=True)
        return

    # 4. Authenticated Application Interface
    active_page = render_sidebar()
    render_navbar(active_page)

    # 5. Active Page Router
    if active_page == "Home":
        render_home_page()
    elif active_page == "Dashboard":
        render_dashboard_page()
    elif active_page == "Notice Board":
        render_notice_board_page()
    elif active_page == "Placements":
        render_placements_page()
    elif active_page == "Workshops":
        render_workshops_page()
    elif active_page == "SmartCampus AI Assistant":
        render_chatbot_page()
    elif active_page == "Settings":
        render_settings_page()
    else:
        render_home_page()

    # 6. Global Application Footer
    render_footer()

if __name__ == "__main__":
    main()
