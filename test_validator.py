from src.browser import BrowserManager
from src.scraper import scrape_relevant_pages
from src.schemas import CompanyIntelligence
from src.validator import validate_contact_points
from src.validator import verify_team_member


manager = BrowserManager()

try:
    manager.start()

    pages = scrape_relevant_pages(
        manager,
        "https://postman.com",
    )

    intelligence = CompanyIntelligence(
        company_overview="Test company.",
        target_audience="Developers.",
        contact_points=[
            {
                "email": "info@postman.com",
                "source_url": "https://postman.com/company/contact-us/",
            },
            {
                "email": "fake@postman.com",
                "source_url": "https://postman.com/company/contact-us/",
            },
        ],
        key_leadership=[],
        confidence_score=0.5,
    )

    unverified = validate_contact_points(
        intelligence,
        pages,
    )

    print(f"Unverified emails: {unverified}")

finally:
    manager.close()


real_leader = verify_team_member(
    pages,
    "Abhinav Asthana",
    "CEO and co-founder",
    "https://postman.com/company/about-postman/",
)

fake_leader = verify_team_member(
    pages,
    "Abhinav Asthana",
    "Chief Financial Officer",
    "https://postman.com/company/about-postman/",
)

print(f"Real leader verified: {real_leader}")
print(f"Fake leader verified: {fake_leader}")