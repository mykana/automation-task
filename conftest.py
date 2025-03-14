"""
todo:
@User: lenovo
@Date: 2025-03-14
@Time: 4:15
May the father of the gods give me power!
"""
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture(scope="session")
def driver():
    """创建共享的WebDriver实例"""
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')  # 无界面模式
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )
    driver.implicitly_wait(10)
    yield driver
    driver.quit()