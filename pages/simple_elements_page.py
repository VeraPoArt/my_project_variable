from playwright.sync_api import expect
import allure

class SimpleElementsPage:
    def __init__(self, page):
        self.page = page
        self.url = None
        
        # Локаторы для полей ввода
        self.name_input = page.get_by_placeholder("Name")
        self.email_input = page.get_by_placeholder("Email Address")
        self.email_me_button = page.get_by_role("button", name="Email Me!")
        self.success_message = page.get_by_text("Thanks for contacting us")

        # Локаторы для радио и чекбоксов
        self.female_radio = page.locator("input[value='female']")
        self.bike_checkbox = "input[value='Bike']"

        # Локатор для выпадающего списка
        self.car_select = page.get_by_role("combobox")

        # Локатор для таблицы
        self.table_cell = page.locator("table#htmlTableId tbody tr:nth-child(2) td:nth-child(1)")

    @allure.step("Переход на страницу с базовым URL: {base_url}")
    def navigate(self, base_url):
        self.url = f"{base_url}/simple-html-elements-for-automation/"
        self.page.goto(self.url)
        self.page.wait_for_load_state('networkidle')

    @allure.step("Заполнение формы контакта с именем: {name} и email: {email}")
    def fill_contact_form(self, name, email):
        self.name_input.click()
        self.name_input.fill(name)
        self.email_input.click()
        self.email_input.fill(email)
        self.email_me_button.click()

    @allure.step("Проверка видимости сообщения успеха")
    def verify_success_message(self):
        self.success_message.scroll_into_view_if_needed()
        expect(self.success_message).to_be_visible()

    @allure.step("Выбор радио-кнопки 'female'")
    def select_female_radio(self):
        self.female_radio.wait_for(state='visible')
        self.female_radio.scroll_into_view_if_needed()
        self.female_radio.click()
        expect(self.female_radio).to_be_checked()

    @allure.step("Выбор чекбокса 'Bike'")
    def select_bike_checkbox(self):
        self.page.click(self.bike_checkbox)

    @allure.step("Выбор автомобиля: {value}")
    def select_car(self, value):
        self.car_select.scroll_into_view_if_needed()
        self.car_select.select_option(value)
        expect(self.car_select).to_have_value(value)

    @allure.step("Проверка текста ячейки таблицы")
    def verify_table_cell_text(self):
        self.table_cell.scroll_into_view_if_needed()
        expect(self.table_cell).to_have_text("Software Development Engineer in Test") 