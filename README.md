# OpportunityRadar V3

OpportunityRadar is a smart web change detection and opportunity tracking system designed for students. It continuously monitors official sources (NPTEL, AICTE, ISRO, Internshala, etc.) for updates on certifications, hackathons, internships, scholarships, and government schemes.

## 🌟 Key Features

- **Automated Scraper**: A Python-based engine that monitors 25+ official platforms every 6 hours.
- **Dynamic Feed**: A modern SvelteKit dashboard with real-time updates and unread status tracking.
- **Personalized Experience**: Filter opportunities by your educational branch (CS, IT, Mech, etc.) and year.
- **Smart Categorization**: Automated tagging and sorting into five distinct opportunity channels.
- **Local-First Data**: Powered by SQLite for high performance and complete data privacy.
- **Student Success Guide**: Built-in onboarding to help new users maximize the platform's features.

## 🛠️ Technology Stack

- **Backend**: Python, Requests, Playwright, SQLite
- **Frontend**: SvelteKit 5, TypeScript, TailwindCSS v4
- **Database**: Better-SQLite3
- **Styling**: Modern dark-themed "Glassmorphism" UI

## 🚀 Getting Started

### Prerequisites

- Node.js 18+
- Python 3.10+

### 1. Setup Data Engine (Scraper)

```bash
# Install dependencies
pip install -r requirements.txt

# Run the scraper
python main.py
```

### 2. Setup Dashboard (UI)

```bash
cd ui

# Install dependencies
npm install

# Run development server
npm run dev
```

The dashboard will be available at `http://localhost:5173`.

## 📁 Project Structure

- `main.py`: The entry point for the scraping engine.
- `ui/`: The SvelteKit dashboard implementation.
- `db/`: Database models and initialization logic.
- `core/`: Core scraping and change detection logic.
- `utils/`: Shared utility functions for text processing.

---

Built for students, by students. Stay ahead of the curve with **OpportunityRadar**.
