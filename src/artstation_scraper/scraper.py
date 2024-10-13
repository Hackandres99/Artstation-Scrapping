from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup, Tag
from time import sleep
from dateutil import parser
from bson import ObjectId
from .models.project.artwork import Artwork, Comment
from .models.project.user import User
from .scraper_interface import ScraperInterface
from .utilities.numbers import suffix


class ArtstationScraper(ScraperInterface):
    def __init__(self, driver) -> None:
        self.driver = driver

    def get_html(self, url: str) -> BeautifulSoup:
        self.driver.get(url)
        sleep(5)

        # To open nested comments
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
            title = artwork.find(
                'h3', {'class': 'project-description-title'}
            ).get_text()

            description = artwork.find(
                'read-more', {'class': 'project-description'}
            ).get_text()

            date = parser.parse(artwork.find(
                'time', {'class': 'project-published'}
            ).attrs['datetime'])

            likes_html = artwork.find(
                'button', {'class': 'btn btn-reset'}
            )
            likes = suffix(likes_html.contents[1]) if likes_html else 0

            views = suffix(artwork.find(
                'i', {'class': 'far fa-eye'}
            ).next_sibling.next_sibling)

            threads = suffix(artwork.find(
                'i', {'class': 'far fa-comments'}
            ).next_sibling.next_sibling)

            comments = []
            artwork_comments = artwork.find(
                'ul', {'class': 'project-comments'}
            )
            if artwork_comments:
                artwork_comments = artwork_comments.find_all(
                    'li', recursive=False
                )
                for i, artwork_comment in enumerate(artwork_comments):
                    if isinstance(artwork_comment, Tag):
                        user_avatar = artwork_comment.find(
                            'img').attrs['src']

                        username = artwork_comment.find(
                            'img').attrs['alt']

                        comment_item = artwork_comment.find(
                            'div', {'class': 'project-comment-item'}
                        )

                        author_html = comment_item.find(
                            'div', {'class': 'author-badge'}
                        )
                        author = True if author_html else False

                        user_headline = comment_item.find(
                            'div', {'class': 'project-comment-headline'}
                        ).attrs['title']

                        message_html = comment_item.find(
                            'div', {'class': 'project-comment-text'}
                        ).find('p')
                        message = (
                            message_html.get_text() if message_html else ''
                        )

                        comment_likes_html = comment_item.find(
                            'show-likes-button')
                        comment_likes = suffix(comment_likes_html.find(
                            'div').find('button').find(
                            'span').next_sibling) if comment_likes_html else 0

                        comment_date = parser.parse(comment_item.find(
                            'time', {'class': 'project-comment-published'}
                        ).attrs['title'])

                        nested_comments = []
                        nestedCommentsHtml = comment_item.find_next_siblings()
                        for nested_comment_item in nestedCommentsHtml:

                            nested_comment = nested_comment_item.find(
                                'project-comment-item'
                            )

                            nested_user_avatar = nested_comment.find(
                                'img').attrs['src']

                            nested_username = nested_comment.find(
                                'img').attrs['alt']

                            nested_item = nested_comment.find(
                                'div', {'class': 'project-comment-item'}
                            )

                            nested_author = nested_item.find(
                                'div', {'class': 'author-badge'}
                            )
                            nested_author = True if nested_author else False

                            nested_user_headline = nested_item.find(
                                'div', {'class': 'project-comment-headline'}
                            ).attrs['title']

                            nestedMessage = nested_item.find(
                                'div', {'class': 'project-comment-text'}
                            ).find('p')
                            nestedMessage = (
                                nestedMessage.text if nestedMessage else ''
                            )

                            nested_likes = nested_item.find(
                                'show-likes-button'
                            )
                            nested_likes = suffix(nested_likes.find(
                                'div').find('button').find(
                                'span').next_sibling) if nested_likes else 0

                            nested_date = parser.parse(nested_item.find(
                                'time', {'class': 'project-comment-published'}
                            ).attrs['title'])

                            nested = Comment(ObjectId(), User(
                                nested_username, nested_author,
                                nested_user_avatar, nested_user_headline),
                                nestedMessage, nested_likes, nested_date, []
                            )
                            nested_comments.append(nested)

                        comment = Comment(ObjectId(), User(
                            username, author, user_avatar,
                            user_headline), message, comment_likes,
                            comment_date, nested_comments
                        )
                        comments.append(comment)

            softwares = {}
            softwares_html = artwork.find_all(
                'a', {'class': 'project-software-item'}
            )
            for software in softwares_html:
                name = software.find(
                    'span', {'class': 'project-software-name'}
                ).get_text()
                img = software.find('img').attrs['src']
                softwares[name] = img

            tags = []
            tags_html = artwork.find_all(
                'a', {'class': 'project-tag-item'}
            )
            for tag in tags_html:
                tags.append(tag.get_text())

            images = []
            images_html = artwork.find_all(
                'img', {'class': 'img img-fluid block-center img-fit'}
            )
            for image in images_html:
                images.append(image.attrs['src'])

        except Exception as err:
            print(f'Artwork data error: {err.args}')

        return Artwork(title, description,
                       date, likes, views,
                       threads, comments,
                       softwares, tags, images
                       )
