import os
from dotenv import load_dotenv
from .utilities.drivers import get_chrome_driver
from .scraper import ArtstationScraper
from .models.artist.artist import Artist, Base
from .models.artist.artwork_preview import Preview
from .models.project.artwork import Artwork
from .processing_interface import ProcessingInterface


class Processing(ProcessingInterface):

    def __init__(self, artist: str = '') -> None:
        load_dotenv()
        self.artstation_url = os.getenv('ARTSTATION_URL')
        self.artist_url = self.artstation_url + artist
        
    def _get_base_data(self) -> tuple[ArtstationScraper, Base]:
        driver = get_chrome_driver(9222)
        artstation_Scraper = ArtstationScraper(driver)
        artist_html = artstation_Scraper.get_html(
            self.artist_url, 'base_data'
        )
        artist_base_data = artstation_Scraper.get_artist_base_data(
            artist_html
        )
        return artstation_Scraper, artist_base_data

    def get_artist(self) -> Artist | dict:
        scraper, base_data = self._get_base_data()
        if base_data.resume_page != '/resume':
            artist_html_resume = scraper.get_html(
                base_data.resume_page, 'artist'
            )
            resume_data = scraper.get_artist_resume_data(
                artist_html_resume
            )
            return Artist(base_data, resume_data)
        else:
            return dict(message='Artist not found')

    def get_artwork(self, artwork_id: str) -> Artwork:
        driver = get_chrome_driver(9222)
        scraper = ArtstationScraper(driver)
        artwork_url = f'{self.artstation_url}artwork/{artwork_id}'
        artwork_html = scraper.get_html(
            artwork_url, 'artwork'
        )
        artwork = scraper.get_artwork_data(
            artwork_html, artwork_id
        )
        return artwork

    def get_previews(self, previews_number: int) -> list[Preview]:
        driver = get_chrome_driver(9222)
        scraper = ArtstationScraper(driver)
        artist_html = scraper.get_html(
            self.artist_url, 'previews', previews_number
        )
        previews = scraper.get_artist_artwork_previews(
            artist_html, previews_number
        )
        return previews
