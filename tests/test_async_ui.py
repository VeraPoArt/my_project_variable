import pytest
from playwright.async_api import expect as async_expect
import asyncio
from .conftest_async import *  
import time

pytestmark = pytest.mark.asyncio

async def test_async_create_contacts_api_check_ui(async_page, async_auth_token, async_api_request_context, config):
    print(f"\nТокен авторизации: {async_auth_token[:10]}...")
    
    # Авторизация
    await async_page.goto(config["base_url"])
    
    # Устанавливаем токен в localStorage и cookie
    await async_page.evaluate(f"localStorage.setItem('token', '{async_auth_token}')")
    await async_page.context.add_cookies([{
        "name": "token",
        "value": async_auth_token,
        "url": config["base_url"]
    }])
    
    # Добавляем заголовок авторизации
    await async_page.set_extra_http_headers({
        "Authorization": f"Bearer {async_auth_token}"
    })
    
    # Переходим на страницу контактов
    await async_page.goto(f"{config['base_url']}/contactList")
    await async_page.wait_for_load_state("networkidle")
    
    # Создаем контакты через API
    contacts_data = [
        ("Alice", "Wonderland", "alice@example.com", "5551234567", "Wonderland St 123"),
        ("Bob", "Builder", "bob@example.com", "5557654321", "Construction Ave 456")
    ]
    
    for first_name, last_name, email, phone, address in contacts_data:
        print(f"\nСоздаем контакт: {first_name} {last_name}")
        payload = {
            "firstName": first_name,
            "lastName": last_name,
            "email": email,
            "phone": phone,
            "street1": address,
            "city": "Test City",
            "stateProvince": "TS",
            "postalCode": "12345",
            "country": "Test Country"
        }
        response = await async_api_request_context.post(
            "/contacts",
            data=payload,
            headers={"Authorization": f"Bearer {async_auth_token}"}
        )
        print(f"Статус создания контакта: {response.status}")
        assert response.ok, f"Failed to create contact {first_name} {last_name}"
    
    # Обновляем страницу
    await async_page.reload()
    await async_page.wait_for_load_state("networkidle")
    
    # Проверяем наличие контактов
    for first_name, last_name, _, _, _ in contacts_data:
        full_name = f"{first_name} {last_name}"
        print(f"\nИщем контакт: {full_name}")
        await async_expect(async_page.get_by_text(full_name)).to_be_visible(timeout=5000)

async def test_async_parallel_ui_api_check(async_page, async_auth_token, async_api_request_context, config):
    """
    Асинхронный тест для параллельной проверки контактов через API и UI
    """
    # Авторизуемся полностью
    await async_page.goto(config["base_url"])
    
    # Устанавливаем токен в localStorage и cookie
    await async_page.evaluate(f"localStorage.setItem('token', '{async_auth_token}')")
    await async_page.context.add_cookies([{
        "name": "token",
        "value": async_auth_token,
        "url": config["base_url"]
    }])
    
    # Добавляем заголовок авторизации
    await async_page.set_extra_http_headers({
        "Authorization": f"Bearer {async_auth_token}"
    })
    
    # Переходим на страницу контактов и ждем загрузки
    await async_page.goto(f"{config['base_url']}/contactList")
    await async_page.wait_for_load_state("networkidle")

    # Создаем тестовый контакт для проверки
    test_contact = {
        "firstName": "Test",
        "lastName": "Contact",
        "email": "test@example.com",
        "phone": "1234567890",
        "street1": "Test Street",
        "city": "Test City",
        "stateProvince": "TS",
        "postalCode": "12345",
        "country": "Test Country"
    }
    
    response = await async_api_request_context.post(
        "/contacts",
        data=test_contact,
        headers={"Authorization": f"Bearer {async_auth_token}"}
    )
    assert response.ok, "Failed to create test contact"

    # Обновляем страницу после создания контакта
    await async_page.reload()
    await async_page.wait_for_load_state("networkidle")

    # Асинхронная функция для проверки через API
    async def check_contacts_api():
        response = await async_api_request_context.get(
            "/contacts",
            headers={"Authorization": f"Bearer {async_auth_token}"}
        )
        assert response.ok
        return await response.json()

    # Асинхронная функция для получения контактов из UI
    async def get_contacts_ui():
        contacts_elements = await async_page.get_by_role("row").all()
        contacts = []
        for element in contacts_elements[1:]:  # Пропускаем заголовок таблицы
            text = await element.text_content()
            contacts.append(text)
        return contacts

    # Выполняем проверки параллельно
    api_contacts, ui_contacts = await asyncio.gather(
        check_contacts_api(),
        get_contacts_ui()
    )

    print("\nКонтакты из API:", api_contacts)
    print("\nКонтакты из UI:", ui_contacts)

    # Проверяем, что количество контактов совпадает
    assert len(api_contacts) == len(ui_contacts), f"""
        Количество контактов не совпадает:
        API контакты: {len(api_contacts)}
        UI контакты: {len(ui_contacts)}
        """

    # Проверяем, что все контакты из API отображаются в UI
    for contact in api_contacts:
        full_name = f"{contact['firstName']} {contact['lastName']}"
        assert any(full_name in ui_contact for ui_contact in ui_contacts), \
            f"Contact {full_name} from API not found in UI" 