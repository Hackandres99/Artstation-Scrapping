from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


def get_chrome_driver(port: int) -> Chrome:
    chrome_options = Options()
    chrome_options.add_argument(f'--remote-debugging-port={str(port)}')
    service = Service(ChromeDriverManager().install())
    driver = Chrome(service=service, options=chrome_options)
    return driver
