# Lightweight Python base — NOT the full Playwright image
FROM python:3.11-slim

WORKDIR /app

# Install system deps + Node.js 20 in one layer to keep image small
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    gnupg \
    ca-certificates \
    # Chromium system deps (minimal)
    libnss3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    # Node.js
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user for HF Spaces (uid 1000)
RUN useradd -m -u 1000 appuser

# Copy and install Python deps first (layer cache — only reruns if requirements.txt changes)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install only Chromium — not Firefox or WebKit
RUN playwright install chromium

# Copy UI and build it (layer cache — only reruns if ui/ changes)
COPY ui/package*.json ./ui/
RUN cd ui && npm install

COPY ui/ ./ui/
RUN cd ui && npm run build

# Copy rest of app
COPY --chown=appuser:appuser . .

# Persistent storage for SQLite (survives redeployments)
RUN mkdir -p /data && chown appuser:appuser /data

# Runtime Environment Variables
ENV DATABASE_PATH=/data/opportunityradar.db
ENV PORT=7860
ENV NODE_ENV=production
ENV PYTHONUNBUFFERED=1
ENV PLAYWRIGHT_BROWSERS_PATH=/home/appuser/.cache/ms-playwright

RUN chmod +x /app/start.sh

USER appuser

EXPOSE 7860

CMD ["/app/start.sh"]
