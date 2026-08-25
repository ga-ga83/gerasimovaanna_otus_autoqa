from HW_7.pages.base_page import BasePage
from selenium.webdriver.common.by import By


class LoginPage(BasePage):


    EMAIL_INPUT = (By.CSS_SELECTOR, "#field-email")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "#field-password")
    SUBMIT_BTN = (By.CSS_SELECTOR, "#submit-login")
    USER_INFO_BLOCK = (By.CSS_SELECTOR, '#_desktop_user_info .user-info')
    LOGOUT_LINK = (By.CSS_SELECTOR, 'a.logout')
    REGISTER_LINK = (By.CSS_SELECTOR, "a[data-link-action='display-register-form']")

    def open_login_page(self):
        self.driver.get(f"{self.base_url}login")


    def enter_email(self, email):
        input_el = self.wait_for_element(self.EMAIL_INPUT)
        input_el.click()
        input_el.send_keys(email)

    def enter_password(self, password):
        input_el = self.wait_for_element(self.PASSWORD_INPUT)
        input_el.click()
        input_el.send_keys(password)

    def click_sign_in(self):
        self.wait_for_clickable(self.SUBMIT_BTN).click(), "Кнопка входа на странице не отображается"

    def assert_user_logged_in(self, expected_text):
        text = self.wait_for_element(self.USER_INFO_BLOCK).text
        assert expected_text in text, f"Пользователь не авторизован. Текст блока: {text}"

    def assert_user_logged_out(self):
        text = self.wait_for_element(self.USER_INFO_BLOCK).text
        assert "Sign in" in text, f"Пользователь еще авторизован, выход не был осуществлен. Текст блока: {text}"

    def click_logout(self):
        self.wait_for_element(self.LOGOUT_LINK).click()

    def get_register_link(self):
        return self.wait_for_element(self.REGISTER_LINK)
