from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver


class BasePage:
    url = None

    def __init__(self, driver):
        self.driver = driver

    def go(self):
        self.driver.get(self.url)

    def wait_until(self, condition, timeout):
        wait = WebDriverWait(self.driver, timeout)
        wait.until(condition)

    def wait_for_all_ajax_to_complete(self):
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

        # Wait up to 10 seconds for all AJAX requests to finish
        WebDriverWait(self.driver, 10).until(self.ajax_complete)

    # Define a custom wait function that returns True when all XMLHttpRequests are complete
    def ajax_complete(self):
        try:
            return 0 == self.driver.execute_script("return window.activeXHRs")
        except Exception:
            # In case there is no window.activeXHRs defined
            pass
