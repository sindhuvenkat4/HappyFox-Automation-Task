from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

from page_objects.base_page import BasePage
from widgets.simple_ember_widgets import SortableTable, BasicDropDown

PRIORITY_NAME_HEADER = "PRIORITY NAME"


class PrioritiesPage(BasePage):

    def navigate_to_priorities_page(self):
        self.navigate_to_page_from_nav_bar("Priorities")
        return self

    def add_priority(self, priority_name, description):
        first_row_element = self.element((By.CSS_SELECTOR, "[data-test-id='priorities-table'] tbody tr"))
        self.click_new_priority_button()\
            .input_priority_name(priority_name)\
            .input_priority_description(description)\
            .click_add_priority_button()
        self.wait_for_stale(first_row_element)
        return self

    def remove_priority(self, priority_name):
        self.inject_JS_to_track_activeXHRs()

        SortableTable(self.get_priorities_table()) \
            .find_row_with_text_for_column(PRIORITY_NAME_HEADER, priority_name) \
            .click_row()

        self.element((By.CSS_SELECTOR, "[data-test-id='priority-delete-trigger']")).click()
        self.wait_for_all_ajax_to_complete()

        xpath_for_dropdown = "//div[@data-test-id='form-field-alternateEntity']//div[@data-ebd-id]"
        if len(self.driver.find_elements(By.XPATH, xpath_for_dropdown)) > 0:
            dropdown_element = self.element((By.XPATH, xpath_for_dropdown))
            BasicDropDown(dropdown_element).select_by_index(0)

        self.element((By.CSS_SELECTOR, "[data-test-id='delete-dependants-primary-action']")).click()

        # When multiple issues have this priority, then it takes time to reassign to new value
        self.wait_for_invisibility_of_element_located_by((By.CSS_SELECTOR, ".hf-ticket-action_loader"), 60)
        toast_locator = (By.CSS_SELECTOR, "[data-test-id='toast-message']")
        assert self.element(toast_locator).is_displayed()
        self.wait_for_invisibility_of_element_located_by(toast_locator)
        return self

    def check_priority_is_not_displayed_in_table(self, priority_name):
        priorities = SortableTable(self.get_priorities_table()).get_all_text_for_column(PRIORITY_NAME_HEADER)
        assert priority_name not in priorities
        return self

    def mark_priority_as_default(self, priority_name):
        priorities_table = self.get_priorities_table()
        default_priority_column = SortableTable(priorities_table)\
            .find_row_with_text_for_column(PRIORITY_NAME_HEADER, priority_name)\
            .get_column("DEFAULT PRIORITY")
        # Inject JS to track AJAX call made
        self.inject_JS_to_track_activeXHRs()
        if len(default_priority_column.find_elements(By.CSS_SELECTOR, "[data-test-id='default-priority']")) > 0:
            return self
        # Make default link appears only on focus...
        ActionChains(self.driver).move_to_element(default_priority_column).click().perform()
        # Wait for the status to be marked as default
        self.wait_for_all_ajax_to_complete()
        self.element((By.CSS_SELECTOR, "[data-test-id=default-priority]"))
        return self

    def check_priorities_table_has_priority(self, priority_name):
        priorities_table = self.get_priorities_table()
        is_new_priority_displayed_in_table = SortableTable(priorities_table)\
            .find_row_with_text_for_column(PRIORITY_NAME_HEADER, priority_name)\
            .is_row_displayed()
        assert is_new_priority_displayed_in_table
        return self

    def get_priorities_table(self):
        return self.element((By.CSS_SELECTOR, "[data-test-id='priorities-table']"))

    def click_add_priority_button(self):
        self.element((By.CSS_SELECTOR, "[data-test-id='add-priority']")).click()
        self.wait_for_invisibility_of_element_located_by(self.get_priority_header_element())
        return self

    def input_priority_description(self, description):
        self.element((By.CSS_SELECTOR, "[data-test-id='form-field-description']")).send_keys(description)
        return self

    def input_priority_name(self, priority_name):
        self.element((By.CSS_SELECTOR, "[data-test-id='form-field-name']")).send_keys(priority_name)
        return self

    def click_new_priority_button(self):
        self.element((By.CSS_SELECTOR, "[data-test-id='new-priority']")).click()
        assert self.element(self.get_priority_header_element()).is_displayed()
        return self

    def get_priority_header_element(self):
        return (By.CSS_SELECTOR, "[data-test-id='add-priority-header']")
