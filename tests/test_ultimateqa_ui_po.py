import pytest
from pages.simple_elements_page import SimpleElementsPage
import allure


@allure.testcase("TMS-001", "Тест ввода текста")
@allure.title("Проверка ввода текста в форму")
@allure.severity(allure.severity_level.NORMAL)
def test_text_input_po(page, config):
    elements_page = SimpleElementsPage(page)
    elements_page.navigate(config["base_url"])
    elements_page.fill_contact_form("Test User", "test@mail.ru")
    elements_page.verify_success_message()

@allure.testcase("TMS-002", "Тест радио-кнопок")
@allure.title("Выбор радио-кнопки 'female'")
@allure.severity(allure.severity_level.NORMAL)
def test_radio_buttons_po(page, config):
    elements_page = SimpleElementsPage(page)
    elements_page.navigate(config["base_url"])
    elements_page.select_female_radio()

@allure.testcase("TMS-003", "Тест чекбоксов")
@allure.title("Выбор чекбокса 'Bike'")
@allure.severity(allure.severity_level.NORMAL)
def test_checkboxes_po(page, config):
    elements_page = SimpleElementsPage(page)
    elements_page.navigate(config["base_url"])
    elements_page.select_bike_checkbox()

@allure.testcase("TMS-004", "Тест выпадающего списка")
@allure.title("Выбор автомобиля 'Audi'")
@allure.severity(allure.severity_level.NORMAL)
def test_select_option_po(page, config):
    elements_page = SimpleElementsPage(page)
    elements_page.navigate(config["base_url"])
    elements_page.select_car("audi")

@allure.testcase("TMS-005", "Тест данных таблицы")
@allure.title("Проверка текста ячейки таблицы")
@allure.severity(allure.severity_level.NORMAL)
def test_table_data_po(page, config):
    elements_page = SimpleElementsPage(page)
    elements_page.navigate(config["base_url"])
    elements_page.verify_table_cell_text() 