"""
SmartCampus AI - User Login View
Authenticates student and admin credentials using bcrypt and manages session authorization state.
"""
import streamlit as st
from core.security import SecurityManager
from core.session import SessionManager
from database_engine.crud import JSONCRUDEngine
from utils.logger import logger

def render_login_page():
    """Renders the login form."""
    st.markdown('<h2 class="auth-header">🔐 Welcome to SmartCampus AI</h2>', unsafe_allow_html=True)
    st.markdown('<p class="auth-subtitle">Enter your credentials to access your SmartCampus workspace.</p>', unsafe_allow_html=True)

    users_crud = JSONCRUDEngine("users.json")

    with st.form("login_form", clear_on_submit=False):
        username_input = st.text_input("Username or Email", placeholder="e.g. alexj or alex.johnson@smartcampus.edu")
        password_input = st.text_input("Password", type="password", placeholder="Enter your password")
        
        submitted = st.form_submit_button("Sign In", use_container_width=True)

        if submitted:
            if not username_input or not password_input:
                st.warning("⚠️ Please fill in both Username/Email and Password.")
                return

            # Search by username or email
            users = users_crud.find_all()
            matched_user = None
            for u in users:
                if (u.get("username", "").lower() == username_input.strip().lower() or
                    u.get("email", "").lower() == username_input.strip().lower()):
                    matched_user = u
                    break

            if matched_user:
                stored_hash = matched_user.get("password", "")
                if SecurityManager.verify_password(password_input, stored_hash):
                    SessionManager.login_user(matched_user)
                    logger.log_event("USER_LOGIN", f"User logged in: {matched_user.get('username')}", matched_user.get('username'))
                    st.toast(f"Welcome back, {matched_user.get('full_name')}!", icon="🎉")
                    st.success("Login successful! Redirecting...")
                    st.rerun()
                else:
                    st.error("❌ Invalid password. Please try again.")
            else:
                st.error("❌ User not found with given credentials.")

    st.markdown("<div style='text-align: center; margin-top: 25px;'>", unsafe_allow_html=True)
    st.markdown("<strong>Don't have an account?</strong>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("✨ Create Account", use_container_width=True, key="goto_register"):
            st.session_state["auth_view"] = "register"
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
