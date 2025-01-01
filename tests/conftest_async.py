"""
Этот файл содержит асинхронные фикстуры для тестов.
Используется совместно с test_async_ui.py.

Для работы асинхронных тестов требуется:
1. pytest-asyncio
2. Конфигурация в pytest.ini 
"""


import pytest
from playwright.async_api import async_playwright
import asyncio
import time

@pytest.fixture(scope="function")
async def async_playwright_instance():
    async with async_playwright() as p:
        yield p

@pytest.fixture(scope="function")
async def async_browser(async_playwright_instance):
    browser = await async_playwright_instance.chromium.launch(
        headless=True,  # Показываем браузер
        slow_mo=500      # Замедляем действия для наглядности
    )
    yield browser
    await browser.close()

@pytest.fixture(scope="function")
async def async_page(async_browser):
    context = await async_browser.new_context(
        viewport={"width": 1920, "height": 1080}
    )
    page = await context.new_page()
    yield page
    await page.close()
    await context.close()

@pytest.fixture(scope="function")
async def async_api_request_context(async_playwright_instance, config):
    request_context = await async_playwright_instance.request.new_context(
        base_url=config["api_base_url"]
    )
    yield request_context
    await request_context.dispose()

@pytest.fixture
async def async_auth_token(async_api_request_context, config):
    print("\n=== Получаем токен авторизации ===")
    unique_email = f"testuser{int(time.time())}@example.com"
    
    # 1. Регистрация нового пользователя
    register_payload = {
        "firstName": "Test",
        "lastName": "User",
        "email": unique_email,
        "password": config["password"]
    }
    print(f"\nРегистрируем пользователя: {unique_email}")
    print(f"URL: {config['api_base_url']}/users")
    print(f"Payload: {register_payload}")
    
    response = await async_api_request_context.post("/users", data=register_payload)
    print(f"Статус регистрации: {response.status}")
    print(f"Ответ: {await response.text()}")
    assert response.ok, "Failed to register user"
    
    # 2. Логин
    login_payload = {
        "email": unique_email,
        "password": config["password"]
    }
    print(f"\nВыполняем вход для: {unique_email}")
    print(f"URL: {config['api_base_url']}/users/login")
    print(f"Payload: {login_payload}")
    
    response = await async_api_request_context.post("/users/login", data=login_payload)
    print(f"Статус входа: {response.status}")
    print(f"Ответ: {await response.text()}")
    assert response.ok, f"Login failed with status {response.status}"
    
    token = (await response.json())["token"]
    print(f"\nПолучен токен: {token[:10]}...")
    return token 