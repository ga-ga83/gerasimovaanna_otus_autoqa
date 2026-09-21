import pytest
import random
import allure
import string
from selenium.webdriver.common.by import By

import allure


class TestHomePage:
    def test_homepage_elements(self, pages):
        with allure.step("Переход на главную страницу"):
            pages["home"].open()

        with allure.step("Проверка наличия поля поиска"):
            pages["home"].assert_search_input_displayed()

        with allure.step("Проверка баннера популярных товаров"):
            pages["home"].assert_popular_products_banner()

        with allure.step("Проверка валюты по умолчанию (EUR)"):
            pages["home"].assert_currency_is_eur()

        with allure.step("Проверка наличия кнопки Sign in"):
            sing_in_el = pages["home"].wait_for_element((By.XPATH, "//span[text()='Sign in']"))
            assert sing_in_el.is_displayed()


class TestCatalog:
    def test_catalog_elements(self, pages):
        with allure.step("Переход в раздел одежды"):
            pages["catalog"].click_clothes_link()

        with allure.step("Проверка текстов категорий"):
            pages["catalog"].assert_categories_text()
            pages["catalog"].assert_submenu_text()
            pages["catalog"].assert_brands_text()
            pages["catalog"].assert_subcategories_header()
            pages["catalog"].assert_clothes_block_text()


class TestProduct:
    def test_product_page(self, pages):
        with allure.step("Переход на страницу товара"):
            pages["product"].click_product_image()

        with allure.step("Проверка заголовка товара"):
            pages["product"].assert_product_title()

        with allure.step("Проверка описания товара"):
            pages["product"].assert_description_displayed_and_text()

        with allure.step("Проверка галереи изображений"):
            pages["product"].assert_image_container()

        with allure.step("Проверка блока цен"):
            pages["product"].assert_prices_block()

    def test_product_order(self, pages):
        with allure.step("Возврат на главную и проверка пустой корзины"):
            pages["home"].go_to_home()
            pages["home"].assert_cart_is_empty()

        with allure.step("Добавление товара в корзину"):
            pages["product"].click_product_image()
            pages["product"].click_add_to_cart()

        with allure.step("Проверка сообщения об успешном добавлении"):
            pages["product"].assert_modal_success_message()
            pages["product"].close_modal()

        with allure.step("Проверка количества товаров в корзине"):
            cart_count_el = pages["home"].wait_for_element((By.CSS_SELECTOR, ".blockcart .cart-products-count"))
            assert cart_count_el.text == "(1)", f"Ожидается 1 товар, получено: {cart_count_el.text}"


class TestLogin:
    def test_go_to_login_page(self, pages):
        with allure.step("Переход на страницу логина"):
            pages["home"].click_sing_in()
            login_page = pages["login"]

        with allure.step("Проверка заголовка и элементов формы"):
            assert 'Login' in login_page.get_title()
            assert login_page.wait_for_element((By.CSS_SELECTOR, "#submit-login")).is_displayed()
            assert login_page.wait_for_element((By.CSS_SELECTOR, "#field-email")).is_displayed()
            assert login_page.wait_for_element((By.CSS_SELECTOR, "#field-password")).is_displayed()
            assert login_page.get_register_link().is_displayed()

    def test_login_flow(self, pages):
        email = f"testuser{random.randint(100, 999)}@example.com"
        password = "Test1234!"
        first_name = "Test"
        last_name = "User"

        with allure.step("Регистрация пользователя"):
            pages["home"].open()
            pages["home"].click_sing_in()
            pages["login"].get_register_link().click()

            reg_page = pages["registration"]
            reg_page.input_firstname(first_name)
            reg_page.input_lastname(last_name)
            reg_page.input_email(email)
            reg_page.enter_password(password)
            reg_page.click_check_books_items()
            reg_page.click_check_books_customer()
            reg_page.click_save_button()

        with allure.step("Проверка авторизации после регистрации"):
            pages["login"].assert_user_logged_in('Sign in')

        with allure.step("Выход из системы"):
            pages["login"].click_logout()
            pages["login"].assert_user_logged_out()


class TestRegistration:
    def test_registration_page(self, pages):
        with allure.step("Переход на страницу регистрации"):
            pages["home"].click_sing_in()
            pages["login"].get_register_link().click()
            reg_page = pages["registration"]

        with allure.step("Проверка заголовка и полей"):
            assert 'Registration' in pages["login"].get_title()
            reg_page.assert_header_text("Create an account")
            reg_page.assert_firstname()
            reg_page.assert_lastname()
            reg_page.assert_save_button()

    def test_registration_new_user(self, pages):
        def generate_email():
            local_part = "".join(random.choices(string.ascii_lowercase, k=8))
            return f"{local_part}@example.com"

        email = generate_email()
        password = "nLTqnaXLw8Ma"
        first_name = "NGGJkk"
        last_name = "Klhhgg"

        with allure.step(f"Регистрация нового пользователя: {email}"):
            pages["home"].click_sing_in()
            pages["login"].get_register_link().click()

            reg_page = pages["registration"]
            reg_page.input_firstname(first_name)
            reg_page.input_lastname(last_name)
            reg_page.input_email(email)
            reg_page.enter_password(password)
            reg_page.click_check_books_items()
            reg_page.click_check_books_customer()
            reg_page.click_save_button()

        with allure.step("Проверка авторизации после регистрации"):
            pages["login"].assert_user_logged_in(f"Sign out {first_name} {last_name}")


class TestCurrency:
    def test_currency_change(self, pages):
        with allure.step("Изменение валюты на USD"):
            pages["home"].open_currency_dropdown()
            pages["home"].select_usd()
            pages["home"].assert_currency_displayed_as_usd()

        with allure.step("Проверка цен в каталоге после смены валюты"):
            pages["catalog"].click_clothes_link()



class TestAdministration:
    def test_authorization(self, pages):
        admin_page = pages["administration"]
        with allure.step("Авторизация в админ-панели"):
            admin_page.open_admin_page()
            admin_page.driver.maximize_window()
            admin_page.enter_email("admin@example.com")
            admin_page.enter_password("Admin123!")
            admin_page.click_login_in()
            admin_page.assert_administration_logged_in()
            admin_page.select_element_page()
            admin_page.select_menu_block()

    def test_create_new_product(self, pages):
        admin_page = pages["administration"]
        product_name = f"Blouse-test {random.randint(10, 999)}"

        with allure.step(f"Создание нового товара: {product_name}"):
            admin_page.subtab_catalog_click()
            admin_page.subtab_products_click()
            admin_page.check_product_page()
            admin_page.new_product_button()
            admin_page.open_product_modal_and_select_standard()
            admin_page.check_form_new_product()
            admin_page.name_new_product(product_name)
            admin_page.save_new_product()
            admin_page.check_message_save_product("Successful update")

        with allure.step("Возврат в каталог и проверка наличия товара"):
            admin_page.select_menu_block()
            admin_page.subtab_catalog_click()
            admin_page.subtab_products_click()
            admin_page.check_product_page()
            admin_page.select_new_product(product_name)

    def test_delete_new_product(self, pages):
        admin_page = pages["administration"]
        with allure.step("Удаление товара из админ-панели"):
            #admin_page.go_to_catalog()
            #admin_page.select_product_delete()
            admin_page.select_submit_menu_product()
            admin_page.menu_product_delete()
            admin_page.modal_dialog_delete()
