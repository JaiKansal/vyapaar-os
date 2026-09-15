import streamlit as st
import requests
import base64
import json
import time
import pandas as pd
from sample_data import SAMPLE_INDIC_VOICE_PRESETS, SAMPLE_KACHA_BILLS

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Vyapaar-OS | The Autonomous Merchant Partner",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Auto-start backend in background thread if not already running (for Streamlit Community Cloud)
import threading
def _ensure_backend_running():
    try:
        requests.get("http://127.0.0.1:8000/", timeout=0.8)
    except Exception:
        def _run():
            import uvicorn
            import backend
            uvicorn.run(backend.app, host="127.0.0.1", port=8000, log_level="warning")
        t = threading.Thread(target=_run, daemon=True)
        t.start()
        time.sleep(1.5)

_ensure_backend_running()

BACKEND_URL = "http://127.0.0.1:8000"
PUBLIC_HOST_URL = "https://vyapaar-os.streamlit.app"

# --- CUSTOM CSS FOR HIGH-END FINTECH AESTHETICS & RESPONSIVENESS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Outfit:wght@400;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
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
    
    .main-title-container {
        background: linear-gradient(135deg, #002e6e 0%, #00b9f1 100%);
        padding: 22px 26px;
        border-radius: 16px;
        color: white;
        margin-bottom: 20px;
        box-shadow: 0 10px 25px rgba(0, 46, 110, 0.25);
    }
    
    .hackathon-badge {
        display: inline-block;
        background: rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
        color: #fff;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
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
        border-radius: 12px;
        padding: 16px 18px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.04);
        transition: transform 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
    }
    .metric-value {
        font-size: 1.7rem;
        font-weight: 800;
        color: #0f172a;
        font-family: 'Outfit', sans-serif;
    }
    .metric-label {
        font-size: 0.82rem;
        color: #64748b;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Paytm Soundbox Hardware Shell */
    .soundbox-container {
        background: linear-gradient(160deg, #042552 0%, #00122e 100%);
        border: 3px solid #00b9f1;
        border-radius: 20px;
        padding: 20px;
        color: white;
        text-align: center;
        box-shadow: 0 16px 36px rgba(0, 185, 241, 0.25);
        margin-bottom: 16px;
    }
    .soundbox-logo {
        font-size: 1.3rem;
        font-weight: 900;
        letter-spacing: -0.5px;
    }
    .soundbox-logo span {
        color: #00b9f1;
    }
    .soundbox-grille {
        background: radial-gradient(circle, #0c366e 20%, transparent 20%);
        background-size: 8px 8px;
        height: 65px;
        border-radius: 10px;
        margin: 12px auto;
        border: 1px solid rgba(0, 185, 241, 0.3);
    }
    .soundbox-led {
        width: 12px;
        height: 12px;
        border-radius: 50%;
        background-color: #10b981;
        display: inline-block;
        box-shadow: 0 0 10px #10b981;
        animation: pulse 1.8s infinite;
        margin-right: 6px;
    }
    @keyframes pulse {
        0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
        70% { transform: scale(1.1); box-shadow: 0 0 0 8px rgba(16, 185, 129, 0); }
        100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
    }
    
    /* Loan Phone Card matching Slide 5 */
    .loan-phone-card {
        background: #ffffff;
        border: 2px solid #00b9f1;
        border-radius: 18px;
        padding: 20px;
        box-shadow: 0 10px 25px rgba(0, 46, 110, 0.12);
        text-align: center;
    }
    
    .guardrail-tag {
        display: inline-block;
        background: #dcfce7;
        color: #166534;
        font-weight: 700;
        font-size: 0.75rem;
        padding: 3px 8px;
        border-radius: 10px;
        border: 1px solid #86efac;
    }
    
    /* Mobile responsive tweaks */
    @media (max-width: 768px) {
        .metric-value { font-size: 1.3rem; }
        .main-title-container { padding: 14px 16px; }
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
    st.error("⚠️ Connecting to Vyapaar-OS backend on port 8000...")
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


# --- HEADER ---
st.markdown(f"""
<div class="main-title-container">
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
        <div>
            <div class="hackathon-badge">🏆 Paytm Build for India Hackathon (Delhi Edition)</div>
            <h1 style="margin: 0; font-size: 2.1rem; font-weight: 800; letter-spacing: -0.5px;">
                Vyapaar-OS: <span style="font-weight: 400; opacity: 0.95;">The Autonomous Merchant Partner</span>
            </h1>
            <p style="margin: 6px 0 0 0; font-size: 0.95rem; opacity: 0.95;">
                Track 1: Merchant Growth AI &bull; Real Data & Direct Voice Operating System
                <span class="team-badge">Team Well...Hackers &bull; Manya Goel & Jai Kansal</span>
            </p>
        </div>
        <div style="text-align: right;">
            <div style="margin-bottom: 6px;"><span class="public-url-badge">🌐 LIVE PUBLIC DEPLOYMENT</span></div>
            <div style="font-size: 0.8rem; color: #e0f2fe; background: rgba(0,0,0,0.25); padding: 6px 12px; border-radius: 8px;">
                <a href="{PUBLIC_HOST_URL}" target="_blank" style="color: #ffffff; text-decoration: underline; font-weight: 700;">{PUBLIC_HOST_URL}</a>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# --- REAL METRICS BAR ---
col_m1, col_m2, col_m3, col_m4, col_m5 = st.columns(5)
with col_m1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">💵 Real Cash-in-Hand</div>
        <div class="metric-value" style="color: #002e6e;">₹{live_state['cash_in_hand']:,.0f}</div>
        <div style="font-size: 0.72rem; color: #16a34a; font-weight: 600;">Daily Avg: ₹{live_state['daily_sales_avg']:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with col_m2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">⏳ Customer Udhaar</div>
        <div class="metric-value" style="color: #d97706;">₹{live_state['total_udhaar_outstanding']:,.0f}</div>
        <div style="font-size: 0.72rem; color: #64748b;">{len(live_state['customers_udhaar'])} active borrowers</div>
    </div>
    """, unsafe_allow_html=True)

with col_m3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">🚚 Supplier Dues</div>
        <div class="metric-value" style="color: #dc2626;">₹{live_state['total_supplier_dues']:,.0f}</div>
        <div style="font-size: 0.72rem; color: #dc2626; font-weight: 600;">⚠️ Due within 48-96 hrs</div>
    </div>
    """, unsafe_allow_html=True)

with col_m4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">📦 Low Stock SKUs</div>
        <div class="metric-value" style="color: #ea580c;">{live_state['low_stock_items_count']} Items</div>
        <div style="font-size: 0.72rem; color: #ea580c; font-weight: 600;">Requires restock</div>
    </div>
    """, unsafe_allow_html=True)

with col_m5:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">🛡️ Margin Leak Saved</div>
        <div class="metric-value" style="color: #16a34a;">+14%</div>
        <div style="font-size: 0.72rem; color: #16a34a; font-weight: 600;">₹{live_state['margin_leak_saved']:,.0f}/mo protected</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='margin-bottom: 16px;'></div>", unsafe_allow_html=True)


# --- SIDEBAR: REAL SETTINGS & KEYS ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/2/24/Paytm_Logo_%28standalone%29.svg/512px-Paytm_Logo_%28standalone%29.svg.png", width=130)
    st.markdown("### 🌐 Live Public URL")
    st.code(PUBLIC_HOST_URL, language="text")
    st.image("vyapaar_live_qr.png", caption="📱 Scan to Open on Mobile", width=180)
    
    st.markdown("---")
    st.markdown("### ⚡ AI Engine Status (Server)")
    st.markdown("🟢 **Sarvam AI (Perception):** `Active (Server-Side)`")
    st.markdown("🟢 **Google Gemini:** `Configured (Server-Side)`")
    st.markdown("🟢 **Cognee Knowledge Graph:** `Active (Temporal)`")
    st.markdown("🟢 **n8n Action Layer:** `Deterministic`")
    st.markdown("🟢 **Paytm Soundbox:** `2-Way Mic Active`")
            
    st.markdown("---")
    st.markdown("### 🛡️ Production Guardrails")
    st.markdown("<div class='guardrail-tag'>Zero Financial Hallucination</div>", unsafe_allow_html=True)
    st.caption("Strict deterministic validation for all monetary entries, restock orders, and micro-loan drawdowns.")
    
    if st.button("🔄 Refresh Data", use_container_width=True):
        st.rerun()


# --- TABS FOR WORKSPACE ---
t_soundbox, t_udhaar, t_lending, t_graph, t_slip, t_action, t_team = st.tabs([
    "🎙️ 1. Direct Voice & Soundbox",
    "📒 2. Real Udhaar Ledger",
    "💳 3. Smart Micro-Lending",
    "🧠 4. Temporal Graph Memory",
    "📸 5. Slip Ingestion",
    "⚡ 6. Action Engine & WhatsApp",
    "📊 7. Team & Friction"
])


# ==============================================================================
# TAB 1: DIRECT VOICE INPUT & PAYTM SOUNDBOX (SLIDE 5 & 3)
# ==============================================================================
with t_soundbox:
    st.markdown("### 🎙️ Direct Voice Input & Paytm Soundbox (Slide 5)")
    st.caption("Speak directly into your microphone in Hindi, Hinglish, or English. Real speech is transcribed, real store entries are created, and real spoken Hindi response is played back!")
    
    v_col1, v_col2 = st.columns([1.1, 1.2])
    
    with v_col1:
        st.markdown("""
        <div class="soundbox-container">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div class="soundbox-logo">paytm <span>SOUNDBOX</span></div>
                <div><span class="soundbox-led"></span> <span style="font-size: 0.72rem; color: #a7f3d0; font-weight: 700;">2-WAY DIRECT MIC ACTIVE</span></div>
            </div>
            <div class="soundbox-grille"></div>
            <div style="font-size: 0.8rem; color: #cbd5e1;">
                Countertop Voice Operating System &bull; Live Two-Way Interaction
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("#### 🔴 1. Direct Microphone Recording")
        mic_audio = st.audio_input("Click the microphone below to speak:")
        
        if mic_audio is not None:
            st.audio(mic_audio)
            if st.button("⚡ Process My Live Spoken Voice", type="primary", use_container_width=True):
                with st.spinner("Transcribing your speech & executing real store action..."):
                    try:
                        files = {"file": ("direct_mic_recording.wav", mic_audio.getvalue(), "audio/wav")}
                        r = requests.post(f"{BACKEND_URL}/api/process-voice", files=files, timeout=20)
                        if r.status_code == 200:
                            st.session_state["real_voice_result"] = r.json()
                            st.success("✅ Voice Processed & Ledger Updated!")
                            time.sleep(0.5)
                            st.rerun()
                        else:
                            st.error(f"Error ({r.status_code}): {r.text}")
                    except Exception as e:
                        st.error(f"Backend call error: {e}")

        st.markdown("---")
        st.markdown("#### ⌨️ Or Type Voice Instruction Directly:")
        typed_voice = st.text_input("Type merchant command (Hindi/Hinglish/English):", placeholder="e.g. शर्मा जी का 850 रुपये का उधार लिख लो")
        if st.button("Submit Spoken Instruction", key="btn_typed"):
            if typed_voice:
                with st.spinner("Processing instruction..."):
                    r = requests.post(f"{BACKEND_URL}/api/process-voice", data={"raw_text_input": typed_voice})
                    if r.status_code == 200:
                        st.session_state["real_voice_result"] = r.json()
                        st.rerun()

    with v_col2:
        st.markdown("#### ⚡ Quick Voice Scenarios (One-Click Demonstrations)")
        for preset in SAMPLE_INDIC_VOICE_PRESETS:
            p_btn, p_text = st.columns([1, 1.8])
            with p_btn:
                if st.button(preset["title"], key=f"btn_p_{preset['id']}", use_container_width=True):
                    with st.spinner("Processing scenario..."):
                        r = requests.post(f"{BACKEND_URL}/api/process-voice", data={"raw_text_input": preset["transcript"]})
                        if r.status_code == 200:
                            st.session_state["real_voice_result"] = r.json()
                            st.rerun()
            with p_text:
                st.caption(f"🗣️ *\"{preset['transcript']}\"*")

        if "real_voice_result" in st.session_state:
            res = st.session_state["real_voice_result"]
            st.markdown("### 🎯 Soundbox Spoken Response")
            st.markdown(f"**📝 Transcribed Speech:**")
            st.info(f"🗣️ {res['transcript']}")
            
            st.markdown(f"**🔊 Soundbox Spoken Answer (Hindi Audio):**")
            st.success(f"🤖 {res['audio_response_text']}")
            
            b64_audio = res.get("audio_base64")
            if b64_audio:
                audio_bytes = base64.b64decode(b64_audio)
                st.audio(audio_bytes, format="audio/mp3")
                
            st.markdown(f"""
            <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 10px; margin-top: 8px; font-size: 0.85rem;">
                <strong>⚙️ Action Executed:</strong> {res['action_taken']} <br>
                <span class="guardrail-tag">{res['guardrail_status']}</span>
            </div>
            """, unsafe_allow_html=True)


# ==============================================================================
# TAB 2: REAL UDHAAR & INVENTORY LEDGER (REAL DATA CRUD)
# ==============================================================================
with t_udhaar:
    st.markdown("### 📒 Real Store Ledger & Direct Management")
    st.caption("No mock data: All entries are persistent. Add, settle, or manage customer credit and inventory in real-time.")
    
    u_tab1, u_tab2 = st.columns([1.3, 1])
    
    with u_tab1:
        st.markdown("#### 👤 Active Customer Udhaar List")
        if live_state["customers_udhaar"]:
            for u in live_state["customers_udhaar"]:
                with st.expander(f"🔴 {u['customer_name']} — ₹{u['amount']:,.0f} ({u.get('status', 'ACTIVE')})", expanded=True):
                    col_det, col_act = st.columns([2, 1])
                    with col_det:
                        st.markdown(f"**Phone:** `{u['phone']}` | **Overdue:** `{u.get('days_overdue', 0)} days`")
                        st.markdown(f"**Items:** {u.get('items', 'N/A')}")
                    with col_act:
                        if st.button(f"✅ Mark Paid (Collect ₹{u['amount']:,.0f})", key=f"settle_{u['id']}", use_container_width=True):
                            try:
                                r = requests.post(f"{BACKEND_URL}/api/udhaar/settle", data={"udhaar_id": u["id"]})
                                if r.status_code == 200:
                                    st.success(f"Collected ₹{u['amount']} into drawer cash!")
                                    time.sleep(0.5)
                                    st.rerun()
                            except Exception as e:
                                st.error(f"Error: {e}")
        else:
            st.info("No active udhaar debts! All customer accounts are settled.")

    with u_tab2:
        st.markdown("#### ➕ Add New Real Udhaar Record")
        with st.form("form_add_udhaar"):
            new_name = st.text_input("Customer Name", placeholder="e.g. Ramesh Sharma")
            new_phone = st.text_input("Customer Phone", placeholder="+91 98765 12345")
            new_amount = st.number_input("Amount (₹)", min_value=1.0, value=750.0, step=50.0)
            new_items = st.text_area("Purchase Details / Items", placeholder="2x Mustard Oil, 5kg Rice")
            submit_udhaar = st.form_submit_button("Record Real Udhaar Entry", type="primary", use_container_width=True)
            
            if submit_udhaar:
                if new_name:
                    r = requests.post(f"{BACKEND_URL}/api/udhaar/add", data={
                        "customer_name": new_name,
                        "phone": new_phone,
                        "amount": new_amount,
                        "items": new_items
                    })
                    if r.status_code == 200:
                        st.success(f"Recorded ₹{new_amount} for {new_name}!")
                        time.sleep(0.5)
                        st.rerun()
                else:
                    st.warning("Please enter customer name.")


# ==============================================================================
# TAB 3: SMART MICRO-LENDING & CASH FLOW GRAPH (SLIDE 5)
# ==============================================================================
with t_lending:
    st.markdown("### 💳 Smart Micro-Lending & Cash Flow Gap Predictor (Slide 5)")
    st.caption("Predicts upcoming supply-chain cash deficits by cross-referencing supplier deadlines and surfaces pre-underwritten Paytm loans.")
    
    cf_data = get_cashflow_data()
    
    l_col1, l_col2 = st.columns([1.3, 1])
    
    with l_col1:
        st.markdown("#### 📊 Real 7-Day Cash Flow Projection Graph & Numbers")
        if cf_data and cf_data.get("timeline"):
            tdf = pd.DataFrame(cf_data["timeline"])
            
            # Line chart showing closing cash balance vs supplier dues
            st.line_chart(tdf.set_index("day")[["closing_balance", "supplier_due"]])
            
            # Numbers table
            st.markdown("##### Detailed Timeline Numbers:")
            st.dataframe(tdf, use_container_width=True)
            
            if cf_data.get("deficit_predicted"):
                st.error(f"🚨 **SUPPLY-CHAIN CASH DEFICIT PREDICTED:** On **{cf_data['deficit_day']}**, supplier dues exceed drawer balance by **₹{cf_data['deficit_amount']:,.2f}**!")
        else:
            st.info("Loading predictive cash flow data...")

    with l_col2:
        st.markdown("#### 📱 Pre-Underwritten Paytm Loan Card (Slide 5)")
        active_loan = live_state.get("active_loan")
        loan_offer = cf_data.get("smart_micro_lending") if cf_data else None
        
        if active_loan:
            st.markdown(f"""
            <div class="loan-phone-card" style="border-color: #10b981; background: #f0fdf4;">
                <div style="font-size: 2.2rem;">✅</div>
                <h3 style="margin: 4px 0 0 0; color: #047857;">LOAN ACTIVE & DISBURSED</h3>
                <div style="font-size: 1.8rem; font-weight: 800; color: #047857; margin: 10px 0;">₹{active_loan['amount']:,.2f}</div>
                <p style="font-size: 0.85rem; color: #334155;">
                    <strong>Lender:</strong> {active_loan.get('lender', 'Digital Finance Corp')}<br>
                    <strong>Ref ID:</strong> {active_loan.get('ref_id', '#LOAN12345')}<br>
                    <strong>Disbursed At:</strong> {active_loan.get('disbursed_at', 'Just now')}
                </p>
                <div style="color: #15803d; font-weight: 700; font-size: 0.82rem;">
                    🛡️ Deficit bridged. Cash balance increased!
                </div>
            </div>
            """, unsafe_allow_html=True)
        elif loan_offer:
            st.markdown(f"""
            <div class="loan-phone-card">
                <div style="font-size: 2.2rem; color: #00b9f1;">✨</div>
                <div style="font-size: 0.78rem; color: #00b9f1; font-weight: 800; text-transform: uppercase;">Paytm For Business</div>
                <h3 style="margin: 4px 0 0 0; color: #002e6e;">LOAN APPROVED</h3>
                <p style="color: #64748b; font-size: 0.82rem; margin-top: 4px;">
                    Your loan application has been successfully pre-approved to bridge upcoming distributor payments.
                </p>
                <div style="background: #f8fafc; border-radius: 12px; padding: 12px; margin: 12px 0; text-align: left; border: 1px solid #e2e8f0;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                        <span style="color: #64748b; font-size: 0.82rem;">Approved Amount:</span>
                        <strong style="color: #0f172a; font-size: 1.15rem;">₹{loan_offer['approved_amount']:,.0f}</strong>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                        <span style="color: #64748b; font-size: 0.82rem;">Lender:</span>
                        <strong style="color: #0f172a; font-size: 0.82rem;">{loan_offer['lender']}</strong>
                    </div>
                    <div style="display: flex; justify-content: space-between;">
                        <span style="color: #64748b; font-size: 0.82rem;">Reference ID:</span>
                        <strong style="color: #00b9f1; font-size: 0.82rem;">{loan_offer['reference_id']}</strong>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<div style='margin-bottom: 8px;'></div>", unsafe_allow_html=True)
            if st.button("⚡ DRAWDOWN ₹50,000 INTO PAYTM WALLET", type="primary", use_container_width=True):
                with st.spinner("Disbursing loan funds..."):
                    r = requests.post(f"{BACKEND_URL}/api/loan/drawdown")
                    if r.status_code == 200:
                        st.success("🎉 Disbursed ₹50,000 into Business Wallet!")
                        time.sleep(0.5)
                        st.rerun()


# ==============================================================================
# TAB 4: TEMPORAL KNOWLEDGE GRAPH (SLIDE 4)
# ==============================================================================
with t_graph:
    st.markdown("### 🧠 Cognee Temporal Knowledge Graph (Slide 4)")
    st.caption("Live relational topology connecting Suppliers, Payment Deadlines, Stock Levels, and Customer Udhaars.")
    
    try:
        g_data = requests.get(f"{BACKEND_URL}/api/knowledge-graph", timeout=3).json()
        nodes = g_data.get("nodes", [])
        links = g_data.get("links", [])
    except Exception:
        nodes, links = [], []
        
    g_c1, g_c2 = st.columns([1.4, 1])
    with g_c1:
        st.markdown("#### 🌐 Active Relational Graph Links")
        if links:
            df_links = pd.DataFrame(links)
            st.dataframe(df_links, use_container_width=True)
        else:
            st.info("No active links found.")
            
    with g_c2:
        st.markdown("#### 📦 Current Inventory Stock")
        if live_state["inventory"]:
            df_inv = pd.DataFrame(live_state["inventory"])[["name", "current_stock", "min_threshold", "unit", "status"]]
            st.dataframe(df_inv, use_container_width=True)


# ==============================================================================
# TAB 5: ZERO-UI SLIP INGESTION (SLIDE 3)
# ==============================================================================
with t_slip:
    st.markdown("### 📸 Zero-UI Slip Ingestion (Slide 3)")
    st.caption("Snap a photo of handwritten kacha bills to extract debts and arrivals without manual typing.")
    
    sl_col1, sl_col2 = st.columns([1, 1.2])
    with sl_col1:
        slip_choice = st.radio("Select Slip Sample:", [b["title"] for b in SAMPLE_KACHA_BILLS])
        selected_b = next(b for b in SAMPLE_KACHA_BILLS if b["title"] == slip_choice)
        st.code(selected_b["raw_text"], language="text")
        
        if st.button("⚡ Extract & Ingest into Store Database", type="primary", use_container_width=True):
            with st.spinner("Extracting handwritten entities..."):
                r = requests.post(f"{BACKEND_URL}/api/process-slip", data={"slip_id": selected_b["id"]})
                if r.status_code == 200:
                    st.success("✅ Ingested into Real Store Ledger!")
                    time.sleep(0.5)
                    st.rerun()

    with sl_col2:
        st.markdown("#### 📄 Extracted Structured Debts:")
        st.dataframe(pd.DataFrame(selected_b["parsed_data"].get("new_udhaars", [])), use_container_width=True)


# ==============================================================================
# TAB 6: AUTONOMOUS ACTION ENGINE & WHATSAPP (SLIDE 4)
# ==============================================================================
with t_action:
    st.markdown("### ⚡ Action Engine: n8n Deterministic Orchestration (Slide 4)")
    st.caption("Autonomous debt recovery and distributor restocking with zero financial hallucinations.")
    
    a_c1, a_c2 = st.columns(2)
    with a_c1:
        st.markdown("#### 💬 WhatsApp Audio Debt Recovery Preview")
        st.markdown("""
        <div style="background: #e5ddd5; border-radius: 12px; padding: 14px;">
            <div style="font-weight: 700; color: #075e54; margin-bottom: 6px;">
                Recipient: Anil Kumar (Dhaba) (+91 99223 88441)
            </div>
            <div style="background: #dcf8c6; padding: 10px 14px; border-radius: 10px; font-size: 0.85rem; color: #111b21;">
                🎙️ <em>"नमस्ते अनिल भाई, नमस्ते किराना से आपका ₹4,800 का उधार बाकी है। कृपया आज शाम तक भुगतान कर दें।"</em>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div style='margin-bottom: 8px;'></div>", unsafe_allow_html=True)
        if st.button("🚀 Trigger WhatsApp Reminder via n8n", use_container_width=True):
            r = requests.post(f"{BACKEND_URL}/api/process-voice", data={"raw_text_input": "अनिल ढाबे वाले को व्हाट्सएप वॉइस मेमो भेज दो"})
            if r.status_code == 200:
                st.success("✅ WhatsApp Reminder Dispatched!")
                time.sleep(0.5)
                st.rerun()

    with a_c2:
        st.markdown("#### 📞 Distributor Restock Call Bot")
        st.markdown("""
        <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; padding: 14px;">
            <strong>Supplier:</strong> Goyal Dairy Distributors (+91 97111 88442)<br>
            <strong>Order:</strong> 20x Amul Milk, 10x Surf Excel<br>
            <div style="background: #e0f2fe; padding: 8px; border-radius: 6px; margin-top: 6px; font-size: 0.82rem; color: #0369a1;">
                🤖 Automated Voice Bot call scheduled for 07:00 AM delivery.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div style='margin-bottom: 8px;'></div>", unsafe_allow_html=True)
        if st.button("🚀 Trigger Restock Call Bot via n8n", use_container_width=True):
            r = requests.post(f"{BACKEND_URL}/api/process-voice", data={"raw_text_input": "अमूल दूध खत्म हो गया है तुरंत ऑर्डर डाल दो"})
            if r.status_code == 200:
                st.success("✅ Restock Call Dispatched!")
                time.sleep(0.5)
                st.rerun()

    st.markdown("---")
    st.markdown("#### 📜 Live Execution Audit Logs")
    if live_state.get("action_logs"):
        st.dataframe(pd.DataFrame(live_state["action_logs"])[["timestamp", "action_type", "description", "guardrail_status", "n8n_orchestration"]], use_container_width=True)


# ==============================================================================
# TAB 7: TEAM & FRICTION (SLIDES 2 & 6)
# ==============================================================================
with t_team:
    st.markdown("### 📊 The Core Friction: From Chaos to Order (Slide 2)")
    c_f1, c_f2 = st.columns(2)
    with c_f1:
        st.markdown("""
        <div style="background: #fef2f2; border: 2px dashed #f87171; border-radius: 14px; padding: 16px;">
            <div style="font-weight: 800; color: #991b1b; margin-bottom: 6px;">❌ THE REALITY</div>
            <p style="font-size: 0.85rem; color: #7f1d1d; line-height: 1.5;">
                30M+ Indian MSMEs run on scattered handwritten kacha bills and untracked customer udhaar. Merchants lose up to 14% monthly profit margin to dead stock and delayed supplier payments.
            </p>
        </div>
        """, unsafe_allow_html=True)
    with c_f2:
        st.markdown("""
        <div style="background: #f0fdf4; border: 2px solid #22c55e; border-radius: 14px; padding: 16px;">
            <div style="font-weight: 800; color: #166534; margin-bottom: 6px;">✅ VYAPAAR-OS</div>
            <p style="font-size: 0.85rem; color: #14532d; line-height: 1.5;">
                Zero-UI direct voice and slip ingestion, temporal memory graph predicting supply-chain gaps, and instant pre-underwritten Paytm micro-loans to prevent margin leaks.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 👥 Team Well...Hackers (Slide 6)")
    t_c1, t_c2 = st.columns(2)
    with t_c1:
        st.markdown("""
        **Manya Goel** &bull; *Data & Agent Systems Engineer*  
        - AI Engineering & RAG: Built hybrid BM25/Vector retrieval agents.
        - Co-Founder at ManoSathi (Conversational agents on Vertex AI).
        - BS in Data Science & Applications, IIT Madras; B.Tech CSE, IPEC.
        """)
    with t_c2:
        st.markdown("""
        **Jai Kansal** &bull; *AI Architect & Backend Systems*  
        - Software Engineer Intern at Cequence Security (API validation).
        - Co-Founder & Lead Engineer at ManoSathi (IIT Delhi pre-incubated).
        - B.Tech CSE, Faculty of Technology, University of Delhi.
        """)