from src.browser import BrowserManager
from src.cleaner import clean_html
from src.scraper import PageEvidence
from src.context_builder import build_context


manager = BrowserManager()

try:
    manager.start()

    html = manager.fetch_page("https://postman.com")

    cleaned = clean_html(html)

    page = PageEvidence(
        url="https://postman.com",
        content=cleaned,
        page_type="homepage",
    )

    context = build_context([page])

    print("CLEANED TEXT:")
    print("—" in cleaned)
    print("â€”" in cleaned)

    print("\nCONTEXT:")
    print("—" in context)
    print("â€”" in context)

finally:
    manager.close()

from src.extractor import extract_company_intelligence

intelligence = extract_company_intelligence(context)

print("\nLLM OUTPUT:")
print(repr(intelligence.company_overview))

print("\nLLM OUTPUT CHARACTERS:")
for char in intelligence.company_overview:
    if ord(char) > 127:
        print(char, ord(char))