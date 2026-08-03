"""
SmartCampus AI - Notice Board View
Full CRUD interface for official announcements with search, filter, sort, and priority badge tags.
"""
import streamlit as st
from core.constants import DEPARTMENTS, NOTICE_PRIORITIES
from core.session import SessionManager
from services.notice_service import NoticeService
from components.cards import render_notice_card
from utils.logger import logger

def render_notice_board_page():
    """Renders Notice Board CRUD view."""
    user = SessionManager.get_current_user()
    user_name = user.get("full_name", "Admin") if user else "Admin"

    notice_svc = NoticeService()

    st.markdown("### 📢 Campus Notice Board")

    # Top Action & Filters Bar
    col_search, col_dept, col_priority = st.columns([2, 1, 1])

    with col_search:
        search_query = st.text_input("🔍 Search Notices", placeholder="Search by title, description, publisher...")
    with col_dept:
        selected_dept = st.selectbox("Department", ["All"] + DEPARTMENTS)
    with col_priority:
        selected_priority = st.selectbox("Priority", ["All"] + NOTICE_PRIORITIES)

    # 1. Create New Notice Expander Form
    with st.expander("➕ Publish New Notice", expanded=False):
        with st.form("create_notice_form", clear_on_submit=True):
            n_title = st.text_input("Notice Title *")
            n_desc = st.text_area("Description / Content *")
            c1, c2, c3 = st.columns(3)
            with c1:
                n_dept = st.selectbox("Department *", ["All Departments"] + DEPARTMENTS)
            with c2:
                n_priority = st.selectbox("Priority *", NOTICE_PRIORITIES)
            with c3:
                n_publisher = st.text_input("Publisher *", value=user_name)

            submit_notice = st.form_submit_button("Publish Announcement", use_container_width=True)

            if submit_notice:
                if not n_title.strip() or not n_desc.strip():
                    st.warning("⚠️ Title and Description are required.")
                else:
                    new_n = notice_svc.create_notice(n_title, n_desc, n_dept, n_priority, n_publisher)
                    logger.log_event("NOTICE_CREATED", f"Notice created: {n_title}", user_name)
                    st.toast("🎉 Notice published successfully!", icon="📢")
                    st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # 2. Filter & Display Notices List
    notices = notice_svc.filter_notices(search_query, selected_dept, selected_priority)

    st.markdown(f"**Found {len(notices)} Notice(s)**")

    if not notices:
        st.info("No notices match your current search and filter criteria.")
        return

    for notice in notices:
        render_notice_card(notice)

        # Update / Delete Controls Row
        c_edit, c_del, c_space = st.columns([1, 1, 4])
        
        with c_edit:
            with st.popover("✏️ Edit"):
                with st.form(f"edit_form_{notice.get('id')}"):
                    e_title = st.text_input("Title", value=notice.get("title"))
                    e_desc = st.text_area("Description", value=notice.get("description"))
                    e_dept = st.selectbox("Department", ["All Departments"] + DEPARTMENTS, index=0)
                    e_priority = st.selectbox("Priority", NOTICE_PRIORITIES, index=NOTICE_PRIORITIES.index(notice.get("priority", "Medium")))
                    e_pub = st.text_input("Publisher", value=notice.get("publisher"))
                    
                    e_save = st.form_submit_button("Save Changes")
                    if e_save:
                        notice_svc.update_notice(notice.get('id'), e_title, e_desc, e_dept, e_priority, e_pub)
                        st.toast("Notice updated successfully!")
                        st.rerun()

        with c_del:
            if st.button("🗑️ Delete", key=f"del_{notice.get('id')}"):
                notice_svc.delete_notice(notice.get('id'))
                logger.log_event("NOTICE_DELETED", f"Deleted notice ID: {notice.get('id')}", user_name)
                st.toast("Notice deleted.")
                st.rerun()

        st.markdown("<hr style='margin: 10px 0 25px 0; opacity: 0.1;'>", unsafe_allow_html=True)
