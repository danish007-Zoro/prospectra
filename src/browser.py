from playwright.sync_api import sync_playwright


class BrowserManager:
    """
    Manages a reusable Playwright browser session.
    """

    def __init__(self):
        self.playwright = None
        self.browser = None

    def start(self):
        """Start Playwright and launch Chromium."""
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=True)

    def fetch_page(self, url: str) -> str:
        """
        Open a URL in a new browser page and return its rendered HTML.
        """

        if self.browser is None:
            raise RuntimeError("BrowserManager has not been started.")

        page = self.browser.new_page()

        try:
            response = page.goto(
                url,
                wait_until="domcontentloaded",
                timeout=30000,
            )

            if response is None:
                raise RuntimeError("No response received from the page.")

            if response.status >= 400:
                raise RuntimeError(
                    f"HTTP error {response.status} while fetching {url}"
                )

            return page.content()

        finally:
            page.close()


    def close(self):
        """Close the browser and Playwright."""
        if self.browser is not None:
            self.browser.close()

        if self.playwright is not None:
            self.playwright.stop()