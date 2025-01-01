from playwright.sync_api import expect
from config.config import ENV_CONFIG
import pytest
import allure

@pytest.fixture(scope="session")
def base_url():
    return ENV_CONFIG["qa"]["base_url"]

@pytest.fixture(autouse=True)
def clear_cookies(page):
    # Очищаем состояние страницы перед каждым тестом
    context = page.context
    context.clear_cookies()

@allure.testcase("TMS-001", "Тест клика на кнопке")
@allure.title("Клик на кнопке по атрибуту name")
@allure.severity(allure.severity_level.NORMAL)
def test_click_button(page, base_url):
    with allure.step("Открываем сайт"):
        page.goto(f"{base_url}/simple-html-elements-for-automation/")

    with allure.step("Нажимаем на кнопку по атрибуту name"):
        page.click("button[name='button1']")
        page.wait_for_url(f"{base_url}/button-success/?button1=", timeout=60000)

    with allure.step("Проверяем, что произошло перенаправление на новую страницу"):
        expect(page).to_have_url(f"{base_url}/button-success/?button1=")
        expect(page.locator("h1.entry-title")).to_have_text("Button success")

@allure.testcase("TMS-002", "Тест клика на ссылке")
@allure.title("Клик на ссылке по относительному пути")
@allure.severity(allure.severity_level.NORMAL)
def test_click_link(page, base_url):
    with allure.step("Открываем сайт"):
        page.goto(f"{base_url}/simple-html-elements-for-automation/")

    with allure.step("Кликаем по ссылке используя относительный путь"):
        page.click("a[href='../link-success/']")

    with allure.step("Проверяем, что открылась нужная страница"):
        expect(page).to_have_url(f"{base_url}/link-success/")
        expect(page.locator("h1.entry-title")).to_have_text("Link success")

@allure.testcase("TMS-003", "Тест ввода текста")
@allure.title("Ввод текста в форму")
@allure.severity(allure.severity_level.NORMAL)
def test_text_input(page, base_url):
    with allure.step("Открываем сайт"):
        page.goto(f"{base_url}/simple-html-elements-for-automation/")
        
    with allure.step("Вводим имя пользователя"):
        name_input = page.get_by_placeholder("Name")
        name_input.click()
        name_input.fill("Test User")

    with allure.step("Вводим email"):
        email_input = page.get_by_placeholder("Email Address")
        email_input.click()
        email_input.fill("test@mail.ru")

    with allure.step("Нажимаем кнопку отправки"):
        page.get_by_role("button", name="Email Me!").click()

    with allure.step("Проверяем появление сообщения"):
        success_message = page.get_by_text("Thanks for contacting us")
        success_message.scroll_into_view_if_needed()
        expect(success_message).to_be_visible(timeout=60000)

@allure.testcase("TMS-004", "Тест радио-кнопок")
@allure.title("Выбор радио-кнопки 'female'")
@allure.severity(allure.severity_level.NORMAL)
def test_radio_buttons(page, base_url):
    with allure.step("Открываем сайт"):
        page.goto(f"{base_url}/simple-html-elements-for-automation/")

    with allure.step("Находим и прокручиваем до радиокнопки"):
        female_radio = page.locator("input[value='female']")
        female_radio.scroll_into_view_if_needed()

    with allure.step("Кликаем по радиокнопке"):
        female_radio.click()

    with allure.step("Проверяем, что радиокнопка выбрана"):
        expect(female_radio).to_be_checked()

@allure.testcase("TMS-005", "Тест чекбоксов")
@allure.title("Выбор чекбокса 'Bike'")
@allure.severity(allure.severity_level.NORMAL)
def test_checkboxes(page, base_url):
    with allure.step("Открываем сайт"):
        page.goto(f"{base_url}/simple-html-elements-for-automation/")

    with allure.step("Устанавливаем флажок 'Bike'"):
        page.click("input[value='Bike']")

@allure.testcase("TMS-006", "Тест выпадающего списка")
@allure.title("Выбор автомобиля 'Audi'")
@allure.severity(allure.severity_level.NORMAL)
def test_select_option(page, base_url):
    with allure.step("Открываем сайт"):
        page.goto(f"{base_url}/simple-html-elements-for-automation/")
        page.wait_for_load_state('networkidle')

    with allure.step("Находим селект по роли и выбираем значение"):
        select = page.get_by_role("combobox")
        select.scroll_into_view_if_needed()
        select.select_option("audi")

    with allure.step("Проверяем, что 'Audi' выбрано"):
        expect(select).to_have_value("audi")

@allure.testcase("TMS-007", "Тест данных таблицы")
@allure.title("Проверка текста ячейки таблицы")
@allure.severity(allure.severity_level.NORMAL)
def test_table_data(page, base_url):
    with allure.step("Открываем сайт"):
        page.goto(f"{base_url}/simple-html-elements-for-automation/")
        page.wait_for_load_state('networkidle')

    # Находим и прокручиваем до таблицы
    table_cell = page.locator("table#htmlTableId tbody tr:nth-child(2) td:nth-child(1)")
    table_cell.scroll_into_view_if_needed()

    # Проверяем содержимое ячейки
    expect(table_cell).to_have_text("Software Development Engineer in Test")
