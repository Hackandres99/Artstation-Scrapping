from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from artstation_scraper.scraper import ArtstationScraper
from artstation_scraper.MDB_connection import ArtworkRepository


def wdriver(port: int):
    chrome_options = Options()
    chrome_options.add_argument(f'--remote-debugging-port={str(port)}')
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver


def main():
    artist = 'onyricstudio'
    # artist = input('Enter artist name: ')
    artstation_Url = 'https://www.artstation.com/'
    artist_Url = artstation_Url + artist
    driver = wdriver(9222)
    artstation_Scraper = ArtstationScraper(driver)
    artist_Html = artstation_Scraper.get_html(artist_Url)
    arttist_Artworks = artstation_Scraper.get_artwork_urls(artist_Html)

    for i, artwork in enumerate(arttist_Artworks):
        artwork_Html = artstation_Scraper.get_html(artwork)
        artwork = artstation_Scraper.get_artwork_data(artwork_Html)
        ArtworkRepository().save_artwork(artwork)
        print(f'Artwork {i + 1} saved successfully.')


if __name__ == '__main__':
    main()
