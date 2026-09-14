from src.browser import BrowserManager
from src.extractor import process_company
from src.schemas import CompanyResult, LLMUsage
from src.validator import validate_intelligence
from src.confidence import (
    calculate_confidence,
    calculate_coverage_score,
)
from src.errors import classify_error
from src.cost_tracker import calculate_llm_cost
from src.linkedin import (
    enrich_team_members_with_linkedin,
    get_company_name,
)


def run_agent(domains: list[str]) -> dict[str, CompanyResult]:
    """
    Process multiple company domains while isolating failures.
    """

    manager = BrowserManager()

    results = {}

    try:
        manager.start()

        for domain in domains:
            print(f"\nProcessing: {domain}")

            try:
                intelligence, pages, usage, navigation_usage = process_company(
                    manager,
                    domain,
                )

                navigation_input_tokens = sum(
                    item.prompt_tokens
                    for item in navigation_usage
                )

                navigation_output_tokens = sum(
                    item.completion_tokens
                    for item in navigation_usage
                )

                input_tokens = (
                    navigation_input_tokens
                    + usage.prompt_tokens
                )

                output_tokens = (
                    navigation_output_tokens
                    + usage.completion_tokens
                )

                total_tokens = (
                    input_tokens
                    + output_tokens
                )

                estimated_cost = calculate_llm_cost(
                    input_tokens,
                    output_tokens,
                )

                print(
                    f"LLM usage: {input_tokens} input + "
                    f"{output_tokens} output = {total_tokens} total tokens"
                )

                print(
                    f"Estimated LLM cost: ${estimated_cost:.6f}"
                )

                (
                    total_contacts,
                    verified_contacts,
                    unverified_emails,
                    total_members,
                    verified_members,
                    unverified_members,
                ) = validate_intelligence(
                    intelligence,
                    pages,
                )
                company_name = get_company_name(domain)

                enrich_team_members_with_linkedin(
                intelligence.key_leadership,
                company_name,
                )
                
                coverage_score = calculate_coverage_score(pages)

                intelligence.confidence_score = calculate_confidence(
                    llm_confidence=intelligence.confidence_score,
                    total_contacts=total_contacts,
                    verified_contacts=verified_contacts,
                    total_members=total_members,
                    verified_members=verified_members,
                    coverage_score=coverage_score,
                )

                print(
                    f"Contacts verified: {verified_contacts}/{total_contacts}"
                )

                print(
                    f"Leadership verified: {verified_members}/{total_members}"
                )

                if unverified_emails:
                    print(f"Unverified emails: {unverified_emails}")

                if unverified_members:
                    print(f"Unverified leadership: {unverified_members}")

                results[domain] = CompanyResult(
                    domain=domain,
                    status="success",
                    intelligence=intelligence,
                    usage=LLMUsage(
                        input_tokens=input_tokens,
                        output_tokens=output_tokens,
                        total_tokens=total_tokens,
                        estimated_cost_usd=estimated_cost,
                    ),
                    error=None,
                )

                print(f"Successfully processed: {domain}")

            except Exception as exc:
                error_type = classify_error(exc)

                results[domain] = CompanyResult(
                    domain=domain,
                    status="failed",
                    intelligence=None,
                    usage=None,
                    error={
                        "stage": "processing",
                        "error_type": error_type,
                        "message": str(exc),
                    },
                )

                print(
                    f"Failed to process {domain}: {exc}"
                )

    finally:
        manager.close()

    return results