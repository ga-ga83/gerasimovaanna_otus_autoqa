import pytest
import random
import string
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

    def test_registration_new_user(self, pages):
        def generate_email():
            # Генерируем случайную часть из 8 строчных букв
            local_part = "".join(random.choices(string.ascii_lowercase, k=8))
            domain = "example.com"
            return f"{local_part}@{domain}"

        # Сохраняем email и пароль в переменные
        email = generate_email()
        password = "nLTqnaXLw8Ma"

        home = pages["home"]
        login_page = pages["login"]
        reg_page = pages["registration"]

        # Переход на страницу регистрации
        home.click_sing_in()
        login_page.get_register_link().click()

        # Заполнение формы регистрации
        reg_page.input_firstname("NGGJkk")
        reg_page.input_lastname("Klhhgg")
        reg_page.input_email(email)
        reg_page.enter_password(password)
        reg_page.click_check_books_items()
        reg_page.click_check_books_customer()
        reg_page.click_save_button()

        # Проверка успешной регистрации
        login_page.assert_user_logged_in("Sign out NGGJkk Klhhgg")


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


class TestAdministration:

    def test_authorization(self, pages):
        """Тест 1: Проверка авторизации на странице"""
        admin_page = pages["administration"]

        admin_page.open_admin_page()
        admin_page.driver.maximize_window()
        admin_page.enter_email("admin@example.com")
        admin_page.enter_password("Admin123!")
        admin_page.click_login_in()

        admin_page.assert_administration_logged_in()
        admin_page.select_element_page()
        admin_page.select_menu_block()

    def test_create_new_product(self, pages):
        """Тест 2: Создание нового товара """
        admin_page = pages["administration"]

        # Логика создания товара
        admin_page.subtab_catalog_click()
        admin_page.subtab_products_click()
        admin_page.check_product_page()

        admin_page.new_product_button()
        admin_page.open_product_modal_and_select_standard()
        admin_page.check_form_new_product()

        product_name = f"Blouse-test {random.randint(10, 999)}"
        admin_page.name_new_product(product_name)
        admin_page.save_new_product()
        admin_page.check_message_save_product("Successful update")

        admin_page.select_menu_block()
        admin_page.subtab_catalog_click()
        admin_page.subtab_products_click()
        admin_page.check_product_page()

        # Поиск созданного товара
        admin_page.select_new_product(product_name)

    def test_delete_new_product(self, pages):
        """Тест: Удаление созданного товара """

        admin_page = pages["administration"]
        #удаление товара
        admin_page.go_to_catalog()
        admin_page.select_product_delete()
        admin_page.select_submit_menu_product()
        admin_page.menu_product_delete()
        admin_page.modal_dialog_delete()

