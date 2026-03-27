#!/bin/bash

# Start the Python Scraper in the background
echo "--- Starting OpportunityRadar Scraper ---"
python3 main.py > scraper.log 2>&1 &

# Start the SvelteKit Dashboard on port 7860
echo "--- Starting OpportunityRadar Dashboard on Port $PORT ---"
cd ui && node build/index.js
