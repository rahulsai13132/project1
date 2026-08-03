"""
SmartCampus AI - Security Module
Handles password hashing and verification using bcrypt.
"""
import bcrypt

class SecurityManager:
    @staticmethod
    def hash_password(password: str) -> str:
        """Hashes a plain text password using bcrypt."""
        if not password:
            raise ValueError("Password cannot be empty")
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        """Verifies a plain text password against a stored bcrypt hash."""
        if not password or not hashed_password:
            return False
        try:
            return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
        except Exception:
            return False
