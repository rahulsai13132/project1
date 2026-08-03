"""
SmartCampus AI - Card Components
Reusable glassmorphism UI card renderers for metrics, notices, placements, and workshops.
"""
import streamlit as st
from typing import Dict, Any, Optional

def render_metric_card(title: str, value: Any, subtext: str = "", icon: str = "📊"):
    """Renders a sleek glassmorphic metric card."""
    html_code = f"""
    <div class="metric-card">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <span class="metric-label">{title}</span>
            <span style="font-size: 20px;">{icon}</span>
        </div>
        <div class="metric-value">{value}</div>
        <div class="metric-subtext">{subtext}</div>
    </div>
    """
    st.markdown(html_code, unsafe_allow_html=True)

def render_notice_card(notice: Dict[str, Any], show_actions: bool = False) -> Optional[str]:
    """Renders a notice card with priority badges and metadata."""
    priority = notice.get("priority", "Low")
    badge_class = f"badge-{priority.lower()}"
    
    st.markdown(f"""
    <div class="glass-card">
        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
            <h4 style="margin: 0; font-size: 18px; color: #F8FAFC;">{notice.get('title')}</h4>
            <span class="badge {badge_class}">{priority}</span>
        </div>
        <p style="color: #94A3B8; font-size: 14px; margin: 10px 0;">{notice.get('description')}</p>
        <div style="display: flex; justify-content: space-between; font-size: 12px; color: #64748B; border-top: 1px solid rgba(255,255,255,0.08); padding-top: 10px; margin-top: 10px;">
            <span>🏢 Department: <strong>{notice.get('department')}</strong></span>
            <span>👤 By: <strong>{notice.get('publisher')}</strong></span>
            <span>📅 {notice.get('date')}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_placement_card(placement: Dict[str, Any]):
    """Renders a placement opportunity card."""
    status = placement.get("status", "Open")
    badge_color = "#34D399" if status == "Open" else ("#FBBF24" if status == "Upcoming" else "#F87171")
    
    st.markdown(f"""
    <div class="glass-card">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <h3 style="margin: 0; color: #F8FAFC;">{placement.get('company')}</h3>
            <span style="background: rgba(255,255,255,0.1); color: {badge_color}; padding: 4px 12px; border-radius: 12px; font-weight: 600; font-size: 12px;">{status}</span>
        </div>
        <div style="margin: 12px 0;">
            <span style="font-size: 20px; font-weight: 700; color: #6366F1;">💰 {placement.get('package')}</span>
            <span style="color: #94A3B8; font-size: 13px; margin-left: 15px;">📍 {placement.get('location')}</span>
        </div>
        <p style="color: #CBD5E1; font-size: 13px; margin: 6px 0;"><strong>Eligibility:</strong> {placement.get('eligibility')}</p>
        <p style="color: #CBD5E1; font-size: 13px; margin: 6px 0;"><strong>Required Skills:</strong> {placement.get('skills_required')}</p>
        <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 14px; pt: 10px; border-top: 1px solid rgba(255,255,255,0.08);">
            <span style="font-size: 12px; color: #F43F5E;">⏳ Deadline: {placement.get('deadline')}</span>
            <a href="{placement.get('apply_link')}" target="_blank" style="background: linear-gradient(135deg, #6366F1, #A855F7); color: white; padding: 6px 16px; border-radius: 8px; text-decoration: none; font-size: 12px; font-weight: 600;">Apply Now ↗</a>
        </div>
    </div>
    """, unsafe_allow_html=True)
