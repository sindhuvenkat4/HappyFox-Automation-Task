from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from page_objects.base_page import BasePage


class LoginPage(BasePage):

    def __init__(self, driver):
        # TODO : Get the Right URL as per the environment
        self.url = "https://interview2.supporthive.com/staff/"
        super().__init__(driver)
        super().go()

    def login(self, username, password):
        self.input_username(username) \
            .input_password(password) \
            .click_login_button() \
            .wait_for_staff_menu_to_appear()
        return self

    def input_username(self, username):
        self.element((By.NAME, "username")).send_keys(username)
        return self

    def input_password(self, password):
        self.element((By.NAME, "password")).send_keys(password)
        return self

    def click_login_button(self):
        login_button = self.element((By.ID, "btn-submit"))
        login_button.click()
        self.wait_for_stale(login_button)
        return self

    def wait_for_staff_menu_to_appear(self):
        self.wait(EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-test-id='staff-menu']")), 15)