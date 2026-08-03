"""
SmartCampus AI Authentication Package
"""
from authentication.login import render_login_page
from authentication.register import render_registration_page
from authentication.logout import perform_logout

__all__ = ["render_login_page", "render_registration_page", "perform_logout"]
