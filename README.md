<div align="center">

# 🧭 NavYatra AI

### Multi-Agent Travel Intelligence & Planning System

**6 Specialized AI Agents | Parallel Execution | Real-Time APIs**

[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![LangGraph](https://img.shields.io/badge/LangGraph-Multi--Agent-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)](https://langchain-ai.github.io/langgraph/)
[![Cerebras](https://img.shields.io/badge/Cerebras-Llama_3.3_70B-6C5CE7?style=for-the-badge)](https://cerebras.ai)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)

---

*NavYatra AI transforms a single natural-language travel query into a comprehensive, weather-aware, day-by-day travel plan — powered by 6 coordinated AI agents running in parallel.*

</div>

---

## 📋 Problem Statement

Planning a trip today means spending **hours juggling 5-6 platforms** — flight aggregators, hotel booking sites, weather apps, travel blogs, and review sites — then manually stitching everything into a coherent plan.

| Pain Point | Impact |
|:-----------|:-------|
| **Fragmented Research** | Travelers switch between 5+ platforms with no unified view |
| **Time Drain** | Average trip planning takes 3-5 hours of manual research |
| **No Intelligence** | Traditional tools list options but don't rank, analyze, or recommend |
| **Weather Blindness** | Plans are made without considering weather conditions |
| **No Personalization** | Static results that ignore traveler preferences |

**NavYatra AI solves this** by deploying 6 specialized AI agents that autonomously research, analyze, and synthesize a complete travel plan from a single sentence — in under 45 seconds.

---

## ✨ What It Does

> **Input**: *"Plan a 3-day trip from Delhi to Goa starting July 10, 2026 for 2 adults"*
>
> **Output**: Analyzed flights with price comparisons, 6-7 hotel recommendations, weather-aware packing advice, curated attractions with insider tips, and a day-by-day itinerary — all in one go.

| Agent | Capability |
|:------|:-----------|
| 🎯 **Coordinator** | Parses natural language into structured travel parameters |
| ✈️ **Flight Intelligence** | Searches real flights via Amadeus, ranks best/cheapest/fastest |
| 🏨 **Hotel Discovery** | Finds 6-7 accommodations with type, location advantage, and suitability |
| 🌤️ **Weather Analysis** | Current conditions + 5-day forecast + packing recommendations |
| 🔍 **Research Agent** | Discovers attractions, food guides, cultural tips, safety advice |
| 📋 **Itinerary Planner** | Synthesizes everything into a weather-aware, day-by-day plan |

---

## 🏗️ Architecture

NavYatra AI uses a **multi-agent graph architecture** powered by LangGraph with parallel fan-out execution.

```
                         ┌──────────────────┐
                         │   STREAMLIT UI   │
                         │  (Dark Theme)    │
                         └────────┬─────────┘
                                  │ HTTP POST /api/plan
                                  ▼
                         ┌──────────────────┐
                         │  FASTAPI SERVER  │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │   COORDINATOR    │
                         │  (Query Parser)  │
                         └──┬───┬───┬───┬───┘
                            │   │   │   │
               ┌────────────┘   │   │   └────────────┐
               ▼                ▼   ▼                ▼
        ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐
        │   FLIGHT   │  │   HOTEL    │  │  WEATHER   │  │  RESEARCH  │
        │  (Amadeus) │  │ (Geoapify) │  │(OpenWeather│  │  (Tavily)  │
        └─────┬──────┘  └─────┬──────┘  └─────┬──────┘  └─────┬──────┘
              │               │               │               │
              └───────────────┴───────┬───────┴───────────────┘
                                      ▼
                             ┌──────────────────┐
                             │    ITINERARY     │
                             │   SYNTHESIZER    │
                             └──────────────────┘
```

**Key**: The 4 domain agents run **in parallel** (LangGraph fan-out), reducing response time from ~3 minutes to **~35-45 seconds**.

---

## 🛠️ Tech Stack

### AI & Orchestration

| Technology | Role |
|:-----------|:-----|
| **LangGraph** | Multi-agent workflow with parallel fan-out/fan-in execution |
| **LangChain** | LLM tool-calling, prompt engineering, and chain composition |
| **Cerebras (Llama 3.3 70B)** | High-speed LLM inference — 1M tokens/day free tier |
| **Pydantic** | Structured data validation for query parsing |

### Backend & Frontend

| Technology | Role |
|:-----------|:-----|
| **FastAPI** | REST API with automatic OpenAPI docs |
| **Streamlit** | Interactive web UI with custom obsidian-dark theme |
| **SQLite** | Session persistence via LangGraph checkpointer |

### External APIs

| API | Provider | What It Returns |
|:----|:---------|:----------------|
| **Amadeus** | [developers.amadeus.com](https://developers.amadeus.com) | Flight routes, prices, airlines, timings |
| **Geoapify** | [geoapify.com](https://www.geoapify.com) | Hotel names, addresses, types, coordinates |
| **OpenWeather** | [openweathermap.org](https://openweathermap.org/api) | Temperature, humidity, wind, 5-day forecast |
| **Tavily** | [tavily.com](https://tavily.com) | Tourist attractions, food guides, cultural tips |

> **Note on APIs**: Amadeus and Geoapify are currently on **sandbox/test environments**. Migration to production endpoints is planned — this will unlock real-time booking data and global availability with no functional code changes required.

---

## 📂 Project Structure

```
NavYatra-AI/
├── agents/                  # AI Agent implementations
│   ├── coordinator.py       # NL query → structured TravelQuery
│   ├── flight_agent.py      # Flight search & analysis
│   ├── hotel_agent.py       # Hotel discovery & ranking
│   ├── weather_agent.py     # Weather analysis & packing advice
│   ├── research_agent.py    # Attractions & cultural research
│   ├── itinerary_agent.py   # Final itinerary synthesis
│   └── llm_utils.py         # LLM factory, retry logic, rate limit handling
│
├── api/                     # External API clients
│   ├── flights.py           # Amadeus API client
│   ├── hotels.py            # Geoapify API client
│   ├── weather.py           # OpenWeather API client
│   └── research.py          # Tavily API client
│
├── graph/                   # LangGraph orchestration
│   ├── state.py             # Shared state (TypedDict)
│   └── workflow.py          # Graph builder + parallel execution
│
├── prompts/                 # Agent prompt templates
│   └── templates.py         # All 6 agent system prompts
│
├── schemas/                 # Data models
│   └── models.py            # TravelQuery Pydantic model
│
├── backend/                 # REST API
│   └── main.py              # FastAPI app with /api/plan endpoint
│
├── frontend/                # Web UI
│   └── app.py               # Streamlit app with premium dark theme
│
├── .env.example             # Template for required API keys
├── requirements.txt         # Python dependencies
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.12+**
- API keys for: **Cerebras**, **Amadeus**, **Geoapify**, **OpenWeather**, **Tavily**

### Setup

```bash
# 1. Clone
git clone https://github.com/Satyam2006chh/NavYatra-AI.git
cd NavYatra-AI

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure API keys
cp .env.example .env
# Edit .env with your keys

# 4. Start backend
python -m uvicorn backend.main:app --reload --port 8000

# 5. Start frontend (new terminal)
streamlit run frontend/app.py --server.port 8501

# 6. Open http://localhost:8501
```

### Getting API Keys

| API | Sign Up | Free Tier |
|:----|:--------|:----------|
| **Cerebras** | [cloud.cerebras.ai](https://cloud.cerebras.ai) | 1M tokens/day |
| **Amadeus** | [developers.amadeus.com](https://developers.amadeus.com) | 500 calls/month |
| **Geoapify** | [geoapify.com](https://www.geoapify.com) | 3,000 calls/day |
| **OpenWeather** | [openweathermap.org](https://openweathermap.org/api) | 1,000 calls/day |
| **Tavily** | [tavily.com](https://tavily.com) | 1,000 calls/month |

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|:-------|:---------|:------------|
| `GET` | `/api/health` | Health check — returns `{"status": "healthy"}` |
| `POST` | `/api/plan` | Generate a complete travel plan from a natural language query |

**Example Request:**
```json
{
  "query": "Plan a 3-day trip from Delhi to Goa starting July 10, 2026 for 2 adults"
}
```

---

## 🗺️ Future Roadmap

| Feature | Description | Status |
|:--------|:------------|:-------|
| **Production APIs** | Migrate Amadeus & Geoapify from sandbox to production for live booking data | 🔜 Planned |
| **MCP Server Integration** | Model Context Protocol for direct flight and hotel booking within the AI interface | 🔜 Planned |
| **Voice AI Agent** | Conversational voice interface to search and book flights hands-free | 📋 Designed |
| **Android App** | Native mobile experience with on-the-go travel planning and offline itineraries | 📋 Designed |
| **Multi-Destination Trips** | Support for complex multi-city itineraries with inter-city transport optimization | 💡 Ideation |
| **Budget Optimizer** | AI-powered budget allocation across flights, hotels, food, and activities | 💡 Ideation |

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add your feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

<div align="center">

**Built by [Satyam Chhabra](https://github.com/Satyam2006chh)** · NavYatra AI — Your AI Travel Companion 🧭

</div>
