from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
from .artwork import Artwork


class ScraperInterface(ABC):
    @abstractmethod
    def get_html(self, url: str) -> BeautifulSoup:
        ...

    @abstractmethod
    def get_artwork_urls(self, artist_html_content: BeautifulSoup) -> list:
        ...

    @abstractmethod
    def get_artwork_data(self, artwork_html_content: BeautifulSoup) -> Artwork:
        ...
