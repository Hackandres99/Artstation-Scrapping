from bs4 import BeautifulSoup
from time import sleep
from .artwork import Artwork
from .scraper_interface import ScraperInterface
from dateutil import parser
from bson import ObjectId


class ArtstationScraper(ScraperInterface):
    def __init__(self, driver) -> None:
        self.driver = driver

    def get_html(self, url: str) -> BeautifulSoup:
        self.driver.get(url)
        sleep(5)
        content = self.driver.page_source
        html = BeautifulSoup(content, 'html.parser')
        return html

    def get_artwork_urls(self, artist_html_content: BeautifulSoup) -> list:
        artwork_urls = []
        artworks = artist_html_content.find_all(
            'projects-list-item',
            {'class': 'gallery-grid-item'}
        )
        for i, p in enumerate(artworks):
            try:
                artwork_url = p.find(
                    'a',
                    {'class': 'gallery-grid-link'}
                ).attrs['href']

                artwork_urls.append(artwork_url)
            except Exception as err:
                print(f'{i + 1}.- Artwork url error: {err.args}')
        return artwork_urls

    def get_artwork_data(self, artwork_html_content: BeautifulSoup) -> Artwork:
        artwork = artwork_html_content
        try:
            title = artwork.find(
                'h3',
                {'class': 'project-description-title'}
            ).get_text()

            description = artwork.find(
                'read-more',
                {'class': 'project-description'}
            ).get_text()

            date = parser.parse(artwork.find(
                'time',
                {'class': 'project-published'}
            ).attrs['datetime'])

            likes_html = artwork.find(
                'button',
                {'class': 'btn btn-reset'}
            )
            if likes_html:
                likes = int(likes_html.contents[1])
            else:
                likes = 0

            views = artwork.find(
                'i',
                {'class': 'far fa-eye'}
            ).next_sibling.next_sibling

            comments = artwork.find(
                'i',
                {'class': 'far fa-comments'}
            ).next_sibling.next_sibling

            softwares = {}
            softwares_html = artwork.find_all(
                'a',
                {'class': 'project-software-item'}
            )
            for software in softwares_html:
                name = software.find(
                    'span',
                    {'class': 'project-software-name'}
                ).get_text()
                img = software.find('img').attrs['src']
                softwares[name] = img

            tags = []
            tags_html = artwork.find_all(
                'a',
                {'class': 'project-tag-item'}
            )
            for tag in tags_html:
                tags.append(tag.get_text())

            images = []
            images_html = artwork.find_all(
                'img',
                {'class': 'img img-fluid block-center img-fit'}
            )
            for image in images_html:
                images.append(image.attrs['src'])

        except Exception as err:
            print(f'Artwork data error: {err.args}')

        return Artwork(
                ObjectId(), title,
                description, date,
                likes, views,
                comments, softwares,
                tags, images
            )
