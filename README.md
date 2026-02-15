<div align="center">
  
![NavYatra AI Showcase](assets/showcase.png)

# 🧭 NavYatra AI

### Intelligent Multi-Agent Travel Planning System

**Powered by 6 Specialized AI Agents | LangGraph Orchestration | Groq LLM**

[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![LangGraph](https://img.shields.io/badge/LangGraph-Multi--Agent-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)](https://langchain-ai.github.io/langgraph/)
[![Groq](https://img.shields.io/badge/Groq-Llama_3.3_70B-F55036?style=for-the-badge)](https://groq.com)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)

---

*NavYatra AI transforms a simple travel query into a comprehensive, day-by-day travel itinerary using a coordinated system of AI agents — each specialized in flights, hotels, weather, attractions, and itinerary planning.*

</div>

---

## 📋 Problem Statement

Planning a trip involves juggling **multiple platforms** — one for flights, another for hotels, a weather app, travel blogs for attractions, and then manually stitching everything into a coherent plan. This is:

- **Time-consuming** — hours spent across 5-6 different websites
- **Fragmented** — no single platform combines flights + hotels + weather + attractions
- **Overwhelming** — too many options without intelligent recommendations
- **Static** — traditional tools don't adapt to weather conditions or traveler preferences

**NavYatra AI solves this** by deploying 6 specialized AI agents that work together to research, analyze, and synthesize a complete travel plan from a single natural language query.

---

## ✨ What NavYatra AI Does

> **Input**: *"Plan a 3-day trip from Delhi to Goa starting July 10, 2026 for 2 adults"*
>
> **Output**: A comprehensive travel plan with analyzed flights, 6-7 hotel options, weather-aware packing advice, curated attractions, and a day-by-day itinerary.

### Key Capabilities

| Feature | Description |
|---------|-------------|
| ✈️ **Flight Intelligence** | Searches real flights via Amadeus API, analyzes best/cheapest/fastest options |
| 🏨 **Hotel Discovery** | Finds 6-7 accommodation options (hotels, resorts, villas) via Geoapify |
| 🌤️ **Weather Analysis** | Current conditions + 5-day forecast with packing suggestions |
| 🎯 **Attraction Research** | Discovers must-visit places, food guides, cultural tips via Tavily |
| 📋 **Smart Itinerary** | Synthesizes all data into a weather-aware, day-by-day travel plan |
| 🛡️ **Fallback Handling** | Cities without airports get professional suggestions for alternative transport |

---

## 🏗️ Architecture & Workflow

NavYatra AI uses a **multi-agent graph architecture** powered by LangGraph. Each agent is a specialized AI node that performs one task exceptionally well.

### System Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                     STREAMLIT FRONTEND                           │
│              (Premium Dark UI + User Input)                      │
└──────────────────────┬───────────────────────────────────────────┘
                       │ HTTP POST /api/plan
                       ▼
┌──────────────────────────────────────────────────────────────────┐
│                     FASTAPI BACKEND                              │
│           (REST API + Request Validation)                        │
└──────────────────────┬───────────────────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────────────────┐
│                  LANGGRAPH WORKFLOW                               │
│                                                                  │
│   ┌─────────────┐                                                │
│   │ Coordinator │──── Parses natural language → TravelQuery      │
│   └──────┬──────┘                                                │
│          │                                                       │
│          ▼                                                       │
│   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│   │ Flight Agent │  │ Hotel Agent  │  │Weather Agent │          │
│   │  (Amadeus)   │  │ (Geoapify)   │  │(OpenWeather) │          │
│   └──────┬───────┘  └──────┬───────┘  └──────┬───────┘          │
│          │                 │                  │                   │
│          │          ┌──────────────┐          │                   │
│          │          │Research Agent│          │                   │
│          │          │  (Tavily)    │          │                   │
│          │          └──────┬───────┘          │                   │
│          │                 │                  │                   │
│          ▼                 ▼                  ▼                   │
│   ┌──────────────────────────────────────────────────┐           │
│   │           ITINERARY SYNTHESIS AGENT               │           │
│   │     (Combines all outputs → Day-by-day plan)      │           │
│   └───────────────────────────────────────────────────┘           │
│                                                                  │
│   SQLite Checkpointer (Session Persistence)                      │
└──────────────────────────────────────────────────────────────────┘
```

### Agent Workflow (Current: Sequential)

```
START → Coordinator → Flight Agent → Hotel Agent → Weather Agent → Research Agent → Itinerary Agent → END
```

> **Note**: Flight, Hotel, Weather, and Research agents are architecturally independent — they only need the Coordinator's output. The system is designed for future parallel execution when rate limits allow, which would reduce response time from ~2.5 minutes to ~40 seconds.

### How Each Agent Works

Each domain agent follows this pattern:

```
1. Receive structured query from Coordinator
2. Call external API (Amadeus/Geoapify/OpenWeather/Tavily)
3. Feed raw API data to Groq LLM with domain-specific prompt
4. LLM analyzes, ranks, and formats the data
5. Return structured, human-readable analysis
```

---

## 🛠️ Tech Stack

### Core AI Framework

| Technology | Purpose |
|-----------|---------|
| **LangGraph** | Multi-agent workflow orchestration with state management |
| **LangChain** | LLM tool-calling, prompt templates, and chain composition |
| **Groq (Llama 3.3 70B)** | Ultra-fast LLM inference for all 6 agents |
| **Pydantic** | Strict schema validation for structured data extraction |

### Backend

| Technology | Purpose |
|-----------|---------|
| **FastAPI** | REST API server with automatic OpenAPI documentation |
| **SQLite** | Session persistence via LangGraph checkpointer |
| **Python-dotenv** | Secure environment variable management |

### Frontend

| Technology | Purpose |
|-----------|---------|
| **Streamlit** | Interactive web UI with custom dark theme |
| **Custom CSS** | Premium obsidian-dark design with cyan/emerald accents |

### External APIs

| API | Provider | Purpose | Data Returned |
|-----|----------|---------|---------------|
| **Amadeus** | Amadeus for Developers | Flight search & pricing | Airlines, times, prices, stops |
| **Geoapify** | Geoapify Places | Hotel/accommodation discovery | Hotel names, addresses, coordinates |
| **OpenWeather** | OpenWeatherMap | Weather data & forecasts | Temperature, humidity, 5-day forecast |
| **Tavily** | Tavily AI | Travel research & attractions | Tourist attractions, food, cultural tips |

---

## 📂 Project Structure

```
NavYatra-AI/
├── agents/                  # AI Agent implementations
│   ├── coordinator.py       # Query parser (NL → structured TravelQuery)
│   ├── flight_agent.py      # Flight search & analysis agent
│   ├── hotel_agent.py       # Hotel discovery & ranking agent
│   ├── weather_agent.py     # Weather analysis & packing agent
│   ├── research_agent.py    # Attraction & cultural research agent
│   ├── itinerary_agent.py   # Final itinerary synthesis agent
│   └── llm_utils.py         # Rate limit handling, retries, LLM factory
│
├── api/                     # External API clients
│   ├── flights.py           # Amadeus API client (IATA codes, flight search)
│   ├── hotels.py            # Geoapify API client (geocoding, hotel search)
│   ├── weather.py           # OpenWeather API client (current + forecast)
│   └── research.py          # Tavily API client (web research)
│
├── graph/                   # LangGraph orchestration
│   ├── state.py             # Shared state definition (TypedDict)
│   └── workflow.py          # Graph builder, node definitions, runner
│
├── prompts/                 # Agent prompt templates
│   └── templates.py         # All 6 agent system prompts
│
├── schemas/                 # Data models
│   └── models.py            # TravelQuery Pydantic model
│
├── backend/                 # REST API server
│   └── main.py              # FastAPI app with /api/plan endpoint
│
├── frontend/                # Web interface
│   └── app.py               # Streamlit app with premium dark UI
│
├── .env                     # API keys (not tracked in git)
├── .env.example             # Template for required API keys
├── .gitignore               # Git ignore rules
└── requirements.txt         # Python dependencies
```

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.12+**
- API keys for: Groq, Amadeus, Geoapify, OpenWeather, Tavily

### 1. Clone the Repository

```bash
git clone https://github.com/Satyam2006chh/NavYatra-AI.git
cd NavYatra-AI
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Copy the example env file and fill in your API keys:

```bash
cp .env.example .env
```

Edit `.env` with your keys:

```env
GROQ_API_KEY=your_groq_api_key
AMADEUS_CLIENT_ID=your_amadeus_client_id
AMADEUS_CLIENT_SECRET=your_amadeus_client_secret
GEOAPIFY_API_KEY=your_geoapify_api_key
OPENWEATHER_API_KEY=your_openweather_api_key
TAVILY_API_KEY=your_tavily_api_key
```

### 4. Start the Backend

```bash
python -m uvicorn backend.main:app --reload --port 8000
```

### 5. Start the Frontend (in a new terminal)

```bash
streamlit run frontend/app.py --server.port 8501
```

### 6. Open the App

Navigate to **http://localhost:8501** in your browser.

---

## 📡 API Reference

### Health Check

```http
GET /api/health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "NavYatra AI"
}
```

### Generate Travel Plan

```http
POST /api/plan
Content-Type: application/json

{
  "query": "Plan a 3-day trip from Delhi to Goa starting July 10, 2026 for 2 adults",
  "thread_id": "optional-session-id"
}
```

**Response:**
```json
{
  "thread_id": "uuid",
  "parsed_input": { "origin_city": "Delhi", "destination_city": "Goa", ... },
  "flight_results": "✈️ Flight analysis...",
  "hotel_results": "🏨 Hotel recommendations...",
  "weather_results": "🌤️ Weather analysis...",
  "research_results": "🎯 Attractions & tips...",
  "itinerary": "📋 Day-by-day travel plan..."
}
```

---

## 🔑 Getting API Keys

| API | Sign Up Link | Free Tier |
|-----|-------------|-----------|
| **Groq** | [console.groq.com](https://console.groq.com) | 100K tokens/day |
| **Amadeus** | [developers.amadeus.com](https://developers.amadeus.com) | 500 calls/month |
| **Geoapify** | [geoapify.com](https://www.geoapify.com) | 3000 calls/day |
| **OpenWeather** | [openweathermap.org](https://openweathermap.org/api) | 1000 calls/day |
| **Tavily** | [tavily.com](https://tavily.com) | 1000 calls/month |

---

## 🧠 LLM & AI Details

NavYatra AI uses **Groq's inference engine** with the **Llama 3.3 70B Versatile** model for all agent reasoning. The system is also compatible with **OpenAI** models — simply swap the LLM provider in `agents/llm_utils.py` to use `ChatOpenAI` instead of `ChatGroq`.

### Why Groq?
- **Speed**: Groq's custom LPU (Language Processing Unit) provides the fastest LLM inference available
- **Quality**: Llama 3.3 70B delivers GPT-4 level reasoning at no cost
- **Free Access**: Generous free tier for development and testing

### Rate Limit Management
The system includes built-in rate limit handling:
- **Exponential backoff** retries on 429/413 errors
- **Agent delays** between sequential calls to respect free-tier TPM limits
- **Output truncation** to keep token usage within limits

---

## 🌟 Realistic Use Cases

NavYatra AI is designed for real-world travel scenarios where complexity, speed, and personalization matter. Let's look at how it transforms the travel experience:

### 1. The Family Vacationer 👨‍👩‍👧‍👦
*   **Use Case**: Planning a long-awaited trip to Kyoto and Bali with specific needs for family-friendly retreats.
*   **NavYatra Solution**: As shown in the **Showcase Image**, NavYatra generates a multi-destination itinerary that balances cultural exploration in Kyoto with tropical relaxation in Bali.

### 2. The Busy Professional 💼
*   **Use Case**: Needs to commute between major hubs for meetings with zero time to research.
*   **NavYatra Solution**: High-speed transit and optimal flight paths are calculated by the **Flight Agent**, providing flight numbers and exact timings instantly.

### 3. The Solo Adventurer ⛰️
*   **Use Case**: Looking for hidden gems and authentic local food spots.
*   **NavYatra Solution**: The **Research Agent** digs deep into local culture to recommend hidden temples and local street food guides.

---

## 📸 UI Preview

NavYatra AI features a premium **obsidian-dark theme** with **cyan and emerald accents**:

- **Hero section** with gradient-styled branding
- **Feature pills** showcasing agent capabilities
- **One-click example prompts** for quick testing
- **Tabbed results** — Flights, Hotels, Weather, Attractions, Itinerary
- **Trip metrics** — origin, destination, date, duration at a glance
- **Footer credit** — Built by Satyam Chhabra

---

## 🚀 Future Roadmap

NavYatra AI is continuously evolving. Here’s what we’re working on:

*   **Production API Migration**: Currently using the **Amadeus & Geoapify Sandbox** environments. We will soon shift to **Production Services** to provide live, real-time booking data and global availability.
*   **Booking System Integration (MCP)**: Integrating the **Model Context Protocol (MCP)** to enable direct flight and hotel booking capabilities within the AI interface.
*   **Latency Optimization**: Implementing **Parallel Agent Execution** to reduce total planning time from minutes to seconds.
*   **Mobile App**: Expanding NavYatra AI to a dedicated mobile experience for on-the-go travel assistance.

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

<div align="center">

**Built with ❤️ by [Satyam Chhabra](https://github.com/Satyam2006chh)**

*NavYatra AI — Your AI-Powered Travel Companion* 🧭

</div>
