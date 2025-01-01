import pytest
from config.config import ENV_CONFIG
from playwright.sync_api import sync_playwright
import time
import json
import allure
import os



def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default="dev",
        help="Укажите окружение: dev, test или stage"
    )

@pytest.fixture(scope="session")
def config(request):
    env = request.config.getoption("--env")
    config = ENV_CONFIG.get(env)
    if not config:
        raise ValueError(f"Неизвестное окружение: {env}")
    return config

@pytest.fixture(scope="session")
def playwright_instance():
    with sync_playwright() as p:
        yield p

@pytest.fixture(scope="session")
def browser(playwright_instance):
    browser = playwright_instance.chromium.launch(
        headless=False,
        slow_mo=1000,
        args=['--window-size=1920,1080']
    )
    yield browser
    browser.close()

@pytest.fixture(scope="session")
def context(browser):
    context = browser.new_context(
        viewport={'width': 1920, 'height': 1080}
    )
    return context

@pytest.fixture(scope="function")
def page(browser):
    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    page = context.new_page()
    yield page
    page.close()
    context.close()


# conftest.py (продолжение)

@pytest.fixture(scope="session")
def api_request_context(playwright_instance, config):
    request_context = playwright_instance.request.new_context(
        base_url=config["api_base_url"]
    )
    yield request_context
    request_context.dispose()

import json

@pytest.fixture
def auth_token(api_request_context, config):
    # Генерируем уникальный email
    unique_email = f"testuser{int(time.time())}@example.com"
    
    # Регистрируем нового пользователя
    register_payload = {
        "firstName": "Test",
        "lastName": "User",
        "email": unique_email,
        "password": config["password"]
    }
    api_request_context.post("/users", data=register_payload)
    
    # Логинимся
    login_payload = {
        "email": unique_email,
        "password": config["password"]
    }
    response = api_request_context.post("/users/login", data=login_payload)
    assert response.ok, f"Login failed with status {response.status}"
    
    return response.json()["token"]

# Добавляем хук для получения информации о статусе теста
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # Запускаем тест
    outcome = yield
    report = outcome.get_result()
    
    # Проверяем, упал ли тест
    if report.when == "call" and report.failed:
        page = item.funcargs['page']
        screenshot_path = f"screenshots/{item.name}.png"
        page.screenshot(path=screenshot_path)  
    
        if os.path.exists(screenshot_path):
            allure.attach.file(
                screenshot_path,
                name="screenshot",
                attachment_type=allure.attachment_type.PNG
            )

