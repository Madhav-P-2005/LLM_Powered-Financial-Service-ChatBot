# Use a lightweight Python image
FROM python:3.11-slim

# Prevent Python from writing .pyc files and enable stdout flushing
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

# Create and set working directory
WORKDIR /app

# Install build deps for any wheels that may need compiling (kept minimal)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install first to leverage Docker layer caching
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the backend code
COPY . /app

# Expose the port Railway will connect to
EXPOSE 8000

# Start the app with gunicorn, binding to the PORT env var
CMD ["bash","-lc","gunicorn -w 2 -b 0.0.0.0:${PORT} app:app"]
