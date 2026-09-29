from HW_8.pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure
import logging
import time


class AdminPage(BasePage):
    EMAIL_INPUT = (By.CSS_SELECTOR, "input[name='email']")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "input[name='passwd']")
    SUBMIT_BTN_LOGIN = (By.XPATH, "//button[@name='submitLogin']")
    HEADER_PANEL = (By.CSS_SELECTOR, '#header')
    DEMO_BTH = (By.XPATH, "//*[@id='page-header-desc-configuration-switch_demo']")
    MENU_BLOCK = (By.CSS_SELECTOR, '#subtab-AdminCatalog > a')
    CATALOG_SUBTAB = (By.CSS_SELECTOR, "#subtab-AdminCatalog > a")
    PRODUCTS_SUBTAB = (By.CSS_SELECTOR, "#subtab-AdminProducts a")
    PRODUCTS_PAGE_ADMIN = (By.CSS_SELECTOR, "a[aria-current='page'][href*='catalog/products']")
    NEW_PRODUCT_BUTTON = (By.CSS_SELECTOR, "a.btn.btn-primary.new-product-button")
    MODAL_CREATE_PRODUCT = (By.CSS_SELECTOR, 'iframe[name="modal-create-product-iframe"]')
    MODAL_STANDARD_PRODUCT_BTN = (By.CSS_SELECTOR, "button[data-value='standard']")
    MODAL_NEW_ADD_PRODUCT = (By.XPATH, "//*[@id='create_product_create']")
    CHECK_CREATE_NEW_PRODUCT = (By.CSS_SELECTOR, "#product_header_name_1")
    SAVE_BTH_NEW_PRODUCT = (By.ID, "product_footer_save")
    CREATE_MESSAGE_ALERT = (By.XPATH, "//p[text()='Successful update']")
    LIST_PRODUCT_ROW = (By.XPATH, "//div[contains(@class, 'card-body')]")

    GOTO_CATALOG = (By.CSS_SELECTOR, "div.form-group.product-footer-left")
    PRODUCT_DELETE = (By.CSS_SELECTOR, "tbody tr:first-child td.column-name a")
    SUBMIT_DROPDOWN_PRODUCT = (By.CSS_SELECTOR, "a[data-toggle='dropdown'][aria-expanded]")
    DELETE_BTH_MENU = (By.XPATH, "//a[contains(@class, 'grid-delete-row-link')]")
    DELETE_MESSAGE_DIALOG = (By.XPATH, "//div[@class='modal-content'][.//h4[text()='Delete selection']]")
    DELETE_BUTTON_MODAL = (By.CSS_SELECTOR, "button.btn-confirm-submit")

    def _wait_page_ready(self):
        """Ожидание полной загрузки страницы."""
        WebDriverWait(self.driver, 20).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

    def open_admin_page(self):
        with allure.step('Переход на страницу админки.'):
            self.driver.get(f"{self.base_url}administration")
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located(self.EMAIL_INPUT)
            )

    def enter_email(self, email):
        with allure.step(f"Ввод Email: {email}"):
            input_el = self.wait_for_element(self.EMAIL_INPUT)
            input_el.click()
            input_el.send_keys(email)

    def enter_password(self, password):
        with allure.step(f"Ввод пароля: {'*' * len(password)}"):
            input_el = self.wait_for_element(self.PASSWORD_INPUT)
            input_el.click()
            input_el.send_keys(password)

    def click_login_in(self):
        with allure.step("Нажатие кнопки входа"):
            self.wait_for_clickable(self.SUBMIT_BTN_LOGIN).click()

    def assert_administration_logged_in(self):
        with allure.step("Проверка авторизации (отображение панели)"):
            text = self.wait_for_element(self.HEADER_PANEL)
            assert text.is_displayed(), "Авторизации на странице админ не было"

    def select_element_page(self):
        return self.wait_for_element(self.DEMO_BTH)

    def select_menu_block(self):
        with allure.step("Клик по меню (Admin Catalog)"):
            self.driver.switch_to.default_content()

            # Ждем, пока элемент появится в DOM и станет видимым
            el = WebDriverWait(self.driver, 30).until(
                lambda d: EC.presence_of_element_located(self.MENU_BLOCK)(d)
            )

            # Дополнительная проверка: элемент не должен быть скрыт
            if not el.is_displayed():
                self.logger.warning("Элемент меню есть в DOM, но скрыт. Ждем явного появления.")
                WebDriverWait(self.driver, 10).until(EC.visibility_of(el))

            # Клик через JS — это самый надежный способ для PrestaShop
            self.driver.execute_script("arguments[0].click();", el)
            time.sleep(1.5)  # Даем JS-меню раскрыться

    def subtab_catalog_click(self):
        with allure.step("Клик по меню Catalog -> Products"):
            self.driver.switch_to.default_content()
            products_link_selector = (By.CSS_SELECTOR, "#subtab-AdminProducts a")

            # 1. Проверка: может, мы уже на странице Products?
            current_url = self.driver.current_url
            if "controller=AdminProducts" in current_url or "catalog/products" in current_url:
                self.logger.info("Уже на странице Products, пропускаем клик.")
                return

            # 2. Пытаемся кликнуть, если Products виден сразу
            try:
                if EC.visibility_of_element_located(products_link_selector)(self.driver):
                    products_el = self.wait_for_element(products_link_selector)
                    self.driver.execute_script("arguments[0].click();", products_el)
                    self.logger.info("Кликнули по Products напрямую.")
                    return
            except Exception:
                pass

            # 3. Раскрываем меню и кликаем
            try:
                menu_el = WebDriverWait(self.driver, 20).until(
                    EC.presence_of_element_located(self.MENU_BLOCK)
                )
                if not menu_el.is_displayed():
                    WebDriverWait(self.driver, 5).until(EC.visibility_of(menu_el))

                self.driver.execute_script("arguments[0].click();", menu_el)
                time.sleep(2)  # Важно: меню раскрывается с анимацией

                products_el = WebDriverWait(self.driver, 15).until(
                    EC.element_to_be_clickable(products_link_selector)
                )
                self.driver.execute_script("arguments[0].click();", products_el)
                self.logger.info("Меню раскрыто, кликнули по Products.")

            except Exception as e:
                # 4. Fallback: прямой URL
                self.logger.warning(f"Не удалось кликнуть меню ({e}), переходим по URL напрямую.")
                self.driver.get(f"{self.base_url}administration/index.php?controller=AdminProducts")

    def subtab_products_click(self):
        with allure.step("Клик по подменю Products"):
            self.driver.switch_to.default_content()
            el = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.PRODUCTS_SUBTAB)
            )
            self.driver.execute_script("arguments[0].click();", el)
        return self

    def check_product_page(self):
        with allure.step("Проверка перехода на страницу Products"):
            self.driver.switch_to.default_content()
            el_text = WebDriverWait(self.driver, 15).until(
                EC.visibility_of_element_located(self.PRODUCTS_PAGE_ADMIN)
            )
            assert el_text.is_displayed(), "Перехода на страницу Products не было"

    def new_product_button(self):
        with allure.step("Клик по кнопке 'Add new product'"):
            self.driver.switch_to.default_content()
            self.wait_for_element(self.NEW_PRODUCT_BUTTON).click()

    def open_product_modal_and_select_standard(self):
        with allure.step("Открытие модалки и выбор стандартного продукта"):
            self.driver.switch_to.default_content()
            iframe = self.wait_for_element(self.MODAL_CREATE_PRODUCT)
            self.driver.switch_to.frame(iframe)

            try:
                standard_btn = self.wait_for_element(self.MODAL_STANDARD_PRODUCT_BTN)
                standard_btn.click()
                btn_add_new_product = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located(self.MODAL_NEW_ADD_PRODUCT)
                )
                self.driver.execute_script("arguments[0].click();", btn_add_new_product)
                time.sleep(1)
            finally:
                self.driver.switch_to.default_content()

    def check_form_new_product(self):
        with allure.step("Проверка отображения формы создания продукта"):
            self.driver.switch_to.default_content()
            self._wait_page_ready()
            el = WebDriverWait(self.driver, 15).until(
                EC.visibility_of_element_located(self.CHECK_CREATE_NEW_PRODUCT)
            )
            assert el.is_displayed(), "Форма создания продукта не открылась"

    def name_new_product(self, product_name):
        with allure.step(f"Ввод имени продукта: {product_name}"):
            input_el = self.wait_for_element(self.CHECK_CREATE_NEW_PRODUCT)
            input_el.click()
            input_el.send_keys(product_name)

    def save_new_product(self):
        with allure.step("Сохранение продукта"):
            self.driver.switch_to.default_content()
            self.click_element(self.SAVE_BTH_NEW_PRODUCT)
            self._wait_page_ready()
            time.sleep(1)

    def check_message_save_product(self, message):
        with allure.step(f"Проверка сообщения об успехе: {message}"):
            self.driver.switch_to.default_content()
            el = WebDriverWait(self.driver, 15).until(
                EC.visibility_of_element_located(self.CREATE_MESSAGE_ALERT)
            )
            assert message in el.text, f"Сообщение '{message}' не найдено. Текст: {el.text}"

    def select_new_product(self, product_name):
        with allure.step(f"Поиск продукта {product_name}"):
            self.driver.switch_to.default_content()
            rows = WebDriverWait(self.driver, 15).until(
                EC.presence_of_all_elements_located(self.LIST_PRODUCT_ROW)
            )
            found = False
            for row in rows:
                if product_name in row.text:
                    found = True
                    break
            assert found, f"Товар '{product_name}' не найден в списке"

    def go_to_catalog(self):
        with allure.step("Возврат к каталогу товаров"):
            self.driver.switch_to.default_content()
            self.click_element(self.GOTO_CATALOG)
            self._wait_page_ready()
            time.sleep(1)

    def select_product_delete(self):
        """Поиск товара из списка, для его удаления"""
        self.driver.switch_to.default_content()
        el = self.wait_for_element(self.PRODUCT_DELETE)
        assert el.is_displayed(), "Кнопка возврата к каталогу товаров не отображается"

    def select_submit_menu_product(self):
        """Поиск подменю на товаре: preview, duplicate, delete"""
        self.driver.switch_to.default_content()
        el = self.wait_for_element(self.SUBMIT_DROPDOWN_PRODUCT)
        assert el.is_displayed(), "Кнопка вызова подменю в строке товара не отображается"
        self.driver.execute_script("arguments[0].click();", el)
        time.sleep(1.5)

    def menu_product_delete(self):
        """Ждем появления элемента и кликаем в обход анимаций."""
        self.driver.switch_to.default_content()
        el = WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located(self.DELETE_BTH_MENU)
        )
        self.driver.execute_script("arguments[0].click();", el)

    def modal_dialog_delete(self):
        with allure.step("Подтверждение удаления товара"):
            self.driver.switch_to.default_content()
            el = WebDriverWait(self.driver, 15).until(
                EC.visibility_of_element_located(self.DELETE_MESSAGE_DIALOG)
            )
            assert el.is_displayed(), "Диалоговое окно удаления не отображается"
            delete_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.DELETE_BUTTON_MODAL)
            )
            delete_btn.click()
            return self