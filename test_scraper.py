from src.scraper import (
    discover_relevant_links,
    get_page_type,
)


def test_discover_relevant_links_only_returns_same_domain():
    html = """
    <html>
        <body>
            <a href="/company/about/">About</a>
            <a href="/company/contact-us/">Contact</a>
            <a href="https://other-example.com/about">External</a>
        </body>
    </html>
    """

    links = discover_relevant_links(
        html,
        "https://example.com",
    )

    assert "https://example.com/company/about/" in links
    assert "https://example.com/company/contact-us/" in links
    assert "https://other-example.com/about" not in links


def test_discover_relevant_links_ignores_homepage():
    html = """
    <html>
        <body>
            <a href="/">Home</a>
            <a href="/company/about/">About</a>
        </body>
    </html>
    """

    links = discover_relevant_links(
        html,
        "https://example.com",
    )

    assert "https://example.com" not in links
    assert "https://example.com/company/about/" in links


def test_relevant_pages_are_ranked_higher():
    html = """
    <html>
        <body>
            <a href="/careers/">Careers</a>
            <a href="/company/about/">About</a>
            <a href="/company/contact-us/">Contact</a>
        </body>
    </html>
    """

    links = discover_relevant_links(
        html,
        "https://example.com",
    )

    assert links[0] == "https://example.com/company/about/"
    assert links[1] == "https://example.com/company/contact-us/"


def test_get_page_type_classifies_common_pages():
    assert (
        get_page_type("https://example.com/company/about/")
        == "about"
    )

    assert (
        get_page_type("https://example.com/company/contact-us/")
        == "contact"
    )

    assert (
        get_page_type("https://example.com/pricing/")
        == "pricing"
    )

    assert (
        get_page_type("https://example.com/company/careers/")
        == "careers"
    )


def test_get_page_type_classifies_homepage():
    assert (
        get_page_type("https://example.com")
        == "homepage"
    )