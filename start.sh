#!/bin/bash

# 1. Initialize SQLite Database & Tables Synchronously
echo "--- Initializing Database ---"
python3 -c "from db.database import init_db; init_db()"

# 2. Start the Python Scraper in the background (Output to console so Render logs it!)
echo "--- Starting OpportunityRadar Scraper ---"
python3 main.py &

# Start the SvelteKit Dashboard on port 7860
echo "--- Starting OpportunityRadar Dashboard on Port $PORT ---"
cd ui && node build/index.js
