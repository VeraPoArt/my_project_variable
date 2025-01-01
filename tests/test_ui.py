from playwright.sync_api import expect
import pytest

def test_login_via_api_and_check_dashboard(page, auth_token, config):
    # Используем токен из фикстуры auth_token
    page.goto(config["base_url"])
    
    # Устанавливаем токен в localStorage и cookie
    page.evaluate(f"localStorage.setItem('token', '{auth_token}')")
    page.context.add_cookies([{
        "name": "token",
        "value": auth_token,
        "url": config["base_url"]
    }])
    
    # Добавляем заголовок авторизации
    page.set_extra_http_headers({
        "Authorization": f"Bearer {auth_token}"
    })
    
    # Переходим на страницу контактов
    page.goto(f"{config['base_url']}/contactList")
    
    # Ждем, пока страница полностью загрузится
    page.wait_for_load_state("networkidle")
    
    # Проверяем элементы на странице контактов
    expect(page.get_by_text("Contact List")).to_be_visible()
    expect(page.get_by_text("Logout")).to_be_visible()
    expect(page.get_by_text("Click on any contact to view the Contact Details")).to_be_visible()
    expect(page.get_by_text("Add a New Contact")).to_be_visible()

    # Проверяем наличие заголовков таблицы
    expect(page.locator("th", has_text="Name")).to_be_visible()
    expect(page.locator("th", has_text="Email")).to_be_visible()
    expect(page.locator("th", has_text="Phone")).to_be_visible()
    expect(page.locator("th", has_text="Address")).to_be_visible()

def test_create_contact_ui_and_verify_api(page, auth_token, api_request_context, config):
    # Авторизуемся через API token
    page.goto(config["base_url"])
    page.evaluate(f"localStorage.setItem('token', '{auth_token}')")
    page.context.add_cookies([{
        "name": "token",
        "value": auth_token,
        "url": config["base_url"]
    }])
    
    # Переходим на страницу контактов
    page.goto(f"{config['base_url']}/contactList")
    
    # Создаем новый контакт через UI
    expect(page.get_by_text("Add a New Contact")).to_be_visible()
    page.get_by_text("Add a New Contact").click()
    
    # Заполняем форму контакта
    page.get_by_label("First Name").fill("Alice")
    page.get_by_label("Last Name").fill("Wonder")
    page.get_by_label("Email").fill("alice@example.com")
    page.get_by_label("Phone").fill("5551234567")
    page.get_by_placeholder("Address 1").fill("Wonderland Street 123")
    page.get_by_label("City").fill("Magic City")
    page.get_by_label("State or Province").fill("WL")
    page.get_by_label("Postal Code").fill("12345")
    page.get_by_label("Country").fill("Wonderland")
    
    # Сохраняем контакт
    page.get_by_role("button", name="Submit").click()
    
    # Проверяем, что контакт создан в UI
    expect(page.get_by_text("Alice Wonder")).to_be_visible()
    
    # Проверяем через API
    response = api_request_context.get(
        f"{config['api_base_url']}/contacts",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.ok, "Failed to get contacts from API"
    
    contacts = response.json()
    found_contact = any(
        contact["firstName"] == "Alice" and contact["lastName"] == "Wonder"
        for contact in contacts
    )
    assert found_contact, "Contact not found in API response"

@pytest.mark.parametrize("contacts_data", [
    [
        ("Alice", "Wonderland", "alice@example.com", "5551234567", "Wonderland St 123"),
        ("Bob", "Builder", "bob@example.com", "5557654321", "Construction Ave 456"),
        ("Charlie", "Chaplin", "charlie@example.com", "5559876543", "Hollywood Blvd 789"),
        ("David", "Copperfield", "david@example.com", "5550123456", "Magic St 321")
    ]
])
def test_create_multiple_contacts(page, auth_token, api_request_context, config, contacts_data):
    # Авторизуемся через API token
    page.goto(config["base_url"])
    page.evaluate(f"localStorage.setItem('token', '{auth_token}')")
    page.context.add_cookies([{
        "name": "token",
        "value": auth_token,
        "url": config["base_url"]
    }])
    
    # Переходим на страницу контактов
    page.goto(f"{config['base_url']}/contactList")
    
    # Создаем контакты
    for first_name, last_name, email, phone, address in contacts_data:
        # Нажимаем кнопку добавления нового контакта
        expect(page.get_by_text("Add a New Contact")).to_be_visible()
        page.get_by_text("Add a New Contact").click()
        
        # Заполняем форму контакта
        page.get_by_label("First Name").fill(first_name)
        page.get_by_label("Last Name").fill(last_name)
        page.get_by_label("Email").fill(email)
        page.get_by_label("Phone").fill(phone)
        page.get_by_placeholder("Address 1").fill(address)
        page.get_by_label("City").fill("Test City")
        page.get_by_label("State or Province").fill("TS")
        page.get_by_label("Postal Code").fill("12345")
        page.get_by_label("Country").fill("Test Country")
        
        # Сохраняем контакт
        page.get_by_role("button", name="Submit").click()
        
        # Проверяем, что контакт создан в UI
        full_name = f"{first_name} {last_name}"
        expect(page.get_by_text(full_name)).to_be_visible()
    
    # Проверяем через API наличие всех созданных контактов
    response = api_request_context.get(
        f"{config['api_base_url']}/contacts",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.ok, "Failed to get contacts from API"
    
    contacts_from_api = response.json()
    
    # Проверяем каждый контакт
    for first_name, last_name, email, phone, _ in contacts_data:
        found_contact = any(
            api_contact["firstName"] == first_name and 
            api_contact["lastName"] == last_name and
            api_contact["email"] == email and
            api_contact["phone"] == phone
            for api_contact in contacts_from_api
        )
        assert found_contact, f"Contact {first_name} {last_name} not found in API response"