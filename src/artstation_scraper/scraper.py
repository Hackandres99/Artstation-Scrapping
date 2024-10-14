from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup, Tag
from time import sleep
from dateutil import parser
from bson import ObjectId
from .models.project.artwork import Artwork
from .models.project.comment import Comment, User, Message
from .scraper_interface import ScraperInterface
from .utilities.numbers import suffix


class ArtstationScraper(ScraperInterface):
    def __init__(self, driver) -> None:
        self.driver = driver

    def get_html(self, url: str) -> BeautifulSoup:
        self.driver.get(url)
        sleep(5)

        # Abrir comentarios anidados
        while True:
            load_data = self.driver.find_elements(By.CSS_SELECTOR, 'a.btn.load-more')
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
        artworks = artist_html_content.find_all('projects-list-item', {'class': 'gallery-grid-item'})
        for i, p in enumerate(artworks):
            try:
                artwork_url = p.find('a', {'class': 'gallery-grid-link'}).attrs['href']
                artwork_urls.append(artwork_url)
            except Exception as err:
                print(f'{i + 1}.- Artwork url error: {err.args}')
        return artwork_urls

    def _extract_title(self, artwork: BeautifulSoup) -> str:
        return artwork.find('h3', {'class': 'project-description-title'}).get_text()

    def _extract_description(self, artwork: BeautifulSoup) -> str:
        return artwork.find('read-more', {'class': 'project-description'}).get_text()

    def _extract_date(self, artwork: BeautifulSoup):
        return parser.parse(artwork.find('time', {'class': 'project-published'}).attrs['datetime'])

    def _extract_likes(self, artwork: BeautifulSoup) -> int:
        likes_html = artwork.find('button', {'class': 'btn btn-reset'})
        return suffix(likes_html.contents[1]) if likes_html else 0

    def _extract_views(self, artwork: BeautifulSoup) -> int:
        return suffix(artwork.find('i', {'class': 'far fa-eye'}).next_sibling.next_sibling)

    def _extract_threads(self, artwork: BeautifulSoup) -> int:
        return suffix(artwork.find('i', {'class': 'far fa-comments'}).next_sibling.next_sibling)

    def _extract_comments(self, artwork: BeautifulSoup) -> list:
        comments = []
        artwork_comments = artwork.find('ul', {'class': 'project-comments'})
        if artwork_comments:
            comment_items = artwork_comments.find_all('li', recursive=False)
            comments = self._extract_comment(comment_items)
        return comments

    def _extract_user_info(self, comment_item: Tag):
        user_avatar = comment_item.find('img').attrs['src']
        username = comment_item.find('img').attrs['alt']
        user_headline = comment_item.find('div', {'class': 'project-comment-headline'}).attrs['title']
        author = True if comment_item.find('div', {'class': 'author-badge'}) else False
        
        return User(username, author, user_avatar, user_headline)

    def _extract_comment_details(self, comment_details: Tag):
        text_html = comment_details.find('div', {'class': 'project-comment-text'}).find('p')
        text = text_html.get_text() if text_html else ''

        comment_likes_html = comment_details.find('show-likes-button')
        comment_likes = suffix(comment_likes_html.find('div').find('button').find('span').next_sibling) if comment_likes_html else 0

        comment_date = parser.parse(comment_details.find('time', {'class': 'project-comment-published'}).attrs['title'])
        
        return Message(text, comment_likes, comment_date)
    
    def _extract_comment(self, comment_items: list) -> list:
        comments = []
        for comment_item in comment_items:
            if isinstance(comment_item, Tag):
                comment_details = comment_item.find('div', {'class': 'project-comment-item'})
                user_info = self._extract_user_info(comment_item)
                comment_detail = self._extract_comment_details(comment_details)

                # Obtener comentarios anidados, si existen
                nested_comments_html = comment_details.find_next_siblings()
                nested_comments = self._extract_comment(nested_comments_html) if nested_comments_html else []

                comment = Comment(
                    ObjectId(),
                    user_info,
                    comment_detail,
                    nested_comments
                )
                comments.append(comment)
        return comments

    def _extract_softwares(self, artwork: BeautifulSoup) -> dict:
        softwares = {}
        softwares_html = artwork.find_all('a', {'class': 'project-software-item'})
        for software in softwares_html:
            name = software.find('span', {'class': 'project-software-name'}).get_text()
            img = software.find('img').attrs['src']
            softwares[name] = img
        return softwares

    def _extract_tags(self, artwork: BeautifulSoup) -> list:
        return [tag.get_text() for tag in artwork.find_all('a', {'class': 'project-tag-item'})]

    def _extract_images(self, artwork: BeautifulSoup) -> list:
        return [image.attrs['src'] for image in artwork.find_all('img', {'class': 'img img-fluid block-center img-fit'})]

    def get_artwork_data(self, artwork_html_content: BeautifulSoup) -> Artwork:
        artwork = artwork_html_content
        try:
            title = self._extract_title(artwork)
            description = self._extract_description(artwork)
            date = self._extract_date(artwork)
            likes = self._extract_likes(artwork)
            views = self._extract_views(artwork)
            threads = self._extract_threads(artwork)

            # Obtener comentarios principales y anidados
            comments = self._extract_comments(artwork)

            softwares = self._extract_softwares(artwork)
            tags = self._extract_tags(artwork)
            images = self._extract_images(artwork)

        except Exception as err:
            print(f'Artwork data error: {err.args}')

        return Artwork(title, description, date, likes, views, threads, comments, softwares, tags, images)
