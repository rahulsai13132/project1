"""
SmartCampus AI - Notice Service
Manages college announcements, priority filtering, department matching, and CRUD using JSONCRUDEngine.
"""
import uuid
from datetime import datetime
from typing import List, Dict, Any, Optional
from database_engine.crud import JSONCRUDEngine

class NoticeService:
    def __init__(self):
        self.crud = JSONCRUDEngine("notices.json")

    def get_all_notices(self) -> List[Dict[str, Any]]:
        """Retrieves all notices sorted by date descending."""
        notices = self.crud.find_all()
        return sorted(notices, key=lambda x: x.get("date", ""), reverse=True)

    def get_notice_by_id(self, notice_id: str) -> Optional[Dict[str, Any]]:
        """Finds notice by notice ID."""
        return self.crud.read("id", notice_id)

    def create_notice(self, title: str, description: str, department: str, priority: str, publisher: str) -> Dict[str, Any]:
        """Creates and persists a new notice."""
        new_notice = {
            "id": f"not_{uuid.uuid4().hex[:8]}",
            "title": title.strip(),
            "description": description.strip(),
            "department": department,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "priority": priority,
            "publisher": publisher.strip()
        }
        self.crud.create(new_notice)
        return new_notice

    def update_notice(self, notice_id: str, title: str, description: str, department: str, priority: str, publisher: str) -> bool:
        """Updates notice fields."""
        updated_data = {
            "title": title.strip(),
            "description": description.strip(),
            "department": department,
            "priority": priority,
            "publisher": publisher.strip()
        }
        return self.crud.update("id", notice_id, updated_data)

    def delete_notice(self, notice_id: str) -> bool:
        """Deletes notice by ID."""
        return self.crud.delete("id", notice_id)

    def filter_notices(self, search_term: str = "", department: str = "All", priority: str = "All") -> List[Dict[str, Any]]:
        """Filters and searches notices."""
        notices = self.get_all_notices()
        filtered = []
        for n in notices:
            matches_search = (
                not search_term or
                search_term.lower() in n.get("title", "").lower() or
                search_term.lower() in n.get("description", "").lower() or
                search_term.lower() in n.get("publisher", "").lower()
            )
            matches_dept = (department == "All" or n.get("department") == department or n.get("department") == "All Departments")
            matches_priority = (priority == "All" or n.get("priority") == priority)

            if matches_search and matches_dept and matches_priority:
                filtered.append(n)
        return filtered
