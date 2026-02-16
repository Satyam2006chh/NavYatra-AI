"""
Streamlit Frontend — NavYatra AI
Premium dark-themed travel planning UI with bold typography.
"""

# Fix asyncio event loop for Windows + Python 3.12
import asyncio
import sys

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

import os
import uuid
import requests
import streamlit as st

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="NavYatra AI",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# CUSTOM CSS — Premium Obsidian Dark + Emerald/Cyan Accents
# ============================================================

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

    /* ═══════ GLOBAL ═══════ */
    .stApp {
        background: #09090b;
        font-family: 'Inter', sans-serif;
        color: #e4e4e7;
    }

    header[data-testid="stHeader"] {
        background: transparent;
    }

    /* ═══════ MARKDOWN — BOLD & READABLE ═══════ */
    .stMarkdown p, .stMarkdown li {
        color: #d4d4d8;
        font-weight: 600;
        font-size: 1.0rem;
        line-height: 1.8;
    }

    .stMarkdown strong, .stMarkdown b {
        color: #ffffff;
        font-weight: 800;
    }

    .stMarkdown h1 {
        color: #ffffff;
        font-weight: 900;
        font-size: 1.8rem;
    }

    .stMarkdown h2 {
        color: #f4f4f5;
        font-weight: 800;
        font-size: 1.5rem;
    }

    .stMarkdown h3 {
        color: #e4e4e7;
        font-weight: 700;
        font-size: 1.25rem;
    }

    .stMarkdown code {
        background: rgba(6, 182, 212, 0.1);
        color: #22d3ee;
        padding: 2px 6px;
        border-radius: 4px;
    }

    /* ═══════ HERO ═══════ */
    .hero-container {
        text-align: center;
        padding: 60px 20px 28px 20px;
    }

    .hero-badge {
        display: inline-block;
        padding: 6px 18px;
        border-radius: 50px;
        font-size: 0.7rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 2px;
        background: rgba(16, 185, 129, 0.1);
        color: #34d399;
        border: 1px solid rgba(16, 185, 129, 0.2);
        margin-bottom: 24px;
    }

    .hero-title {
        font-size: 3.8rem;
        font-weight: 900;
        color: #ffffff;
        letter-spacing: -1.5px;
        margin-bottom: 4px;
        line-height: 1.1;
    }

    .hero-title span {
        background: linear-gradient(135deg, #06b6d4, #10b981, #34d399);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-sub {
        font-size: 1.05rem;
        color: #71717a;
        font-weight: 500;
        margin-top: 8px;
        letter-spacing: 0.2px;
    }

    /* ═══════ FEATURES ═══════ */
    .features-grid {
        display: flex;
        justify-content: center;
        gap: 12px;
        flex-wrap: wrap;
        margin: 32px auto 16px auto;
        max-width: 700px;
    }

    .feat {
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 10px 20px;
        border-radius: 10px;
        font-size: 0.82rem;
        font-weight: 600;
        color: #a1a1aa;
        background: #18181b;
        border: 1px solid #27272a;
        transition: all 0.25s ease;
    }

    .feat:hover {
        border-color: #06b6d4;
        color: #e4e4e7;
        background: rgba(6, 182, 212, 0.04);
    }

    .feat-icon {
        font-size: 1.15rem;
    }

    /* ═══════ TECH TAGS ═══════ */
    .tech-bar {
        display: flex;
        justify-content: center;
        gap: 8px;
        flex-wrap: wrap;
        margin: 20px auto 40px auto;
    }

    .tech {
        padding: 4px 12px;
        border-radius: 5px;
        font-size: 0.65rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #06b6d4;
        background: rgba(6, 182, 212, 0.06);
        border: 1px solid rgba(6, 182, 212, 0.12);
    }

    /* ═══════ SECTION DIVIDERS ═══════ */
    hr {
        border: none !important;
        height: 1px !important;
        background: #27272a !important;
        margin: 28px 0 !important;
    }

    /* ═══════ INPUT ═══════ */
    .input-header {
        color: #a1a1aa;
        font-size: 0.85rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 10px;
    }

    .stTextArea textarea {
        background: #18181b !important;
        border: 2px solid #27272a !important;
        border-radius: 12px !important;
        color: #f4f4f5 !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.95rem !important;
        font-weight: 500 !important;
        padding: 16px !important;
    }

    .stTextArea textarea:focus {
        border-color: #06b6d4 !important;
        box-shadow: 0 0 0 3px rgba(6, 182, 212, 0.1) !important;
    }

    .stTextArea textarea::placeholder {
        color: #3f3f46 !important;
        font-weight: 500 !important;
    }

    /* ═══════ MAIN CTA BUTTON ═══════ */
    .stButton > button {
        background: linear-gradient(135deg, #06b6d4, #10b981) !important;
        color: #000000 !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 14px 40px !important;
        font-weight: 800 !important;
        font-size: 1rem !important;
        letter-spacing: 0.4px;
        transition: all 0.3s ease !important;
        width: 100%;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 12px 40px rgba(6, 182, 212, 0.2) !important;
    }

    /* ═══════ EXAMPLE PROMPT BUTTONS ═══════ */
    .stColumn .stButton > button {
        background: #18181b !important;
        border: 1px solid #27272a !important;
        color: #a1a1aa !important;
        font-weight: 600 !important;
        font-size: 0.78rem !important;
        padding: 10px 14px !important;
        border-radius: 10px !important;
    }

    .stColumn .stButton > button:hover {
        background: rgba(6, 182, 212, 0.06) !important;
        border-color: #06b6d4 !important;
        color: #22d3ee !important;
        transform: none !important;
        box-shadow: none !important;
    }

    /* ═══════ RESULT SECTION ═══════ */
    .result-banner {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 14px 22px;
        border-radius: 12px;
        background: rgba(16, 185, 129, 0.05);
        border: 1px solid rgba(16, 185, 129, 0.15);
        margin-bottom: 20px;
    }

    .result-banner-text {
        color: #34d399;
        font-weight: 700;
        font-size: 0.9rem;
    }

    /* ═══════ METRICS ═══════ */
    [data-testid="stMetric"] {
        background: #18181b;
        border: 1px solid #27272a;
        border-radius: 12px;
        padding: 16px;
    }

    [data-testid="stMetricLabel"] {
        color: #52525b !important;
        font-size: 0.7rem !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        letter-spacing: 0.8px;
    }

    [data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-size: 1.15rem !important;
        font-weight: 800 !important;
    }

    /* ═══════ TABS ═══════ */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        background: transparent;
        border-bottom: 2px solid #18181b;
        padding-bottom: 0;
    }

    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 8px 8px 0 0;
        color: #71717a;
        border: none;
        padding: 12px 22px;
        font-weight: 700;
        font-size: 0.85rem;
    }

    .stTabs [aria-selected="true"] {
        background: #18181b !important;
        color: #22d3ee !important;
        border-bottom: 2px solid #06b6d4 !important;
    }

    .stTabs [data-baseweb="tab-panel"] {
        background: #18181b;
        border-radius: 0 0 14px 14px;
        border: 1px solid #27272a;
        border-top: none;
        padding: 24px;
    }

    /* ═══════ SPINNER ═══════ */
    .stSpinner > div {
        color: #06b6d4 !important;
    }

    /* ═══════ ALERT / ERROR / INFO ═══════ */
    .stAlert {
        border-radius: 12px !important;
    }

    /* ═══════ FOOTER ═══════ */
    .site-footer {
        text-align: center;
        padding: 48px 0 24px 0;
        border-top: 1px solid #18181b;
        margin-top: 40px;
    }

    .footer-credit {
        color: #a1a1aa;
        font-weight: 700;
        font-size: 0.9rem;
        margin-bottom: 6px;
    }

    .footer-credit strong {
        color: #ffffff;
        font-weight: 800;
    }

    .footer-tech {
        color: #3f3f46;
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.5px;
    }

    /* ═══════ SCROLLBAR ═══════ */
    ::-webkit-scrollbar {
        width: 6px;
    }

    ::-webkit-scrollbar-track {
        background: #09090b;
    }

    ::-webkit-scrollbar-thumb {
        background: #27272a;
        border-radius: 3px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: #3f3f46;
    }
</style>
""", unsafe_allow_html=True)


# ============================================================
# HERO SECTION
# ============================================================

st.markdown("""
<div class="hero-container">
    <div class="hero-badge">✦ Multi-Agent AI System</div>
    <div class="hero-title">Nav<span>Yatra</span> AI</div>
    <div class="hero-sub">Intelligent Travel Planning, Powered by 6 Specialized AI Agents</div>
</div>
""", unsafe_allow_html=True)


# ============================================================
# FEATURES
# ============================================================

st.markdown("""
<div class="features-grid">
    <div class="feat"><span class="feat-icon">✈️</span> Flight Intelligence</div>
    <div class="feat"><span class="feat-icon">🏨</span> Hotel Discovery</div>
    <div class="feat"><span class="feat-icon">🌤️</span> Weather Analysis</div>
    <div class="feat"><span class="feat-icon">🎯</span> Attraction Research</div>
    <div class="feat"><span class="feat-icon">📋</span> Smart Itinerary</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="tech-bar">
    <span class="tech">LangGraph</span>
    <span class="tech">LangChain</span>
    <span class="tech">Cerebras LLM</span>
    <span class="tech">FastAPI</span>
    <span class="tech">Pydantic</span>
    <span class="tech">SQLite</span>
</div>
""", unsafe_allow_html=True)


# ============================================================
# EXAMPLE PROMPTS
# ============================================================

st.markdown('<p style="text-align:center; color:#52525b; font-size:0.8rem; font-weight:600; letter-spacing:0.5px;">TRY AN EXAMPLE</p>', unsafe_allow_html=True)

example_cols = st.columns(3)

EXAMPLES = [
    "Plan a 3-day trip from Delhi to Goa starting July 10, 2026 for 2 adults",
    "I want to travel from Mumbai to Manali for 5 days next month, I love adventure",
    "Weekend getaway from Bangalore to Coorg for 2 adults, budget-friendly"
]

for i, col in enumerate(example_cols):
    with col:
        if st.button(EXAMPLES[i], key=f"example_{i}", use_container_width=True):
            st.session_state["user_query"] = EXAMPLES[i]


# ============================================================
# INPUT SECTION
# ============================================================

st.markdown("---")

user_query = st.text_area(
    "🗺️  DESCRIBE YOUR TRIP",
    value=st.session_state.get("user_query", ""),
    height=90,
    placeholder="E.g.: Plan a 3-day trip from Delhi to Goa starting July 10, 2026 for 2 adults..."
)

col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    plan_button = st.button("🧭  Generate Travel Plan", use_container_width=True)


# ============================================================
# BACKEND CONFIG
# ============================================================

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")


# ============================================================
# PROCESS AND DISPLAY RESULTS
# ============================================================

if plan_button and user_query:

    if "thread_id" not in st.session_state:
        st.session_state["thread_id"] = str(uuid.uuid4())

    thread_id = st.session_state["thread_id"]

    st.markdown("---")

    with st.spinner("🧭 NavYatra AI is crafting your travel plan... This should take about 45 seconds."):
        try:
            response = requests.post(
                f"{BACKEND_URL}/api/plan",
                json={"query": user_query, "thread_id": thread_id},
                timeout=600
            )

            if response.status_code == 200:
                result = response.json()
                st.session_state["result"] = result
            else:
                st.error(f"❌ Error: {response.text}")

        except requests.exceptions.ConnectionError:
            st.error("⚠️ Cannot connect to backend. Make sure the FastAPI server is running on port 8000.")
            st.code("python -m uvicorn backend.main:app --reload --port 8000", language="bash")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")


# Display results
if "result" in st.session_state:
    result = st.session_state["result"]

    # Success banner
    st.markdown("""
    <div class="result-banner">
        <span style="font-size:1.2rem;">✅</span>
        <span class="result-banner-text">Travel Plan Generated Successfully</span>
    </div>
    """, unsafe_allow_html=True)

    # Trip Summary Metrics
    parsed = result.get("parsed_input", {})
    if parsed:
        mc = st.columns(4)
        with mc[0]:
            st.metric("From", parsed.get("origin_city", "—"))
        with mc[1]:
            st.metric("To", parsed.get("destination_city", "—"))
        with mc[2]:
            st.metric("Date", parsed.get("departure_date", "—"))
        with mc[3]:
            st.metric("Duration", f"{parsed.get('num_days', '—')} days")

    st.markdown("")  # spacer

    # Tabbed Results
    tabs = st.tabs(["✈️ Flights", "🏨 Hotels", "🌤️ Weather", "🎯 Attractions", "📋 Itinerary"])

    with tabs[0]:
        flight_data = result.get("flight_results", "")
        if flight_data:
            st.markdown(flight_data)
        else:
            st.info("🛫 No flight data was returned. The destination may not have a commercial airport. Check the itinerary tab for alternative travel suggestions.")

    with tabs[1]:
        hotel_data = result.get("hotel_results", "")
        if hotel_data:
            st.markdown(hotel_data)
        else:
            st.info("🏨 No hotel data was returned for this destination.")

    with tabs[2]:
        weather_data = result.get("weather_results", "")
        if weather_data:
            st.markdown(weather_data)
        else:
            st.info("🌤️ No weather data was returned for this destination.")

    with tabs[3]:
        research_data = result.get("research_results", "")
        if research_data:
            st.markdown(research_data)
        else:
            st.info("🎯 No attraction data was returned for this destination.")

    with tabs[4]:
        itinerary_data = result.get("itinerary", "")
        if itinerary_data:
            st.markdown(itinerary_data)
        else:
            st.info("📋 Itinerary could not be generated. Please try again.")

    # Session info
    st.markdown(
        f'<div style="text-align:center; color:#3f3f46; font-size:0.7rem; font-weight:600; margin-top:24px;">'
        f'Session: {result.get("thread_id", "—")} &nbsp;•&nbsp; Powered by Cerebras + LangGraph</div>',
        unsafe_allow_html=True
    )

elif plan_button and not user_query:
    st.warning("⚠️ Please enter a travel query first!")


# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="site-footer">
    <div class="footer-credit">Built by <strong>Satyam Chhabra</strong></div>
    <div class="footer-tech">Powered by LangGraph • LangChain • Cerebras • FastAPI • Streamlit</div>
</div>
""", unsafe_allow_html=True)
