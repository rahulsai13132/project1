"""
SmartCampus AI Core Module
"""
from core.config import Config
from core.constants import DEPARTMENTS, ACADEMIC_YEARS, NOTICE_PRIORITIES, PLACEMENT_STATUSES, THEME_MODES, LANGUAGES, MOTIVATIONAL_QUOTES
from core.security import SecurityManager
from core.session import SessionManager

__all__ = [
    "Config",
    "DEPARTMENTS",
    "ACADEMIC_YEARS",
    "NOTICE_PRIORITIES",
    "PLACEMENT_STATUSES",
    "THEME_MODES",
    "LANGUAGES",
    "MOTIVATIONAL_QUOTES",
    "SecurityManager",
    "SessionManager"
]
