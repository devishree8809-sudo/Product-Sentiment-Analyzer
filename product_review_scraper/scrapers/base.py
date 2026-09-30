import random
import time
import requests
from abc import ABC, abstractmethod

class BaseScraper(ABC):
    """
    Abstract base class for e-commerce review scrapers.
    Provides utility methods for User-Agent rotation, session management,
    and request delays.
    """

    USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0"
    ]

    def __init__(self):
        self.session = requests.Session()

    def get_headers(self) -> dict:
        """
        Generates realistic browser headers, rotating the User-Agent.
        """
        return {
            "User-Agent": random.choice(self.USER_AGENTS)
        }

    def delay(self, min_seconds: float = 1.0, max_seconds: float = 3.0):
        """
        Sleeps for a random duration to mimic real human browsing behavior.
        """
        sleep_time = random.uniform(min_seconds, max_seconds)
        time.sleep(sleep_time)

    @abstractmethod
    def scrape(self, target: str, limit: int = 50, **kwargs) -> list:
        """
        Scrapes review data for a target.

        Args:
            target (str): ASIN for Amazon, product slug for Flipkart.
            limit (int): Maximum number of reviews to extract.

        Returns:
            list: List of dictionaries representing individual reviews.
        """
        pass
