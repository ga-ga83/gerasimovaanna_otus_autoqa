from HW_8.pages.base_page import BasePage
from selenium.webdriver.common.by import By
import allure
import logging


class ProductPage(BasePage):

    PRODUCT_IMAGE = (By.CSS_SELECTOR, "img[alt='Hummingbird printed t-shirt']")
    PRODUCT_TITLE = (By.XPATH, "//h1[text()='Hummingbird printed t-shirt']")
    DESCRIPTION_SHORT = (By.CSS_SELECTOR, "#product-description-short-1")
    IMAGES_CONTAINER = (By.CSS_SELECTOR, ".images-container.js-images-container")
    PRICES_BLOCK = (By.CSS_SELECTOR, ".product-prices.js-product-prices")
    ADD_TO_CARD_BTN = (By.CSS_SELECTOR, "button[data-button-action='add-to-cart']")
    MODAL_SUCCESS_MSG = (By.CSS_SELECTOR, "#blockcart-modal .modal-header h4.modal-title")
    MODAL_CLOSE_BTN = (By.CSS_SELECTOR, "#blockcart-modal button.close")

    def click_product_image(self):
        with allure.step(f'Преход по иконке продукта'):
            self.wait_for_clickable(self.PRODUCT_IMAGE).click()

    def assert_product_title(self):
        with allure.step(f'Проверка заголовка с наименованием продукта'):
            text = self.wait_for_element(self.PRODUCT_TITLE).text
            assert "HUMMINGBIRD PRINTED T-SHIRT" in text, f"Неверный заголовок, на странице нет заголовка с текстом: 'HUMMINGBIRD PRINTED T-SHIRT': отображается {text}"

    def assert_description_displayed_and_text(self):
        with allure.step(f'Проврка наличия описания товара'):
            el_text = self.wait_for_element(self.DESCRIPTION_SHORT)
            assert el_text.is_displayed(), "Краткое описание товара не отображается на странице"
            expected_text = "Regular fit, round neckline, short sleeves"
            assert expected_text in el_text.text, f"Текст описания не совпадает. Ожидаемый текст {expected_text}, отображаемый текст {el_text}"

    def assert_image_container(self):
        with allure.step(f'Проврка отображения фото товара'):
            el = self.wait_for_element(self.IMAGES_CONTAINER)
            assert el.is_displayed(), "Не отображается фото товара"

    def assert_prices_block(self):
        with allure.step(f'Проверка отображения цены товара'):
            el = self.wait_for_element(self.PRICES_BLOCK)
            assert el.is_displayed(), "Цена товара не отображается"

    def click_add_to_cart(self):
        with allure.step(f'Проверка наличия кнопки добавления товара на странице'):
            self.wait_for_clickable(self.ADD_TO_CARD_BTN).click(), "Кнопка добавления товара в корзину не отображается"

    def assert_modal_success_message(self):
        with allure.step(f'Проверка уведомления о добавлении товара'):
            text = self.wait_for_element(self.MODAL_SUCCESS_MSG).text
            assert "Product successfully added" in text, f"Ожидался текст об успешном добавлении, но получено: '{text}'"

    def close_modal(self):
        with allure.step(f'Выход из моального окна'):
            self.wait_for_clickable(self.MODAL_CLOSE_BTN).click()
