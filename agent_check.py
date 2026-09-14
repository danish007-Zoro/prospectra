from src.agent import run_agent


DOMAINS = [
    "https://postman.com",
    "https://this-domain-definitely-does-not-exist-123456789.com",
    "https://vapi.ai",
]


results = run_agent(DOMAINS)

print("\n" + "=" * 60)
print("FINAL RESULTS")
print("=" * 60)

for domain, result in results.items():
    print(f"\n{domain}")

    if isinstance(result, dict) and "error" in result:
        print(f"ERROR: {result['error']}")
    else:
        print(result.model_dump_json(indent=2))