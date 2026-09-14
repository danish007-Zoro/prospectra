import json
from pathlib import Path

from src.agent import run_agent


DOMAINS = [
    "https://postman.com",
    "https://supabase.com",
    "https://vapi.ai",
]


def main():
    results = run_agent(DOMAINS)

    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    output_file = output_dir / "output.json"

    output_data = {
        domain: result.model_dump()
        for domain, result in results.items()
    }

    with output_file.open("w", encoding="utf-8") as file:
        json.dump(
            output_data,
            file,
            indent=2,
            ensure_ascii=False,
        )

    print(f"\nOutput written to: {output_file}")


if __name__ == "__main__":
    main()