"""
SmartCampus AI - Placement Service
Manages placement drives, job listings, applications, eligibility, and CSV exports.
"""
import uuid
from typing import List, Dict, Any, Optional
from database_engine.crud import JSONCRUDEngine

class PlacementService:
    def __init__(self):
        self.crud = JSONCRUDEngine("placements.json")

    def get_all_placements(self) -> List[Dict[str, Any]]:
        """Returns all placement opportunities."""
        return self.crud.find_all()

    def get_placement_by_id(self, placement_id: str) -> Optional[Dict[str, Any]]:
        """Reads placement by ID."""
        return self.crud.read("id", placement_id)

    def create_placement(
        self, company: str, package: str, location: str, eligibility: str,
        skills_required: str, deadline: str, apply_link: str, status: str
    ) -> Dict[str, Any]:
        """Creates a new placement opportunity."""
        new_item = {
            "id": f"plc_{uuid.uuid4().hex[:8]}",
            "company": company.strip(),
            "package": package.strip(),
            "location": location.strip(),
            "eligibility": eligibility.strip(),
            "skills_required": skills_required.strip(),
            "deadline": deadline,
            "apply_link": apply_link.strip(),
            "status": status
        }
        self.crud.create(new_item)
        return new_item

    def update_placement(
        self, placement_id: str, company: str, package: str, location: str,
        eligibility: str, skills_required: str, deadline: str, apply_link: str, status: str
    ) -> bool:
        """Updates placement entry."""
        updated_data = {
            "company": company.strip(),
            "package": package.strip(),
            "location": location.strip(),
            "eligibility": eligibility.strip(),
            "skills_required": skills_required.strip(),
            "deadline": deadline,
            "apply_link": apply_link.strip(),
            "status": status
        }
        return self.crud.update("id", placement_id, updated_data)

    def delete_placement(self, placement_id: str) -> bool:
        """Deletes placement entry by ID."""
        return self.crud.delete("id", placement_id)

    def filter_placements(self, search_term: str = "", status: str = "All") -> List[Dict[str, Any]]:
        """Filters placement listings by search term and status."""
        items = self.get_all_placements()
        filtered = []
        for item in items:
            matches_search = (
                not search_term or
                search_term.lower() in item.get("company", "").lower() or
                search_term.lower() in item.get("skills_required", "").lower() or
                search_term.lower() in item.get("location", "").lower()
            )
            matches_status = (status == "All" or item.get("status") == status)
            if matches_search and matches_status:
                filtered.append(item)
        return filtered
