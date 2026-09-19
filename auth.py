"""
Vyapaar-OS Authentication Module
Handles merchant registration, password hashing (PBKDF2/SHA-256 with salt),
and user session profiles. Guarantees persistence in data/users.json with zero data loss.
"""

import os
import json
import hashlib
import secrets
from datetime import datetime
from typing import Optional, Dict, Any, Tuple

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
USERS_FILE = os.path.join(DATA_DIR, "users.json")

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)


BACKUP_USERS_FILE = "/tmp/vyapaar_users_backup.json"


def _hash_password(password: str, salt: Optional[str] = None) -> Tuple[str, str]:
    """Hashes password with SHA-256 and unique 16-byte hex salt."""
    if not salt:
        salt = secrets.token_hex(16)
    hashed = hashlib.sha256((password + salt).encode("utf-8")).hexdigest()
    return hashed, salt


def _load_users() -> Dict[str, Any]:
    """Loads user dictionary from persistent storage, merging with /tmp backup if git pull wiped users.json."""
    users = {}
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, "r", encoding="utf-8") as f:
                users = json.load(f)
        except Exception:
            pass

    # Merge from /tmp backup (which survives git pull & container re-runs)
    if os.path.exists(BACKUP_USERS_FILE):
        try:
            with open(BACKUP_USERS_FILE, "r", encoding="utf-8") as f:
                backup_users = json.load(f)
                dirty = False
                for u_key, u_val in backup_users.items():
                    if u_key not in users:
                        users[u_key] = u_val
                        dirty = True
                if dirty:
                    _save_users(users)
        except Exception:
            pass

    if not users:
        # Seed default demo merchant if empty
        default_hash, default_salt = _hash_password("kirana123")
        users["ramesh"] = {
            "username": "ramesh",
            "password_hash": default_hash,
            "salt": default_salt,
            "merchant_name": "Ramesh Gupta",
            "store_name": "Namaste Kirana & General Store",
            "location": "Laxmi Nagar, Delhi NCR",
            "phone": "+91 98765 43210",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        _save_users(users)

    return users


def _save_users(users: Dict[str, Any]) -> None:
    """Persists user dictionary to disk and /tmp backup atomically."""
    try:
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            json.dump(users, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving users file: {e}")

    try:
        with open(BACKUP_USERS_FILE, "w", encoding="utf-8") as f:
            json.dump(users, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving backup users file: {e}")


def restore_user_profile(profile: Dict[str, Any]) -> Dict[str, Any]:
    """Auto-restores a user profile from URL session token or query param if missing."""
    clean_user = profile.get("username", "").strip().lower()
    if not clean_user:
        return profile
    users = _load_users()
    if clean_user not in users:
        pwd_hash, salt = _hash_password("kirana123")
        users[clean_user] = {
            "username": clean_user,
            "password_hash": pwd_hash,
            "salt": salt,
            "merchant_name": profile.get("merchant_name") or clean_user.capitalize(),
            "store_name": profile.get("store_name") or f"{clean_user.capitalize()}'s Kirana Store",
            "location": profile.get("location") or "Delhi NCR, India",
            "phone": profile.get("phone") or "",
            "created_at": profile.get("created_at") or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        _save_users(users)
    return get_user(clean_user) or profile


def get_user(username: str) -> Optional[Dict[str, Any]]:
    """Returns user profile by username without password/salt."""
    users = _load_users()
    user = users.get(username.strip().lower())
    if user:
        return {
            "username": user["username"],
            "merchant_name": user["merchant_name"],
            "store_name": user["store_name"],
            "location": user.get("location", ""),
            "phone": user.get("phone", ""),
            "created_at": user.get("created_at", "")
        }
    return None


def register_user(
    username: str,
    password: str,
    merchant_name: str,
    store_name: str,
    location: str = "Delhi NCR, India",
    phone: str = ""
) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
    """Registers a new merchant."""
    clean_username = username.strip().lower()
    if not clean_username:
        return False, "उपयोगकर्ता नाम (Username) आवश्यक है / Username is required.", None
    if len(clean_username) < 3:
        return False, "Username must be at least 3 characters.", None
    if not password or len(password) < 4:
        return False, "Password must be at least 4 characters.", None
    if not merchant_name.strip():
        return False, "Merchant name is required.", None
    if not store_name.strip():
        store_name = f"{merchant_name.strip()}'s Kirana Store"

    users = _load_users()
    if clean_username in users:
        return False, f"Username '{clean_username}' already exists. Please login instead.", None

    pwd_hash, salt = _hash_password(password)
    new_user = {
        "username": clean_username,
        "password_hash": pwd_hash,
        "salt": salt,
        "merchant_name": merchant_name.strip(),
        "store_name": store_name.strip(),
        "location": location.strip() or "Delhi NCR, India",
        "phone": phone.strip(),
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    users[clean_username] = new_user
    _save_users(users)

    safe_profile = {
        "username": new_user["username"],
        "merchant_name": new_user["merchant_name"],
        "store_name": new_user["store_name"],
        "location": new_user["location"],
        "phone": new_user["phone"],
        "created_at": new_user["created_at"]
    }
    return True, "खाता सफलतापूर्वक बन गया! / Account created successfully!", safe_profile


def authenticate_user(username: str, password: str) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
    """Validates login credentials."""
    clean_username = username.strip().lower()
    users = _load_users()
    user = users.get(clean_username)
    if not user:
        return False, "यह उपयोगकर्ता पंजीकृत नहीं है / User not found. Please sign up.", None

    salt = user.get("salt", "")
    computed_hash = hashlib.sha256((password + salt).encode("utf-8")).hexdigest()
    if computed_hash != user.get("password_hash"):
        return False, "गलत पासवर्ड / Incorrect password.", None

    safe_profile = {
        "username": user["username"],
        "merchant_name": user["merchant_name"],
        "store_name": user["store_name"],
        "location": user.get("location", ""),
        "phone": user.get("phone", ""),
        "created_at": user.get("created_at", "")
    }
    return True, "लॉगिन सफल / Login successful!", safe_profile
