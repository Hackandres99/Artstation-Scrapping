import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup, Tag
from bson import ObjectId
from datetime import datetime
from .numbers import suffix
from dateutil import parser
from ..models.project.comment import Comment, User, Message
from ..models.software_proficiency import Sofware


def extract_title(artwork: BeautifulSoup) -> str:
    title_html = artwork.find(
        'h3', {'class': 'project-description-title'}
    )
    title = title_html.get_text() if title_html else ''
    return title


def extract_description(artwork: BeautifulSoup) -> str:
    description_html = artwork.find(
        'read-more', {'class': 'project-description'}
    )
    description = description_html.get_text() if description_html else ''
    return description


def extract_date(artwork: BeautifulSoup) -> datetime:
    date_html = artwork.find(
        'time', {'class': 'project-published'}
    )
    date = parser.parse(
        date_html.attrs['datetime']
    ) if date_html else datetime.min
    return date


def extract_likes(artwork: BeautifulSoup) -> int:
    likes_html = artwork.find('button', {'class': 'btn btn-reset'})
    likes = suffix(likes_html.contents[1]) if likes_html else 0
    return likes


def extract_views(artwork: BeautifulSoup) -> int:
    views_html = artwork.find(
        'i', {'class': 'far fa-eye'}
    )
    views = views = suffix(
        views_html.next_sibling.next_sibling
    ) if views_html else 0
    return views


def extract_threads(artwork: BeautifulSoup) -> int:
    threads_html = artwork.find(
        'i', {'class': 'far fa-comments'}
    )
    threads = threads = suffix(
        threads_html.next_sibling.next_sibling
    ) if threads_html else 0
    return threads


def extract_softwares(artwork: BeautifulSoup) -> list:
    softwares = []
    softwares_html = artwork.find_all('a', {'class': 'project-software-item'})
    for software in softwares_html:
        name_html = software.find(
            'span', {'class': 'project-software-name'}
        )
        name = name_html.get_text() if name_html else ''
        img_html = software.find('img')
        img = img_html.attrs['src'] if img_html else ''
        softwares.append(Sofware(name, img))
    return softwares


def extract_tags(artwork: BeautifulSoup) -> list:
    return [tag.get_text() if tag else '' for tag in artwork.find_all(
        'a', {'class': 'project-tag-item'}
    )]


def extract_images(artwork: BeautifulSoup) -> list:
    return [image.attrs['src'] if image else '' for image in artwork.find_all(
        'img', {'class': 'img img-fluid block-center img-fit'}
    )]


def extract_artist_url(artwork: BeautifulSoup) -> str:
    load_dotenv()
    artist_id_html = artwork.find(
        'div', {'class': 'project-author-name'}
    ).find('a')
    artist_id = (artist_id_html.attrs['href'])[1:] if artist_id_html else ''
    artist_url = os.getenv('ARTSTATION_URL') + artist_id
    return artist_url


def extract_user_info(comment_item: Tag):
    avatar_html = comment_item.find('img')
    avatar = avatar_html.attrs['src'] if avatar_html else ''

    name_html = comment_item.find(
        'div', {'class': 'project-comment-user'}
    ).find('a')
    name = name_html.get_text() if name_html else ''

    headline_html = comment_item.find(
        'div', {'class': 'project-comment-headline'}
    )
    headline = headline_html.attrs['title'] if headline_html else ''

    author_html = name_html.find_next_sibling(
        'div', {'class': 'author-badge'}
    )
    author = True if author_html else False

    return User(name, author, avatar, headline)


def extract_comment_details(comment_details: Tag):
    text_html = comment_details.find(
        'div', {'class': 'project-comment-text'}
    ).find('p')
    text = text_html.get_text() if text_html else ''

    likes_html = comment_details.find('show-likes-button')
    likes = suffix(likes_html.find('div').find('button').find(
        'span').next_sibling) if likes_html else 0

    date_html = comment_details.find(
        'time', {'class': 'project-comment-published'}
    )
    date = parser.parse(
        date_html.attrs['title']
    ) if date_html else datetime.min
    return Message(text, likes, date)


def extract_comment(comment_items: list) -> list:
    comments = []
    for comment_item in comment_items:
        if isinstance(comment_item, Tag):
            comment_details = comment_item.find(
                'div', {'class': 'project-comment-item'}
            )
            user_info = extract_user_info(comment_item)
            comment_detail = extract_comment_details(comment_details)
            # Obtener comentarios anidados, si existen
            nested_comments_html = comment_details.find_next_siblings()
            nested_comments = extract_comment(
                nested_comments_html
            ) if nested_comments_html else []
            comment = Comment(
                ObjectId(),
                user_info,
                comment_detail,
                nested_comments
            )
            comments.append(comment)
    return comments


def extract_comments(artwork: BeautifulSoup) -> list:
    comments = []
    artwork_comments = artwork.find('ul', {'class': 'project-comments'})
    if artwork_comments:
        comment_items = artwork_comments.find_all('li', recursive=False)
        comments = extract_comment(comment_items)
    return comments
