"""
todo:
@User: lenovo
@Date: 2025-03-14
@Time: 4:16
May the father of the gods give me power!
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def create_driver(headless=True):
    """创建配置好的WebDriver实例"""
    options = Options()
    if headless:
        options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    return driver