from bs4 import BeautifulSoup, Tag
from dateutil import parser
from ..models.project.comment import User, Message
from .numbers import suffix

def _extract_title(artwork: BeautifulSoup) -> str:
    return artwork.find('h3', {'class': 'project-description-title'}).get_text()

def _extract_description(artwork: BeautifulSoup) -> str:
    return artwork.find('read-more', {'class': 'project-description'}).get_text()

def _extract_date(artwork: BeautifulSoup):
    return parser.parse(artwork.find('time', {'class': 'project-published'}).attrs['datetime'])

def _extract_likes(artwork: BeautifulSoup) -> int:
    likes_html = artwork.find('button', {'class': 'btn btn-reset'})
    return suffix(likes_html.contents[1]) if likes_html else 0

def _extract_views(artwork: BeautifulSoup) -> int:
    return suffix(artwork.find('i', {'class': 'far fa-eye'}).next_sibling.next_sibling)

def _extract_threads(artwork: BeautifulSoup) -> int:
    return suffix(artwork.find('i', {'class': 'far fa-comments'}).next_sibling.next_sibling)

def _extract_softwares(artwork: BeautifulSoup) -> dict:
    softwares = {}
    softwares_html = artwork.find_all('a', {'class': 'project-software-item'})
    for software in softwares_html:
        name = software.find('span', {'class': 'project-software-name'}).get_text()
        img = software.find('img').attrs['src']
        softwares[name] = img
    return softwares

def _extract_tags(artwork: BeautifulSoup) -> list:
    return [tag.get_text() for tag in artwork.find_all('a', {'class': 'project-tag-item'})]

def _extract_images(artwork: BeautifulSoup) -> list:
    return [image.attrs['src'] for image in artwork.find_all('img', {'class': 'img img-fluid block-center img-fit'})]

def _extract_user_info(comment_item: Tag) -> User:
    user_avatar = comment_item.find('img').attrs['src']
    username = comment_item.find('img').attrs['alt']
    user_headline = comment_item.find('div', {'class': 'project-comment-headline'}).attrs['title']
    author = True if comment_item.find('div', {'class': 'author-badge'}) else False

    return User(username, author, user_avatar, user_headline)

def _extract_comment_details(comment_details: Tag) -> Message:
    text_html = comment_details.find('div', {'class': 'project-comment-text'}).find('p')
    text = text_html.get_text() if text_html else ''

    comment_likes_html = comment_details.find('show-likes-button')
    comment_likes = suffix(comment_likes_html.find('div').find('button').find('span').next_sibling) if comment_likes_html else 0

    comment_date = parser.parse(comment_details.find('time', {'class': 'project-comment-published'}).attrs['title'])
    
    return Message(text, comment_likes, comment_date)
