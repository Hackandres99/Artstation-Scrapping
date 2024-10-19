from bs4 import BeautifulSoup
from time import sleep
from .scraper_interface import ScraperInterface
from .models.project.artwork import Artwork
from .models.artist.artist import Base, Resume
from .models.artist.artwork_preview import Preview
from .utilities.scripts import (
    scroll_to_bottom,
    open_nested_comments
)
from .utilities.artwork_extractors import (
    extract_artist_url,
    extract_title,
    extract_description,
    extract_date,
    extract_likes,
    extract_views,
    extract_threads,
    extract_softwares,
    extract_tags,
    extract_images,
    extract_comments
)
from .utilities.artist_extractors import (
    extract_id_and_resume,
    extract_follows,
    extract_artworks_count,
    extract_interests,
    extract_artist_artwork_previews,
    extract_avatar,
    extract_name,
    extract_headline,
    extract_location,
    extract_email,
    extract_socials,
    extract_sections,
    extract_skills,
    extract_sofware_proficiency,
    extract_productions,
    extract_experiences
)


class ArtstationScraper(ScraperInterface):

    def __init__(self, driver) -> None:
        self.driver = driver

    def get_html(
        self, url: str, method: str, previews_number: int | str = 0
    ) -> BeautifulSoup:
        self.driver.get(url)
        match method:
            case 'artwork':
                sleep(3)
                open_nested_comments(self.driver)
            case 'previews':
                scroll_to_bottom(self.driver, previews_number)
            case _:
                sleep(2)
        content = self.driver.page_source
        html = BeautifulSoup(content, 'html.parser')
        return html

    def get_artist_base_data(
        self, artist_html_content: BeautifulSoup
    ) -> Base | None:
        artist = artist_html_content
        try:
            artist_id, resume_page_link = extract_id_and_resume(artist)
            interests = extract_interests(artist)
            followers, following = extract_follows(artist)
            artworks_count = extract_artworks_count(artist)
        except Exception as err:
            print(f'Artist base data error: {err.args}')
        return Base(artist_id, resume_page_link, followers,
                    following, artworks_count, interests)

    def get_artist_resume_data(
        self, artist_html_resume: BeautifulSoup
    ) -> Resume | None:
        artist = artist_html_resume
        try:
            avatar = extract_avatar(artist)
            name = extract_name(artist)
            headline = extract_headline(artist)
            location = extract_location(artist)
            email = extract_email(artist)
            socials = extract_socials(artist)
            summary, pdf = extract_sections(artist)
            skills = extract_skills(artist)
            softwares = extract_sofware_proficiency(artist)
            productions = extract_productions(artist)
            experiences = extract_experiences(artist)
        except Exception as err:
            print(f'Artist resume data error: {err.args}')
        return Resume(avatar, name, headline,
                      location, email, socials,
                      summary, pdf, skills,
                      softwares, productions, experiences)

    def get_artwork_data(
        self, artwork_html_content: BeautifulSoup, artwork_id: str
    ) -> Artwork | dict:
        artwork = artwork_html_content
        try:
            title = extract_title(artwork)
            description = extract_description(artwork)
            date = extract_date(artwork)
            likes = extract_likes(artwork)
            views = extract_views(artwork)
            threads = extract_threads(artwork)
            comments = extract_comments(artwork)
            softwares = extract_softwares(artwork)
            tags = extract_tags(artwork)
            images = extract_images(artwork)
            artist_url = extract_artist_url(artwork)
        except Exception:
            return dict(message='Artwork not found')

        return Artwork(artwork_id, title, description,
                       date, likes, views, threads,
                       comments, softwares, tags,
                       images, artist_url)

    def get_artist_artwork_previews(
        self, artist_html_content: BeautifulSoup, previews_number: int
    ) -> list[Preview]:
        artist = artist_html_content
        try:
            artwork_previews = extract_artist_artwork_previews(
                artist, previews_number
            )
        except Exception as err:
            print(f'Artworks data error: {err.args}')
        return artwork_previews
