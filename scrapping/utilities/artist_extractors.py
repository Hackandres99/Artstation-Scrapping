from bs4 import BeautifulSoup
from .numbers import suffix
from ..models.artist.resume import (
    Social, Sofware, Production, Experience
)
from ..models.artist.period import Period
from ..models.artist.artwork_preview import Preview


def extract_id_and_resume(artist: BeautifulSoup) -> list:
    id_and_resume = ['', '']
    _page_html = artist.find(
        'ul', {'class': 'addition-info-list'}
    )

    id_html = _page_html.find('a').get_text() if _page_html else ''
    end = id_html[: id_html.rindex('.')].rindex('.') if id_html != '' else 0
    id_and_resume[0] = id_html[: end] if end != 0 else ''

    _page = _page_html.find('a').attrs['href'] if _page_html else ''
    id_and_resume[1] = f'{_page}/resume'

    return id_and_resume


def extract_follows(artist: BeautifulSoup) -> list:
    follows = [0, 0]
    conections_html = artist.find('div', {'class': 'connections'})
    conections_html = conections_html.find_all(
        'span', {'class': 'connection-item-count'}
    ) if conections_html else '  '
    followers_html = conections_html[0]
    following_html = conections_html[1]
    follows[0] = suffix(
        followers_html.get_text()
        ) if followers_html != ' ' else 0
    follows[1] = suffix(
        following_html.get_text()
        ) if following_html != ' ' else 0
    return follows


def extract_artworks_count(artist: BeautifulSoup) -> int:
    count_html = artist.find('page-header')
    count_html = count_html.find(
        'div', {'class': 'profile-page-info'}
    ) if count_html else ''
    count_text = count_html.get_text() if count_html else 0
    end = count_text.index(' ') if count_text != 0 else 0
    count = suffix(count_text[:end]) if end != 0 else 0
    return count


def extract_interests(artist: BeautifulSoup) -> list:
    sidebar_blocks = artist.find_all('h4')
    interests = []
    for block in sidebar_blocks:
        if block.get_text() == 'Interested In':
            interests_html = block.find_next_sibling().find_all('span')
            for interest in interests_html:
                interests.append(interest.get_text())
    return interests


def extract_artist_artwork_previews(
    artist: BeautifulSoup, previews_number: int | str
) -> list:
    artwork_previews = []
    artworks = artist.find_all(
        'projects-list-item', {'class': 'gallery-grid-item'}
    )
    for order, artwork in enumerate(artworks):
        try:

            artwork_html = artwork.find(
                'a', {'class': 'gallery-grid-link'}
            )
            url = artwork_html.attrs['href'] if artwork_html else ''

            start = url.rindex('/')
            id = url[start + 1:]

            image_html = artwork_html.find(
                'img', {'class': 'gallery-grid-background-image'}
            )
            image = image_html.attrs['src'] if image_html else ''

            title_html = artwork_html.find(
                'div', {'class': 'gallery-grid-title'}
            )
            title = title_html.get_text() if title_html else ''

            if order == previews_number:
                break
            artwork_previews.append(Preview(id, order + 1, title, image, url))
        except Exception as err:
            print(f'{order + 1}.- Artwork preview error: {err.args}')

    if str(previews_number).isalpha():
        return artwork_previews if previews_number == 'all' else []
    else:
        return artwork_previews if previews_number > 0 else []


def extract_avatar(artist: BeautifulSoup) -> str:
    avatar_html = artist.find(
        'div', {'class': 'about-photo'}
    ).find('img')
    avatar = avatar_html.attrs['src'] if avatar_html else ''
    return avatar


def extract_name(artist: BeautifulSoup) -> str:
    name_html = artist.find(
        'div', {'class': 'about-name'}
    )
    name = name_html.get_text() if name_html else ''
    return name


def extract_headline(artist: BeautifulSoup) -> str:
    headline_html = artist.find(
        'div', {'class': 'about-position'}
    )
    headline = headline_html.get_text() if headline_html else ''
    return headline


def extract_location(artist: BeautifulSoup) -> str:
    location_html = artist.find(
        'div', {'class': 'about-location'}
    )
    location = location_html.contents[1] if location_html else ''
    return location


def extract_email(artist: BeautifulSoup) -> str:
    email_html = artist.find(
        'div', {'class': 'about-email'}
    ).find('a')
    email = email_html.get_text() if email_html else ''
    return email


def extract_socials(artist: BeautifulSoup) -> list:
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


def extract_sections(artist: BeautifulSoup) -> list:
    sections = ['', '']
    sections_html = artist.find_all('h2')
    for section in sections_html:
        if section.get_text() == 'Summary':
            sections[0] = section.find_next_sibling().get_text()
        if section.get_text() == 'Resume PDF':
            sections[1] = section.find_next_sibling().attrs['href']
    return sections


def extract_skills(artist: BeautifulSoup) -> list:
    skills = []
    skills_html = artist.find('div', {'class': 'tag-list'}).find_all('span')
    for skill in skills_html:
        skills.append(skill.get_text())
    return skills


def extract_sofware_proficiency(artist: BeautifulSoup) -> list:
    softwares = []
    softwares_html = artist.find_all('div', {'class': 'software-icon-item'})
    for software in softwares_html:
        software_name = software.find('img').find_next_sibling().get_text()
        software_image = software.find('img').attrs['src']
        softwares.append(Sofware(software_name, software_image))
    return softwares


def extract_productions(artist: BeautifulSoup) -> list:
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


def extract_experiences(artist: BeautifulSoup) -> list:
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
