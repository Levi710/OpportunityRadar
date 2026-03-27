# Build stage for SvelteKit
FROM node:20 AS ui-builder
WORKDIR /app/ui
COPY ui/package*.json ./
RUN npm install
COPY ui/ .
RUN npm run build

# Final stage
FROM python:3.11-slim
WORKDIR /app

# Install Node.js 20
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    build-essential \
    python3-dev \
    libsqlite3-dev \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Install Playwright dependencies
RUN npx playwright install-deps

# Copy Python requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN playwright install chromium

# Copy the rest of the application
COPY . .

# Copy the built UI from the builder stage
COPY --from=ui-builder /app/ui/build /app/ui/build
COPY --from=ui-builder /app/ui/package.json /app/ui/package.json

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
