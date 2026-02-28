# Use official Python 3.11 slim image
FROM python:3.11-slim

# Install system dependencies: ffmpeg, libsndfile1, git (for pip git deps)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsndfile1 \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy backend folder
COPY backend/ /app/

# Upgrade pip and install requirements
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Expose port (Render injects $PORT)
EXPOSE $PORT

# Start the app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "$PORT"]