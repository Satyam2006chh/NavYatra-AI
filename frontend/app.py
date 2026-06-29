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
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS — Premium Dark Theme
# ============================================================

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&display=swap');

    /* ═══════ GLOBAL & ANIMATED BACKGROUND (PREMIUM DARK) ═══════ */
    .stApp {
        background: linear-gradient(-45deg, #030712, #111827, #1e293b, #0f172a);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
        font-family: 'Outfit', sans-serif;
        color: #e2e8f0;
    }

    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    header[data-testid="stHeader"] {
        background: transparent;
    }

    /* ═══════ MARKDOWN ═══════ */
    .stMarkdown p, .stMarkdown li {
        color: #cbd5e1;
        font-weight: 400;
        font-size: 1.1rem;
        line-height: 1.8;
    }

    .stMarkdown strong, .stMarkdown b {
        color: #ffffff;
        font-weight: 700;
        text-shadow: 0 0 10px rgba(255,255,255,0.1);
    }

    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #f8fafc;
        font-weight: 800;
        letter-spacing: -0.5px;
    }

    /* ═══════ HERO ═══════ */
    .hero-container {
        text-align: center;
        padding: 60px 20px 40px 20px;
    }

    .hero-badge {
        display: inline-block;
        padding: 8px 24px;
        border-radius: 50px;
        font-size: 0.75rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 3px;
        background: rgba(6, 182, 212, 0.15); /* Cyan */
        color: #22d3ee;
        border: 1px solid rgba(6, 182, 212, 0.3);
        box-shadow: 0 0 20px rgba(6, 182, 212, 0.2);
        margin-bottom: 24px;
        backdrop-filter: blur(10px);
    }

    .hero-title {
        font-size: 4.5rem;
        font-weight: 900;
        color: #ffffff;
        letter-spacing: -2px;
        margin-bottom: 8px;
        line-height: 1.1;
        text-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }

    .hero-title span {
        /* Cyan to Blue Gradient */
        background: linear-gradient(135deg, #06b6d4 0%, #3b82f6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: pulseGlow 3s infinite alternate;
    }

    @keyframes pulseGlow {
        from { filter: drop-shadow(0 0 10px rgba(6, 182, 212, 0.4)); }
        to { filter: drop-shadow(0 0 25px rgba(59, 130, 246, 0.8)); }
    }

    .hero-sub {
        font-size: 1.2rem;
        color: #94a3b8;
        font-weight: 400;
        margin-top: 12px;
        letter-spacing: 0.5px;
    }

    /* ═══════ FEATURES ═══════ */
    .features-grid {
        display: flex;
        justify-content: center;
        gap: 16px;
        flex-wrap: wrap;
        margin: 40px auto 20px auto;
        max-width: 800px;
    }

    .feat {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 12px 24px;
        border-radius: 14px;
        font-size: 0.95rem;
        font-weight: 600;
        color: #cbd5e1;
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .feat:hover {
        transform: translateY(-5px) scale(1.02);
        border-color: rgba(59, 130, 246, 0.5); /* Blue Hover */
        color: #ffffff;
        box-shadow: 0 10px 25px rgba(59, 130, 246, 0.2);
        background: rgba(59, 130, 246, 0.05);
    }

    /* ═══════ TECH TAGS ═══════ */
    .tech-bar {
        display: flex;
        justify-content: center;
        gap: 10px;
        flex-wrap: wrap;
        margin: 20px auto 50px auto;
    }

    .tech {
        padding: 6px 16px;
        border-radius: 8px;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        color: #94a3b8;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(4px);
    }

    /* ═══════ INPUT & TEXTAREA ═══════ */
    .stTextArea textarea {
        background: rgba(15, 23, 42, 0.6) !important;
        border: 2px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 16px !important;
        color: #f8fafc !important;
        font-family: 'Outfit', sans-serif !important;
        font-size: 1.1rem !important;
        padding: 20px !important;
        box-shadow: inset 0 2px 10px rgba(0,0,0,0.2) !important;
        transition: all 0.3s ease !important;
    }

    .stTextArea textarea:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.15), inset 0 2px 10px rgba(0,0,0,0.2) !important;
    }

    /* ═══════ NORMAL BUTTONS (Example Prompts) ═══════ */
    .stButton > button[kind="secondary"] {
        background: rgba(255, 255, 255, 0.03) !important;
        color: #e2e8f0 !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 10px !important;
        padding: 12px 16px !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
        transition: all 0.3s ease !important;
    }

    .stButton > button[kind="secondary"]:hover {
        background: rgba(59, 130, 246, 0.08) !important;
        border-color: #3b82f6 !important;
        color: #ffffff !important;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.2) !important;
    }

    /* ═══════ MAIN CTA BUTTON ═══════ */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #06b6d4 0%, #3b82f6 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 14px !important;
        padding: 16px 40px !important;
        font-weight: 800 !important;
        font-size: 1.1rem !important;
        letter-spacing: 1px !important;
        text-transform: uppercase;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 8px 25px rgba(59, 130, 246, 0.3) !important;
        width: 100%;
        margin-top: 10px;
    }

    .stButton > button[kind="primary"]:hover {
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: 0 15px 35px rgba(59, 130, 246, 0.5) !important;
    }

    /* ═══════ TABS ═══════ */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: transparent;
        border-bottom: 2px solid rgba(255, 255, 255, 0.05);
        padding-bottom: 0;
    }

    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 255, 255, 0.02);
        border-radius: 12px 12px 0 0;
        color: #94a3b8;
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-bottom: none;
        padding: 14px 28px;
        font-weight: 700;
        font-size: 0.95rem;
        transition: all 0.3s ease;
    }

    .stTabs [aria-selected="true"] {
        background: rgba(15, 23, 42, 0.8) !important;
        color: #38bdf8 !important;
        border-bottom: 2px solid #38bdf8 !important;
    }

    .stTabs [data-baseweb="tab-panel"] {
        background: rgba(15, 23, 42, 0.6);
        border-radius: 0 0 16px 16px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-top: none;
        padding: 30px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.2);
    }

    /* ═══════ METRICS ═══════ */
    [data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        transition: transform 0.3s ease;
    }
    
    [data-testid="stMetric"]:hover {
        transform: translateY(-3px);
        border-color: rgba(56, 189, 248, 0.3);
    }

    [data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
        font-size: 0.8rem !important;
        font-weight: 700 !important;
        letter-spacing: 1px;
    }

    [data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-size: 1.4rem !important;
        font-weight: 900 !important;
        text-shadow: 0 2px 10px rgba(255,255,255,0.1);
    }

    /* ═══════ SIDEBAR ═══════ */
    [data-testid="stSidebar"] {
        background: rgba(3, 7, 18, 0.95);
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }

    hr {
        border-color: rgba(255,255,255,0.1) !important;
    }

    /* Callout styling */
    .callout-box {
        background: rgba(59, 130, 246, 0.1);
        border-left: 4px solid #3b82f6;
        padding: 16px 20px;
        border-radius: 0 8px 8px 0;
        margin-bottom: 20px;
    }
    .callout-title {
        color: #60a5fa;
        font-weight: 800;
        margin-bottom: 8px;
        font-size: 1.05rem;
    }
    .callout-text {
        color: #e2e8f0;
        font-size: 0.95rem;
        line-height: 1.6;
    }
</style>
""", unsafe_allow_html=True)


# ============================================================
# SIDEBAR — API Key Configuration
# ============================================================

with st.sidebar:
    st.markdown('<div class="sidebar-title">🔑 API Keys</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-subtitle">Enter your own API keys to use NavYatra AI</div>', unsafe_allow_html=True)

    st.markdown('<div class="key-section-label">🧠 LLM Provider</div>', unsafe_allow_html=True)
    api_cerebras = st.text_input("Cerebras API Key", type="password", key="cerebras_key",
                                  placeholder="Get free key → cloud.cerebras.ai")

    st.markdown('<div class="key-section-label">✈️ Flights & 🔍 Research</div>', unsafe_allow_html=True)
    api_serpapi = st.text_input("SerpApi Key (Google Flights & Maps)", type="password", key="serpapi_key",
                                    placeholder="serpapi.com")

    st.markdown('<div class="key-section-label">🏨 Hotel Discovery</div>', unsafe_allow_html=True)
    api_rapidapi = st.text_input("RapidAPI Key (Booking.com)", type="password", key="rapidapi_key",
                                  placeholder="rapidapi.com")

    st.markdown('<div class="key-section-label">🌤️ Weather</div>', unsafe_allow_html=True)
    api_openweather = st.text_input("OpenWeather API Key", type="password", key="openweather_key",
                                     placeholder="openweathermap.org")

    st.markdown("---")
    st.markdown(
        '<p style="color:#3f3f46; font-size:0.7rem; font-weight:600;">'
        '🔒 Keys are sent directly to the backend per request and are never stored.</p>',
        unsafe_allow_html=True
    )


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
# HOW TO PROMPT (RULES & EXAMPLES)
# ============================================================

st.markdown("""
<div class="callout-box">
    <div class="callout-title">💡 How to Prompt NavYatra AI</div>
    <div class="callout-text">
        <strong>1. Be Specific:</strong> Include your <b>origin</b>, <b>destination</b>, <b>start date</b>, <b>duration</b>, and <b>number of travelers (adults & children)</b>.<br>
        <strong>2. Choose Transport:</strong> Specify <b>"by flight"</b> or <b>"by train"</b>. The AI will intelligently route you to the nearest airport or railway station if your destination doesn't have one.<br>
        <strong>3. Currency:</strong> Tell the AI your preferred currency (e.g., <b>USD</b>, <b>EUR</b>, <b>INR</b>).<br>
        <strong>4. Preferences:</strong> Mention if you prefer budget, luxury, adventure, or relaxation.
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<p style="color:#94a3b8; font-size:0.85rem; font-weight:700; letter-spacing:1px; margin-bottom:10px;">👇 CLICK A SAMPLE PROMPT TO TRY</p>', unsafe_allow_html=True)

example_cols = st.columns(3)

EXAMPLES = [
    "Plan a 4-day luxury trip from Delhi to Manali by train starting July 10, 2026 for 2 adults and 1 child in USD.",
    "I want a budget beach getaway from Mumbai to Goa by flight for 5 days next month in EUR.",
    "Weekend trip from Bangalore to Coorg by train for 2 adults, focus on nature and relaxation in INR."
]

for i, col in enumerate(example_cols):
    with col:
        if st.button(EXAMPLES[i], key=f"example_{i}", use_container_width=True):
            st.session_state["user_query"] = EXAMPLES[i]

# ============================================================
# INPUT SECTION
# ============================================================

st.markdown("<br>", unsafe_allow_html=True)

user_query = st.text_area(
    "🗺️ DESCRIBE YOUR TRIP",
    value=st.session_state.get("user_query", ""),
    height=120,
    placeholder="E.g.: Plan a 3-day trip from Delhi to Goa starting July 10, 2026 for 2 adults..."
)

col1, col2, col3 = st.columns([1, 1.5, 1])
with col2:
    plan_button = st.button("🧭 Generate Travel Plan", use_container_width=True, type="primary")


# ============================================================
# BACKEND CONFIG
# ============================================================

BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")


# ============================================================
# PROCESS AND DISPLAY RESULTS
# ============================================================

if plan_button and user_query:

    # Validate all API keys are provided
    all_keys = {
        "Cerebras API Key": api_cerebras,
        "SerpApi Key": api_serpapi,
        "RapidAPI Key": api_rapidapi,
        "OpenWeather API Key": api_openweather,
    }
    missing_keys = [name for name, value in all_keys.items() if not value]

    if missing_keys:
        st.error(f"⚠️ Please enter all API keys in the sidebar before generating a plan.")
        st.warning(f"**Missing keys:** {', '.join(missing_keys)}")
        st.info("💡 Open the sidebar (click **>** at the top-left) to enter your API keys. All keys are free to obtain!")
    else:
        if "thread_id" not in st.session_state:
            st.session_state["thread_id"] = str(uuid.uuid4())

        thread_id = st.session_state["thread_id"]

        st.markdown("---")

        import json
        
        status = st.status("🧭 NavYatra AI is crafting your travel plan...", expanded=True)
        try:
            response = requests.post(
                f"{BACKEND_URL}/api/plan_stream",
                json={
                    "query": user_query,
                    "thread_id": thread_id,
                    "cerebras_api_key": api_cerebras,
                    "serpapi_key": api_serpapi,
                    "rapidapi_key": api_rapidapi,
                    "openweather_api_key": api_openweather,
                },
                stream=True,
                timeout=600
            )

            for line in response.iter_lines():
                if line:
                    decoded_line = line.decode('utf-8')
                    if decoded_line.startswith("data: "):
                        data = json.loads(decoded_line[6:])
                        
                        if data.get("error"):
                            status.error(f"Error: {data['error']}")
                            break
                        
                        agent = data.get("agent")
                        msg = data.get("status")
                        
                        if agent == "system":
                            status.write(f"⚙️ {msg}")
                        elif agent == "coordinator":
                            status.write(f"🧠 {msg}")
                        elif agent == "flight_agent":
                            status.write(f"✈️ {msg}")
                        elif agent == "train_agent":
                            status.write(f"🚆 {msg}")
                        elif agent == "hotel_agent":
                            status.write(f"🏨 {msg}")
                        elif agent == "weather_agent":
                            status.write(f"🌤️ {msg}")
                        elif agent == "research_agent":
                            status.write(f"🎯 {msg}")
                        elif agent == "itinerary_agent":
                            status.write(f"📋 {msg}")
                        elif agent == "complete":
                            status.update(label="✅ Travel Plan Complete!", state="complete", expanded=False)
                            st.session_state["result"] = data

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
    tabs = st.tabs(["🚆 Transport", "🏨 Hotels", "🌤️ Weather", "🎯 Attractions", "📋 Itinerary"])

    with tabs[0]:
        raw_flights = result.get("raw_flight_results", {})
        raw_trains = result.get("raw_train_results", {})
        
        # Determine which transport mode ran
        if raw_trains:
            
            train_data = result.get("train_results", "")
            if train_data:
                st.markdown(train_data)
            else:
                st.info("🚆 No train data was returned for this route.")
        else:
                
            flight_data = result.get("flight_results", "")
            if flight_data:
                st.markdown(flight_data)
            elif not raw_flights:
                st.info("🛫 No flight data was returned. The destination may not have a commercial airport.")

    with tabs[1]:
        raw_hotels = result.get("raw_hotel_results", {})
            
        hotel_data = result.get("hotel_results", "")
        if hotel_data:
            st.markdown(hotel_data)
        elif not raw_hotels:
            st.info("🏨 No hotel data was returned for this destination.")

    with tabs[2]:
        raw_weather = result.get("raw_weather_results", {})
            
        weather_data = result.get("weather_results", "")
        if weather_data:
            st.markdown(weather_data)
        elif not raw_weather:
            st.info("🌤️ No weather data was returned for this destination.")

    with tabs[3]:
        raw_research = result.get("raw_research_results", {})
            
        research_data = result.get("research_results", "")
        if research_data:
            st.markdown(research_data)
        elif not raw_research:
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
