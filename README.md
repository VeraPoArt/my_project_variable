# Playwright Tests

Добро пожаловать в репозиторий тестов, написанных с использованием **Playwright**!  
Здесь вы найдёте различные автотесты, которые покрывают как **API**, так и **UI** функциональность приложения, а также примеры использования **асинхронных тестов**, **Page Object Model** и многое другое.

---

## Содержание
1. [conftest_async.py](#conftest_asyncpy)
2. [test_api_dop.py](#test_api_doppy)
3. [test_api_example_assert.py](#test_api_example_assertpy)
4. [test_api_example.py](#test_api_examplepy)
5. [test_api.py](#test_apipy)
6. [test_async_ui.py](#test_async_uipy)
7. [test_codegen_example1.py](#test_codegen_example1py)
8. [test_codegen_example2.py](#test_codegen_example2py)
9. [test_combined.py](#test_combinedpy)
10. [test_example.py](#test_examplepy)
11. [test_ui.py](#test_uipy)
12. [test_ultimateqa_ui_po.py](#test_ultimateqa_ui_popy)
13. [test_ultimateqa_ui.py](#test_ultimateqa_uipy)

---

## conftest_async.py
> **Файл**: `conftest_async.py`  
> ⚙️ **Назначение**: Содержит **асинхронные** фикстуры для тестов. Используется совместно с `test_async_ui.py`.  
>
> *Файл не запускается напрямую, но должен находиться в рабочем окружении для корректной работы асинхронных тестов.*

---

## test_api_dop.py
> **Файл**: `test_api_dop.py`  
> 🧪 **Назначение**: Дополнительные API-тесты, включая **негативные сценарии**. Проверяют работу API в более сложных ситуациях, чем базовые тесты.  
>
> **Как запускать**:
> ```bash
> pytest tests/test_api_dop.py --env=stage
> ```
> Запускайте эти тесты на окружении **stage**, чтобы убедиться, что API корректно обрабатывает сложные или неверные входные данные.

---

## test_api_example_assert.py
> **Файл**: `test_api_example_assert.py`  
> 🧩 **Назначение**: **Простые API-тесты** с использованием только `assert`. Подходит для быстрого старта и проверки базовой функциональности.  
>
> **Как запускать**:
> ```bash
> pytest tests/test_api_example_assert.py --env=test
> ```
> Используйте окружение **test** для быстрого цикла разработки и отладки.

---

## test_api_example.py
> **Файл**: `test_api_example.py`  
> 🧩 **Назначение**: **Простые API-тесты**, покрывающие базовые кейсы обращения к API.  
>
> **Как запускать**:
> ```bash
> pytest tests/test_api_example.py --env=test
> ```
> Также рекомендовано использовать окружение **test** для начальных проверок.

---

## test_api.py
> **Файл**: `test_api.py`  
> 🏗 **Назначение**: **Полное покрытие операций** с пользователями и контактами в API: регистрация, вход, получение, создание, обновление и удаление.  
>
> **Как запускать**:
> ```bash
> pytest tests/test_api.py --env=stage
> ```
> Рекомендуется использовать окружение **stage** для более широкого тестирования, приближенного к боевым условиям.

---

## test_async_ui.py
> **Файл**: `test_async_ui.py`  
> ⚡ **Назначение**: Тесты асинхронного пользовательского интерфейса. Убеждаемся, что асинхронные операции не блокируют UI и работают корректно.  
>
> **Как запускать все тесты**:
> ```bash
> pytest tests/test_async_ui.py --env=stage
> ```
>
> **Как запустить конкретный тест**:
> ```bash
> pytest tests/test_async_ui.py::имя_теста --env=stage
> ```

---

## test_codegen_example1.py
> **Файл**: `test_codegen_example1.py`  
> 🛠 **Назначение**: Адаптированный тест после записи **Playwright Inspector** (путь №1) с использованием фикстуры `page` из `conftest.py`.  
>
> **Как запускать**:
> ```bash
> pytest tests/test_codegen_example1.py --env=dev
> ```
> Запуск на окружении **dev** для отладки и первичной проверки работы.

---

## test_codegen_example2.py
> **Файл**: `test_codegen_example2.py`  
> 🛠 **Назначение**: Адаптированный тест после записи **Playwright Inspector** (путь №2) с использованием **контекста** внутри теста и фикстуры из `conftest.py`.  
>
> **Как запускать**:
> ```bash
> pytest tests/test_codegen_example2.py --env=dev
> ```
> Также рекомендуется окружение **dev** для облегчённого тестирования и отладки.

---

## test_combined.py
> **Файл**: `test_combined.py`  
> 🔀 **Назначение**: **Комбинированные тесты**, проверяющие сразу несколько функциональностей. Включают комплексные сценарии пользовательского взаимодействия, работу с несколькими вкладками и различные переходы между страницами.  
>
> **Как запускать**:
> ```bash
> pytest tests/test_combined.py --env=qa -v -s
> ```
> Рекомендуется использовать окружение **qa** для более всесторонней проверки.

---

## test_example.py
> **Файл**: `test_example.py`  
> 📄 **Назначение**: **Базовый** UI-тест для проверки открытия веб-страницы и наличия ожидаемого заголовка.  
>
> **Как запускать**:
> ```bash
> pytest tests/test_example.py --env=dev
> ```
> Тест служит первичной проверкой работоспособности и видимости ключевых элементов интерфейса.

---

## test_ui.py
> **Файл**: `test_ui.py`  
> 🌐 **Назначение**: **Интеграция API и UI-тестов**. Проверяются сценарии, когда необходимо использовать данные из API непосредственно в UI.  
>
> **Как запускать**:
> ```bash
> pytest tests/test_ui.py --env=stage
> ```
> Запускайте на **stage** для подтверждения стабильности интеграции.

---

## test_ultimateqa_ui_po.py
> **Файл**: `test_ultimateqa_ui_po.py`  
> 🏛 **Назначение**: Тесты, использующие **Page Object Model (POM)**, что упрощает поддержку и реюз методов взаимодействия со страницей.  
>
> В качестве примера POM есть файл `pages\simple_elements_page.py`.  
>
> **Как запускать**:
> ```bash
> pytest tests/test_ultimateqa_ui_po.py --env=qa
> ```
> Окружение **qa** хорошо подходит для комплексного UI-тестирования.

---

## test_ultimateqa_ui.py
> **Файл**: `test_ultimateqa_ui.py`  
> 🖱 **Назначение**: Проверка UI-элементов — ввод текста, нажатие кнопок, выбор элементов из списков, клики по радиокнопкам и т.д.  
>
> **Как запускать**:
> ```bash
> pytest tests/test_ultimateqa_ui.py --env=qa
> ```
> Запуск этих тестов на **qa** помогает убедиться, что интерфейс сохраняет работоспособность при пользовательских сценариях.

---

### Общие рекомендации по запуску
1. Установить все зависимости (включая Playwright) и проинициализировать браузеры, выполнив:
   ```bash
   pip install -r requirements.txt
   playwright install
