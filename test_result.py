from src.schemas import CompanyResult


success = CompanyResult(
    domain="postman.com",
    status="success",
    intelligence=None,
    error=None,
)

failure = CompanyResult(
    domain="bad-domain.com",
    status="failed",
    intelligence=None,
    error={
        "stage": "scraping",
        "error_type": "NetworkError",
        "message": "Unable to resolve domain",
    },
)

print("SUCCESS:")
print(success.model_dump_json(indent=2))

print("\nFAILURE:")
print(failure.model_dump_json(indent=2))