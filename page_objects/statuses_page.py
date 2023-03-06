from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait

from page_objects.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from widgets.simple_ember_widgets import BasicDropDown
from widgets.simple_ember_widgets import SortableTable

STATUS_NAME_HEADER = "STATUS NAME"


class StatusesPage(BasePage):

    def check_status_is_displayed_in_table(self, status_name):
        table_element = self.get_statuses_table()
        is_new_status_displayed = SortableTable(table_element) \
            .find_row_with_text_for_column(STATUS_NAME_HEADER, status_name) \
            .is_row_displayed()
        assert is_new_status_displayed
        return self

    def check_status_is_not_displayed_in_table(self, status_name):
        statuses = SortableTable(self.get_statuses_table()).get_all_text_for_column(STATUS_NAME_HEADER)
        assert status_name.upper() not in statuses
        return self

    def get_statuses_table(self):
        return self.element((By.CSS_SELECTOR, "[data-test-id='statuses-table']"))

    def mark_status_as_default(self, status_name):
        table_element = self.get_statuses_table()
        default_status_column = SortableTable(table_element) \
            .find_row_with_text_for_column(STATUS_NAME_HEADER, status_name) \
            .get_column("DEFAULT STATUS")
        # Inject JS to track AJAX call made
        self.inject_JS_to_track_activeXHRs()
        # Make default link appears only on focus...
        if len(default_status_column.find_elements(By.CSS_SELECTOR, "[data-test-id='default-status']")) > 0:
            return self
        ActionChains(self.driver).move_to_element(default_status_column).click().perform()
        # Wait for the status to be marked as default
        self.wait_for_all_ajax_to_complete()
        self.element((By.CSS_SELECTOR, "[data-test-id=default-status]"))
        return self

    def add_status(self, status_name, status_behaviour):
        first_status = self.element(self.get_display_status_columns_locator())
        self.click_new_status_button() \
            .input_status_name(status_name) \
            .select_behaviour(status_behaviour) \
            .click_add_status_button()
        self.wait_for_invisibility_of_element_located_by((By.CSS_SELECTOR, "[data-test-id='add-status-header']"))
        self.wait_for_stale(first_status)
        return self

    def remove_status(self, status_name):
        self.inject_JS_to_track_activeXHRs()

        SortableTable(self.get_statuses_table()) \
            .find_row_with_text_for_column(STATUS_NAME_HEADER, status_name) \
            .click_row()

        self.element((By.CSS_SELECTOR, "[data-test-id='status-delete-trigger']")).click()
        self.wait_for_all_ajax_to_complete()

        xpath_for_dropdown = "//div[@data-test-id='form-field-alternateEntity']//div[@data-ebd-id]"
        if len(self.driver.find_elements(By.XPATH, xpath_for_dropdown)) > 0:
            dropdown_element = self.element((By.XPATH, xpath_for_dropdown))
            BasicDropDown(dropdown_element).select_by_index(0)

        self.element((By.CSS_SELECTOR, "[data-test-id='delete-dependants-primary-action']")).click()

        # When multiple issues have this status, then it takes time to reassign to new value
        self.wait_for_invisibility_of_element_located_by((By.CSS_SELECTOR, ".hf-ticket-action_loader"), 60)
        toast_locator = (By.CSS_SELECTOR, "[data-test-id='toast-message']")
        assert self.element(toast_locator).is_displayed()
        self.wait_for_invisibility_of_element_located_by(toast_locator)
        return self

    def click_add_status_button(self):
        self.element((By.CSS_SELECTOR, "[data-test-id='add-status']")).click()
        return self

    def select_behaviour(self, status_behaviour):
        drop_down_element = self.element((By.CSS_SELECTOR, "[aria-label='Behavior']"))
        BasicDropDown(drop_down_element) \
            .select_by_text(status_behaviour)
        return self

    def input_status_name(self, status_name):
        self.element((By.CSS_SELECTOR, "[data-test-id='form-field-name']")).send_keys(status_name)
        return self

    @staticmethod
    def get_display_status_columns_locator():
        return By.XPATH, "//table//div[contains(@class,'display-status')]"

    def click_new_status_button(self):
        self.element((By.CSS_SELECTOR, "[data-test-id='new-status']")).click()
        return self

    def navigate_to_statuses_page(self):
        self.navigate_to_page_from_nav_bar("Statuses")
        return self
