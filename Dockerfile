# Use Microsoft's official Playwright Python image
FROM mcr.microsoft.com/playwright/python:v1.44.0-jammy

WORKDIR /app

# Install Node.js 20 (Vite 7 requirement)
RUN apt-get update && apt-get install -y curl \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# 1. Build the UI
COPY ui/package*.json ./ui/
RUN cd ui && npm install

COPY ui/ ./ui/
RUN cd ui && npm run build

# 2. Setup the Scraper
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3. Final Prep
COPY . .

# Setup start script
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

# Expose the dashboard port
EXPOSE 3000

# Set environment variables
ENV NODE_ENV=production
ENV PORT=3000
ENV DATABASE_PATH=/app/opportunityradar.db

CMD ["/app/start.sh"]
