from HW_8.pages.base_page import BasePage
from selenium.webdriver.common.by import By
import allure
import logging


class LoginPage(BasePage):

    EMAIL_INPUT = (By.CSS_SELECTOR, "#field-email")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "#field-password")
    SUBMIT_BTN = (By.CSS_SELECTOR, "#submit-login")
    USER_INFO_BLOCK = (By.CSS_SELECTOR, '#_desktop_user_info .user-info')
    LOGOUT_LINK = (By.CSS_SELECTOR, 'a.logout')
    REGISTER_LINK = (By.CSS_SELECTOR, "a[data-link-action='display-register-form']")

    def open_login_page(self):
        with allure.step("Переход на страницу логина"):
            self.driver.get(f"{self.base_url}login")

    def enter_email(self, email):
        with allure.step(f"Ввод email: {email}"):
            input_el = self.wait_for_element(self.EMAIL_INPUT)
            input_el.click()
            input_el.send_keys(email)

    def enter_password(self, password):
        with allure.step(f"Ввод пароля: {'*' * len(password)}"):
            input_el = self.wait_for_element(self.PASSWORD_INPUT)
            input_el.click()
            input_el.send_keys(password)

    def click_sign_in(self):
        with allure.step("Клик по кнопке Sign In"):
            self.wait_for_clickable(self.SUBMIT_BTN).click()

    def assert_user_logged_in(self, expected_text):
        with allure.step(f"Проверка авторизации. Ожидание текста: {expected_text}"):
            text = self.wait_for_element(self.USER_INFO_BLOCK).text
            assert expected_text in text, f"Пользователь не авторизован. Текст блока: {text}"

    def assert_user_logged_out(self):
        with allure.step("Проверка выхода из системы"):
            text = self.wait_for_element(self.USER_INFO_BLOCK).text
            assert "Sign in" in text, f"Пользователь еще авторизован. Текст блока: {text}"

    def click_logout(self):
        with allure.step("Клик по кнопке Logout"):
            self.wait_for_element(self.LOGOUT_LINK).click()

    def get_register_link(self):
        return self.wait_for_element(self.REGISTER_LINK)