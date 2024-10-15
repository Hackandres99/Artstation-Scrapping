from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bson import ObjectId
from artstation_scraper.scraper import ArtstationScraper
from artstation_scraper.models.artist.artist import Artist
# from artstation_scraper.MDB_connection import ArtworkRepository


def wdriver(port: int):
    chrome_options = Options()
    chrome_options.add_argument(f'--remote-debugging-port={str(port)}')
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver


def get_artist():
    ...


def get_artwork():
    ...


def get_artworks():
    ...


def main():
    artist = 'onyricstudio'  # Enter artist name
    artstation_url = 'https://www.artstation.com/'
    artist_url = artstation_url + artist

    driver = wdriver(9222)
    artstation_Scraper = ArtstationScraper(driver)

    artist_Html = artstation_Scraper.get_html(artist_url)
    artist_base_data = artstation_Scraper.get_artist_base_data(artist_Html)

    artist_html_resume = artstation_Scraper.get_html(
        artist_base_data.resume_page
    )
    artist_resume_data = artstation_Scraper.get_artist_resume_data(
        artist_html_resume
    )

    print(Artist(ObjectId(), artist_base_data, artist_resume_data))

    for i, artwork in enumerate(artist_base_data.artwork_urls):
        artwork_index = 27  # To choose the artwork, change index
        if i == artwork_index - 1:
            artwork_Html = artstation_Scraper.get_html(artwork)
            artwork = artstation_Scraper.get_artwork_data(
                artwork_Html, artist_url
            )
            print(artwork)
        # ArtworkRepository().save_artwork(artwork)
        # print(f'Artwork {i + 1} saved successfully.')


if __name__ == '__main__':
    main()
