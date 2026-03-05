# ============================================
# NavYatra AI — Dockerfile
# Multi-Agent Travel Planning System
# ============================================

# 1. Use official Python 3.12 slim image (lightweight)
FROM python:3.12-slim

# 2. Set working directory inside the container
WORKDIR /app

# 3. Copy requirements first (for Docker layer caching)
COPY requirements.txt .

# 4. Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the entire project into the container
COPY . .

# 6. Make the startup script executable
RUN chmod +x start.sh

# 7. Expose ports for backend (8000) and frontend (8501)
EXPOSE 8000 8501

# 8. Run both servers using the startup script
CMD ["bash", "start.sh"]
