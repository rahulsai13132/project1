"""
SmartCampus AI - Session State Manager
Manages Streamlit user session states, active page selection, and login credentials.
"""
import streamlit as st
from typing import Dict, Any, Optional

class SessionManager:
    @staticmethod
    def init_session():
        """Initializes session variables if not already set."""
        if "authenticated" not in st.session_state:
            st.session_state["authenticated"] = False
        if "user" not in st.session_state:
            st.session_state["user"] = None
        if "active_page" not in st.session_state:
            st.session_state["active_page"] = "Home"
        if "theme" not in st.session_state:
            st.session_state["theme"] = "Dark"
        if "chat_history" not in st.session_state:
            st.session_state["chat_history"] = []
        if "auth_view" not in st.session_state:
            st.session_state["auth_view"] = "login"

    @staticmethod
    def login_user(user_data: Dict[str, Any]):
        """Logs in user by setting session parameters."""
        st.session_state["authenticated"] = True
        st.session_state["user"] = user_data
        st.session_state["active_page"] = "Home"

    @staticmethod
    def logout_user():
        """Logs out user and resets session states."""
        st.session_state["authenticated"] = False
        st.session_state["user"] = None
        st.session_state["active_page"] = "Home"
        st.session_state["auth_view"] = "login"

    @staticmethod
    def get_current_user() -> Optional[Dict[str, Any]]:
        """Returns the current logged-in user details."""
        return st.session_state.get("user")

    @staticmethod
    def is_authenticated() -> bool:
        """Returns True if a user is logged in."""
        return st.session_state.get("authenticated", False)
