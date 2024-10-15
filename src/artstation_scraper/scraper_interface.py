from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
from .models.project.artwork import Artwork
from .models.artist.artist import Base, Resume


class ScraperInterface(ABC):

    @abstractmethod
    def get_html(self, url: str) -> BeautifulSoup:
        ...

    @abstractmethod
    def get_artist_base_data(self, artist_html_content: BeautifulSoup) -> Base:
        ...

    @abstractmethod
    def get_artist_resume_data(
        self, artist_html_resume: BeautifulSoup
    ) -> Resume:
        ...

    @abstractmethod
    def get_artwork_data(
        self, artwork_html_content: BeautifulSoup, artist_url: str
    ) -> Artwork:
        ...
