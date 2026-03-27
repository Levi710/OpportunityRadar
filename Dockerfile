# Use Microsoft's official Playwright Python image
FROM mcr.microsoft.com/playwright/python:v1.44.0-jammy

WORKDIR /app

# Install Node.js 20 (Vite 7 requirement)
RUN apt-get update && apt-get install -y curl \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# 1. Setup Environment
COPY . .

# 2. Build the UI
RUN cd ui && npm install
RUN cd ui && npm run build

# 3. Setup the Scraper
RUN pip install --no-cache-dir -r requirements.txt

# 4. Browser Setup
RUN playwright install chromium
RUN npx playwright install-deps

# 5. Final Prep
RUN chmod +x /app/start.sh

# Expose the HF Spaces port
EXPOSE 7860

# Set environment variables
ENV NODE_ENV=production
ENV PORT=7860
ENV DATABASE_PATH=/app/opportunityradar.db

CMD ["/app/start.sh"]
