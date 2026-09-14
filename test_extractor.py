from src.browser import BrowserManager
from src.extractor import process_company


manager = BrowserManager()

try:
    manager.start()

    result = process_company(
        manager,
        "https://postman.com",
    )

    print("\n" + "=" * 60)
    print("EXTRACTED COMPANY INTELLIGENCE")
    print("=" * 60)

    print(result.model_dump_json(indent=2))

finally:
    manager.close()