# Dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install panspace (CPU version)
RUN pip install --no-cache-dir panspace[cpu]

# Expose Streamlit port
EXPOSE 8501

# Run the app
CMD ["panspace", "app"]