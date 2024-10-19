from abc import ABC, abstractmethod
from .scraper import ArtstationScraper
from .models.project.artwork import Artwork
from .models.artist.artist import Artist, Base
from .models.artist.artwork_preview import Preview


class ProcessingInterface(ABC):

    @abstractmethod
    def _get_base_data(self) -> tuple[ArtstationScraper, Base]:
        ...

    @abstractmethod
    def get_artist(self) -> Artist | dict:
        ...

    @abstractmethod
    def get_artwork(self, artwork_index: int) -> Artwork:
        ...

    @abstractmethod
    def get_previews(self, previews_number: int | str) -> list[Preview]:
        ...

    @abstractmethod
    def get_artworks(self, artworks_number: int | str) -> list[Artwork]:
        ...
