from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bson import ObjectId
from .scraper import ArtstationScraper
from .models.artist.artist import Artist, Base
from .models.project.artwork import Artwork
from .processing_interface import ProcessingInterface

class Processing(ProcessingInterface):

    def __init__(self, artist) -> None:
        self.artist = artist

    def get_driver(self, port: int) -> Chrome:
        chrome_options = Options()
        chrome_options.add_argument(f'--remote-debugging-port={str(port)}')
        service = Service(ChromeDriverManager().install())
        driver = Chrome(service=service, options=chrome_options)
        return driver


    def get_base_data(self) -> tuple[ArtstationScraper, Base, str]:
        artstation_url = 'https://www.artstation.com/'
        artist_url = artstation_url + self.artist

        driver = self.get_driver(9222)
        artstation_Scraper = ArtstationScraper(driver)

        artist_Html = artstation_Scraper.get_html(artist_url)
        artist_base_data = artstation_Scraper.get_artist_base_data(artist_Html)

        return artstation_Scraper, artist_base_data, artist_url



    def get_artist(self) -> Artist:
        scraper, base_data, _ = self.get_base_data()
        artist_html_resume = scraper.get_html(base_data.resume_page)
        resume_data = scraper.get_artist_resume_data(
            artist_html_resume
        )
        return Artist(ObjectId(), base_data, resume_data)


    def get_artwork(self, artwork_index: int) -> Artwork:
        scraper, base_data, artist_url = self.get_base_data()
        for i, artwork in enumerate(base_data.artwork_urls):
            if i == artwork_index - 1:
                artwork_Html = scraper.get_html(artwork)
                artwork = scraper.get_artwork_data(
                    artwork_Html, artist_url
                )
                return artwork


    def get_artworks(self) -> list[Artwork]:
        scraper, base_data, artist_url = self.get_base_data()
        artworks = []
        for artwork_url in base_data.artwork_urls:
            artwork_html = scraper.get_html(artwork_url)
            artwork = scraper.get_artwork_data(
                artwork_html, artist_url
            )
            artworks.append(artwork)
        return artworks
