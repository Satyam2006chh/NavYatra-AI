#!/bin/bash

# ============================================
# NavYatra AI — Docker Startup Script
# Starts both FastAPI backend and Streamlit frontend
# ============================================

echo "🚀 Starting NavYatra AI..."
echo "📡 Backend  → http://localhost:8000"
echo "🌐 Frontend → http://localhost:8501"
echo ""

# Start FastAPI backend in the background
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 &

# Start Streamlit frontend in the foreground
streamlit run frontend/app.py --server.port 8501 --server.address 0.0.0.0 --server.headless true
