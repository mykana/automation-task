"""
todo:
@User: lenovo
@Date: 2025-03-14
@Time: 4:16
May the father of the gods give me power!
"""
import pytest
from pages.login_page import LoginPage
import allure


@allure.feature('登录功能')
class TestLogin:
    @allure.story('成功登录')
    def test_successful_login(self, driver):
        login_page = LoginPage(driver)
        driver.get("https://example.com/login")

        with allure.step('输入正确的用户名和密码'):
            login_page.login("test_user", "correct_password")

        with allure.step('验证登录成功'):
            assert "dashboard" in driver.current_url

    @allure.story('登录失败')
    @pytest.mark.parametrize("username,password", [
        ("wrong_user", "wrong_pass"),
        ("", ""),
        ("test_user", "wrong_pass")
    ])
    def test_failed_login(self, driver, username, password):
        login_page = LoginPage(driver)
        driver.get("https://example.com/login")

        with allure.step(f'使用用户名 {username} 尝试登录'):
            login_page.login(username, password)

        with allure.step('验证显示错误信息'):
            error_message = driver.find_element(By.CLASS_NAME, "error-message")
            assert error_message.is_displayed()