from HW_8.pages.base_page import BasePage
from selenium.webdriver.common.by import By
import allure
import logging


class HomePage(BasePage):

    SEARСH_INPUT = (By.NAME, "s")
    POPULAR_PRODUCTS_TITLE = (By.CSS_SELECTOR, "h2.products-section-title")
    SIGN_IN_LINK = (By.XPATH, "//span[text()='Sign in']")
    CURRENCY_BUTTON = (By.CSS_SELECTOR, "#_desktop_currency_selector button")
    HOME_LINK = (By.XPATH, "//a[./span[text()='Home']]")
    CART_COUNT = (By.CSS_SELECTOR, ".blockcart .cart-products-count")
    CURRENCY_DROPDOWN = (By.CSS_SELECTOR, "button[aria-label='Currency dropdown']")
    USD_OPTION = (By.CSS_SELECTOR, "#_desktop_currency_selector a[title='US Dollar']")
    CURRENCY_CURRENCY_TEXT = (By.CSS_SELECTOR, "#_desktop_currency_selector button span._gray-darker")


    def assert_search_input_displayed(self):
        with allure.step(f'Проверка отображения блока поиска'):
            search_input = self.wait_for_presence(self.SEARСH_INPUT)
            assert search_input.is_displayed(), "Поиск не отображен"

    def assert_popular_products_banner(self):
        with allure.step(f'Проверка баннера'):
            text = self.wait_for_element(self.POPULAR_PRODUCTS_TITLE).text
            assert 'POPULAR PRODUCTS' in text, f"Баннер не содержит 'POPULAR PRODUCTS'. Текст: {text}"

    def click_sing_in(self):
        with allure.step(f'Нажатие метки sign_in на странице'):
            self.wait_for_clickable(self.SIGN_IN_LINK).click()

    def assert_currency_is_eur(self):
        with allure.step(f'Проверка отображения валюты'):
            text = self.wait_for_clickable(self.CURRENCY_BUTTON).text
            assert "EUR" in text, f"Валюта не EUR. Текст: {text}"

    def go_to_home(self):
        with allure.step(f'Возврат на главную страницу'):
            self.wait_for_clickable(self.HOME_LINK).click()

    def assert_cart_is_empty(self):
        with allure.step(f'Проверка состояния корзины до добавления товара'):
            text = self.wait_for_element(self.CART_COUNT).text
            assert text == "(0)", f"Ожидалась отображение пустой корзины, но: {text}"

    def open_currency_dropdown(self):
        with allure.step(f'Переход для смены валют'):
            self.wait_for_clickable(self.CURRENCY_DROPDOWN).click()

    def select_usd(self):
        with allure.step(f'Смена валюты'):
            self.wait_for_clickable(self.USD_OPTION).click()

    def assert_currency_displayed_as_usd(self):
        with allure.step(f'Проверка изменения валюты'):
            text = self.wait_for_element(self.CURRENCY_CURRENCY_TEXT).text
            assert text == "USD $", f"Ожидалось отображение USD $, но: {text}"

