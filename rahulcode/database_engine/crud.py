"""
SmartCampus AI - Generic CRUD Engine
Reusable CRUD abstraction for all JSON database models.
Provides create(), read(), update(), delete(), find(), find_all(), save(), and load().
"""
from typing import List, Dict, Any, Optional, Callable
from database_engine.json_database import JSONDatabaseManager
from utils.logger import logger

class JSONCRUDEngine:
    """Generic CRUD operations manager for JSON file resources."""

    def __init__(self, resource_name: str, db_manager: Optional[JSONDatabaseManager] = None):
        self.resource_name = resource_name if resource_name.endswith(".json") else f"{resource_name}.json"
        self.db_manager = db_manager or JSONDatabaseManager()

    def load(self) -> List[Dict[str, Any]]:
        """Loads all records from the JSON database file."""
        return self.db_manager.read_file(self.resource_name)

    def save(self, data: List[Dict[str, Any]]) -> bool:
        """Saves full list of records back to the JSON database file."""
        return self.db_manager.write_file(self.resource_name, data)

    def find_all(self) -> List[Dict[str, Any]]:
        """Returns all items in the collection."""
        return self.load()

    def find(self, predicate: Callable[[Dict[str, Any]], bool]) -> List[Dict[str, Any]]:
        """Finds all records matching a filter predicate function."""
        records = self.load()
        return [item for item in records if predicate(item)]

    def read(self, key: str, value: Any) -> Optional[Dict[str, Any]]:
        """Reads a single item by key-value match (e.g. id='not_001')."""
        records = self.load()
        for item in records:
            if item.get(key) == value:
                return item
        return None

    def create(self, item: Dict[str, Any]) -> Tuple_Item:
        """Creates a new record and appends it to the dataset."""
        records = self.load()
        records.append(item)
        success = self.save(records)
        if success:
            logger.info(f"Created record in {self.resource_name}: {item.get('id', 'N/A')}")
        return success, item

    def update(self, key: str, value: Any, updated_fields: Dict[str, Any]) -> bool:
        """Updates an existing record matching key=value with new fields."""
        records = self.load()
        updated = False
        for i, item in enumerate(records):
            if item.get(key) == value:
                records[i].update(updated_fields)
                updated = True
                break
        if updated:
            success = self.save(records)
            if success:
                logger.info(f"Updated record in {self.resource_name} where {key}={value}")
            return success
        return False

    def delete(self, key: str, value: Any) -> bool:
        """Deletes a record matching key=value."""
        records = self.load()
        filtered = [item for item in records if item.get(key) != value]
        if len(filtered) < len(records):
            success = self.save(filtered)
            if success:
                logger.info(f"Deleted record in {self.resource_name} where {key}={value}")
            return success
        return False

Tuple_Item = tuple[bool, Dict[str, Any]]
