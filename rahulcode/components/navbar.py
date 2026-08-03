"""
SmartCampus AI - Top Navbar Component
Renders the glassmorphic top header bar with date badge, page header, and user quick status.
"""
import streamlit as st
from utils.helpers import HelperUtils
from core.session import SessionManager

def render_navbar(page_title: str):
    """Renders top header navbar with user context."""
    user = SessionManager.get_current_user()
    today_str = HelperUtils.get_today_date_str()
    user_display = user.get('username', 'Guest') if user else 'Guest'

    st.markdown(f"""
    <div class="main-header">
        <div>
            <h1 class="title-text">{page_title}</h1>
            <p style="color: #94A3B8; font-size: 13px; margin: 2px 0 0 0;">SmartCampus AI Platform • Logged in as <strong>@{user_display}</strong></p>
        </div>
        <div style="background: rgba(99, 102, 241, 0.15); border: 1px solid rgba(99, 102, 241, 0.3); border-radius: 20px; padding: 6px 16px; color: #A5B4FC; font-size: 13px; font-weight: 600;">
            📅 {today_str}
        </div>
    </div>
    """, unsafe_allow_html=True)
