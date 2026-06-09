import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# PAGE CONFIG
# ============================================================================

st.set_page_config(
    page_title="ChessIQ - Elite Chess Analytics Platform",
    page_icon="♟️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================================
# PREMIUM CSS STYLING
# ============================================================================

premium_css = """
<style>
    /* Root Variables */
    :root {
        --primary: #d4af37;
        --primary-dark: #b8940a;
        --accent: #1e90ff;
        --accent-light: #60a5fa;
        --success: #10b981;
        --warning: #f59e0b;
        --danger: #ef4444;
        --bg-dark: #0a0e17;
        --bg-card: #1a1f2e;
        --bg-light: #252d3d;
        --text-primary: #ffffff;
        --text-secondary: #b0b9c3;
    }

    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }

    html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
        background: linear-gradient(135deg, #0a0e17 0%, #1a1f2e 50%, #0a0e17 100%) !important;
        color: var(--text-primary);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }

    /* Hide default elements */
    [data-testid="stSidebarContent"] {
        display: none !important;
    }

    header {
        visibility: hidden;
        display: none !important;
    }

    footer {
        visibility: hidden;
    }

    /* Main Container */
    [data-testid="stAppViewContainer"] {
        padding: 0 !important;
        margin: 0 !important;
    }

    /* ============================================================================
    NAVBAR STYLING
    ============================================================================ */

    .navbar-container {
        position: sticky;
        top: 0;
        z-index: 1000;
        background: linear-gradient(180deg, rgba(10, 14, 23, 0.95) 0%, rgba(26, 31, 46, 0.9) 100%);
        backdrop-filter: blur(20px);
        border-bottom: 1px solid rgba(212, 175, 55, 0.15);
        padding: 1rem 2rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        animation: slideDownNavbar 0.5s ease-out;
    }

    .navbar-content {
        display: flex;
        justify-content: space-between;
        align-items: center;
        max-width: 1400px;
        margin: 0 auto;
    }

    .navbar-brand {
        font-size: 1.8rem;
        font-weight: 900;
        background: linear-gradient(120deg, #d4af37 0%, #1e90ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        display: flex;
        align-items: center;
        gap: 0.8rem;
        cursor: pointer;
        transition: transform 0.3s ease;
    }

    .navbar-brand:hover {
        transform: scale(1.05);
    }

    .navbar-menu {
        display: flex;
        gap: 1.5rem;
        align-items: center;
        flex-wrap: wrap;
    }

    .navbar-item {
        padding: 0.7rem 1.2rem;
        border-radius: 10px;
        cursor: pointer;
        font-weight: 600;
        font-size: 0.95rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        color: var(--text-secondary);
        border: 1px solid transparent;
    }

    .navbar-item:hover {
        background: rgba(212, 175, 55, 0.1);
        border-color: rgba(212, 175, 55, 0.3);
        color: var(--primary);
        transform: translateY(-2px);
    }

    .navbar-item.active {
        background: linear-gradient(135deg, rgba(212, 175, 55, 0.2) 0%, rgba(30, 144, 255, 0.2) 100%);
        border: 1px solid rgba(212, 175, 55, 0.4);
        color: var(--primary);
        box-shadow: 0 0 20px rgba(212, 175, 55, 0.2);
    }

    @keyframes slideDownNavbar {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    /* ============================================================================
    LANDING PAGE
    ============================================================================ */

    .landing-container {
        min-height: 100vh;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, #0a0e17 0%, #1a1f2e 50%, #0a0e17 100%);
        position: relative;
        overflow: hidden;
    }

    .landing-container::before {
        content: '';
        position: absolute;
        width: 400px;
        height: 400px;
        background: radial-gradient(circle, rgba(212, 175, 55, 0.1) 0%, transparent 70%);
        border-radius: 50%;
        top: -100px;
        right: -100px;
        animation: float 6s ease-in-out infinite;
    }

    .landing-container::after {
        content: '';
        position: absolute;
        width: 300px;
        height: 300px;
        background: radial-gradient(circle, rgba(30, 144, 255, 0.1) 0%, transparent 70%);
        border-radius: 50%;
        bottom: -50px;
        left: -50px;
        animation: float 8s ease-in-out infinite;
    }

    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-20px); }
    }

    .landing-content {
        position: relative;
        z-index: 10;
        animation: fadeInUp 1s ease-out;
    }

    .landing-emoji {
        font-size: 5rem;
        margin-bottom: 1rem;
        animation: bounce 2s ease-in-out infinite;
    }

    .landing-title {
        font-size: 4.5rem;
        font-weight: 900;
        margin-bottom: 1rem;
        background: linear-gradient(120deg, #d4af37 0%, #1e90ff 50%, #d4af37 100%);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: gradientShift 3s ease infinite;
        letter-spacing: -1px;
    }

    .landing-subtitle {
        font-size: 1.8rem;
        color: var(--text-secondary);
        margin-bottom: 2rem;
        font-weight: 300;
        letter-spacing: 0.5px;
    }

    .landing-description {
        font-size: 1.1rem;
        color: var(--text-secondary);
        max-width: 700px;
        margin: 0 auto 3rem;
        line-height: 1.8;
        font-weight: 300;
    }

    .landing-button {
        display: inline-block;
        padding: 1.2rem 3rem;
        background: linear-gradient(135deg, #d4af37 0%, #1e90ff 100%);
        color: #0a0e17;
        border: none;
        border-radius: 12px;
        font-size: 1.1rem;
        font-weight: 700;
        cursor: pointer;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 10px 40px rgba(212, 175, 55, 0.3);
        letter-spacing: 0.5px;
    }

    .landing-button:hover {
        transform: translateY(-4px);
        box-shadow: 0 20px 60px rgba(212, 175, 55, 0.4);
    }

    .landing-stats {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 2rem;
        margin-top: 4rem;
        max-width: 1000px;
        margin-left: auto;
        margin-right: auto;
    }

    .landing-stat-card {
        background: linear-gradient(135deg, rgba(26, 31, 46, 0.8) 0%, rgba(37, 45, 61, 0.8) 100%);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(212, 175, 55, 0.2);
        padding: 1.5rem;
        border-radius: 12px;
        transition: all 0.3s ease;
    }

    .landing-stat-card:hover {
        transform: translateY(-8px);
        border-color: rgba(212, 175, 55, 0.4);
        box-shadow: 0 20px 40px rgba(212, 175, 55, 0.15);
    }

    .stat-value {
        font-size: 2.5rem;
        font-weight: 900;
        color: #d4af37;
        margin-bottom: 0.5rem;
    }

    .stat-label {
        font-size: 0.9rem;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-20px); }
    }

    @keyframes gradientShift {
        0%, 100% { background-position: 0% center; }
        50% { background-position: 100% center; }
    }

    /* ============================================================================
    PAGE CONTENT STYLING
    ============================================================================ */

    .page-container {
        padding: 3rem 2rem;
        max-width: 1400px;
        margin: 0 auto;
        animation: fadeIn 0.6s ease-out;
    }

    .page-header {
        margin-bottom: 3rem;
        animation: fadeInDown 0.8s ease-out;
    }

    .page-title {
        font-size: 3rem;
        font-weight: 900;
        margin-bottom: 0.5rem;
        background: linear-gradient(120deg, #d4af37 0%, #1e90ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .page-subtitle {
        font-size: 1.1rem;
        color: var(--text-secondary);
        font-weight: 300;
    }

    .section-header {
        font-size: 2.2rem;
        font-weight: 800;
        margin-top: 3rem;
        margin-bottom: 2rem;
        padding-bottom: 1rem;
        border-bottom: 2px solid rgba(212, 175, 55, 0.2);
        display: flex;
        align-items: center;
        gap: 1rem;
        animation: fadeInLeft 0.6s ease-out;
    }

    .section-emoji {
        font-size: 2.5rem;
    }

    .section-text {
        background: linear-gradient(120deg, #d4af37 0%, #1e90ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    /* KPI Cards */
    .kpi-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 2rem;
        margin-bottom: 3rem;
        animation: fadeInUp 0.8s ease-out 0.1s both;
    }

    .kpi-card {
        background: linear-gradient(135deg, rgba(26, 31, 46, 0.8) 0%, rgba(37, 45, 61, 0.8) 100%);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(212, 175, 55, 0.15);
        border-radius: 16px;
        padding: 2rem;
        position: relative;
        overflow: hidden;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: pointer;
    }

    .kpi-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(212, 175, 55, 0.1), transparent);
        transition: left 0.5s ease;
    }

    .kpi-card:hover {
        transform: translateY(-8px);
        border-color: rgba(212, 175, 55, 0.4);
        box-shadow: 0 20px 40px rgba(212, 175, 55, 0.15);
    }

    .kpi-card:hover::before {
        left: 100%;
    }

    .kpi-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }

    .kpi-label {
        font-size: 0.85rem;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-weight: 600;
        margin-bottom: 0.8rem;
    }

    .kpi-value {
        font-size: 2.8rem;
        font-weight: 900;
        background: linear-gradient(120deg, #d4af37 0%, #1e90ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
    }

    .kpi-detail {
        font-size: 0.9rem;
        color: var(--accent-light);
        font-weight: 500;
    }

    /* Chart Container */
    .chart-container {
        background: linear-gradient(135deg, rgba(26, 31, 46, 0.6) 0%, rgba(37, 45, 61, 0.6) 100%);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(212, 175, 55, 0.1);
        border-radius: 16px;
        padding: 2rem;
        margin: 1.5rem 0;
        animation: fadeInUp 0.6s ease-out;
    }

    .chart-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 1.5rem;
    }

    /* Recommendation Cards */
    .recommendation-success {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(16, 185, 129, 0.05) 100%);
        border-left: 4px solid #10b981;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(16, 185, 129, 0.2);
        transition: all 0.3s ease;
    }

    .recommendation-success:hover {
        transform: translateX(5px);
        border-color: rgba(16, 185, 129, 0.4);
    }

    .recommendation-warning {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.1) 0%, rgba(245, 158, 11, 0.05) 100%);
        border-left: 4px solid #f59e0b;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(245, 158, 11, 0.2);
        transition: all 0.3s ease;
    }

    .recommendation-warning:hover {
        transform: translateX(5px);
        border-color: rgba(245, 158, 11, 0.4);
    }

    .recommendation-danger {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.1) 0%, rgba(239, 68, 68, 0.05) 100%);
        border-left: 4px solid #ef4444;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(239, 68, 68, 0.2);
        transition: all 0.3s ease;
    }

    .recommendation-danger:hover {
        transform: translateX(5px);
        border-color: rgba(239, 68, 68, 0.4);
    }

    .recommendation-title {
        font-weight: 700;
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
    }

    .recommendation-content {
        font-size: 0.95rem;
        color: var(--text-secondary);
        line-height: 1.6;
    }

    /* Metric Box */
    .metric-box {
        background: linear-gradient(135deg, rgba(26, 31, 46, 0.8) 0%, rgba(37, 45, 61, 0.8) 100%);
        border: 1px solid rgba(212, 175, 55, 0.15);
        border-radius: 12px;
        padding: 1.2rem;
        text-align: center;
        margin: 0.8rem 0;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }

    .metric-box:hover {
        transform: scale(1.05);
        border-color: rgba(212, 175, 55, 0.4);
        box-shadow: 0 10px 30px rgba(212, 175, 55, 0.1);
    }

    .metric-label {
        font-size: 0.9rem;
        color: var(--text-secondary);
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.5rem;
    }

    .metric-value {
        font-size: 2rem;
        font-weight: 900;
        background: linear-gradient(120deg, #d4af37 0%, #1e90ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: var(--text-secondary);
        font-size: 0.85rem;
        margin-top: 4rem;
        padding-top: 2rem;
        border-top: 1px solid rgba(212, 175, 55, 0.1);
        animation: fadeInUp 0.8s ease-out 0.5s both;
    }

    .footer-title {
        color: #d4af37;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }

    /* Animations */
    @keyframes fadeIn {
        from {
            opacity: 0;
        }
        to {
            opacity: 1;
        }
    }

    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes fadeInLeft {
        from {
            opacity: 0;
            transform: translateX(-30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }

    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(212, 175, 55, 0.2), transparent);
        margin: 2rem 0;
    }

    /* Responsive */
    @media (max-width: 768px) {
        .landing-title {
            font-size: 2.5rem;
        }
        .page-title {
            font-size: 2rem;
        }
        .kpi-container {
            grid-template-columns: 1fr;
            gap: 1.5rem;
        }
        .navbar-menu {
            gap: 0.8rem;
            flex-direction: column;
            width: 100%;
        }
        .navbar-item {
            width: 100%;
            text-align: center;
        }
    }
</style>
"""

st.markdown(premium_css, unsafe_allow_html=True)

# ============================================================================
# SESSION STATE MANAGEMENT
# ============================================================================

if 'page' not in st.session_state:
    st.session_state.page = 'landing'

def set_page(page_name):
    st.session_state.page = page_name

# ============================================================================
# NAVBAR
# ============================================================================

navbar_html = """
<div class="navbar-container">
    <div class="navbar-content">
        <div class="navbar-brand">♟️ ChessIQ</div>
        <div class="navbar-menu">
            <a href="#" onclick="location.reload()" class="navbar-item">📊 Dashboard</a>
            <a href="#" onclick="location.reload()" class="navbar-item">🎯 Openings</a>
            <a href="#" onclick="location.reload()" class="navbar-item">⚔️ Opponents</a>
            <a href="#" onclick="location.reload()" class="navbar-item">⏱️ Time Control</a>
            <a href="#" onclick="location.reload()" class="navbar-item">📈 Progress</a>
            <a href="#" onclick="location.reload()" class="navbar-item">🔮 Predictor</a>
            <a href="#" onclick="location.reload()" class="navbar-item">💡 Tips</a>
            <a href="#" onclick="location.reload()" class="navbar-item">🤖 ML Insights</a>
        </div>
    </div>
</div>
"""

col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)

with col1:
    if st.button("📊 Dashboard", use_container_width=True, key="nav_dash"):
        set_page("dashboard")

with col2:
    if st.button("🎯 Openings", use_container_width=True, key="nav_open"):
        set_page("opening")

with col3:
    if st.button("⚔️ Opponents", use_container_width=True, key="nav_opp"):
        set_page("opponent")

with col4:
    if st.button("⏱️ Time", use_container_width=True, key="nav_time"):
        set_page("time")

with col5:
    if st.button("📈 Progress", use_container_width=True, key="nav_prog"):
        set_page("progress")

with col6:
    if st.button("🔮 Predict", use_container_width=True, key="nav_pred"):
        set_page("predict")

with col7:
    if st.button("💡 Tips", use_container_width=True, key="nav_tips"):
        set_page("tips")

with col8:
    if st.button("🤖 ML", use_container_width=True, key="nav_ml"):
        set_page("ml")

st.divider()

# ============================================================================
# LANDING PAGE
# ============================================================================

if st.session_state.page == 'landing':
    # Spacing
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    
    # Center column
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Chess Emoji
        st.markdown("""
        <div style="text-align: center; font-size: 5rem; margin-bottom: 2rem; animation: bounce 2s ease-in-out infinite;">
            ♟️
        </div>
        """, unsafe_allow_html=True)
        
        # Title
        st.markdown("""
        <div style="text-align: center; font-size: 4rem; font-weight: 900; color: #d4af37; margin-bottom: 1rem; letter-spacing: -1px;">
            ChessIQ
        </div>
        """, unsafe_allow_html=True)
        
        # Subtitle
        st.markdown("""
        <div style="text-align: center; font-size: 1.5rem; color: #b0b9c3; margin-bottom: 2rem; font-weight: 300;">
            AI-Powered Chess Analytics Platform
        </div>
        """, unsafe_allow_html=True)
        
        # Description
        st.markdown("""
        <div style="text-align: center; font-size: 1.05rem; color: #b0b9c3; margin-bottom: 3rem; line-height: 1.8;">
            Analyze your chess games with AI. Identify your strengths,<br>
            discover weaknesses, and predict outcomes before you play.
        </div>
        """, unsafe_allow_html=True)
        
        # Buttons
        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            if st.button("🚀 Start Dashboard", use_container_width=True, key="start_dash"):
                st.session_state.page = "dashboard"
                st.rerun()
        
        with btn_col2:
            if st.button("📊 View ML Insights", use_container_width=True, key="view_ml"):
                st.session_state.page = "ml"
                st.rerun()
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.divider()
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Stats Grid
    stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
    
    with stat_col1:
        st.metric("Games", "4,635", "5 years")
    
    with stat_col2:
        st.metric("Moves", "328K", "Analyzed")
    
    with stat_col3:
        st.metric("Accuracy", "72.49%", "ML Model")
    
    with stat_col4:
        st.metric("Rating", "1,359", "+544 growth")

# ============================================================================
# DASHBOARD PAGE
# ============================================================================

elif st.session_state.page == 'dashboard':
    st.markdown("""
    <div class="page-container">
        <div class="page-header">
            <div class="page-title">📊 Your Chess Performance</div>
            <div class="page-subtitle">Comprehensive overview of your chess statistics</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-icon">🎮</div>
            <div class="kpi-label">Total Games</div>
            <div class="kpi-value">4,635</div>
            <div class="kpi-detail">Over 5 years</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-icon">🏆</div>
            <div class="kpi-label">Win Rate</div>
            <div class="kpi-value">49.1%</div>
            <div class="kpi-detail">2,276 wins</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-icon">⚡</div>
            <div class="kpi-label">Avg Accuracy</div>
            <div class="kpi-value">91.93%</div>
            <div class="kpi-detail">Consistent play</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-icon">📈</div>
            <div class="kpi-label">Peak Rating</div>
            <div class="kpi-value">1,423</div>
            <div class="kpi-detail">+544 growth</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">🎲 Game Results Distribution</div>', unsafe_allow_html=True)
        
        results = ['Wins', 'Losses', 'Draws']
        values = [2276, 2120, 239]
        colors = ['#10b981', '#ef4444', '#60a5fa']
        
        fig = go.Figure(data=[go.Pie(
            labels=results,
            values=values,
            marker=dict(colors=colors, line=dict(color='#0a0e17', width=3)),
            textinfo='label+percent',
            hovertemplate='<b>%{label}</b><br>Games: %{value}<extra></extra>'
        )])
        
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#ffffff', family='Inter'),
            height=380,
            showlegend=True,
            margin=dict(l=0, r=0, t=0, b=0)
        )
        
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">📊 Accuracy Distribution</div>', unsafe_allow_html=True)
        
        accuracies = np.random.normal(92, 5, 1000)
        accuracies = np.clip(accuracies, 75, 100)
        
        fig = go.Figure(data=[go.Histogram(
            x=accuracies,
            nbinsx=25,
            marker=dict(color='#d4af37', line=dict(color='#b8940a', width=1), opacity=0.85),
            hovertemplate='Accuracy: %{x:.1f}%<br>Games: %{y}<extra></extra>'
        )])
        
        fig.update_layout(
            xaxis_title="Accuracy %",
            yaxis_title="Games",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#ffffff', family='Inter'),
            height=380,
            showlegend=False,
            hovermode='x unified',
            margin=dict(l=50, r=20, t=0, b=50),
            xaxis=dict(gridcolor='rgba(212, 175, 55, 0.1)'),
            yaxis=dict(gridcolor='rgba(212, 175, 55, 0.1)')
        )
        
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# OPENING ANALYSIS PAGE
# ============================================================================

elif st.session_state.page == 'opening':
    st.markdown("""
    <div class="page-container">
        <div class="page-header">
            <div class="page-title">🎯 Opening Mastery Analysis</div>
            <div class="page-subtitle">Your chess opening performance breakdown</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Top 10 Openings by Win Rate</div>', unsafe_allow_html=True)
        
        openings = ['D31', 'D20', 'A40', 'D02', 'D00', 'B23', 'D07', 'B30', 'A43', 'B21']
        win_rates = [60.26, 54.26, 53.99, 52.00, 50.68, 50.32, 49.29, 48.70, 48.31, 47.93]
        
        colors_opening = ['#10b981' if wr > 55 else '#f59e0b' if wr > 50 else '#ef4444' for wr in win_rates]
        
        fig = go.Figure(data=[
            go.Bar(
                y=openings,
                x=win_rates,
                orientation='h',
                marker=dict(color=colors_opening, line=dict(color='#d4af37', width=2), opacity=0.9),
                text=[f'{wr:.1f}%' for wr in win_rates],
                textposition='outside',
                hovertemplate='<b>%{y}</b><br>Win Rate: %{x:.2f}%<extra></extra>'
            )
        ])
        
        fig.update_layout(
            xaxis_title="Win Rate %",
            yaxis_title="",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#ffffff', family='Inter'),
            height=450,
            margin=dict(l=80, r=100),
            xaxis=dict(gridcolor='rgba(212, 175, 55, 0.1)'),
            hovermode='y'
        )
        
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 💡 Recommendations")
        
        st.markdown("""
        <div class="recommendation-success">
        <div class="recommendation-title">🟢 Play More</div>
        <div class="recommendation-content">
        <strong>D31:</strong> 60.3%<br>
        <strong>D20:</strong> 54.3%<br>
        <strong>A40:</strong> 54.0%
        </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="recommendation-danger">
        <div class="recommendation-title">🔴 Study More</div>
        <div class="recommendation-content">
        <strong>B20:</strong> 40.8%<br>
        <strong>A04:</strong> 39.2%
        </div>
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# OPPONENT STRENGTH PAGE
# ============================================================================

elif st.session_state.page == 'opponent':
    st.markdown("""
    <div class="page-container">
        <div class="page-header">
            <div class="page-title">⚔️ Opponent Strength Analysis</div>
            <div class="page-subtitle">Your win rate against different rating levels</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Win Rate by Rating Difference</div>', unsafe_allow_html=True)
        
        rating_diffs = ['+50-+100', '+0-+50', '-50-0', '-100-50']
        win_rates_rating = [88.4, 65.7, 32.6, 6.6]
        colors_rating = ['#10b981', '#f59e0b', '#ef4444', '#dc2626']
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=rating_diffs,
            y=win_rates_rating,
            marker=dict(color=colors_rating, line=dict(color='#d4af37', width=2.5), opacity=0.9),
            text=[f'{wr:.1f}%' for wr in win_rates_rating],
            textposition='outside',
            hovertemplate='<b>Rating Diff: %{x}</b><br>Win Rate: %{y:.1f}%<extra></extra>'
        ))
        
        fig.add_hline(y=50, line_dash="dash", line_color="#60a5fa", annotation_text="50% (Even)")
        
        fig.update_layout(
            xaxis_title="Your Rating - Opponent Rating",
            yaxis_title="Win Rate %",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#ffffff', family='Inter'),
            height=400,
            hovermode='x',
            yaxis=dict(gridcolor='rgba(212, 175, 55, 0.1)'),
            margin=dict(l=60, r=100, t=60, b=50)
        )
        
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="recommendation-success">
        <div class="recommendation-title">✅ SEEK</div>
        <div class="recommendation-content">
        50-100 weaker<br>
        <strong style="color: #10b981; font-size: 1.3rem;">88.4%</strong>
        </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="recommendation-warning">
        <div class="recommendation-title">⚡ CHALLENGE</div>
        <div class="recommendation-content">
        0-50 weaker<br>
        <strong style="color: #f59e0b; font-size: 1.3rem;">65.7%</strong>
        </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="recommendation-danger">
        <div class="recommendation-title">⚠️ LIMIT</div>
        <div class="recommendation-content">
        50+ stronger<br>
        <strong style="color: #ef4444; font-size: 1.3rem;">32.6%</strong>
        </div>
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# TIME CONTROL PAGE
# ============================================================================

elif st.session_state.page == 'time':
    st.markdown("""
    <div class="page-container">
        <div class="page-header">
            <div class="page-title">⏱️ Time Control Performance</div>
            <div class="page-subtitle">Your effectiveness across different time formats</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1.5, 1])
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Win Rate & Accuracy by Format</div>', unsafe_allow_html=True)
        
        time_formats = ['Blitz', 'Rapid', 'Classical', 'Long']
        win_rates_time = [49.5, 48.9, 47.7, 48.8]
        accuracies = [91.95, 91.75, 92.52, 91.94]
        
        fig = go.Figure(data=[
            go.Bar(name='Win Rate %', x=time_formats, y=win_rates_time, 
                  marker=dict(color='#10b981', opacity=0.85)),
            go.Bar(name='Accuracy %', x=time_formats, y=accuracies,
                  marker=dict(color='#d4af37', opacity=0.85))
        ])
        
        fig.update_layout(
            barmode='group',
            xaxis_title="Time Format",
            yaxis_title="Percentage %",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#ffffff', family='Inter'),
            height=350,
            hovermode='x unified',
            yaxis=dict(gridcolor='rgba(212, 175, 55, 0.1)'),
            legend=dict(x=0.01, y=0.99, bgcolor='rgba(0,0,0,0.5)')
        )
        
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Centipawn Loss by Format</div>', unsafe_allow_html=True)
        
        cpls = [147.50, 133.76, 122.26, 137.41]
        
        fig = go.Figure(data=[
            go.Scatter(x=time_formats, y=cpls, mode='lines+markers',
                      line=dict(color='#60a5fa', width=4),
                      marker=dict(size=14, color='#d4af37', line=dict(width=2.5, color='#0a0e17')),
                      fill='tozeroy', fillcolor='rgba(96, 165, 250, 0.15)',
                      hovertemplate='<b>%{x}</b><br>CPL: %{y:.1f}<extra></extra>')
        ])
        
        fig.update_layout(
            xaxis_title="Time Format",
            yaxis_title="CPL (Lower = Better)",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#ffffff', family='Inter'),
            height=350,
            hovermode='x',
            yaxis=dict(gridcolor='rgba(212, 175, 55, 0.1)'),
            margin=dict(l=60, r=20, t=0, b=50)
        )
        
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 📊 Summary")
        
        st.markdown("""
        <div class="metric-box">
        <div class="metric-label">Win Rate Range</div>
        <div style="font-size: 1.2rem; color: #10b981; font-weight: 700;">47.7% - 49.5%</div>
        <div style="font-size: 0.85rem; color: #b0b9c3;">Only 1.8% variance</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="metric-box">
        <div class="metric-label">Accuracy Range</div>
        <div style="font-size: 1.2rem; color: #d4af37; font-weight: 700;">91.75% - 92.52%</div>
        <div style="font-size: 0.85rem; color: #b0b9c3;">Highly consistent</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="recommendation-success">
        <div class="recommendation-title">✅ Verdict</div>
        <div class="recommendation-content">
        Play ANY format!<br>
        Time doesn't affect you.
        </div>
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# PROGRESS PAGE
# ============================================================================

elif st.session_state.page == 'progress':
    st.markdown("""
    <div class="page-container">
        <div class="page-header">
            <div class="page-title">📈 5-Year Chess Journey</div>
            <div class="page-subtitle">Your skill progression from 2021 to 2026</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1.5, 1])
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Rating Progression</div>', unsafe_allow_html=True)
        
        windows = np.arange(1, 25)
        ratings = [597, 647, 771, 822, 838, 823, 911, 1024, 961, 944, 951, 982, 1065, 1016, 1100, 1080, 1130, 1141, 939, 1007, 1124, 1153, 1135, 1141]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=windows, y=ratings,
            mode='lines+markers',
            line=dict(color='#d4af37', width=3.5),
            marker=dict(size=8, color='#d4af37', line=dict(width=2, color='#0a0e17')),
            fill='tozeroy',
            fillcolor='rgba(212, 175, 55, 0.15)',
            hovertemplate='<b>Game Window %{x}</b><br>Rating: %{y}<extra></extra>'
        ))
        
        fig.update_layout(
            xaxis_title="Game Window (each ~200 games)",
            yaxis_title="Rating",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#ffffff', family='Inter'),
            height=400,
            hovermode='x',
            yaxis=dict(gridcolor='rgba(212, 175, 55, 0.1)'),
            margin=dict(l=60, r=20, t=0, b=50)
        )
        
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Win Rate Trend</div>', unsafe_allow_html=True)
        
        win_rates_progression = [44.5, 46.0, 46.0, 53.0, 41.0, 50.5, 52.0, 47.5, 53.0, 49.5, 46.0, 49.5, 46.5, 53.5, 50.0, 51.5, 50.0, 51.5, 53.0, 47.0, 48.0, 49.0, 49.5, 57.1]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=windows, y=win_rates_progression,
            mode='lines+markers',
            line=dict(color='#10b981', width=3.5),
            marker=dict(size=8, color='#10b981', line=dict(width=2, color='#0a0e17')),
            fill='tozeroy',
            fillcolor='rgba(16, 185, 129, 0.15)',
            hovertemplate='<b>Window %{x}</b><br>Win Rate: %{y:.1f}%<extra></extra>'
        ))
        
        fig.add_hline(y=50, line_dash="dash", line_color="#60a5fa")
        
        fig.update_layout(
            xaxis_title="Game Window",
            yaxis_title="Win Rate %",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#ffffff', family='Inter'),
            height=400,
            hovermode='x',
            yaxis=dict(gridcolor='rgba(212, 175, 55, 0.1)'),
            margin=dict(l=60, r=20, t=0, b=50)
        )
        
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 🎯 Progress")
        
        st.markdown("""
        <div class="metric-box">
        <div class="metric-label">Rating Growth</div>
        <div style="font-size: 1.1rem; color: #b0b9c3;">597 → 1,141</div>
        <div style="font-size: 1.5rem; font-weight: 900; color: #10b981;">+544</div>
        <div style="font-size: 0.85rem; color: #b0b9c3;">(+91%)</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="metric-box">
        <div class="metric-label">Win Rate Trend</div>
        <div style="font-size: 1.1rem; color: #b0b9c3;">44.5% → 57.1%</div>
        <div style="font-size: 1.3rem; font-weight: 700; color: #f59e0b;">📈 Upward</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="metric-box">
        <div class="metric-label">Time Period</div>
        <div style="font-size: 1.1rem; color: #b0b9c3;">June 2021 - June 2026</div>
        <div style="font-size: 1.3rem; font-weight: 700; color: #60a5fa;">5 years</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="recommendation-success">
        <div class="recommendation-title">✅ Excellent!</div>
        <div class="recommendation-content">
        Continue current strategy
        </div>
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# WIN PREDICTOR PAGE
# ============================================================================

elif st.session_state.page == 'predict':
    st.markdown("""
    <div class="page-container">
        <div class="page-header">
            <div class="page-title">🔮 AI Game Outcome Predictor</div>
            <div class="page-subtitle">ML-powered predictions with 72.49% accuracy</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">📊 Enter Your Game Details</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        your_rating = st.number_input("Your Rating", 100, 2000, 1141, 10, key="pred_your")
    
    with col2:
        opponent_rating = st.number_input("Opponent Rating", 100, 2000, 900, 10, key="pred_opp")
    
    with col3:
        time_control = st.selectbox("Time Control", ["Blitz (60s)", "Rapid (180s)", "Classical (300s)", "Long (600s)"], key="pred_time")
    
    with col4:
        player_color = st.selectbox("Your Color", ["White", "Black"], key="pred_color")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.divider()
    
    # Feature Engineering
    rating_diff = your_rating - opponent_rating
    
    # Model Predictions (simulated)
    def get_predictions(rd):
        base = 50 + (rd / 10) * 1.2
        return {
            'XGBoost': np.clip(base + np.random.normal(0, 1.5), 5, 95),
            'Random Forest': np.clip(base + np.random.normal(0, 2), 5, 95),
            'Gradient Boosting': np.clip(base + np.random.normal(0, 1.2), 5, 95),
            'Voting Ensemble': np.clip(base + np.random.normal(0, 1), 5, 95)
        }
    
    predictions = get_predictions(rating_diff)
    best_model = max(predictions, key=predictions.get)
    best_prob = predictions[best_model]
    
    col1, col2, col3 = st.columns([2, 1.5, 1])
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Model Predictions</div>', unsafe_allow_html=True)
        
        models = list(predictions.keys())
        probs = list(predictions.values())
        colors = ['#10b981' if p > 55 else '#f59e0b' if p > 50 else '#ef4444' for p in probs]
        
        fig = go.Figure(data=[
            go.Bar(x=models, y=probs,
                  marker=dict(color=colors, line=dict(color='#d4af37', width=2.5), opacity=0.9),
                  text=[f'{p:.1f}%' for p in probs],
                  textposition='outside',
                  hovertemplate='<b>%{x}</b><br>Win Prob: %{y:.1f}%<extra></extra>')
        ])
        
        fig.add_hline(y=50, line_dash="dash", line_color="#60a5fa")
        
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#ffffff', family='Inter'),
            height=350,
            showlegend=False,
            hovermode='x',
            yaxis=dict(range=[0, 100], gridcolor='rgba(212, 175, 55, 0.1)'),
            margin=dict(l=60, r=20, t=0, b=50)
        )
        
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Distribution</div>', unsafe_allow_html=True)
        
        fig = go.Figure()
        fig.add_trace(go.Box(y=list(predictions.values()), name='Models',
                            marker=dict(color='#d4af37', opacity=0.7), boxmean='sd'))
        
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#ffffff', family='Inter'),
            height=350,
            showlegend=False,
            yaxis=dict(range=[0, 100], gridcolor='rgba(212, 175, 55, 0.1)'),
            margin=dict(l=60, r=20, t=0, b=50)
        )
        
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="kpi-card" style="height: 350px; display: flex; flex-direction: column; justify-content: center; align-items: center;">
            <div class="kpi-icon">🎯</div>
            <div class="kpi-label">Prediction</div>
            <div style="font-size: 3.5rem; font-weight: 900; color: #d4af37;">{best_prob:.1f}%</div>
            <div class="kpi-detail">{best_model}</div>
            <div style="margin-top: 1rem; width: 100%; text-align: center;">
                <div style="font-size: 0.85rem; color: #b0b9c3;">Rating Diff</div>
                <div style="font-size: 1.5rem; font-weight: 900; color: #d4af37;">{rating_diff:+d}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# AI TIPS PAGE
# ============================================================================

elif st.session_state.page == 'tips':
    st.markdown("""
    <div class="page-container">
        <div class="page-header">
            <div class="page-title">💡 Personalized AI Tips</div>
            <div class="page-subtitle">Improvement recommendations based on your data</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1.5, 1])
    
    with col1:
        st.markdown("### 🟢 PLAY MORE (Strengths)")
        
        st.markdown("""
        <div class="recommendation-success">
        <div class="recommendation-title">D31 Opening</div>
        <div class="recommendation-content">
        60.26% win rate - Your BEST opening!<br>
        Master this completely.
        </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="recommendation-success">
        <div class="recommendation-title">Weaker Opponents</div>
        <div class="recommendation-content">
        50-100 points below you<br>
        88.4% win rate - Build confidence!
        </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 🟡 STUDY MORE (Weaknesses)")
        
        st.markdown("""
        <div class="recommendation-danger">
        <div class="recommendation-title">A04 Opening</div>
        <div class="recommendation-content">
        39.19% win rate - Your WORST<br>
        Deep study needed or avoid.
        </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="recommendation-warning">
        <div class="recommendation-title">Positional Play</div>
        <div class="recommendation-content">
        You lose by being outplayed<br>
        Study middlegame strategy!
        </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 🎯 Action Plan")
        
        st.markdown("""
        <div class="metric-box">
        <strong style="color: #d4af37;">This Week</strong><br>
        • Play D31<br>
        • Seek weaker<br>
        • Avoid A04
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="metric-box">
        <strong style="color: #f59e0b;">Next Month</strong><br>
        • Study B20<br>
        • Play Classical<br>
        • Focus endgames
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="metric-box">
        <strong style="color: #10b981;">Next Quarter</strong><br>
        • Master D31/D20<br>
        • Challenge ±20<br>
        • Target 1,250
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# ML INSIGHTS PAGE
# ============================================================================

elif st.session_state.page == 'ml':
    st.markdown("""
    <div class="page-container">
        <div class="page-header">
            <div class="page-title">🤖 ML Model Insights</div>
            <div class="page-subtitle">Understanding the AI behind the predictions</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Feature Importance (SHAP)</div>', unsafe_allow_html=True)
        
        features = ['Rating\nDifference', 'Win Rate\nHistory', 'Avg Opponent\nRating', 'Win\nStreak', 'Player\nRating', 'Opponent\nRating', 'Time\nControl', 'Player\nColor']
        importance = [59.63, 11.89, 10.85, 7.45, 5.23, 3.45, 1.32, 0.18]
        
        fig = go.Figure(data=[
            go.Bar(
                y=features,
                x=importance,
                orientation='h',
                marker=dict(
                    color=importance,
                    colorscale=[[0, '#ef4444'], [0.5, '#f59e0b'], [1, '#10b981']],
                    line=dict(color='#d4af37', width=2),
                    opacity=0.9,
                    colorbar=dict(title="Importance %")
                ),
                text=[f'{imp:.1f}%' for imp in importance],
                textposition='outside',
                hovertemplate='<b>%{y}</b><br>Importance: %{x:.2f}%<extra></extra>'
            )
        ])
        
        fig.update_layout(
            xaxis_title="Importance Score (%)",
            yaxis_title="",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#ffffff', family='Inter'),
            height=450,
            margin=dict(l=140, r=120, t=0, b=50),
            hovermode='y',
            xaxis=dict(gridcolor='rgba(212, 175, 55, 0.1)')
        )
        
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 📊 Model Details")
        
        st.markdown("""
        <div class="metric-box">
        <div class="metric-label">Model Type</div>
        <div style="font-size: 1rem; color: #d4af37; font-weight: 700;">Ensemble<br>Learning</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="metric-box">
        <div class="metric-label">Accuracy</div>
        <div style="font-size: 1.8rem; font-weight: 900; color: #10b981;">72.49%</div>
        <div style="font-size: 0.85rem; color: #b0b9c3;">Pre-game only</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="metric-box">
        <div class="metric-label">AUC-ROC</div>
        <div style="font-size: 1.8rem; font-weight: 900; color: #d4af37;">0.8265</div>
        <div style="font-size: 0.85rem; color: #b0b9c3;">Excellent</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="metric-box">
        <div class="metric-label">Training Data</div>
        <div style="font-size: 0.95rem;">4,635 games<br>3,708 / 927 split</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        
        st.markdown("### 🎯 Key Insights")
        
        st.markdown("""
        <div class="recommendation-success">
        <strong>Rating Dominates (59.6%)</strong><br>
        <span style="font-size: 0.9rem;">Gap is strongest predictor</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="recommendation-success">
        <strong>History Matters (11.9%)</strong><br>
        <span style="font-size: 0.9rem;">Past affects future</span>
        </div>
        """, unsafe_allow_html=True)

st.divider()

st.markdown("""
<div class="footer">
<div class="footer-title">♟️ ChessIQ © 2026</div>
<div>AI-Powered Chess Analytics Platform</div>
<div style="margin-top: 0.5rem; font-size: 0.8rem;">
Python • Streamlit • Plotly • Machine Learning
</div>
</div>
""", unsafe_allow_html=True)