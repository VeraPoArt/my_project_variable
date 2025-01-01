from playwright.sync_api import expect
from config.config import ENV_CONFIG
import pytest

@pytest.fixture(scope="session")
def base_url():
    return ENV_CONFIG["qa"]["base_url"]

@pytest.fixture(autouse=True)
def clear_cookies(page):
    # Очищаем состояние страницы перед каждым тестом
    context = page.context
    context.clear_cookies()

def test_click_button(page, base_url):
    # Открываем страницу
    page.goto(f"{base_url}/simple-html-elements-for-automation/")

    # Нажимаем на кнопку по атрибуту name
    page.click("button[name='button1']")

    # Проверяем, что произошло перенаправление на новую страницу
    expect(page).to_have_url(f"{base_url}/button-success/?button1=")
    expect(page.locator("h1.entry-title")).to_have_text("Button success")

def test_click_link(page, base_url):
    # Открываем страницу
    page.goto(f"{base_url}/simple-html-elements-for-automation/")

    # Кликаем по ссылке используя относительный путь
    page.click("a[href='../link-success/']")

    # Проверяем, что открылась нужная страница
    expect(page).to_have_url(f"{base_url}/link-success/")
    expect(page.locator("h1.entry-title")).to_have_text("Link success")

def test_text_input(page, base_url):
    # Открываем страницу
    page.goto(f"{base_url}/simple-html-elements-for-automation/")

    # Вводим имя пользователя
    name_input = page.get_by_placeholder("Name")
    name_input.click()
    name_input.fill("Test User")

    # Вводим email
    email_input = page.get_by_placeholder("Email Address")
    email_input.click()
    email_input.fill("test@mail.ru")

    # Нажимаем кнопку отправки
    page.get_by_role("button", name="Email Me!").click()

    # Проверяем появление сообщения
    success_message = page.get_by_text("Thanks for contacting us")
    success_message.scroll_into_view_if_needed()
    expect(success_message).to_be_visible()

def test_radio_buttons(page, base_url):
    # Открываем страницу
    page.goto(f"{base_url}/simple-html-elements-for-automation/")

    # Находим и прокручиваем до радиокнопки
    female_radio = page.locator("input[value='female']")
    female_radio.scroll_into_view_if_needed()

    # Кликаем по радиокнопке
    female_radio.click()

    # Проверяем, что радиокнопка выбрана
    expect(female_radio).to_be_checked()

def test_checkboxes(page, base_url):
    # Открываем страницу
    page.goto(f"{base_url}/simple-html-elements-for-automation/")

    # Устанавливаем флажок "Bike"
    page.click("input[value='Bike']")


def test_select_option(page, base_url):
    # Открываем страницу
    page.goto(f"{base_url}/simple-html-elements-for-automation/")
    page.wait_for_load_state('networkidle')

    # Находим селект по роли и выбираем значение
    select = page.get_by_role("combobox")
    select.scroll_into_view_if_needed()
    select.select_option("audi")

    # Проверяем, что "Audi" выбрано
    expect(select).to_have_value("audi")

def test_table_data(page, base_url):
    # Открываем страницу
    page.goto(f"{base_url}/simple-html-elements-for-automation/")
    page.wait_for_load_state('networkidle')

    # Находим и прокручиваем до таблицы
    table_cell = page.locator("table#htmlTableId tbody tr:nth-child(2) td:nth-child(1)")
    table_cell.scroll_into_view_if_needed()

    # Проверяем содержимое ячейки
    expect(table_cell).to_have_text("Software Development Engineer in Test")
