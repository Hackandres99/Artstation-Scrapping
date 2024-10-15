from abc import ABC, abstractmethod
from selenium.webdriver import Chrome
from .scraper import ArtstationScraper
from .models.project.artwork import Artwork
from .models.artist.artist import Artist, Base


class ProcessingInterface(ABC):

    @abstractmethod
    def get_driver(self, port: int) -> Chrome:
        ...

    @abstractmethod
    def get_base_data(self) -> tuple[ArtstationScraper, Base, str]:
        ...

    @abstractmethod
    def get_artist(self) -> Artist:
        ...

    @abstractmethod
    def get_artwork(self, artwork_index: int) -> Artwork:
        ...
    
    @abstractmethod
    def get_artworks(self) -> list[Artwork]:
        ...