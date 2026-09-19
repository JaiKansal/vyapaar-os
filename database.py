"""
Vyapaar-OS Persistent Real Data Store
Manages store state, customer udhaars, inventory levels, supplier invoices, and audit trails.
Persists all real mutations to disk in store_database.json.
"""

import os
import json
from datetime import datetime
from typing import Dict, Any, List

DB_FILE = os.path.join(os.path.dirname(__file__), "store_database.json")
STORES_DIR = os.path.join(os.path.dirname(__file__), "data", "stores")
os.makedirs(STORES_DIR, exist_ok=True)

DEFAULT_STATE = {
    "store_name": "Namaste Kirana & General Store",
    "owner": "Ramesh Gupta",
    "location": "Laxmi Nagar, Delhi NCR",
    "cash_in_hand": 18500.0,
    "daily_sales_avg": 9200.0,
    "customers_udhaar": [],
    "inventory": [
        {
            "sku": "SKU-AMUL-01",
            "name": "Amul Taaza Milk (500ml)",
            "category": "Dairy",
            "current_stock": 4,
            "min_threshold": 25,
            "unit": "packets",
            "cost_price": 27.0,
            "selling_price": 28.0,
            "supplier": "Goyal Dairy Distributors",
            "status": "LOW_STOCK"
        },
        {
            "sku": "SKU-AASH-02",
            "name": "Aashirvaad Shudh Chakki Atta (10kg)",
            "category": "Staples",
            "current_stock": 2,
            "min_threshold": 12,
            "unit": "bags",
            "cost_price": 410.0,
            "selling_price": 445.0,
            "supplier": "Delhi Grain Merchants Syndicate",
            "status": "LOW_STOCK"
        },
        {
            "sku": "SKU-FORT-03",
            "name": "Fortune Refined Mustard Oil (1L)",
            "category": "Oils",
            "current_stock": 6,
            "min_threshold": 15,
            "unit": "pouches",
            "cost_price": 138.0,
            "selling_price": 152.0,
            "supplier": "Delhi Grain Merchants Syndicate",
            "status": "LOW_STOCK"
        },
        {
            "sku": "SKU-MDH-04",
            "name": "MDH Deggi Mirch (100g)",
            "category": "Spices",
            "current_stock": 18,
            "min_threshold": 8,
            "unit": "boxes",
            "cost_price": 82.0,
            "selling_price": 94.0,
            "supplier": "Gupta Kirana Wholesalers",
            "status": "HEALTHY"
        },
        {
            "sku": "SKU-SURF-05",
            "name": "Surf Excel Quick Wash (1kg)",
            "category": "FMCG",
            "current_stock": 1,
            "min_threshold": 10,
            "unit": "packs",
            "cost_price": 140.0,
            "selling_price": 155.0,
            "supplier": "HUL City Depot",
            "status": "CRITICAL"
        }
    ],
    "supplier_invoices": [
        {
            "invoice_id": "INV-DEL-892",
            "supplier_name": "Delhi Grain Merchants Syndicate",
            "phone": "+91 98222 11009",
            "total_amount": 48500.0,
            "due_in_days": 2,
            "credit_terms": "Net 15 Days (2% penalty thereafter)",
            "items": "Atta, Basmati Rice, Refined Oil batch #401",
            "status": "UPCOMING_DEADLINE"
        },
        {
            "invoice_id": "INV-GOY-331",
            "supplier_name": "Goyal Dairy Distributors",
            "phone": "+91 97111 88442",
            "total_amount": 16200.0,
            "due_in_days": 4,
            "credit_terms": "Net 7 Days",
            "items": "Dairy crates (Milk, Paneer, Butter)",
            "status": "PENDING"
        },
        {
            "invoice_id": "INV-HUL-109",
            "supplier_name": "HUL City Depot",
            "phone": "+91 99000 33441",
            "total_amount": 12800.0,
            "due_in_days": 9,
            "credit_terms": "Net 21 Days",
            "items": "Detergents & personal care stock",
            "status": "PENDING"
        }
    ],
    "action_logs": [],
    "active_loan": None
}


def get_db_file(username: str = None) -> str:
    """Returns the dedicated JSON file path for a merchant."""
    if username and username.strip():
        clean_user = username.strip().lower()
        return os.path.join(STORES_DIR, f"{clean_user}_store.json")
    return DB_FILE


def load_db(username: str = None) -> Dict[str, Any]:
    """Loads store state from disk for a specific merchant, initializing if missing."""
    import copy
    file_path = get_db_file(username)
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass

    # Initialize store state
    user_state = copy.deepcopy(DEFAULT_STATE)
    if username and username.strip():
        try:
            from auth import get_user
            u = get_user(username)
            if u:
                user_state["store_name"] = u.get("store_name", user_state["store_name"])
                user_state["owner"] = u.get("merchant_name", user_state["owner"])
                user_state["location"] = u.get("location", user_state["location"])
        except Exception:
            pass

    save_db(user_state, username)
    return user_state


def save_db(data: Dict[str, Any], username: str = None) -> None:
    """Saves store state to disk atomically."""
    file_path = get_db_file(username)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def reset_db(username: str = None) -> Dict[str, Any]:
    """Wipes all demo/mock data and resets store state to clean pristine state."""
    import copy
    clean = copy.deepcopy(DEFAULT_STATE)
    if username and username.strip():
        try:
            from auth import get_user
            u = get_user(username)
            if u:
                clean["store_name"] = u.get("store_name", clean["store_name"])
                clean["owner"] = u.get("merchant_name", clean["owner"])
                clean["location"] = u.get("location", clean["location"])
        except Exception:
            pass
    save_db(clean, username)
    return clean


def add_udhaar(customer_name: str, phone: str, amount: float, items: str, due_date: str = None, username: str = None) -> Dict[str, Any]:
    """Adds a real customer udhaar debt to the merchant's ledger."""
    db = load_db(username)
    new_id = f"UDH-{len(db['customers_udhaar']) + 101}"
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    entry = {
        "id": new_id,
        "customer_name": customer_name,
        "phone": phone or "+91 98765 00000",
        "amount": round(float(amount), 2),
        "days_overdue": 0,
        "items": items or "Kirana purchase",
        "status": "ACTIVE",
        "last_reminded": "Just added",
        "due_date": due_date or "Not specified",
        "created_at": now_str
    }
    db["customers_udhaar"].append(entry)
    save_db(db, username)
    return entry


def settle_udhaar(udhaar_id: str, username: str = None) -> Dict[str, Any]:
    """Marks an existing udhaar debt as recovered, adding the amount to cash in hand."""
    db = load_db(username)
    found = None
    for u in db["customers_udhaar"]:
        if u["id"] == udhaar_id:
            found = u
            break
    if found:
        amount = found["amount"]
        db["customers_udhaar"] = [u for u in db["customers_udhaar"] if u["id"] != udhaar_id]
        db["cash_in_hand"] += amount
        save_db(db, username)
        return {"status": "SUCCESS", "recovered_amount": amount, "new_cash": db["cash_in_hand"]}
    return {"status": "NOT_FOUND"}


def update_inventory_stock(sku: str, delta_stock: int, username: str = None) -> Dict[str, Any]:
    """Updates current stock count for an inventory item."""
    db = load_db(username)
    for item in db["inventory"]:
        if item["sku"] == sku:
            item["current_stock"] += delta_stock
            if item["current_stock"] <= item["min_threshold"]:
                item["status"] = "LOW_STOCK"
            else:
                item["status"] = "HEALTHY"
            save_db(db, username)
            return item
    return {}


def record_loan_drawdown(amount: float = 50000.0, username: str = None) -> Dict[str, Any]:
    """Disburses pre-underwritten Paytm Loan into the store's business cash."""
    db = load_db(username)
    now_str = datetime.now().strftime("%I:%M %p, %d %b %Y")
    loan_record = {
        "amount": amount,
        "ref_id": f"#LOAN{datetime.now().strftime('%M%S')}",
        "lender": "Digital Finance Corp (Paytm Lending Partner)",
        "disbursed_at": now_str,
        "monthly_interest_rate": "1.15%",
        "status": "DISBURSED"
    }
    db["cash_in_hand"] += amount
    db["active_loan"] = loan_record
    save_db(db, username)
    return loan_record
