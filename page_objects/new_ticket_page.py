from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

from page_objects.base_page import BasePage


class NewTicketPage(BasePage):

    def __init__(self, driver):
        # TODO : Get the Right URL as per the environment
        self.url = "https://interview2.supporthive.com/new/"
        super().__init__(driver)
        super().go()
        # Server returns 403 on submission of new ticket for some reason (maybe old CSRF token set during agent login
        # is not cleared/ server restricting Selenium scripts -- requests in quick succession)
        self.driver.refresh()

    def create_new_ticket(self, subject, message, full_name, email):
        self.input_subject(subject)\
            .input_message(message)\
            .input_full_name(full_name)\
            .input_email(email)\
            .click_create_ticket_button()
        return self

    def input_subject(self, subject):
        self.element((By.NAME, "subject")).send_keys(subject)
        return self

    def input_message(self, message):
        self.element((By.XPATH, "//div[@role='textbox']")).send_keys(message)
        return self

    def input_full_name(self, full_name):
        self.element((By.NAME, "name")).send_keys(full_name)
        return self

    def input_email(self, email):
        self.element((By.NAME, "email")).send_keys(email)
        return self

    def click_create_ticket_button(self):
        self.element((By.ID, "submit")).click()
        assert self.element((By.CSS_SELECTOR, ".hf-custom-message-after-ticket-creation")).is_displayed()
        return self
