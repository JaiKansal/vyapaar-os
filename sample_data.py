"""
Sample data for Vyapaar-OS: The Autonomous Merchant Partner
Kirana Store: "Namaste Kirana & General Store" (Delhi NCR)
Contains initial state for temporal memory, Indic voice prompts, sample kacha bills, and distributor credit terms.
"""

INITIAL_STORE_STATE = {
    "store_name": "Namaste Kirana Store",
    "owner": "Ramesh Gupta",
    "location": "Laxmi Nagar, Delhi",
    "cash_in_hand": 18500.0,
    "daily_sales_avg": 9200.0,
    "customers_udhaar": [
        {
            "id": "UDH-101",
            "customer_name": "Suresh Sharma",
            "phone": "+91 98765 43210",
            "amount": 2450.0,
            "days_overdue": 14,
            "items": "2x Basmati Rice 5kg, Cooking Oil 2L, Spices",
            "status": "OVERDUE",
            "last_reminded": "3 days ago"
        },
        {
            "id": "UDH-102",
            "customer_name": "Pooja Verma",
            "phone": "+91 98111 22334",
            "amount": 1120.0,
            "days_overdue": 6,
            "items": "Atta 10kg, Tea Leaves 500g, Sugar 2kg",
            "status": "PENDING",
            "last_reminded": "Never"
        },
        {
            "id": "UDH-103",
            "customer_name": "Anil Kumar (Dhaba)",
            "phone": "+91 99223 88441",
            "amount": 4800.0,
            "days_overdue": 21,
            "items": "Commercial Dal 20kg, Rice 30kg, Mustard Oil",
            "status": "CRITICAL",
            "last_reminded": "7 days ago"
        }
    ],
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
    ]
}

SAMPLE_INDIC_VOICE_PRESETS = [
    {
        "id": "preset_udhaar_hindi",
        "title": "📝 Record Udhaar (Hindi)",
        "dialect": "Hindi (Delhi / UP)",
        "transcript": "अरे भैया, शर्मा जी को 850 रुपये का राशन उधार लिख लो, बोले हैं इतवार को दे जाएंगे।",
        "english_meaning": "Record ₹850 grocery udhaar for Sharma ji, he promised to pay by Sunday.",
        "intent": "RECORD_UDHAAR",
        "extracted_entities": {
            "customer": "Suresh Sharma",
            "amount": 850.0,
            "due_date": "Sunday",
            "category": "Groceries"
        },
        "audio_response_text": "ठीक है, शर्मा जी का ₹850 का उधार खाता में दर्ज कर दिया गया है।",
        "action": "UDHAAR_RECORDED"
    },
    {
        "id": "preset_restock_hinglish",
        "title": "📦 Low Stock Restock (Hinglish)",
        "dialect": "Hinglish",
        "transcript": "अमूल दूध और 10 पैकेट सर्फ एक्सेल खत्म हो गया है, तुरंत डिस्ट्रीब्यूटर को ऑर्डर डाल दो।",
        "english_meaning": "Amul milk and 10 packs of Surf Excel are out of stock, immediately place order to distributor.",
        "intent": "RESTOCK_SUPPLIER",
        "extracted_entities": {
            "items": [
                {"name": "Amul Milk", "qty": 20, "unit": "packets"},
                {"name": "Surf Excel", "qty": 10, "unit": "packs"}
            ],
            "urgency": "IMMEDIATE"
        },
        "audio_response_text": "अमूल दूध और सर्फ एक्सेल का रीस्टॉक ऑर्डर n8n के जरिए गोयल डिस्ट्रीब्यूटर्स को भेज दिया गया है।",
        "action": "RESTOCK_TRIGGERED"
    },
    {
        "id": "preset_udhaar_remind_hindi",
        "title": "🔔 Trigger WhatsApp Debt Recovery (Hindi)",
        "dialect": "Hindi",
        "transcript": "अनिल ढाबे वाले का बहुत दिन से 4800 का उधार अटका है, उसको प्यार से एक वॉइस मेमो भेज दो।",
        "english_meaning": "Anil Dhaba has 4,800 udhaar pending for days, send him a polite voice reminder on WhatsApp.",
        "intent": "RECOVER_UDHAAR",
        "extracted_entities": {
            "customer": "Anil Kumar (Dhaba)",
            "amount": 4800.0,
            "channel": "WhatsApp Audio"
        },
        "audio_response_text": "अनिल जी को 4800 रुपये के उधार का विनम्र व्हाट्सएप ऑडियो नोट भेज दिया गया है।",
        "action": "WHATSAPP_AUDIO_SENT"
    },
    {
        "id": "preset_supplier_due_tamil",
        "title": "💰 Supplier Credit Query (Tamil/Indic)",
        "dialect": "Tamil / Indic",
        "transcript": "इस हफ्ते सप्लायर को कुल कितना भुगतान करना है और क्या गल्ले में पैसे पूरे हैं?",
        "english_meaning": "How much total do we need to pay suppliers this week, and do we have enough cash in the drawer?",
        "intent": "CHECK_CASHFLOW",
        "extracted_entities": {
            "query_type": "SUPPLIER_PAYMENTS_AND_CASHFLOW"
        },
        "audio_response_text": "अगले 48 घंटों में दिल्ली ग्रेन मर्चेंट को 48,500 रुपये देने हैं, पर गल्ले में केवल 18,500 रुपये हैं। 43,000 रुपये का घाटा अनुमानित है। पेटीएम 50,000 रुपये का इंस्टेंट लोन उपलब्ध है।",
        "action": "CASHFLOW_DEFICIT_PREDICTED"
    }
]

SAMPLE_KACHA_BILLS = [
    {
        "id": "bill_01",
        "title": "हस्तलिखित कच्चा पर्चा (Kirana Daily Slip)",
        "description": "Handwritten kirana paper slip with customer credit entries and distributor arrival.",
        "raw_text": """श्री गणेशाय नमः
दिनांक: 14-Sep-2026
कच्चा खाता:
1. सुरेश शर्मा - 2 पैकेट फॉर्च्यून तेल + 5kg बासमती = ₹850 (उधार)
2. पूजा वर्मा - 10kg आटा + 2kg चीनी = ₹620 (उधार)
3. गोयल डेयरी सप्लाई आगमन - 40 पैकेट अमूल दूध = ₹1,080 (नकद दिया ₹300, बाकी ₹780)
4. ढाबा अनिल - किराना सामान = ₹1,200 (उधार दर्ज)
कुल नया उधार: ₹2,670""",
        "parsed_data": {
            "new_udhaars": [
                {"customer": "Suresh Sharma", "amount": 850.0, "items": "2x Fortune Oil + 5kg Basmati"},
                {"customer": "Pooja Verma", "amount": 620.0, "items": "10kg Atta + 2kg Sugar"},
                {"customer": "Anil Kumar (Dhaba)", "amount": 1200.0, "items": "Kirana goods"}
            ],
            "supplier_deliveries": [
                {"supplier": "Goyal Dairy Distributors", "item": "Amul Milk 40 pkts", "payable": 780.0}
            ]
        }
    },
    {
        "id": "bill_02",
        "title": "सप्लायर बीजक (Delhi Grain Syndicate Slip)",
        "description": "Distributor invoice slip specifying strict credit terms and due date.",
        "raw_text": """DELHI GRAIN MERCHANTS SYNDICATE
Naya Bazar, Khari Baoli, Delhi
INVOICE NO: DG-2026-904   Date: 01-Sep-2026
To: Namaste Kirana Store (Prop. Ramesh Gupta)

Items:
- Aashirvaad Atta (50 bags @ 410) = ₹20,500
- Basmati Rice (15 bags @ 1200) = ₹18,000
- Fortune Mustard (5 cartons) = ₹10,000
-----------------------------------------
TOTAL AMOUNT: ₹48,500
CREDIT TERMS: Strictly 15 days. Due Date: 16-Sep-2026.
Late penalty: 24% p.a.""",
        "parsed_data": {
            "supplier": "Delhi Grain Merchants Syndicate",
            "invoice_no": "DG-2026-904",
            "amount_due": 48500.0,
            "due_date": "16-Sep-2026",
            "days_left": 2,
            "penalty_risk": "24% p.a. late penalty"
        }
    }
]
