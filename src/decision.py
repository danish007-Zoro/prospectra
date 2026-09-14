import os

from dotenv import load_dotenv
from openai import OpenAI

from src.schemas import NavigationDecision


load_dotenv()


client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)


def decide_next_page(
    context: str,
    available_urls: list[str],
) -> tuple[NavigationDecision, object]:
    """
    Ask the LLM whether the agent should visit another page
    or finish collecting evidence.
    """

    url_list = "\n".join(
        f"- {url}"
        for url in available_urls
    )

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a web navigation decision-maker for a company "
                    "intelligence agent. Review the collected website evidence "
                    "and decide whether more information is needed. "
                    "The required information is: "
                    "(1) company overview, "
                    "(2) target audience / ideal customer profile, "
                    "(3) public contact emails, and "
                    "(4) key leadership/team members. "

                    "Before choosing an action, evaluate each required category "
                    "against the collected evidence. "

                    "Choose finish only when the evidence sufficiently supports "
                    "all four categories. "

                    "If one or more categories are missing or weakly supported, "
                    "choose visit_page and select the single available URL most "
                    "likely to provide the missing information. "

                    "Do not visit pages merely to obtain more detail when the "
                    "required categories are already sufficiently supported. "

                    "Never invent a URL. "
                    "Only select a URL from the provided list. "
                ),
            },
            {
                "role": "user",
                "content": (
                    f"CURRENT EVIDENCE:\n\n"
                    f"{context}\n\n"
                    f"AVAILABLE URLS:\n\n"
                    f"{url_list}"
                    f"DECISION RULE:\n"
                    f"Assess the four required categories using only the "
                    f"evidence above. If all four are sufficiently supported, "
                    f"finish. Otherwise, visit the most useful available page."
                ),
            },
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "navigation_decision",
                "strict": True,
                "schema": NavigationDecision.model_json_schema(),
            },
        },
    )

    decision = NavigationDecision.model_validate_json(
        response.choices[0].message.content
    )

    return decision, response.usage