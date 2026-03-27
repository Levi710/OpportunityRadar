#!/bin/bash

# Start the Python Scraper in the background
echo "Starting OpportunityRadar Scraper..."
python main.py &

# Start the SvelteKit Dashboard
echo "Starting OpportunityRadar Dashboard..."
cd ui && node build
