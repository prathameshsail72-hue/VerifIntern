import streamlit as st
import requests
import os

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000/api")

st.set_page_config(page_title="VerifIntern | Student Trust Shield", page_icon="🛡️", layout="wide")

# Inject Custom CSS for Premium Aesthetics
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Main background with subtle gradient */
.stApp {
    background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
    color: #f8fafc;
}

/* Glassmorphism Cards */
div[data-testid="stForm"], div[data-testid="stVerticalBlock"] > div > div > div > div[data-testid="stVerticalBlock"] {
    background: rgba(255, 255, 255, 0.03) !important;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    padding: 1.5rem;
}

/* Inputs and text areas */
.stTextInput input, .stTextArea textarea, .stSelectbox select {
    background: rgba(15, 23, 42, 0.6) !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    color: white !important;
    border-radius: 8px !important;
}

/* Buttons */
.stButton > button, .stFormSubmitButton > button {
    background: linear-gradient(90deg, #3b82f6 0%, #8b5cf6 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.5rem 1.5rem !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
}

.stButton > button:hover, .stFormSubmitButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 4px 15px rgba(139, 92, 246, 0.4) !important;
}

/* Headers */
h1, h2, h3 {
    color: #e2e8f0 !important;
    font-weight: 700 !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 2rem;
    justify-content: center;
}
.stTabs [data-baseweb="tab"] {
    color: #94a3b8 !important;
}
.stTabs [aria-selected="true"] {
    color: #3b82f6 !important;
    border-bottom-color: #3b82f6 !important;
}

/* Metrics */
[data-testid="stMetricValue"] {
    font-size: 2.5rem !important;
    font-weight: 700 !important;
    background: -webkit-linear-gradient(#60a5fa, #a78bfa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
</style>
""", unsafe_allow_html=True)

# Main UI
st.markdown("<h1 style='text-align: center; margin-bottom: 0;'>🛡️ VerifIntern</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 1.2rem; margin-bottom: 2rem;'>Automated Recruiter & Internship Trust Shield</p>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["🔍 Analyze Company", "📢 Report Scam"])

with tab1:
    st.markdown("<h3 style='text-align: center;'>🔎 Company Trust Profile Verification</h3>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        search_query = st.text_input("Enter company or recruiter domain name:", placeholder="e.g. Sketchy Tech Solutions")
        analyze_btn = st.button("Analyze Trust Profile", use_container_width=True)
        
    if analyze_btn:
        if search_query:
            with st.spinner("Executing OSINT verification engines..."):
                try:
                    response = requests.get(f"{API_URL}/search", params={"name": search_query}).json()
                    
                    st.divider()
                    
                    # Status Indicator
                    status = response.get('verification_status', 'UNKNOWN')
                    if "SAFE" in status:
                        st.success(f"**Verification Status:** {status}")
                    elif "CAUTION" in status:
                        st.warning(f"**Verification Status:** {status}")
                    else:
                        st.error(f"**Verification Status:** {status}")
                        
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    # Metrics Grid
                    m1, m2, m3 = st.columns(3)
                    with m1:
                        st.metric("Trust Score", f"{response.get('trust_score', 0)} / 100")
                    with m2:
                        st.metric("Domain Age", f"{response.get('domain_age_months', 0)} months")
                    with m3:
                        st.metric("Total Incident Flags", response.get('total_scam_reports', 0))
                        
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    # Details
                    st.markdown("#### Detailed Intelligence")
                    details_col1, details_col2 = st.columns(2)
                    with details_col1:
                        st.info(f"**Target Domain:** {response.get('domain', 'N/A')}")
                    with details_col2:
                        if response.get('money_demanded_reports', 0) > 0:
                            st.error(f"**Financial Demands Flagged:** {response.get('money_demanded_reports')}")
                        else:
                            st.info(f"**Financial Demands Flagged:** 0")
                            
                except Exception as e:
                    st.error(f"Could not communicate with backend engine. Ensure main.py is running. Error: {e}")
        else:
            st.info("Please enter a name to execute queries.")

with tab2:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h3 style='text-align: center;'>🚨 Submit Incident Report</h3>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #94a3b8;'>Help protect fellow students by crowdsourcing risk signals.</p>", unsafe_allow_html=True)
        
        with st.form("report_form", clear_on_submit=True):
            fcol1, fcol2 = st.columns(2)
            with fcol1:
                c_name = st.text_input("Company Name*")
            with fcol2:
                channel = st.selectbox("Communication Channel*", ["WhatsApp", "Telegram", "Gmail", "LinkedIn DM", "Other"])
                
            demanded_cash = st.checkbox("Did they ask you for money upfront? (Registration, security deposit, training fees)")
            desc = st.text_area("Incident Description*", placeholder="Provide a brief description of what happened...")
            
            st.markdown("<br>", unsafe_allow_html=True)
            submitted = st.form_submit_button("Submit Incident Record", use_container_width=True)
            
            if submitted:
                if c_name and desc:
                    payload = {
                        "company_name": c_name,
                        "communication_channel": channel,
                        "asked_for_money": demanded_cash,
                        "scam_description": desc
                    }
                    try:
                        res = requests.post(f"{API_URL}/report", json=payload).json()
                        st.success("✅ Report securely logged. Thank you for protecting the community!")
                    except Exception as e:
                        st.error(f"Error submitting report to backend: {e}")
                else:
                    st.warning("Please fill in all required fields marked with *.")