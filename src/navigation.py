from src.browser import BrowserManager
from src.cleaner import clean_html
from src.decision import decide_next_page
from src.scraper import (
    PageEvidence,
    discover_relevant_links,
    get_page_type,
)


MAX_AGENT_STEPS = 5


class NavigationState:
    """
    Tracks the state of the autonomous navigation loop.
    """

    def __init__(self):
        self.visited_urls: set[str] = set()
        self.available_urls: list[str] = []
        self.pages = []
        self.navigation_usage = []


def initialize_navigation(
    homepage_url: str,
) -> NavigationState:
    """
    Initialize navigation state with the homepage.
    """

    state = NavigationState()
    state.available_urls.append(homepage_url)

    return state


def mark_url_visited(
    state: NavigationState,
    url: str,
) -> None:
    """
    Mark a URL as visited and remove it from available URLs.
    """

    if url not in state.visited_urls:
        state.visited_urls.add(url)

    if url in state.available_urls:
        state.available_urls.remove(url)


def add_available_urls(
    state: NavigationState,
    urls: list[str],
) -> None:
    """
    Add newly discovered URLs that have not already been visited
    or added to the available URL list.
    """

    for url in urls:
        if url in state.visited_urls:
            continue

        if url in state.available_urls:
            continue

        state.available_urls.append(url)


def is_available_url(
    state: NavigationState,
    url: str | None,
) -> bool:
    """
    Check whether a URL is currently available for navigation.
    """

    if not url:
        return False

    return (
        url in state.available_urls
        and url not in state.visited_urls
    )


def update_available_urls(
    state: NavigationState,
    html: str,
    base_url: str,
) -> None:
    """
    Discover relevant links from a page and add them to navigation state.
    """

    discovered_urls = discover_relevant_links(
        html,
        base_url,
    )

    add_available_urls(
        state,
        discovered_urls,
    )

def build_requirement_status(
    state: NavigationState,
) -> str:
    """
    Determine which required information categories are
    represented in the collected website evidence.
    """

    combined_content = "\n".join(
        page.content.lower()
        for page in state.pages
    )

    has_overview = any(
        keyword in combined_content
        for keyword in [
            "about",
            "platform",
            "company",
            "founded",
            "mission",
        ]
    )

    has_audience = any(
        keyword in combined_content
        for keyword in [
            "developers",
            "engineers",
            "teams",
            "enterprises",
            "businesses",
            "startups",
        ]
    )

    has_contact = any(
        keyword in combined_content
        for keyword in [
            "@",
            "contact",
            "email",
        ]
    )

    has_leadership = any(
        keyword in combined_content
        for keyword in [
            "ceo",
            "cto",
            "co-founder",
            "founder",
            "leadership",
            "executive",
        ]
    )

    return (
        f"Company overview: "
        f"{'FOUND' if has_overview else 'MISSING'}\n"
        f"Target audience: "
        f"{'FOUND' if has_audience else 'MISSING'}\n"
        f"Public contact emails: "
        f"{'FOUND' if has_contact else 'MISSING'}\n"
        f"Key leadership/team: "
        f"{'FOUND' if has_leadership else 'MISSING'}"
    )

def build_navigation_context(
    state: NavigationState,
    max_chars: int = 6000,
) -> str:
    """
    Build a compact representation of collected evidence
    for the navigation decision-maker.
    """

    context_parts = []
    total_chars = 0
    separator = "\n\n---\n\n"

    for page in state.pages:
        page_text = (
            f"PAGE TYPE: {page.page_type}\n"
            f"SOURCE URL: {page.url}\n"
            f"CONTENT:\n{page.content}\n"
        )

        if total_chars >= max_chars:
            break

        remaining_chars = max_chars - total_chars

        if context_parts:
            if remaining_chars <= len(separator):
                break

            context_parts.append(separator)
            total_chars += len(separator)
            remaining_chars = max_chars - total_chars

        if len(page_text) > remaining_chars:
            page_text = page_text[:remaining_chars]

        context_parts.append(page_text)
        total_chars += len(page_text)

    return "".join(context_parts)

def choose_next_action(
    state: NavigationState,
):
    context = build_navigation_context(state)

    decision, usage = decide_next_page(
        context=context,
        available_urls=state.available_urls,
    )

    state.navigation_usage.append(usage)

    return decision

def execute_navigation(
    state: NavigationState,
    manager: BrowserManager,
    target_url: str,
):
    """
    Visit the selected URL and add its evidence to navigation state.
    A page-level failure is isolated so navigation can continue.
    """
    if not is_available_url(state, target_url):
        raise ValueError(
            f"URL is not available for navigation: {target_url}"
        )

    try:
        html = manager.fetch_page(target_url)

        page = PageEvidence(
            url=target_url,
            content=clean_html(html),
            page_type=get_page_type(target_url),
        )

        state.pages.append(page)
        update_available_urls(
            state,
            html,
            target_url,
        )

        return page

    except Exception as exc:
        print(
            f"Failed to navigate to {target_url}: {exc}"
        )
        return None

    finally:
        mark_url_visited(
            state,
            target_url,
        )

def run_navigation_loop(
    manager: BrowserManager,
    homepage_url: str,
) -> NavigationState:
    """
    Run the autonomous navigation loop.
    """

    state = initialize_navigation(homepage_url)

    homepage_html = manager.fetch_page(homepage_url)

    homepage_page = PageEvidence(
        url=homepage_url,
        content=clean_html(homepage_html),
        page_type=get_page_type(homepage_url),
    )

    state.pages.append(homepage_page)

    mark_url_visited(
        state,
        homepage_url,
    )

    update_available_urls(
        state,
        homepage_html,
        homepage_url,
    )

    for step in range(MAX_AGENT_STEPS):
        print(f"\nAgent step: {step + 1}/{MAX_AGENT_STEPS}")

        if not state.available_urls:
            print("No more available URLs.")
            break

        decision = choose_next_action(state)

        print(
            f"Decision: {decision.action}"
        )

        print(
            f"Reason: {decision.reason}"
        )

        if decision.action == "finish":
            print("Agent decided to finish.")
            break

        if not is_available_url(
            state,
            decision.target_url,
        ):
            print(
                f"Invalid navigation target: "
                f"{decision.target_url}"
            )
            continue

        execute_navigation(
            state,
            manager,
            decision.target_url,
        )

    return state