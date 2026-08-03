"""
SmartCampus AI - Logout Module
Clears active user session states and redirects to login interface.
"""
import streamlit as st
from core.session import SessionManager
from utils.logger import logger

def perform_logout():
    """Logs out user and clears session state."""
    user = SessionManager.get_current_user()
    username = user.get("username", "user") if user else "user"
    logger.log_event("USER_LOGOUT", f"User logged out: {username}", username)
    SessionManager.logout_user()
    st.toast("Logged out successfully.", icon="🚪")
    st.rerun()
