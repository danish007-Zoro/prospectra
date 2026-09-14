from src.browser import BrowserManager
from src.cleaner import clean_html


manager = BrowserManager()

try:
    manager.start()

    url = "https://postman.com/company/about-postman/"
    html = manager.fetch_page(url)

    clean_text = clean_html(html)

    print("Clean text characters:", len(clean_text))
    print("\n--- CLEAN TEXT ---\n")
    print(clean_text)

finally:
    manager.close()