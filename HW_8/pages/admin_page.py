from HW_8.pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import allure
import logging
import time


class AdminPage(BasePage):
    EMAIL_INPUT = (By.CSS_SELECTOR, "input[name='email']")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "input[name='passwd']")
    SUBMIT_BTN_LOGIN = (By.XPATH, "//button[@name='submitLogin']")
    HEADER_PANEL = (By.CSS_SELECTOR, '#header')
    DEMO_BTH = (By.XPATH, "//*[@id='page-header-desc-configuration-switch_demo']")

    MENU_BLOCK = (By.CSS_SELECTOR, "#subtab-AdminCatalog > a")
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
        try:
            WebDriverWait(self.driver, 30).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
        except Exception:
            self.logger.warning("Не удалось дождаться document.readyState, продолжаем работу.")

    def _ensure_dashboard(self):
        """Возвращает на дашборд, если мы ушли со страницы администратора."""
        if "AdminDashboard" not in self.driver.current_url and "administration" not in self.driver.current_url:
            self.driver.get(f"{self.base_url}administration")
            self._wait_page_ready()
            time.sleep(1)

    def open_admin_page(self):
        with allure.step('Переход на страницу админки.'):
            self.driver.get(f"{self.base_url}administration")

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
            assert text.is_displayed(), "Авторизации на странице админ не была"

    def select_element_page(self):
        return self.wait_for_element(self.DEMO_BTH)

    def select_menu_block(self):
        """Клик по меню Catalog — пробуем несколько стратегий поиска."""
        with allure.step("Клик по меню (Admin Catalog)"):
            self.driver.switch_to.default_content()

            # Если уже в разделе Catalog/Products — повторный клик не нужен
            current_url = self.driver.current_url
            if "AdminCatalog" in current_url or "catalog/products" in current_url:
                self.logger.info("Уже в разделе Catalog, повторный клик не нужен.")
                return

            # Если не на дашборде — возвращаемся
            if "AdminDashboard" not in current_url and "administration" not in current_url:
                self.driver.get(f"{self.base_url}administration")
                self._wait_page_ready()
                time.sleep(1)

            self.logger.info(f"select_menu_block: URL={self.driver.current_url}, Title={self.driver.title}")

            # Стратегия 1: по ID элемента
            link = self.driver.execute_script(
                'var a = document.querySelector("#subtab-AdminCatalog a"); return a || null;'
            )
            if link:
                self.driver.execute_script("arguments[0].click();", link)
                self.logger.info("Клик по ссылке Catalog (по ID) выполнен.")
                time.sleep(2.5)
                return

            # Стратегия 2: по href содержит AdminCatalog (legacy URL)
            link = self.driver.execute_script(
                "var a = document.querySelector('a[href*=\"AdminCatalog\"]'); return a || null;"
            )
            if link:
                self.driver.execute_script("arguments[0].click();", link)
                self.logger.info("Клик по ссылке Catalog (по href) выполнен.")
                time.sleep(2.5)
                return

            # Стратегия 3: по тексту ссылки
            link = self.driver.execute_script(
                "var links = document.querySelectorAll('#header ul a, .sidebar a, nav a'); "
                "for (var i = 0; i < links.length; i++) { "
                "  if (links[i].textContent.trim() === 'Catalog') return links[i]; "
                "} return null;"
            )
            if link:
                self.driver.execute_script("arguments[0].click();", link)
                self.logger.info("Клик по ссылке Catalog (по тексту) выполнен.")
                time.sleep(2.5)
                return

            # Стратегия 4: ждём появления через WebDriverWait
            link = WebDriverWait(self.driver, 30).until(
                lambda d: d.execute_script(
                    'var a = document.querySelector("#subtab-AdminCatalog a, a[href*=\"AdminCatalog\"]"); '
                    "return a || null;"
                )
            )
            self.driver.execute_script("arguments[0].click();", link)
            self.logger.info("Клик по ссылке Catalog (через WebDriverWait) выполнен.")
            time.sleep(2.5)

    def subtab_catalog_click(self):
        """Переход к Products — пробуем несколько стратегий."""
        with allure.step("Переход к Products (Catalog -> Products)"):
            self.driver.switch_to.default_content()

            # Проверяем, не на странице ли мы уже
            current_url = self.driver.current_url
            if "catalog/products" in current_url or "AdminProducts" in current_url:
                if "Invalid" not in self.driver.title:
                    self.logger.info("Уже на странице Products.")
                    return

            # Способ 1: по ID элемента
            link = self.driver.execute_script(
                'var a = document.querySelector("#subtab-AdminProducts a"); return a || null;'
            )
            if link:
                self.driver.execute_script("arguments[0].click();", link)
                self.logger.info("Кликнули по ссылке на Products (по ID).")
                self._wait_page_ready()
                time.sleep(2)
                return

            # Способ 2: по href содержит AdminProducts (legacy URL)
            link = self.driver.execute_script(
                "var a = document.querySelector('a[href*=\"AdminProducts\"]'); return a || null;"
            )
            if link:
                self.driver.execute_script("arguments[0].click();", link)
                self.logger.info("Кликнули по прямой ссылке на Products (по href).")
                self._wait_page_ready()
                time.sleep(2)
                return

            # Способ 3: по href содержит catalog/products (Symfony route)
            link = self.driver.execute_script(
                "var a = document.querySelector('a[href*=\"catalog/products\"]'); return a || null;"
            )
            if link:
                self.driver.execute_script("arguments[0].click();", link)
                self.logger.info("Кликнули по ссылке на Products (Symfony route).")
                self._wait_page_ready()
                time.sleep(2)
                return

            # Способ 4: раскрываем Catalog, потом ищем Products
            try:
                self.select_menu_block()
                time.sleep(1)
                link = self.driver.execute_script(
                    'var a = document.querySelector("#subtab-AdminProducts a, a[href*=\"AdminProducts\"], a[href*=\"catalog/products\"]"); '
                    "return a || null;"
                )
                if link:
                    self.driver.execute_script("arguments[0].click();", link)
                    self.logger.info("Меню раскрыто, кликнули по Products.")
                    self._wait_page_ready()
                    time.sleep(2)
                    return
            except Exception:
                pass

            # Способ 5: извлекаем href и переходим напрямую
            href = self.driver.execute_script(
                'var a = document.querySelector("#subtab-AdminProducts a, a[href*=\"AdminProducts\"], a[href*=\"catalog/products\"]"); '
                "return a ? a.getAttribute('href') : null;"
            )
            if href:
                full_url = href if href.startswith("http") else f"{self.base_url}administration/{href.lstrip('/')}"
                self.driver.get(full_url)
                self.logger.info(f"Переход по URL с токеном из ссылки: {full_url}")
                self._wait_page_ready()
                time.sleep(2)
                return

            raise RuntimeError("Не удалось найти ссылку на AdminProducts ни одним способом")

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
            el_text = self.wait_for_element(self.PRODUCTS_PAGE_ADMIN)
            assert el_text.is_displayed(), "Перехода на страницу Products не было"

    def new_product_button(self):
        with allure.step("Клик по кнопке 'Add new product'"):
            self.wait_for_element(self.NEW_PRODUCT_BUTTON).click()

    def open_product_modal_and_select_standard(self):
        with allure.step("Открытие модалки и выбор стандартного продукта"):
            iframe = self.wait_for_element(self.MODAL_CREATE_PRODUCT)
            self.driver.switch_to.frame(iframe)

            try:
                standard_btn = self.wait_for_element(self.MODAL_STANDARD_PRODUCT_BTN)
                standard_btn.click()
                btn_add_new_product = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located(self.MODAL_NEW_ADD_PRODUCT)
                )
                self.driver.execute_script("arguments[0].click();", btn_add_new_product)
            finally:
                self.driver.switch_to.default_content()

    def check_form_new_product(self):
        with allure.step("Проверка отображения формы создания продукта"):
            el = self.wait_for_element(self.CHECK_CREATE_NEW_PRODUCT)
            assert el.is_displayed(), "Форма создания продукта не открылась"

    def name_new_product(self, product_name):
        with allure.step(f"Ввод имени продукта: {product_name}"):
            input_el = self.wait_for_element(self.CHECK_CREATE_NEW_PRODUCT)
            input_el.click()
            input_el.clear()
            input_el.send_keys(product_name)

    def save_new_product(self):
        with allure.step("Сохранение продукта"):
            self.click_element(self.SAVE_BTH_NEW_PRODUCT)
            self._wait_page_ready()
            time.sleep(1)

    def check_message_save_product(self, message):
        with allure.step(f"Проверка сообщения об успехе: {message}"):
            el = self.wait_for_element(self.CREATE_MESSAGE_ALERT)
            assert message in el.text, f"Сообщение '{message}' не найдено. Текст: {el.text}"

    def select_new_product(self, product_name):
        with allure.step(f"Поиск продукта {product_name}"):
            rows = self.driver.find_elements(*self.LIST_PRODUCT_ROW)
            found = False
            for row in rows:
                if product_name in row.text:
                    found = True
                    break
            assert found, f"Товар '{product_name}' не найден в списке"

    def go_to_catalog(self):
        self.click_element(self.GOTO_CATALOG)
        self._wait_page_ready()
        time.sleep(1)

    def select_product_delete(self):
        """Поиск товара из списка, для его удаления"""
        el = self.wait_for_element(self.PRODUCT_DELETE)
        assert el.is_displayed(), "Кнопка возврата к каталогу товаров не отображается"

    def select_submit_menu_product(self):
        """Поиск подменю на товаре: preview, duplicate, delete"""
        self.driver.switch_to.default_content()

        self.logger.info(f"select_submit_menu_product: URL={self.driver.current_url}, Title={self.driver.title}")

        # Пробуем основной селектор
        try:
            el = WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable(self.SUBMIT_DROPDOWN_PRODUCT)
            )
            self.driver.execute_script("arguments[0].click();", el)
            time.sleep(2)
            return
        except Exception:
            self.logger.warning("Основной селектор dropdown не сработал, пробуем альтернативный.")

        # Fallback: ищем через JS любой элемент с dropdown-toggle в таблице
        try:
            self.driver.execute_script(
                "var el = document.querySelector(\"table tr a.dropdown-toggle, table tr [data-toggle='dropdown']\"); "
                "if (el) { el.click(); }"
            )
            time.sleep(2)
            self.logger.info("Альтернативный клик по dropdown выполнен.")
        except Exception as e:
            self.logger.error(f"Не удалось найти dropdown: {e}")
            raise

    def menu_product_delete(self):
        """Ждем появления элемента в коде и кликаем в обход анимаций."""
        self.driver.switch_to.default_content()

        # Ждем появления элемента (presence, а не visibility — анимации не помеха)
        el = WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located(self.DELETE_BTH_MENU)
        )
        self.driver.execute_script("arguments[0].click();", el)

    def modal_dialog_delete(self):
        with allure.step("Подтверждение удаления товара"):
            """Ждём появления диалогового окна при удалении и подтверждаем удаление."""
            el = self.wait_for_element(self.DELETE_MESSAGE_DIALOG)
            assert el.is_displayed(), "Диалоговое окно удаления не отображается на странице"
            delete_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.DELETE_BUTTON_MODAL)
            )
            delete_btn.click()
            return self