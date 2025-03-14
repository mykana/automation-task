"""
todo:
@User: lenovo
@Date: 2025-03-14
@Time: 4:16
May the father of the gods give me power!
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.username_input = (By.ID, "username")
        self.password_input = (By.ID, "password")
        self.login_button = (By.ID, "login-button")

    def login(self, username, password):
        """执行登录操作"""
        self.driver.find_element(*self.username_input).send_keys(username)
        self.driver.find_element(*self.password_input).send_keys(password)
        self.driver.find_element(*self.login_button).click()

        # 等待登录成功
        WebDriverWait(self.driver, 10).until(
            EC.url_contains("/dashboard")
        )