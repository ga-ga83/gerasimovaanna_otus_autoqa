from HW_8.pages.base_page import BasePage
from selenium.webdriver.common.by import By
import allure
import logging


class CatalogPage(BasePage):
    CLOTHES_LINK = (By.XPATH, "//a[@href='http://localhost:8081/3-clothes']")
    CATEGORIES_BLOCK = (By.CSS_SELECTOR, ".block-categories")
    SUBMENU_BLOCK = (By.CSS_SELECTOR, ".block-categories .category-sub-menu")
    BRANDS_BLOCK = (By.XPATH, "//div[@id='search_filters_brands']")
    SUBCATEGORIES_HEADER = (By.XPATH, "//h2[text()='Subcategories']")
    CLOTHES_BLOCK = (By.XPATH, "//div[@class='block-category card card-block']")
    PRICE_LABEL = (By.CSS_SELECTOR, "ul.faceted-slider[data-slider-label='Price'] p")

    def click_clothes_link(self):
        with allure.step(f'Переход на страницу каталога'):
            self.wait_for_clickable(self.CLOTHES_LINK).click()

    def assert_categories_text(self):
        with allure.step(f'Проверка наименования категорий'):
            text = self.wait_for_element(self.CATEGORIES_BLOCK).text
            assert "CLOTHES\nMen\nWomen" in text, f"Неверный текст категорий: {text}"

    def assert_submenu_text(self):
        with allure.step(f'Проверка подменю'):
            text = self.wait_for_element(self.SUBMENU_BLOCK).text
            assert "Men\nWomen" in text, f"Неверный текст подменю: {text}"

    def assert_brands_text(self):
        with allure.step(f'Проверка блока брендов'):
            text = self.wait_for_element(self.BRANDS_BLOCK).text
            assert "BRANDS\n" in text, f"Неверный текст брендов: {text}"

    def assert_subcategories_header(self):
        with allure.step(f'Проверка заголовка подкатегорий'):
            text = self.wait_for_element(self.SUBCATEGORIES_HEADER).text
            assert "Subcategories" in text, f"Неверный заголовок подкатегорий: {text}"

    def assert_clothes_block_text(self):
        with allure.step(f'Проверка текста в блоке Одежда'):
            text = self.wait_for_element(self.CLOTHES_BLOCK).text
            assert "CLOTHES\n" in text, f"Неверный текст блока одежды: {text}"

    def assert_price_range_usd(self):
        with allure.step(f'Проверка диапазона цен, после смены валюты на главной странице'):
            text = self.wait_for_element(self.PRICE_LABEL).text
            assert "$22.00 - $42.00" in text, f"В диапазоне цен отображается парметры не в usd, валюта не изменена: {text}"
