# Lightweight Python base — NOT the full Playwright image
FROM python:3.11-slim

WORKDIR /app

# Install system deps + Node.js 20 in one layer to keep image small
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    gnupg \
    ca-certificates \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user for HF Spaces (uid 1000)
RUN useradd -m -u 1000 appuser

# Install python packages and Playwright system deps as root
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN playwright install-deps chromium

# Prepare Data Directory for SQLite
RUN mkdir -p /data && chown appuser:appuser /data
ENV DATABASE_PATH=/data/opportunityradar.db

# Set up UI dependencies (Layer cache)
COPY ui/package*.json ./ui/
RUN cd ui && npm ci

# Copy UI source and build
COPY ui/ ./ui/
# Disable Svelte static prerendering during build to prevent SQLite crashes
ENV PRERENDER=false
RUN cd ui && npm run build

# Copy remaining application files
COPY --chown=appuser:appuser . .

# Ensure start script is executable
RUN chmod +x /app/start.sh

# Switch to non-root user for actual browser install and execution
USER appuser
ENV PLAYWRIGHT_BROWSERS_PATH=/home/appuser/.cache/ms-playwright
RUN playwright install chromium

# Runtime Environment Variables
ENV PORT=7860
ENV NODE_ENV=production

EXPOSE 7860

CMD ["/app/start.sh"]
