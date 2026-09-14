from src.browser import BrowserManager
from src.scraper import scrape_relevant_pages
from src.context_builder import build_context


manager = BrowserManager()

try:
    manager.start()

    pages = scrape_relevant_pages(
        manager,
        "https://postman.com",
    )

    context = build_context(pages)

    print(f"Pages scraped: {len(pages)}")
    print(f"Context characters: {len(context)}")
    print("\n" + "=" * 80)
    print(context[:5000])

finally:
    manager.close()