import pytest
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture
def wait(browser: WebDriver) -> WebDriverWait:
    """Фикстура для явного ожидания"""
    return WebDriverWait(driver=browser, timeout=10)


def test_homepage_elements(browser: WebDriver, base_url: str, wait: WebDriverWait) -> None:
    """Тест, содержащий все проверки элементов на Главной странице"""
    browser.get(base_url)

    # 1. Проверка наименования вкладки
    assert 'PrestaShop' in browser.title

    # 2. Проверка наличия блока поиска по каталогу
    search_input = wait.until(EC.presence_of_element_located((By.NAME, "s")))
    assert search_input.is_displayed()

    # 3. Проверка текста-баннера POPULAR PRODUCTS
    element_popular_products = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "h2.products-section-title"))
    )
    assert 'POPULAR PRODUCTS' in element_popular_products.text

    # 4. Проверка наличия блока авторизации
    sign_in_element = wait.until(EC.visibility_of_element_located((By.XPATH, "//span[text()='Sign in']")))
    assert sign_in_element.is_displayed()

    # 5. Проверка наличия блока выбора валюты
    currency_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#_desktop_currency_selector button"))
    )
    assert "EUR" in currency_button.text


def test_catalog_elements(browser: WebDriver, base_url: str, wait: WebDriverWait) -> None:
    """Тест, содержащий все проверки элементов на странице каталога"""
    locator = (By.XPATH, "//a[@href='http://localhost:8081/3-clothes']")
    clothes_link = wait.until(EC.element_to_be_clickable(locator))
    clothes_link.click()
    # 1. Проверка успешного перехода в каталог
    check_element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".block-categories")))
    assert "CLOTHES\nMen\nWomen" in check_element.text

    # 2. Проверка наличия подкатегорий каталога
    check_drop_catalog = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".block-categories .category-sub-menu")))
    assert "Men\nWomen" in check_drop_catalog.text

    # 3. Проверка наличия блока бренды
    check_brands = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='search_filters_brands']")))
    assert 'BRANDS\n' in check_brands.text

    # 4. Проверка блока для перехода
    element_subcategories = wait.until(EC.visibility_of_element_located((By.XPATH, "//h2[text()='Subcategories']")))
    assert 'Subcategories' in element_subcategories.text

    # 5. Проверка блока Одежда
    element_check_clothec = wait.until(
        EC.visibility_of_element_located((By.XPATH, "//div[@class='block-category card card-block']")))
    assert 'CLOTHES\n' in element_check_clothec.text


def test_product_page(browser: WebDriver, base_url: str, wait: WebDriverWait) -> None:
    """Тест по карточке товара"""
    locator = (By.CSS_SELECTOR, "img[alt='Hummingbird printed t-shirt']")
    product_page = wait.until(EC.element_to_be_clickable(locator))
    product_page.click()
    # 1. Проверка корректности открытия карточки товара (по заголовку)
    check_product = wait.until(
        EC.visibility_of_element_located((By.XPATH, "//h1[text()='Hummingbird printed t-shirt']")))
    assert 'HUMMINGBIRD PRINTED T-SHIRT' in check_product.text, "На странице нет заголовка с текстом: 'HUMMINGBIRD PRINTED T-SHIRT'"

    # 2. Проверка отображения блока описания товара на странице
    product_description = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "#product-description-short-1")))
    assert product_description.is_displayed(), "Краткое описание товара не отображается на странице"
    expected_text = "Regular fit, round neckline, short sleeves"
    assert expected_text in product_description.text, (
        f"Ожидаемый текст '{expected_text}' не найден в описании"
    )

    # 3. Проверка наличия изображения товара на странице
    product_image = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".images-container.js-images-container")))
    assert product_image.is_displayed(), "Не отображается фото товара"

    # 4. Проверка отображения цены товара
    product_price = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".product-prices.js-product-prices")))
    assert product_price.is_displayed(), "Цена товара не отображается"

    # 5. Проверка отображения кнопки Добавить в корзину
    product_to_card = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "button[data-button-action='add-to-cart']")))
    assert product_to_card.is_displayed(), "Кнопка добавления товара в корзину не отображается"


def test_go_to_login_page(browser: WebDriver, base_url: str, wait: WebDriverWait) -> None:
    """Тест странице логина"""
    # 1. Переход на страницу login, проверка наименования страницы в барузере
    login_page_locator = wait.until(EC.visibility_of_element_located((By.XPATH, "//span[text()='Sign in']")))
    login_page_locator.click()
    assert 'Login' in browser.title

    # 2. Проверка наличия кнопки для входа на странице
    submit_login = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "#submit-login"))
    )
    assert submit_login.is_displayed(), "Кнопка входа на странице не отображается"
    # 3. Проверка наличия поля для ввода адреса электронной почты (email)
    email_input = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#field-email")))
    assert email_input.is_displayed(), "Не отображается поле ввода email"
    # 4. Проверка наличия поля для ввода пароля (password)
    password_input = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#field-password")))
    assert password_input.is_displayed(), "Не отображается поле ввода password"
    # 5. Проверка кнопки Регистрации нового пользователя
    new_account_button = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "a[data-link-action='display-register-form']")))
    assert new_account_button.is_displayed(), "Не отображается кнопка регистрации нового пользователя"


def test_go_to_login_page(browser: WebDriver, base_url: str, wait: WebDriverWait) -> None:
    browser.get(f"{base_url}login")
    login_new_email = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#field-email")))
    assert login_new_email.is_displayed(), "Поле ввода login (email) не отображается на странице"
    login_new_email.click()
    login_new_email.send_keys("gerasimowa@inbox.ru")
    login_new_password = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#field-password")))
    assert login_new_password.is_displayed(), "Поле ввода login (password) не отображается на странице"
    login_new_password.click()
    login_new_password.send_keys("1234lanos!")
    button_sign_in = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#submit-login')))
    assert button_sign_in.is_displayed(), "Кнопка submit-login(SIGN IN) не отображается на странице"
    button_sign_in.click()
    login_new_check = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#_desktop_user_info .user-info')))
    assert login_new_check.is_displayed()
    assert 'Sign out adminn lanos' in login_new_check.text
    sing_out = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'a.logout')))
    sing_out.click()
    logaut_check = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#_desktop_user_info .user-info')))
    assert logaut_check.is_displayed()
    assert 'Sign in' in logaut_check.text

def test_registration_page(browser: WebDriver, base_url: str, wait: WebDriverWait) -> None:
    """Тест странице регистрации нового пользователя"""
    login_page_locator = wait.until(EC.visibility_of_element_located((By.XPATH, "//span[text()='Sign in']")))
    login_page_locator.click()
    # 1. Переход на страницу Registration, проверка наименования страницы в барузере
    new_account_button = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "a[data-link-action='display-register-form']")))
    new_account_button.click()
    assert 'Registration' in browser.title
    # 2. Проверка заголовка на странице
    header_element = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".page-header h1"))
    )
    assert header_element.is_displayed(), "Заголовок страницы регистрации не отображается"
    assert header_element.text.strip() == "Create an account", (
        f"Текст заголовка '{header_element.text}' не совпадает с ожидаемым"
    )
    #3. Проверка поля для ввода имени
    firstname_input = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#field-firstname")))
    assert firstname_input.is_displayed(), "Поле ввода имени (firstname) не отображается на странице"

    #4. Проверка поля для ввода фамилии
    firstname_input = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#field-lastname")))
    assert firstname_input.is_displayed(), "Поле ввода имени (firstname) не отображается на странице"

    #5. Проверка кнопки Сохранить
    save_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-link-action='save-customer']"))
    )
    assert save_button.is_displayed(), "Кнопка Сохранить не отображается на странице"

def test_product_order(browser: WebDriver, base_url: str, wait: WebDriverWait) -> None:
    """Тест добавления товара с главной страницы в корзину, и проверка его отображения в ней"""
    #Возврат на Главную страницу
    home_link = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//a[./span[text()='Home']]"))
    )
    home_link.click()
    assert browser.current_url == base_url or browser.current_url == f"{base_url}/"

    #Проверка, что корзина пуста перед добавлением товара
    cart_count_element = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".blockcart .cart-products-count"))
    )
    assert cart_count_element.text == "(0)", f"Ожидалась пустая корзина, но отображается: {cart_count_element.text}"
    #Выбор товара и добавление его в корзину
    locator = (By.CSS_SELECTOR, "img[alt='Hummingbird printed t-shirt']")
    product_page = wait.until(EC.element_to_be_clickable(locator))
    product_page.click()
    product_to_cart = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-button-action='add-to-cart']"))
    )
    product_to_cart.click()

    # СТАБИЛЬНОЕ ОЖИДАНИЕ МОДАЛЬНОГО ОКНА:
    # 1. Сначала ждем, что контейнер модалки вообще появился в DOM (используем ID, специфичный для PrestaShop)
    modal_container = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#blockcart-modal"))
    )

    # 2. Ждем, пока само окно или текст в нем станут окончательно видимыми
    success_message = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "#blockcart-modal .modal-header h4.modal-title"))
    )

    assert "Product successfully added" in success_message.text, (
        f"Ожидался текст об успешном добавлении, но получено: '{success_message.text}'"
    )

    # Кнопку закрытия ищем внутри модального окна
    close_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#blockcart-modal button.close"))
    )
    close_button.click()

    cart_count_element_check = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".blockcart .cart-products-count")))
    assert cart_count_element_check.text == "(1)", f"Ожидается отображение одного товара в корзине, но отображается: {cart_count_element.text}"

def test_currency_change(browser: WebDriver, base_url: str, wait: WebDriverWait) -> None:
    """Тест переключения валюты, с проверкой, что валюта изменена на товарах в каталоге"""
    currency_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Currency dropdown']")))
    currency_button.click()
    usd_option = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#_desktop_currency_selector a[title='US Dollar']")))
    usd_option.click()
    current_currency = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "#_desktop_currency_selector button span._gray-darker"))
    )

    # Проверяем, что текст кнопки обновился на 'USD $'
    assert current_currency.text == "USD $", f"Ожидалась валюта USD $, но отображается: '{current_currency.text}'"
    locator = (By.XPATH, "//a[@href='http://localhost:8081/3-clothes']")
    clothes_link = wait.until(EC.element_to_be_clickable(locator))
    clothes_link.click()
    price_label = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "ul.faceted-slider[data-slider-label='Price'] p"))
    )
    assert "$21.00 - $42.00" in price_label.text, "Валюта на странице каталога не переключена на US Dollar$"

