from src.schemas import CompanyIntelligence


result = CompanyIntelligence(
    company_overview=(
        "Postman is an API platform used to build and test APIs. "
        "It helps teams collaborate throughout the API lifecycle."
    ),
    target_audience="Software developers and engineering teams.",
    contact_points=[],
    key_leadership=[
        {
            "name": "Abhinav Asthana",
            "role": "CEO & Co-founder",
            "linkedin_url": None,
            "source_url": "https://postman.com/company/about-postman/",
        }
    ],
    confidence_score=0.9,
)

print(result)