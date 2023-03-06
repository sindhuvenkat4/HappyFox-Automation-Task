from selenium.webdriver.common.by import By

from page_objects.base_page import BasePage
from widgets.simple_ember_widgets import TicketBox, BasicDropDown


class TicketDetailPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.wait_for_invisibility_of_element_located_by((By.CSS_SELECTOR, "article.hf-mod-dummy"))
        self.inject_JS_to_track_activeXHRs()

    def check_ticket_status(self, expected_status):
        actual_status = TicketBox(self.get_ticket()).get_ticket_status()
        assert expected_status.lower() == actual_status.lower()
        return self

    def check_ticket_priority(self, expected_priority):
        actual_priority = TicketBox(self.get_ticket()).get_ticket_priority()
        assert expected_priority.lower() == actual_priority.lower()
        return self

    def check_tags(self, expected_tag):
        actual_tag = self.element((By.CSS_SELECTOR, "[data-test-id='tag']")).text
        assert expected_tag == actual_tag
        return self

    def reply_with_canned_response(self, context, canned_action_name):
        self.click_reply_link() \
            .apply_canned_response(canned_action_name)

        # Get canned response's status and priority for validation and set to context
        canned_response_status = self.element((By.CSS_SELECTOR, ".hf-floating-editor_footer-container [data-test-id='ticket-box_status']")).text
        canned_response_priority = self.element((By.CSS_SELECTOR, ".hf-floating-editor_footer-container [data-test-id='ticket-box_priority']")).text

        self.element((By.CSS_SELECTOR, ".hf-floating-editor_footer-container [data-test-id='editor-add-tags-trigger']")).click()
        canned_response_tag = BasicDropDown(self.element((By.CSS_SELECTOR, "[aria-label='Add Tags']")))\
            .get_selected_option().split("\n")[1]

        context.canned_response_status = canned_response_status
        context.canned_response_priority = canned_response_priority
        context.canned_response_tag = canned_response_tag

        self.click_add_reply_button() \
            .check_ticket_updated_toast_is_displayed()
        self.wait_for_invisibility_of_element_located_by(self.get_toast_locator())
        return self

    def check_ticket_updated_toast_is_displayed(self):
        assert self.element(self.get_toast_locator()).is_displayed()
        return self

    @staticmethod
    def get_toast_locator():
        return By.XPATH, "//div[text()='Ticket has been updated successfully']"

    def click_add_reply_button(self):
        self.element((By.CSS_SELECTOR, "[data-test-id='add-update-reply-button']")).click()
        return self

    def apply_canned_response(self, canned_action_name):
        # Canned responses AJAX call needs to be completed before clicking 'Add Canned action' button
        self.wait_for_all_ajax_to_complete()
        # Waiting for one of the editor buttons to be displayed before adding canned action response
        # Otherwise, the selected canned response ends up not getting added to editor
        assert self.element((By.CSS_SELECTOR, "[title='Markdown']")).is_displayed()

        self.element((By.XPATH, "//*[@data-test-id='canned-action-trigger']/..")).click()
        dropdown_element = self.dom_element((By.CSS_SELECTOR, "[aria-label='Canned Action']"))
        BasicDropDown(dropdown_element).select_by_text(canned_action_name)
        self.element((By.CSS_SELECTOR, "[data-test-id='hf-add-canned-action']")).click()
        return self

    def click_reply_link(self):
        self.element((By.CSS_SELECTOR, "[data-test-id='reply-link']")).click()
        return self

    def get_ticket(self):
        return self.element((By.CSS_SELECTOR, "[data-test-id='ticket-box']"))
