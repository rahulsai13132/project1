"""
SmartCampus AI - Workshop Service
Manages college workshops, seat allocations, registrations, and CRUD.
"""
import uuid
from typing import List, Dict, Any, Optional
from database_engine.crud import JSONCRUDEngine

class WorkshopService:
    def __init__(self):
        self.crud = JSONCRUDEngine("workshops.json")

    def get_all_workshops(self) -> List[Dict[str, Any]]:
        """Returns all workshop items."""
        return self.crud.find_all()

    def get_workshop_by_id(self, workshop_id: str) -> Optional[Dict[str, Any]]:
        """Reads workshop by ID."""
        return self.crud.read("id", workshop_id)

    def create_workshop(
        self, workshop_name: str, trainer: str, venue: str, department: str,
        date: str, seats: int, description: str, registration_link: str
    ) -> Dict[str, Any]:
        """Creates a new workshop."""
        new_item = {
            "id": f"wsp_{uuid.uuid4().hex[:8]}",
            "workshop_name": workshop_name.strip(),
            "trainer": trainer.strip(),
            "venue": venue.strip(),
            "department": department,
            "date": date,
            "seats": int(seats),
            "description": description.strip(),
            "registration_link": registration_link.strip(),
            "registered_count": 0
        }
        self.crud.create(new_item)
        return new_item

    def update_workshop(
        self, workshop_id: str, workshop_name: str, trainer: str, venue: str, department: str,
        date: str, seats: int, description: str, registration_link: str
    ) -> bool:
        """Updates workshop details."""
        updated_data = {
            "workshop_name": workshop_name.strip(),
            "trainer": trainer.strip(),
            "venue": venue.strip(),
            "department": department,
            "date": date,
            "seats": int(seats),
            "description": description.strip(),
            "registration_link": registration_link.strip()
        }
        return self.crud.update("id", workshop_id, updated_data)

    def delete_workshop(self, workshop_id: str) -> bool:
        """Deletes workshop by ID."""
        return self.crud.delete("id", workshop_id)

    def register_user_for_workshop(self, workshop_id: str) -> bool:
        """Increments registered seat count if seats available."""
        wsp = self.get_workshop_by_id(workshop_id)
        if not wsp:
            return False
        seats = wsp.get("seats", 0)
        reg_count = wsp.get("registered_count", 0)
        if reg_count < seats:
            return self.crud.update("id", workshop_id, {"registered_count": reg_count + 1})
        return False

    def filter_workshops(self, search_term: str = "", department: str = "All") -> List[Dict[str, Any]]:
        """Filters workshops by query string and department."""
        items = self.get_all_workshops()
        filtered = []
        for item in items:
            matches_search = (
                not search_term or
                search_term.lower() in item.get("workshop_name", "").lower() or
                search_term.lower() in item.get("trainer", "").lower() or
                search_term.lower() in item.get("description", "").lower()
            )
            matches_dept = (department == "All" or item.get("department") == department)
            if matches_search and matches_dept:
                filtered.append(item)
        return filtered
