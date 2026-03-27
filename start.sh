#!/bin/bash

# Start the Python Scraper in the background
echo "--- Starting OpportunityRadar Scraper ---"
python3 main.py > scraper.log 2>&1 &

# Start the SvelteKit Dashboard
echo "--- Starting OpportunityRadar Dashboard ---"
cd ui && node build/index.js
