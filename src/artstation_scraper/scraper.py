from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from time import sleep
from bson import ObjectId
from .scraper_interface import ScraperInterface
from .models.project.artwork import Artwork
from .models.artist.artist import Base, Resume
from .utilities.artwork_extractors import (
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
from .utilities.artist_extractors import (
    _extract_resume_page_link,
    _extract_follows,
    _extract_interests,
    _extract_artwork_urls,
    _extract_avatar,
    _extract_name,
    _extract_headline,
    _extract_location,
    _extract_email,
    _extract_socials,
    _extract_sections,
    _extract_skills,
    _extract_sofware_proficiency,
    _extract_productions,
    _extract_experiences
)


class ArtstationScraper(ScraperInterface):

    def __init__(self, driver) -> None:
        self.driver = driver

    def get_html(self, url: str) -> BeautifulSoup:
        self.driver.get(url)
        sleep(5)
        while True:  # Open nested comments
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

    def get_artist_base_data(
            self, artist_html_content: BeautifulSoup
    ) -> Base:
        artist = artist_html_content
        try:
            resume_page_link = _extract_resume_page_link(artist)
            interests = _extract_interests(artist)
            followers, following = _extract_follows(artist)
            artwork_urls = _extract_artwork_urls(artist)
        except Exception as err:
            print(f'Artist base data error: {err.args}')
        return Base(resume_page_link, followers,
                    following, interests, artwork_urls)

    def get_artist_resume_data(
            self, artist_html_resume: BeautifulSoup
    ) -> Resume:
        artist = artist_html_resume
        try:
            avatar = _extract_avatar(artist)
            name = _extract_name(artist)
            headline = _extract_headline(artist)
            location = _extract_location(artist)
            email = _extract_email(artist)
            socials = _extract_socials(artist)
            summary, pdf = _extract_sections(artist)
            skills = _extract_skills(artist)
            softwares = _extract_sofware_proficiency(artist)
            productions = _extract_productions(artist)
            experiences = _extract_experiences(artist)
        except Exception as err:
            print(f'Artist resume data error: {err.args}')
        return Resume(avatar, name, headline,
                      location, email, socials,
                      summary, pdf, skills,
                      softwares, productions, experiences)

    def get_artwork_data(
            self, artwork_html_content: BeautifulSoup, artist_url: str
    ) -> Artwork:
        artwork = artwork_html_content
        try:
            title = _extract_title(artwork)
            description = _extract_description(artwork)
            date = _extract_date(artwork)
            likes = _extract_likes(artwork)
            views = _extract_views(artwork)
            threads = _extract_threads(artwork)
            comments = _extract_comments(artwork)
            softwares = _extract_softwares(artwork)
            tags = _extract_tags(artwork)
            images = _extract_images(artwork)
        except Exception as err:
            print(f'Artwork data error: {err.args}')
        return Artwork(ObjectId(), title, description,
                       date, likes, views, threads,
                       comments, softwares, tags,
                       images, artist_url)
