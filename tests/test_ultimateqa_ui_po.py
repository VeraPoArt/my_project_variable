import pytest
from pages.simple_elements_page import SimpleElementsPage

def test_text_input_po(page, config):
    elements_page = SimpleElementsPage(page)
    elements_page.navigate(config["base_url"])
    elements_page.fill_contact_form("Test User", "test@mail.ru")
    elements_page.verify_success_message()

def test_radio_buttons_po(page, config):
    elements_page = SimpleElementsPage(page)
    elements_page.navigate(config["base_url"])
    elements_page.select_female_radio()

def test_checkboxes_po(page, config):
    elements_page = SimpleElementsPage(page)
    elements_page.navigate(config["base_url"])
    elements_page.select_bike_checkbox()

def test_select_option_po(page, config):
    elements_page = SimpleElementsPage(page)
    elements_page.navigate(config["base_url"])
    elements_page.select_car("audi")

def test_table_data_po(page, config):
    elements_page = SimpleElementsPage(page)
    elements_page.navigate(config["base_url"])
    elements_page.verify_table_cell_text() 