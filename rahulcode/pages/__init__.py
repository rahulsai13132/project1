"""
SmartCampus AI Pages Package
"""
from pages.home import render_home_page
from pages.dashboard import render_dashboard_page
from pages.notice_board import render_notice_board_page
from pages.placements import render_placements_page
from pages.workshops import render_workshops_page
from pages.chatbot import render_chatbot_page
from pages.settings import render_settings_page

__all__ = [
    "render_home_page",
    "render_dashboard_page",
    "render_notice_board_page",
    "render_placements_page",
    "render_workshops_page",
    "render_chatbot_page",
    "render_settings_page"
]
