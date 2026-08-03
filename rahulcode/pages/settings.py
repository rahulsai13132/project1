"""
SmartCampus AI - Settings & Profile View
User profile updates, password change, dark/light theme options, notification toggles, and language preferences.
"""
import streamlit as st
from core.constants import DEPARTMENTS, ACADEMIC_YEARS, THEME_MODES, LANGUAGES
from core.security import SecurityManager
from core.session import SessionManager
from database_engine.crud import JSONCRUDEngine
from utils.validators import InputValidator
from utils.logger import logger

def render_settings_page():
    """Renders Settings and User Profile management view."""
    user = SessionManager.get_current_user()
    if not user:
        st.warning("Please log in to manage your settings.")
        return

    users_crud = JSONCRUDEngine("users.json")
    settings_crud = JSONCRUDEngine("settings.json")

    st.markdown("### ⚙ Account Settings & Preferences")

    tab1, tab2, tab3 = st.tabs(["👤 Profile Information", "🔐 Security & Password", "🎨 System Preferences"])

    # --- TAB 1: Profile Information ---
    with tab1:
        st.markdown("#### Update Personal Information")
        with st.form("profile_form"):
            col1, col2 = st.columns(2)
            with col1:
                f_name = st.text_input("Full Name", value=user.get("full_name", ""))
                s_id = st.text_input("Student ID", value=user.get("student_id", ""), disabled=True)
                dept = st.selectbox("Department", DEPARTMENTS, index=DEPARTMENTS.index(user.get("department")) if user.get("department") in DEPARTMENTS else 0)
            with col2:
                year = st.selectbox("Academic Year", ACADEMIC_YEARS, index=ACADEMIC_YEARS.index(user.get("year")) if user.get("year") in ACADEMIC_YEARS else 0)
                email = st.text_input("Email", value=user.get("email", ""))
                mobile = st.text_input("Mobile Number", value=user.get("mobile", ""))

            st.markdown("##### 🖼 Profile Picture")
            uploaded_pic = st.file_uploader("Upload Avatar / Profile Picture", type=["png", "jpg", "jpeg"])
            if uploaded_pic:
                st.image(uploaded_pic, width=100, caption="Preview Avatar")

            save_profile = st.form_submit_button("Save Profile Updates")

            if save_profile:
                if not InputValidator.validate_email(email):
                    st.error("❌ Invalid email format.")
                elif not InputValidator.validate_mobile(mobile):
                    st.error("❌ Invalid mobile format.")
                else:
                    updated_user = {
                        "full_name": f_name.strip(),
                        "department": dept,
                        "year": year,
                        "email": email.strip(),
                        "mobile": mobile.strip()
                    }
                    users_crud.update("id", user.get("id"), updated_user)
                    
                    # Update local session state
                    user.update(updated_user)
                    st.session_state["user"] = user
                    logger.log_event("PROFILE_UPDATED", f"Updated profile for: {user.get('username')}", user.get('username'))
                    st.toast("🎉 Profile updated successfully!", icon="✅")
                    st.rerun()

    # --- TAB 2: Security & Password ---
    with tab2:
        st.markdown("#### Change Account Password")
        with st.form("password_form"):
            curr_pass = st.text_input("Current Password", type="password")
            new_pass = st.text_input("New Password", type="password")
            confirm_new_pass = st.text_input("Confirm New Password", type="password")

            save_pass = st.form_submit_button("Update Password")

            if save_pass:
                stored_hash = user.get("password", "")
                if not SecurityManager.verify_password(curr_pass, stored_hash):
                    st.error("❌ Current password is incorrect.")
                else:
                    valid, msg = InputValidator.validate_password(new_pass, confirm_new_pass)
                    if not valid:
                        st.error(f"❌ {msg}")
                    else:
                        new_hash = SecurityManager.hash_password(new_pass)
                        users_crud.update("id", user.get("id"), {"password": new_hash})
                        user["password"] = new_hash
                        st.session_state["user"] = user
                        logger.log_event("PASSWORD_CHANGED", f"Changed password for: {user.get('username')}", user.get('username'))
                        st.toast("🎉 Password updated successfully!", icon="🔐")
                        st.rerun()

    # --- TAB 3: System Preferences ---
    with tab3:
        st.markdown("#### App Customization")
        current_settings = settings_crud.read("id", "setting_global") or {}

        with st.form("preferences_form"):
            theme_choice = st.selectbox("Theme Mode", THEME_MODES, index=0 if current_settings.get("theme_mode", "Dark") == "Dark" else 1)
            notify_enabled = st.toggle("Enable Desktop & In-App Notifications", value=current_settings.get("notifications_enabled", True))
            lang_choice = st.selectbox("Interface Language", LANGUAGES, index=LANGUAGES.index(current_settings.get("language", "English")) if current_settings.get("language") in LANGUAGES else 0)
            auto_summ = st.toggle("Auto-Summarize High Priority Notices", value=current_settings.get("auto_summarize_notices", True))

            save_pref = st.form_submit_button("Save Preferences")

            if save_pref:
                updated_settings = {
                    "id": "setting_global",
                    "theme_mode": theme_choice,
                    "notifications_enabled": notify_enabled,
                    "language": lang_choice,
                    "auto_summarize_notices": auto_summ
                }
                settings_crud.update("id", "setting_global", updated_settings)
                st.session_state["theme"] = theme_choice
                st.toast("🎉 Preferences saved!", icon="⚙")
                st.rerun()
