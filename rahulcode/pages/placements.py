"""
SmartCampus AI - Placement Portal View
CRUD for campus drives, salary packages, eligibility filters, and CSV export functionality.
"""
import streamlit as st
from core.constants import PLACEMENT_STATUSES
from core.session import SessionManager
from services.placement_service import PlacementService
from components.cards import render_placement_card
from utils.helpers import HelperUtils
from utils.logger import logger

def render_placements_page():
    """Renders Placements Portal view."""
    user = SessionManager.get_current_user()
    user_name = user.get("full_name", "User") if user else "User"

    placement_svc = PlacementService()

    st.markdown("### 💼 Campus Placement & Internship Drives")

    # Search & Filter Controls
    col_search, col_status, col_export = st.columns([2, 1, 1])

    with col_search:
        search_query = st.text_input("🔍 Search Company / Skills", placeholder="e.g. Google, Python, Remote...")
    with col_status:
        selected_status = st.selectbox("Status", ["All"] + PLACEMENT_STATUSES)
    with col_export:
        all_placements = placement_svc.get_all_placements()
        csv_data = HelperUtils.export_to_csv(all_placements)
        st.download_button(
            label="📥 Export CSV",
            data=csv_data,
            file_name="smartcampus_placements_2026.csv",
            mime="text/csv",
            use_container_width=True
        )

    # 1. Add New Placement Drive Expander Form
    with st.expander("➕ Post New Placement Drive", expanded=False):
        with st.form("create_placement_form", clear_on_submit=True):
            c1, c2 = st.columns(2)
            with c1:
                p_company = st.text_input("Company Name *")
                p_package = st.text_input("Package Offered *", placeholder="e.g. $120,000 / year")
                p_location = st.text_input("Location *", placeholder="e.g. San Francisco, CA / Remote")
                p_deadline = st.date_input("Application Deadline *")
            with c2:
                p_eligibility = st.text_input("Eligibility Criteria *", placeholder="e.g. GPA >= 3.5, Final Year")
                p_skills = st.text_input("Skills Required *", placeholder="e.g. Python, SQL, React")
                p_link = st.text_input("Application Link *", placeholder="https://careers.company.com")
                p_status = st.selectbox("Drive Status *", PLACEMENT_STATUSES)

            submit_plc = st.form_submit_button("Publish Drive Listing", use_container_width=True)

            if submit_plc:
                if not p_company.strip() or not p_package.strip():
                    st.warning("⚠️ Company Name and Package are required.")
                else:
                    placement_svc.create_placement(
                        p_company, p_package, p_location, p_eligibility,
                        p_skills, str(p_deadline), p_link, p_status
                    )
                    logger.log_event("PLACEMENT_CREATED", f"Placement drive added: {p_company}", user_name)
                    st.toast("🎉 Placement drive published successfully!", icon="💼")
                    st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # 2. Filtered Listing
    placements = placement_svc.filter_placements(search_query, selected_status)
    st.markdown(f"**Displaying {len(placements)} Opportunity(ies)**")

    if not placements:
        st.info("No placement drives found matching your criteria.")
        return

    for item in placements:
        render_placement_card(item)

        # Action Buttons
        col_ed, col_del, col_sp = st.columns([1, 1, 4])
        with col_ed:
            with st.popover("✏️ Edit Drive"):
                with st.form(f"edit_plc_{item.get('id')}"):
                    e_comp = st.text_input("Company", value=item.get("company"))
                    e_pkg = st.text_input("Package", value=item.get("package"))
                    e_loc = st.text_input("Location", value=item.get("location"))
                    e_elig = st.text_input("Eligibility", value=item.get("eligibility"))
                    e_skills = st.text_input("Skills", value=item.get("skills_required"))
                    e_deadline = st.text_input("Deadline", value=item.get("deadline"))
                    e_link = st.text_input("Apply Link", value=item.get("apply_link"))
                    e_status = st.selectbox("Status", PLACEMENT_STATUSES, index=PLACEMENT_STATUSES.index(item.get("status", "Open")))

                    if st.form_submit_button("Save Drive"):
                        placement_svc.update_placement(
                            item.get('id'), e_comp, e_pkg, e_loc, e_elig, e_skills, e_deadline, e_link, e_status
                        )
                        st.toast("Placement drive updated!")
                        st.rerun()

        with col_del:
            if st.button("🗑️ Delete Drive", key=f"del_plc_{item.get('id')}"):
                placement_svc.delete_placement(item.get('id'))
                logger.log_event("PLACEMENT_DELETED", f"Deleted placement ID: {item.get('id')}", user_name)
                st.toast("Drive listing deleted.")
                st.rerun()

        st.markdown("<hr style='margin: 10px 0 25px 0; opacity: 0.1;'>", unsafe_allow_html=True)
