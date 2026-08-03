"""
SmartCampus AI - Input Validation Utilities
Validates emails, mobile numbers, passwords, student IDs, and string inputs.
"""
import re
from typing import Tuple

class InputValidator:
    EMAIL_REGEX = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    MOBILE_REGEX = r'^\+?[0-9]{10,14}$'

    @classmethod
    def validate_email(cls, email: str) -> bool:
        """Validates email format."""
        if not email or not isinstance(email, str):
            return False
        return bool(re.match(cls.EMAIL_REGEX, email.strip()))

    @classmethod
    def validate_mobile(cls, mobile: str) -> bool:
        """Validates mobile number format."""
        if not mobile or not isinstance(mobile, str):
            return False
        return bool(re.match(cls.MOBILE_REGEX, mobile.strip()))

    @classmethod
    def validate_password(cls, password: str, confirm_password: str, min_length: int = 6) -> Tuple[bool, str]:
        """Validates password criteria and match."""
        if not password:
            return False, "Password cannot be empty."
        if len(password) < min_length:
            return False, f"Password must be at least {min_length} characters long."
        if password != confirm_password:
            return False, "Passwords do not match."
        return True, "Valid password."

    @classmethod
    def validate_registration(
        cls,
        full_name: str,
        student_id: str,
        email: str,
        mobile: str,
        username: str,
        password: str,
        confirm_password: str
    ) -> Tuple[bool, str]:
        """Performs full registration validation suite."""
        if not full_name.strip():
            return False, "Full Name is required."
        if not student_id.strip():
            return False, "Student ID is required."
        if not username.strip():
            return False, "Username is required."
        if len(username.strip()) < 3:
            return False, "Username must be at least 3 characters long."
        if not cls.validate_email(email):
            return False, "Invalid email address format."
        if not cls.validate_mobile(mobile):
            return False, "Invalid mobile number format (must be 10-14 digits)."
        
        valid_pass, msg = cls.validate_password(password, confirm_password)
        if not valid_pass:
            return False, msg

        return True, "Validation successful."
