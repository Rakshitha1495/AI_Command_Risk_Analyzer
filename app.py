import streamlit as st
import pandas as pd
import plotly.express as px
from rules import analyze_command
from ai_module import get_ai_response

# 1. PAGE CONFIG
st.set_page_config(
    page_title="COMMAND ANALYZER", 
    layout="wide"
)

# 2. CUSTOM COLOR PALETTE CSS (Kept exactly as you provided)
st.markdown("""
    <style>
    .stApp {
        background-color: #0d1117;
        color: #c9d1d9;
        font-family: 'Segoe UI', sans-serif;
    }
    
    .main-title {
        color: #58a6ff;
        font-size: 2.5rem !important;
        font-weight: 700;
    }

    [data-testid="stMetricLabel"] {
        font-size: 1.1rem !important;
        color: #79c0ff !important;
        font-weight: 600;
        text-transform: uppercase;
    }
    [data-testid="stMetricValue"] {
        color: #58a6ff !important;
        font-size: 3.5rem !important;
    }

    .network-header {
        color: #a5d6ff;
        font-size: 1.2rem !important;
        font-weight: 600;
        text-transform: uppercase;
    }
    .explanation-header {
        color: #d2a8ff;
        font-size: 1.2rem !important;
        font-weight: 600;
        text-transform: uppercase;
    }

    .threat-header { color: #ff7b72; font-size: 1.4rem; font-weight: 600; }
    .mitigation-header { color: #3fb950; font-size: 1.4rem; font-weight: 600; }

    .content-text { font-size: 1.15rem; color: #e6edf3; padding: 5px 0; }
    
    .ai-box {
        font-size: 1.2rem !important;
        color: #ffffff !important;
        background-color: #161b22;
        padding: 20px;
        border-radius: 6px;
        border: 1px solid #30363d;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. HEADER & INPUT
st.markdown('<div class="main-title">COMMAND RISK ANALYZER</div>', unsafe_allow_html=True)
st.markdown("---")

st.markdown('<div style="color:#8b949e; font-weight:600;">ENTER COMMAND</div>', unsafe_allow_html=True)
command = st.text_input("", placeholder="Awaiting terminal syntax...")

if st.button("ANALYZE"):
    if command.strip() == "":
        st.warning("Input required.")
    else:
        # --- LOGIC UPGRADE START ---
        # 1. Run Pre-defined rules
        result = analyze_command(command)
        
        # 2. Get AI Detailed Insight
        ai_output = get_ai_response(command)
        
        # 3. HYBRID INTELLIGENCE CHECK
        # This prevents "rm -rf" from showing as LOW if the AI warns about it.
        danger_keywords = ["danger", "caution", "risk", "delete", "remove", "critical", "warning"]
        if "LOW" in result["risk"] and any(word in ai_output.lower() for word in danger_keywords):
            result["risk"] = "MEDIUM (AI Flagged)"
            result["impact"] = "The AI Engine detected a threat pattern not found in standard rule libraries."
            result["solution"] = "Review the Detailed Explanation below before executing."
        # --- LOGIC UPGRADE END ---

        # Calculate score for metrics
        score = 90 if result["risk"] == "LOW" else (60 if "MEDIUM" in result["risk"] else 30)

        # 4. METRICS ROW
        m_col1, m_col2, m_col3 = st.columns(3)
        with m_col1:
            st.metric(label="RISK LEVEL", value=result["risk"])
        with m_col2:
            st.metric(label="CONFIDENCE", value=f"{score}%")
        with m_col3:
            st.metric(label="ENGINE", value="HYBRID V2.0")

        st.markdown("---")
        
        # 5. ANALYSIS DETAILS
        col_left, col_right = st.columns([2, 1])

        with col_left:
            st.markdown('<div class="threat-header">THREAT IMPACT</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="content-text">{result["impact"]}</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="mitigation-header">MITIGATION STRATEGY</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="content-text">{result["solution"]}</div>', unsafe_allow_html=True)

        with col_right:
            st.markdown('<div class="network-header">🌐 NETWORK VIEW</div>', unsafe_allow_html=True)
            # Ensure this URL is correct for the icon to show up
            # Replace the old st.image line with this:
            st.image("network.jpg", width=160)
            status_color = "#3fb950" if "LOW" in result["risk"] else "#ff7b72"
            st.markdown(f"<span style='color:{status_color}; font-weight:bold;'>SYSTEM STATUS: {result['risk']}</span>", unsafe_allow_html=True)

        # 6. AI EXPLANATION
        st.markdown("---")
        st.markdown('<div class="explanation-header">DETAILED EXPLANATION</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="ai-box">{ai_output}</div>', unsafe_allow_html=True)
        st.caption("💡 Tip: Use 'man <command>' to learn more about this command.")

# FOOTER
st.markdown("---")
st.caption("Terminal Security Intel // 2026")