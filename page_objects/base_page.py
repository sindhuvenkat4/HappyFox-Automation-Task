from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    url = None
    WAIT_TIMEOUT = 15

    def __init__(self, driver):
        self.driver = driver

    def go(self):
        self.driver.get(self.url)

    def wait(self, condition, timeout):
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(condition)

    def wait_for_relative_element(self, element, condition, timeout):
        wait = WebDriverWait(element, timeout)
        return wait.until(condition)

    def element(self, locator) -> WebElement:
        return self.wait(EC.element_to_be_clickable(locator), BasePage.WAIT_TIMEOUT)

    def dom_element(self, locator) -> WebElement:
        using, value = locator
        return self.driver.find_element(using, value)

    def elements(self, locator):
        return self.wait(EC.visibility_of_all_elements_located(locator), BasePage.WAIT_TIMEOUT)

    def wait_for_stale(self, element):
        return self.wait(EC.staleness_of(element), BasePage.WAIT_TIMEOUT)

    def wait_for_invisibility_of_element_located_by(self, locator, wait_timeout=WAIT_TIMEOUT):
        return self.wait(EC.invisibility_of_element_located(locator), wait_timeout)

    def wait_for_all_ajax_to_complete(self):
        # Wait up to 10 seconds for all AJAX requests to finish
        WebDriverWait(self.driver, 15).until(lambda driver:  self.ajax_complete())

    def inject_JS_to_track_activeXHRs(self):
        # Define a JavaScript function that counts the active XMLHttpRequests and stores it in window.activeXHRs
        js_script = """
        var oldSend, i;
        if (window.activeXHRs === undefined) {
            window.activeXHRs = 0;
            oldSend = XMLHttpRequest.prototype.send;
            XMLHttpRequest.prototype.send = function() {
                window.activeXHRs++;
                this.addEventListener('readystatechange', function() {
                    if(this.readyState == 4) {
                        window.activeXHRs--;
                    }
                }, false);
                oldSend.apply(this, arguments);
            };
        }
        """
        # Execute the JavaScript function once before waiting for AJAX requests
        self.driver.execute_script(js_script)

    # Define a custom wait function that returns True when all XMLHttpRequests are complete
    def ajax_complete(self):
        try:
            return 0 == self.driver.execute_script("return window.activeXHRs")
        except Exception:
            # In case there is no window.activeXHRs defined
            pass

    def navigate_to_page_from_nav_bar(self, link_text):
        self.element((By.CSS_SELECTOR, "[data-test-id='module-switcher_trigger']")).click()
        self.element((By.LINK_TEXT, link_text)).click()

    def logout(self):
        self.element((By.CSS_SELECTOR, "[data-test-id='staff-profile-image']")).click()
        self.element((By.LINK_TEXT, "Logout")).click()
        assert self.element((By.CSS_SELECTOR, ".confirmation")).is_displayed()
