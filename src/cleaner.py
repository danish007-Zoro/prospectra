from bs4 import BeautifulSoup


CONTENT_TAGS = ["h1", "h2", "h3", "p", "li"]


def clean_html(html: str) -> str:
    """
    Convert rendered HTML into structured, LLM-ready text.
    """

    soup = BeautifulSoup(html, "html.parser")

    # Remove elements that don't contain useful textual content.
    for element in soup(["script", "style", "svg", "noscript"]):
        element.decompose()

    # Prefer the main content area when available.
    main = soup.find("main")

    if main:
        container = main
    else:
        container = soup

    sections = []

    for element in container.find_all(CONTENT_TAGS):
        text = element.get_text(" ", strip=True)

        if not text:
            continue

        if element.name == "h1":
            sections.append(f"# {text}")

        elif element.name == "h2":
            sections.append(f"## {text}")

        elif element.name == "h3":
            sections.append(f"### {text}")

        elif element.name == "li":
            sections.append(f"- {text}")

        else:
            sections.append(text)

    return "\n\n".join(sections)