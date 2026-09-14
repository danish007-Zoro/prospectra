from src.navigation import (
    NavigationState,
    add_available_urls,
    mark_url_visited,
    is_available_url,
    build_navigation_context,
)
from src.scraper import PageEvidence
from unittest.mock import Mock

from src.navigation import execute_navigation


def test_mark_url_visited_removes_url_from_available():
    state = NavigationState()
    state.available_urls = ["https://example.com/about"]

    mark_url_visited(
        state,
        "https://example.com/about",
    )

    assert "https://example.com/about" in state.visited_urls
    assert "https://example.com/about" not in state.available_urls


def test_add_available_urls_ignores_visited_urls():
    state = NavigationState()
    state.visited_urls.add("https://example.com/about")

    add_available_urls(
        state,
        [
            "https://example.com/about",
            "https://example.com/contact",
        ],
    )

    assert state.available_urls == [
        "https://example.com/contact"
    ]


def test_add_available_urls_ignores_duplicates():
    state = NavigationState()

    add_available_urls(
        state,
        [
            "https://example.com/about",
            "https://example.com/about",
        ],
    )

    assert state.available_urls == [
        "https://example.com/about"
    ]


def test_valid_navigation_target_is_accepted():
    state = NavigationState()
    state.available_urls = [
        "https://example.com/about"
    ]

    assert is_available_url(
        state,
        "https://example.com/about",
    ) is True


def test_invalid_navigation_target_is_rejected():
    state = NavigationState()
    state.available_urls = [
        "https://example.com/about"
    ]

    assert is_available_url(
        state,
        "https://example.com/fake",
    ) is False


def test_visited_navigation_target_is_rejected():
    state = NavigationState()
    state.available_urls = [
        "https://example.com/about"
    ]
    state.visited_urls.add(
        "https://example.com/about"
    )

    assert is_available_url(
        state,
        "https://example.com/about",
    ) is False


def test_navigation_context_respects_character_limit():
    state = NavigationState()

    state.pages = [
        PageEvidence(
            url="https://example.com/about",
            content="A" * 10000,
            page_type="about",
        )
    ]

    context = build_navigation_context(
        state,
        max_chars=6000,
    )

    assert len(context) <= 6000

def test_execute_navigation_handles_page_failure():
    state = NavigationState()
    target_url = "https://example.com/about"
    state.available_urls = [target_url]

    manager = Mock()
    manager.fetch_page.side_effect = TimeoutError(
        "Simulated page timeout"
    )

    result = execute_navigation(
        state,
        manager,
        target_url,
    )

    assert result is None
    assert target_url in state.visited_urls
    assert target_url not in state.available_urls
    assert state.pages == []