# Use official Python 3.11 slim image (lightweight, compatible with your deps)
FROM python:3.11-slim

# Install system dependencies (ffmpeg + audio libs for Whisper)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory to backend
WORKDIR /app

# Copy only backend (since frontend is separate)
COPY backend/ /app/

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Expose the port Render expects
EXPOSE $PORT

# Start command (Render will inject $PORT)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "$PORT"]