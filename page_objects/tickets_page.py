from selenium.webdriver.common.by import By

from page_objects.base_page import BasePage
from widgets.simple_ember_widgets import TicketBox


class TicketsPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.wait_for_invisibility_of_element_located_by((By.CSS_SELECTOR, ".hf-list-dummy-tickets"))

    def check_ticket_status_by_title(self, ticket_title, expected_status):
        required_ticket = self.get_ticket_by_title(ticket_title)
        actual_status = TicketBox(required_ticket).get_ticket_status()
        assert expected_status.lower() == actual_status.lower()
        return self

    def check_ticket_priority_by_title(self, ticket_title, expected_priority):
        required_ticket = self.get_ticket_by_title(ticket_title)
        actual_priority = TicketBox(required_ticket).get_ticket_priority()
        assert expected_priority.lower() == actual_priority.lower()
        return self

    def open_ticket_by_title(self, ticket_title):
        required_ticket = self.get_ticket_by_title(ticket_title)
        TicketBox(required_ticket).open_ticket()

    def get_ticket_by_title(self, ticket_title):
        return self.element((By.XPATH, f"//article[@data-test-id='ticket-box'][contains(., '{ticket_title}')]"))
