from HW_8.pages.base_page import BasePage
from selenium.webdriver.common.by import By
import allure
import logging


class RegistrationPage(BasePage):

    HEADER_REGISTRATION_PAGE = (By.CSS_SELECTOR, ".page-header h1")
    FIRSTNAME_INPUT = (By.CSS_SELECTOR, "#field-firstname")
    LASTNAME_INPUT = (By.CSS_SELECTOR, "#field-lastname")
    SAVE_BUTTON = (By.CSS_SELECTOR, "button[data-link-action='save-customer']")
    SELECT_RADIO_BTH = (By.CSS_SELECTOR, "input[name='id_gender'][value='1']")
    EMAIL_INPUT = (By.CSS_SELECTOR, "#field-email")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "#field-password")
    CHECK_BOOKS_TERMS = (By.XPATH, "//label[contains(., 'I agree to the terms')]")
    CHECK_BOOKS_CUSTOMER = (By.XPATH, "//label[contains(., 'Customer data privacy')]")


    def assert_header_text(self, expected_text):
        with allure.step(f'Проверка заголовка на странице регистрации'):
            text = self.wait_for_element(self.HEADER_REGISTRATION_PAGE).text
            assert text.strip() == expected_text, f"Отображаемый текст заголовка '{text}' не совпадает с ожидаемым. Ожидаемый текст: {expected_text}"

    def assert_firstname(self):
        with allure.step(f'Заполнение поля firstname'):
            el = self.wait_for_element(self.FIRSTNAME_INPUT)
            assert el.is_displayed(), "Поле ввода имени (firstname) не отображается на странице"

    def assert_lastname(self):
        with allure.step(f'Заполение поля lastname'):
            el = self.wait_for_element(self.LASTNAME_INPUT)
            assert el.is_displayed(), "Поле ввода имени (lastname) не отображается на странице"

    def assert_save_button(self):
        with allure.step(f'Проверка отображения кнопки Сохранить'):
            el = self.wait_for_clickable(self.SAVE_BUTTON)
            assert el.is_displayed(), "Кнопка Сохранить не отображается на странице"

    #методы для рагистрации ногово пользователя
    def select_radio_bth(self):
        with allure.step(f'Выбор пола пользователя'):
            el = self.wait_for_clickable(self.SELECT_RADIO_BTH)

    def input_firstname(self, fistname):
        with allure.step(f'Заполнение поля firstname: ввод имени пользователя'):
            input_el = self.wait_for_element(self.FIRSTNAME_INPUT)
            input_el.click()
            input_el.send_keys(fistname)

    def input_lastname(self, lastname):
        with allure.step(f'Заполнение поля lastname: ввод фамилии пользователя'):
            input_el = self.wait_for_element(self.LASTNAME_INPUT)
            input_el.click()
            input_el.send_keys(lastname)

    def input_email(self, email):
        with allure.step(f'Заполнение поля email'):
            input_el = self.wait_for_element(self.EMAIL_INPUT)
            input_el.click()
            input_el.send_keys(email)

    def enter_password(self, password):
        with allure.step(f'Заполнение поля password'):
            input_el = self.wait_for_element(self.PASSWORD_INPUT)
            input_el.click()
            input_el.send_keys(password)

    def click_check_books_items(self):
        with allure.step(f'Установка чекбокса согласия'):
            input_el = self.wait_for_element(self.CHECK_BOOKS_TERMS)
            input_el.click()

    def click_check_books_customer(self):
        with allure.step(f'Установка обязательного чекбокса'):
            input_el = self.wait_for_element(self.CHECK_BOOKS_CUSTOMER)
            input_el.click()

    def click_save_button(self):
        with allure.step(f'Нажатие кнопки Сохранить'):
            el = self.wait_for_element(self.SAVE_BUTTON)
            el.click()
