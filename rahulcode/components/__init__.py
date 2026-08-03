"""
SmartCampus AI Components Package
"""
from components.sidebar import render_sidebar
from components.navbar import render_navbar
from components.footer import render_footer
from components.cards import render_metric_card, render_notice_card, render_placement_card

__all__ = [
    "render_sidebar",
    "render_navbar",
    "render_footer",
    "render_metric_card",
    "render_notice_card",
    "render_placement_card"
]
