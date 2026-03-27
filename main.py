"""OpportunityRadar — entry point that initializes the system and starts the scheduler."""

import json
import sys
from pathlib import Path

from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel

from utils.logger import setup_logger
from db.database import init_db
from db.models import get_source_count, insert_source
from core.scheduler import start_scheduler

console = Console()


def print_banner():
    """Display a startup banner in the terminal using rich."""
    banner_text = (
        "[bold cyan]OpportunityRadar[/bold cyan]\n"
        "[dim]Website change detection for student opportunities[/dim]\n"
        "[dim]Monitoring official MNC & government sources[/dim]"
    )
    console.print(Panel(banner_text, border_style="bright_blue", padding=(1, 2)))


def seed_sources():
    """Load sources from config/sources.json and insert/update them in the database.
    """
    sources_path = Path(__file__).resolve().parent / "config" / "sources.json"

    if not sources_path.exists():
        logger.error("sources.json not found at {}", sources_path)
        return

    with open(sources_path, "r", encoding="utf-8") as f:
        sources = json.load(f)

    for s in sources:
        insert_source(
            name=s["name"],
            url=s["url"],
            css_selector=s["css_selector"],
            is_js_rendered=s.get("is_js_rendered", False),
            category=s.get("category", "general"),
            tags=s.get("tags", ["all"])
        )
        logger.info("Seeded/Updated source: {}", s["name"])

    logger.info("Processed {} sources from sources.json", len(sources))


if __name__ == "__main__":
    # Load environment variables
    load_dotenv()

    # Setup logging
    logger = setup_logger()

    # Startup banner
    print_banner()

    # Initialize database
    logger.info("Initializing database...")
    init_db()

    # Seed sources from JSON
    logger.info("Checking if sources need seeding...")
    seed_sources()

    # Start the scheduler (blocks forever)
    try:
        print()
        console.print("[bold green]✓[/bold green] System ready — scheduler starting\n")
        start_scheduler()
    except (KeyboardInterrupt, SystemExit):
        console.print("\n[bold yellow]⏹ Scheduler stopped by user[/bold yellow]")
        sys.exit(0)
