"""
SmartCampus AI - User Registration View
Handles student account creation, field validation, duplicate checking, and bcrypt password hashing.
"""
import uuid
from datetime import datetime
import streamlit as st
from core.constants import DEPARTMENTS, ACADEMIC_YEARS
from core.security import SecurityManager
from database_engine.crud import JSONCRUDEngine
from utils.validators import InputValidator
from utils.logger import logger

def render_registration_page():
    """Renders user registration form."""
    st.markdown('<h2 class="auth-header">🚀 Create SmartCampus Account</h2>', unsafe_allow_html=True)
    st.markdown('<p class="auth-subtitle">Join the SmartCampus AI ecosystem to access personalized tools & insights.</p>', unsafe_allow_html=True)

    users_crud = JSONCRUDEngine("users.json")

    with st.form("registration_form", clear_on_submit=False):
        col1, col2 = st.columns(2)
        with col1:
            full_name = st.text_input("Full Name *", placeholder="e.g. Jane Doe")
            student_id = st.text_input("Student ID *", placeholder="e.g. STU2026105")
            department = st.selectbox("Department *", DEPARTMENTS)
            year = st.selectbox("Academic Year *", ACADEMIC_YEARS)
            email = st.text_input("Email Address *", placeholder="jane.doe@smartcampus.edu")

        with col2:
            mobile = st.text_input("Mobile Number *", placeholder="+19876543210")
            username = st.text_input("Username *", placeholder="janedoe")
            password = st.text_input("Password *", type="password")
            confirm_password = st.text_input("Confirm Password *", type="password")

        submitted = st.form_submit_button("Register Account", use_container_width=True)

        if submitted:
            # 1. Input Validation
            valid, msg = InputValidator.validate_registration(
                full_name, student_id, email, mobile, username, password, confirm_password
            )
            if not valid:
                st.error(f"❌ {msg}")
                return

            # 2. Check for duplicate username / email
            existing_users = users_crud.find_all()
            for u in existing_users:
                if u.get("username", "").lower() == username.strip().lower():
                    st.error("❌ Username already taken. Please choose another.")
                    return
                if u.get("email", "").lower() == email.strip().lower():
                    st.error("❌ Email address already registered. Please login instead.")
                    return

            # 3. Hash password & create user record
            hashed_pass = SecurityManager.hash_password(password)
            new_user = {
                "id": f"usr_{uuid.uuid4().hex[:8]}",
                "full_name": full_name.strip(),
                "student_id": student_id.strip(),
                "department": department,
                "year": year,
                "email": email.strip(),
                "mobile": mobile.strip(),
                "username": username.strip(),
                "password": hashed_pass,
                "created_at": datetime.now().isoformat()
            }

            success, _ = users_crud.create(new_user)
            if success:
                logger.log_event("USER_REGISTRATION", f"Registered new user: {username}", username)
                st.success("🎉 Registration successful! Redirecting to login page...")
                st.session_state["auth_view"] = "login"
                st.rerun()
            else:
                st.error("❌ Failed to save user account. Please try again.")

    st.markdown("<hr style='margin: 20px 0; opacity: 0.2;'>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        if st.button("Already have an account? Log In", use_container_width=True, key="switch_to_login"):
            st.session_state["auth_view"] = "login"
            st.rerun()
