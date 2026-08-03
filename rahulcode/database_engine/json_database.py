"""
SmartCampus AI - Reusable JSON Database Engine
Handles file I/O, automatic directory and file creation, backups, and initial sample data seeding.
"""
import os
import json
import shutil
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any
from core.config import Config
from core.security import SecurityManager
from utils.logger import logger

class JSONDatabaseManager:
    """Core JSON File Database Manager"""
    
    def __init__(self, db_dir: Path = Config.DATABASE_DIR):
        self.db_dir = Path(db_dir)
        self._ensure_database_dir()
        self._initialize_default_files()

    def _ensure_database_dir(self):
        """Creates the database directory if missing."""
        if not self.db_dir.exists():
            self.db_dir.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created database directory at {self.db_dir}")

    def get_file_path(self, filename: str) -> Path:
        """Returns the full Path object for a given JSON filename."""
        if not filename.endswith(".json"):
            filename = f"{filename}.json"
        return self.db_dir / filename

    def read_file(self, filename: str) -> List[Dict[str, Any]]:
        """Reads and parses JSON content from file safely."""
        filepath = self.get_file_path(filename)
        if not filepath.exists():
            return []
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
        except Exception as e:
            logger.error(f"Error reading JSON file {filepath}: {str(e)}")
            return []

    def write_file(self, filename: str, data: List[Dict[str, Any]]) -> bool:
        """Writes data to JSON file atomically with indentation."""
        filepath = self.get_file_path(filename)
        try:
            temp_path = filepath.with_suffix(".tmp")
            with open(temp_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            os.replace(temp_path, filepath)
            return True
        except Exception as e:
            logger.error(f"Error writing to JSON file {filepath}: {str(e)}")
            return False

    def create_backup(self, filename: str) -> bool:
        """Creates a timestamped backup copy of a JSON database file."""
        filepath = self.get_file_path(filename)
        if not filepath.exists():
            return False
        try:
            backup_dir = self.db_dir / "backups"
            backup_dir.mkdir(exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = backup_dir / f"{filepath.stem}_{timestamp}.json"
            shutil.copy2(filepath, backup_file)
            logger.info(f"Backup created: {backup_file}")
            return True
        except Exception as e:
            logger.error(f"Backup failed for {filename}: {str(e)}")
            return False

    def _initialize_default_files(self):
        """Creates missing JSON files and seeds rich default data."""
        default_seeds = {
            "users.json": self._get_default_users(),
            "notices.json": self._get_default_notices(),
            "placements.json": self._get_default_placements(),
            "workshops.json": self._get_default_workshops(),
            "settings.json": self._get_default_settings(),
            "logs.json": self._get_default_logs()
        }

        for filename, seed_data in default_seeds.items():
            filepath = self.get_file_path(filename)
            if not filepath.exists():
                logger.info(f"Seeding missing JSON database file: {filename}")
                self.write_file(filename, seed_data)

    def _get_default_users(self) -> List[Dict[str, Any]]:
        """Default seed user credentials."""
        hashed_pass = SecurityManager.hash_password("password123")
        return [
            {
                "id": "usr_001",
                "full_name": "Alex Johnson",
                "student_id": "STU2026001",
                "department": "Computer Science & Engineering",
                "year": "Final Year (BE)",
                "email": "alex.johnson@smartcampus.edu",
                "mobile": "+19876543210",
                "username": "alexj",
                "password": hashed_pass,
                "created_at": datetime.now().isoformat()
            },
            {
                "id": "usr_002",
                "full_name": "Sarah Miller",
                "student_id": "STU2026002",
                "department": "Data Science & AI",
                "year": "Third Year (TE)",
                "email": "sarah.m@smartcampus.edu",
                "mobile": "+19876543211",
                "username": "sarahm",
                "password": hashed_pass,
                "created_at": datetime.now().isoformat()
            }
        ]

    def _get_default_notices(self) -> List[Dict[str, Any]]:
        """Default notices seed data."""
        return [
            {
                "id": "not_001",
                "title": "Annual Hackathon 2026 Registration Open",
                "description": "SmartCampus Hackathon 2026 kicks off next week! Form teams of up to 4 students and showcase innovative solutions in AI, IoT, and Web Dev. Cash prizes worth $5,000.",
                "department": "Computer Science & Engineering",
                "date": "2026-08-01",
                "priority": "High",
                "publisher": "Dean of Academics"
            },
            {
                "id": "not_002",
                "title": "Mid-Semester Examination Schedule Released",
                "description": "The official timetable for Mid-Semester Exams is now uploaded on the student portal. Exams commence on August 20th.",
                "department": "All Departments",
                "date": "2026-08-02",
                "priority": "High",
                "publisher": "Examination Cell"
            },
            {
                "id": "not_003",
                "title": "Campus Placement Drive by TechCorp",
                "description": "TechCorp is visiting for Campus Recruitment for Software Engineers and Data Analysts. Eligible streams: CSE, IT, Data Science.",
                "department": "Information Technology",
                "date": "2026-08-03",
                "priority": "Medium",
                "publisher": "Training & Placement Cell"
            }
        ]

    def _get_default_placements(self) -> List[Dict[str, Any]]:
        """Default placements seed data."""
        return [
            {
                "id": "plc_001",
                "company": "Google Cloud",
                "package": "$120,000 / year",
                "location": "Mountain View, CA / Remote",
                "eligibility": "GPA >= 3.5, CSE / IT / Data Science",
                "skills_required": "Python, Go, Distributed Systems, Cloud Architecture",
                "deadline": "2026-08-25",
                "apply_link": "https://careers.google.com",
                "status": "Open"
            },
            {
                "id": "plc_002",
                "company": "Microsoft AI Solutions",
                "package": "$115,000 / year",
                "location": "Redmond, WA",
                "eligibility": "Final Year Students, CSE / AI",
                "skills_required": "PyTorch, Machine Learning, OpenAI APIs, Azure",
                "deadline": "2026-08-30",
                "apply_link": "https://careers.microsoft.com",
                "status": "Open"
            },
            {
                "id": "plc_003",
                "company": "Tesla Robotics",
                "package": "$110,000 / year",
                "location": "Austin, TX",
                "eligibility": "BE Mechanical, Electrical, Electronics",
                "skills_required": "C++, Robotics, Control Systems, Computer Vision",
                "deadline": "2026-09-05",
                "apply_link": "https://www.tesla.com/careers",
                "status": "Upcoming"
            }
        ]

    def _get_default_workshops(self) -> List[Dict[str, Any]]:
        """Default workshops seed data."""
        return [
            {
                "id": "wsp_001",
                "workshop_name": "Generative AI & LLM Fine-Tuning",
                "trainer": "Dr. Aris Thorne (AI Specialist)",
                "venue": "Auditorium A & Online Live",
                "department": "Data Science & AI",
                "date": "2026-08-15",
                "seats": 60,
                "description": "Hands-on masterclass building custom AI agents using LangChain, OpenAI API, and Streamlit.",
                "registration_link": "https://smartcampus.edu/workshops/genai"
            },
            {
                "id": "wsp_002",
                "workshop_name": "Modern Cloud DevOps with Kubernetes & Terraform",
                "trainer": "Elena Rostova (DevOps Architect)",
                "venue": "Computer Lab 4",
                "department": "Computer Science & Engineering",
                "date": "2026-08-18",
                "seats": 45,
                "description": "Learn container orchestration, CI/CD pipelines, and cloud automation best practices.",
                "registration_link": "https://smartcampus.edu/workshops/devops"
            }
        ]

    def _get_default_settings(self) -> List[Dict[str, Any]]:
        """Default settings seed data."""
        return [
            {
                "id": "setting_global",
                "theme_mode": "Dark",
                "notifications_enabled": True,
                "language": "English",
                "auto_summarize_notices": True
            }
        ]

    def _get_default_logs(self) -> List[Dict[str, Any]]:
        """Default logs seed data."""
        return [
            {
                "id": "log_001",
                "timestamp": datetime.now().isoformat(),
                "user": "system",
                "action": "SYSTEM_STARTUP",
                "details": "SmartCampus AI JSON database initialized successfully."
            }
        ]
