"""
SmartCampus AI - Analytics Dashboard View
Renders key metrics, student stats, recent logs, quick action shortcuts,
and interactive Plotly visualizations (Pie, Line, Bar charts).
"""
import streamlit as st
import plotly.express as px
import pandas as pd
from core.session import SessionManager
from services.notice_service import NoticeService
from services.placement_service import PlacementService
from services.workshop_service import WorkshopService
from database_engine.crud import JSONCRUDEngine
from components.cards import render_metric_card

def render_dashboard_page():
    """Renders the Dashboard analytics view."""
    user = SessionManager.get_current_user()
    user_name = user.get("full_name", "Student") if user else "Student"

    notice_svc = NoticeService()
    placement_svc = PlacementService()
    workshop_svc = WorkshopService()
    users_crud = JSONCRUDEngine("users.json")
    logs_crud = JSONCRUDEngine("logs.json")

    # Fetch data
    all_users = users_crud.find_all()
    all_notices = notice_svc.get_all_notices()
    all_placements = placement_svc.get_all_placements()
    all_workshops = workshop_svc.get_all_workshops()
    recent_logs = logs_crud.find_all()[-5:]

    # 1. Top Metrics Bar
    st.markdown("### 📊 System Overview")
    m1, m2, m3, m4 = st.columns(4)

    with m1:
        render_metric_card("Total Registered Students", len(all_users), "Active Accounts", "🎓")
    with m2:
        render_metric_card("Active College Notices", len(all_notices), "Published Bulletins", "📢")
    with m3:
        render_metric_card("Placement Drives", len(all_placements), "Open Opportunities", "💼")
    with m4:
        render_metric_card("Upcoming Workshops", len(all_workshops), "Skill Sessions", "🎯")

    st.markdown("<br>", unsafe_allow_html=True)

    # 2. Interactive Plotly Visualizations Grid
    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("#### 🍩 Notice Distribution by Priority")
        if all_notices:
            df_notices = pd.DataFrame(all_notices)
            priority_counts = df_notices['priority'].value_counts().reset_index()
            priority_counts.columns = ['Priority', 'Count']
            
            fig_pie = px.pie(
                priority_counts,
                names='Priority',
                values='Count',
                hole=0.4,
                color_discrete_sequence=['#EF4444', '#F59E0B', '#10B981']
            )
            fig_pie.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#F8FAFC'),
                margin=dict(t=20, b=20, l=20, r=20),
                legend=dict(orientation="h", yanchor="bottom", y=-0.2)
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("No notice data available for chart.")

    with col_right:
        st.markdown("#### 📊 Workshop Capacity & Seats Filled")
        if all_workshops:
            df_wsp = pd.DataFrame(all_workshops)
            fig_bar = px.bar(
                df_wsp,
                x='workshop_name',
                y=['seats', 'registered_count'],
                barmode='group',
                labels={'value': 'Count', 'workshop_name': 'Workshop', 'variable': 'Metric'},
                color_discrete_sequence=['#6366F1', '#34D399']
            )
            fig_bar.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#F8FAFC'),
                margin=dict(t=20, b=20, l=20, r=20),
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)')
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("No workshop data available for chart.")

    # 3. Line Chart: Placement Deadline Timeline
    st.markdown("#### 📈 Placement Opportunities Timeline")
    if all_placements:
        df_plc = pd.DataFrame(all_placements)
        df_plc['deadline_dt'] = pd.to_datetime(df_plc['deadline'], errors='coerce')
        df_timeline = df_plc.sort_values('deadline_dt')
        
        fig_line = px.line(
            df_timeline,
            x='deadline',
            y='company',
            markers=True,
            title="Drive Deadlines",
            color_discrete_sequence=['#EC4899']
        )
        fig_line.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#F8FAFC'),
            margin=dict(t=30, b=20, l=20, r=20),
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)')
        )
        st.plotly_chart(fig_line, use_container_width=True)

    # 4. Quick Actions & Recent Activities
    col_act, col_logs = st.columns([1, 1])

    with col_act:
        st.markdown("#### ⚡ Quick Actions")
        st.markdown("""
        <div class="glass-card">
            <p style="color: #94A3B8; font-size: 13px;">Manage your SmartCampus workspace efficiently:</p>
        </div>
        """, unsafe_allow_html=True)
        q1, q2 = st.columns(2)
        with q1:
            if st.button("📢 Create Notice", use_container_width=True):
                st.session_state["active_page"] = "Notice Board"
                st.rerun()
        with q2:
            if st.button("💼 Add Placement Drive", use_container_width=True):
                st.session_state["active_page"] = "Placements"
                st.rerun()

    with col_logs:
        st.markdown("#### 🕒 Recent System Activity")
        if recent_logs:
            for log in reversed(recent_logs):
                st.markdown(f"""
                <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 8px; padding: 10px 14px; margin-bottom: 8px;">
                    <div style="display: flex; justify-content: space-between; font-size: 12px; color: #6366F1; font-weight: 600;">
                        <span>{log.get('action')}</span>
                        <span style="color: #64748B;">{log.get('timestamp')[:19].replace('T', ' ')}</span>
                    </div>
                    <div style="font-size: 13px; color: #CBD5E1; margin-top: 2px;">{log.get('details')}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No activity logs recorded.")
