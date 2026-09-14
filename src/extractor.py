import os

from dotenv import load_dotenv
from openai import OpenAI

from src.schemas import CompanyIntelligence
from src.browser import BrowserManager
from src.context_builder import build_context
from src.scraper import scrape_relevant_pages


load_dotenv()


client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)


def extract_company_intelligence(context: str) -> CompanyIntelligence:
    """
    Extract structured company intelligence from scraped web evidence.
    """

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a company intelligence extraction system. "
                    "Extract information only from the provided website evidence. "
                    "Do not use outside knowledge. "
                    "Do not invent, assume, or infer specific facts that are not "
                    "explicitly supported by the evidence. "
                    "For contact points, include only public generic or business "
                    "email addresses that appear in the provided evidence. "
                    "For leadership, include only people whose names and roles are "
                    "explicitly stated in the provided evidence. "
                    "Only provide a LinkedIn URL when a LinkedIn URL is explicitly "
                    "present in the evidence; otherwise use null. "
                    "For every extracted item, use the source URL of the page where "
                    "the supporting evidence appears. "
                    "If information is unavailable, use an empty list or null where "
                    "appropriate. "
                    "Keep the company overview concise and limited to two sentences. "
                    "The confidence score should reflect how complete and well-supported "
                    "the extracted information is."
                ),
            },
            {
                "role": "user",
                "content": context,
            },
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "company_intelligence",
                "strict": True,
                "schema": CompanyIntelligence.model_json_schema(),
            },
        },
    )

    intelligence = CompanyIntelligence.model_validate_json(
        response.choices[0].message.content
    )

    return intelligence, response.usage

def process_company(
    manager: BrowserManager,
    domain: str,
) -> tuple[CompanyIntelligence, list, object]:
    """
    Scrape a company website and extract structured intelligence.
    """

    pages = scrape_relevant_pages(
        manager,
        domain,
    )

    context = build_context(pages)

    intelligence, usage = extract_company_intelligence(context)

    return intelligence, pages, usage