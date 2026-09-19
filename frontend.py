import streamlit as st
import streamlit.components.v1 as components
import requests
import base64
import json
import time
import pandas as pd
import os
# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Vyapaar-OS | The Autonomous Kirana Partner",
    page_icon="🏪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Auto-detect active backend port (8000 or 8001)
def _find_backend_url():
    for p in [8000, 8001, 8080]:
        try:
            r = requests.get(f"http://127.0.0.1:{p}/", timeout=0.25)
            if r.status_code == 200:
                return f"http://127.0.0.1:{p}"
        except Exception:
            pass
    return "http://127.0.0.1:8000"

BACKEND_URL = _find_backend_url()
PUBLIC_HOST_URL = "https://vyapaar-os.streamlit.app"

# --- CUSTOM CSS FOR HIGH-END FINTECH & KIRANA AESTHETICS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Outfit:wght@400;600;700;800&family=Noto+Sans+Devanagari:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', 'Noto Sans Devanagari', sans-serif;
    }
    
    /* Eliminate excessive top padding and blank space */
    .block-container,
    .main .block-container,
    div[data-testid="stAppViewBlockContainer"],
    div[data-testid="block-container"] {
        padding-top: 0.6rem !important;
        padding-bottom: 2rem !important;
    }
    header[data-testid="stHeader"] {
        display: none !important;
        height: 0 !important;
    }
    
    /* Completely hide Streamlit Cloud footer, "Hosted with Streamlit" badge, and header */
    #MainMenu {visibility: hidden !important; display: none !important;}
    footer {visibility: hidden !important; display: none !important;}
    header {visibility: hidden !important; display: none !important;}
    [data-testid="stToolbar"] {visibility: hidden !important; display: none !important;}
    [data-testid="stDecoration"] {visibility: hidden !important; display: none !important;}
    [data-testid="stStatusWidget"] {visibility: hidden !important; display: none !important;}
    .stDeployButton {display: none !important;}
    div[class*="viewerBadge_"] {display: none !important; visibility: hidden !important;}
    a[class*="viewerBadge_"] {display: none !important; visibility: hidden !important;}
    span[class*="viewerBadge_"] {display: none !important; visibility: hidden !important;}
    div[data-testid="stBottomBlockContainer"] {display: none !important;}
    .reportview-container .main footer {visibility: hidden !important;}
    iframe[title="streamlit_viewer_badge"] {display: none !important;}
    
    .kirana-title-container {
        background: linear-gradient(135deg, #002e6e 0%, #0084c7 60%, #00b9f1 100%);
        padding: 20px 24px;
        border-radius: 16px;
        color: white;
        margin-bottom: 16px;
        box-shadow: 0 10px 25px rgba(0, 46, 110, 0.22);
    }
    
    .tech-title-container {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 60%, #002e6e 100%);
        padding: 20px 24px;
        border-radius: 16px;
        color: white;
        margin-bottom: 16px;
        box-shadow: 0 10px 25px rgba(15, 23, 42, 0.3);
    }
    
    .hackathon-badge {
        display: inline-block;
        background: rgba(255, 255, 255, 0.18);
        backdrop-filter: blur(10px);
        color: #fff;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        margin-bottom: 8px;
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    .team-badge {
        display: inline-block;
        background: #00BAF2;
        color: #002e6e;
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 0.78rem;
        font-weight: 800;
        margin-left: 8px;
    }
    
    .public-url-badge {
        display: inline-block;
        background: #10b981;
        color: #ffffff;
        padding: 4px 12px;
        border-radius: 14px;
        font-size: 0.78rem;
        font-weight: 800;
        letter-spacing: 0.3px;
        box-shadow: 0 2px 8px rgba(16, 185, 129, 0.4);
    }
    
    .metric-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 16px 18px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.04);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(0,0,0,0.08);
    }
    .metric-value {
        font-size: 1.65rem;
        font-weight: 800;
        line-height: 1.2;
        margin: 4px 0;
        font-family: 'Outfit', sans-serif;
    }
    .metric-label {
        font-size: 0.82rem;
        color: #475569;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .soundbox-container {
        background: linear-gradient(145deg, #1e293b 0%, #0f172a 100%);
        border: 2px solid #38bdf8;
        border-radius: 20px;
        padding: 22px;
        color: white;
        box-shadow: 0 12px 30px rgba(0, 185, 241, 0.2);
        margin-bottom: 20px;
    }
    .soundbox-logo {
        font-family: 'Outfit', sans-serif;
        font-size: 1.5rem;
        font-weight: 900;
        color: #00BAF2;
        letter-spacing: 0.5px;
    }
    .soundbox-logo span {
        color: #ffffff;
        font-weight: 400;
    }
    .soundbox-grille {
        background: radial-gradient(circle, #334155 10%, transparent 11%);
        background-size: 8px 8px;
        height: 48px;
        border-radius: 10px;
        margin: 14px 0;
        border: 1px solid #475569;
    }
    .soundbox-led {
        height: 12px;
        width: 12px;
        background-color: #10b981;
        border-radius: 50%;
        display: inline-block;
        box-shadow: 0 0 10px #10b981;
        animation: pulse 2s infinite;
        vertical-align: middle;
        margin-right: 6px;
    }
    
    .loan-phone-card {
        background: #ffffff;
        border: 2px solid #00b9f1;
        border-radius: 18px;
        padding: 22px;
        box-shadow: 0 10px 25px rgba(0, 185, 241, 0.15);
        text-align: center;
    }
    
    .customer-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 16px 18px;
        margin-bottom: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    }
    
    .guardrail-tag {
        background: #ecfdf5;
        color: #059669;
        font-weight: 700;
        font-size: 0.75rem;
        padding: 3px 8px;
        border-radius: 10px;
        border: 1px solid #86efac;
        display: inline-block;
    }
    
    /* Mobile responsive tweaks */
    @media (max-width: 768px) {
        .metric-value { font-size: 1.3rem; }
        .kirana-title-container, .tech-title-container { padding: 14px 16px; }
    }
</style>
""", unsafe_allow_html=True)


# --- DATA FETCHING ---
def get_live_state():
    try:
        r = requests.get(f"{BACKEND_URL}/api/store-state", timeout=4)
        if r.status_code == 200:
            return r.json()
    except Exception:
        pass
    return None

def get_cashflow_data():
    try:
        r = requests.get(f"{BACKEND_URL}/api/predict-cashflow", timeout=4)
        if r.status_code == 200:
            return r.json()
    except Exception:
        pass
    return None

live_state = get_live_state()
if not live_state:
    st.info("🔄 Connecting to Vyapaar-OS backend on port 8000...")
    live_state = {
        "store_name": "Namaste Kirana & General Store",
        "cash_in_hand": 18500.0,
        "daily_sales_avg": 9200.0,
        "total_udhaar_outstanding": 8370.0,
        "total_supplier_dues": 77500.0,
        "low_stock_items_count": 4,
        "margin_leak_saved": 38640.0,
        "customers_udhaar": [],
        "inventory": [],
        "supplier_invoices": [],
        "action_logs": [],
        "active_loan": None
    }




# Language helper setup
if "app_lang" not in st.session_state:
    st.session_state["app_lang"] = "हिन्दी"

def T(hi_text, en_text):
    return en_text if st.session_state.get("app_lang") == "English" else hi_text

# Top Bar with Language Toggle
col_lang_left, col_lang_right = st.columns([4, 1.2])
with col_lang_right:
    top_lang = st.radio(
        "Language / भाषा:",
        ["🇮🇳 हिन्दी", "🇬🇧 English"],
        index=0 if st.session_state.get("app_lang") == "हिन्दी" else 1,
        horizontal=True,
        key="top_lang_toggle"
    )
    selected_lang = "हिन्दी" if "हिन्दी" in top_lang else "English"
    if selected_lang != st.session_state.get("app_lang"):
        st.session_state["app_lang"] = selected_lang
        st.rerun()

st.markdown(f'''
<div class="kirana-title-container">
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
        <div>
            <div class="hackathon-badge">{T("🏪 डिजिटल किराना मुनीमजी • काउंटर स्टेशन", "🏪 Digital Kirana Munimji • Counter Station")}</div>
            <h1 style="margin: 0; font-size: 2.1rem; font-weight: 800; letter-spacing: -0.5px;">
                {T("नमस्ते किराना एवं जनरल स्टोर", "Namaste Kirana & General Store")}
            </h1>
            <p style="margin: 6px 0 0 0; font-size: 0.96rem; opacity: 0.95;">
                {T("व्यापार-OS • आवाज़ से हिसाब लिखें, उधार वसूलें, और 1-क्लिक में सप्लायर को आर्डर भेजें", "Vyapaar-OS • Voice Ledger, Udhaar Recovery, and 1-Click Supplier Restock")}
                <span class="team-badge">Powered by Paytm Soundbox & Sarvam AI</span>
            </p>
        </div>
        <div style="text-align: right;">
            <div style="margin-bottom: 6px;"><span class="public-url-badge">🟢 {T("साउंडबॉक्स एक्टिव", "Soundbox Active")}</span></div>
            <div style="font-size: 0.8rem; color: #e0f2fe; background: rgba(0,0,0,0.22); padding: 6px 12px; border-radius: 8px;">
                {T("काउंटर माइक • 2-वे वॉयस तैयार", "Counter Mic • 2-Way Voice Ready")}
            </div>
        </div>
    </div>
</div>
''', unsafe_allow_html=True)


# Kirana Shopkeeper KPIs
col_m1, col_m2, col_m3, col_m4, col_m5 = st.columns(5)
with col_m1:
    st.markdown(f'''
    <div class="metric-card">
        <div class="metric-label">{T("💰 गल्ले में कैश", "💰 Cash in Drawer")}</div>
        <div class="metric-value" style="color: #002e6e;">₹{live_state['cash_in_hand']:,.0f}</div>
        <div style="font-size: 0.74rem; color: #16a34a; font-weight: 600;">{T("दैनिक बिक्री", "Daily Sales")}: ₹{live_state['daily_sales_avg']:,.0f}</div>
    </div>
    ''', unsafe_allow_html=True)

with col_m2:
    st.markdown(f'''
    <div class="metric-card">
        <div class="metric-label">{T("📒 बाज़ार का उधार", "📒 Customer Udhaar")}</div>
        <div class="metric-value" style="color: #d97706;">₹{live_state['total_udhaar_outstanding']:,.0f}</div>
        <div style="font-size: 0.74rem; color: #64748b;">{len(live_state['customers_udhaar'])} {T("ग्राहकों से लेना बाकी", "active borrowers")}</div>
    </div>
    ''', unsafe_allow_html=True)

with col_m3:
    st.markdown(f'''
    <div class="metric-card">
        <div class="metric-label">{T("🚚 सप्लायर का बकाया", "🚚 Supplier Dues")}</div>
        <div class="metric-value" style="color: #dc2626;">₹{live_state['total_supplier_dues']:,.0f}</div>
        <div style="font-size: 0.74rem; color: #dc2626; font-weight: 600;">⚠️ {T("2 से 4 दिन में देना है", "Due in 2-4 days")}</div>
    </div>
    ''', unsafe_allow_html=True)

with col_m4:
    st.markdown(f'''
    <div class="metric-card">
        <div class="metric-label">{T("📦 कम सामान (स्टॉक)", "📦 Low Stock SKUs")}</div>
        <div class="metric-value" style="color: #ea580c;">{live_state['low_stock_items_count']} {T("सामान", "Items")}</div>
        <div style="font-size: 0.74rem; color: #ea580c; font-weight: 600;">{T("तुरंत मंगाना आवश्यक", "Restock needed")}</div>
    </div>
    ''', unsafe_allow_html=True)

with col_m5:
    st.markdown(f'''
    <div class="metric-card">
        <div class="metric-label">{T("🛡️ बचाया गया मुनाफा", "🛡️ Margin Protected")}</div>
        <div class="metric-value" style="color: #16a34a;">+14%</div>
        <div style="font-size: 0.74rem; color: #16a34a; font-weight: 600;">₹{live_state['margin_leak_saved']:,.0f}/{T("माह सुरक्षित", "mo saved")}</div>
    </div>
    ''', unsafe_allow_html=True)
st.markdown("<div style='margin-bottom: 12px;'></div>", unsafe_allow_html=True)


with st.sidebar:
    st.markdown('''
    <div style="display: flex; align-items: baseline; gap: 8px; margin-bottom: 14px;">
        <span style="font-family: 'Inter', sans-serif; font-size: 1.9rem; font-weight: 900; color: #002e6e; letter-spacing: -1.2px;">paytm</span>
        <span style="background: #00b9f1; color: #ffffff; font-size: 0.68rem; font-weight: 800; padding: 2px 7px; border-radius: 5px; letter-spacing: 0.8px;">BUSINESS</span>
    </div>
    ''', unsafe_allow_html=True)

    sb_lang = st.radio("🌐 भाषा / Language:", ["🇮🇳 हिन्दी", "🇬🇧 English"], index=0 if st.session_state.get("app_lang") == "हिन्दी" else 1, key="sb_lang_toggle")
    new_lang = "हिन्दी" if "हिन्दी" in sb_lang else "English"
    if new_lang != st.session_state.get("app_lang"):
        st.session_state["app_lang"] = new_lang
        st.rerun()

    st.markdown(f"### {T('🏪 नमस्ते किराना स्टोर', '🏪 Namaste Kirana Store')}")
    st.markdown(f"📍 {T('मुख्य बाज़ार, दिल्ली', 'Main Bazaar, Delhi')}")
    st.markdown(f"📞 {T('साउंडबॉक्स आईडी:', 'Soundbox ID:')} `PTM-SBX-8821`")
    st.markdown("---")
    st.markdown(f"#### 📱 {T('मोबाइल पर खोलें', 'Open on Mobile')}")
    if os.path.exists("vyapaar_live_qr.png"):
        st.image("vyapaar_live_qr.png", caption=T("दुकानदार QR स्कैन करें", "Scan Merchant QR"), width=170)
    st.markdown("---")
    st.markdown(f"#### 🟢 {T('सिस्टम स्थिति', 'System Status')}")
    st.markdown(f"✅ **{T('साउंडबॉक्स', 'Soundbox')}:** {T('ऑनलाइन (2-वे एक्टिव)', 'Online (2-Way Active)')}")
    st.markdown(f"✅ **{T('सरवम एआई', 'Sarvam AI')}:** {T('सक्रिय (Indic Vision & Voice)', 'Active (Indic Vision & Voice)')}")
    st.markdown(f"✅ **{T('खाता बही', 'Ledger')}:** {T('सुरक्षित (Zero Hallucination)', 'Secure (Zero Hallucination)')}")
    st.markdown(f"✅ **{T('Paytm वॉलेट', 'Paytm Wallet')}:** {T('कनेक्टेड', 'Connected')}")

    st.markdown("---")
    st.markdown(f"#### 🔄 {T('डेमो रीसेट', 'Demo Reset')}")
    if st.button(T("🧹 सारा डेमो डेटा रीसेट करें", "🧹 Reset All Demo Data"), use_container_width=True):
        try:
            requests.post(f"{BACKEND_URL}/api/reset-db", timeout=3)
        except Exception:
            pass
        from database import reset_db
        reset_db()
        st.session_state.clear()
        st.success(T("✅ डेटा रीसेट हो गया!", "✅ Data reset successfully!"))
        time.sleep(0.4)
        st.rerun()


tab_voice, tab_khata, tab_loan, tab_stock, tab_parchi = st.tabs([
    T("🎙️ बोलकर हिसाब (Soundbox)", "🎙️ Voice Ingestion (Soundbox)"),
    T("📒 खाता बही (उधार वसूली)", "📒 Udhaar Ledger (Recovery)"),
    T("💰 गल्ला और इमरजेंसी लोन", "💰 Cashflow & Instant Loan"),
    T("📦 दुकान का सामान और आर्डर", "📦 Inventory & Supplier Orders"),
    T("📸 कागज़ की पर्ची स्कैनर", "📸 Paper Slip Scanner")
])

# --------------------------------------------------------------------------
# DUKAAN TAB 1: BOLO AUR LIKHO (SOUNDBOX VOICE)
# --------------------------------------------------------------------------
with tab_voice:
    # Hands-Free Wake Word Banner (Google Assistant / Siri Style - Zero Click)
    st.markdown("""
    <div style="background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); border: 2px solid #00b9f1; border-radius: 14px; padding: 14px 18px; color: #fff; margin-bottom: 16px; box-shadow: 0 4px 14px rgba(0, 185, 241, 0.15);">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
            <div>
                <span style="font-size: 1.05rem; font-weight: 800; color: #38bdf8;">🤖 ऑटोमैटिक वेक-वर्ड साउंडबॉक्स (Always-On Voice Assistant)</span>
                <div style="font-size: 0.88rem; color: #cbd5e1; margin-top: 4px;">
                    Google Assistant या Siri की तरह — बिना कोई बटन दबाए सीधे काउंटर पर बोलें: 
                    <span style="color: #4ade80; font-weight: 700; background: rgba(74,222,128,0.15); padding: 2px 8px; border-radius: 6px;">"हे मुनीमजी"</span> या 
                    <span style="color: #38bdf8; font-weight: 700; background: rgba(56,189,248,0.15); padding: 2px 8px; border-radius: 6px;">"नमस्ते मुनीमजी"</span> या 
                    <span style="color: #facc15; font-weight: 700; background: rgba(250,204,21,0.15); padding: 2px 8px; border-radius: 6px;">"Hey Munimji"</span>
                </div>
            </div>
            <div>
                <span class="guardrail-tag" style="background: #0284c7; color: #ffffff; border-color: #38bdf8;">⚡ Always-On Soundbox Co-Pilot</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Embedded Always-On Continuous Web Speech Listener (No Button Needed)
    wake_listener_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{ font-family: 'Inter', sans-serif; margin: 0; padding: 0; background: transparent; color: #0f172a; }}
            .wake-box {{
                background: #f8fafc;
                border: 1.5px solid #cbd5e1;
                border-radius: 12px;
                padding: 14px 16px;
                margin-bottom: 14px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.04);
            }}
            .wake-status {{
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 10px;
                font-size: 0.92rem;
                font-weight: 600;
                margin-bottom: 8px;
            }}
            .status-left {{
                display: flex;
                align-items: center;
                gap: 10px;
            }}
            .pulse-dot {{
                height: 14px;
                width: 14px;
                border-radius: 50%;
                background-color: #10b981;
                display: inline-block;
                box-shadow: 0 0 10px #10b981;
                animation: pulseGreen 1.6s infinite ease-in-out;
            }}
            .pulse-dot.wake-triggered {{
                background-color: #00b9f1;
                box-shadow: 0 0 14px #00b9f1;
                animation: pulseBlue 0.8s infinite ease-in-out;
            }}
            @keyframes pulseGreen {{
                0% {{ transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }}
                70% {{ transform: scale(1.15); box-shadow: 0 0 0 10px rgba(16, 185, 129, 0); }}
                100% {{ transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }}
            }}
            @keyframes pulseBlue {{
                0% {{ transform: scale(0.95); box-shadow: 0 0 0 0 rgba(0, 185, 241, 0.8); }}
                70% {{ transform: scale(1.25); box-shadow: 0 0 0 12px rgba(0, 185, 241, 0); }}
                100% {{ transform: scale(0.95); box-shadow: 0 0 0 0 rgba(0, 185, 241, 0); }}
            }}
            .badge-live {{
                background: rgba(16, 185, 129, 0.12);
                color: #059669;
                border: 1px solid #10b981;
                padding: 3px 10px;
                border-radius: 20px;
                font-size: 0.75rem;
                font-weight: 700;
                letter-spacing: 0.5px;
            }}
            .transcript-box {{
                background: #ffffff;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                padding: 9px 13px;
                font-size: 0.86rem;
                min-height: 30px;
                margin-top: 6px;
                color: #334155;
                line-height: 1.4;
            }}
        </style>
    </head>
    <body>
        <div class="wake-box">
            <div class="wake-status">
                <div class="status-left">
                    <span id="dot" class="pulse-dot"></span>
                    <span id="status_text">🟢 <strong>साउंडबॉक्स माइक हमेशा चालू है (Always-On Active) • बोलें: 'हे मुनीमजी' या 'नमस्ते मुनीमजी'</strong></span>
                </div>
                <span class="badge-live">LIVE LISTENING</span>
            </div>
            <div class="transcript-box" id="transcript_display">
                🎙️ <em>साउंडबॉक्स काउंटर पर हमेशा सुन रहा है। बिना कोई बटन दबाए सीधे बोलें "हे मुनीमजी" (उदा: "हे मुनीमजी, शर्मा जी का ₹500 उधार लिख लो")...</em>
            </div>
        </div>

        <script>
            // ═══════════════════════════════════════════════════
            //  HYBRID ALWAYS-ON SOUNDBOX LISTENER
            //  Wake Word: Real-time Web Speech (0ms latency, always-on)
            //  STT: Sarvam Saaras v3 (/api/process-voice with clean WAV)
            //  TTS: Sarvam Bulbul v2 (natural Indian shopkeeper voice)
            // ═══════════════════════════════════════════════════
            var isProcessing = false;   // true while API request is in-flight
            var isPlaying    = false;   // true while TTS audio is playing (mic MUTED)
            var wakeDetected = false;   // true once wake word is heard
            var silenceTimer = null;    // timer to detect end of command speech
            var activeCommandText = "";
            var backendUrl = "{BACKEND_URL}";

            // PCM Audio recording via Web Audio API (outputs pure WAV)
            var audioCtx = null;
            var micStream = null;
            var micSource = null;
            var pcmProcessor = null;
            var pcmChunks = [];
            var pcmLength = 0;
            var isRecordingWav = false;

            // Wake-word regex — matches Hindi, Hinglish, English wake phrases
            var WAKE_REGEX = /(हे\\s*मुनीम|नमस्ते\\s*मुनीम|सुनो\\s*मुनीम|मुनीम\\s*जी|मुनीमजी|hey\\s*munim|he\\s*munim|ok\\s*munim|namaste\\s*munim|munimji)/i;

            // ───────────────────────────────────────────────────
            // Web Audio PCM WAV Recorder
            // ───────────────────────────────────────────────────
            function initAudioContext(stream) {{
                try {{
                    micStream = stream;
                    var AudioCtxClass = window.AudioContext || window.webkitAudioContext;
                    if (!AudioCtxClass) return;
                    audioCtx = new AudioCtxClass();
                    micSource = audioCtx.createMediaStreamSource(stream);
                    pcmProcessor = audioCtx.createScriptProcessor(4096, 1, 1);
                    pcmProcessor.onaudioprocess = function(e) {{
                        if (!isRecordingWav) return;
                        var input = e.inputBuffer.getChannelData(0);
                        pcmChunks.push(new Float32Array(input));
                        pcmLength += input.length;
                    }};
                    micSource.connect(pcmProcessor);
                    pcmProcessor.connect(audioCtx.destination);
                }} catch(e) {{
                    console.warn('Web Audio PCM init error:', e);
                }}
            }}

            function startWavRecording() {{
                pcmChunks = [];
                pcmLength = 0;
                isRecordingWav = true;
                if (audioCtx && audioCtx.state === 'suspended') {{
                    audioCtx.resume();
                }}
            }}

            function stopWavRecordingAndGetBlob() {{
                isRecordingWav = false;
                if (pcmLength === 0 || !audioCtx) return null;
                var merged = new Float32Array(pcmLength);
                var offset = 0;
                for (var i = 0; i < pcmChunks.length; i++) {{
                    merged.set(pcmChunks[i], offset);
                    offset += pcmChunks[i].length;
                }}
                pcmChunks = [];
                pcmLength = 0;

                var sRate = audioCtx.sampleRate || 44100;
                var wavBuf = new ArrayBuffer(44 + merged.length * 2);
                var view = new DataView(wavBuf);

                function wStr(pos, str) {{
                    for (var i = 0; i < str.length; i++) {{
                        view.setUint8(pos + i, str.charCodeAt(i));
                    }}
                }}
                wStr(0, 'RIFF');
                view.setUint32(4, 36 + merged.length * 2, true);
                wStr(8, 'WAVE');
                wStr(12, 'fmt ');
                view.setUint32(16, 16, true);
                view.setUint16(20, 1, true); // PCM
                view.setUint16(22, 1, true); // Mono
                view.setUint32(24, sRate, true);
                view.setUint32(28, sRate * 2, true);
                view.setUint16(32, 2, true);
                view.setUint16(34, 16, true);
                wStr(36, 'data');
                view.setUint32(40, merged.length * 2, true);

                var dOff = 44;
                for (var i = 0; i < merged.length; i++, dOff += 2) {{
                    var s = Math.max(-1, Math.min(1, merged[i]));
                    view.setInt16(dOff, s < 0 ? s * 0x8000 : s * 0x7FFF, true);
                }}
                return new Blob([view], {{ type: 'audio/wav' }});
            }}

            // ───────────────────────────────────────────────────
            // Speech Recognition Setup (Wake Word Detection)
            // ───────────────────────────────────────────────────
            var recognition = null;
            var SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;

            function startRecognition() {{
                if (!SpeechRec) {{
                    document.getElementById('status_text').innerHTML =
                        '⚠️ <strong>ब्राउज़र में Web Speech उपलब्ध नहीं है — कृपया Chrome इस्तेमाल करें</strong>';
                    return;
                }}
                if (recognition) {{
                    try {{ recognition.abort(); }} catch(e) {{}}
                }}

                recognition = new SpeechRec();
                recognition.continuous = true;
                recognition.interimResults = true;
                recognition.lang = 'hi-IN';

                recognition.onstart = function() {{
                    console.log('[Vyapaar Soundbox] Mic listening for wake word...');
                }};

                recognition.onresult = function(event) {{
                    if (isPlaying || isProcessing) return;

                    var fullInterim = '';
                    for (var i = event.resultIndex; i < event.results.length; i++) {{
                        fullInterim += event.results[i][0].transcript + ' ';
                    }}
                    var text = fullInterim.trim();
                    if (!text) return;

                    // Check for wake word
                    if (!wakeDetected) {{
                        if (WAKE_REGEX.test(text)) {{
                            // ── INSTANT WAKE-UP ──
                            wakeDetected = true;
                            startWavRecording();

                            document.getElementById('dot').className = 'pulse-dot wake-triggered';
                            document.getElementById('status_text').innerHTML =
                                '⚡ <strong>\"हे मुनीमजी\" सक्रिय — सुन रहे हैं (Sarvam AI)...</strong>';
                            document.getElementById('transcript_display').innerHTML =
                                '🗣️ <strong style="color:#0084c7;">' + text + '</strong>';

                            activeCommandText = text;

                            if (silenceTimer) clearTimeout(silenceTimer);
                            silenceTimer = setTimeout(function() {{
                                if (wakeDetected && !isProcessing && !isPlaying) {{
                                    commitCommand();
                                }}
                            }}, 1600);
                        }}
                        // Standby mode: ignores room chatter
                    }} else {{
                        // ── WAKE ALREADY ACTIVE — ACCUMULATE COMMAND ──
                        activeCommandText = text;
                        document.getElementById('transcript_display').innerHTML =
                            '🗣️ <strong style="color:#0084c7;">' + activeCommandText + '</strong>';

                        if (silenceTimer) clearTimeout(silenceTimer);
                        silenceTimer = setTimeout(function() {{
                            if (wakeDetected && !isProcessing && !isPlaying) {{
                                commitCommand();
                            }}
                        }}, 1500);
                    }}
                }};

                recognition.onerror = function(e) {{
                    console.warn('[Soundbox Mic Notice]', e.error);
                    if (e.error === 'not-allowed') {{
                        document.getElementById('status_text').innerHTML =
                            '⚠️ <strong>माइक की अनुमति नहीं मिली &bull; ऊपर URL बार में माइक आइकॉन पर क्लिक करके Allow करें</strong>';
                    }}
                }};

                recognition.onend = function() {{
                    // Auto-restart if we are still in standby and not playing audio
                    if (!isPlaying && !isProcessing) {{
                        setTimeout(function() {{
                            try {{ recognition.start(); }} catch(e) {{}}
                        }}, 200);
                    }}
                }};

                try {{
                    recognition.start();
                }} catch(e) {{
                    console.warn('Recognition start error:', e);
                }}
            }}

            function commitCommand() {{
                if (isProcessing || isPlaying) return;
                var cmd = activeCommandText;
                if (!cmd || cmd.trim().length === 0) return;
                var wavBlob = stopWavRecordingAndGetBlob();
                executeVoiceCommand(cmd, wavBlob);
            }}

            // ───────────────────────────────────────────────────
            // Execute voice command → /api/process-voice
            // ───────────────────────────────────────────────────
            function executeVoiceCommand(text, wavBlob) {{
                if (isProcessing || isPlaying) return;
                isProcessing = true;
                wakeDetected = false;
                if (silenceTimer) clearTimeout(silenceTimer);

                // MUTE MIC: Stop recognition so speaker audio is never heard
                isPlaying = true;
                if (recognition) {{
                    try {{ recognition.stop(); }} catch(e) {{}}
                }}

                document.getElementById('status_text').innerHTML =
                    '⏳ <strong>साउंडबॉक्स हिसाब जोड़ रहा है (Sarvam AI)...</strong>';
                document.getElementById('transcript_display').innerHTML =
                    '⏳ <em>प्रोसेस हो रहा है: \"' + text + '\"</em>';

                var formData = new FormData();
                formData.append('raw_text_input', text);
                if (wavBlob) {{
                    formData.append('file', wavBlob, 'command.wav');
                }}

                var endpoints = [
                    'http://127.0.0.1:8000/api/process-voice',
                    backendUrl + '/api/process-voice',
                    'http://localhost:8000/api/process-voice',
                    'http://127.0.0.1:8001/api/process-voice',
                    'http://localhost:8001/api/process-voice'
                ];

                function tryFetch(i) {{
                    if (i >= endpoints.length) {{
                        document.getElementById('status_text').innerHTML =
                            '⚠️ <strong>बैकएंड से संपर्क नहीं हो सका — port 8000/8001 चेक करें</strong>';
                        setTimeout(resetStandby, 3000);
                        return;
                    }}
                    fetch(endpoints[i], {{ method: 'POST', body: formData }})
                    .then(function(res) {{
                        if (!res.ok) throw new Error('HTTP ' + res.status);
                        return res.json();
                    }})
                    .then(function(data) {{
                        var respText = data.audio_response_text || 'निर्देश दर्ज हुआ';
                        document.getElementById('status_text').innerHTML =
                            '🔊 <strong>साउंडबॉक्स (Sarvam Bulbul) बोल रहा है...</strong>';
                        document.getElementById('transcript_display').innerHTML =
                            '✅ <strong>साउंडबॉक्स:</strong> ' + respText;

                        if (data.audio_base64) {{
                            var snd = new Audio('data:audio/mp3;base64,' + data.audio_base64);
                            snd.onended = function() {{
                                // 600ms buffer after audio finishes before restarting mic
                                setTimeout(resetStandby, 600);
                            }};
                            snd.onerror = function() {{ resetStandby(); }};
                            snd.play().catch(function() {{ resetStandby(); }});
                        }} else {{
                            setTimeout(resetStandby, 3000);
                        }}
                    }})
                    .catch(function(err) {{
                        console.log('Endpoint ' + endpoints[i] + ' failed:', err);
                        tryFetch(i + 1);
                    }});
                }}
                tryFetch(0);
            }}

            // ───────────────────────────────────────────────────
            // Reset to standby, restart listen loop
            // ───────────────────────────────────────────────────
            function resetStandby() {{
                isProcessing = false;
                wakeDetected = false;
                activeCommandText = "";

                document.getElementById('dot').className = 'pulse-dot';
                document.getElementById('status_text').innerHTML =
                    '🟢 <strong>साउंडबॉक्स हमेशा सुन रहा है (Always-On) • बोलें: &ldquo;हे मुनीमजी&rdquo; या &ldquo;नमस्ते मुनीमजी&rdquo;</strong>';
                document.getElementById('transcript_display').innerHTML =
                    '🎙️ <em>साउंडबॉक्स काउंटर पर हमेशा सुन रहा है। बिना कोई बटन दबाए सीधे बोलें: <strong>\"हे मुनीमजी\"</strong></em>';

                // Re-enable microphone and start recognition
                setTimeout(function() {{
                    isPlaying = false;
                    isProcessing = false;
                    startRecognition();
                }}, 400);
            }}

            // Request mic permission on page load and start listening
            if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {{
                navigator.mediaDevices.getUserMedia({{ audio: true }})
                .then(function(stream) {{
                    initAudioContext(stream);
                    startRecognition();
                }})
                .catch(function(err) {{
                    console.warn('getUserMedia notice:', err);
                    startRecognition();
                }});
            }} else {{
                startRecognition();
            }}
        </script>
    </body>
    </html>
    """
    components.html(wake_listener_html, height=135)

    v1, v2 = st.columns([1.1, 1.2])
    with v1:
        st.markdown(r"""
        <div class="soundbox-container">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div class="soundbox-logo">paytm <span>SOUNDBOX</span></div>
                <div><span class="soundbox-led"></span> <span style="font-size: 0.72rem; color: #a7f3d0; font-weight: 700;">काउंटर माइक एक्टिव</span></div>
            </div>
            <div class="soundbox-grille"></div>
            <div style="font-size: 0.85rem; color: #cbd5e1;">
                दुकान का साउंडबॉक्स &bull; वेक-वर्ड "नमस्ते मुनीमजी" पर सक्रिय
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("#### 🎤 1. माइक दबाकर बोलें:")
        mic_audio = st.audio_input("काउंटर पर बोलने के लिए माइक बटन दबाएं:")
        if mic_audio is not None:
            st.audio(mic_audio)
            if st.button("⚡ मेरी आवाज़ से हिसाब चढ़ाओ", type="primary"):
                with st.spinner("साउंडबॉक्स आवाज़ प्रोसेस कर रहा है..."):
                    try:
                        files = {"file": ("direct_mic_recording.wav", mic_audio.getvalue(), "audio/wav")}
                        r = requests.post(f"{BACKEND_URL}/api/process-voice", files=files, timeout=20)
                        if r.status_code == 200:
                            st.session_state["real_voice_result"] = r.json()
                            st.success("✅ बही-खाता अपडेट हो गया!")
                            time.sleep(0.5)
                            st.rerun()
                        else:
                            st.error(f"त्रुटि: {r.text}")
                    except Exception as e:
                        st.error(f"बैकएंड कनेक्शन समस्या: {e}")

        st.markdown("---")
        st.markdown("#### ⌨️ या लिखकर निर्देश दें:")
        typed_voice = st.text_input("यहाँ लिखें (वेक-वर्ड के साथ या बिना):", placeholder="उदा: नमस्ते मुनीमजी, शर्मा जी का 850 रुपये उधार लिख लो")
        if st.button("📝 हिसाब दर्ज करें", key="btn_dukaan_typed_main"):
            if typed_voice:
                with st.spinner("दर्ज किया जा रहा है..."):
                    r = requests.post(f"{BACKEND_URL}/api/process-voice", data={"raw_text_input": typed_voice})
                    if r.status_code == 200:
                        st.session_state["real_voice_result"] = r.json()
                        st.success("✅ दर्ज हो गया!")
                        time.sleep(0.5)
                        st.rerun()

    with v2:
        st.markdown("#### 📢 साउंडबॉक्स वॉइस मॉनिटर & लाइव रिस्पांस")
        if "real_voice_result" in st.session_state:
            res = st.session_state["real_voice_result"]
            if res.get("wake_word_detected"):
                st.markdown("<span class='guardrail-tag' style='background: #dcfce7; color: #15803d; border-color: #86efac;'>🟢 वेक-वर्ड पहचाना गया</span>", unsafe_allow_html=True)
            st.info(f"🗣️ **पहचाना गया निर्देश:** {res.get('transcript', '')}")
            st.success(f"🔊 **साउंडबॉक्स (Sarvam Bulbul):** {res.get('audio_response_text', '')}")
            
            b64_audio = res.get("audio_base64")
            if b64_audio:
                audio_bytes = base64.b64decode(b64_audio)
                st.audio(audio_bytes, format="audio/mp3")

            if res.get("action_taken"):
                st.caption(f"⚙️ **दर्ज कार्यवाही:** {res.get('action_taken')}")
        else:
            st.markdown("""
            <div style="background: #f8fafc; border: 1.5px dashed #cbd5e1; border-radius: 12px; padding: 24px 20px; text-align: center;">
                <div style="font-size: 2.2rem; margin-bottom: 8px;">🎙️</div>
                <strong style="color: #1e293b; font-size: 1.05rem;">साउंडबॉक्स लाइव सुन रहा है (Hands-Free Active)</strong>
                <p style="color: #64748b; font-size: 0.88rem; margin-top: 8px; line-height: 1.6;">
                    काउंटर पर बिना कोई बटन दबाए सीधे बोलें:<br>
                    <strong style="color: #0284c7;">"हे मुनीमजी, सुरेश शर्मा जी के 1000 रुपये उधार लिखो जो वो 20 सितंबर को देंगे"</strong><br>
                    या <strong style="color: #0284c7;">"हे मुनीमजी, अमूल दूध के 20 पैकेट आर्डर डाल दो"</strong>
                </p>
                <div style="margin-top: 12px;">
                    <span style="background: #e0f2fe; color: #0369a1; padding: 4px 14px; border-radius: 20px; font-size: 0.78rem; font-weight: 700;">
                        ⚡ Sarvam Saaras v3 STT &bull; Sarvam Bulbul v2 TTS
                    </span>
                </div>
            </div>
            """, unsafe_allow_html=True)

# --------------------------------------------------------------------------
# DUKAAN TAB 2: KHATA BAHI (CUSTOMER UDHAAR RECOVERY)
# --------------------------------------------------------------------------
with tab_khata:
    st.markdown("### 📒 ग्राहकों का उधार खाता (उगाही और हिसाब)")
    st.caption("कागज़ की डायरी की जगह डिजिटल खाता बही: 1-क्लिक में पैसे वसूलें या WhatsApp पर तकादा संदेश भेजें।")

    k_col1, k_col2 = st.columns([2, 1.2])
    with k_col1:
        st.markdown(f"#### 👥 कुल उधार ग्राहक: **{len(live_state.get('customers_udhaar', []))}**")
        
        if live_state.get("customers_udhaar"):
            for cust in live_state["customers_udhaar"]:
                c_name = cust.get("customer_name") or cust.get("name", "ग्राहक")
                c_amt = cust.get("amount") if cust.get("amount") is not None else cust.get("total_due", 0.0)
                c_phone = cust.get("phone", "+91 98765 00000")
                c_id = cust.get("id", "")
                items_raw = cust.get("items", "किराना सामान")
                items_str = ", ".join(items_raw) if isinstance(items_raw, list) else str(items_raw)
                last_tx = cust.get("last_reminded") or cust.get("created_at") or cust.get("last_transaction", "हाल ही में")
                due_date_str = cust.get("due_date")
                due_badge = f'<span style="background: #fef3c7; color: #b45309; border: 1px solid #fde68a; padding: 2px 8px; border-radius: 6px; font-weight: 700; font-size: 0.75rem;">📅 देय तारीख: {due_date_str}</span>' if due_date_str and due_date_str != "Not specified" else ""

                c_box1, c_box2, c_box3 = st.columns([2.2, 1, 1])
                with c_box1:
                    st.markdown(f"""
                    <div class="customer-card">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <strong style="font-size: 1.05rem; color: #0f172a;">{c_name}</strong>
                            <span style="font-size: 1.15rem; font-weight: 800; color: #d97706;">₹{c_amt:,.0f}</span>
                        </div>
                        <div style="font-size: 0.82rem; color: #64748b; margin-top: 4px;">
                            📞 {c_phone} &bull; <em>{items_str}</em>
                        </div>
                        <div style="display: flex; gap: 8px; align-items: center; margin-top: 5px; flex-wrap: wrap;">
                            <span style="font-size: 0.75rem; color: #94a3b8;">अंतिम लेन-देन: {last_tx}</span>
                            {due_badge}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                with c_box2:
                    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
                    if st.button("🟢 पैसे मिल गए", key=f"settle_main_{c_id}"):
                        with st.spinner("खाता चुकता किया जा रहा है..."):
                            r = requests.post(f"{BACKEND_URL}/api/udhaar/settle", data={"udhaar_id": c_id})
                            if r.status_code == 200:
                                st.success(f"✅ {c_name} का उधार चुकता हो गया!")
                                time.sleep(0.5)
                                st.rerun()
                with c_box3:
                    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
                    if st.button("📲 तकादा भेजें", key=f"remind_main_{c_id}"):
                        with st.spinner("तकादा संदेश भेजा जा रहा है..."):
                            r = requests.post(f"{BACKEND_URL}/api/process-voice", data={"raw_text_input": f"{c_name} को व्हाट्सएप पर तकादा संदेश भेजो"})
                            if r.status_code == 200:
                                st.success("✅ तकादा भेज दिया!")
                                time.sleep(0.5)
                                st.rerun()
        else:
            st.info("वर्तमान में कोई बकाया उधार नहीं है।")

    with k_col2:
        st.markdown("#### ➕ नया उधार ग्राहक जोड़ें")
        with st.form("form_add_udhaar_main"):
            new_c_name = st.text_input("ग्राहक का नाम", placeholder="उदा: रमेश गुप्ता")
            new_c_phone = st.text_input("फ़ोन नंबर", placeholder="+91 98111 00000")
            new_c_amt = st.number_input("उधार राशि (₹)", min_value=10.0, step=50.0, value=250.0)
            new_c_items = st.text_input("सामान का विवरण", placeholder="उदा: आटा 5kg, सरसों तेल 1L")
            
            submitted = st.form_submit_button("➕ बही-खाते में जोड़ें", type="primary")
            if submitted:
                if new_c_name:
                    r = requests.post(f"{BACKEND_URL}/api/udhaar/add", data={
                        "customer_name": new_c_name,
                        "phone": new_c_phone,
                        "amount": new_c_amt,
                        "items": new_c_items
                    })
                    if r.status_code == 200:
                        st.success("✅ नया उधार दर्ज हुआ!")
                        time.sleep(0.5)
                        st.rerun()

# --------------------------------------------------------------------------
# DUKAAN TAB 3: GALLA & EMERGENCY LOAN (SMART CASH PREDICTION)
# --------------------------------------------------------------------------
with tab_loan:
    st.markdown("### 💰 गल्ला और इमरजेंसी वर्किंग कैपिटल लोन")
    st.caption("सप्लायर के बड़े बिलों के कारण दुकान का माल न रुके: व्यापार-OS गल्ले की कमी पहले ही भांप लेता है।")

    cf_data = get_cashflow_data()
    gl_c1, gl_c2 = st.columns([1.2, 1])

    with gl_c1:
        st.markdown("#### 📊 अगले 7 दिनों का गल्ला और खर्चे का अनुमान")
        if cf_data and cf_data.get("timeline"):
            tdf = pd.DataFrame(cf_data["timeline"])
            tdf_renamed = tdf.rename(columns={
                "day": "दिन",
                "inflow": "बिक्री और वसूली (₹)",
                "supplier_due": "सप्लायर का भुगतान (₹)",
                "closing_balance": "गल्ले का शेष (₹)"
            })
            st.dataframe(tdf_renamed, hide_index=True)

            if cf_data.get("deficit_predicted"):
                st.warning(f"⚠️ **गल्ले में कमी की चेतावनी:** **{cf_data['deficit_day']}** को सप्लायर को देने के लिए **₹{cf_data['deficit_amount']:,.0f}** कम पड़ सकते हैं!")
            else:
                st.success("✅ गल्ले में पर्याप्त नकदी उपलब्ध है।")
        else:
            st.info("कैश फ्लो डेटा लोड हो रहा है...")

    with gl_c2:
        st.markdown("#### ⚡ 1-क्लिक इमरजेंसी गल्ला सपोर्ट")
        active_loan = live_state.get("active_loan")
        loan_offer = cf_data.get("smart_micro_lending") if cf_data else None

        if active_loan:
            st.markdown(f"""
            <div class="loan-phone-card" style="border-color: #10b981; background: #f0fdf4;">
                <div style="font-size: 2.2rem;">✅</div>
                <h3 style="margin: 4px 0 0 0; color: #047857;">लोन गल्ले में जुड़ चुका है</h3>
                <div style="font-size: 1.9rem; font-weight: 800; color: #047857; margin: 10px 0;">₹{active_loan['amount']:,.0f}</div>
                <p style="font-size: 0.85rem; color: #334155;">
                    <strong>पार्टनर:</strong> {active_loan.get('lender', 'Paytm Business Finance')}<br>
                    <strong>रेफरेंस नंबर:</strong> {active_loan.get('ref_id', '#LOAN12345')}<br>
                    <strong>समय:</strong> {active_loan.get('disbursed_at', 'आज')}
                </p>
                <div style="color: #15803d; font-weight: 700; font-size: 0.85rem;">
                    🛡️ सप्लायर भुगतान सुरक्षित &bull; दुकान का माल नहीं रुकेगा!
                </div>
            </div>
            """, unsafe_allow_html=True)
        elif loan_offer:
            st.markdown(f"""
            <div class="loan-phone-card">
                <div style="font-size: 2rem; color: #00b9f1;">✨</div>
                <div style="font-size: 0.8rem; color: #00b9f1; font-weight: 800; text-transform: uppercase;">Paytm For Business</div>
                <h3 style="margin: 4px 0 0 0; color: #002e6e;">प्री-अप्रूव्ड वर्किंग कैपिटल लोन</h3>
                <p style="color: #64748b; font-size: 0.85rem; margin-top: 4px;">
                    सप्लायर भुगतान में कमी को पूरा करने के लिए तुरंत उपलब्ध।
                </p>
                <div style="background: #f8fafc; border-radius: 12px; padding: 14px; margin: 12px 0; text-align: left; border: 1px solid #e2e8f0;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
                        <span style="color: #64748b;">स्वीकृत राशि:</span>
                        <strong style="color: #0f172a; font-size: 1.25rem;">₹{loan_offer['approved_amount']:,.0f}</strong>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
                        <span style="color: #64748b;">पार्टनर बैंक:</span>
                        <strong style="color: #0f172a;">{loan_offer['lender']}</strong>
                    </div>
                    <div style="display: flex; justify-content: space-between;">
                        <span style="color: #64748b;">प्रोसेसिंग:</span>
                        <strong style="color: #10b981;">तुरंत (0% पेपरवर्क)</strong>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
            if st.button("🚀 ₹50,000 अभी गल्ले में ट्रांसफर करें", type="primary", key="btn_drawdown_main"):
                with st.spinner("Paytm वॉलेट में लोन ट्रांसफर हो रहा है..."):
                    r = requests.post(f"{BACKEND_URL}/api/loan/drawdown")
                    if r.status_code == 200:
                        st.success("🎉 ₹50,000 आपके गल्ले में सफलतापूर्वक जुड़ गए!")
                        time.sleep(0.5)
                        st.rerun()

# --------------------------------------------------------------------------
# DUKAAN TAB 4: STOCK & RESTOCK ORDERS
# --------------------------------------------------------------------------
with tab_stock:
    st.markdown("### 📦 दुकान का सामान और सप्लायर आर्डर")
    st.caption("सामान खत्म होने से पहले ही आर्डर करें ताकि ग्राहक खाली हाथ न लौटे।")

    st_c1, st_c2 = st.columns([1.5, 1])
    with st_c1:
        st.markdown("#### 🛒 किराना सामान स्थिति (इन्वेंट्री):")
        if live_state.get("inventory"):
            inv_items = live_state["inventory"]
            for idx, item in enumerate(inv_items):
                sku_id = item.get("sku") or item.get("id", f"sku_{idx}")
                item_name = item.get("name", "किराना सामान")
                curr_stock = item.get("current_stock", 0)
                min_thresh = item.get("min_threshold", 0)
                unit = item.get("unit", "यूनिट")
                status_raw = item.get("status", "HEALTHY")
                is_low = status_raw in ["LOW_STOCK", "CRITICAL_LOW", "LOW"] or curr_stock <= min_thresh
                status_badge = "🔴 कम है (Low)" if is_low else "🟢 पर्याप्त (OK)"

                i_col1, i_col2 = st.columns([2.5, 1.2])
                with i_col1:
                    st.markdown(f"""
                    <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 10px; padding: 12px 14px; margin-bottom: 8px;">
                        <div style="display: flex; justify-content: space-between;">
                            <strong>{item_name}</strong>
                            <span style="font-weight: 700;">{status_badge}</span>
                        </div>
                        <div style="font-size: 0.82rem; color: #64748b; margin-top: 4px;">
                            वर्तमान स्टॉक: <strong>{curr_stock} {unit}</strong> &bull; न्यूनतम सीमा: {min_thresh} {unit}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                with i_col2:
                    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
                    if is_low:
                        if st.button(f"🛒 आर्डर भेजें", key=f"reorder_main_{sku_id}"):
                            with st.spinner(f"{item_name} का आर्डर भेजा जा रहा है..."):
                                r = requests.post(f"{BACKEND_URL}/api/process-voice", data={"raw_text_input": f"{item_name} 20 पैकेट ऑर्डर डाल दो"})
                                if r.status_code == 200:
                                    st.success(f"✅ {item_name} का आर्डर डिस्ट्रीब्यूटर को भेज दिया!")
                                    time.sleep(0.5)
                                    st.rerun()

    with st_c2:
        st.markdown("#### 🚚 सप्लायर बिल एवं देय तिथियां:")
        if live_state.get("supplier_invoices"):
            for inv in live_state["supplier_invoices"]:
                st.markdown(f"""
                <div style="background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 12px; padding: 14px; margin-bottom: 10px;">
                    <div style="display: flex; justify-content: space-between;">
                        <strong style="color: #0f172a;">{inv['supplier_name']}</strong>
                        <strong style="color: #dc2626; font-size: 1.05rem;">₹{inv['total_amount']:,.0f}</strong>
                    </div>
                    <div style="font-size: 0.82rem; color: #475569; margin-top: 4px;">
                        इनवॉइस #: {inv['invoice_id']} &bull; देय: <strong>{inv['due_in_days']} दिन में</strong>
                    </div>
                </div>
                """, unsafe_allow_html=True)

# --------------------------------------------------------------------------
# DUKAAN TAB 5: PARCHI SCANNER
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
# TAB 5: PARCHI SCANNER (1-CLICK SARVAM VISION ZERO-UI INGESTION)
# --------------------------------------------------------------------------
with tab_parchi:
    st.markdown(f"### {T('📸 कागज़ की कच्ची पर्ची स्कैनर (Zero-UI Ingestion)', '📸 Paper Kacha Slip Scanner (Zero-UI Ingestion)')}")
    st.caption(T('सरवम एआई (Sarvam Vision 1.5) सीधे फोटो से ग्राहक नाम, सामान और उधार राशि बही-खाते में चढ़ा देता है — बिना किसी टाइपिंग के!', 'Sarvam AI Document Intelligence reads handwritten slips directly into the live ledger — zero manual typing required!'))

    p_c1, p_c2 = st.columns([1, 1.2])
    with p_c1:
        slip_mode = st.radio(
            T('पर्ची का स्रोत:', 'Select Slip Source:'),
            [
                T('📷 पर्ची की फोटो अपलोड करें', '📷 Upload Slip Photo'),
                T('📄 किराना टेस्ट पर्ची (Sample Bill)', '📄 Kirana Test Slip')
            ],
            horizontal=True,
            key='radio_slip_source_main'
        )

        active_image_bytes = None
        active_image_filename = None

        if '📷' in slip_mode:
            uploaded_slip = st.file_uploader(
                T('पर्ची की फोटो चुनें (JPG/PNG):', 'Choose Slip Photo (JPG/PNG):'),
                type=['png', 'jpg', 'jpeg'],
                key='upl_slip_main'
            )
            if uploaded_slip:
                active_image_bytes = uploaded_slip.getvalue()
                active_image_filename = uploaded_slip.name
                st.image(uploaded_slip, caption=T('अपलोड की गई पर्ची', 'Uploaded Slip'), use_container_width=True)
            else:
                st.info(T('👆 कृपया ऊपर कच्ची पर्ची की फोटो अपलोड करें।', '👆 Please upload a photo of the handwritten slip above.'))
        else:
            if os.path.exists('test_kacha_slip.jpg'):
                with open('test_kacha_slip.jpg', 'rb') as f:
                    active_image_bytes = f.read()
                active_image_filename = 'test_kacha_slip.jpg'
                st.image('test_kacha_slip.jpg', caption=T('हस्तलिखित किराना पर्ची (Sample Kirana Slip)', 'Handwritten Kirana Slip (Sample)'), use_container_width=True)
            else:
                st.warning('test_kacha_slip.jpg not found.')

        # 1-CLICK ACTION BUTTON - NO CONFUSING BUTTONS, NO EXPLANATION ASKED!
        st.markdown("<div style='height: 6px;'></div>", unsafe_allow_html=True)
        btn_scan = st.button(
            T('⚡ पर्ची स्कैन करें और सीधे बही-खाते में जोड़ें', '⚡ Scan Slip & Directly Ingest into Ledger'),
            type='primary',
            use_container_width=True,
            key='btn_scan_parchi_direct'
        )

        if btn_scan:
            if active_image_bytes:
                with st.spinner(T('🔍 सरवम एआई (Sarvam Document Intelligence) द्वारा फोटो से हिसाब निकाला जा रहा है...', '🔍 Sarvam AI is reading handwritten slip directly from image...')):
                    try:
                        files = {'file': (active_image_filename or 'slip.jpg', active_image_bytes, 'image/jpeg')}
                        r = requests.post(f"{BACKEND_URL}/api/process-slip", files=files, timeout=35)
                        if r.status_code == 200:
                            res_json = r.json()
                            st.session_state['slip_result'] = res_json
                            st.session_state['extracted_raw_text'] = res_json.get('raw_text', '')
                            st.success(T('✅ पर्ची का हिसाब सीधे बही-खाते में दर्ज हो गया!', '✅ Slip debts directly ingested into live ledger!'))
                            time.sleep(0.5)
                            st.rerun()
                        else:
                            st.error(f"Backend error ({r.status_code}): {r.text}")
                    except Exception as ex:
                        st.error(f"Error connecting to backend: {ex}")
            else:
                st.warning(T('कृपया पहले पर्ची की फोटो चुनें।', 'Please upload or select a slip photo first.'))

        # Collapsed optional fallback for blurry slips
        is_editor_open = st.session_state.get('open_slip_text_editor', False) or bool(st.session_state.get('extracted_raw_text'))
        with st.expander(T('✍️ वैकल्पिक: यदि पर्ची बहुत धुंधली हो तो पाठ देखें/बदलें', '✍️ Optional: View or edit text if slip is blurry'), expanded=is_editor_open):
            fallback_text = st.text_area(
                T('पर्ची का पाठ (Slip Text):', 'Slip Text:'),
                value=st.session_state.get('extracted_raw_text', ''),
                height=110,
                placeholder=T('उदा:\n1. सुरेश शर्मा - 2 पैकेट तेल = ₹850\n2. पूजा वर्मा - 10kg आटा = ₹620\n3. ढाबा अनिल = ₹1200',
                              'e.g.:\n1. Suresh Sharma - 2x Oil = ₹850\n2. Pooja Verma - 10kg Atta = ₹620\n3. Dhaba Anil = ₹1200'),
                key='input_fallback_slip_text'
            )
            if st.button(T('⚡ इस पाठ से खाता अपडेट करें', '⚡ Update Ledger from This Text'), key='btn_update_from_text', type='secondary', use_container_width=True):
                # Retrieve the most current text from session state or widget variable
                text_to_process = st.session_state.get('input_fallback_slip_text') or fallback_text or ''
                text_to_process = text_to_process.strip()
                if text_to_process and len(text_to_process) >= 2:
                    st.session_state['open_slip_text_editor'] = True
                    with st.spinner(T('खाता बही में दर्ज हो रहा है...', 'Updating store ledger...')):
                        try:
                            # Dynamic backend port lookup to always target active backend
                            active_url = _find_backend_url()
                            r = requests.post(f"{active_url}/api/process-slip", data={'raw_text_input': text_to_process}, timeout=25)
                            if r.status_code == 200:
                                res_payload = r.json()
                                st.session_state['slip_result'] = res_payload
                                st.session_state['extracted_raw_text'] = text_to_process
                                st.success(T('✅ खाता सफलतापूर्वक अपडेट हो गया!', '✅ Ledger updated successfully from text!'))
                                time.sleep(0.4)
                                st.rerun()
                            else:
                                st.error(f"Backend error ({r.status_code}): {r.text}")
                        except Exception as e:
                            st.error(f"Error connecting to backend: {e}")
                else:
                    st.warning(T('कृपया पहले पर्ची का पाठ दर्ज करें (उदा: सुरेश शर्मा = ₹850)', 'Please enter slip text first (e.g. Suresh Sharma = ₹850)'))

    with p_c2:
        st.markdown(f"#### {T('📄 पर्ची से निकाला गया हिसाब:', '📄 Extracted Ledger Debts:')}")
        if 'slip_result' in st.session_state:
            s_res = st.session_state['slip_result']
            st.success(f"✅ {s_res.get('action_status', T('हिसाब दर्ज हुआ', 'Debts Ingested'))}")
            
            # Detected raw text
            raw_detected = s_res.get('raw_text', '')
            if raw_detected:
                with st.expander(T('👁️ सरवम एआई द्वारा पढ़ा गया मूल पाठ (Detected Text)', '👁️ Original Text Detected by Sarvam AI'), expanded=True):
                    st.code(raw_detected, language='markdown')

            slip_df = pd.DataFrame(s_res.get('parsed_entities', {}).get('new_udhaars', []))
            if not slip_df.empty:
                rename_map = {
                    'customer': T('ग्राहक (Customer)', 'Customer'),
                    'amount': T('उधार राशि (Amount ₹)', 'Amount (₹)'),
                    'items': T('सामान (Items)', 'Items Description'),
                    'due_date': T('तारीख (Date)', 'Date')
                }
                slip_df = slip_df.rename(columns={k: v for k, v in rename_map.items() if k in slip_df.columns})
                st.dataframe(slip_df, hide_index=True, use_container_width=True)
            else:
                st.warning(T('पर्ची से कोई वैध उधार नहीं मिला।', 'No valid debts found in slip.'))
        else:
            st.info(T('पर्ची स्कैन करने पर यहाँ सरवम एआई द्वारा निकाले गए ग्राहकों के नाम, सामान और उधार की सूची दिखेगी।', 'Parsed customer names, items, and debt amounts will appear here once processed by Sarvam AI.'))
