import pytest
from selenium.webdriver.common.by import By



class TestHomePage:
    def test_homepage_elements(self, pages):
        home = pages["home"]
        home.open()

        home.assert_search_input_displayed()
        home.assert_popular_products_banner()
        home.assert_currency_is_eur()

        #проверка наличия кнопки "Sing in"
        sing_in_el = home.wait_for_element((By.XPATH, "//span[text()='Sign in']"))
        assert sing_in_el.is_displayed()

class TestCatalog:
    def test_catalog_elements(self, pages):
        catalog = pages["catalog"]

        #Переход в каталог
        catalog.click_clothes_link()
        #Проверки внутри страницы каталога
        catalog.assert_categories_text()
        catalog.assert_submenu_text()
        catalog.assert_brands_text()
        catalog.assert_subcategories_header()
        catalog.assert_clothes_block_text()


class TestProduct:
    def test_product_page(self, pages):
        product = pages["product"]

        # Переход на товар
        product.click_product_image()

        # Проверки внутри страницы товара
        product.assert_product_title()
        product.assert_description_displayed_and_text()
        product.assert_image_container()
        product.assert_prices_block()

        btn = product.wait_for_clickable((By.CSS_SELECTOR, "button[data-button-action='add-to-cart']"))
        assert btn.is_displayed()

    def test_product_order(self, pages):
        home = pages["home"]
        product = pages["product"]

        # Возврат на главную
        home.go_to_home()

        # Проверка пустой корзины
        home.assert_cart_is_empty()

        # Добавление в корзину
        product.click_product_image()
        product.click_add_to_cart()

        # Проверка успеха
        product.assert_modal_success_message()
        product.close_modal()

        # Проверка корзины (1 товар)
        # Так как assert_cart_is_empty проверяет "(0)", нам нужен метод для проверки "(1)" или переиспользовать логику
        # Добавим временную проверку URL или текста, так как в HomePage нет метода assert_cart_count_is_one
        cart_count_el = home.wait_for_element((By.CSS_SELECTOR, ".blockcart .cart-products-count"))
        assert cart_count_el.text == "(1)", f"Ожидается 1 товар, получено: {cart_count_el.text}"


class TestLogin:
    def test_go_to_login_page(self, pages):
        home = pages["home"]
        login_page = pages["login"]

        home.click_sing_in()

        # Проверка заголовка
        assert 'Login' in login_page.get_title()

        # Проверка полей
        assert login_page.wait_for_element((By.CSS_SELECTOR, "#submit-login")).is_displayed()
        assert login_page.wait_for_element((By.CSS_SELECTOR, "#field-email")).is_displayed()
        assert login_page.wait_for_element((By.CSS_SELECTOR, "#field-password")).is_displayed()
        assert login_page.get_register_link().is_displayed()

    def test_login_flow(self, pages):
        login_page = pages["login"]

        login_page.open_login_page()
        login_page.enter_email("gerasimowa@inbox.ru")
        login_page.enter_password("1234lanos!")
        login_page.click_sign_in()

        # Проверка входа
        login_page.assert_user_logged_in('Sign out adminn lanos')

        # Выход
        login_page.click_logout()
        login_page.assert_user_logged_out()


class TestRegistration:
    def test_registration_page(self, pages):
        home = pages["home"]
        login_page = pages["login"]
        reg_page = pages["registration"]

        home.click_sing_in()
        login_page.get_register_link().click()

        # Проверка заголовка
        assert 'Registration' in login_page.get_title()
        reg_page.assert_header_text("Create an account")

        # Проверка полей
        reg_page.assert_firstname()
        reg_page.assert_lastname()
        reg_page.assert_save_button()


class TestCurrency:
    def test_currency_change(self, pages):
        home_page = pages["home"]
        catalog = pages["catalog"]

        # Переключение валюты
        home_page.open_currency_dropdown()
        home_page.select_usd()

        # Проверка отображения валюты
        home_page.assert_currency_displayed_as_usd()

        # Переход в каталог для проверки цен
        catalog.click_clothes_link()