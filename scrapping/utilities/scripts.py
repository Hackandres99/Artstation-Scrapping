from time import sleep
from selenium.webdriver.common.by import By


def scroll_to_bottom(driver, previews_number):
    last_height = driver.execute_script(
        "return document.body.scrollHeight"
    )
    num = previews_number
    if str(num).isalpha():
        scrolls_number = 0
        if num == 'all':
            scrolls_number = 1
    else:
        scrolls_number = 0 if num < 51 else 3 if num < 101 else 4 + (
            num - 101) // 50

    scrolls = 0
    while scrolls < scrolls_number:
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);"
        )
        sleep(2)
        new_height = driver.execute_script(
            "return document.body.scrollHeight"
        )
        if new_height == last_height:
            break
        last_height = new_height
        if num != 'all':
            scrolls += 1
    else:
        sleep(2)


def open_nested_comments(driver):
    while True:
        load_comments = driver.find_elements(
            By.CSS_SELECTOR, 'a.btn.load-more'
        )
        if not load_comments:
            break
        for comments in load_comments:
            comments.click()
            sleep(1)


def open_sidebar(driver):
    load_base_data = driver.find_elements(
        By.CSS_SELECTOR, 'button.desktop-toggle-btn'
    )
    if load_base_data:
        load_base_data[0].click()
