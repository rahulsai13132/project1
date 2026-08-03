"""
SmartCampus AI - Workshops Page View
CRUD for skill development workshops, trainer profiles, venue allocations, and seat registration tracking.
"""
import streamlit as st
from core.constants import DEPARTMENTS
from core.session import SessionManager
from services.workshop_service import WorkshopService
from utils.logger import logger

def render_workshops_page():
    """Renders Workshops management page."""
    user = SessionManager.get_current_user()
    user_name = user.get("full_name", "Student") if user else "Student"

    workshop_svc = WorkshopService()

    st.markdown("### 🎯 Skill Workshops & Masterclasses")

    # Search & Department Filter
    c_search, c_dept = st.columns([2, 1])
    with c_search:
        search_query = st.text_input("🔍 Search Workshops", placeholder="Search by name, trainer, topic...")
    with c_dept:
        selected_dept = st.selectbox("Department", ["All"] + DEPARTMENTS)

    # 1. Create New Workshop Expander
    with st.expander("➕ Host New Workshop", expanded=False):
        with st.form("create_workshop_form", clear_on_submit=True):
            w_name = st.text_input("Workshop Name *")
            w_trainer = st.text_input("Trainer / Speaker *", placeholder="e.g. Dr. Aris Thorne")
            w_venue = st.text_input("Venue / Platform *", placeholder="e.g. Auditorium A or Zoom")
            c1, c2, c3 = st.columns(3)
            with c1:
                w_dept = st.selectbox("Department *", DEPARTMENTS)
            with c2:
                w_date = st.date_input("Event Date *")
            with c3:
                w_seats = st.number_input("Total Capacity (Seats) *", min_value=1, value=50)
            
            w_desc = st.text_area("Workshop Description *")
            w_link = st.text_input("Registration Link / Info URL *", value="https://smartcampus.edu/register")

            submit_wsp = st.form_submit_button("Publish Workshop", use_container_width=True)

            if submit_wsp:
                if not w_name.strip() or not w_trainer.strip():
                    st.warning("⚠️ Workshop Name and Trainer are required.")
                else:
                    workshop_svc.create_workshop(
                        w_name, w_trainer, w_venue, w_dept,
                        str(w_date), w_seats, w_desc, w_link
                    )
                    logger.log_event("WORKSHOP_CREATED", f"Created workshop: {w_name}", user_name)
                    st.toast("🎉 Workshop created successfully!", icon="🎯")
                    st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # 2. Filtered Workshops Listing
    workshops = workshop_svc.filter_workshops(search_query, selected_dept)
    st.markdown(f"**Found {len(workshops)} Workshop(s)**")

    if not workshops:
        st.info("No workshops match your filters.")
        return

    for wsp in workshops:
        total_seats = wsp.get("seats", 50)
        registered = wsp.get("registered_count", 0)
        available = total_seats - registered

        st.markdown(f"""
        <div class="glass-card">
            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                <div>
                    <span style="background: rgba(99,102,241,0.2); color: #A5B4FC; padding: 4px 10px; border-radius: 12px; font-size: 11px; font-weight: 700; text-transform: uppercase;">{wsp.get('department')}</span>
                    <h3 style="margin: 8px 0 4px 0; color: #F8FAFC;">{wsp.get('workshop_name')}</h3>
                </div>
                <div style="text-align: right;">
                    <span style="font-size: 14px; font-weight: 700; color: {'#34D399' if available > 0 else '#F87171'};">
                        {available} / {total_seats} Seats Left
                    </span>
                </div>
            </div>
            <p style="color: #94A3B8; font-size: 14px; margin: 8px 0;"><strong>👨‍🏫 Instructor:</strong> {wsp.get('trainer')} | 📍 <strong>Venue:</strong> {wsp.get('venue')} | 📅 <strong>Date:</strong> {wsp.get('date')}</p>
            <p style="color: #CBD5E1; font-size: 13px;">{wsp.get('description')}</p>
        </div>
        """, unsafe_allow_html=True)

        # Action Buttons Row
        c_reg, c_ed, c_del, c_sp = st.columns([2, 1, 1, 3])

        with c_reg:
            if available > 0:
                if st.button("✨ Register Seat Now", key=f"reg_wsp_{wsp.get('id')}", use_container_width=True):
                    workshop_svc.register_user_for_workshop(wsp.get('id'))
                    logger.log_event("WORKSHOP_REGISTRATION", f"User registered for workshop: {wsp.get('workshop_name')}", user_name)
                    st.toast(f"🎉 Successfully registered for {wsp.get('workshop_name')}!", icon="✅")
                    st.rerun()
            else:
                st.button("🚫 Workshop Full", disabled=True, key=f"full_wsp_{wsp.get('id')}", use_container_width=True)

        with c_ed:
            with st.popover("✏️ Edit"):
                with st.form(f"edit_wsp_{wsp.get('id')}"):
                    e_name = st.text_input("Name", value=wsp.get("workshop_name"))
                    e_trainer = st.text_input("Trainer", value=wsp.get("trainer"))
                    e_venue = st.text_input("Venue", value=wsp.get("venue"))
                    e_dept = st.selectbox("Department", DEPARTMENTS, index=DEPARTMENTS.index(wsp.get("department")) if wsp.get("department") in DEPARTMENTS else 0)
                    e_date = st.text_input("Date", value=wsp.get("date"))
                    e_seats = st.number_input("Seats", value=wsp.get("seats"))
                    e_desc = st.text_area("Description", value=wsp.get("description"))
                    e_link = st.text_input("Link", value=wsp.get("registration_link"))

                    if st.form_submit_button("Save Changes"):
                        workshop_svc.update_workshop(
                            wsp.get('id'), e_name, e_trainer, e_venue, e_dept, e_date, e_seats, e_desc, e_link
                        )
                        st.toast("Workshop details updated!")
                        st.rerun()

        with c_del:
            if st.button("🗑️ Delete", key=f"del_wsp_{wsp.get('id')}"):
                workshop_svc.delete_workshop(wsp.get('id'))
                logger.log_event("WORKSHOP_DELETED", f"Deleted workshop ID: {wsp.get('id')}", user_name)
                st.toast("Workshop deleted.")
                st.rerun()

        st.markdown("<hr style='margin: 10px 0 25px 0; opacity: 0.1;'>", unsafe_allow_html=True)
