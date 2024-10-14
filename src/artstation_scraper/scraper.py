from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from time import sleep
from .models.project.artwork import Artwork
from .scraper_interface import ScraperInterface
from .utilities.bs4_extractors import (
    _extract_title,
    _extract_description,
    _extract_date,
    _extract_likes,
    _extract_views,
    _extract_threads,
    _extract_softwares,
    _extract_tags,
    _extract_images,
    _extract_comments
)


class ArtstationScraper(ScraperInterface):
    def __init__(self, driver) -> None:
        self.driver = driver

    def get_html(self, url: str) -> BeautifulSoup:
        self.driver.get(url)
        sleep(5)

        # Abrir comentarios anidados
        while True:
            load_data = self.driver.find_elements(
                By.CSS_SELECTOR, 'a.btn.load-more'
            )
            if not load_data:
                break

            for data in load_data:
                data.click()
                sleep(2)

        content = self.driver.page_source
        html = BeautifulSoup(content, 'html.parser')
        return html

    def get_artwork_urls(self, artist_html_content: BeautifulSoup) -> list:
        artwork_urls = []
        artworks = artist_html_content.find_all(
            'projects-list-item', {'class': 'gallery-grid-item'}
        )
        for i, p in enumerate(artworks):
            try:
                artwork_url = p.find(
                    'a', {'class': 'gallery-grid-link'}
                ).attrs['href']
                artwork_urls.append(artwork_url)
            except Exception as err:
                print(f'{i + 1}.- Artwork url error: {err.args}')
        return artwork_urls

    def get_artwork_data(self, artwork_html_content: BeautifulSoup) -> Artwork:
        artwork = artwork_html_content
        try:
            title = _extract_title(artwork)
            description = _extract_description(artwork)
            date = _extract_date(artwork)
            likes = _extract_likes(artwork)
            views = _extract_views(artwork)
            threads = _extract_threads(artwork)

            # Obtener comentarios principales y anidados
            comments = _extract_comments(artwork)
            softwares = _extract_softwares(artwork)
            tags = _extract_tags(artwork)
            images = _extract_images(artwork)

        except Exception as err:
            print(f'Artwork data error: {err.args}')

        return Artwork(title, description,
                       date, likes, views,
                       threads, comments,
                       softwares, tags, images
                       )
