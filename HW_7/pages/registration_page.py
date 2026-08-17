from HW_7.pages.base_page import BasePage
from selenium.webdriver.common.by import By

class RegistrationPage(BasePage):

    HEADER_REGISTRATION_PAGE = (By.CSS_SELECTOR, ".page-header h1")
    FIRSTNAME_INPUT = (By.CSS_SELECTOR, "#field-firstname")
    LASTNAME_INPUT = (By.CSS_SELECTOR, "#field-lastname")
    SAVE_BUTTON = (By.CSS_SELECTOR, "button[data-link-action='save-customer']")

    def assert_header_text(self, expected_text):
        text = self.wait_for_element(self.HEADER_REGISTRATION_PAGE).text
        assert text.strip() == expected_text, f"Отображаемый текст заголовка '{text}' не совпадает с ожидаемым. Ожидаемый текст: {expected_text}"

    def assert_firstname(self):
        el = self.wait_for_element(self.FIRSTNAME_INPUT)
        assert el.is_displayed(), "Поле ввода имени (firstname) не отображается на странице"

    def assert_lastname(self):
        el = self.wait_for_element(self.LASTNAME_INPUT)
        assert el.is_displayed(), "Поле ввода имени (lastname) не отображается на странице"

    def assert_save_button(self):
        el = self.wait_for_clickable(self.SAVE_BUTTON)
        assert el.is_displayed(), "Кнопка Сохранить не отображается на странице"