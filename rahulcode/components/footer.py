"""
SmartCampus AI - Footer Component
Renders the bottom application footer with copyright and system status.
"""
import streamlit as st

def render_footer():
    """Renders bottom page footer."""
    st.markdown("""
    <div style="text-align: center; padding: 30px 0 15px 0; color: #64748B; font-size: 12px; border-top: 1px solid rgba(255,255,255,0.08); margin-top: 40px;">
        <p style="margin: 0;">SmartCampus AI System • Built with Streamlit &amp; OpenAI Engine</p>
        <p style="margin: 4px 0 0 0;">© 2026 SmartCampus AI Technologies Inc. All rights reserved.</p>
    </div>
    """, unsafe_allow_html=True)
