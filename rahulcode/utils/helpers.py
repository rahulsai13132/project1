"""
SmartCampus AI - Helper Functions
Formatting, date parsing, CSV generation, and utility functions.
"""
from datetime import datetime
import pandas as pd
from typing import List, Dict, Any

class HelperUtils:
    @staticmethod
    def get_today_date_str() -> str:
        """Returns today's date formatted nicely."""
        return datetime.now().strftime("%B %d, %Y")

    @staticmethod
    def format_date(date_str: str) -> str:
        """Formats ISO date string to human readable format."""
        try:
            dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
            return dt.strftime("%b %d, %Y")
        except Exception:
            return date_str

    @staticmethod
    def export_to_csv(data: List[Dict[str, Any]]) -> str:
        """Converts a list of dicts to CSV string."""
        if not data:
            return ""
        df = pd.DataFrame(data)
        return df.to_csv(index=False)

    @staticmethod
    def truncate_text(text: str, max_chars: int = 100) -> str:
        """Truncates text with ellipsis if longer than max_chars."""
        if not text:
            return ""
        if len(text) <= max_chars:
            return text
        return text[:max_chars].rstrip() + "..."
