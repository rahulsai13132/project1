"""
SmartCampus AI - Logging Utilities
Provides unified application logging to standard output and database logs.
"""
import logging
from datetime import datetime
from typing import Dict, Any

# Configure standard Python logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

class AppLogger:
    def __init__(self, name: str = "SmartCampusAI"):
        self.logger = logging.getLogger(name)

    def info(self, msg: str):
        self.logger.info(msg)

    def warning(self, msg: str):
        self.logger.warning(msg)

    def error(self, msg: str):
        self.logger.error(msg)

    def log_event(self, action: str, details: str, user: str = "system") -> Dict[str, Any]:
        """Creates a structured log event entry."""
        log_entry = {
            "id": f"log_{datetime.now().strftime('%Y%m%d%H%M%S%f')}",
            "timestamp": datetime.now().isoformat(),
            "user": user,
            "action": action,
            "details": details
        }
        self.info(f"[{user}] {action}: {details}")
        return log_entry

logger = AppLogger()
