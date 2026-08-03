"""
SmartCampus AI - Home Page View
Renders College Banner, Welcome Section, Latest Notices, Upcoming Workshops, Placement Highlights,
Motivational Quote generator, AI Suggestions, and Quick Navigation Cards.
"""
import random
import streamlit as st
from core.session import SessionManager
from core.constants import MOTIVATIONAL_QUOTES
from services.notice_service import NoticeService
from services.placement_service import PlacementService
from services.workshop_service import WorkshopService
from components.cards import render_notice_card, render_placement_card

def render_home_page():
    """Renders the Home page view."""
    user = SessionManager.get_current_user()
    user_name = user.get("full_name", "Student") if user else "Student"
    user_dept = user.get("department", "Engineering") if user else "Engineering"

    # Services
    notice_svc = NoticeService()
    placement_svc = PlacementService()
    workshop_svc = WorkshopService()

    # 1. Hero Banner Visual
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(99, 102, 241, 0.2), rgba(168, 85, 247, 0.2)); border: 1px solid rgba(255, 255, 255, 0.15); border-radius: 16px; padding: 30px; margin-bottom: 25px; backdrop-filter: blur(12px);">
        <h1 style="font-family: 'Outfit', sans-serif; font-size: 32px; font-weight: 800; background: linear-gradient(135deg, #6366F1, #A855F7, #EC4899); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 0 0 10px 0;">
            Welcome to SmartCampus AI, {user_name}! 👋
        </h1>
        <p style="color: #CBD5E1; font-size: 15px; max-width: 800px; margin: 0 0 20px 0;">
            Your centralized AI-powered hub for campus announcements, career placement preparation, skill workshops, and intelligent academic assistance in <strong>{user_dept}</strong>.
        </p>
        <div style="display: flex; gap: 12px; flex-wrap: wrap;">
            <span style="background: rgba(99, 102, 241, 0.3); border: 1px solid rgba(99, 102, 241, 0.5); color: #A5B4FC; padding: 6px 14px; border-radius: 20px; font-size: 12px; font-weight: 600;">✨ AI Career Assistant Active</span>
            <span style="background: rgba(16, 185, 129, 0.3); border: 1px solid rgba(16, 185, 129, 0.5); color: #6EE7B7; padding: 6px 14px; border-radius: 20px; font-size: 12px; font-weight: 600;">⚡ Campus Drives Open</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 2. Motivational Quote Card
    quote = random.choice(MOTIVATIONAL_QUOTES)
    st.markdown(f"""
    <div style="background: rgba(18, 24, 38, 0.6); border-left: 4px solid #A855F7; padding: 14px 20px; border-radius: 8px; margin-bottom: 25px;">
        <span style="font-size: 13px; color: #94A3B8; font-style: italic;">💡 Daily Inspiration:</span>
        <p style="font-size: 15px; color: #F8FAFC; margin: 4px 0 0 0; font-weight: 500;">"{quote}"</p>
    </div>
    """, unsafe_allow_html=True)

    # 3. Quick Navigation Cards Grid
    st.markdown("### ⚡ Quick Navigation")
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        if st.button("📊 View Dashboard", use_container_width=True):
            st.session_state["active_page"] = "Dashboard"
            st.rerun()
    with c2:
        if st.button("📢 Notice Board", use_container_width=True):
            st.session_state["active_page"] = "Notice Board"
            st.rerun()
    with c3:
        if st.button("💼 Placement Portal", use_container_width=True):
            st.session_state["active_page"] = "Placements"
            st.rerun()
    with c4:
        if st.button("🤖 Ask AI Assistant", use_container_width=True):
            st.session_state["active_page"] = "SmartCampus AI Assistant"
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # 4. Main Two Column Grid: Notices & Placements Preview
    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("### 📢 Latest Announcements")
        recent_notices = notice_svc.get_all_notices()[:3]
        if recent_notices:
            for notice in recent_notices:
                render_notice_card(notice)
        else:
            st.info("No active notices found.")

    with col_right:
        st.markdown("### 💼 Featured Placement Drives")
        featured_placements = placement_svc.get_all_placements()[:2]
        if featured_placements:
            for plc in featured_placements:
                render_placement_card(plc)
        else:
            st.info("No placement drives available right now.")

    # 5. Upcoming Workshops Section
    st.markdown("### 🎯 Upcoming Workshops")
    workshops = workshop_svc.get_all_workshops()[:2]
    if workshops:
        w_cols = st.columns(len(workshops))
        for idx, wsp in enumerate(workshops):
            with w_cols[idx]:
                st.markdown(f"""
                <div class="glass-card">
                    <div style="font-size: 12px; color: #6366F1; font-weight: 700; text-transform: uppercase;">{wsp.get('department')}</div>
                    <h4 style="margin: 6px 0; color: #F8FAFC;">{wsp.get('workshop_name')}</h4>
                    <p style="color: #94A3B8; font-size: 13px;">👨‍🏫 Trainer: {wsp.get('trainer')}</p>
                    <p style="color: #CBD5E1; font-size: 12px;">📅 {wsp.get('date')} | 📍 {wsp.get('venue')}</p>
                    <div style="background: rgba(255,255,255,0.05); padding: 8px; border-radius: 8px; font-size: 12px; color: #34D399;">
                        💺 Available Seats: {wsp.get('seats', 0) - wsp.get('registered_count', 0)} / {wsp.get('seats')}
                    </div>
                </div>
                """, unsafe_allow_html=True)
