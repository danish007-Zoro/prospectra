from unittest.mock import patch

from src.agent import run_agent
from src.schemas import CompanyIntelligence


def test_one_company_failure_does_not_stop_other_companies():
    successful_intelligence = CompanyIntelligence(
        company_overview="A test company that provides software.",
        target_audience="Software developers.",
        contact_points=[],
        key_leadership=[],
        confidence_score=0.8,
    )

    def fake_process_company(manager, domain):
        if "bad-domain" in domain:
            raise RuntimeError("Simulated scraping failure")

        return (
            successful_intelligence,
            [],
            type(
                "Usage",
                (),
                {
                    "prompt_tokens": 100,
                    "completion_tokens": 50,
                },
            )(),
            [],
        )

    with patch(
        "src.agent.process_company",
        side_effect=fake_process_company,
    ):
        results = run_agent(
            [
                "https://bad-domain.com",
                "https://good-domain.com",
            ]
        )

    assert results["https://bad-domain.com"].status == "failed"
    assert results["https://bad-domain.com"].error is not None

    assert results["https://good-domain.com"].status == "success"
    assert results["https://good-domain.com"].intelligence is not None