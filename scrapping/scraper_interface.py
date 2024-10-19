from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
from .models.project.artwork import Artwork
from .models.artist.artist import Base, Resume
from .models.artist.artwork_preview import Preview


class ScraperInterface(ABC):

    @abstractmethod
    def get_html(
        self, url: str, method: str, previews_number: int
    ) -> BeautifulSoup:
        ...

    @abstractmethod
    def get_artist_base_data(
        self, artist_html_content: BeautifulSoup
    ) -> Base:
        ...

    @abstractmethod
    def get_artist_resume_data(
        self, artist_html_resume: BeautifulSoup
    ) -> Resume:
        ...

    @abstractmethod
    def get_artwork_data(
        self, artwork_html_content: BeautifulSoup, artwork_id: str
    ) -> Artwork | dict:
        ...

    @abstractmethod
    def get_artist_artwork_previews(
        self, artist_html_content: BeautifulSoup, previews_number: int
    ) -> list[Preview]:
        ...
