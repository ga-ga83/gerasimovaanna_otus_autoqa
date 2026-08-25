from HW_7.pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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


    def open_admin_page(self):
        self.driver.get(f"{self.base_url}administration")

    def enter_email(self, email):
        input_el = self.wait_for_element(self.EMAIL_INPUT)
        input_el.click()
        input_el.send_keys(email)

    def enter_password(self, password):
        input_el = self.wait_for_element(self.PASSWORD_INPUT)
        input_el.click()
        input_el.send_keys(password)

    def click_login_in(self):
        self.wait_for_clickable(self.SUBMIT_BTN_LOGIN).click(), "Кнопка входа на странице не отображается"

    def assert_administration_logged_in(self):
        text = self.wait_for_element(self.HEADER_PANEL)
        assert text.is_displayed(), f"Авторизации на странице админ не было"

    def select_element_page(self):
        return self.wait_for_element(self.DEMO_BTH)

    def select_menu_block(self):
        """Ждем появления элемента в коде и кликаем в обход анимаций."""
        self.driver.switch_to.default_content()  # На всякий случай выходим из фреймов
        # 1. Ждем просто видимости элемента на экране
        el = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.MENU_BLOCK)
        )
        # 2. Кликаем с помощью JS, ему не страшны анимации и перекрытия
        self.driver.execute_script("arguments[0].click();", el)


    def subtab_catalog_click(self):
        """Ждем появления элемента в коде и кликаем в обход анимаций."""
        self.driver.switch_to.default_content()  # На всякий случай выходим из фреймов
        # 1. Ждем просто видимости элемента на экране
        el = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.CATALOG_SUBTAB)
        )
        # 2. Кликаем с помощью JS, ему не страшны анимации и перекрытия
        self.driver.execute_script("arguments[0].click();", el)


    def subtab_products_click(self):
        """Ждем появления элемента в коде и кликаем в обход анимаций."""
        self.driver.switch_to.default_content()  # На всякий случай выходим из фреймов
        # 1. Ждем просто видимости элемента на экране
        el = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.PRODUCTS_SUBTAB)
        )
        # 2. Кликаем с помощью JS, ему не страшны анимации и перекрытия
        self.driver.execute_script("arguments[0].click();", el)
        return self


    def check_product_page(self):
        el_text = self.wait_for_element(self.PRODUCTS_PAGE_ADMIN)
        assert el_text.is_displayed(), "Перехода на страницу Products не было"

    def new_product_button(self):
        self.wait_for_element(self.NEW_PRODUCT_BUTTON).click()

    def open_product_modal_and_select_standard(self):
        # 1. Ждем фрейм и переключаемся внутрь него
        iframe = self.wait_for_element(self.MODAL_CREATE_PRODUCT)
        self.driver.switch_to.frame(iframe)

        try:
            # 2. Ждем кнопку выбора продукта и кликаем
            standard_btn = self.wait_for_element(self.MODAL_STANDARD_PRODUCT_BTN)
            standard_btn.click()
            # 3. Ждем появления финальной кнопки добавления товара
            btn_add_new_product = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.MODAL_NEW_ADD_PRODUCT)
            )
            # Используем JS, чтобы обойти перекрытие панелью Symfony
            self.driver.execute_script("arguments[0].click();", btn_add_new_product)
        finally:
            # 4. Возвращаемся обратно на главную страницу (выходим из iframe при любом исходе)
            self.driver.switch_to.default_content()
        # Возвращаем self для удобства построения цепочек методов
        return self

    def check_form_new_product(self):
        el = self.wait_for_element(self.CHECK_CREATE_NEW_PRODUCT)
        assert el.is_displayed(), "Страница создания нового товара не открыта"

    def name_new_product(self, product_name):
        input_el = self.wait_for_element(self.CHECK_CREATE_NEW_PRODUCT)
        input_el.click()
        input_el.send_keys(product_name)

    def save_new_product(self):
        el = self.wait_for_element(self.SAVE_BTH_NEW_PRODUCT)
        assert el.is_displayed(), "Кнопка сохранения изменений в новом товаре не активна"
        el.click()

    def check_message_save_product(self, expected_text):

        el = self.wait_for_presence(self.CREATE_MESSAGE_ALERT)
        # Получаем текст и сравниваем
        actual_text = el.text.strip()
        assert actual_text == expected_text, (
            f"Отображаемый текст сообщения '{actual_text}' не совпадает с ожидаемым. "
            f"Ожидаемый текст: {expected_text}"
        )

    def select_new_product(self, product_name: str):
        """
        Ждет появления товара по его динамическому имени и кликает по нему.
        """
        # 1. Создаем динамический XPath с именем товара
        product_xpath = f"//div[@id='product_grid']//*[contains(text(), '{product_name}')]"
        # 2. Ждем, пока элемент станет видимым и доступным для клика
        product_element = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, product_xpath))
        )
        # 3. Кликаем по найденному товару
        product_element.click()
        return product_name

# Методы для удаления продукта из списка
    def go_to_catalog(self):
        el = self.wait_for_element(self.GOTO_CATALOG)
        el.click()


    def select_product_delete(self):
        """Поиск товара из списка, для его удаления"""
        el = self.wait_for_element(self.PRODUCT_DELETE)
        assert el.is_displayed(),"Кнопка возврата к каталогу товаров не отображается"



    def select_submit_menu_product(self):
        """Поиск подменю на товаре: preview, duplicate, delete"""
        el = self.wait_for_element(self.SUBMIT_DROPDOWN_PRODUCT)
        assert el.is_displayed(), "Кнопка вызова подменю в строке товара не отображается на странице"
        el.click()


    def menu_product_delete(self):
        """Ждем появления элемента в коде и кликаем в обход анимаций."""
        self.driver.switch_to.default_content()  # На всякий случай выходим из фреймов
        # 1. Ждем просто видимости элемента на экране
        el = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.DELETE_BTH_MENU)
        )
        # 2. Кликаем с помощью JS, ему не страшны анимации и перекрытия
        self.driver.execute_script("arguments[0].click();", el)

    def modal_dialog_delete(self):
        """Ждём появления диалогового окна при удалении и подтверждаем удаление."""
        # Ждём, пока появится модальное окно (по классу .modal-dialog)
        el = self.wait_for_element(self.DELETE_MESSAGE_DIALOG)
        assert el.is_displayed(), "Диалоговое окно удаления не отображается на странице"
        # Находим кнопку Delete внутри модального окна
        delete_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.DELETE_BUTTON_MODAL)
        )
        delete_btn.click()

        return self
