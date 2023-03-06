from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


class BasicDropDown:

    # Basic DropDown implementation
    # element should be div which has 'data-ebd-id' attribute attached to it
    def __init__(self, element):
        self.drop_down: WebElement = element
        self.id = self.drop_down.get_attribute("data-ebd-id").split("-")[0]
        self.container: WebElement = self.drop_down.find_element(By.XPATH, "..")

    def open(self):
        if self.drop_down.get_attribute("aria-expanded") != "true":
            self.drop_down.click()
        return self

    def close(self):
        if self.drop_down.get_attribute("aria-expanded") == "true":
            self.drop_down.click()
        return self

    def select_by_text(self, text):
        # If the intended option is already selected
        if self.get_selected_option() == text:
            return self
        option_elements = self._get_options()
        for option in option_elements:
            if option.text == text:
                option.click()
                return self
        # If the text is not a part of the dropdown
        raise ValueError(f"{text} is not a part of the dropdown!")

    def select_by_index(self, index):
        options_length = len(self._get_options())
        if index >= options_length:
            raise ValueError(f"{index} cannot be selected in this dropdown which has length of {options_length}")
        self._get_options()[index].click()

    def get_selected_option(self):
        return self.drop_down.text

    def _get_options(self):
        self.open()
        return self.container.find_elements(By.CSS_SELECTOR, f"[id='ember-power-select-options-{self.id}'] > li")


class SortableTable:

    # element could be any container that contains both table header and  table body
    def __init__(self, element):
        self.table_headers = None
        self.header_name_to_index_dict = None
        self.table_container: WebElement = element
        self.init_table_headers()

    def init_table_headers(self):
        self.table_headers = self.table_container.find_elements(By.CSS_SELECTOR, ".lt-head tr > th")
        self.header_name_to_index_dict = {header.text: index + 1 for index, header in enumerate(self.table_headers)}

    def get_column_index(self, column_name):
        return self.header_name_to_index_dict[column_name]

    def find_row_with_text_for_column(self, column_name, text):
        index = self.get_column_index(column_name)
        row_element = self.table_container.find_element(By.XPATH, f".//tbody/tr[./td[{index}][contains(., '{text}')]]")
        return SortableTable.SortableRow(self, row_element)

    def get_all_text_for_column(self, column_name):
        index = self.get_column_index(column_name)
        column_elements = self.table_container.find_elements(By.XPATH, f".//tbody/tr/td[{index}]")
        column_names = list(map(lambda column: column.text, column_elements))
        return column_names

    class SortableRow:

        def __init__(self, sortable_table, row_element):
            self.sortable_table = sortable_table
            self.row_element: WebElement = row_element

        def click_row(self):
            self.row_element.click()

        def is_row_displayed(self):
            return self.row_element.is_displayed()

        def get_column_value(self, column_name):
            return self.get_column(column_name).text

        def get_column(self, column_name):
            index = self.sortable_table.get_column_index(column_name)
            return self.row_element.find_element(By.XPATH, f"./td[{index}]")


class TicketBox:

    # WebElement should be the article which has 'data-test-id' attribute set to 'ticket-box'
    def __init__(self, element: WebElement):
        self.ticket_box = element

    def get_ticket_status(self):
        return self.ticket_box.find_element(By.CSS_SELECTOR, "[data-test-id='ticket-box_status']").text

    def get_ticket_priority(self):
        return self.ticket_box.find_element(By.CSS_SELECTOR, "[data-test-id='ticket-box_priority']").text

    def open_ticket(self):
        return self.ticket_box.find_element(By.XPATH, ".//a[contains(@data-test-id, 'link-to-ticket-details')]").click()
