import pytest
from playwright.sync_api import expect

def test_multiple_tabs(page, config):
    # Открываем первую страницу и заполняем форму
    page.goto(f"{config['base_url']}/simple-html-elements-for-automation/")
    
    # Заполняем форму на первой вкладке
    name_input = page.get_by_placeholder("Name")
    name_input.click()
    name_input.fill("Test User")
    
    email_input = page.get_by_placeholder("Email Address")
    email_input.click()
    email_input.fill("test@mail.ru")
    
    # Открываем новую вкладку
    new_page = page.context.new_page()
    new_page.goto(f"{config['base_url']}/simple-html-elements-for-automation/")
    new_page.wait_for_load_state('networkidle')
    
    # Работаем во второй вкладке - выбираем опцию из выпадающего списка
    select = new_page.get_by_role("combobox")
    select.scroll_into_view_if_needed()
    select.select_option("audi")
    expect(select).to_have_value("audi")
    
    # Возвращаемся на первую вкладку и отправляем форму
    page.bring_to_front()
    page.get_by_role("button", name="Email Me!").click()
    
    # Проверяем сообщение об успехе
    success_message = page.get_by_text("Thanks for contacting us")
    success_message.scroll_into_view_if_needed()
    expect(success_message).to_be_visible()
    
    # Снова переключаемся на вторую вкладку и проверяем таблицу
    new_page.bring_to_front()
    table_cell = new_page.locator("table#htmlTableId tbody tr:nth-child(2) td:nth-child(1)")
    table_cell.scroll_into_view_if_needed()
    expect(table_cell).to_have_text("Software Development Engineer in Test") 