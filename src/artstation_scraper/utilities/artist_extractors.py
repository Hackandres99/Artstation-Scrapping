from bs4 import BeautifulSoup
from .numbers import suffix
from ..models.artist.resume import (
    Social, Sofware, Production, Experience
)
from ..models.artist.period import Period


def _extract_resume_page_link(artist: BeautifulSoup) -> str:
    _page = artist.find(
        'ul', {'class': 'addition-info-list'}
    ).find('a').attrs['href']
    resume_page_link = f'{_page}/resume'
    return resume_page_link


def _extract_follows(artist: BeautifulSoup) -> tuple[int, int]:
    conections_html = artist.find(
        'div', {'class': 'connections'}).find_all(
            'span', {'class': 'connection-item-count'}
        )
    followers = suffix(conections_html[0].get_text())
    following = suffix(conections_html[1].get_text())
    return followers, following


def _extract_interests(artist: BeautifulSoup) -> list:
    sidebar_blocks = artist.find_all('h4')
    interests = []
    for block in sidebar_blocks:
        if block.get_text() == 'Interested In':
            interests_html = block.find_next_sibling().find_all('span')
            for interest in interests_html:
                interests.append(interest.get_text())
    return interests


def _extract_artwork_urls(artist: BeautifulSoup) -> list:
    artwork_urls = []
    artworks = artist.find_all(
        'projects-list-item', {'class': 'gallery-grid-item'}
    )
    for i, artwork in enumerate(artworks):
        try:
            artwork_url = artwork.find(
                'a', {'class': 'gallery-grid-link'}
            ).attrs['href']
            artwork_urls.append(artwork_url)
        except Exception as err:
            print(f'{i + 1}.- Artwork url error: {err.args}')
    return artwork_urls


def _extract_avatar(artist: BeautifulSoup) -> str:
    return artist.find(
        'div', {'class': 'about-photo'}
    ).find('img').attrs['src']


def _extract_name(artist: BeautifulSoup) -> str:
    return artist.find(
        'div', {'class': 'about-name'}
    ).get_text()


def _extract_headline(artist: BeautifulSoup) -> str:
    return artist.find(
        'div', {'class': 'about-position'}
    ).get_text()


def _extract_location(artist: BeautifulSoup) -> str:
    return artist.find(
        'div', {'class': 'about-location'}
    ).contents[1]


def _extract_email(artist: BeautifulSoup) -> str:
    return artist.find(
        'div', {'class': 'about-email'}
    ).find('a').get_text()


def _extract_socials(artist: BeautifulSoup) -> list:
    socials = []
    socials_html = artist.find_all('div', {'class': 'so-item'})
    for social_html in socials_html:
        image: str = social_html.find('a').attrs['href']
        start = image.index('.') + 1
        end = image.index('.', start)
        social_name = image[start:end]
        social = Social(social_name, image)
        socials.append(social)
    return socials


def _extract_sections(artist: BeautifulSoup) -> list:
    sections = ['', '']
    sections_html = artist.find_all('h2')
    for section in sections_html:
        if section.get_text() == 'Summary':
            sections[0] = section.find_next_sibling().get_text()
        if section.get_text() == 'Resume PDF':
            sections[1] = section.find_next_sibling().attrs['href']
    return sections


def _extract_skills(artist: BeautifulSoup) -> list:
    skills = []
    skills_html = artist.find('div', {'class': 'tag-list'}).find_all('span')
    for skill in skills_html:
        skills.append(skill.get_text())
    return skills


def _extract_sofware_proficiency(artist: BeautifulSoup) -> list:
    softwares = []
    softwares_html = artist.find_all('div', {'class': 'software-icon-item'})
    for software in softwares_html:
        software_name = software.find('img').find_next_sibling().get_text()
        software_image = software.find('img').attrs['src']
        softwares.append(Sofware(software_name, software_image))
    return softwares


def _extract_productions(artist: BeautifulSoup) -> list:
    productions = []
    productions_html = artist.find_all('li', {'class': 'production-item'})
    for production in productions_html:
        production_image = production.find('img').attrs['src']
        _type = production.find(
            'div', {'class': 'production-info-label'}
        ).get_text()
        values = production.find_all('div', {'class': 'production-info-value'})
        production_name = values[0].get_text()
        year = values[1].get_text()
        role = values[2].get_text()
        company = values[3].get_text()

        productions.append(Production(
            _type, production_name,
            production_image, year,
            role, company
        ))
    return productions


def _extract_experiences(artist: BeautifulSoup) -> list:
    experiences = []
    experiences_html = artist.find_all('li', {'class', 'experience-item'})
    for experience in experiences_html:
        experience_role = experience.find(
            'div', {'class': 'experience-job'}
        ).get_text()
        experience_location = experience.find(
            'div', {'class': 'experience-location'}
        ).get_text()
        period_text = experience.find(
            'div', {'class': 'experience-period'}
        ).get_text()
        _index = period_text.index('-')
        date1 = period_text[:_index].strip()
        date2 = period_text[_index + 1:].strip()
        period = Period(date1, date2)
        description = ''
        descriptions_html = experience.find(
            'div', {'class': 'experience-description'}
        ).find_all('p')
        for description_html in descriptions_html:
            description += description_html.get_text()
        experiences.append(Experience(
            experience_role, experience_location,
            period, description))
    return experiences
